"""Sharpening layers for expected-K rankings.

1. Pitcher pitch-mix vs LHB / RHB (Statcast pitch-level)
2. Batter K% vs pitcher hand (Stats API vl/vr splits)
3. Recent-form overlay from last 3 starts
4. Outing-risk flags from BB/9, HR/9, xFIP
"""

from __future__ import annotations

import re
from concurrent.futures import ThreadPoolExecutor, as_completed
from io import StringIO
from typing import Any, Callable

import pandas as pd
import requests

USER_AGENT = (
    "mlb-k-matchups/1.0 (+https://github.com; research; contact: local-cli)"
)

STATCAST_PITCHER_URL = (
    "https://baseballsavant.mlb.com/statcast_search/csv"
    "?all=true&hfSea={year}%7C&hfGT=R%7C&player_type=pitcher"
    "&pitchers_lookup%5B%5D={pitcher_id}&min_pitches=1&type=details"
)

FANGRAPHS_PITCHING_URL = (
    "https://www.fangraphs.com/api/leaders/major-league/data"
    "?age=&pos=all&stats=pit&lg=all&qual=0&season={year}&season1={year}"
    "&startdate={year}-01-01&enddate={year}-12-31&month=0&hand=&team=0"
    "&pageitems=2000&pagenum=1&ind=0&rost=0&players=&type=8"
    "&postseason=&sortdir=default&sortstat=WAR"
)

PEOPLE_HITTING_SPLITS_URL = (
    "https://statsapi.mlb.com/api/v1/people"
    "?personIds={ids}"
    "&hydrate=stats(group=[hitting],type=[statSplits],sitCodes=[vl,vr],season={year})"
)

PEOPLE_GAMELOG_URL = (
    "https://statsapi.mlb.com/api/v1/people"
    "?personIds={ids}"
    "&hydrate=stats(group=[pitching],type=[gameLog],season={year})"
)

PEOPLE_SEASON_PITCHING_URL = (
    "https://statsapi.mlb.com/api/v1/people"
    "?personIds={ids}"
    "&hydrate=stats(group=[pitching],type=[season],season={year})"
)

# Ignore non-pitch / rare codes when building mixes.
SKIP_PITCH_TYPES = {"PO", "IN", "AB", "UN", "FA", ""}

MIN_HAND_SPLIT_PITCHES = 80
FORM_BLEND = 0.30
FORM_MIN_STARTS = 2
PLATOON_FULL_PA = 80
BB9_WARN = 3.5
BB9_HIGH = 4.0
HR9_WARN = 1.20
HR9_HIGH = 1.50
XFIP_WARN = 4.20
XFIP_HIGH = 4.80

PITCH_NAMES = {
    "FF": "4-Seam Fastball",
    "SI": "Sinker",
    "FC": "Cutter",
    "SL": "Slider",
    "CH": "Changeup",
    "CU": "Curveball",
    "KC": "Knuckle Curve",
    "FS": "Split-Finger",
    "ST": "Sweeper",
    "SV": "Slurve",
    "KN": "Knuckleball",
    "EP": "Eephus",
    "FO": "Forkball",
    "SC": "Screwball",
}


def _get(url: str, verbose: bool, log: Callable[[bool, str], None]) -> requests.Response:
    log(verbose, f"GET {url}")
    resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=90)
    resp.raise_for_status()
    return resp


def parse_innings_pitched(value: Any) -> float | None:
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    text = str(value).strip()
    if not text:
        return None
    try:
        if "." in text:
            whole, frac = text.split(".", 1)
            return int(whole) + (int(frac) / 3.0)
        return float(text)
    except (TypeError, ValueError):
        return None


def effective_bat_side(bat_side: str | None, pitcher_hand: str | None) -> str | None:
    """Stand used vs this pitcher (switch-hitters take the platoon advantage)."""
    if not bat_side:
        return None
    side = str(bat_side).upper()
    if side == "S":
        ph = (pitcher_hand or "").upper()
        if ph == "L":
            return "R"
        if ph == "R":
            return "L"
        return "R"
    if side in {"L", "R"}:
        return side
    return None


def _usage_frame_from_counts(
    counts: dict[str, int], min_usage: float
) -> pd.DataFrame | None:
    if not counts:
        return None
    total = float(sum(counts.values()))
    if total <= 0:
        return None
    rows = []
    for pt, n in counts.items():
        usage_pct = 100.0 * float(n) / total
        if usage_pct < min_usage:
            continue
        rows.append(
            {
                "pitch_type": pt,
                "pitch_name": PITCH_NAMES.get(pt, pt),
                "pitch_usage": usage_pct,
                "pitches": float(n),
            }
        )
    if not rows:
        return None
    df = pd.DataFrame(rows)
    s = float(df["pitch_usage"].sum())
    if s <= 0:
        return None
    df["usage_frac"] = df["pitch_usage"] / s
    return df.sort_values("usage_frac", ascending=False).reset_index(drop=True)


def _counts_from_pitch_df(df: pd.DataFrame) -> dict[str, dict[str, int]]:
    """Return {ALL|L|R: {pitch_type: count}}."""
    out: dict[str, dict[str, int]] = {"ALL": {}, "L": {}, "R": {}}
    if df is None or df.empty:
        return out
    work = df.copy()
    work["pitch_type"] = work["pitch_type"].astype(str).str.upper()
    work = work[~work["pitch_type"].isin(SKIP_PITCH_TYPES)]
    if "stand" in work.columns:
        work["stand"] = work["stand"].astype(str).str.upper()
    for pt, n in work["pitch_type"].value_counts().items():
        out["ALL"][str(pt)] = int(n)
    if "stand" in work.columns:
        for stand in ("L", "R"):
            sub = work[work["stand"] == stand]
            for pt, n in sub["pitch_type"].value_counts().items():
                out[stand][str(pt)] = int(n)
    return out


def fetch_pitcher_hand_mixes(
    pitcher_ids: list[int],
    year: int,
    min_usage: float,
    verbose: bool,
    log: Callable[[bool, str], None],
) -> dict[int, dict[str, Any]]:
    """Per pitcher: usage frames for ALL / L / R plus pitch totals."""
    ids = sorted({int(x) for x in pitcher_ids if x is not None})
    out: dict[int, dict[str, Any]] = {}

    def _one(pid: int) -> tuple[int, dict[str, Any] | None]:
        url = STATCAST_PITCHER_URL.format(year=year, pitcher_id=pid)
        try:
            resp = _get(url, verbose, log)
            text = resp.content.decode("utf-8-sig")
            if not text.strip() or "pitch_type" not in text.split("\n", 1)[0]:
                return pid, None
            df = pd.read_csv(StringIO(text))
        except Exception as exc:  # noqa: BLE001 - keep slate scoring alive
            log(verbose, f"hand-mix fetch failed for {pid}: {exc}")
            return pid, None
        counts = _counts_from_pitch_df(df)
        mixes: dict[str, Any] = {
            "pitches_all": int(sum(counts["ALL"].values())),
            "pitches_l": int(sum(counts["L"].values())),
            "pitches_r": int(sum(counts["R"].values())),
            "usage_all": _usage_frame_from_counts(counts["ALL"], min_usage),
            "usage_l": None,
            "usage_r": None,
        }
        if mixes["pitches_l"] >= MIN_HAND_SPLIT_PITCHES:
            mixes["usage_l"] = _usage_frame_from_counts(counts["L"], min_usage)
        if mixes["pitches_r"] >= MIN_HAND_SPLIT_PITCHES:
            mixes["usage_r"] = _usage_frame_from_counts(counts["R"], min_usage)
        return pid, mixes

    workers = min(8, max(1, len(ids)))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futs = [pool.submit(_one, pid) for pid in ids]
        for fut in as_completed(futs):
            pid, mixes = fut.result()
            if mixes is not None:
                out[pid] = mixes
    return out


def usage_for_batter_side(
    mixes: dict[str, Any] | None,
    fallback: pd.DataFrame | None,
    bat_side: str | None,
) -> tuple[pd.DataFrame | None, str]:
    """Pick LHB/RHB-specific mix when sample is large enough."""
    if mixes:
        if bat_side == "L" and mixes.get("usage_l") is not None:
            return mixes["usage_l"], "vs_lhb"
        if bat_side == "R" and mixes.get("usage_r") is not None:
            return mixes["usage_r"], "vs_rhb"
        if mixes.get("usage_all") is not None:
            return mixes["usage_all"], "overall_statcast"
    return fallback, "overall_arsenal"


def arsenal_from_mixes(
    mixes: dict[str, Any] | None,
    fallback: pd.DataFrame | None,
) -> list[dict[str, Any]]:
    """Union arsenal rows with overall + vs-L / vs-R usage for display."""
    base = None
    if mixes and mixes.get("usage_all") is not None:
        base = mixes["usage_all"]
    elif fallback is not None:
        base = fallback
    if base is None or base.empty:
        return []

    def _map(frame: pd.DataFrame | None) -> dict[str, float]:
        if frame is None or frame.empty:
            return {}
        return {
            str(r["pitch_type"]): float(r["pitch_usage"])
            for _, r in frame.iterrows()
        }

    l_map = _map(mixes.get("usage_l") if mixes else None)
    r_map = _map(mixes.get("usage_r") if mixes else None)
    rows: list[dict[str, Any]] = []
    for _, row in base.sort_values("usage_frac", ascending=False).iterrows():
        pt = str(row["pitch_type"])
        rows.append(
            {
                "pitch_type": pt,
                "pitch_name": (
                    str(row["pitch_name"])
                    if "pitch_name" in row.index and pd.notna(row.get("pitch_name"))
                    else PITCH_NAMES.get(pt, pt)
                ),
                "usage_pct": float(row["pitch_usage"]),
                "usage_frac": float(row["usage_frac"]),
                "usage_vs_lhb": l_map.get(pt),
                "usage_vs_rhb": r_map.get(pt),
            }
        )
    return rows


def fetch_batter_hand_k_rates(
    batter_ids: list[int],
    year: int,
    verbose: bool,
    log: Callable[[bool, str], None],
) -> dict[int, dict[str, Any]]:
    """K% vs LHP (vl) and vs RHP (vr) keyed by batter id."""
    ids = sorted({int(x) for x in batter_ids if x is not None})
    out: dict[int, dict[str, Any]] = {}
    for i in range(0, len(ids), 40):
        chunk = ids[i : i + 40]
        url = PEOPLE_HITTING_SPLITS_URL.format(
            ids=",".join(str(x) for x in chunk), year=year
        )
        payload = _get(url, verbose, log).json()
        for person in payload.get("people", []):
            pid = person.get("id")
            if pid is None:
                continue
            entry: dict[str, Any] = {
                "k_pct_vs_lhp": None,
                "k_pct_vs_rhp": None,
                "pa_vs_lhp": 0.0,
                "pa_vs_rhp": 0.0,
            }
            for block in person.get("stats") or []:
                for split in block.get("splits") or []:
                    code = ((split.get("split") or {}).get("code") or "").lower()
                    stat = split.get("stat") or {}
                    pa = float(stat.get("plateAppearances") or 0)
                    so = float(stat.get("strikeOuts") or 0)
                    if pa <= 0:
                        continue
                    k_pct = 100.0 * so / pa
                    if code == "vl":
                        entry["k_pct_vs_lhp"] = k_pct
                        entry["pa_vs_lhp"] = pa
                    elif code == "vr":
                        entry["k_pct_vs_rhp"] = k_pct
                        entry["pa_vs_rhp"] = pa
            out[int(pid)] = entry
    return out


def platoon_adjust_k_pct(
    arsenal_k_pct: float,
    batter_rates: dict[str, Any] | None,
    pitcher_hand: str | None,
) -> tuple[float, float | None, str]:
    """Soft multiplicative adjust using batter K% vs pitcher hand."""
    if not batter_rates or not pitcher_hand:
        return arsenal_k_pct, None, "none"
    ph = str(pitcher_hand).upper()
    if ph == "L":
        k_hand = batter_rates.get("k_pct_vs_lhp")
        pa_hand = float(batter_rates.get("pa_vs_lhp") or 0)
        k_other = batter_rates.get("k_pct_vs_rhp")
        pa_other = float(batter_rates.get("pa_vs_rhp") or 0)
        label = "vs_lhp"
    elif ph == "R":
        k_hand = batter_rates.get("k_pct_vs_rhp")
        pa_hand = float(batter_rates.get("pa_vs_rhp") or 0)
        k_other = batter_rates.get("k_pct_vs_lhp")
        pa_other = float(batter_rates.get("pa_vs_lhp") or 0)
        label = "vs_rhp"
    else:
        return arsenal_k_pct, None, "none"

    if k_hand is None or pa_hand < 25:
        return arsenal_k_pct, None, "thin_sample"

    # Baseline = PA-weighted overall from the two split buckets when available.
    if k_other is not None and pa_other > 0:
        overall = (
            (float(k_hand) * pa_hand + float(k_other) * pa_other)
            / (pa_hand + pa_other)
        )
    else:
        overall = float(k_hand)
    if overall <= 0:
        return arsenal_k_pct, None, "none"

    raw_factor = float(k_hand) / overall
    weight = min(1.0, pa_hand / PLATOON_FULL_PA)
    factor = 1.0 + weight * (raw_factor - 1.0)
    # Keep adjustments bounded so thin pitch samples don't explode.
    factor = max(0.75, min(1.30, factor))
    return arsenal_k_pct * factor, factor, label


def fetch_pitcher_recent_form(
    pitcher_ids: list[int],
    year: int,
    verbose: bool,
    log: Callable[[bool, str], None],
    last_n: int = 3,
) -> dict[int, dict[str, Any]]:
    """Last-N starts: avg Ks, K/9, IP."""
    ids = sorted({int(x) for x in pitcher_ids if x is not None})
    out: dict[int, dict[str, Any]] = {}
    for i in range(0, len(ids), 30):
        chunk = ids[i : i + 30]
        url = PEOPLE_GAMELOG_URL.format(
            ids=",".join(str(x) for x in chunk), year=year
        )
        payload = _get(url, verbose, log).json()
        for person in payload.get("people", []):
            pid = person.get("id")
            if pid is None:
                continue
            starts: list[dict[str, Any]] = []
            for block in person.get("stats") or []:
                for split in block.get("splits") or []:
                    stat = split.get("stat") or {}
                    if float(stat.get("gamesStarted") or 0) < 1:
                        continue
                    ip = parse_innings_pitched(stat.get("inningsPitched")) or 0.0
                    so = float(stat.get("strikeOuts") or 0)
                    starts.append(
                        {
                            "date": split.get("date"),
                            "ip": ip,
                            "so": so,
                            "k9": (so * 9.0 / ip) if ip > 0 else None,
                        }
                    )
            # API returns newest last for some payloads; sort by date.
            starts.sort(key=lambda s: str(s.get("date") or ""))
            recent = starts[-last_n:]
            if not recent:
                continue
            ip_sum = sum(float(s["ip"]) for s in recent)
            so_sum = sum(float(s["so"]) for s in recent)
            out[int(pid)] = {
                "last3_gs": len(recent),
                "last3_ks": so_sum / len(recent),
                "last3_ip": ip_sum / len(recent),
                "last3_k9": (so_sum * 9.0 / ip_sum) if ip_sum > 0 else None,
            }
    return out


def apply_recent_form_overlay(
    expected_ks: float,
    projected_ip: float,
    form: dict[str, Any] | None,
) -> tuple[float, float | None, float | None]:
    """Blend model Ks with last-3 K/9 run rate. Returns (blended, form_ks, weight)."""
    if not form or expected_ks is None:
        return expected_ks, None, None
    gs = int(form.get("last3_gs") or 0)
    k9 = form.get("last3_k9")
    if gs < FORM_MIN_STARTS or k9 is None or not projected_ip:
        return expected_ks, None, None
    form_ks = float(k9) / 9.0 * float(projected_ip)
    weight = FORM_BLEND * min(1.0, gs / 3.0)
    blended = (1.0 - weight) * float(expected_ks) + weight * form_ks
    return blended, form_ks, weight


def fetch_fangraphs_pitching(
    year: int, verbose: bool, log: Callable[[bool, str], None]
) -> dict[int, dict[str, float]]:
    """xFIP / BB/9 / HR/9 / K/9 keyed by MLBAM id."""
    url = FANGRAPHS_PITCHING_URL.format(year=year)
    try:
        payload = _get(url, verbose, log).json()
    except Exception as exc:  # noqa: BLE001
        log(verbose, f"FanGraphs fetch failed: {exc}")
        return {}
    out: dict[int, dict[str, float]] = {}
    for row in payload.get("data") or []:
        pid = row.get("xMLBAMID")
        if pid is None:
            continue
        try:
            out[int(pid)] = {
                "xfip": float(row["xFIP"]) if row.get("xFIP") is not None else float("nan"),
                "fip": float(row["FIP"]) if row.get("FIP") is not None else float("nan"),
                "bb9": float(row["BB/9"]) if row.get("BB/9") is not None else float("nan"),
                "hr9": float(row["HR/9"]) if row.get("HR/9") is not None else float("nan"),
                "k9": float(row["K/9"]) if row.get("K/9") is not None else float("nan"),
            }
        except (TypeError, ValueError):
            continue
    return out


def fetch_pitcher_rate_stats(
    pitcher_ids: list[int],
    year: int,
    verbose: bool,
    log: Callable[[bool, str], None],
) -> dict[int, dict[str, float]]:
    """Stats API fallback rates: BB/9, HR/9, K/9."""
    ids = sorted({int(x) for x in pitcher_ids if x is not None})
    out: dict[int, dict[str, float]] = {}
    for i in range(0, len(ids), 40):
        chunk = ids[i : i + 40]
        url = PEOPLE_SEASON_PITCHING_URL.format(
            ids=",".join(str(x) for x in chunk), year=year
        )
        payload = _get(url, verbose, log).json()
        for person in payload.get("people", []):
            pid = person.get("id")
            if pid is None:
                continue
            for block in person.get("stats") or []:
                splits = block.get("splits") or []
                if not splits:
                    continue
                stat = splits[0].get("stat") or {}
                out[int(pid)] = {
                    "bb9": float(stat["walksPer9Inn"])
                    if stat.get("walksPer9Inn") not in (None, "")
                    else float("nan"),
                    "hr9": float(stat["homeRunsPer9"])
                    if stat.get("homeRunsPer9") not in (None, "")
                    else float("nan"),
                    "k9": float(stat["strikeoutsPer9Inn"])
                    if stat.get("strikeoutsPer9Inn") not in (None, "")
                    else float("nan"),
                    "xfip": float("nan"),
                }
                break
    return out


def merge_risk_metrics(
    pitcher_id: int | None,
    fangraphs: dict[int, dict[str, float]],
    api_rates: dict[int, dict[str, float]],
) -> dict[str, Any]:
    if pitcher_id is None:
        return {
            "bb9": None,
            "hr9": None,
            "k9": None,
            "xfip": None,
            "risk_source": None,
        }
    pid = int(pitcher_id)
    fg = fangraphs.get(pid) or {}
    api = api_rates.get(pid) or {}

    def _pick(key: str) -> float | None:
        for src in (fg, api):
            val = src.get(key)
            if val is None:
                continue
            try:
                f = float(val)
            except (TypeError, ValueError):
                continue
            if pd.isna(f):
                continue
            return f
        return None

    bb9 = _pick("bb9")
    hr9 = _pick("hr9")
    k9 = _pick("k9")
    xfip = _pick("xfip")
    source = "fangraphs" if pid in fangraphs else ("statsapi" if pid in api_rates else None)
    return {
        "bb9": bb9,
        "hr9": hr9,
        "k9": k9,
        "xfip": xfip,
        "risk_source": source,
    }


def classify_outing_risk(bb9: float | None, hr9: float | None, xfip: float | None) -> dict[str, Any]:
    flags: list[str] = []
    score = 0
    if bb9 is not None:
        if bb9 >= BB9_HIGH:
            flags.append("high_bb")
            score += 2
        elif bb9 >= BB9_WARN:
            flags.append("elev_bb")
            score += 1
    if hr9 is not None:
        if hr9 >= HR9_HIGH:
            flags.append("high_hr")
            score += 2
        elif hr9 >= HR9_WARN:
            flags.append("elev_hr")
            score += 1
    if xfip is not None:
        if xfip >= XFIP_HIGH:
            flags.append("high_xfip")
            score += 2
        elif xfip >= XFIP_WARN:
            flags.append("elev_xfip")
            score += 1

    if score >= 4:
        level = "high"
    elif score >= 2:
        level = "medium"
    elif score >= 1:
        level = "low"
    else:
        level = "clear"

    # Mild early-exit haircut for walk risk only (overs care about innings).
    bf_factor = 1.0
    if bb9 is not None:
        if bb9 >= BB9_HIGH:
            bf_factor = 0.90
        elif bb9 >= BB9_WARN:
            bf_factor = 0.95

    return {
        "outing_risk": level,
        "risk_flags": ",".join(flags),
        "risk_score": score,
        "bf_risk_factor": bf_factor,
    }


def strip_html_name(value: Any) -> str:
    if value is None:
        return ""
    return re.sub(r"<[^>]+>", "", str(value)).strip()
