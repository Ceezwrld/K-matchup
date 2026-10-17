"""Zone-overlap heat maps: pitcher location vs batter swing/damage.

Pulls Statcast pitch-level ``plate_x`` / ``plate_z`` / Savant ``zone`` for a
starter and each opposing lineup batter, then flags HOT / WARM / COLD pockets:

- **HOT** — pitcher throws there often AND batter damages (xwOBA on BIP)
- **COLD** — pitcher lives there but batter is weak (chase / soft contact)
- **WARM** — middling frequency + solid damage

Also builds a **recent** window (default last 30 days) beside season and tags
agreement (``CONFIRM`` / ``SEASON_ONLY`` / ``RECENT_ONLY`` / ``CONFLICT``) plus
honest **low-sample** FYI flags when BIP / pitch counts are thin.

Display / research only — does **not** change ``expected_ks`` or hits scores.

CLI examples::

    # Full opposing lineup from today's hits board
    python mlb-k-matchups/zone_overlap.py \\
        --hits hits-2026-10-15.csv --pitcher "Griffin Jax"

    # Explicit ids
    python mlb-k-matchups/zone_overlap.py \\
        --pitcher-id 643377 --pitcher-name "Griffin Jax" \\
        --batters "Steven Kwan:680757,José Ramírez:608070"

    # Top N by hits_score from the hits CSV
    python mlb-k-matchups/zone_overlap.py \\
        --hits hits-2026-10-15.csv --pitcher "Gavin Williams" --top 3

    # Season only (skip recent window)
    python mlb-k-matchups/zone_overlap.py \\
        --hits hits-DATE.csv --pitcher "Nick Martinez" --no-recent
"""

from __future__ import annotations

import argparse
import json
import re
from datetime import date, timedelta
from io import StringIO
from pathlib import Path
from typing import Any

import pandas as pd
import requests

USER_AGENT = "mlb-k-matchups/zone-overlap/1.0 (+research)"

STATCAST_PITCHER_URL = (
    "https://baseballsavant.mlb.com/statcast_search/csv"
    "?all=true&hfSea={year}%7C&hfGT=R%7CPO%7CS%7C&player_type=pitcher"
    "&pitchers_lookup%5B%5D={pitcher_id}&min_pitches=1&type=details"
)
STATCAST_BATTER_URL = (
    "https://baseballsavant.mlb.com/statcast_search/csv"
    "?all=true&hfSea={year}%7C&hfGT=R%7CPO%7CS%7C&player_type=batter"
    "&batters_lookup%5B%5D={batter_id}&min_pitches=1&type=details"
)

# Sample / recency thresholds (honest sizing, not vetoes)
DEFAULT_RECENT_DAYS = 30
LOW_BATTER_PITCHES_VS_HAND = 450  # season pitches vs that pitcher hand
LOW_ZONE_BIP = 15  # BIP in a zone before HOT/WARM/COLD is "thin"
LOW_RECENT_PITCHES_VS_HAND = 120
LOW_RECENT_ZONE_BIP = 8
MIN_PITCHER_RECENT_PITCHES = 150  # else keep season throw% only
SEASON_MIN_ZONE_PITCHES = 15
RECENT_MIN_ZONE_PITCHES = 8
SEASON_MIN_BIP_XWOBA = 5
RECENT_MIN_BIP_XWOBA = 3

# Catcher's view labels for Savant zones 1–9 / 11–14
ZONE_LABEL = {
    1: "HI-IN (3B)",
    2: "HI-MID",
    3: "HI-AWAY (1B)",
    4: "MID-IN",
    5: "HEART",
    6: "MID-AWAY",
    7: "LO-IN",
    8: "LO-MID",
    9: "LO-AWAY",
    11: "OUT-UP-3B",
    12: "OUT-UP-1B",
    13: "OUT-DN-3B",
    14: "OUT-DN-1B",
}

SWING_DESC = {
    "hit_into_play",
    "foul",
    "foul_tip",
    "swinging_strike",
    "swinging_strike_blocked",
    "foul_bunt",
    "missed_bunt",
    "swinging_pitchout",
}
WHIFF_DESC = {"swinging_strike", "swinging_strike_blocked", "missed_bunt"}


def fetch_statcast(url: str, *, timeout: int = 120) -> pd.DataFrame:
    r = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=timeout)
    r.raise_for_status()
    text = r.content.decode("utf-8", errors="replace").replace("\x00", "")
    if not text.strip():
        return pd.DataFrame()
    return pd.read_csv(StringIO(text), low_memory=False)


def fetch_pitcher_pitches(pitcher_id: int, year: int) -> pd.DataFrame:
    url = STATCAST_PITCHER_URL.format(year=year, pitcher_id=pitcher_id)
    df = fetch_statcast(url)
    if df.empty:
        url = url.replace("hfGT=R%7CPO%7CS%7C", "hfGT=R%7C")
        df = fetch_statcast(url)
    return df


def fetch_batter_pitches(batter_id: int, year: int) -> pd.DataFrame:
    url = STATCAST_BATTER_URL.format(year=year, batter_id=batter_id)
    df = fetch_statcast(url)
    if df.empty:
        url = url.replace("hfGT=R%7CPO%7CS%7C", "hfGT=R%7C")
        df = fetch_statcast(url)
    return df


def filter_by_recent_days(
    df: pd.DataFrame,
    days: int,
    *,
    as_of: date | None = None,
) -> pd.DataFrame:
    """Keep pitches whose ``game_date`` falls in the last ``days`` ending ``as_of``."""
    if df.empty or days <= 0 or "game_date" not in df.columns:
        return df.iloc[0:0].copy()
    gd = pd.to_datetime(df["game_date"], errors="coerce")
    end = pd.Timestamp(as_of or date.today())
    start = end - pd.Timedelta(days=int(days))
    mask = (gd >= start) & (gd <= end)
    return df.loc[mask].copy()


def _zone_series(df: pd.DataFrame) -> pd.Series:
    return pd.to_numeric(df.get("zone"), errors="coerce")


def analyze_pitcher(df: pd.DataFrame) -> dict[str, Any]:
    d = df.dropna(subset=["plate_x", "plate_z"]).copy()
    d["zone"] = _zone_series(d)
    out: dict[str, Any] = {
        "n": int(len(d)),
        "by_pitch": (
            d["pitch_type"].value_counts(normalize=True).round(3).to_dict()
            if "pitch_type" in d.columns
            else {}
        ),
        "velo": (
            d.groupby("pitch_type")["release_speed"].mean().round(1).to_dict()
            if {"pitch_type", "release_speed"} <= set(d.columns)
            else {}
        ),
        "by_stand": {},
    }
    if "stand" not in d.columns:
        return out
    for stand, g in d.groupby("stand"):
        loc = (
            g["zone"]
            .value_counts(normalize=True)
            .reindex(list(range(1, 10)) + [11, 12, 13, 14])
            .fillna(0)
        )
        top = loc.sort_values(ascending=False).head(6)
        pitch_loc: dict[str, dict[str, float]] = {}
        # Full zone-id shares per pitch (for heatmaps) + usage vs this hand
        pitch_loc_zones: dict[str, dict[int, float]] = {}
        pitch_usage: dict[str, float] = {}
        zone_pitch_mix: dict[int, list[dict[str, Any]]] = {}
        if "pitch_type" in g.columns:
            pitch_usage = {
                str(pt): round(float(v), 3)
                for pt, v in g["pitch_type"].value_counts(normalize=True).items()
            }
            for pt, gg in g.groupby("pitch_type"):
                if len(gg) < 30:
                    continue
                zc_all = gg["zone"].value_counts(normalize=True)
                pitch_loc_zones[str(pt)] = {
                    int(i): round(float(v), 4)
                    for i, v in zc_all.items()
                    if pd.notna(i) and float(v) > 0
                }
                zc = zc_all.head(3)
                pitch_loc[str(pt)] = {
                    ZONE_LABEL.get(int(i), str(i)): round(float(v), 3)
                    for i, v in zc.items()
                    if pd.notna(i)
                }
            # For each zone: which pitches are thrown there (share of pitches in zone)
            for z, zg in g.dropna(subset=["zone"]).groupby("zone"):
                z = int(z)
                if len(zg) < 12:
                    continue
                mix = zg["pitch_type"].value_counts(normalize=True).head(3)
                zone_pitch_mix[z] = [
                    {
                        "pitch": str(pt),
                        "share": round(float(share), 3),
                        "label": ZONE_LABEL.get(z, str(z)),
                    }
                    for pt, share in mix.items()
                ]
        out["by_stand"][str(stand)] = {
            "n": int(len(g)),
            "inzone": round(float(g["zone"].isin(range(1, 10)).mean()), 3),
            "heart": round(float(g["zone"].eq(5).mean()), 3),
            "mean_px": round(float(g["plate_x"].mean()), 3),
            "mean_pz": round(float(g["plate_z"].mean()), 3),
            "top_zones": {
                ZONE_LABEL.get(int(i), str(i)): round(float(v), 3)
                for i, v in top.items()
                if pd.notna(i)
            },
            "pitch_usage": pitch_usage,
            "pitch_loc": pitch_loc,
            "pitch_loc_zones": pitch_loc_zones,
            "zone_pitch_mix": {
                int(z): mix for z, mix in zone_pitch_mix.items()
            },
            "zone_share": {
                int(i): round(float(v), 4)
                for i, v in loc.items()
                if pd.notna(i) and float(v) > 0
            },
        }
    out["_df"] = d
    return out


def analyze_batter_vs_hand(
    df: pd.DataFrame,
    *,
    name: str,
    vs_hand: str,
    min_zone_pitches: int = SEASON_MIN_ZONE_PITCHES,
    min_bip_xwoba: int = SEASON_MIN_BIP_XWOBA,
    window: str = "season",
) -> dict[str, Any]:
    """Batter swing / damage by zone vs pitcher hand (``R`` or ``L``)."""
    d = df.copy()
    if "p_throws" in d.columns:
        d = d[d["p_throws"] == vs_hand]
    d = d.dropna(subset=["plate_x", "plate_z"])
    d["zone"] = _zone_series(d)
    d["is_swing"] = d["description"].isin(SWING_DESC)
    d["is_whiff"] = d["description"].isin(WHIFF_DESC)
    d["xwoba"] = pd.to_numeric(
        d.get("estimated_woba_using_speedangle"), errors="coerce"
    )
    d["ev"] = pd.to_numeric(d.get("launch_speed"), errors="coerce")
    if "type" in d.columns:
        d["is_bip"] = d["type"].eq("X")
    else:
        d["is_bip"] = d["description"].eq("hit_into_play")
    if "launch_speed_angle" in d.columns:
        d["is_barrel"] = d["launch_speed_angle"].eq(6)
    else:
        d["is_barrel"] = False

    rows: list[dict[str, Any]] = []
    for z, g in d.groupby("zone"):
        if pd.isna(z):
            continue
        z = int(z)
        n = len(g)
        if n < int(min_zone_pitches):
            continue
        swings = int(g["is_swing"].sum())
        whiffs = int(g["is_whiff"].sum())
        bip = g[g["is_bip"]]
        xw = bip["xwoba"].mean() if len(bip) >= int(min_bip_xwoba) else float("nan")
        ev = bip["ev"].mean() if len(bip) >= int(min_bip_xwoba) else float("nan")
        brl = bip["is_barrel"].mean() if len(bip) >= int(min_bip_xwoba) else float("nan")
        rows.append(
            {
                "zone": z,
                "label": ZONE_LABEL.get(z, str(z)),
                "n": n,
                "swing_pct": round(100 * swings / n, 1),
                "whiff_of_swing": (
                    round(100 * whiffs / swings, 1) if swings else None
                ),
                "bip": int(len(bip)),
                "xwoba_bip": None if pd.isna(xw) else round(float(xw), 3),
                "ev_bip": None if pd.isna(ev) else round(float(ev), 1),
                "barrel_bip": None if pd.isna(brl) else round(100 * float(brl), 1),
            }
        )
    zone_df = pd.DataFrame(rows)
    empty = {
        "name": name,
        "vs_hand": vs_hand,
        "window": window,
        "n_pitches": int(len(d)),
        "stand": None,
        "all_zones": [],
        "top_swing_zones": [],
        "top_damage_zones": [],
        "sample_flags": [],
    }
    if zone_df.empty:
        empty["sample_flags"] = (
            ["LOW_SAMPLE_RECENT"] if window == "recent" else ["LOW_SAMPLE_BATTER"]
        )
        return empty

    dmg_floor = 5 if window == "recent" else 8
    swing_floor = 12 if window == "recent" else 25
    dmg = zone_df[
        (zone_df["bip"] >= dmg_floor) & zone_df["xwoba_bip"].notna()
    ].sort_values("xwoba_bip", ascending=False)
    swing = zone_df[zone_df["n"] >= swing_floor].sort_values(
        "swing_pct", ascending=False
    )
    stand = None
    if "stand" in d.columns and len(d):
        stand = str(d["stand"].mode().iloc[0])

    flags: list[str] = []
    n_pitches = int(len(d))
    if window == "season" and n_pitches < LOW_BATTER_PITCHES_VS_HAND:
        flags.append("LOW_SAMPLE_BATTER")
    if window == "recent" and n_pitches < LOW_RECENT_PITCHES_VS_HAND:
        flags.append("LOW_SAMPLE_RECENT")

    return {
        "name": name,
        "vs_hand": vs_hand,
        "window": window,
        "n_pitches": n_pitches,
        "stand": stand,
        "sample_flags": flags,
        "swing_pct": round(100 * float(d["is_swing"].mean()), 1) if len(d) else None,
        "whiff_of_swing": (
            round(
                100 * float(d["is_whiff"].sum()) / max(float(d["is_swing"].sum()), 1),
                1,
            )
            if len(d)
            else None
        ),
        "top_swing_zones": swing.head(5)[
            ["label", "swing_pct", "n", "whiff_of_swing"]
        ].to_dict("records"),
        "top_damage_zones": dmg.head(5)[
            ["label", "xwoba_bip", "ev_bip", "barrel_bip", "bip", "swing_pct"]
        ].to_dict("records"),
        "all_zones": zone_df.to_dict("records"),
        "_zone_df": zone_df,
    }


def _risk_from_share_xwoba(share: float, xw: float | None) -> str:
    if xw is None:
        return "—"
    if float(xw) >= 0.400 and float(share) >= 0.06:
        return "HOT"
    if float(xw) >= 0.350 and float(share) >= 0.05:
        return "WARM"
    if float(xw) <= 0.280 and float(share) >= 0.07:
        return "COLD"
    return "—"


def overlap_rows(
    batter: dict[str, Any],
    pitcher_stand_block: dict[str, Any],
    *,
    low_bip: int = LOW_ZONE_BIP,
) -> list[dict[str, Any]]:
    """Join pitcher zone share vs batter damage for the batter's stand."""
    share_map = pitcher_stand_block.get("zone_share") or {}
    dmg = {int(r["zone"]): r for r in batter.get("all_zones") or []}
    rows: list[dict[str, Any]] = []
    for z, share in share_map.items():
        z = int(z)
        b = dmg.get(z)
        if not b:
            continue
        xw = b.get("xwoba_bip")
        bip = int(b.get("bip") or 0)
        score = None
        if xw is not None and bip >= 6:
            score = round(float(share) * float(xw) * 100, 2)
        risk = _risk_from_share_xwoba(float(share), xw)
        flags: list[str] = []
        if risk in ("HOT", "WARM", "COLD") and bip < int(low_bip):
            flags.append("LOW_SAMPLE_ZONE")
        rows.append(
            {
                "zone": z,
                "label": ZONE_LABEL.get(z, str(z)),
                "pitcher_pct": round(100 * float(share), 1),
                "batter_swing": b.get("swing_pct"),
                "batter_xwoba": xw,
                "batter_ev": b.get("ev_bip"),
                "batter_barrel": b.get("barrel_bip"),
                "bip": bip,
                "overlap_score": score,
                "risk": risk,
                "sample_flags": flags,
            }
        )
    rows.sort(
        key=lambda r: (
            r["overlap_score"] is not None,
            r["overlap_score"] or 0,
        ),
        reverse=True,
    )
    return rows


def _agreement_tag(season_risk: str, recent_risk: str | None) -> str | None:
    """How season and recent zone flags line up."""
    s = season_risk if season_risk in ("HOT", "WARM", "COLD") else None
    r = recent_risk if recent_risk in ("HOT", "WARM", "COLD") else None
    if not s and not r:
        return None
    if s and r:
        if s == r:
            return "CONFIRM"
        # HOT vs COLD (or reverse) is a real conflict; HOT vs WARM = soft confirm
        if {s, r} == {"HOT", "COLD"} or {s, r} == {"WARM", "COLD"}:
            return "CONFLICT"
        if {s, r} <= {"HOT", "WARM"}:
            return "CONFIRM"
        return "CONFLICT"
    if s and not r:
        return "SEASON_ONLY"
    return "RECENT_ONLY"


def merge_season_recent_overlaps(
    season_rows: list[dict[str, Any]],
    recent_rows: list[dict[str, Any]] | None,
) -> list[dict[str, Any]]:
    """Attach recent risk/xwOBA onto season overlap rows + agreement tags."""
    recent_map = {int(r["zone"]): r for r in (recent_rows or [])}
    out: list[dict[str, Any]] = []
    seen: set[int] = set()
    for row in season_rows:
        z = int(row["zone"])
        seen.add(z)
        rr = recent_map.get(z)
        merged = dict(row)
        merged["season_risk"] = row.get("risk")
        merged["recent_risk"] = rr.get("risk") if rr else None
        merged["recent_xwoba"] = rr.get("batter_xwoba") if rr else None
        merged["recent_bip"] = rr.get("bip") if rr else None
        merged["recent_pitcher_pct"] = rr.get("pitcher_pct") if rr else None
        flags = list(row.get("sample_flags") or [])
        if rr:
            for f in rr.get("sample_flags") or []:
                if f not in flags:
                    flags.append(f)
            if (rr.get("bip") or 0) < LOW_RECENT_ZONE_BIP and rr.get("risk") in (
                "HOT",
                "WARM",
                "COLD",
            ):
                if "LOW_SAMPLE_RECENT" not in flags:
                    flags.append("LOW_SAMPLE_RECENT")
        merged["sample_flags"] = flags
        merged["agreement"] = _agreement_tag(
            str(merged.get("season_risk") or "—"),
            merged.get("recent_risk"),
        )
        # Prefer confirmed HOTs when sorting
        conf_boost = 1 if merged.get("agreement") == "CONFIRM" else 0
        merged["_sort_boost"] = conf_boost
        out.append(merged)

    # Recent-only zones that season missed (still on pitcher tunnel)
    for z, rr in recent_map.items():
        if z in seen:
            continue
        if rr.get("risk") not in ("HOT", "WARM", "COLD"):
            continue
        flags = list(rr.get("sample_flags") or [])
        if "LOW_SAMPLE_RECENT" not in flags:
            flags.append("LOW_SAMPLE_RECENT")
        out.append(
            {
                "zone": z,
                "label": rr.get("label") or ZONE_LABEL.get(z, str(z)),
                "pitcher_pct": rr.get("pitcher_pct"),
                "batter_swing": rr.get("batter_swing"),
                "batter_xwoba": rr.get("batter_xwoba"),
                "batter_ev": rr.get("batter_ev"),
                "batter_barrel": rr.get("batter_barrel"),
                "bip": rr.get("bip"),
                "overlap_score": rr.get("overlap_score"),
                "risk": rr.get("risk"),  # surface recent for viz
                "season_risk": "—",
                "recent_risk": rr.get("risk"),
                "recent_xwoba": rr.get("batter_xwoba"),
                "recent_bip": rr.get("bip"),
                "recent_pitcher_pct": rr.get("pitcher_pct"),
                "sample_flags": flags,
                "agreement": "RECENT_ONLY",
                "_sort_boost": 0,
            }
        )

    out.sort(
        key=lambda r: (
            r.get("_sort_boost") or 0,
            r.get("overlap_score") is not None,
            r.get("overlap_score") or 0,
        ),
        reverse=True,
    )
    for r in out:
        r.pop("_sort_boost", None)
    return out


def batter_sample_summary(
    season: dict[str, Any],
    recent: dict[str, Any] | None,
) -> list[str]:
    """Player-level FYI flags for the lean card."""
    flags: list[str] = []
    for f in season.get("sample_flags") or []:
        if f not in flags:
            flags.append(f)
    if recent:
        for f in recent.get("sample_flags") or []:
            if f not in flags:
                flags.append(f)
        if int(recent.get("n_pitches") or 0) < LOW_RECENT_PITCHES_VS_HAND:
            if "LOW_SAMPLE_RECENT" not in flags:
                flags.append("LOW_SAMPLE_RECENT")
    return flags


def slugify(name: str) -> str:
    import unicodedata

    s = unicodedata.normalize("NFKD", name.lower().strip())
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = re.sub(r"[^a-z0-9]+", "-", s)
    return s.strip("-") or "pitcher"


def render_markdown(
    *,
    pitcher_name: str,
    pitcher_id: int,
    pitcher_hand: str,
    year: int,
    game: str | None,
    pitcher_sum: dict[str, Any],
    batters: list[dict[str, Any]],
    overlaps: dict[str, list[dict[str, Any]]],
    hits_rows: list[dict[str, Any]] | None = None,
    recent_days: int | None = None,
) -> str:
    lines: list[str] = []
    lines.append(f"# Zone overlap — vs {pitcher_name} ({year} Statcast)")
    lines.append("")
    if game:
        lines.append(f"**Game:** {game}")
    lines.append(
        f"**Pitcher:** {pitcher_name} ({pitcher_hand}HP, id {pitcher_id}) · "
        f"n={pitcher_sum.get('n')} pitches"
    )
    recent_meta = pitcher_sum.get("recent") or {}
    if recent_days:
        rn = recent_meta.get("n")
        lines.append(
            f"**Windows:** season + **last {recent_days}d**"
            + (f" (pitcher recent n={rn})" if rn is not None else "")
        )
    lines.append("")
    lines.append(
        "Catcher’s view. Display-only — does not change Exp K or hits scores. "
        "HOT/WARM/COLD use **season** pitcher location × batter damage; "
        "**recent** confirms or flags conflict. "
        "`LOW_SAMPLE_*` = FYI — size down, don’t veto automatically."
    )
    lines.append("")
    mix = pitcher_sum.get("by_pitch") or {}
    velo = pitcher_sum.get("velo") or {}
    if mix:
        mix_s = " / ".join(f"{k} {100 * v:.0f}%" for k, v in sorted(mix.items(), key=lambda x: -x[1]))
        lines.append(f"**Mix:** {mix_s}")
    if velo:
        vel_s = ", ".join(f"{k} ~{v}" for k, v in sorted(velo.items()))
        lines.append(f"**Velo:** {vel_s}")
    lines.append("")
    lines.append("## Where the pitcher throws")
    lines.append("")
    for stand, block in (pitcher_sum.get("by_stand") or {}).items():
        lines.append(
            f"### vs {stand}HB — in-zone {100 * block['inzone']:.0f}% · "
            f"heart {100 * block['heart']:.0f}% · "
            f"mean px={block['mean_px']} (neg=3B) pz={block['mean_pz']}"
        )
        lines.append("")
        top = block.get("top_zones") or {}
        if top:
            lines.append(
                "- Top zones: "
                + ", ".join(f"{k} {100 * v:.0f}%" for k, v in top.items())
            )
        usage = block.get("pitch_usage") or {}
        if usage:
            lines.append(
                "- **Usage vs this hand:** "
                + ", ".join(
                    f"{pt} {100 * share:.0f}%"
                    for pt, share in sorted(usage.items(), key=lambda x: -x[1])
                )
            )
        pl = block.get("pitch_loc") or {}
        for pt, locs in pl.items():
            lines.append(
                f"- **{pt} lands:** "
                + ", ".join(f"{k} {100 * v:.0f}%" for k, v in locs.items())
            )
        # Top zones → which pitches build them
        zmix = block.get("zone_pitch_mix") or {}
        share = block.get("zone_share") or {}
        top_z = sorted(share.items(), key=lambda x: -float(x[1]))[:4]
        if top_z and zmix:
            bits = []
            for z, sh in top_z:
                z = int(z)
                mix = zmix.get(z) or zmix.get(str(z)) or []
                if not mix:
                    continue
                pitches = "+".join(
                    f"{m['pitch']} {100 * m['share']:.0f}%" for m in mix[:2]
                )
                bits.append(
                    f"{ZONE_LABEL.get(z, z)} ({100 * float(sh):.0f}% throws → {pitches})"
                )
            if bits:
                lines.append("- **Zone → pitch mix:** " + "; ".join(bits))
        lines.append("")

    lines.append("## Batter heat vs opposing hand → overlap")
    lines.append("")
    for b in batters:
        name = b["name"]
        recent_b = b.get("recent") or {}
        rn = recent_b.get("n_pitches")
        lines.append(
            f"### {name} (stand {b.get('stand')}, vs {b.get('vs_hand')}HP, "
            f"season n={b.get('n_pitches')}"
            + (f", recent n={rn}" if rn is not None else "")
            + ")"
        )
        flags = b.get("sample_flags") or []
        if flags:
            lines.append(
                "- **FYI sample:** "
                + ", ".join(flags)
                + " — thin MLB / recent sample; inform size, don’t auto-fade"
            )
        lines.append(
            f"- Swing {b.get('swing_pct')}% · whiff/swing {b.get('whiff_of_swing')}%"
        )
        if b.get("top_swing_zones"):
            lines.append("- **Top swing (season):** " + "; ".join(
                f"{r['label']} {r['swing_pct']}%" for r in b["top_swing_zones"][:4]
            ))
        if b.get("top_damage_zones"):
            lines.append("- **Top damage season (xwOBA BIP):** " + "; ".join(
                f"{r['label']} {r['xwoba_bip']:.3f} "
                f"(EV {r['ev_bip']}, brl {r['barrel_bip']}%, BIP {r['bip']})"
                for r in b["top_damage_zones"][:4]
            ))
        if recent_b.get("top_damage_zones"):
            lines.append(
                f"- **Top damage recent ({recent_days or '?'}d):** "
                + "; ".join(
                    f"{r['label']} {r['xwoba_bip']:.3f} (BIP {r['bip']})"
                    for r in recent_b["top_damage_zones"][:4]
                )
            )
        ov = overlaps.get(name) or []
        hot = [
            r
            for r in ov
            if (r.get("season_risk") or r.get("risk")) in ("HOT", "WARM")
            and r.get("batter_xwoba") is not None
        ]
        cold = [
            r for r in ov if (r.get("season_risk") or r.get("risk")) == "COLD"
        ]
        if hot:
            bits = []
            for r in hot[:5]:
                ag = r.get("agreement") or ""
                ag_s = f" · {ag}" if ag else ""
                recent_bit = ""
                if r.get("recent_risk"):
                    recent_bit = (
                        f", recent {r['recent_risk']} "
                        f"xwOBA {r.get('recent_xwoba')} BIP {r.get('recent_bip')}"
                    )
                thin = ""
                if r.get("sample_flags"):
                    thin = " [" + ",".join(r["sample_flags"]) + "]"
                bits.append(
                    f"{r.get('season_risk') or r.get('risk')} {r['label']} "
                    f"(W {r['pitcher_pct']}%, xwOBA {r['batter_xwoba']}"
                    f"{recent_bit}{ag_s}){thin}"
                )
            lines.append("- **HOT/WARM overlap:** " + "; ".join(bits))
        if cold:
            lines.append("- **COLD vs his tunnel:** " + "; ".join(
                f"{r['label']} (W {r['pitcher_pct']}%, xwOBA {r['batter_xwoba']}"
                + (
                    f", recent {r['recent_risk']}"
                    if r.get("recent_risk")
                    else ""
                )
                + (f" · {r['agreement']}" if r.get("agreement") else "")
                + ")"
                for r in cold[:3]
            ))
        confirm = [r for r in ov if r.get("agreement") == "CONFIRM"]
        conflict = [r for r in ov if r.get("agreement") == "CONFLICT"]
        if confirm:
            lines.append(
                "- **Season ∩ recent CONFIRM:** "
                + ", ".join(
                    f"{r.get('season_risk') or r.get('risk')} {r['label']}"
                    for r in confirm[:5]
                )
            )
        if conflict:
            lines.append(
                "- **Season vs recent CONFLICT:** "
                + ", ".join(
                    f"{r['label']} ({r.get('season_risk')}→{r.get('recent_risk')})"
                    for r in conflict[:4]
                )
            )
        lines.append("")

    if hits_rows:
        lines.append("## Hits / H+R+RBI board (same slate)")
        lines.append("")
        lines.append(
            "| Slot | Batter | Hits | HR/RBI | AVG vs hand | Barrel | HH | Zone note |"
        )
        lines.append(
            "|------|--------|------|--------|-------------|--------|----|-----------|"
        )
        for r in hits_rows:
            note = r.get("zone_note") or "—"
            lines.append(
                f"| {r.get('slot','')} | {r['batter']} | "
                f"{r['hits_score']:.1f} | {r['hr_rbi_score']:.1f} | "
                f"{r.get('avg_vs_hand', float('nan')):.3f} | "
                f"{r.get('barrel_pct', float('nan')):.1f}% | "
                f"{r.get('hard_hit_pct', float('nan')):.1f}% | {note} |"
            )
        lines.append("")

    lines.append(
        "*Generated by `mlb-k-matchups/zone_overlap.py` — re-run on future "
        "slates with `--hits` + `--pitcher`. Prefer CONFIRM HOTs; treat "
        "`LOW_SAMPLE_*` as sizing FYI.*"
    )
    return "\n".join(lines) + "\n"


def batters_from_hits(
    hits_path: Path,
    pitcher_name: str,
    *,
    top: int | None = None,
) -> tuple[str | None, str | None, int | None, list[dict[str, Any]], pd.DataFrame]:
    """Return game, pitcher_team, pitcher_id, batter list, filtered hits frame."""
    hits = pd.read_csv(hits_path)
    sub = hits[hits["pitcher"].astype(str).str.casefold() == pitcher_name.casefold()].copy()
    if sub.empty:
        # fuzzy contains
        sub = hits[
            hits["pitcher"].astype(str).str.contains(pitcher_name, case=False, na=False)
        ].copy()
    if sub.empty:
        raise SystemExit(f"No rows in {hits_path} for pitcher={pitcher_name!r}")
    sub = sub.sort_values(["hits_score"], ascending=False)
    if top is not None and top > 0:
        chosen = sub.head(top)
    else:
        chosen = sub
    game = str(chosen["game"].iloc[0]) if "game" in chosen.columns else None
    pteam = str(chosen["pitcher_team"].iloc[0]) if "pitcher_team" in chosen.columns else None
    # pitcher_id may live on rankings; hits often lacks it
    pid = None
    batters = []
    for _, r in chosen.iterrows():
        batters.append(
            {
                "name": str(r["batter"]),
                "id": int(r["batter_id"]),
                "slot": int(r["slot"]) if pd.notna(r.get("slot")) else None,
                "bat_side": r.get("bat_side"),
                "team": r.get("team"),
                "hits_score": float(r["hits_score"]),
                "hr_rbi_score": float(r["hr_rbi_score"]),
                "avg_vs_hand": float(r["avg_vs_hand"]) if pd.notna(r.get("avg_vs_hand")) else None,
                "barrel_pct": float(r["barrel_pct"]) if pd.notna(r.get("barrel_pct")) else None,
                "hard_hit_pct": float(r["hard_hit_pct"]) if pd.notna(r.get("hard_hit_pct")) else None,
                "xwoba": float(r["xwoba"]) if pd.notna(r.get("xwoba")) else None,
            }
        )
    return game, pteam, pid, batters, sub.sort_values("slot")


def resolve_pitcher_id(
    pitcher_name: str,
    rankings_path: Path | None,
    explicit: int | None,
) -> tuple[int, str]:
    if explicit:
        hand = "R"
        if rankings_path and rankings_path.exists():
            rk = pd.read_csv(rankings_path)
            m = rk[rk["pitcher"].astype(str).str.casefold() == pitcher_name.casefold()]
            if not m.empty and "pitch_hand" in m.columns:
                hand = str(m["pitch_hand"].iloc[0])
        return explicit, hand
    if not rankings_path or not rankings_path.exists():
        raise SystemExit("Need --pitcher-id or --rankings to resolve pitcher id")
    rk = pd.read_csv(rankings_path)
    m = rk[rk["pitcher"].astype(str).str.casefold() == pitcher_name.casefold()]
    if m.empty:
        m = rk[rk["pitcher"].astype(str).str.contains(pitcher_name, case=False, na=False)]
    if m.empty:
        raise SystemExit(f"Pitcher {pitcher_name!r} not in {rankings_path}")
    return int(m["pitcher_id"].iloc[0]), str(m["pitch_hand"].iloc[0])


def zone_note_for_batter(
    ov: list[dict[str, Any]],
    *,
    sample_flags: list[str] | None = None,
) -> str:
    """Compact note for hits-board table: risk + agreement + sample FYI."""
    def _season_risk(r: dict[str, Any]) -> str:
        return str(r.get("season_risk") or r.get("risk") or "—")

    hot = [r for r in ov if _season_risk(r) == "HOT"]
    warm = [r for r in ov if _season_risk(r) == "WARM"]
    cold = [r for r in ov if _season_risk(r) == "COLD"]
    confirm = [r for r in ov if r.get("agreement") == "CONFIRM"]
    bits: list[str] = []
    if confirm:
        bits.append(
            "CONFIRM "
            + "/".join(
                f"{_season_risk(r)} {r['label']}" for r in confirm[:2]
            )
        )
    elif hot:
        bits.append("HOT " + "/".join(r["label"] for r in hot[:2]))
    elif warm:
        bits.append("WARM " + "/".join(r["label"] for r in warm[:2]))
    if cold:
        bits.append("COLD " + cold[0]["label"])
    conflict = [r for r in ov if r.get("agreement") == "CONFLICT"]
    if conflict:
        bits.append("CONFLICT " + conflict[0]["label"])
    thin = [f for f in (sample_flags or []) if f.startswith("LOW_SAMPLE")]
    if thin:
        bits.append("+".join(thin[:2]))
    return "; ".join(bits) if bits else "—"


def run_overlap(
    *,
    pitcher_name: str,
    pitcher_id: int,
    pitcher_hand: str,
    year: int,
    batter_specs: list[dict[str, Any]],
    game: str | None = None,
    recent_days: int | None = DEFAULT_RECENT_DAYS,
    as_of: date | None = None,
) -> dict[str, Any]:
    print(f"Fetching {pitcher_name} ({pitcher_id}) {year} Statcast…")
    pdf = fetch_pitcher_pitches(pitcher_id, year)
    if pdf.empty:
        raise SystemExit(f"No Statcast pitches for pitcher_id={pitcher_id} year={year}")
    p_sum = analyze_pitcher(pdf)
    vs_hand = pitcher_hand.upper()[0]

    # Recent pitcher location only if enough pitches; else keep season tunnel.
    p_recent_sum: dict[str, Any] | None = None
    if recent_days and recent_days > 0:
        pdf_r = filter_by_recent_days(pdf, recent_days, as_of=as_of)
        if len(pdf_r) >= MIN_PITCHER_RECENT_PITCHES:
            p_recent_sum = analyze_pitcher(pdf_r)
            print(
                f"  pitcher recent {recent_days}d: n={len(pdf_r)} "
                f"(using recent throw% for recent overlaps)"
            )
        else:
            print(
                f"  pitcher recent {recent_days}d: n={len(pdf_r)} "
                f"< {MIN_PITCHER_RECENT_PITCHES} — season throw% only"
            )

    batter_results: list[dict[str, Any]] = []
    overlaps: dict[str, list[dict[str, Any]]] = {}
    for spec in batter_specs:
        name = spec["name"]
        bid = int(spec["id"])
        print(f"  batter {name} ({bid})…")
        bdf = fetch_batter_pitches(bid, year)
        if bdf.empty:
            print("    skip — no pitches")
            continue
        b_sum = analyze_batter_vs_hand(
            bdf,
            name=name,
            vs_hand=vs_hand,
            min_zone_pitches=SEASON_MIN_ZONE_PITCHES,
            min_bip_xwoba=SEASON_MIN_BIP_XWOBA,
            window="season",
        )
        stand = b_sum.get("stand") or "R"
        block = (p_sum.get("by_stand") or {}).get(stand) or {}
        season_ov = overlap_rows(b_sum, block, low_bip=LOW_ZONE_BIP) if block else []

        recent_sum: dict[str, Any] | None = None
        recent_ov: list[dict[str, Any]] | None = None
        if recent_days and recent_days > 0:
            bdf_r = filter_by_recent_days(bdf, recent_days, as_of=as_of)
            recent_sum = analyze_batter_vs_hand(
                bdf_r,
                name=name,
                vs_hand=vs_hand,
                min_zone_pitches=RECENT_MIN_ZONE_PITCHES,
                min_bip_xwoba=RECENT_MIN_BIP_XWOBA,
                window="recent",
            )
            # Prefer recent pitcher location when sample is enough; else season plan.
            r_block = block
            if p_recent_sum:
                r_block = (p_recent_sum.get("by_stand") or {}).get(stand) or block
            recent_ov = (
                overlap_rows(recent_sum, r_block, low_bip=LOW_RECENT_ZONE_BIP)
                if r_block
                else []
            )
            print(
                f"    season n={b_sum.get('n_pitches')} · "
                f"recent{recent_days}d n={recent_sum.get('n_pitches')}"
            )

        merged = merge_season_recent_overlaps(season_ov, recent_ov)
        clean = {k: v for k, v in b_sum.items() if not k.startswith("_")}
        clean["slot"] = spec.get("slot")
        clean["team"] = spec.get("team")
        if recent_sum is not None:
            clean["recent"] = {
                k: v for k, v in recent_sum.items() if not k.startswith("_")
            }
        clean["sample_flags"] = batter_sample_summary(b_sum, recent_sum)
        batter_results.append(clean)
        overlaps[name] = merged

    p_clean = {k: v for k, v in p_sum.items() if not k.startswith("_")}
    if recent_days:
        p_clean["recent_days"] = recent_days
        p_clean["recent"] = {
            "n": int(len(filter_by_recent_days(pdf, recent_days, as_of=as_of))),
            "used_for_throw_pct": p_recent_sum is not None,
            "as_of": (as_of or date.today()).isoformat(),
        }
    return {
        "pitcher": {
            "name": pitcher_name,
            "id": pitcher_id,
            "hand": vs_hand,
            "year": year,
            "game": game,
            **p_clean,
        },
        "batters": batter_results,
        "overlaps": overlaps,
        "meta": {
            "recent_days": recent_days,
            "as_of": (as_of or date.today()).isoformat() if recent_days else None,
            "thresholds": {
                "low_batter_pitches_vs_hand": LOW_BATTER_PITCHES_VS_HAND,
                "low_zone_bip": LOW_ZONE_BIP,
                "low_recent_pitches_vs_hand": LOW_RECENT_PITCHES_VS_HAND,
                "low_recent_zone_bip": LOW_RECENT_ZONE_BIP,
            },
        },
    }


def parse_batter_arg(raw: str) -> list[dict[str, Any]]:
    """Parse ``Name:id,Name:id``."""
    out = []
    for part in raw.split(","):
        part = part.strip()
        if not part:
            continue
        if ":" not in part:
            raise SystemExit(f"Batter spec needs Name:id — got {part!r}")
        name, sid = part.rsplit(":", 1)
        out.append({"name": name.strip(), "id": int(sid.strip())})
    return out


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--year", type=int, default=2026)
    p.add_argument("--pitcher", default=None, help="Pitcher display name")
    p.add_argument("--pitcher-id", type=int, default=None)
    p.add_argument(
        "--pitcher-hand",
        default=None,
        help="R or L (default: from rankings CSV)",
    )
    p.add_argument("--hits", type=Path, default=None, help="hits-YYYY-MM-DD.csv")
    p.add_argument(
        "--rankings",
        type=Path,
        default=None,
        help="rankings-YYYY-MM-DD.csv (for pitcher_id / hand)",
    )
    p.add_argument(
        "--top",
        type=int,
        default=None,
        help="Only top N batters by hits_score from --hits (default: full lineup)",
    )
    p.add_argument(
        "--batters",
        default=None,
        help="Explicit Name:id,Name:id (overrides --hits batter list)",
    )
    p.add_argument(
        "-o",
        "--output-prefix",
        type=Path,
        default=None,
        help="Write PREFIX.md and PREFIX.json (default: zone-overlap-<slug>-<date>)",
    )
    p.add_argument(
        "--images",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Write PNG zone heatmaps + HTML gallery (default: on)",
    )
    p.add_argument(
        "--images-dir",
        type=Path,
        default=None,
        help="Directory for PNGs/gallery (default: zone-maps/<pitcher-slug>-<date>)",
    )
    p.add_argument(
        "--from-json",
        type=Path,
        default=None,
        help="Skip Statcast fetch — rebuild markdown/images from an existing overlap JSON",
    )
    p.add_argument(
        "--recent-days",
        type=int,
        default=DEFAULT_RECENT_DAYS,
        help=(
            "Also score a rolling recent window (default: "
            f"{DEFAULT_RECENT_DAYS}). Use 0 with --no-recent to skip."
        ),
    )
    p.add_argument(
        "--recent",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Compare season HOTs to a recent Statcast window (default: on)",
    )
    p.add_argument(
        "--as-of",
        default=None,
        help="End date for recent window YYYY-MM-DD (default: today)",
    )
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    game = None
    hits_rows: list[dict[str, Any]] | None = None
    recent_days = int(args.recent_days) if args.recent else 0
    if recent_days <= 0:
        recent_days_opt: int | None = None
    else:
        recent_days_opt = recent_days
    as_of_date: date | None = None
    if args.as_of:
        as_of_date = date.fromisoformat(str(args.as_of))

    # Rebuild images / notes from a prior JSON (no Statcast re-pull)
    if args.from_json:
        payload = json.loads(Path(args.from_json).read_text())
        pitcher = payload.get("pitcher") or {}
        pid = int(pitcher.get("id") or 0)
        hand = str(pitcher.get("hand") or "R")
        game = pitcher.get("game")
        args.pitcher = str(args.pitcher or pitcher.get("name") or "pitcher")
        date_bit = ""
        m = re.search(r"\d{4}-\d{2}-\d{2}", str(args.from_json))
        if m:
            date_bit = m.group(0)
        prefix = args.output_prefix or Path(
            f"zone-overlap-{slugify(args.pitcher)}"
            + (f"-{date_bit}" if date_bit else "")
        )
        md_path = Path(str(prefix) + ".md")
        json_path = Path(str(prefix) + ".json")
        meta = payload.get("meta") or {}
        md = render_markdown(
            pitcher_name=args.pitcher,
            pitcher_id=pid,
            pitcher_hand=hand,
            year=int(pitcher.get("year") or args.year),
            game=str(game) if game else None,
            pitcher_sum=pitcher,
            batters=payload.get("batters") or [],
            overlaps=payload.get("overlaps") or {},
            hits_rows=None,
            recent_days=meta.get("recent_days") or pitcher.get("recent_days"),
        )
        md_path.write_text(md)
        json_path.write_text(json.dumps(payload, indent=2, default=str))
        print(f"Wrote {md_path}")
        print(f"Wrote {json_path}")
        if args.images:
            from heatmap_viz import build_images_from_payload

            img_dir = args.images_dir or Path(
                f"zone-maps/{slugify(args.pitcher)}"
                + (f"-{date_bit}" if date_bit else "")
            )
            info = build_images_from_payload(payload, out_dir=img_dir)
            print(f"Wrote gallery {info['gallery']} ({len(info['cards'])} batters)")
        return

    batter_specs: list[dict[str, Any]]
    if args.batters:
        batter_specs = parse_batter_arg(args.batters)
    elif args.hits:
        game, _pteam, _pid, batter_specs, full = batters_from_hits(
            args.hits, args.pitcher, top=args.top
        )
        hits_rows = []
        for _, r in full.sort_values("hits_score", ascending=False).iterrows():
            hits_rows.append(
                {
                    "slot": int(r["slot"]) if pd.notna(r.get("slot")) else "",
                    "batter": r["batter"],
                    "hits_score": float(r["hits_score"]),
                    "hr_rbi_score": float(r["hr_rbi_score"]),
                    "avg_vs_hand": float(r["avg_vs_hand"]) if pd.notna(r.get("avg_vs_hand")) else float("nan"),
                    "barrel_pct": float(r["barrel_pct"]) if pd.notna(r.get("barrel_pct")) else float("nan"),
                    "hard_hit_pct": float(r["hard_hit_pct"]) if pd.notna(r.get("hard_hit_pct")) else float("nan"),
                }
            )
    else:
        raise SystemExit("Provide --hits, --batters, or --from-json")

    if not args.pitcher:
        raise SystemExit("--pitcher is required unless using --from-json")

    # Infer rankings path beside hits
    rankings = args.rankings
    if rankings is None and args.hits:
        cand = args.hits.with_name(
            args.hits.name.replace("hits-", "rankings-", 1)
        )
        if cand.exists():
            rankings = cand

    pid, hand = resolve_pitcher_id(args.pitcher, rankings, args.pitcher_id)
    if args.pitcher_hand:
        hand = args.pitcher_hand.upper()[0]

    payload = run_overlap(
        pitcher_name=args.pitcher,
        pitcher_id=pid,
        pitcher_hand=hand,
        year=args.year,
        batter_specs=batter_specs,
        game=game,
        recent_days=recent_days_opt,
        as_of=as_of_date,
    )

    # Attach zone notes onto hits rows
    if hits_rows is not None:
        batter_by_name = {b["name"]: b for b in payload.get("batters") or []}
        for row in hits_rows:
            ov = payload["overlaps"].get(row["batter"]) or []
            flags = (batter_by_name.get(row["batter"]) or {}).get("sample_flags")
            row["zone_note"] = zone_note_for_batter(ov, sample_flags=flags)

    # Default output prefix
    date_bit = ""
    if args.hits and re.search(r"\d{4}-\d{2}-\d{2}", args.hits.name):
        date_bit = re.search(r"\d{4}-\d{2}-\d{2}", args.hits.name).group(0)
    prefix = args.output_prefix
    if prefix is None:
        slug = slugify(args.pitcher)
        prefix = Path(
            f"zone-overlap-{slug}" + (f"-{date_bit}" if date_bit else "")
        )

    md = render_markdown(
        pitcher_name=args.pitcher,
        pitcher_id=pid,
        pitcher_hand=hand,
        year=args.year,
        game=game,
        pitcher_sum=payload["pitcher"],
        batters=payload["batters"],
        overlaps=payload["overlaps"],
        hits_rows=hits_rows,
        recent_days=recent_days_opt,
    )
    md_path = Path(str(prefix) + ".md") if prefix.suffix != ".md" else prefix
    if prefix.suffix == ".md":
        json_path = prefix.with_suffix(".json")
    else:
        md_path = Path(str(prefix) + ".md")
        json_path = Path(str(prefix) + ".json")

    md_path.write_text(md)
    json_path.write_text(json.dumps(payload, indent=2, default=str))
    print(f"Wrote {md_path}")
    print(f"Wrote {json_path}")

    if args.images:
        from heatmap_viz import build_images_from_payload

        img_dir = args.images_dir or Path(
            f"zone-maps/{slugify(args.pitcher)}"
            + (f"-{date_bit}" if date_bit else "")
        )
        info = build_images_from_payload(payload, out_dir=img_dir)
        print(f"Wrote gallery {info['gallery']} ({len(info['cards'])} batters)")


if __name__ == "__main__":
    main()
