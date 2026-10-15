"""Zone-overlap heat maps: pitcher location vs batter swing/damage.

Pulls Statcast pitch-level ``plate_x`` / ``plate_z`` / Savant ``zone`` for a
starter and each opposing lineup batter, then flags HOT / WARM / COLD pockets:

- **HOT** — pitcher throws there often AND batter damages (xwOBA on BIP)
- **COLD** — pitcher lives there but batter is weak (chase / soft contact)
- **WARM** — middling frequency + solid damage

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
"""

from __future__ import annotations

import argparse
import json
import re
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
        if n < 15:
            continue
        swings = int(g["is_swing"].sum())
        whiffs = int(g["is_whiff"].sum())
        bip = g[g["is_bip"]]
        xw = bip["xwoba"].mean() if len(bip) >= 5 else float("nan")
        ev = bip["ev"].mean() if len(bip) >= 5 else float("nan")
        brl = bip["is_barrel"].mean() if len(bip) >= 5 else float("nan")
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
    if zone_df.empty:
        return {
            "name": name,
            "vs_hand": vs_hand,
            "n_pitches": int(len(d)),
            "stand": None,
            "all_zones": [],
            "top_swing_zones": [],
            "top_damage_zones": [],
        }

    dmg = zone_df[
        (zone_df["bip"] >= 8) & zone_df["xwoba_bip"].notna()
    ].sort_values("xwoba_bip", ascending=False)
    swing = zone_df[zone_df["n"] >= 25].sort_values("swing_pct", ascending=False)
    stand = None
    if "stand" in d.columns and len(d):
        stand = str(d["stand"].mode().iloc[0])

    return {
        "name": name,
        "vs_hand": vs_hand,
        "n_pitches": int(len(d)),
        "stand": stand,
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


def overlap_rows(
    batter: dict[str, Any],
    pitcher_stand_block: dict[str, Any],
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
        score = None
        if xw is not None and b.get("bip", 0) >= 6:
            score = round(float(share) * float(xw) * 100, 2)
        risk = "—"
        if xw is not None and float(xw) >= 0.400 and float(share) >= 0.06:
            risk = "HOT"
        elif xw is not None and float(xw) >= 0.350 and float(share) >= 0.05:
            risk = "WARM"
        elif xw is not None and float(xw) <= 0.280 and float(share) >= 0.07:
            risk = "COLD"
        rows.append(
            {
                "zone": z,
                "label": ZONE_LABEL.get(z, str(z)),
                "pitcher_pct": round(100 * float(share), 1),
                "batter_swing": b.get("swing_pct"),
                "batter_xwoba": xw,
                "batter_ev": b.get("ev_bip"),
                "batter_barrel": b.get("barrel_bip"),
                "bip": b.get("bip"),
                "overlap_score": score,
                "risk": risk,
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
    lines.append("")
    lines.append(
        "Catcher’s view. Display-only — does not change Exp K or hits scores."
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
        lines.append(
            f"### {name} (stand {b.get('stand')}, vs {b.get('vs_hand')}HP, "
            f"n={b.get('n_pitches')})"
        )
        lines.append(
            f"- Swing {b.get('swing_pct')}% · whiff/swing {b.get('whiff_of_swing')}%"
        )
        if b.get("top_swing_zones"):
            lines.append("- **Top swing:** " + "; ".join(
                f"{r['label']} {r['swing_pct']}%" for r in b["top_swing_zones"][:4]
            ))
        if b.get("top_damage_zones"):
            lines.append("- **Top damage (xwOBA BIP):** " + "; ".join(
                f"{r['label']} {r['xwoba_bip']:.3f} "
                f"(EV {r['ev_bip']}, brl {r['barrel_bip']}%)"
                for r in b["top_damage_zones"][:4]
            ))
        ov = overlaps.get(name) or []
        hot = [r for r in ov if r["risk"] in ("HOT", "WARM") and r.get("batter_xwoba") is not None]
        cold = [r for r in ov if r["risk"] == "COLD"]
        if hot:
            lines.append("- **HOT/WARM overlap:** " + "; ".join(
                f"{r['risk']} {r['label']} (W {r['pitcher_pct']}%, "
                f"xwOBA {r['batter_xwoba']})"
                for r in hot[:5]
            ))
        if cold:
            lines.append("- **COLD vs his tunnel:** " + "; ".join(
                f"{r['label']} (W {r['pitcher_pct']}%, xwOBA {r['batter_xwoba']})"
                for r in cold[:3]
            ))
        lines.append("")

    if hits_rows:
        lines.append("## Hits / H+R+RBI board (same slate)")
        lines.append("")
        lines.append("| Slot | Batter | Hits | HR/RBI | AVG vs hand | Barrel | HH | Zone note |")
        lines.append("|------|--------|------|--------|-------------|--------|----|-----------|")
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
        "slates with `--hits` + `--pitcher`.*"
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


def zone_note_for_batter(ov: list[dict[str, Any]]) -> str:
    hot = [r for r in ov if r["risk"] == "HOT"]
    warm = [r for r in ov if r["risk"] == "WARM"]
    cold = [r for r in ov if r["risk"] == "COLD"]
    bits = []
    if hot:
        bits.append("HOT " + "/".join(r["label"] for r in hot[:2]))
    elif warm:
        bits.append("WARM " + "/".join(r["label"] for r in warm[:2]))
    if cold:
        bits.append("COLD " + cold[0]["label"])
    return "; ".join(bits) if bits else "—"


def run_overlap(
    *,
    pitcher_name: str,
    pitcher_id: int,
    pitcher_hand: str,
    year: int,
    batter_specs: list[dict[str, Any]],
    game: str | None = None,
) -> dict[str, Any]:
    print(f"Fetching {pitcher_name} ({pitcher_id}) {year} Statcast…")
    pdf = fetch_pitcher_pitches(pitcher_id, year)
    if pdf.empty:
        raise SystemExit(f"No Statcast pitches for pitcher_id={pitcher_id} year={year}")
    p_sum = analyze_pitcher(pdf)
    vs_hand = pitcher_hand.upper()[0]

    batter_results: list[dict[str, Any]] = []
    overlaps: dict[str, list[dict[str, Any]]] = {}
    for spec in batter_specs:
        name = spec["name"]
        bid = int(spec["id"])
        print(f"  batter {name} ({bid})…")
        bdf = fetch_batter_pitches(bid, year)
        if bdf.empty:
            print(f"    skip — no pitches")
            continue
        b_sum = analyze_batter_vs_hand(bdf, name=name, vs_hand=vs_hand)
        stand = b_sum.get("stand") or "R"
        block = (p_sum.get("by_stand") or {}).get(stand) or {}
        ov = overlap_rows(b_sum, block) if block else []
        # strip private frames
        clean = {k: v for k, v in b_sum.items() if not k.startswith("_")}
        clean["slot"] = spec.get("slot")
        clean["team"] = spec.get("team")
        batter_results.append(clean)
        overlaps[name] = ov

    p_clean = {k: v for k, v in p_sum.items() if not k.startswith("_")}
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
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    game = None
    hits_rows: list[dict[str, Any]] | None = None

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
    )

    # Attach zone notes onto hits rows
    if hits_rows is not None:
        for row in hits_rows:
            ov = payload["overlaps"].get(row["batter"]) or []
            row["zone_note"] = zone_note_for_batter(ov)

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
