"""Sharpening layers for expected-K rankings.

1. Pitcher pitch-mix vs LHB / RHB (Statcast pitch-level)
2. Batter pitch-type K% vs LHP / RHP (Statcast PA endings)
3. Batter overall K% vs pitcher hand (Stats API vl/vr splits)
4. Recent-form overlay from last 3 starts
5. Outing-risk flags from BB/9, HR/9, xFIP
6. Outing survival / early-exit haircut (BB + short recent IP + HR/xFIP)
7. Opposing lineup K% / contact form overlay on expected Ks
8. Ticket outlook — soft-contact FILLER profile gated by opposing
   lineup arsenal rank (expected_k_pct vs slate)
9. Pitcher stuff ceiling — own velo/whiff by pitch → SPIKE caution
   (does not change expected_ks; blocks soft-under autopilot)

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

# Pitcher-own stuff ceiling (usage-weighted whiff / primary FB velo).
# Display + SPIKE gate only — never blended into expected_ks.
STUFF_WHIFF_ELITE = 30.0
STUFF_WHIFF_STRONG = 26.0
STUFF_WHIFF_AVG = 22.0
SPIKE_K9 = 10.0
SPIKE_STUFF_WHIFF = 28.0
SPIKE_STUFF_WHIFF_WITH_VELO = 26.0
SPIKE_FB_VELO = 95.0

# Total-trust / under-confirm gates (ticket sizing — do not move expected_ks).
# ELITE/STRONG + high Exp K only trusts the *total* when STYLE is WHIFF (8/4 Dobbins/Tidwell).
TRUST_TOTAL_EXP_KS = 5.5
# Soft under needs ≥2 of: GB/FLY style, contact_heavy BIP, Exp K ≤ floor (8/4 Dobnak/Assad).
UNDER_CONFIRM_EXP_KS = 4.2
UNDER_CONFIRM_MIN = 2
FASTBALL_TYPES = ("FF", "SI", "FC", "FT")
WHIFF_DESCS = {
    "swinging_strike",
    "swinging_strike_blocked",
    "foul_tip",
}
SWING_DESCS = WHIFF_DESCS | {
    "foul",
    "foul_bunt",
    "bunt_foul_tip",
    "hit_into_play",
    "foul_pitchout",
    "swinging_pitchout",
}

# Early-exit / survival haircuts (multiplicative on projected BF/IP).
SURVIVAL_FLOOR = 0.82
SHORT_RECENT_IP_HARD = 4.0
SHORT_RECENT_IP_SOFT = 4.75

# Opposing lineup offense overlay (mild ± on matchup expected_ks).
LEAGUE_K_PCT = 22.5
LEAGUE_AVG = 0.245
# Balls in play / PA ≈ (AB − SO) / PA. High BIP = contact-heavy nine.
LEAGUE_BIP_PCT = 68.0
OFFENSE_FACTOR_MAX = 0.07
OFFENSE_RECENT_GAMES = 10
OFFENSE_MIN_RECENT_PA = 25
# Contact environment labels from lineup BIP% (+ K% confirmation).
CONTACT_HEAVY_BIP = 71.0
WHIFF_PRONE_BIP = 64.0

# Plate discipline / pitch-count layer (lineup BB% + K% shape).
LEAGUE_BB_PCT = 8.3
DISCIPLINE_KS_FACTOR_MAX = 0.05  # mild ± on expected_ks
DISCIPLINE_BF_FLOOR = 0.90  # patient lineups can trim up to ~10% BF/IP
PATIENT_BB_PCT = 9.5
FREE_SWING_BB_PCT = 7.0

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


def _pitch_stuff_from_df(df: pd.DataFrame) -> dict[str, dict[str, Any]]:
    """Per-pitch velo + whiff% from a Statcast pitch-detail frame.

    Whiff% = swinging misses / swings (Savant-style). Velo = mean release_speed.
    """
    out: dict[str, dict[str, Any]] = {}
    if df is None or df.empty or "pitch_type" not in df.columns:
        return out
    work = df.copy()
    work["pitch_type"] = work["pitch_type"].astype(str).str.upper()
    work = work[~work["pitch_type"].isin(SKIP_PITCH_TYPES)]
    if work.empty:
        return out
    has_speed = "release_speed" in work.columns
    has_desc = "description" in work.columns
    if has_speed:
        work["release_speed"] = pd.to_numeric(work["release_speed"], errors="coerce")
    if has_desc:
        work["description"] = work["description"].astype(str).str.lower()
    for pt, g in work.groupby("pitch_type"):
        n = int(len(g))
        velo = None
        if has_speed:
            speeds = g["release_speed"].dropna()
            if not speeds.empty:
                velo = float(speeds.mean())
        whiff = None
        if has_desc:
            desc = g["description"]
            swings = int(desc.isin(SWING_DESCS).sum())
            whiffs = int(desc.isin(WHIFF_DESCS).sum())
            if swings > 0:
                whiff = 100.0 * whiffs / swings
        out[str(pt)] = {
            "pitches": n,
            "velo": velo,
            "whiff_percent": whiff,
            "source": "statcast",
        }
    return out


def build_savant_pitcher_stuff(arsenal: pd.DataFrame) -> dict[int, dict[str, dict[str, Any]]]:
    """Index Savant pitcher-arsenal board rows: pid → pitch_type → whiff/usage."""
    out: dict[int, dict[str, dict[str, Any]]] = {}
    if arsenal is None or arsenal.empty:
        return out
    need = {"player_id", "pitch_type"}
    if not need.issubset(set(arsenal.columns)):
        return out
    work = arsenal.copy()
    work["player_id"] = pd.to_numeric(work["player_id"], errors="coerce")
    work = work.dropna(subset=["player_id", "pitch_type"])
    for c in ("whiff_percent", "k_percent", "pitch_usage", "pitches"):
        if c in work.columns:
            work[c] = pd.to_numeric(work[c], errors="coerce")
    for pid, g in work.groupby("player_id"):
        by_pt: dict[str, dict[str, Any]] = {}
        for _, row in g.iterrows():
            pt = str(row["pitch_type"]).upper()
            if pt in SKIP_PITCH_TYPES:
                continue
            by_pt[pt] = {
                "pitch_name": (
                    str(row["pitch_name"])
                    if "pitch_name" in row.index and pd.notna(row.get("pitch_name"))
                    else PITCH_NAMES.get(pt, pt)
                ),
                "whiff_percent": (
                    float(row["whiff_percent"])
                    if "whiff_percent" in row.index and pd.notna(row.get("whiff_percent"))
                    else None
                ),
                "k_percent": (
                    float(row["k_percent"])
                    if "k_percent" in row.index and pd.notna(row.get("k_percent"))
                    else None
                ),
                "pitch_usage": (
                    float(row["pitch_usage"])
                    if "pitch_usage" in row.index and pd.notna(row.get("pitch_usage"))
                    else None
                ),
                "pitches": (
                    float(row["pitches"])
                    if "pitches" in row.index and pd.notna(row.get("pitches"))
                    else None
                ),
                "source": "savant_arsenal",
            }
        if by_pt:
            out[int(pid)] = by_pt
    return out


def fetch_pitcher_hand_mixes(
    pitcher_ids: list[int],
    year: int,
    min_usage: float,
    verbose: bool,
    log: Callable[[bool, str], None],
) -> dict[int, dict[str, Any]]:
    """Per pitcher: usage frames for ALL / L / R plus pitch totals + stuff."""
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
            "pitch_stuff": _pitch_stuff_from_df(df),
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
    savant_stuff: dict[str, dict[str, Any]] | None = None,
) -> list[dict[str, Any]]:
    """Union arsenal rows with overall + vs-L / vs-R usage for display.

    When available, attaches pitcher-own whiff% (Savant preferred) and
    release velo (Statcast) per pitch — ceiling layer only.
    """
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
    sc_stuff = (mixes or {}).get("pitch_stuff") or {}
    savant_stuff = savant_stuff or {}
    rows: list[dict[str, Any]] = []
    for _, row in base.sort_values("usage_frac", ascending=False).iterrows():
        pt = str(row["pitch_type"])
        sav = savant_stuff.get(pt) or savant_stuff.get(pt.upper()) or {}
        sc = sc_stuff.get(pt) or sc_stuff.get(pt.upper()) or {}
        pitcher_whiff = sav.get("whiff_percent")
        if pitcher_whiff is None:
            pitcher_whiff = sc.get("whiff_percent")
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
                "pitcher_whiff_pct": pitcher_whiff,
                "pitcher_velo": sc.get("velo"),
                "pitcher_k_pct": sav.get("k_percent"),
            }
        )
    return rows


def stuff_grade(whiff_pct: float | None) -> str:
    """Absolute grade on pitcher usage-weighted own whiff%."""
    if whiff_pct is None or (isinstance(whiff_pct, float) and pd.isna(whiff_pct)):
        return ""
    w = float(whiff_pct)
    if w >= STUFF_WHIFF_ELITE:
        return "elite"
    if w >= STUFF_WHIFF_STRONG:
        return "strong"
    if w >= STUFF_WHIFF_AVG:
        return "avg"
    return "soft"


def _primary_fb_velo(pitch_stuff: dict[str, dict[str, Any]]) -> tuple[float | None, str]:
    """Pick primary fastball velo: most-thrown among FF/SI/FC/FT with a velo."""
    best_pt = ""
    best_n = -1
    best_velo: float | None = None
    for pt in FASTBALL_TYPES:
        info = pitch_stuff.get(pt) or {}
        velo = info.get("velo")
        if velo is None:
            continue
        n = int(info.get("pitches") or 0)
        if n > best_n:
            best_n = n
            best_velo = float(velo)
            best_pt = pt
    return best_velo, best_pt


def classify_spike_risk(
    *,
    k9: float | None,
    last3_k9: float | None,
    stuff_whiff_pct: float | None,
    stuff_fb_velo: float | None,
) -> tuple[bool, str]:
    """True when pitcher has a high-K ceiling — do not auto soft-under."""
    bits: list[str] = []
    if k9 is not None and float(k9) >= SPIKE_K9:
        bits.append(f"K9 {float(k9):.1f}")
    if last3_k9 is not None and float(last3_k9) >= SPIKE_K9:
        bits.append(f"L3 K9 {float(last3_k9):.1f}")
    if stuff_whiff_pct is not None and float(stuff_whiff_pct) >= SPIKE_STUFF_WHIFF:
        bits.append(f"stuff whiff {float(stuff_whiff_pct):.1f}%")
    elif (
        stuff_whiff_pct is not None
        and stuff_fb_velo is not None
        and float(stuff_whiff_pct) >= SPIKE_STUFF_WHIFF_WITH_VELO
        and float(stuff_fb_velo) >= SPIKE_FB_VELO
    ):
        bits.append(
            f"stuff whiff {float(stuff_whiff_pct):.1f}% + FB {float(stuff_fb_velo):.1f}"
        )
    if not bits:
        return False, ""
    return True, ", ".join(bits)


def apply_pitcher_stuff_overlay(
    df: pd.DataFrame,
    savant_stuff: dict[int, dict[str, dict[str, Any]]],
    hand_mixes: dict[int, dict[str, Any]],
) -> pd.DataFrame:
    """Attach usage-weighted pitcher whiff / FB velo + SPIKE flag.

    Ceiling / caution layer only — does not modify expected_ks.
    """
    out = df.copy()
    for col, default in (
        ("stuff_whiff_pct", pd.NA),
        ("stuff_fb_velo", pd.NA),
        ("stuff_fb_pitch", ""),
        ("stuff_grade", ""),
        ("spike_risk", False),
        ("spike_flags", ""),
        ("stuff_source", ""),
    ):
        if col not in out.columns:
            out[col] = default

    for idx, row in out.iterrows():
        pid_raw = row.get("pitcher_id")
        if pid_raw is None or (isinstance(pid_raw, float) and pd.isna(pid_raw)):
            continue
        try:
            pid = int(pid_raw)
        except (TypeError, ValueError):
            continue

        sav = savant_stuff.get(pid) or {}
        mixes = hand_mixes.get(pid) or {}
        sc_stuff = mixes.get("pitch_stuff") or {}

        # Prefer arsenal / pitch_lineup_avg usage already on the row.
        arsenal_rows = row.get("arsenal") or row.get("pitch_lineup_avg") or []
        if isinstance(arsenal_rows, float) and pd.isna(arsenal_rows):
            arsenal_rows = []
        usage_pairs: list[tuple[str, float]] = []
        if isinstance(arsenal_rows, list) and arsenal_rows:
            for p in arsenal_rows:
                pt = str(p.get("pitch_type") or "").upper()
                frac = p.get("usage_frac")
                if not pt or frac is None:
                    continue
                usage_pairs.append((pt, float(frac)))
        elif mixes.get("usage_all") is not None:
            frame = mixes["usage_all"]
            for _, r in frame.iterrows():
                usage_pairs.append((str(r["pitch_type"]).upper(), float(r["usage_frac"])))

        whiff_num = 0.0
        whiff_den = 0.0
        source_bits: list[str] = []
        for pt, frac in usage_pairs:
            w = None
            src = ""
            if pt in sav and sav[pt].get("whiff_percent") is not None:
                w = float(sav[pt]["whiff_percent"])
                src = "savant"
            elif pt in sc_stuff and sc_stuff[pt].get("whiff_percent") is not None:
                w = float(sc_stuff[pt]["whiff_percent"])
                src = "statcast"
            if w is None:
                continue
            whiff_num += frac * w
            whiff_den += frac
            if src and src not in source_bits:
                source_bits.append(src)

        stuff_whiff = (whiff_num / whiff_den) if whiff_den > 0 else None
        fb_velo, fb_pt = _primary_fb_velo(sc_stuff)

        # Enrich per-pitch display rows in place.
        for key in ("arsenal", "pitch_lineup_avg"):
            pitches = row.get(key)
            if not isinstance(pitches, list) or not pitches:
                continue
            enriched = []
            for p in pitches:
                pt = str(p.get("pitch_type") or "").upper()
                sav_p = sav.get(pt) or {}
                sc_p = sc_stuff.get(pt) or {}
                e = dict(p)
                if e.get("pitcher_whiff_pct") is None:
                    e["pitcher_whiff_pct"] = sav_p.get("whiff_percent")
                    if e["pitcher_whiff_pct"] is None:
                        e["pitcher_whiff_pct"] = sc_p.get("whiff_percent")
                if e.get("pitcher_velo") is None:
                    e["pitcher_velo"] = sc_p.get("velo")
                if e.get("pitcher_k_pct") is None:
                    e["pitcher_k_pct"] = sav_p.get("k_percent")
                enriched.append(e)
            out.at[idx, key] = enriched

        try:
            k9 = (
                float(row["k9"])
                if row.get("k9") is not None and pd.notna(row.get("k9"))
                else None
            )
        except (TypeError, ValueError):
            k9 = None
        try:
            l3k9 = (
                float(row["last3_k9"])
                if row.get("last3_k9") is not None and pd.notna(row.get("last3_k9"))
                else None
            )
        except (TypeError, ValueError):
            l3k9 = None

        spike, spike_flags = classify_spike_risk(
            k9=k9,
            last3_k9=l3k9,
            stuff_whiff_pct=stuff_whiff,
            stuff_fb_velo=fb_velo,
        )
        out.at[idx, "stuff_whiff_pct"] = stuff_whiff
        out.at[idx, "stuff_fb_velo"] = fb_velo
        out.at[idx, "stuff_fb_pitch"] = fb_pt
        out.at[idx, "stuff_grade"] = stuff_grade(stuff_whiff)
        out.at[idx, "spike_risk"] = spike
        out.at[idx, "spike_flags"] = spike_flags
        out.at[idx, "stuff_source"] = "+".join(source_bits) if source_bits else (
            "statcast_velo" if fb_velo is not None else ""
        )
    return out


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


def _fg_float(value: Any) -> float:
    if value is None:
        return float("nan")
    try:
        f = float(value)
    except (TypeError, ValueError):
        return float("nan")
    return f if not pd.isna(f) else float("nan")


def _strike_pct_from_counts(strikes: Any, pitches: Any) -> float:
    """Pitches thrown for strikes / all pitches → 0–100 Strike%."""
    try:
        s = float(strikes)
        p = float(pitches)
    except (TypeError, ValueError):
        return float("nan")
    if pd.isna(s) or pd.isna(p) or p <= 0:
        return float("nan")
    return 100.0 * s / p


def _fg_pct(value: Any) -> float:
    """FanGraphs % fields may be 0–1 proportions or 0–100."""
    if value is None:
        return float("nan")
    try:
        f = float(value)
    except (TypeError, ValueError):
        return float("nan")
    if pd.isna(f):
        return float("nan")
    if 0.0 <= f <= 1.5:
        f *= 100.0
    return f


def fetch_fangraphs_pitching(
    year: int, verbose: bool, log: Callable[[bool, str], None]
) -> dict[int, dict[str, float]]:
    """xFIP / rates / contact profile (K%, Contact%, GB%, FB%, IFFB%) by MLBAM id."""
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
                "pitcher_k_pct": _fg_pct(row.get("K%")),
                "pitcher_contact_pct": _fg_pct(row.get("Contact%")),
                "pitcher_gb_pct": _fg_pct(row.get("GB%")),
                "pitcher_fb_pct": _fg_pct(row.get("FB%")),
                "pitcher_iffb_pct": _fg_pct(row.get("IFFB%")),
                "pitcher_soft_pct": _fg_pct(row.get("Soft%")),
                "strike_pct": _strike_pct_from_counts(
                    row.get("Strikes"), row.get("Pitches")
                ),
                "f_strike_pct": _fg_pct(row.get("F-Strike%")),
                "zone_pct": _fg_pct(row.get("Zone%")),
                "pitches": _fg_float(row.get("Pitches")),
                "strikes": _fg_float(row.get("Strikes")),
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
    """Stats API fallback rates: BB/9, HR/9, K/9 + rough K%/GB% from BIP outs."""
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
                try:
                    bf = float(stat.get("battersFaced") or 0)
                    so = float(stat.get("strikeOuts") or 0)
                    go = float(stat.get("groundOuts") or 0)
                    ao = float(stat.get("airOuts") or 0)
                    strikes = float(stat.get("strikes") or 0)
                    pitches = float(stat.get("numberOfPitches") or 0)
                except (TypeError, ValueError):
                    bf = so = go = ao = strikes = pitches = 0.0
                bip_outs = go + ao
                strike_pct = _fg_pct(stat.get("strikePercentage"))
                if pd.isna(strike_pct):
                    strike_pct = _strike_pct_from_counts(strikes, pitches)
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
                    "pitcher_k_pct": (100.0 * so / bf) if bf > 0 else float("nan"),
                    # Approx GB% of in-play outs (not true batted-ball GB%).
                    "pitcher_gb_pct": (100.0 * go / bip_outs) if bip_outs > 0 else float("nan"),
                    "pitcher_fb_pct": (100.0 * ao / bip_outs) if bip_outs > 0 else float("nan"),
                    "pitcher_contact_pct": float("nan"),
                    "pitcher_iffb_pct": float("nan"),
                    "pitcher_soft_pct": float("nan"),
                    "strike_pct": strike_pct,
                    "f_strike_pct": float("nan"),
                    "zone_pct": float("nan"),
                    "pitches": pitches if pitches > 0 else float("nan"),
                    "strikes": strikes if strikes > 0 else float("nan"),
                }
                break
    return out


# Pitcher out-getting style bands (season profile; confirmation layer).
PITCHER_WHIFF_K = 24.5
PITCHER_WHIFF_CONTACT = 75.0
PITCHER_GB_CONTACT = 48.0
PITCHER_GB_K_MAX = 22.0
PITCHER_FB = 40.0
PITCHER_IFFB = 11.0


def classify_pitcher_style(
    *,
    k_pct: float | None,
    contact_pct: float | None,
    gb_pct: float | None,
    fb_pct: float | None,
    iffb_pct: float | None,
    k9: float | None = None,
) -> tuple[str, str]:
    """Return (style, short flags) for how a pitcher usually gets outs.

    Styles:
      whiff      — strikeout-first
      contact_gb — ground-ball / in-play outs
      fly_popup  — fly-ball + popup (IFFB) tendency
      balanced   — mixed
    """
    bits: list[str] = []
    k = float(k_pct) if k_pct is not None else None
    con = float(contact_pct) if contact_pct is not None else None
    gb = float(gb_pct) if gb_pct is not None else None
    fb = float(fb_pct) if fb_pct is not None else None
    iffb = float(iffb_pct) if iffb_pct is not None else None

    whiff = False
    if k is not None and k >= PITCHER_WHIFF_K:
        whiff = True
        bits.append(f"K% {k:.1f}")
    elif k9 is not None and float(k9) >= 10.0 and (k is None or k >= 23.0):
        whiff = True
        bits.append(f"K9 {float(k9):.1f}")
    if con is not None and con <= PITCHER_WHIFF_CONTACT and whiff:
        bits.append(f"Contact% {con:.1f}")

    gb_style = gb is not None and gb >= PITCHER_GB_CONTACT and (
        k is None or k <= PITCHER_GB_K_MAX
    )
    if gb_style:
        bits.append(f"GB% {gb:.1f}")

    fly_style = (
        fb is not None
        and fb >= PITCHER_FB
        and iffb is not None
        and iffb >= PITCHER_IFFB
    )
    if fly_style:
        bits.append(f"FB% {fb:.1f}")
        bits.append(f"IFFB% {iffb:.1f}")

    # Prefer the dominant identity; whiff wins ties (K props care most).
    if whiff and not gb_style:
        return "whiff", ", ".join(bits)
    if gb_style and not whiff:
        return "contact_gb", ", ".join(bits)
    if fly_style and not whiff:
        return "fly_popup", ", ".join(bits)
    if whiff and gb_style:
        return "whiff", ", ".join(bits)  # K-first even if GB is high
    if bits:
        return "balanced", ", ".join(bits)
    # Enough rate data to call balanced; otherwise leave blank (no chip).
    if k is not None or gb is not None or fb is not None:
        return "balanced", ""
    return "", ""


def merge_risk_metrics(
    pitcher_id: int | None,
    fangraphs: dict[int, dict[str, float]],
    api_rates: dict[int, dict[str, float]],
) -> dict[str, Any]:
    empty = {
        "bb9": None,
        "hr9": None,
        "k9": None,
        "xfip": None,
        "pitcher_k_pct": None,
        "pitcher_contact_pct": None,
        "pitcher_gb_pct": None,
        "pitcher_fb_pct": None,
        "pitcher_iffb_pct": None,
        "pitcher_soft_pct": None,
        "strike_pct": None,
        "f_strike_pct": None,
        "zone_pct": None,
        "pitches": None,
        "strikes": None,
        "pitcher_style": "",
        "pitcher_style_flags": "",
        "risk_source": None,
    }
    if pitcher_id is None:
        return empty
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
    pk = _pick("pitcher_k_pct")
    pc = _pick("pitcher_contact_pct")
    gb = _pick("pitcher_gb_pct")
    fb = _pick("pitcher_fb_pct")
    iffb = _pick("pitcher_iffb_pct")
    soft = _pick("pitcher_soft_pct")
    strike_pct = _pick("strike_pct")
    f_strike_pct = _pick("f_strike_pct")
    zone_pct = _pick("zone_pct")
    pitches = _pick("pitches")
    strikes = _pick("strikes")
    style, style_flags = classify_pitcher_style(
        k_pct=pk,
        contact_pct=pc,
        gb_pct=gb,
        fb_pct=fb,
        iffb_pct=iffb,
        k9=k9,
    )
    source = "fangraphs" if pid in fangraphs else ("statsapi" if pid in api_rates else None)
    return {
        "bb9": bb9,
        "hr9": hr9,
        "k9": k9,
        "xfip": xfip,
        "pitcher_k_pct": pk,
        "pitcher_contact_pct": pc,
        "pitcher_gb_pct": gb,
        "pitcher_fb_pct": fb,
        "pitcher_iffb_pct": iffb,
        "pitcher_soft_pct": soft,
        "strike_pct": strike_pct,
        "f_strike_pct": f_strike_pct,
        "zone_pct": zone_pct,
        "pitches": pitches,
        "strikes": strikes,
        "pitcher_style": style,
        "pitcher_style_flags": style_flags,
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


def _bip_pct(ab: float | None, so: float | None, pa: float | None) -> float | None:
    """Balls-in-play % of PA ≈ (AB − SO) / PA."""
    try:
        ab_f = float(ab or 0.0)
        so_f = float(so or 0.0)
        pa_f = float(pa or 0.0)
    except (TypeError, ValueError):
        return None
    if pa_f <= 0:
        return None
    bip = max(0.0, ab_f - min(so_f, ab_f))
    return 100.0 * bip / pa_f


def fetch_batter_offense_profiles(
    batter_ids: list[int],
    year: int,
    verbose: bool,
    log: Callable[[bool, str], None],
) -> dict[int, dict[str, Any]]:
    """Season + recent K%/AVG/BB%/BIP% for offense + discipline overlays."""
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
            season_k = season_avg = season_pa = season_bb = None
            season_ab = season_so = None
            recent_so = recent_ab = recent_h = recent_pa = recent_bb = 0.0
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
                    bb = st.get("baseOnBalls")
                    try:
                        if so is not None and pa not in (None, 0, "0"):
                            season_k = 100.0 * float(so) / float(pa)
                        elif so is not None and ab not in (None, 0, "0"):
                            season_k = 100.0 * float(so) / float(ab)
                        if h is not None and ab not in (None, 0, "0"):
                            season_avg = float(h) / float(ab)
                        if pa is not None:
                            season_pa = float(pa)
                        if ab is not None:
                            season_ab = float(ab)
                        if so is not None:
                            season_so = float(so)
                        if bb is not None and pa not in (None, 0, "0"):
                            season_bb = 100.0 * float(bb) / float(pa)
                    except (TypeError, ValueError, ZeroDivisionError):
                        pass
                elif typ in ("game log", "gamelog"):
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
                                    "bb": float(st.get("baseOnBalls") or 0),
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
                        recent_bb += g["bb"]
                        recent_pa += g["pa"]
            recent_k = (
                100.0 * recent_so / recent_pa if recent_pa > 0 else None
            )
            recent_avg = recent_h / recent_ab if recent_ab > 0 else None
            recent_bb_pct = (
                100.0 * recent_bb / recent_pa if recent_pa > 0 else None
            )
            out[int(pid)] = {
                "season_k_pct": season_k,
                "season_avg": season_avg,
                "season_pa": season_pa,
                "season_ab": season_ab,
                "season_so": season_so,
                "season_bb_pct": season_bb,
                "season_bip_pct": _bip_pct(season_ab, season_so, season_pa),
                "recent_k_pct": recent_k,
                "recent_avg": recent_avg,
                "recent_pa": recent_pa,
                "recent_ab": recent_ab,
                "recent_so": recent_so,
                "recent_bb_pct": recent_bb_pct,
                "recent_bip_pct": _bip_pct(recent_ab, recent_so, recent_pa),
            }
    return out


def classify_contact_grade(
    bip_pct: float | None, k_pct: float | None
) -> str:
    """Label lineup contact environment from BIP% (+ K% confirm)."""
    if bip_pct is None:
        return ""
    bip = float(bip_pct)
    k = float(k_pct) if k_pct is not None else LEAGUE_K_PCT
    if bip >= CONTACT_HEAVY_BIP or (bip >= 69.0 and k <= 19.5):
        return "contact_heavy"
    if bip <= WHIFF_PRONE_BIP or (bip <= 66.0 and k >= 25.0):
        return "whiff_prone"
    return "neutral"


def summarize_lineup_offense(
    lineup: list[dict[str, Any]],
    profiles: dict[int, dict[str, Any]],
) -> dict[str, Any]:
    """PA-weighted lineup K% / AVG / BB% / BIP%; prefer recent when sample OK."""
    # rows: pa, k, avg, bb, bip
    recent_rows: list[tuple[float, float, float, float, float]] = []
    season_rows: list[tuple[float, float, float, float, float]] = []
    for slot in lineup:
        try:
            bid = int(slot["batter_id"])
        except (KeyError, TypeError, ValueError):
            continue
        prof = profiles.get(bid) or {}
        r_pa = float(prof.get("recent_pa") or 0.0)
        r_k = prof.get("recent_k_pct")
        r_avg = prof.get("recent_avg")
        r_bb = prof.get("recent_bb_pct")
        r_bip = prof.get("recent_bip_pct")
        if r_pa > 0 and r_k is not None:
            recent_rows.append(
                (
                    r_pa,
                    float(r_k),
                    float(r_avg) if r_avg is not None else LEAGUE_AVG,
                    float(r_bb) if r_bb is not None else LEAGUE_BB_PCT,
                    float(r_bip) if r_bip is not None else LEAGUE_BIP_PCT,
                )
            )
        s_pa = float(prof.get("season_pa") or 0.0) or 1.0
        s_k = prof.get("season_k_pct")
        s_avg = prof.get("season_avg")
        s_bb = prof.get("season_bb_pct")
        s_bip = prof.get("season_bip_pct")
        if s_k is not None:
            season_rows.append(
                (
                    s_pa,
                    float(s_k),
                    float(s_avg) if s_avg is not None else LEAGUE_AVG,
                    float(s_bb) if s_bb is not None else LEAGUE_BB_PCT,
                    float(s_bip) if s_bip is not None else LEAGUE_BIP_PCT,
                )
            )

    def _wavg(
        rows: list[tuple[float, float, float, float, float]],
    ) -> tuple[float | None, float | None, float | None, float | None, float]:
        if not rows:
            return None, None, None, None, 0.0
        tw = sum(r[0] for r in rows)
        if tw <= 0:
            return None, None, None, None, 0.0
        k = sum(r[0] * r[1] for r in rows) / tw
        avg = sum(r[0] * r[2] for r in rows) / tw
        bb = sum(r[0] * r[3] for r in rows) / tw
        bip = sum(r[0] * r[4] for r in rows) / tw
        return k, avg, bb, bip, tw

    recent_pa_total = sum(r[0] for r in recent_rows)
    if recent_pa_total >= OFFENSE_MIN_RECENT_PA and recent_rows:
        k_pct, avg, bb_pct, bip_pct, pa = _wavg(recent_rows)
        source = "recent"
        n = len(recent_rows)
    elif season_rows:
        k_pct, avg, bb_pct, bip_pct, pa = _wavg(season_rows)
        source = "season"
        n = len(season_rows)
    else:
        return {
            "lineup_k_pct": None,
            "lineup_avg": None,
            "lineup_bb_pct": None,
            "lineup_bip_pct": None,
            "contact_grade": "",
            "offense_pa": 0.0,
            "offense_source": None,
            "offense_n": 0,
            "discipline_grade": None,
        }

    grade = classify_discipline_grade(bb_pct, k_pct)
    contact = classify_contact_grade(bip_pct, k_pct)
    return {
        "lineup_k_pct": k_pct,
        "lineup_avg": avg,
        "lineup_bb_pct": bb_pct,
        "lineup_bip_pct": bip_pct,
        "contact_grade": contact,
        "offense_pa": pa,
        "offense_source": source,
        "offense_n": n,
        "discipline_grade": grade,
    }


def classify_discipline_grade(
    bb_pct: float | None, k_pct: float | None
) -> str | None:
    """Label opposing lineup plate approach from BB% + K% shape."""
    if bb_pct is None:
        return None
    bb = float(bb_pct)
    k = float(k_pct) if k_pct is not None else LEAGUE_K_PCT
    if bb >= PATIENT_BB_PCT and k >= 25.0:
        return "three_true"  # walks + whiffs — pitch-count heavy but still Ks
    if bb >= PATIENT_BB_PCT and k <= 23.0:
        return "patient"  # true discipline — dangerous for K overs / pitch counts
    if bb >= 10.0:
        return "patient"
    if bb <= FREE_SWING_BB_PCT and k >= 24.0:
        return "free_swing"
    if bb <= FREE_SWING_BB_PCT:
        return "aggressive"
    return "neutral"


def apply_lineup_offense_overlay(
    expected_ks: float,
    summary: dict[str, Any] | None,
) -> tuple[float, float | None, dict[str, Any]]:
    """Mild ± adjust matchup Ks from opposing lineup K% / BIP contact.

    Higher lineup K% → more pitcher Ks.
    Higher balls-in-play % (contact-heavy nine) → fewer pitcher Ks.
    AVG remains a small secondary contact cue. Capped at ±OFFENSE_FACTOR_MAX.
    """
    empty = {
        "lineup_k_pct": None,
        "lineup_avg": None,
        "lineup_bb_pct": None,
        "lineup_bip_pct": None,
        "contact_grade": "",
        "offense_source": None,
        "offense_factor": None,
        "discipline_grade": None,
    }
    if expected_ks is None or summary is None:
        return expected_ks, None, empty
    k_pct = summary.get("lineup_k_pct")
    avg = summary.get("lineup_avg")
    bip_pct = summary.get("lineup_bip_pct")
    if k_pct is None:
        return expected_ks, None, {
            **empty,
            "lineup_bb_pct": summary.get("lineup_bb_pct"),
            "lineup_bip_pct": summary.get("lineup_bip_pct"),
            "contact_grade": summary.get("contact_grade") or "",
            "discipline_grade": summary.get("discipline_grade"),
            "offense_source": summary.get("offense_source"),
        }

    # Whiff-prone lineups boost Ks; contact/BIP-heavy lineups trim them.
    k_edge = (float(k_pct) - LEAGUE_K_PCT) / 100.0
    bip_edge = 0.0
    if bip_pct is not None:
        bip_edge = -(float(bip_pct) - LEAGUE_BIP_PCT) / 100.0
    avg_edge = 0.0
    if avg is not None:
        avg_edge = -(float(avg) - LEAGUE_AVG) * 0.25
    raw = (k_edge * 1.05) + (bip_edge * 0.90) + avg_edge
    delta = max(-OFFENSE_FACTOR_MAX, min(OFFENSE_FACTOR_MAX, raw))
    factor = 1.0 + delta
    blended = float(expected_ks) * factor
    contact = summary.get("contact_grade") or classify_contact_grade(
        float(bip_pct) if bip_pct is not None else None, float(k_pct)
    )
    meta = {
        "lineup_k_pct": float(k_pct),
        "lineup_avg": None if avg is None else float(avg),
        "lineup_bb_pct": summary.get("lineup_bb_pct"),
        "lineup_bip_pct": None if bip_pct is None else float(bip_pct),
        "contact_grade": contact,
        "offense_source": summary.get("offense_source"),
        "offense_factor": factor,
        "offense_pa": summary.get("offense_pa"),
        "offense_n": summary.get("offense_n"),
        "discipline_grade": summary.get("discipline_grade"),
    }
    return blended, factor, meta


def apply_lineup_discipline_overlay(
    expected_ks: float,
    projected_bf: float,
    projected_ip: float,
    summary: dict[str, Any] | None,
) -> tuple[float, float, float, dict[str, Any]]:
    """Haircut Ks + outing length when the opposing nine is patient / walk-heavy.

    High lineup BB% → longer PAs / pitch counts → earlier hooks and fewer K
    opportunities beyond what raw batter K% already captures. Returns adjusted
    expected_ks, projected_bf, projected_ip, and discipline meta.
    """
    empty = {
        "lineup_bb_pct": None,
        "discipline_grade": None,
        "discipline_ks_factor": None,
        "discipline_bf_factor": None,
        "pitch_count_risk": None,
    }
    if summary is None:
        return expected_ks, projected_bf, projected_ip, empty
    bb_pct = summary.get("lineup_bb_pct")
    k_pct = summary.get("lineup_k_pct")
    grade = summary.get("discipline_grade") or classify_discipline_grade(bb_pct, k_pct)
    if bb_pct is None:
        return expected_ks, projected_bf, projected_ip, {
            **empty,
            "discipline_grade": grade,
        }

    bb = float(bb_pct)
    bb_edge = (bb - LEAGUE_BB_PCT) / 100.0  # + = more walks than league

    # K overlay: patient / walk-heavy softens Ks; free-swingers nudge up slightly.
    if grade == "patient":
        ks_raw = -bb_edge * 1.35 - 0.015
    elif grade == "three_true":
        ks_raw = -bb_edge * 0.55  # still whiff; lighter K haircut
    elif grade in ("free_swing", "aggressive"):
        ks_raw = -bb_edge * 0.80  # low BB → slight K bump when bb_edge negative
    else:
        ks_raw = -bb_edge * 0.90
    ks_delta = max(-DISCIPLINE_KS_FACTOR_MAX, min(DISCIPLINE_KS_FACTOR_MAX, ks_raw))
    ks_factor = 1.0 + ks_delta

    # Pitch-count / survival: only haircut when BB% is elevated.
    if bb >= PATIENT_BB_PCT:
        trim = min(1.0 - DISCIPLINE_BF_FLOOR, max(0.0, (bb - LEAGUE_BB_PCT) * 0.012))
        if grade == "three_true":
            trim *= 0.75
        bf_factor = max(DISCIPLINE_BF_FLOOR, 1.0 - trim)
        pitch_risk = "high" if bf_factor <= 0.93 else "elevated"
    elif bb >= LEAGUE_BB_PCT + 0.6:
        bf_factor = max(0.96, 1.0 - (bb - LEAGUE_BB_PCT) * 0.008)
        pitch_risk = "mild"
    else:
        bf_factor = 1.0
        pitch_risk = "low" if grade in ("free_swing", "aggressive") else "neutral"

    new_ks = float(expected_ks) * ks_factor
    new_bf = float(projected_bf) * bf_factor
    new_ip = float(projected_ip) * bf_factor
    meta = {
        "lineup_bb_pct": bb,
        "lineup_k_pct": None if k_pct is None else float(k_pct),
        "discipline_grade": grade,
        "discipline_ks_factor": ks_factor,
        "discipline_bf_factor": bf_factor,
        "pitch_count_risk": pitch_risk,
    }
    return new_ks, new_bf, new_ip, meta


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


# Soft-contact / low-K volume profile (Montero-style). Pitcher-side only;
# final ticket_outlook also needs opposing arsenal matchup rank.
FILLER_K9_MAX = 7.2
FILLER_L3_SOFT = 4.5
FILLER_XFIP_SOFT = 4.3
# Arsenal matchup (slate-relative): percentile of expected_k_pct among today's arms.
# Useful for "who's best on the slate" — NOT the solo pitcher-vs-lineup read.
MATCHUP_STRONG_PCT = 0.65  # >= 65th pct of slate expected_k_pct
MATCHUP_ELITE_PCT = 0.80
MATCHUP_SOFT_PCT = 0.40  # below = soft matchup → hard FILLER

# Absolute arsenal-vs-THIS-lineup bands on expected_k_pct (does not depend on slate size).
# This is the solo quality read: how vulnerable is this nine to this pitcher's mix.
ABS_MATCHUP_ELITE = 24.0   # clear plus vs this nine
ABS_MATCHUP_STRONG = 22.5  # at/above league K% (LEAGUE_K_PCT)
ABS_MATCHUP_AVG = 20.0     # playable mid; below = soft


def absolute_matchup_grade(expected_k_pct: float | None) -> str:
    """Solo arsenal-vs-lineup grade from absolute expected_k_pct bands."""
    if expected_k_pct is None or (isinstance(expected_k_pct, float) and pd.isna(expected_k_pct)):
        return ""
    k = float(expected_k_pct)
    if k >= ABS_MATCHUP_ELITE:
        return "elite"
    if k >= ABS_MATCHUP_STRONG:
        return "strong"
    if k >= ABS_MATCHUP_AVG:
        return "avg"
    return "soft"


def soft_contact_profile(row: dict[str, Any]) -> tuple[bool, str]:
    """True when pitcher looks like a soft-contact / low-K volume arm.

    Flags: K9 ≲ 7, soft last-3 Ks, and/or elevated xFIP. Does not look at
    the opposing lineup — pair with arsenal matchup rank for outlook.
    """
    try:
        k9 = float(row["k9"]) if row.get("k9") is not None and pd.notna(row.get("k9")) else None
    except (TypeError, ValueError):
        k9 = None
    try:
        l3 = (
            float(row["last3_ks"])
            if row.get("last3_ks") is not None and pd.notna(row.get("last3_ks"))
            else None
        )
    except (TypeError, ValueError):
        l3 = None
    try:
        xfip = (
            float(row["xfip"])
            if row.get("xfip") is not None and pd.notna(row.get("xfip"))
            else None
        )
    except (TypeError, ValueError):
        xfip = None
    flags = str(row.get("risk_flags") or "")
    elev_xfip = ("elev_xfip" in flags) or (
        xfip is not None and xfip >= FILLER_XFIP_SOFT
    )
    soft_l3 = l3 is not None and l3 <= FILLER_L3_SOFT
    low_k9 = k9 is not None and k9 <= FILLER_K9_MAX
    if not low_k9:
        return False, ""
    bits: list[str] = [f"K9 {k9:.1f}"]
    if soft_l3:
        bits.append(f"soft L3 {l3:.1f}")
    if elev_xfip and xfip is not None:
        bits.append(f"elev_xFIP {xfip:.2f}")
    # Need soft recent Ks and/or elev xFIP — pure mid-K9 with hot L3 is not FILLER.
    if soft_l3 or elev_xfip:
        return True, ", ".join(bits)
    if k9 <= 7.0 and (l3 is None or l3 <= 5.5):
        return True, ", ".join(bits + ["low-K volume"])
    return False, ""


def _under_confirm_bits(row: dict[str, Any], exp_ks: float | None) -> tuple[int, list[str]]:
    """Count soft-under confirmation signals (need ≥ UNDER_CONFIRM_MIN)."""
    bits: list[str] = []
    pstyle = str(row.get("pitcher_style") or "").strip().lower()
    contact = str(row.get("contact_grade") or "").strip().lower()
    if pstyle in ("contact_gb", "fly_popup"):
        bits.append("GB/FLY style")
    if contact == "contact_heavy":
        bits.append("opp contact-heavy BIP")
    if exp_ks is not None and exp_ks <= UNDER_CONFIRM_EXP_KS:
        bits.append(f"Exp K ≤{UNDER_CONFIRM_EXP_KS:g}")
    return len(bits), bits


def apply_ticket_outlook(df: pd.DataFrame) -> pd.DataFrame:
    """Label FILLER / MATCHUP_OK / SPIKE / THIN_TOTAL / UNDER_OK for tickets.

    Primary matchup read is **absolute** `expected_k_pct` vs this nine
    (`arsenal_abs_grade`) — elite/strong/avg/soft bands that do not depend on
    who else is starting today. Slate rank/percentile (`arsenal_matchup_rank`,
    `matchup_grade`) stay as secondary "today's relative" context.

    - FILLER: soft-contact profile AND absolute matchup not strong → pass / O3.5
    - MATCHUP_OK: soft-contact profile BUT absolute arsenal vs lineup is
      strong/elite → disclose; soft O3.5 / thin O4.5 only, never nuke
    - THIN_TOTAL: ELITE/STRONG + high Exp K but STYLE not WHIFF → thin overs only
      (do not trust the juiced total; 8/4 Dobbins/Tidwell)
    - UNDER_OK: SOFT non-SPIKE with ≥2 under confirms (GB/FLY, contact-heavy,
      Exp K ≤ floor) → preferred soft-under lane (8/4 Dobnak/Assad)
    - SPIKE: soft solo + stuff ceiling → no soft U6
    - (blank): normal process arm
    """
    out = df.copy()
    for col, default in (
        ("soft_contact_profile", False),
        ("profile_flags", ""),
        ("arsenal_matchup_rank", pd.NA),
        ("arsenal_matchup_pctile", pd.NA),
        ("matchup_grade", ""),
        ("arsenal_abs_grade", ""),
        ("arsenal_vs_league", pd.NA),
        ("arsenal_vs_opp", pd.NA),
        ("ticket_outlook", ""),
        ("ticket_note", ""),
        ("under_confirm_n", pd.NA),
        ("total_trust", ""),
    ):
        if col not in out.columns:
            out[col] = default

    scored = out["status"].eq("ok") & out["expected_k_pct"].notna()
    n = int(scored.sum())
    if n == 0:
        return out

    # Rank 1 = highest arsenal K% vs opposing lineup on this slate (relative only).
    ranks = out.loc[scored, "expected_k_pct"].rank(ascending=False, method="min")
    out.loc[scored, "arsenal_matchup_rank"] = ranks.astype(int)
    # Percentile 1.0 = best matchup on slate.
    pctile = out.loc[scored, "expected_k_pct"].rank(pct=True, method="average")
    out.loc[scored, "arsenal_matchup_pctile"] = pctile

    for idx in out.index[scored]:
        row = out.loc[idx]
        soft, profile_flags = soft_contact_profile(row.to_dict())
        out.at[idx, "soft_contact_profile"] = soft
        out.at[idx, "profile_flags"] = profile_flags
        p = float(row["arsenal_matchup_pctile"])
        if p >= MATCHUP_ELITE_PCT:
            slate_grade = "elite"
        elif p >= MATCHUP_STRONG_PCT:
            slate_grade = "strong"
        elif p >= MATCHUP_SOFT_PCT:
            slate_grade = "avg"
        else:
            slate_grade = "soft"
        out.at[idx, "matchup_grade"] = slate_grade

        kpct = float(row["expected_k_pct"])
        abs_grade = absolute_matchup_grade(kpct)
        out.at[idx, "arsenal_abs_grade"] = abs_grade
        vs_league = kpct - LEAGUE_K_PCT
        out.at[idx, "arsenal_vs_league"] = vs_league
        opp_k = row.get("lineup_k_pct")
        vs_opp: float | None = None
        opp_bit = ""
        if opp_k is not None and not (isinstance(opp_k, float) and pd.isna(opp_k)):
            vs_opp = kpct - float(opp_k)
            out.at[idx, "arsenal_vs_opp"] = vs_opp
            opp_bit = f", opp K% {float(opp_k):.1f}"
        ark = int(row["arsenal_matchup_rank"]) if pd.notna(row["arsenal_matchup_rank"]) else "?"
        edge_bit = f", {vs_league:+.1f} vs lg"
        if vs_opp is not None:
            edge_bit += f", {vs_opp:+.1f} vs opp K%"
        # Primary = absolute solo grade; slate #/grade is secondary context.
        matchup_bit = (
            f"arsenal K% {kpct:.1f} ({abs_grade} solo{edge_bit}{opp_bit}; "
            f"slate #{ark}/{n} {slate_grade})"
        )

        spike = bool(row.get("spike_risk"))
        spike_flags = str(row.get("spike_flags") or "").strip()
        stuff_w = row.get("stuff_whiff_pct")
        stuff_g = str(row.get("stuff_grade") or "").strip()
        fb_velo = row.get("stuff_fb_velo")
        exp_ks_raw = row.get("expected_ks")
        exp_ks: float | None = None
        if exp_ks_raw is not None and not (
            isinstance(exp_ks_raw, float) and pd.isna(exp_ks_raw)
        ):
            exp_ks = float(exp_ks_raw)
        stuff_bit = ""
        if stuff_w is not None and not (isinstance(stuff_w, float) and pd.isna(stuff_w)):
            stuff_bit = f"; stuff whiff {float(stuff_w):.1f}%"
            if stuff_g:
                stuff_bit += f" ({stuff_g})"
            if fb_velo is not None and not (
                isinstance(fb_velo, float) and pd.isna(fb_velo)
            ):
                fb_pt = str(row.get("stuff_fb_pitch") or "FB")
                stuff_bit += f", {fb_pt} {float(fb_velo):.1f} mph"
        spike_caveat = ""
        if spike:
            spike_caveat = (
                f"; SPIKE ({spike_flags}) — no soft U6; prefer U6.5+ or pass"
            )

        # Pitcher out-getting style (season K%/Contact%/GB%/FB%/IFFB) — confirmation only.
        pstyle = str(row.get("pitcher_style") or "").strip().lower()
        pflags = str(row.get("pitcher_style_flags") or "").strip()
        style_bit = ""
        style_cue = ""
        if pstyle == "whiff":
            style_bit = f"; pitcher style WHIFF ({pflags or 'K-first'})"
            style_cue = "; K-first arm — confirms overs / SPIKE caution on soft unders"
        elif pstyle == "contact_gb":
            style_bit = f"; pitcher style GB/contact ({pflags or 'in-play outs'})"
            style_cue = (
                "; GB/contact out-getter — soft matchup strengthens under; "
                "elite mix alone is not a nuke over without length"
            )
        elif pstyle == "fly_popup":
            style_bit = f"; pitcher style FLY/popup ({pflags or 'air outs'})"
            style_cue = (
                "; fly/popup out-getter — BIP outs over Ks; same under cue as GB style"
            )
        elif pstyle == "balanced" and pflags:
            style_bit = f"; pitcher style balanced ({pflags})"

        # Total-trust: juiced Exp K on ELITE/STRONG only if STYLE WHIFF.
        # Hard THIN_TOTAL badge = GB/FLY (BIP outs). BAL gets a soft note only
        # (8/4 Manaea BAL cashed; Dobbins GB was the leak).
        total_trust = ""
        trust_cue = ""
        high_total = exp_ks is not None and exp_ks >= TRUST_TOTAL_EXP_KS
        if abs_grade in ("elite", "strong") and high_total:
            if pstyle == "whiff":
                total_trust = "trust"
                trust_cue = (
                    f"; TRUST total — ELITE/STRONG + WHIFF + Exp K "
                    f"{exp_ks:.1f} (≥{TRUST_TOTAL_EXP_KS:g})"
                )
            elif pstyle in ("contact_gb", "fly_popup"):
                total_trust = "thin"
                sty_label = "GB" if pstyle == "contact_gb" else "FLY"
                trust_cue = (
                    f"; THIN total — Exp K {exp_ks:.1f} with STYLE {sty_label} "
                    f"(BIP outs); O3.5 / thin O4.5 only, do not nuke the number"
                )
            elif pstyle == "balanced":
                total_trust = "caution"
                trust_cue = (
                    f"; total caution — Exp K {exp_ks:.1f} with STYLE BAL "
                    f"(not WHIFF); prefer O4.5 floor over juiced O5.5+/O6.5"
                )
        out.at[idx, "total_trust"] = total_trust

        # Soft-under confirmation stack (does not override SPIKE).
        under_n, under_bits = _under_confirm_bits(row.to_dict(), exp_ks)
        out.at[idx, "under_confirm_n"] = under_n
        under_cue = ""
        if abs_grade == "soft" and not spike:
            if under_n >= UNDER_CONFIRM_MIN:
                under_cue = (
                    f"; UNDER_OK — {under_n}/{UNDER_CONFIRM_MIN}+ confirms "
                    f"({', '.join(under_bits)})"
                )
            else:
                need = UNDER_CONFIRM_MIN - under_n
                have = ", ".join(under_bits) if under_bits else "none"
                under_cue = (
                    f"; weak under — only {under_n}/{UNDER_CONFIRM_MIN} confirms "
                    f"({have}); need {need} more of GB/FLY · contact-heavy · "
                    f"Exp K ≤{UNDER_CONFIRM_EXP_KS:g} (or take U6.5+ / pass)"
                )

        role = str(row.get("outing_role") or "starter")
        role_caveat = ""
        if role in ("swingman", "opener_likely", "opener"):
            role_caveat = f"; also {role} — fade full-outing chalk"

        if not soft:
            note = matchup_bit + stuff_bit + style_bit
            # Soft solo matchup + high stuff ceiling = classic false under.
            if abs_grade == "soft" and spike:
                out.at[idx, "ticket_outlook"] = "SPIKE"
                out.at[idx, "ticket_note"] = (
                    f"{note}{spike_caveat} — solo SOFT vs lineup but pitcher "
                    f"stuff/K9 can clear 6+{style_cue}"
                )
            elif abs_grade == "soft" and under_n >= UNDER_CONFIRM_MIN:
                out.at[idx, "ticket_outlook"] = "UNDER_OK"
                out.at[idx, "ticket_note"] = (
                    f"{note}{under_cue}{style_cue}{role_caveat}"
                )
            elif total_trust == "thin":
                out.at[idx, "ticket_outlook"] = "THIN_TOTAL"
                out.at[idx, "ticket_note"] = (
                    note
                    + (f"; stuff ceiling ({spike_flags})" if spike else "")
                    + trust_cue
                    + (style_cue if pstyle in ("contact_gb", "fly_popup", "balanced") else "")
                    + role_caveat
                )
            else:
                # High-stuff overs keep a blank outlook; SPIKE chip still shows.
                out.at[idx, "ticket_outlook"] = ""
                out.at[idx, "ticket_note"] = (
                    note
                    + (f"; stuff ceiling ({spike_flags})" if spike else "")
                    + (style_cue if pstyle == "whiff" and abs_grade in ("elite", "strong") else "")
                    + trust_cue
                    + under_cue
                    + role_caveat
                )
            continue

        # Soft-contact profile path — gate on absolute solo grade.
        if abs_grade in ("elite", "strong"):
            out.at[idx, "ticket_outlook"] = "MATCHUP_OK"
            thin_extra = trust_cue if total_trust == "thin" else ""
            out.at[idx, "ticket_note"] = (
                f"soft-contact profile ({profile_flags}) but {matchup_bit}"
                f"{stuff_bit}{style_bit} — O3.5 / thin O4.5 K only; disclose, not a nuke "
                f"anchor; if skipping Ks, consider pitcher outs when IP/risk holds"
                f"{style_cue}{thin_extra}{role_caveat}"
            )
        else:
            # Soft-contact + soft matchup, but SPIKE stuff → don't sell as locked under.
            if spike:
                out.at[idx, "ticket_outlook"] = "SPIKE"
                out.at[idx, "ticket_note"] = (
                    f"soft-contact ({profile_flags}) + {matchup_bit}{stuff_bit}"
                    f"{style_bit}{spike_caveat}{style_cue}{role_caveat}"
                )
            else:
                # FILLER for K overs, but surface UNDER_OK when BIP/style confirms under.
                if under_n >= UNDER_CONFIRM_MIN:
                    out.at[idx, "ticket_outlook"] = "UNDER_OK"
                    out.at[idx, "ticket_note"] = (
                        f"soft-contact ({profile_flags}) + {matchup_bit}{stuff_bit}"
                        f"{style_bit}{under_cue} — FILLER on K overs (pass/O3.5); "
                        f"under lane preferred when confirms hold; pitcher outs also live "
                        f"if clear/low risk and projected IP holds"
                        f"{style_cue}{role_caveat}"
                    )
                else:
                    out.at[idx, "ticket_outlook"] = "FILLER"
                    out.at[idx, "ticket_note"] = (
                        f"soft-contact ({profile_flags}) + {matchup_bit}{stuff_bit}"
                        f"{style_bit} "
                        f"— FILLER on Ks: pass or O3.5; does not help a K ticket; "
                        f"consider pitcher outs if clear/low risk and projected IP holds"
                        f"{under_cue}{style_cue}{role_caveat}"
                    )
    return out


def strip_html_name(value: Any) -> str:
    if value is None:
        return ""
    return re.sub(r"<[^>]+>", "", str(value)).strip()
