"""Sharpening layers for expected-K rankings.

1. Pitcher pitch-mix vs LHB / RHB (Statcast pitch-level)
2. Batter pitch-type K% vs LHP / RHP (Statcast PA endings)
3. Batter overall K% vs pitcher hand (Stats API vl/vr splits)
4. Recent-form overlay from last 3 starts
5. Outing-risk flags from BB/9, HR/9, xFIP
6. Outing survival / early-exit haircut (BB + short recent IP + HR/xFIP)
7. Opposing lineup K% / contact form overlay on expected Ks

Hits-prop helpers (barrel / hard-hit / xwOBA) live here too but are
display-only — they never modify expected_ks.
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

PEOPLE_HITTING_OFFENSE_URL = (
    "https://statsapi.mlb.com/api/v1/people"
    "?personIds={ids}"
    "&hydrate=stats(group=[hitting],type=[season,gameLog],season={year})"
)

STATCAST_BATTER_URL = (
    "https://baseballsavant.mlb.com/statcast_search/csv"
    "?all=true&hfSea={year}%7C&hfGT=R%7C&player_type=batter"
    "&batters_lookup%5B%5D={batter_id}&min_pitches=1&type=details"
)

SAVANT_BARRELS_URL = (
    "https://baseballsavant.mlb.com/leaderboard/statcast"
    "?type=batter&year={year}&position=&team=&min=1&csv=true"
)
SAVANT_EXPECTED_URL = (
    "https://baseballsavant.mlb.com/leaderboard/expected_statistics"
    "?type=batter&year={year}&position=&team=&filterType=pa&min=1&csv=true"
)

# Ignore non-pitch / rare codes when building mixes.
SKIP_PITCH_TYPES = {"PO", "IN", "AB", "UN", "FA", ""}

MIN_HAND_SPLIT_PITCHES = 80
MIN_PA_PITCH_VS_HAND = 15
FORM_BLEND = 0.30
FORM_MIN_STARTS = 2
PLATOON_FULL_PA = 80
BB9_WARN = 3.5
BB9_HIGH = 4.0
HR9_WARN = 1.20
HR9_HIGH = 1.50
XFIP_WARN = 4.20
XFIP_HIGH = 4.80

# Early-exit / survival haircuts (multiplicative on projected BF/IP).
SURVIVAL_FLOOR = 0.82
SHORT_RECENT_IP_HARD = 4.0
SHORT_RECENT_IP_SOFT = 4.75

# Opposing lineup offense overlay (mild ± on matchup expected_ks).
LEAGUE_K_PCT = 22.5
LEAGUE_AVG = 0.245
OFFENSE_FACTOR_MAX = 0.07
OFFENSE_RECENT_GAMES = 10
OFFENSE_MIN_RECENT_PA = 25

# Hits-prop contact baselines (display-only; not used in expected_ks).
LEAGUE_BARREL_PCT = 8.0
LEAGUE_HARD_HIT_PCT = 40.0
LEAGUE_XWOBA = 0.320
LEAGUE_XBA = 0.250
HITS_AVG_WEIGHT = 0.40
HITS_CONTACT_WEIGHT = 0.35
HITS_EXPECTED_WEIGHT = 0.25
MIN_BIP_CONTACT = 20

K_EVENTS = {"strikeout", "strikeout_double_play"}

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
                "avg_vs_lhp": None,
                "avg_vs_rhp": None,
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
                    avg = None
                    try:
                        ab = float(stat.get("atBats") or 0)
                        h = float(stat.get("hits") or 0)
                        if ab > 0:
                            avg = h / ab
                    except (TypeError, ValueError, ZeroDivisionError):
                        avg = None
                    if code == "vl":
                        entry["k_pct_vs_lhp"] = k_pct
                        entry["pa_vs_lhp"] = pa
                        entry["avg_vs_lhp"] = avg
                    elif code == "vr":
                        entry["k_pct_vs_rhp"] = k_pct
                        entry["pa_vs_rhp"] = pa
                        entry["avg_vs_rhp"] = avg
            out[int(pid)] = entry
    return out


def _pitch_k_rates_from_pa_df(pa_df: pd.DataFrame) -> dict[str, dict[str, float]]:
    """pitch_type -> {k_percent, pa} from PA-ending Statcast rows."""
    if pa_df is None or pa_df.empty:
        return {}
    work = pa_df.copy()
    work["pitch_type"] = work["pitch_type"].astype(str).str.upper()
    work = work[~work["pitch_type"].isin(SKIP_PITCH_TYPES)]
    if work.empty:
        return {}
    events = work["events"].astype(str).str.lower()
    work["is_k"] = events.isin(K_EVENTS)
    out: dict[str, dict[str, float]] = {}
    for pt, g in work.groupby("pitch_type"):
        pa = float(len(g))
        if pa <= 0:
            continue
        k = float(g["is_k"].sum())
        out[str(pt)] = {"k_percent": 100.0 * k / pa, "pa": pa}
    return out


def fetch_batter_pitch_k_vs_hand(
    batter_ids: list[int],
    year: int,
    verbose: bool,
    log: Callable[[bool, str], None],
    *,
    min_pa: int = MIN_PA_PITCH_VS_HAND,
) -> dict[int, dict[str, dict[str, dict[str, float]]]]:
    """True batter K% by pitch_type vs LHP / RHP from Statcast PA endings.

    Returns: batter_id -> {"L"|"R" -> pitch_type -> {k_percent, pa}}
    Only keeps pitch buckets with pa >= min_pa.
    """
    ids = sorted({int(x) for x in batter_ids if x is not None})
    out: dict[int, dict[str, dict[str, dict[str, float]]]] = {}

    def _one(bid: int) -> tuple[int, dict[str, dict[str, dict[str, float]]] | None]:
        url = STATCAST_BATTER_URL.format(year=year, batter_id=bid)
        try:
            resp = _get(url, verbose, log)
            text = resp.content.decode("utf-8-sig")
            if not text.strip() or "pitch_type" not in text.split("\n", 1)[0]:
                return bid, None
            df = pd.read_csv(StringIO(text))
        except Exception as exc:  # noqa: BLE001
            log(verbose, f"batter pitch×hand fetch failed for {bid}: {exc}")
            return bid, None
        if df.empty or "events" not in df.columns or "p_throws" not in df.columns:
            return bid, None
        pa = df[df["events"].notna() & (df["events"].astype(str).str.len() > 0)].copy()
        if pa.empty:
            return bid, None
        pa["p_throws"] = pa["p_throws"].astype(str).str.upper()
        sides: dict[str, dict[str, dict[str, float]]] = {}
        for hand in ("L", "R"):
            rates = _pitch_k_rates_from_pa_df(pa[pa["p_throws"] == hand])
            kept = {
                pt: vals
                for pt, vals in rates.items()
                if float(vals.get("pa") or 0) >= float(min_pa)
            }
            if kept:
                sides[hand] = kept
        return bid, sides or None

    workers = min(10, max(1, len(ids)))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futs = [pool.submit(_one, bid) for bid in ids]
        for fut in as_completed(futs):
            bid, sides = fut.result()
            if sides:
                out[bid] = sides
    log(
        verbose,
        f"batter pitch×hand rates: {len(out)}/{len(ids)} batters with usable splits",
    )
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


def classify_outing_risk(
    bb9: float | None,
    hr9: float | None,
    xfip: float | None,
    form: dict[str, Any] | None = None,
    projected_ip: float | None = None,
) -> dict[str, Any]:
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

    # Survival / early-exit haircut on projected BF/IP (overs care about innings).
    bf_factor = 1.0
    survival_flags: list[str] = []
    if bb9 is not None:
        if bb9 >= BB9_HIGH:
            bf_factor *= 0.90
        elif bb9 >= BB9_WARN:
            bf_factor *= 0.95

    last3_ip = None if not form else form.get("last3_ip")
    try:
        last3_ip_f = float(last3_ip) if last3_ip is not None else None
    except (TypeError, ValueError):
        last3_ip_f = None
    try:
        proj_ip_f = float(projected_ip) if projected_ip is not None else None
    except (TypeError, ValueError):
        proj_ip_f = None

    if last3_ip_f is not None:
        if last3_ip_f < SHORT_RECENT_IP_HARD:
            bf_factor *= 0.93
            survival_flags.append("short_recent_ip")
            score += 1
        elif last3_ip_f < SHORT_RECENT_IP_SOFT and (
            proj_ip_f is None or last3_ip_f < proj_ip_f * 0.80
        ):
            bf_factor *= 0.96
            survival_flags.append("short_recent_ip")

    if hr9 is not None and hr9 >= HR9_HIGH:
        bf_factor *= 0.97
        survival_flags.append("exit_hr")

    if (
        xfip is not None
        and xfip >= XFIP_HIGH
        and bb9 is not None
        and bb9 >= BB9_WARN
    ):
        bf_factor *= 0.97
        survival_flags.append("exit_xfip_bb")

    bf_factor = max(SURVIVAL_FLOOR, min(1.0, bf_factor))

    # Re-tier if survival bumps pushed score.
    if score >= 4:
        level = "high"
    elif score >= 2:
        level = "medium"
    elif score >= 1:
        level = "low"
    else:
        level = "clear"

    all_flags = list(flags)
    for sf in survival_flags:
        if sf not in all_flags:
            all_flags.append(sf)

    return {
        "outing_risk": level,
        "risk_flags": ",".join(all_flags),
        "risk_score": score,
        "bf_risk_factor": bf_factor,
        "survival_flags": ",".join(survival_flags),
    }


def fetch_batter_offense_profiles(
    batter_ids: list[int],
    year: int,
    verbose: bool,
    log: Callable[[bool, str], None],
) -> dict[int, dict[str, Any]]:
    """Season + recent hitting K%/AVG for lineup offense overlays."""
    ids = sorted({int(x) for x in batter_ids if x is not None})
    out: dict[int, dict[str, Any]] = {}
    for i in range(0, len(ids), 25):
        chunk = ids[i : i + 25]
        url = PEOPLE_HITTING_OFFENSE_URL.format(
            ids=",".join(str(x) for x in chunk), year=year
        )
        try:
            payload = _get(url, verbose, log).json()
        except Exception as exc:  # noqa: BLE001
            log(verbose, f"batter offense fetch failed: {exc}")
            continue
        for person in payload.get("people", []):
            pid = person.get("id")
            if pid is None:
                continue
            season_k = season_avg = season_pa = None
            recent_so = recent_ab = recent_h = recent_pa = 0.0
            for block in person.get("stats") or []:
                typ = ((block.get("type") or {}).get("displayName") or "").lower()
                splits = block.get("splits") or []
                if not splits:
                    continue
                if typ == "season":
                    st = splits[0].get("stat") or {}
                    so = st.get("strikeOuts")
                    ab = st.get("atBats")
                    h = st.get("hits")
                    pa = st.get("plateAppearances")
                    try:
                        if so is not None and pa not in (None, 0, "0"):
                            season_k = 100.0 * float(so) / float(pa)
                        elif so is not None and ab not in (None, 0, "0"):
                            season_k = 100.0 * float(so) / float(ab)
                        if h is not None and ab not in (None, 0, "0"):
                            season_avg = float(h) / float(ab)
                        if pa is not None:
                            season_pa = float(pa)
                    except (TypeError, ValueError, ZeroDivisionError):
                        pass
                elif typ in ("game log", "gamelog"):
                    # Splits are chronological; take last N games with AB/PA.
                    games = []
                    for s in splits:
                        st = s.get("stat") or {}
                        try:
                            ab = float(st.get("atBats") or 0)
                            pa = float(st.get("plateAppearances") or ab)
                            if pa <= 0 and ab <= 0:
                                continue
                            games.append(
                                {
                                    "date": str(s.get("date") or ""),
                                    "so": float(st.get("strikeOuts") or 0),
                                    "ab": ab,
                                    "h": float(st.get("hits") or 0),
                                    "pa": pa if pa > 0 else ab,
                                }
                            )
                        except (TypeError, ValueError):
                            continue
                    games.sort(key=lambda g: g["date"])
                    for g in games[-OFFENSE_RECENT_GAMES:]:
                        recent_so += g["so"]
                        recent_ab += g["ab"]
                        recent_h += g["h"]
                        recent_pa += g["pa"]
            recent_k = (
                100.0 * recent_so / recent_pa if recent_pa > 0 else None
            )
            recent_avg = recent_h / recent_ab if recent_ab > 0 else None
            out[int(pid)] = {
                "season_k_pct": season_k,
                "season_avg": season_avg,
                "season_pa": season_pa,
                "recent_k_pct": recent_k,
                "recent_avg": recent_avg,
                "recent_pa": recent_pa,
                "recent_ab": recent_ab,
            }
    return out


def summarize_lineup_offense(
    lineup: list[dict[str, Any]],
    profiles: dict[int, dict[str, Any]],
) -> dict[str, Any]:
    """PA-weighted lineup K% / AVG; prefer recent form when sample is enough."""
    recent_rows: list[tuple[float, float, float]] = []  # pa, k, avg
    season_rows: list[tuple[float, float, float]] = []
    for slot in lineup:
        try:
            bid = int(slot["batter_id"])
        except (KeyError, TypeError, ValueError):
            continue
        prof = profiles.get(bid) or {}
        r_pa = float(prof.get("recent_pa") or 0.0)
        r_k = prof.get("recent_k_pct")
        r_avg = prof.get("recent_avg")
        if r_pa > 0 and r_k is not None:
            recent_rows.append((r_pa, float(r_k), float(r_avg) if r_avg is not None else LEAGUE_AVG))
        s_pa = float(prof.get("season_pa") or 0.0) or 1.0
        s_k = prof.get("season_k_pct")
        s_avg = prof.get("season_avg")
        if s_k is not None:
            season_rows.append(
                (s_pa, float(s_k), float(s_avg) if s_avg is not None else LEAGUE_AVG)
            )

    def _wavg(rows: list[tuple[float, float, float]]) -> tuple[float | None, float | None, float]:
        if not rows:
            return None, None, 0.0
        tw = sum(r[0] for r in rows)
        if tw <= 0:
            return None, None, 0.0
        k = sum(r[0] * r[1] for r in rows) / tw
        avg = sum(r[0] * r[2] for r in rows) / tw
        return k, avg, tw

    recent_pa_total = sum(r[0] for r in recent_rows)
    if recent_pa_total >= OFFENSE_MIN_RECENT_PA and recent_rows:
        k_pct, avg, pa = _wavg(recent_rows)
        source = "recent"
    elif season_rows:
        k_pct, avg, pa = _wavg(season_rows)
        source = "season"
    else:
        return {
            "lineup_k_pct": None,
            "lineup_avg": None,
            "offense_pa": 0.0,
            "offense_source": None,
            "offense_n": 0,
        }

    return {
        "lineup_k_pct": k_pct,
        "lineup_avg": avg,
        "offense_pa": pa,
        "offense_source": source,
        "offense_n": len(recent_rows) if source == "recent" else len(season_rows),
    }


def apply_lineup_offense_overlay(
    expected_ks: float,
    summary: dict[str, Any] | None,
) -> tuple[float, float | None, dict[str, Any]]:
    """Mild ± adjust matchup Ks from opposing lineup K%/contact.

    Higher lineup K% → more pitcher Ks. Higher AVG / contact → fewer Ks.
    Capped at ±OFFENSE_FACTOR_MAX so this stays a sharpening layer.
    """
    empty = {
        "lineup_k_pct": None,
        "lineup_avg": None,
        "offense_source": None,
        "offense_factor": None,
    }
    if expected_ks is None or summary is None:
        return expected_ks, None, empty
    k_pct = summary.get("lineup_k_pct")
    avg = summary.get("lineup_avg")
    if k_pct is None:
        return expected_ks, None, {**empty, **{k: summary.get(k) for k in empty}}

    k_edge = (float(k_pct) - LEAGUE_K_PCT) / 100.0
    contact_edge = 0.0
    if avg is not None:
        # Elevated AVG with soft K% is a contact environment.
        contact_edge = -(float(avg) - LEAGUE_AVG) * 0.55
    raw = (k_edge * 1.15) + contact_edge
    delta = max(-OFFENSE_FACTOR_MAX, min(OFFENSE_FACTOR_MAX, raw))
    factor = 1.0 + delta
    blended = float(expected_ks) * factor
    meta = {
        "lineup_k_pct": float(k_pct),
        "lineup_avg": None if avg is None else float(avg),
        "offense_source": summary.get("offense_source"),
        "offense_factor": factor,
        "offense_pa": summary.get("offense_pa"),
        "offense_n": summary.get("offense_n"),
    }
    return blended, factor, meta


def fetch_batter_contact_quality(
    year: int,
    verbose: bool,
    log: Callable[[bool, str], None],
) -> dict[int, dict[str, Any]]:
    """Season barrel% / hard-hit% / xwOBA from Savant (Hits props only)."""
    out: dict[int, dict[str, Any]] = {}

    def _load(url: str) -> pd.DataFrame | None:
        try:
            resp = _get(url, verbose, log)
            text = resp.content.decode("utf-8-sig")
            if not text.strip():
                return None
            return pd.read_csv(StringIO(text))
        except Exception as exc:  # noqa: BLE001
            log(verbose, f"contact-quality fetch failed ({url}): {exc}")
            return None

    barrels = _load(SAVANT_BARRELS_URL.format(year=year))
    if barrels is not None and not barrels.empty and "player_id" in barrels.columns:
        for _, row in barrels.iterrows():
            try:
                pid = int(row["player_id"])
            except (TypeError, ValueError):
                continue
            entry = out.setdefault(pid, {})
            try:
                bip = float(row["attempts"]) if pd.notna(row.get("attempts")) else None
            except (TypeError, ValueError):
                bip = None
            entry["bip"] = bip
            for src, dst in (
                ("brl_percent", "barrel_pct"),
                ("ev95percent", "hard_hit_pct"),
                ("avg_hit_speed", "avg_ev"),
                ("brl_pa", "barrel_pa_pct"),
            ):
                if src not in row.index or pd.isna(row.get(src)):
                    continue
                try:
                    entry[dst] = float(row[src])
                except (TypeError, ValueError):
                    continue

    expected = _load(SAVANT_EXPECTED_URL.format(year=year))
    if expected is not None and not expected.empty and "player_id" in expected.columns:
        for _, row in expected.iterrows():
            try:
                pid = int(row["player_id"])
            except (TypeError, ValueError):
                continue
            entry = out.setdefault(pid, {})
            for src, dst in (
                ("est_woba", "xwoba"),
                ("est_ba", "xba"),
                ("ba", "ba"),
                ("woba", "woba"),
                ("bip", "bip_expected"),
                ("pa", "pa"),
            ):
                if src not in row.index or pd.isna(row.get(src)):
                    continue
                try:
                    entry[dst] = float(row[src])
                except (TypeError, ValueError):
                    continue
            if entry.get("bip") is None and entry.get("bip_expected") is not None:
                entry["bip"] = entry["bip_expected"]

    return out


def score_batter_hits_props(
    batter_id: int,
    pitcher_hand: str | None,
    *,
    contact: dict[int, dict[str, Any]] | None,
    hand_rates: dict[int, dict[str, Any]] | None,
    offense: dict[int, dict[str, Any]] | None,
) -> dict[str, Any]:
    """Hits / H+R+RBI helper scores. Never used by expected_ks.

    Returns a ~0–100 score where ~50 ≈ league-average quality.
    """
    contact = contact or {}
    hand_rates = hand_rates or {}
    offense = offense or {}
    cq = contact.get(int(batter_id)) or {}
    hr = hand_rates.get(int(batter_id)) or {}
    off = offense.get(int(batter_id)) or {}

    ph = (pitcher_hand or "").upper()
    avg_vs_hand = None
    avg_source = None
    if ph == "L" and hr.get("avg_vs_lhp") is not None:
        avg_vs_hand = float(hr["avg_vs_lhp"])
        avg_source = "vs_lhp"
    elif ph == "R" and hr.get("avg_vs_rhp") is not None:
        avg_vs_hand = float(hr["avg_vs_rhp"])
        avg_source = "vs_rhp"
    elif off.get("recent_avg") is not None:
        avg_vs_hand = float(off["recent_avg"])
        avg_source = "recent"
    elif off.get("season_avg") is not None:
        avg_vs_hand = float(off["season_avg"])
        avg_source = "season"
    elif cq.get("ba") is not None:
        avg_vs_hand = float(cq["ba"])
        avg_source = "savant_ba"

    barrel = cq.get("barrel_pct")
    hard_hit = cq.get("hard_hit_pct")
    xwoba = cq.get("xwoba")
    xba = cq.get("xba")
    bip = cq.get("bip")
    thin = bip is not None and float(bip) < MIN_BIP_CONTACT

    # Component z-ish scores centered at 50.
    def _comp(val: float | None, league: float, scale: float) -> float | None:
        if val is None:
            return None
        return 50.0 + (float(val) - league) / scale * 10.0

    avg_s = _comp(avg_vs_hand, LEAGUE_AVG, 0.040)
    # Contact quality: blend barrel + hard-hit when both exist.
    barrel_s = _comp(None if thin else barrel, LEAGUE_BARREL_PCT, 4.0)
    hard_s = _comp(None if thin else hard_hit, LEAGUE_HARD_HIT_PCT, 8.0)
    if barrel_s is not None and hard_s is not None:
        contact_s = 0.55 * barrel_s + 0.45 * hard_s
    else:
        contact_s = barrel_s if barrel_s is not None else hard_s

    xwoba_s = _comp(None if thin else xwoba, LEAGUE_XWOBA, 0.040)
    xba_s = _comp(None if thin else xba, LEAGUE_XBA, 0.035)
    if xwoba_s is not None and xba_s is not None:
        expected_s = 0.65 * xwoba_s + 0.35 * xba_s
    else:
        expected_s = xwoba_s if xwoba_s is not None else xba_s

    parts: list[tuple[float, float]] = []
    if avg_s is not None:
        parts.append((HITS_AVG_WEIGHT, avg_s))
    if contact_s is not None:
        parts.append((HITS_CONTACT_WEIGHT, contact_s))
    if expected_s is not None:
        parts.append((HITS_EXPECTED_WEIGHT, expected_s))

    hits_score = None
    if parts:
        wsum = sum(w for w, _ in parts)
        hits_score = sum(w * s for w, s in parts) / wsum

    # H+R+RBI leans more on barrel/xwOBA (power + on-base quality).
    hr_rbi_score = None
    power_parts: list[tuple[float, float]] = []
    if contact_s is not None:
        power_parts.append((0.45, contact_s))
    if expected_s is not None:
        power_parts.append((0.35, expected_s))
    if avg_s is not None:
        power_parts.append((0.20, avg_s))
    if power_parts:
        wsum = sum(w for w, _ in power_parts)
        hr_rbi_score = sum(w * s for w, s in power_parts) / wsum

    return {
        "barrel_pct": None if barrel is None else float(barrel),
        "hard_hit_pct": None if hard_hit is None else float(hard_hit),
        "avg_ev": cq.get("avg_ev"),
        "xwoba": None if xwoba is None else float(xwoba),
        "xba": None if xba is None else float(xba),
        "avg_vs_hand": avg_vs_hand,
        "avg_vs_hand_source": avg_source,
        "bip": bip,
        "hits_score": hits_score,
        "hr_rbi_score": hr_rbi_score,
        "hits_thin_sample": bool(thin),
    }


def enrich_lineup_hits_props(
    batter_detail: list[dict[str, Any]],
    pitcher_hand: str | None,
    *,
    contact: dict[int, dict[str, Any]],
    hand_rates: dict[int, dict[str, Any]],
    offense: dict[int, dict[str, Any]],
) -> list[dict[str, Any]]:
    """Attach Hits-prop fields onto batter_detail without touching K fields."""
    for b in batter_detail:
        bid = b.get("batter_id")
        if bid is None:
            continue
        try:
            pid = int(bid)
        except (TypeError, ValueError):
            continue
        scored = score_batter_hits_props(
            pid,
            pitcher_hand,
            contact=contact,
            hand_rates=hand_rates,
            offense=offense,
        )
        # Explicitly do not write expected_k_pct / status used by K model.
        for key, val in scored.items():
            b[key] = val
    return batter_detail


def build_hits_board(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Flat slate of batters ranked by hits_score (separate from pitcher K board)."""
    board: list[dict[str, Any]] = []
    for row in rows:
        if row.get("status") != "ok":
            continue
        for b in row.get("batter_detail") or []:
            if b.get("hits_score") is None:
                continue
            board.append(
                {
                    "batter": b.get("batter"),
                    "batter_id": b.get("batter_id"),
                    "slot": b.get("slot"),
                    "bat_side": b.get("bat_side"),
                    "team": row.get("opponent"),
                    "pitcher": row.get("pitcher"),
                    "pitcher_team": row.get("pitcher_team"),
                    "pitch_hand": row.get("pitch_hand"),
                    "game": row.get("game"),
                    "game_time_ct": row.get("game_time_ct"),
                    "lineup_source": row.get("lineup_source"),
                    "avg_vs_hand": b.get("avg_vs_hand"),
                    "avg_vs_hand_source": b.get("avg_vs_hand_source"),
                    "barrel_pct": b.get("barrel_pct"),
                    "hard_hit_pct": b.get("hard_hit_pct"),
                    "xwoba": b.get("xwoba"),
                    "xba": b.get("xba"),
                    "hits_score": b.get("hits_score"),
                    "hr_rbi_score": b.get("hr_rbi_score"),
                    "hits_thin_sample": b.get("hits_thin_sample"),
                    # K% shown for context only — not an input to hits_score blend beyond display.
                    "expected_k_pct": b.get("expected_k_pct"),
                }
            )
    board.sort(
        key=lambda r: (
            -float(r["hits_score"]),
            -float(r["hr_rbi_score"] or 0),
            str(r.get("batter") or ""),
        )
    )
    for i, r in enumerate(board, 1):
        r["rank"] = i
    return board


def strip_html_name(value: Any) -> str:
    if value is None:
        return ""
    return re.sub(r"<[^>]+>", "", str(value)).strip()
