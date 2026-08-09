"""Self-contained interactive HTML export for K-matchup rankings.

Heatmaps and matchup detail are server-rendered into the HTML so they work
even when the file is opened from a host that blocks JavaScript (e.g. GitHub
raw). Light JS only enhances search / sort / filter.
"""

from __future__ import annotations

import html as html_lib
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import pandas as pd

from sharpen import (  # noqa: E402
    ABS_MATCHUP_AVG,
    ABS_MATCHUP_ELITE,
    ABS_MATCHUP_STRONG,
    CONTACT_HEAVY_BIP,
    LEAGUE_BIP_PCT,
    LEAGUE_K_PCT,
    TRUST_TOTAL_EXP_KS,
    UNDER_CONFIRM_EXP_KS,
    UNDER_CONFIRM_MIN,
    WHIFF_PRONE_BIP,
)

# Canonical public board URL. Bookmark this — never commit-SHA previews.
# htmlpreview renders interactive tabs; always point at main (not a commit SHA).
STABLE_BOARD_URL = (
    "https://htmlpreview.github.io/?https://raw.githubusercontent.com/"
    "Ceezwrld/K-matchup/main/index.html"
)
STABLE_BOARD_PAGES_URL = "https://ceezwrld.github.io/K-matchup/"


def _json_safe(value: Any) -> Any:
    if value is None:
        return None
    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass
    if isinstance(value, (pd.Timestamp, datetime)):
        return value.isoformat()
    if isinstance(value, (int, float, str, bool)):
        return value
    if hasattr(value, "item"):
        try:
            item = value.item()
            try:
                if pd.isna(item):
                    return None
            except (TypeError, ValueError):
                pass
            return item
        except (ValueError, AttributeError):
            pass
    return value


def _esc(value: Any) -> str:
    if value is None:
        return ""
    return html_lib.escape(str(value), quote=True)


def _fmt(value: Any, digits: int = 2, *, signed: bool = False) -> str:
    v = _json_safe(value)
    if v is None:
        return "—"
    try:
        x = float(v)
        return f"{x:+.{digits}f}" if signed else f"{x:.{digits}f}"
    except (TypeError, ValueError):
        return "—"


def _heat_style(k: Any) -> str:
    """Arsenal bar fill: green helps pitcher (high K%), red helps batters (low K%)."""
    v = _json_safe(k)
    if v is None:
        return "background:transparent;color:var(--muted)"
    band = _grade_for("batter_k_pct", v)
    # Match rate-chip palette so bars and % chips read the same.
    if band == "low":
        return "background:rgba(140,40,40,0.62)"
    if band == "mid":
        return "background:rgba(154,91,18,0.58)"
    if band == "high":
        return "background:rgba(15,106,77,0.58)"
    if band == "elite":
        return "background:rgba(15,106,77,0.82)"
    return "background:rgba(20,32,26,0.15)"


def _grade_band(value: Any, low: float, mid: float, high: float) -> str | None:
    """Map a numeric value onto low / mid / high / elite (higher = better)."""
    v = _json_safe(value)
    if v is None:
        return None
    try:
        x = float(v)
    except (TypeError, ValueError):
        return None
    if x < low:
        return "low"
    if x < mid:
        return "mid"
    if x < high:
        return "high"
    return "elite"


def _grade_band_desc(value: Any, best: float, good: float, ok: float) -> str | None:
    """Map a numeric value onto elite / high / mid / low (lower = better)."""
    v = _json_safe(value)
    if v is None:
        return None
    try:
        x = float(v)
    except (TypeError, ValueError):
        return None
    if x <= best:
        return "elite"
    if x <= good:
        return "high"
    if x <= ok:
        return "mid"
    return "low"


def _grade_for(metric: str, value: Any) -> str | None:
    """Color-grade key projection / rates metrics for the HTML board.

    Bands are K-prop oriented: green = helps strikeout scripts / command,
    red = soft for overs (does not invent unders by itself).
    """
    if metric == "expected_ks":
        return _grade_band(value, 4.0, 5.0, 6.0)
    if metric == "expected_k_pct":
        # Align with solo arsenal bands: SOFT <20 · AVG ≥20 · STRONG ≥22.5 · ELITE ≥24
        return _grade_band(value, ABS_MATCHUP_AVG, ABS_MATCHUP_STRONG, ABS_MATCHUP_ELITE)
    if metric == "projected_ip":
        return _grade_band(value, 5.0, 5.75, 6.5)
    if metric == "tto":
        return _grade_band(value, 2.2, 2.6, 3.0)
    if metric == "batter_k_pct":
        return _grade_band(value, 15.0, 20.0, 25.0)
    if metric == "pitch_usage_pct":
        # Featured pitch weight — higher = more of the outing / more trustworthy
        return _grade_band(value, 12.0, 20.0, 30.0)
    if metric == "pitch_usage_vs_hand":
        # Platoon usage share for a pitch — high = that hand sees it a lot
        return _grade_band(value, 20.0, 35.0, 50.0)
    if metric == "pitch_whiff_pct":
        # Per-pitch pitcher whiff — high helps Ks (good)
        return _grade_band(value, 18.0, 26.0, 34.0)
    if metric == "pitch_velo_fb":
        # Fastball velo — higher = better stuff ceiling
        return _grade_band(value, 92.0, 94.5, 96.5)
    if metric == "pitch_velo_offspeed":
        # Offspeed/breaking velo is not a good/bad K signal — leave ungraded
        return None
    # Arsenal matchup strip
    if metric in ("arsenal_vs_league", "arsenal_vs_opp"):
        # Signed edges vs league / vs opp K% — positive helps overs
        return _grade_band(value, -1.0, 0.5, 2.0)
    if metric == "opp_k_pct":
        return _grade_band(value, 20.0, 23.0, 26.0)
    if metric == "opp_bip_pct":
        # Lower BIP helps overs (whiff_prone); higher helps unders
        return _grade_band_desc(value, WHIFF_PRONE_BIP, LEAGUE_BIP_PCT, CONTACT_HEAVY_BIP)
    if metric == "opp_bb_pct":
        # Higher BB% = patient / pitch-count risk
        return _grade_band_desc(value, 7.0, 9.0, 10.5)
    # Rates / command — attack-plate pack thresholds from backtest-lessons.
    if metric == "strike_pct":
        # ≥66 elite · ≥65 good · ≥63 avg · <63 soft (≤62 poor for overs)
        return _grade_band(value, 63.0, 65.0, 66.0)
    if metric == "f_strike_pct":
        # League F-Strike% ~60–61
        return _grade_band(value, 58.0, 62.0, 65.0)
    if metric == "zone_pct":
        # ≥44 elite · ≥43 attack · ≥40 avg · <40 off-plate
        return _grade_band(value, 40.0, 43.0, 44.0)
    if metric == "swstr_pct":
        # League SwStr% ~11; ≥13 elite miss · ≥11.5 good · ≥10 avg
        return _grade_band(value, 10.0, 11.5, 13.0)
    if metric == "csw_pct":
        # CSW (C+SwStr%) ~28–29; ≥31 elite · ≥29.5 good · ≥27.5 avg
        return _grade_band(value, 27.5, 29.5, 31.0)
    if metric == "o_swing_pct":
        # Pitcher O-Swing% (chase induced) ~33; ≥35 elite · ≥33 good · ≥30 avg
        return _grade_band(value, 30.0, 33.0, 35.0)
    if metric == "pitcher_soft_pct":
        # Higher Soft% = soft-contact arm (helps FILLER/under; soft for K overs)
        return _grade_band_desc(value, 17.0, 20.0, 22.0)
    if metric in ("k9", "last3_k9", "last3_k9_adj"):
        return _grade_band(value, 7.0, 8.5, 10.0)
    if metric in ("last3_ks", "last3_ks_adj"):
        return _grade_band(value, 3.5, 5.0, 6.5)
    if metric == "last3_opp_k_pct":
        # Higher = L3 faced juiced K clubs (form may be inflated)
        return _grade_band_desc(value, 20.5, 22.5, 24.5)
    if metric == "bb9":
        return _grade_band_desc(value, 2.2, 2.8, 3.5)
    if metric == "hr9":
        return _grade_band_desc(value, 0.9, 1.2, 1.5)
    if metric == "xfip":
        return _grade_band_desc(value, 3.40, 3.90, 4.50)
    if metric == "pitcher_k_pct":
        return _grade_band(value, 20.0, 24.0, 27.0)
    if metric == "pitcher_contact_pct":
        # Lower contact% = more whiff
        return _grade_band_desc(value, 72.0, 76.0, 80.0)
    if metric == "stuff_whiff_pct":
        return _grade_band(value, 20.0, 24.0, 28.0)
    return None


def _grade_class(metric: str, value: Any) -> str:
    band = _grade_for(metric, value)
    return f" grade-{band}" if band else ""


def _rate_chip(
    label: str,
    value: Any,
    metric: str,
    digits: int = 1,
    *,
    suffix: str = "",
    title: str = "",
    signed: bool = False,
    extra_class: str = "",
) -> str:
    """Colored pill for one Rates / form / arsenal matchup stat."""
    band = _grade_for(metric, value)
    shown = _fmt(value, digits, signed=signed)
    extra = f" {extra_class.strip()}" if extra_class else ""
    if shown == "—":
        return (
            f"<span class='rate-chip rate-na{extra}' title='{_esc(title or label)}'>"
            f"{_esc(label)} —</span>"
        )
    cls = f"rate-chip grade-{band}{extra}" if band else f"rate-chip{extra}"
    tip = title or label
    return (
        f"<span class='{cls}' title='{_esc(tip)}'>"
        f"<span class='rate-lab'>{_esc(label)}</span> "
        f"<span class='rate-val'>{_esc(shown)}{_esc(suffix)}</span>"
        f"</span>"
    )


def _is_fastball_pitch(pitch_type: Any, pitch_name: Any = None) -> bool:
    pt = str(pitch_type or "").upper()
    if pt in {"FF", "FA", "SI", "FC", "FT"}:
        return True
    if pt in {"FS", "CH", "CU", "SL", "ST", "SV", "KC", "EP", "SC"}:
        return False
    name = str(pitch_name or "").lower()
    return any(tok in name for tok in ("4-seam", "four-seam", "sinker", "cutter", "fastball"))


def _band_chip(label: str, band: str | None, *, title: str = "", value: str = "") -> str:
    """Colored pill from an explicit band (elite/high/mid/low)."""
    cls = f"rate-chip grade-{band}" if band else "rate-chip rate-na"
    val = value or label
    lab = label if value else ""
    if lab:
        return (
            f"<span class='{cls}' title='{_esc(title or label)}'>"
            f"<span class='rate-lab'>{_esc(lab)}</span> "
            f"<span class='rate-val'>{_esc(val)}</span>"
            f"</span>"
        )
    return (
        f"<span class='{cls}' title='{_esc(title or label)}'>"
        f"<span class='rate-val'>{_esc(val)}</span>"
        f"</span>"
    )


def _solo_grade_band(abs_grade: str | None) -> str | None:
    g = (abs_grade or "").strip().lower()
    return {
        "elite": "elite",
        "strong": "high",
        "avg": "mid",
        "soft": "low",
    }.get(g)


def _contact_grade_band(contact_grade: str | None) -> str | None:
    """whiff_prone helps overs (green); contact_heavy helps unders (red)."""
    g = (contact_grade or "").strip().lower()
    return {
        "whiff_prone": "elite",
        "neutral": "mid",
        "contact_heavy": "low",
    }.get(g)

def _lineup_label(src: Any) -> tuple[str, str]:
    if not src:
        return "miss", "none"
    s = str(src)
    if s == "official":
        return "official", "official"
    if s.startswith("prior:"):
        return "prior", f"prior {s[6:]}"
    return "miss", s


def _hand_label(code: Any, role: str) -> str:
    """role: 'P' -> LHP/RHP, 'B' -> LHB/RHB."""
    if not code:
        return ""
    c = str(code).upper()
    if c not in {"L", "R", "S"}:
        return ""
    if role == "P":
        return f"{c}HP"
    if c == "S":
        return "SHB"
    return f"{c}HB"


def _hand_side_class(code: Any) -> str:
    """CSS side class for L/R/S hand chips (green / amber / muted)."""
    c = str(code or "").upper()
    if c == "L":
        return "hand-l"
    if c == "R":
        return "hand-r"
    if c == "S":
        return "hand-s"
    return ""


def _hand_chip_html(code: Any, role: str, *, title: str = "") -> str:
    """Colored LHB/RHB (or LHP/RHP) chip for arsenal / lineup separation."""
    label = _hand_label(code, role)
    if not label:
        return ""
    side = _hand_side_class(code)
    tip = title or (
        "Left-handed batter"
        if label == "LHB"
        else "Right-handed batter"
        if label == "RHB"
        else "Switch-hitter"
        if label == "SHB"
        else "Left-handed pitcher"
        if label == "LHP"
        else "Right-handed pitcher"
        if label == "RHP"
        else "Handedness"
    )
    cls = f"hand {side}".strip()
    return (
        f" <span class='{cls}' title='{_esc(tip)}'>{_esc(label)}</span>"
    )


def rows_for_html(df: pd.DataFrame) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for _, r in df.iterrows():
        detail = r.get("batter_detail") or []
        if isinstance(detail, float) and pd.isna(detail):
            detail = []
        arsenal = r.get("arsenal") or []
        if isinstance(arsenal, float) and pd.isna(arsenal):
            arsenal = []
        pitch_avg = r.get("pitch_lineup_avg") or []
        if isinstance(pitch_avg, float) and pd.isna(pitch_avg):
            pitch_avg = []

        clean_detail = []
        for b in detail:
            pitches = []
            for p in b.get("pitches") or []:
                pitches.append(
                    {
                        "pitch_type": p.get("pitch_type"),
                        "pitch_name": p.get("pitch_name"),
                        "usage_pct": _json_safe(p.get("usage_pct")),
                        "usage_frac": _json_safe(p.get("usage_frac")),
                        "k_percent": _json_safe(p.get("k_percent")),
                        "whiff_percent": _json_safe(p.get("whiff_percent")),
                        "pa": _json_safe(p.get("pa")),
                        "k_source": p.get("k_source"),
                    }
                )
            clean_detail.append(
                {
                    "slot": _json_safe(b.get("slot")),
                    "batter_id": _json_safe(b.get("batter_id")),
                    "batter": b.get("batter"),
                    "bat_side": b.get("bat_side"),
                    "stand_used": b.get("stand_used"),
                    "usage_source": b.get("usage_source"),
                    "expected_k_pct": _json_safe(b.get("expected_k_pct")),
                    "expected_k_pct_raw": _json_safe(b.get("expected_k_pct_raw")),
                    "platoon_factor": _json_safe(b.get("platoon_factor")),
                    "expected_whiff_pct": _json_safe(b.get("expected_whiff_pct")),
                    "status": b.get("status"),
                    "barrel_pct": _json_safe(b.get("barrel_pct")),
                    "hard_hit_pct": _json_safe(b.get("hard_hit_pct")),
                    "xwoba": _json_safe(b.get("xwoba")),
                    "xba": _json_safe(b.get("xba")),
                    "avg_vs_hand": _json_safe(b.get("avg_vs_hand")),
                    "avg_vs_hand_source": b.get("avg_vs_hand_source"),
                    "hits_score": _json_safe(b.get("hits_score")),
                    "hr_rbi_score": _json_safe(b.get("hr_rbi_score")),
                    "hits_thin_sample": bool(b.get("hits_thin_sample")),
                    "pitches": pitches,
                }
            )

        clean_arsenal = []
        for p in arsenal:
            clean_arsenal.append(
                {
                    "pitch_type": p.get("pitch_type"),
                    "pitch_name": p.get("pitch_name"),
                    "usage_pct": _json_safe(p.get("usage_pct")),
                    "usage_frac": _json_safe(p.get("usage_frac")),
                    "usage_vs_lhb": _json_safe(p.get("usage_vs_lhb")),
                    "usage_vs_rhb": _json_safe(p.get("usage_vs_rhb")),
                    "pitcher_whiff_pct": _json_safe(p.get("pitcher_whiff_pct")),
                    "pitcher_velo": _json_safe(p.get("pitcher_velo")),
                    "pitcher_k_pct": _json_safe(p.get("pitcher_k_pct")),
                }
            )
        clean_pitch_avg = []
        for p in pitch_avg:
            clean_pitch_avg.append(
                {
                    "pitch_type": p.get("pitch_type"),
                    "pitch_name": p.get("pitch_name"),
                    "usage_pct": _json_safe(p.get("usage_pct")),
                    "usage_frac": _json_safe(p.get("usage_frac")),
                    "usage_vs_lhb": _json_safe(p.get("usage_vs_lhb")),
                    "usage_vs_rhb": _json_safe(p.get("usage_vs_rhb")),
                    "lineup_k_pct": _json_safe(p.get("lineup_k_pct")),
                    "batters_with_rate": _json_safe(p.get("batters_with_rate")),
                    "pitcher_whiff_pct": _json_safe(p.get("pitcher_whiff_pct")),
                    "pitcher_velo": _json_safe(p.get("pitcher_velo")),
                    "pitcher_k_pct": _json_safe(p.get("pitcher_k_pct")),
                }
            )

        rows.append(
            {
                "rank": _json_safe(r.get("rank")),
                "pitcher": r.get("pitcher"),
                "pitcher_id": _json_safe(r.get("pitcher_id")),
                "pitcher_team": r.get("pitcher_team"),
                "pitch_hand": r.get("pitch_hand"),
                "opponent": r.get("opponent"),
                "game": r.get("game"),
                "game_time_ct": r.get("game_time_ct"),
                "status": r.get("status"),
                "lineup_source": r.get("lineup_source"),
                "expected_ks": _json_safe(r.get("expected_ks")),
                "expected_ks_model": _json_safe(r.get("expected_ks_model")),
                "expected_k_pct": _json_safe(r.get("expected_k_pct")),
                "expected_ks_1x": _json_safe(r.get("expected_ks_1x")),
                "expected_whiff_pct": _json_safe(r.get("expected_whiff_pct")),
                "projected_ip": _json_safe(r.get("projected_ip")),
                "projected_bf": _json_safe(r.get("projected_bf")),
                "times_through_order": _json_safe(r.get("times_through_order")),
                "outing_source": r.get("outing_source"),
                "outing_role": r.get("outing_role"),
                "lineup_batters": _json_safe(r.get("lineup_batters")),
                "lineup_scored": _json_safe(r.get("lineup_scored")),
                "lineup_coverage": _json_safe(r.get("lineup_coverage")),
                "bf_scored": _json_safe(r.get("bf_scored")),
                "batters_faced_assumed": _json_safe(r.get("batters_faced_assumed")),
                "missing_batters": r.get("missing_batters") or "",
                "bb9": _json_safe(r.get("bb9")),
                "hr9": _json_safe(r.get("hr9")),
                "k9": _json_safe(r.get("k9")),
                "xfip": _json_safe(r.get("xfip")),
                "strike_pct": _json_safe(r.get("strike_pct")),
                "f_strike_pct": _json_safe(r.get("f_strike_pct")),
                "zone_pct": _json_safe(r.get("zone_pct")),
                "o_swing_pct": _json_safe(r.get("o_swing_pct")),
                "pitches": _json_safe(r.get("pitches")),
                "strikes": _json_safe(r.get("strikes")),
                "outing_risk": r.get("outing_risk"),
                "risk_flags": r.get("risk_flags") or "",
                "bf_risk_factor": _json_safe(r.get("bf_risk_factor")),
                "survival_flags": r.get("survival_flags") or "",
                "last3_ks": _json_safe(r.get("last3_ks")),
                "last3_k9": _json_safe(r.get("last3_k9")),
                "last3_ks_adj": _json_safe(r.get("last3_ks_adj")),
                "last3_k9_adj": _json_safe(r.get("last3_k9_adj")),
                "last3_opp_k_pct": _json_safe(r.get("last3_opp_k_pct")),
                "form_opp_factor": _json_safe(r.get("form_opp_factor")),
                "form_opp_note": r.get("form_opp_note") or "",
                "form_ks": _json_safe(r.get("form_ks")),
                "form_weight": _json_safe(r.get("form_weight")),
                "lineup_k_pct": _json_safe(r.get("lineup_k_pct")),
                "lineup_k_pct_vs_lhp": _json_safe(r.get("lineup_k_pct_vs_lhp")),
                "lineup_k_pct_vs_rhp": _json_safe(r.get("lineup_k_pct_vs_rhp")),
                "lineup_k_pct_vs_hand": _json_safe(r.get("lineup_k_pct_vs_hand")),
                "lineup_k_vs_hand_side": r.get("lineup_k_vs_hand_side") or "",
                "lineup_k_vs_hand_source": r.get("lineup_k_vs_hand_source") or "",
                "lineup_avg": _json_safe(r.get("lineup_avg")),
                "lineup_bb_pct": _json_safe(r.get("lineup_bb_pct")),
                "lineup_bip_pct": _json_safe(r.get("lineup_bip_pct")),
                "contact_grade": r.get("contact_grade") or "",
                "offense_source": r.get("offense_source"),
                "offense_factor": _json_safe(r.get("offense_factor")),
                "discipline_grade": r.get("discipline_grade") or "",
                "discipline_ks_factor": _json_safe(r.get("discipline_ks_factor")),
                "discipline_bf_factor": _json_safe(r.get("discipline_bf_factor")),
                "pitch_count_risk": r.get("pitch_count_risk") or "",
                "soft_contact_profile": bool(r.get("soft_contact_profile")),
                "profile_flags": r.get("profile_flags") or "",
                "arsenal_matchup_rank": _json_safe(r.get("arsenal_matchup_rank")),
                "arsenal_matchup_pctile": _json_safe(r.get("arsenal_matchup_pctile")),
                "matchup_grade": r.get("matchup_grade") or "",
                "arsenal_abs_grade": r.get("arsenal_abs_grade") or "",
                "arsenal_vs_league": _json_safe(r.get("arsenal_vs_league")),
                "arsenal_vs_opp": _json_safe(r.get("arsenal_vs_opp")),
                "stuff_whiff_pct": _json_safe(r.get("stuff_whiff_pct")),
                "stuff_fb_velo": _json_safe(r.get("stuff_fb_velo")),
                "stuff_fb_pitch": r.get("stuff_fb_pitch") or "",
                "stuff_grade": r.get("stuff_grade") or "",
                "stuff_source": r.get("stuff_source") or "",
                "spike_risk": bool(r.get("spike_risk")),
                "spike_flags": r.get("spike_flags") or "",
                "pitcher_k_pct": _json_safe(r.get("pitcher_k_pct")),
                "pitcher_contact_pct": _json_safe(r.get("pitcher_contact_pct")),
                "pitcher_gb_pct": _json_safe(r.get("pitcher_gb_pct")),
                "pitcher_fb_pct": _json_safe(r.get("pitcher_fb_pct")),
                "pitcher_iffb_pct": _json_safe(r.get("pitcher_iffb_pct")),
                "pitcher_soft_pct": _json_safe(r.get("pitcher_soft_pct")),
                "swstr_pct": _json_safe(r.get("swstr_pct")),
                "csw_pct": _json_safe(r.get("csw_pct")),
                "stuff_ceiling_bump": _json_safe(r.get("stuff_ceiling_bump")),
                "stuff_ceiling_note": r.get("stuff_ceiling_note") or "",
                "pitcher_style": r.get("pitcher_style") or "",
                "pitcher_style_flags": r.get("pitcher_style_flags") or "",
                "ticket_outlook": r.get("ticket_outlook") or "",
                "ticket_note": r.get("ticket_note") or "",
                "vs_team_games": _json_safe(r.get("vs_team_games")),
                "vs_team_ks": _json_safe(r.get("vs_team_ks")),
                "vs_team_pa": _json_safe(r.get("vs_team_pa")),
                "vs_team_k_pct": _json_safe(r.get("vs_team_k_pct")),
                "vs_team_avg": r.get("vs_team_avg") or "",
                "vs_team_ops": r.get("vs_team_ops") or "",
                "vs_team_bb": _json_safe(r.get("vs_team_bb")),
                "vs_team_hr": _json_safe(r.get("vs_team_hr")),
                "vs_team_home_g": _json_safe(r.get("vs_team_home_g")),
                "vs_team_home_ks": _json_safe(r.get("vs_team_home_ks")),
                "vs_team_home_avg_ks": _json_safe(r.get("vs_team_home_avg_ks")),
                "vs_team_away_g": _json_safe(r.get("vs_team_away_g")),
                "vs_team_away_ks": _json_safe(r.get("vs_team_away_ks")),
                "vs_team_away_avg_ks": _json_safe(r.get("vs_team_away_avg_ks")),
                "vs_team_recent": r.get("vs_team_recent") or "",
                "vs_team_games_detail": _clean_vs_team_games(
                    r.get("vs_team_games_detail")
                ),
                "arsenal": clean_arsenal,
                "pitch_lineup_avg": clean_pitch_avg,
                "batters": clean_detail,
            }
        )
    return rows


def _clean_vs_team_games(raw: Any) -> list[dict[str, Any]]:
    if raw is None or (isinstance(raw, float) and pd.isna(raw)):
        return []
    if isinstance(raw, str):
        return []
    out: list[dict[str, Any]] = []
    for g in list(raw or []):
        if not isinstance(g, dict):
            continue
        out.append(
            {
                "date": g.get("date") or "",
                "site": g.get("site") or ("H" if g.get("is_home") else "A"),
                "is_home": bool(g.get("is_home")),
                "ip": g.get("ip") or "",
                "ks": _json_safe(g.get("ks")),
                "bb": _json_safe(g.get("bb")),
                "hits": _json_safe(g.get("hits")),
                "er": _json_safe(g.get("er")),
                "hr": _json_safe(g.get("hr")),
                "bf": _json_safe(g.get("bf")),
                "games_started": _json_safe(g.get("games_started")),
            }
        )
    return out


def _render_vs_team_panel(row: dict[str, Any]) -> str:
    """Career + recent H/A game log for pitcher vs opposing batting team."""
    opp = row.get("opponent") or "opp"
    games = int(row.get("vs_team_games") or 0) if row.get("vs_team_games") is not None else 0
    detail = row.get("vs_team_games_detail") or []
    if games <= 0 and not detail:
        return (
            f"<p class='hint'>No prior pitcher-vs-{_esc(opp)} history in MLB "
            "career totals / recent game logs.</p>"
        )

    k_pct = row.get("vs_team_k_pct")
    summary = (
        f"<div class='vs-summary'>"
        f"<div><span class='meta-label'>Career vs {_esc(opp)}</span>"
        f"<span class='meta-value'>{games} G · "
        f"{_esc(row.get('vs_team_ks'))} K / {_esc(row.get('vs_team_pa'))} PA"
        f"{'' if k_pct is None else ' · K% ' + _fmt(k_pct, 1)}"
        f" · AVG {_esc(row.get('vs_team_avg') or '—')}"
        f" · OPS {_esc(row.get('vs_team_ops') or '—')}"
        f" · BB {_esc(row.get('vs_team_bb'))} · HR {_esc(row.get('vs_team_hr'))}"
        f"</span></div>"
    )
    hg = row.get("vs_team_home_g")
    ag = row.get("vs_team_away_g")
    if (hg or 0) or (ag or 0):
        summary += (
            "<div><span class='meta-label'>Site split (game logs)</span>"
            f"<span class='meta-value'>"
            f"HOME {_esc(hg)} G · {_esc(row.get('vs_team_home_ks'))} K"
            f"{'' if row.get('vs_team_home_avg_ks') is None else ' (' + _fmt(row.get('vs_team_home_avg_ks'), 1) + ' K/G)'}"
            f" · AWAY {_esc(ag)} G · {_esc(row.get('vs_team_away_ks'))} K"
            f"{'' if row.get('vs_team_away_avg_ks') is None else ' (' + _fmt(row.get('vs_team_away_avg_ks'), 1) + ' K/G)'}"
            f"</span></div>"
        )
    summary += "</div>"

    if not detail:
        return (
            summary
            + "<p class='hint'>Career totals only — no recent game-log rows "
            "in the pulled seasons.</p>"
        )

    rows_html = [
        "<div class='vs-table'>"
        "<div class='vs-head'>"
        "<div>Date</div><div>Site</div><div>IP</div><div>K</div>"
        "<div>BB</div><div>H</div><div>ER</div><div>HR</div><div>BF</div>"
        "</div>"
    ]
    for g in detail:
        site = g.get("site") or "A"
        site_word = "HOME" if site == "H" else "AWAY"
        site_cls = "home" if site == "H" else "away"
        rows_html.append(
            f"<div class='vs-row'>"
            f"<div>{_esc(g.get('date'))}</div>"
            f"<div><span class='site site-{site_cls}'>{site_word}</span></div>"
            f"<div>{_esc(g.get('ip'))}</div>"
            f"<div>{_esc(g.get('ks'))}</div>"
            f"<div>{_esc(g.get('bb'))}</div>"
            f"<div>{_esc(g.get('hits'))}</div>"
            f"<div>{_esc(g.get('er'))}</div>"
            f"<div>{_esc(g.get('hr'))}</div>"
            f"<div>{_esc(g.get('bf'))}</div>"
            f"</div>"
        )
    rows_html.append("</div>")
    rows_html.append(
        "<p class='hint'>Site is the <strong>pitcher’s</strong> home/away "
        "(HOME = pitched at home vs this batting team). Use with arsenal rank — "
        "history confirms or cautions the model side.</p>"
    )
    return summary + "".join(rows_html)


def _render_pitch_matrix(row: dict[str, Any], uid: str | None = None) -> str:
    """Stacked pitch sections + batter lists (no tab chips / horizontal scroll)."""
    _ = uid
    arsenal = row.get("pitch_lineup_avg") or row.get("arsenal") or []
    if not arsenal:
        return '<p class="hint">No arsenal pitch breakdown available.</p>'

    batters = row.get("batters") or []
    blocks: list[str] = []

    for i, p in enumerate(arsenal):
        pt = p.get("pitch_type")
        pname = p.get("pitch_name") or pt
        avg_k = p.get("lineup_k_pct")
        # Full pitch-header line as green/amber/red chips (good vs bad).
        meta_chips: list[str] = [
            _rate_chip(
                "overall",
                p.get("usage_pct"),
                "pitch_usage_pct",
                1,
                suffix="%",
                title="Pitch usage overall — green = featured pitch, red = sparse",
            )
        ]
        vs_l = p.get("usage_vs_lhb")
        vs_r = p.get("usage_vs_rhb")
        if vs_l is not None or vs_r is not None:
            meta_chips.append(
                _rate_chip(
                    "vs L",
                    vs_l,
                    "pitch_usage_vs_hand",
                    0,
                    suffix="%",
                    extra_class="hand-l",
                    title="Usage vs LHB — green = throws it a lot to lefties (platoon weight)",
                )
            )
            meta_chips.append(
                _rate_chip(
                    "vs R",
                    vs_r,
                    "pitch_usage_vs_hand",
                    0,
                    suffix="%",
                    extra_class="hand-r",
                    title="Usage vs RHB — green = throws it a lot to righties (platoon weight)",
                )
            )
        p_whiff = p.get("pitcher_whiff_pct")
        p_velo = p.get("pitcher_velo")
        if p_whiff is not None:
            meta_chips.append(
                _rate_chip(
                    "whiff",
                    p_whiff,
                    "pitch_whiff_pct",
                    1,
                    suffix="%",
                    title="Pitcher's whiff% on this pitch — green = miss / K helper, red = soft",
                )
            )
        if p_velo is not None:
            velo_metric = (
                "pitch_velo_fb"
                if _is_fastball_pitch(pt, pname)
                else "pitch_velo_offspeed"
            )
            meta_chips.append(
                _rate_chip(
                    "velo",
                    p_velo,
                    velo_metric,
                    1,
                    suffix=" mph",
                    title=(
                        "Fastball velo — green = plus heat"
                        if velo_metric == "pitch_velo_fb"
                        else "Offspeed/breaking velo (informational — not a good/bad K grade)"
                    ),
                )
            )
        meta_chips.append(
            _rate_chip(
                "lineup avg",
                avg_k,
                "batter_k_pct",
                1,
                suffix="%",
                title="Lineup-average K% vs this pitch — green helps the pitcher, red helps the batters",
            )
        )
        open_attr = " open" if i == 0 else ""

        rows_html: list[str] = []
        for b in batters:
            side_html = _hand_chip_html(b.get("bat_side"), "B")
            hit = next(
                (x for x in (b.get("pitches") or []) if x.get("pitch_type") == pt),
                {},
            )
            k = hit.get("k_percent")
            src = hit.get("k_source") or ""
            marker = "†" if src in {"league_pitch", "league_platoon"} else ""
            k_txt = "—" if k is None else f"{_fmt(k, 1)}%{marker}"
            width = 0 if k is None else max(4, min(100, float(k)))
            pa = hit.get("pa")
            pa_txt = "—" if pa is None else _fmt(pa, 0)
            k_grade = _grade_class("batter_k_pct", k)
            tip = (
                f"source {_esc(src or 'pitch')} · PA {_esc(pa_txt)} — "
                "green helps pitcher · amber medium · red helps batters"
            )
            rows_html.append(
                "<div class='pitch-row'>"
                "<div class='who'>"
                f"<span class='slot'>{_esc(b.get('slot'))}.</span>"
                f"<span class='name'>{_esc(b.get('batter') or '—')}{side_html}</span>"
                "</div>"
                "<div class='meter'>"
                f"<span class='bar' style='width:{width:.0f}%;{_heat_style(k)}'></span>"
                "</div>"
                f"<div class='kval{k_grade}' title='{tip}'>"
                f"{k_txt}</div>"
                "</div>"
            )

        width_avg = 0 if avg_k is None else max(4, min(100, float(avg_k)))
        avg_grade = _grade_class("batter_k_pct", avg_k)
        rows_html.append(
            "<div class='pitch-row avg'>"
            "<div class='who'><span class='name'>Lineup avg</span></div>"
            "<div class='meter'>"
            f"<span class='bar' style='width:{width_avg:.0f}%;{_heat_style(avg_k)}'></span>"
            "</div>"
            f"<div class='kval{avg_grade}' "
            "title='Lineup avg — green helps pitcher · amber medium · red helps batters'>"
            f"{'—' if avg_k is None else _fmt(avg_k, 1) + '%'}</div>"
            "</div>"
        )
        blocks.append(
            f"<details class='pitch-block'{open_attr}>"
            "<summary>"
            f"<span class='pname'>{_esc(pname)}</span>"
            f"<span class='pmeta'>{''.join(meta_chips)}</span>"
            "</summary>"
            f"<div class='pitch-list'>{''.join(rows_html)}</div>"
            "</details>"
        )

    return (
        "<div class='pitch-stack'>"
        f"{''.join(blocks)}"
        "<p class='hint'>"
        "Pitch header chips are green/amber/red by whether the number helps the "
        "pitcher: <strong>overall</strong> (featured vs sparse) · "
        "<strong>vs L / vs R</strong> (platoon usage weight; L amber edge / R green edge) · "
        "<strong>whiff</strong> (miss%) · <strong>velo</strong> (FB heat only) · "
        "<strong>lineup avg</strong> (K% vs this pitch). "
        "Open a pitch for each batter’s K% — same green = helps pitcher / "
        "<strong class='hint-red'>red</strong> = helps batters scale. "
        "Rates prefer true K% vs this pitcher’s hand when sample ≥15 PA; "
        "else overall pitch K%; "
        "<code>†</code> = same-handed league average. "
        "Whiff / velo are own-stuff ceiling — do not change Exp K."
        "</p>"
        "</div>"
    )



def _render_lineup_panel(row: dict[str, Any]) -> str:
    cards = []
    for b in row.get("batters") or []:
        miss = b.get("status") != "ok"
        k_raw = None if miss else b.get("expected_k_pct")
        k = "n/a" if miss else f"{_fmt(k_raw, 1)}%"
        k_grade = "" if miss else _grade_class("batter_k_pct", k_raw)
        side_html = _hand_chip_html(b.get("bat_side"), "B")
        hits = b.get("hits_score")
        hits_html = ""
        if hits is not None:
            hits_html = (
                f"<span class='hits-meta' title='Hits prop score (not used in expected Ks)'>"
                f"hits {_fmt(hits, 0)}"
                f"{'' if b.get('barrel_pct') is None else ' · brl ' + _fmt(b.get('barrel_pct'), 1) + '%'}"
                f"{'' if b.get('hard_hit_pct') is None else ' · hh ' + _fmt(b.get('hard_hit_pct'), 1) + '%'}"
                f"</span>"
            )
        tip = (
            ""
            if miss
            else " title='Arsenal-weighted K% — green helps pitcher · "
            "amber medium · red helps batters'"
        )
        cards.append(
            f"<div class='batter {'missing' if miss else ''}'>"
            f"<span><span class='slot'>{_esc(b.get('slot'))}.</span> "
            f"{_esc(b.get('batter') or '—')}{side_html}{hits_html}</span>"
            f"<span class='k{k_grade}'{tip}>{k}</span>"
            "</div>"
        )
    if not cards:
        return "<div class='empty'>No batter detail</div>"
    return (
        f"<div class='batter-grid'>{''.join(cards)}</div>"
        "<p class='hint'>Right-side values are arsenal-weighted <strong>K%</strong> vs this "
        "starter — <strong>green</strong> helps the pitcher, "
        "<strong class='hint-amber'>amber</strong> medium, "
        "<strong class='hint-red'>red</strong> helps the batters. "
        "Hits / barrel / hard-hit scores are a separate Hits-prop layer and "
        "<strong>do not</strong> change expected strikeouts.</p>"
    )


def _render_hits_board(hits_board: list[dict[str, Any]] | None) -> str:
    if not hits_board:
        return (
            "<section class='hits-board' id='hitsBoard'>"
            "<h2>Hits board <span>(display-only)</span></h2>"
            "<p class='hits-lede'>No hits props ranked for this slate yet.</p>"
            "</section>"
        )
    rows = []
    for r in hits_board[:15]:
        rows.append(
            "<div class='hits-row'>"
            f"<span class='rk'>{_esc(r.get('rank'))}</span>"
            f"<span class='name'>{_esc(r.get('batter') or '—')}</span>"
            f"<span class='vs'>vs {_esc(r.get('pitcher') or '—')} "
            f"({_esc(r.get('pitch_hand') or '?')}HP)</span>"
            f"<span class='num'>{_fmt(r.get('hits_score'), 0)}</span>"
            f"<span class='num'>{_fmt(r.get('hr_rbi_score'), 0)}</span>"
            f"<span class='num'>{_fmt(r.get('barrel_pct'), 1)}</span>"
            f"<span class='num'>{_fmt(r.get('hard_hit_pct'), 1)}</span>"
            f"<span class='num'>{_fmt(r.get('avg_vs_hand'), 3)}</span>"
            "</div>"
        )
    return (
        "<section class='hits-board' id='hitsBoard'>"
        "<h2>Hits board <span>(display-only)</span></h2>"
        "<p class='hits-lede'>Barrel%, hard-hit%, xwOBA, and AVG vs pitcher hand — "
        "ranked for Hits / H+R+RBI props. This board never feeds the strikeout model.</p>"
        "<div class='hits-colhead'>"
        "<div>#</div><div>Batter</div><div>Matchup</div>"
        "<div>Hits</div><div>H+R+RBI</div><div>Brl%</div><div>HH%</div><div>AVG vs</div>"
        "</div>"
        f"<div class='hits-list'>{''.join(rows)}</div>"
        "</section>"
    )


def _render_matchup_card(row: dict[str, Any], idx: int) -> str:
    kind, label = _lineup_label(row.get("lineup_source"))
    tto = row.get("times_through_order")
    tto_s = "—" if tto is None else f"{_fmt(tto)}×"
    status = row.get("status") or ""
    scored = status == "ok" and row.get("expected_ks") is not None
    pitcher_hand = _hand_label(row.get("pitch_hand"), "P")
    hand_html = _hand_chip_html(row.get("pitch_hand"), "P")
    outlook = (row.get("ticket_outlook") or "").strip()
    search = " ".join(
        str(x)
        for x in [
            row.get("pitcher"),
            pitcher_hand,
            row.get("pitcher_team"),
            row.get("opponent"),
            row.get("game"),
            row.get("game_time_ct"),
            row.get("lineup_source"),
            status,
            outlook,
            row.get("matchup_grade"),
        ]
        if x
    ).lower()

    uid = f"m{idx}"
    game_time = row.get("game_time_ct")
    game_html = f"<div class='game'>{_esc(row.get('game') or '—')}"
    if game_time:
        game_html += f"<span class='gametime'>{_esc(game_time)}</span>"
    game_html += "</div>"
    ks_grade = _grade_class("expected_ks", row.get("expected_ks"))
    ip_grade = _grade_class("projected_ip", row.get("projected_ip"))
    tto_grade = _grade_class("tto", row.get("times_through_order"))
    kpct_grade = _grade_class("expected_k_pct", row.get("expected_k_pct"))

    badge_html = f"<span class='badge {kind}'>{_esc(label)}</span>"
    if outlook:
        badge_html += (
            f"<span class='outlook outlook-{_esc(outlook.lower())}'>"
            f"{_esc(outlook.replace('_', ' '))}</span>"
        )
    # Primary: absolute solo arsenal-vs-THIS-lineup grade (not slate-relative).
    # Secondary chips: slate arsenal # and opp lineup K% # (today's relative only).
    ark = row.get("arsenal_matchup_rank")
    opp_rank = row.get("opp_lineup_k_rank")
    abs_grade = (row.get("arsenal_abs_grade") or "").strip()
    chips: list[str] = []
    if abs_grade and scored:
        chips.append(
            f"<span class='ark ark-abs ark-{_esc(abs_grade)}' "
            f"title='Solo arsenal vs this batting team "
            f"(absolute expected K% bands: elite≥24, strong≥22.5, avg≥20, soft&lt;20). "
            f"Does not depend on other pitchers today.'>"
            f"{_esc(abs_grade.upper())}</span>"
        )
    if row.get("spike_risk") and scored:
        spike_title = row.get("spike_flags") or "high K ceiling"
        chips.append(
            f"<span class='ark ark-spike' "
            f"title='SPIKE / stuff ceiling: {_esc(spike_title)}. "
            f"Do not auto soft-under (prefer U6.5+ or pass). "
            f"Does not change Exp K.'>SPIKE</span>"
        )
    # Pitcher style lives next to the name (not buried in the K% chip stack).
    pstyle = (row.get("pitcher_style") or "").strip().lower()
    style_labels = {
        "whiff": ("WHIFF", "K-first / strikeout outs"),
        "contact_gb": ("GB", "ground-ball / in-play outs"),
        "fly_popup": ("FLY", "fly-ball + popup (IFFB) outs"),
        "balanced": ("BAL", "mixed out-getting profile"),
    }
    style_chip_html = ""
    if pstyle and scored:
        chip_txt, chip_desc = style_labels.get(
            pstyle, (pstyle.upper()[:4], pstyle)
        )
        style_flags = row.get("pitcher_style_flags") or ""
        style_chip_html = (
            f"<span class='style-chip ark-pstyle-{_esc(pstyle)}' "
            f"title='Pitcher out-getting style: {_esc(chip_desc)}"
            f"{'' if not style_flags else ' — ' + _esc(style_flags)}. "
            f"Season FanGraphs K%/Contact%/GB%/FB%/IFFB — confirmation only; "
            f"does not change Exp K.'>"
            f"<span class='style-chip-lab'>STYLE</span> {_esc(chip_txt)}"
            f"</span>"
        )
    if opp_rank is not None and scored:
        chips.append(
            f"<span class='ark ark-opp' "
            f"title='Opposing batting-team K% rank on slate "
            f"(#1 = highest opp lineup K%) — relative only'>#{_esc(opp_rank)}</span>"
        )
    if ark is not None and scored:
        slate_grade = (row.get("matchup_grade") or "").strip()
        chips.append(
            f"<span class='ark ark-slate ark-{_esc(slate_grade or 'avg')}' "
            f"title='Slate rank of arsenal K% vs lineup "
            f"(#1 = best matchup among today\\'s starters) — relative only'>"
            f"#{_esc(ark)}</span>"
        )
    chips_html = (
        f"<span class='rank-chips'>{''.join(chips)}</span>" if chips else ""
    )

    def _stat(classes: str, value_html: str, lab: str, title: str) -> str:
        return (
            f"<div class='num {classes}' title='{_esc(title)}'>"
            f"<span class='nval'>{value_html}</span>"
            f"<span class='nlab'>{_esc(lab)}</span>"
            f"</div>"
        )

    summary = (
        "<div class='summary-grid'>"
        f"<div class='rank'>{_esc(row.get('rank') if row.get('rank') is not None else '—')}</div>"
        "<div class='who'>"
        f"<div class='pitcher'>{_esc(row.get('pitcher') or '—')}{hand_html}"
        f"{style_chip_html}</div>"
        f"<div class='sub'>{_esc(row.get('pitcher_team') or '?')} vs "
        f"{_esc(row.get('opponent') or '?')}"
        f"{'' if status in ('', 'ok') else ' · ' + _esc(status)}</div>"
        "</div>"
        f"{game_html}"
        "<div class='stat-row'>"
        f"{_stat(f'ks{ks_grade}', _fmt(row.get('expected_ks')), 'Exp K', 'Expected strikeouts')}"
        f"{_stat(f'ip{ip_grade}', _fmt(row.get('projected_ip'), 1), 'IP', 'Projected innings pitched')}"
        f"{_stat(f'tto{tto_grade}', tto_s, 'TTO', 'Times through the order')}"
        f"<div class='num kpct{kpct_grade}' title='Arsenal K% vs opposing lineup'>"
        f"{chips_html}"
        f"<span class='nval'>"
        f"<span class='kpct-val'>{_fmt(row.get('expected_k_pct'))}</span>"
        f"</span>"
        f"<span class='nlab'>K%</span>"
        f"</div>"
        "</div>"
        f"<div class='badges'>{badge_html}</div>"
        "</div>"
    )

    risk = row.get("outing_risk") or "clear"
    risk_flags = row.get("risk_flags") or ""
    role = row.get("outing_role") or "starter"
    role_html = ""
    if role and role != "starter":
        role_html = (
            f"<span class='role role-{_esc(role)}'>{_esc(role.replace('_', ' '))}</span>"
        )

    bf = (
        row.get("projected_bf")
        if row.get("projected_bf") is not None
        else row.get("batters_faced_assumed")
    )
    cover = (
        "—"
        if row.get("lineup_coverage") is None
        else f"{int(round(100 * float(row['lineup_coverage'])))}%"
    )
    outing_val = (
        f"{_fmt(row.get('projected_ip'), 1)} IP · {tto_s} · BF {_esc(bf)} · cover {cover}"
    )
    rates_chips = [
        _rate_chip(
            "BB/9",
            row.get("bb9"),
            "bb9",
            2,
            title="Walk rate — lower is better for command / length",
        ),
        _rate_chip(
            "HR/9",
            row.get("hr9"),
            "hr9",
            2,
            title="Home-run rate — lower is better",
        ),
        _rate_chip(
            "xFIP",
            row.get("xfip"),
            "xfip",
            2,
            title="Expected FIP — lower is better",
        ),
        _rate_chip(
            "K9",
            row.get("k9"),
            "k9",
            1,
            title="Season K/9 — higher helps K scripts",
        ),
    ]
    if row.get("strike_pct") is not None:
        rates_chips.append(
            _rate_chip(
                "Strike%",
                row.get("strike_pct"),
                "strike_pct",
                1,
                title="Strikes ÷ pitches · ≥~65 confirms attack-plate overs",
            )
        )
    if row.get("f_strike_pct") is not None:
        rates_chips.append(
            _rate_chip(
                "F-Strike%",
                row.get("f_strike_pct"),
                "f_strike_pct",
                1,
                title="First-pitch strike rate — higher = more ahead counts",
            )
        )
    if row.get("zone_pct") is not None:
        rates_chips.append(
            _rate_chip(
                "Zone%",
                row.get("zone_pct"),
                "zone_pct",
                1,
                title="In-zone rate · ≥~43 with high Strike% = attacks the plate",
            )
        )
    if row.get("swstr_pct") is not None:
        rates_chips.append(
            _rate_chip(
                "SwStr%",
                row.get("swstr_pct"),
                "swstr_pct",
                1,
                title="Swinging-strike rate — miss confirm (does not flip arsenal side)",
            )
        )
    if row.get("o_swing_pct") is not None:
        rates_chips.append(
            _rate_chip(
                "O-Swing%",
                row.get("o_swing_pct"),
                "o_swing_pct",
                1,
                title="Chase rate induced (FanGraphs O-Swing%) — higher = more chase; Rates confirm only",
            )
        )
    if row.get("csw_pct") is not None:
        rates_chips.append(
            _rate_chip(
                "CSW%",
                row.get("csw_pct"),
                "csw_pct",
                1,
                title="Called + swinging strike (FanGraphs C+SwStr%) — command/miss pack",
            )
        )
    if row.get("pitcher_soft_pct") is not None:
        rates_chips.append(
            _rate_chip(
                "Soft%",
                row.get("pitcher_soft_pct"),
                "pitcher_soft_pct",
                1,
                title="Soft-contact rate · ≥~20 helps FILLER / UNDER_OK confirms",
            )
        )
    form_chips: list[str] = []
    if row.get("last3_ks") is not None:
        form_chips.append(
            _rate_chip(
                "L3 K",
                row.get("last3_ks"),
                "last3_ks",
                1,
                title="Avg strikeouts over last 3 starts (raw)",
            )
        )
    if row.get("last3_k9") is not None:
        form_chips.append(
            _rate_chip(
                "L3 K/9",
                row.get("last3_k9"),
                "last3_k9",
                1,
                title="K/9 over last 3 starts (raw)",
            )
        )
    if row.get("last3_k9_adj") is not None:
        tip = "L3 K/9 scaled by league K% ÷ mean opponent-team K% faced"
        note = (row.get("form_opp_note") or "").strip()
        if note:
            tip = f"{tip} · {note}"
        form_chips.append(
            _rate_chip(
                "L3 K/9 adj",
                row.get("last3_k9_adj"),
                "last3_k9_adj",
                1,
                title=tip,
            )
        )
    if row.get("last3_opp_k_pct") is not None:
        form_chips.append(
            _rate_chip(
                "L3 opp K%",
                row.get("last3_opp_k_pct"),
                "last3_opp_k_pct",
                1,
                title=(
                    row.get("form_opp_note")
                    or "Mean season K% of teams faced in last 3 starts"
                ),
            )
        )
    form_html = (
        "".join(form_chips)
        if form_chips
        else "<span class='rate-chip rate-na'>no L3 form</span>"
    )
    rates_html = "".join(rates_chips) + form_html

    stuff_bits: list[str] = []
    if row.get("stuff_whiff_pct") is not None:
        sg = (row.get("stuff_grade") or "").strip()
        tip = f"Usage-weighted pitcher whiff%{'' if not sg else ' (' + sg + ')'}"
        stuff_bits.append(
            _rate_chip(
                "stuff whiff",
                row.get("stuff_whiff_pct"),
                "stuff_whiff_pct",
                1,
                suffix="%" + (f" ({sg})" if sg else ""),
                title=tip,
            )
        )
    if row.get("stuff_fb_velo") is not None:
        pitch = row.get("stuff_fb_pitch") or "FB"
        stuff_bits.append(
            f"<span class='rate-chip rate-na' title='Primary fastball velocity'>"
            f"<span class='rate-lab'>{_esc(pitch)}</span> "
            f"<span class='rate-val'>{_esc(_fmt(row.get('stuff_fb_velo'), 1))} mph</span>"
            f"</span>"
        )
    if row.get("spike_risk"):
        stuff_bits.append(
            f"<span class='rate-chip rate-spike' title='Stuff / K9 ceiling — no soft U6'>"
            f"<span class='rate-lab'>SPIKE</span> "
            f"<span class='rate-val'>{_esc(row.get('spike_flags') or '')}</span>"
            f"</span>"
        )
    bump = row.get("stuff_ceiling_bump")
    if bump is not None and float(bump or 0) > 0:
        tip = row.get("stuff_ceiling_note") or "Attack-plate stuff bump on Exp K"
        stuff_bits.append(
            f"<span class='rate-chip grade-high' title='{_esc(tip)}'>"
            f"<span class='rate-lab'>stuff bump</span> "
            f"<span class='rate-val'>+{_esc(_fmt(bump, 2))}</span>"
            f"</span>"
        )
    stuff_val = "".join(stuff_bits)

    style_bits: list[str] = []
    pstyle = (row.get("pitcher_style") or "").strip().lower()
    if pstyle:
        style_names = {
            "whiff": "K-first (WHIFF)",
            "contact_gb": "GB / in-play",
            "fly_popup": "Fly / popup",
            "balanced": "Balanced",
        }
        style_bits.append(
            f"<span class='rate-chip rate-na'>"
            f"<span class='rate-val'>{_esc(style_names.get(pstyle, pstyle))}</span>"
            f"</span>"
        )
        if row.get("pitcher_k_pct") is not None:
            style_bits.append(
                _rate_chip(
                    "K%",
                    row.get("pitcher_k_pct"),
                    "pitcher_k_pct",
                    1,
                    title="Season pitcher K% — higher confirms WHIFF",
                )
            )
        if row.get("pitcher_contact_pct") is not None:
            style_bits.append(
                _rate_chip(
                    "Con%",
                    row.get("pitcher_contact_pct"),
                    "pitcher_contact_pct",
                    1,
                    title="Season contact% — lower = more swing-and-miss",
                )
            )
        if row.get("pitcher_gb_pct") is not None:
            style_bits.append(
                f"<span class='rate-chip rate-na' title='Ground-ball rate'>"
                f"<span class='rate-lab'>GB%</span> "
                f"<span class='rate-val'>{_esc(_fmt(row.get('pitcher_gb_pct'), 1))}</span>"
                f"</span>"
            )
        if row.get("pitcher_fb_pct") is not None:
            style_bits.append(
                f"<span class='rate-chip rate-na' title='Fly-ball rate'>"
                f"<span class='rate-lab'>FB%</span> "
                f"<span class='rate-val'>{_esc(_fmt(row.get('pitcher_fb_pct'), 1))}</span>"
                f"</span>"
            )
        if row.get("pitcher_iffb_pct") is not None:
            style_bits.append(
                f"<span class='rate-chip rate-na' title='Infield-fly rate'>"
                f"<span class='rate-lab'>IFFB%</span> "
                f"<span class='rate-val'>{_esc(_fmt(row.get('pitcher_iffb_pct'), 1))}</span>"
                f"</span>"
            )
    style_val = "".join(style_bits)
    opp = row.get("opponent") or "opp"
    matchup_bits: list[str] = []
    if abs_grade:
        matchup_bits.append(
            _band_chip(
                "solo",
                _solo_grade_band(abs_grade),
                value=f"{abs_grade.upper()} vs {opp}",
                title=(
                    "Solo arsenal vs this nine — picks the side "
                    "(ELITE/STRONG over · SOFT under · AVG usually pass)"
                ),
            )
        )
    if row.get("expected_k_pct") is not None:
        matchup_bits.append(
            _rate_chip(
                "arsenal K%",
                row.get("expected_k_pct"),
                "expected_k_pct",
                1,
                title=(
                    f"Arsenal-weighted K% vs lineup · "
                    f"ELITE≥{ABS_MATCHUP_ELITE:g} STRONG≥{ABS_MATCHUP_STRONG:g} "
                    f"AVG≥{ABS_MATCHUP_AVG:g} SOFT<{ABS_MATCHUP_AVG:g}"
                ),
            )
        )
    if row.get("arsenal_vs_league") is not None:
        matchup_bits.append(
            _rate_chip(
                "vs league",
                row.get("arsenal_vs_league"),
                "arsenal_vs_league",
                1,
                signed=True,
                title="Arsenal K% minus league ~22.5% — positive helps overs",
            )
        )
    if row.get("arsenal_vs_opp") is not None:
        matchup_bits.append(
            _rate_chip(
                "vs opp K%",
                row.get("arsenal_vs_opp"),
                "arsenal_vs_opp",
                1,
                signed=True,
                title="Mix vs lineup raw K% — positive = mix beats the nine's tendency",
            )
        )
    if ark is not None:
        slate_g = (row.get("matchup_grade") or "").strip()
        slate_band = _solo_grade_band(slate_g) if slate_g else None
        slate_txt = f"#{ark}" + (f" {slate_g}" if slate_g else "")
        matchup_bits.append(
            _band_chip(
                "slate",
                slate_band,
                value=slate_txt,
                title="Slate-relative arsenal rank only — secondary to solo grade",
            )
        )
    # Prefer opp K% vs this pitcher's hand; keep overall as secondary chip.
    opp_hand = row.get("lineup_k_pct_vs_hand")
    opp_side = str(row.get("lineup_k_vs_hand_side") or "").strip().upper()
    if opp_hand is not None:
        side_lab = f"vs {opp_side}HP" if opp_side in ("L", "R") else "vs hand"
        matchup_bits.append(
            _rate_chip(
                f"opp K% {side_lab}",
                opp_hand,
                "opp_k_pct",
                1,
                title=(
                    f"Lineup season K% {side_lab} — primary opp-K confirm "
                    "(higher helps overs)"
                ),
            )
        )
        if row.get("lineup_k_pct") is not None:
            src = row.get("offense_source") or ""
            matchup_bits.append(
                _rate_chip(
                    "opp K% all",
                    row.get("lineup_k_pct"),
                    "opp_k_pct",
                    1,
                    title=(
                        "Overall lineup K%"
                        + (f" ({src})" if src else "")
                        + " — secondary to vs-hand"
                    ),
                )
            )
    elif row.get("lineup_k_pct") is not None:
        src = row.get("offense_source") or ""
        tip = "Opposing lineup K%" + (f" ({src})" if src else "")
        matchup_bits.append(
            _rate_chip(
                "opp K%",
                row.get("lineup_k_pct"),
                "opp_k_pct",
                1,
                title=tip + " — higher helps overs",
            )
        )
    if row.get("lineup_bip_pct") is not None:
        cg = (row.get("contact_grade") or "").strip()
        bip_band = _contact_grade_band(cg) or _grade_for(
            "opp_bip_pct", row.get("lineup_bip_pct")
        )
        bip_label = "opp BIP"
        bip_val = _fmt(row.get("lineup_bip_pct"), 1) + "%"
        if cg:
            bip_val += f" {cg.replace('_', ' ')}"
        matchup_bits.append(
            _band_chip(
                bip_label,
                bip_band,
                value=bip_val,
                title=(
                    "Lineup balls-in-play % — whiff_prone helps overs · "
                    "contact_heavy helps unders"
                ),
            )
        )
    if row.get("lineup_bb_pct") is not None:
        matchup_bits.append(
            _rate_chip(
                "opp BB%",
                row.get("lineup_bb_pct"),
                "opp_bb_pct",
                1,
                title="Opposing lineup BB% — high = patient / pitch-count risk",
            )
        )
    grade = (row.get("discipline_grade") or "").strip()
    if grade:
        disc_band = {
            "aggressive": "high",
            "free_swing": "elite",
            "neutral": "mid",
            "patient": "low",
            "three_true": "mid",
        }.get(grade.lower())
        matchup_bits.append(
            _band_chip(
                "disc",
                disc_band,
                value=grade.replace("_", " "),
                title="Plate-discipline grade for the opposing nine",
            )
        )
    pc = (row.get("pitch_count_risk") or "").strip()
    if pc and pc not in ("neutral", "low"):
        pc_band = "low" if pc in ("elevated", "high") else "mid"
        matchup_bits.append(
            _band_chip(
                "pitch-count",
                pc_band,
                value=pc,
                title="Pitch-count risk from patient / walk-heavy nines",
            )
        )
    matchup_val = "".join(matchup_bits) if matchup_bits else "—"
    vs_g = row.get("vs_team_games")
    vs_bits: list[str] = []
    if vs_g is not None and int(vs_g or 0) > 0:
        vs_bits.append(f"{int(vs_g)} G")
        if row.get("vs_team_k_pct") is not None:
            vs_bits.append(f"K% {_fmt(row.get('vs_team_k_pct'), 1)}")
        if row.get("vs_team_ops"):
            vs_bits.append(f"OPS {_esc(row.get('vs_team_ops'))}")
        hg = int(row.get("vs_team_home_g") or 0)
        ag = int(row.get("vs_team_away_g") or 0)
        if hg or ag:
            vs_bits.append(
                f"HOME {hg}G/{int(row.get('vs_team_home_ks') or 0)}K · "
                f"AWAY {ag}G/{int(row.get('vs_team_away_ks') or 0)}K"
            )
    # Always surface a couple recent H/A lines in the meta strip (not tab-only).
    recent_preview = ""
    detail = row.get("vs_team_games_detail") or []
    if detail:
        bits = []
        for g in detail[:3]:
            site = g.get("site") or ("H" if g.get("is_home") else "A")
            site_word = "HOME" if site == "H" else "AWAY"
            bits.append(f"{g.get('date')} {site_word} {g.get('ks')}K")
        recent_preview = " · ".join(bits)
    elif row.get("vs_team_recent"):
        # CSV reload path: recent is already a "; "-joined string with H/A codes.
        parts = [p.strip() for p in str(row.get("vs_team_recent")).split(";") if p.strip()]
        recent_preview = " · ".join(parts[:3]).replace(" H:", " HOME:").replace(" A:", " AWAY:")
    vs_val = " · ".join(vs_bits) if vs_bits else "no prior history"
    if recent_preview:
        vs_val = f"{vs_val}<br><span class='vs-recent'>{_esc(recent_preview)}</span>" if vs_bits else _esc(recent_preview)

    risk_chip = (
        f"<span class='risk risk-{_esc(risk)}'>risk {_esc(risk)}"
        f"{'' if not risk_flags else ' · ' + _esc(risk_flags)}</span>"
    )

    head = (
        "<div class='meta-strip'>"
        # Card read order: solo arsenal → style → stuff → rates → outing → history.
        "<div class='meta-cell meta-matchup'>"
        "<span class='meta-label'>Arsenal matchup</span>"
        f"<span class='meta-value meta-rates'>{matchup_val}</span>"
        "</div>"
        "<div class='meta-cell meta-pstyle'>"
        "<span class='meta-label'>Pitcher style (Ks vs BIP outs)</span>"
        f"<span class='meta-value meta-rates'>"
        f"{style_val if style_val else '—'}"
        "</span>"
        "</div>"
        "<div class='meta-cell meta-stuff'>"
        "<span class='meta-label'>Stuff ceiling (velo / whiff)</span>"
        f"<span class='meta-value meta-rates'>"
        f"{stuff_val if stuff_val else '—'}"
        "</span>"
        "</div>"
        "<div class='meta-cell meta-rates-cell'>"
        "<span class='meta-label'>Rates / form</span>"
        f"<span class='meta-value meta-rates'>{rates_html} {risk_chip}</span>"
        "</div>"
        "<div class='meta-cell'>"
        "<span class='meta-label'>Outing / form</span>"
        f"<span class='meta-value'>{outing_val}{role_html}</span>"
        "</div>"
        "<div class='meta-cell meta-history'>"
        f"<span class='meta-label'>vs {_esc(opp)} history (HOME/AWAY)</span>"
        f"<span class='meta-value'>{vs_val}</span>"
        "</div>"
        "</div>"
    )
    ticket_note = (row.get("ticket_note") or "").strip()
    # Banner for flagged outlooks (FILLER / MATCHUP_OK / SPIKE / THIN_TOTAL / UNDER_OK).
    if outlook:
        note = _esc(ticket_note) if ticket_note else matchup_val
        head += (
            f"<div class='outlook-banner outlook-{_esc(outlook.lower())}'>"
            f"<strong>{_esc(outlook.replace('_', ' '))}</strong>"
            f"<span>{note}</span>"
            "</div>"
        )

    # CSS-only tabs — full-width segmented control.
    tabs = (
        f"<div class='tabs' role='tablist'>"
        f"<input type='radio' name='tab-{uid}' id='tab-{uid}-pitches' checked />"
        f"<label class='tab' for='tab-{uid}-pitches'>"
        f"<span class='tab-full'>Arsenal vs lineup</span>"
        f"<span class='tab-short'>Arsenal</span>"
        f"</label>"
        f"<input type='radio' name='tab-{uid}' id='tab-{uid}-lineup' />"
        f"<label class='tab' for='tab-{uid}-lineup'>"
        f"<span class='tab-full'>Batting order</span>"
        f"<span class='tab-short'>Order</span>"
        f"</label>"
        f"<input type='radio' name='tab-{uid}' id='tab-{uid}-history' />"
        f"<label class='tab' for='tab-{uid}-history'>"
        f"<span class='tab-full'>vs Team history</span>"
        f"<span class='tab-short'>History</span>"
        f"</label>"
        f"<div class='tab-panel panel-pitches'>{_render_pitch_matrix(row, uid)}</div>"
        f"<div class='tab-panel panel-lineup'>{_render_lineup_panel(row)}</div>"
        f"<div class='tab-panel panel-history'>{_render_vs_team_panel(row)}</div>"
        f"</div>"
    )

    return (
        f"<details class='matchup' data-search='{_esc(search)}' "
        f"data-lineup='{_esc(row.get('lineup_source') or '')}' "
        f"data-status='{'scored' if scored else 'missing'}' "
        f"data-expected-ks='{_json_safe(row.get('expected_ks'))}' "
        f"data-projected-ip='{_json_safe(row.get('projected_ip'))}' "
        f"data-tto='{_json_safe(row.get('times_through_order'))}' "
        f"data-kpct='{_json_safe(row.get('expected_k_pct'))}' "
        f"data-rank='{_json_safe(row.get('rank'))}' "
        f"data-pitcher='{_esc(row.get('pitcher') or '')}'>"
        f"<summary>{summary}</summary>"
        f"<div class='detail'>{head}{tabs}</div>"
        "</details>"
    )


def _key_chip(text: str, css: str, title: str = "") -> str:
    tip = f" title='{_esc(title)}'" if title else ""
    return f"<span class='key-chip {_esc(css)}'{tip}>{_esc(text)}</span>"


def _render_model_keys(*, avg_strike_pct: float | None = None) -> str:
    """Top-of-board legend: color-coded BIP / solo / style / outlook keys."""
    bip_chips = (
        _key_chip(
            f"whiff_prone ≤{WHIFF_PRONE_BIP:g}%",
            "key-bip-whiff",
            "Low BIP / high-K nines — helps overs",
        )
        + _key_chip(
            f"league ~{LEAGUE_BIP_PCT:g}%",
            "key-bip-league",
            "Neutral contact environment",
        )
        + _key_chip(
            f"contact_heavy ≥{CONTACT_HEAVY_BIP:g}%",
            "key-bip-contact",
            "High BIP nines — helps unders (also ≥69% with K% ≤19.5)",
        )
    )
    bip_note = (
        "Low BIP helps overs · high BIP helps unders"
        " · contact_heavy also if BIP ≥69% with K% ≤19.5."
    )
    solo_chips = (
        _key_chip(f"ELITE ≥{ABS_MATCHUP_ELITE:g}%", "ark ark-elite")
        + _key_chip(f"STRONG ≥{ABS_MATCHUP_STRONG:g}%", "ark ark-strong")
        + _key_chip(f"AVG ≥{ABS_MATCHUP_AVG:g}%", "ark ark-avg")
        + _key_chip(f"SOFT <{ABS_MATCHUP_AVG:g}%", "ark ark-soft")
    )
    solo_note = (
        f"Arsenal K% vs this nine (league ~{LEAGUE_K_PCT:g}%)."
        " Side first — Exp K sizes the line."
    )
    style_chips = (
        _key_chip("WHIFF", "ark-pstyle-whiff", "Trust K totals")
        + _key_chip("GB", "ark-pstyle-contact_gb", "Ground-ball / BIP outs")
        + _key_chip("FLY", "ark-pstyle-fly_popup", "Fly / popup BIP outs")
        + _key_chip("BAL", "ark-pstyle-balanced", "Mixed profile — caution on juiced totals")
    )
    style_note = "WHIFF = trust K totals · GB/FLY = BIP outs (thin juiced totals) · BAL = caution."
    outlook_chips = (
        _key_chip(
            "TRUST",
            "outlook outlook-trust",
            f"ELITE/STRONG + WHIFF + Exp K ≥{TRUST_TOTAL_EXP_KS:g}",
        )
        + _key_chip(
            "THIN TOTAL",
            "outlook outlook-thin_total",
            "High Exp K but GB/FLY — O3.5 / thin O4.5 only",
        )
        + _key_chip(
            "UNDER OK",
            "outlook outlook-under_ok",
            f"SOFT + ≥{UNDER_CONFIRM_MIN:g} of GB/FLY · contact_heavy · "
            f"Exp K ≤{UNDER_CONFIRM_EXP_KS:g} · Soft%≥20",
        )
        + _key_chip("SPIKE", "outlook outlook-spike", "No soft U6")
        + _key_chip("MATCHUP OK", "outlook outlook-matchup_ok", "Thin O3.5 only")
        + _key_chip("FILLER", "outlook outlook-filler", "Pass K overs")
    )
    outlook_note = (
        f"TRUST needs Exp K ≥{TRUST_TOTAL_EXP_KS:g} · UNDER_OK needs"
        f" ≥{UNDER_CONFIRM_MIN:g} confirms (incl Soft%) · SPIKE blocks soft U6."
    )
    strike_chips = (
        _key_chip(
            "Strike% ≥66",
            "rate-chip grade-elite",
            "Elite command — sizes up WHIFF overs",
        )
        + _key_chip(
            "≥65",
            "rate-chip grade-high",
            "Attack-plate confirm (≥~65 Strike% / ≥~43 Zone%)",
        )
        + _key_chip(
            "~63–65",
            "rate-chip grade-mid",
            "Average strike rate",
        )
        + _key_chip(
            "<63",
            "rate-chip grade-low",
            "Soft for overs — does not auto-under SPIKE/WHIFF",
        )
        + _key_chip(
            "Zone% ≥43",
            "rate-chip grade-high",
            "In-zone attack — pair with high Strike%",
        )
        + _key_chip(
            "Zone% <40",
            "rate-chip grade-low",
            "Off-plate / nibble profile",
        )
    )
    if avg_strike_pct is not None:
        strike_chips += _key_chip(
            f"slate avg {_fmt(avg_strike_pct, 1)}%",
            "rate-chip grade-mid",
            "Average Strike% across today's scored starters",
        )
    strike_note = (
        "Green = good for K scripts · amber = average · red = soft for overs. "
        "Rates chips: Strike%/Zone%/SwStr%/O-Swing%/CSW% (miss+chase+command) · Soft% "
        "(elevated helps FILLER/under). L3 K/9 adj = form scaled for opponent K% faced. "
        "Command/chase confirms the script — they do not flip the side. "
        "Attack-plate + WHIFF + strong stuff can add a tiny Exp K bump."
    )
    return (
        "<div class='model-keys' aria-label='Model keys'>"
        "<div class='keys-title'>Keys — what to aim for</div>"
        "<div class='key-row'>"
        "<span class='key-lab'>Opp BIP</span>"
        f"<span class='key-val'><span class='key-chips'>{bip_chips}</span>"
        f"<span class='key-note'>{bip_note}</span></span>"
        "</div>"
        "<div class='key-row'>"
        "<span class='key-lab'>Strike%</span>"
        f"<span class='key-val'><span class='key-chips'>{strike_chips}</span>"
        f"<span class='key-note'>{strike_note}</span></span>"
        "</div>"
        "<div class='key-row'>"
        "<span class='key-lab'>Solo grade</span>"
        f"<span class='key-val'><span class='key-chips'>{solo_chips}</span>"
        f"<span class='key-note'>{solo_note}</span></span>"
        "</div>"
        "<div class='key-row'>"
        "<span class='key-lab'>Style</span>"
        f"<span class='key-val'><span class='key-chips'>{style_chips}</span>"
        f"<span class='key-note'>{style_note}</span></span>"
        "</div>"
        "<div class='key-row'>"
        "<span class='key-lab'>Outlook</span>"
        f"<span class='key-val'><span class='key-chips'>{outlook_chips}</span>"
        f"<span class='key-note'>{outlook_note}</span></span>"
        "</div>"
        "</div>"
    )


def write_interactive_html(
    path: str,
    df: pd.DataFrame,
    *,
    game_date: str,
    batters_faced: float | None = None,
    hits_board: list[dict[str, Any]] | None = None,
) -> None:
    rows = rows_for_html(df)
    # Opposing batting-team K% rank on this slate (#1 = highest lineup K%).
    opp_scored = [
        (i, float(r["lineup_k_pct"]))
        for i, r in enumerate(rows)
        if r.get("status") == "ok" and r.get("lineup_k_pct") is not None
    ]
    opp_scored.sort(key=lambda x: -x[1])
    for opp_rank, (i, _) in enumerate(opp_scored, start=1):
        rows[i]["opp_lineup_k_rank"] = opp_rank

    scored = [r for r in rows if r.get("status") == "ok" and r.get("expected_ks") is not None]
    official = sum(1 for r in scored if r.get("lineup_source") == "official")
    avg_ip = (
        sum(float(r["projected_ip"]) for r in scored if r.get("projected_ip") is not None)
        / len([r for r in scored if r.get("projected_ip") is not None])
        if any(r.get("projected_ip") is not None for r in scored)
        else None
    )
    avg_tto = (
        sum(
            float(r["times_through_order"])
            for r in scored
            if r.get("times_through_order") is not None
        )
        / len([r for r in scored if r.get("times_through_order") is not None])
        if any(r.get("times_through_order") is not None for r in scored)
        else None
    )
    strike_vals = [
        float(r["strike_pct"])
        for r in scored
        if r.get("strike_pct") is not None
    ]
    avg_strike_pct = (sum(strike_vals) / len(strike_vals)) if strike_vals else None

    # Prefer scored first, then missing — same as CLI rank order already in df.
    cards = "\n".join(_render_matchup_card(r, i) for i, r in enumerate(rows))
    hits_html = _render_hits_board(hits_board)

    generated = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    meta_bits = [
        ("Date", game_date),
        ("Generated", generated),
        ("Avg proj IP", _fmt(avg_ip, 1) if avg_ip is not None else "—"),
        ("Avg TTO", f"{_fmt(avg_tto)}×" if avg_tto is not None else "—"),
        (
            "Avg Strike%",
            f"{_fmt(avg_strike_pct, 1)}%" if avg_strike_pct is not None else "—",
        ),
        ("Scored", str(len(scored))),
        ("Official lineups", f"{official}/{len(scored)}"),
    ]
    meta_html = "".join(
        f"<span class='chip'>{_esc(k)}: <strong>{_esc(v)}</strong></span>"
        for k, v in meta_bits
    )
    freshness = (
        f"<div class='freshness' role='status'>"
        f"<strong>Bookmark:</strong> <a href='{STABLE_BOARD_URL}'>{_esc(STABLE_BOARD_URL)}</a>"
        f" — same link every day; tracks <code>main</code> and updates in place. "
        f"Optional Pages URL after one Settings enable: "
        f"<a href='{STABLE_BOARD_PAGES_URL}'>{_esc(STABLE_BOARD_PAGES_URL)}</a>. "
        f"Slate <strong>{_esc(game_date)}</strong> · built <strong>{_esc(generated)}</strong> · "
        f"official lineups <strong>{official}/{len(scored)}</strong>. "
        f"Hard-refresh before tickets; never use old commit / htmlpreview links."
        f"</div>"
    )
    model_keys = _render_model_keys(avg_strike_pct=avg_strike_pct)

    payload = {
        "generated_at": generated,
        "game_date": game_date,
        "stable_board_url": STABLE_BOARD_URL,
        "batters_faced_override": batters_faced,
        "avg_projected_ip": avg_ip,
        "avg_times_through": avg_tto,
        "avg_strike_pct": avg_strike_pct,
        "row_count": len(rows),
        "official_lineups": official,
        "hits_board_count": len(hits_board or []),
    }

    html = HTML_TEMPLATE
    html = html.replace("__META_CHIPS__", meta_html)
    html = html.replace("__FRESHNESS__", freshness)
    html = html.replace("__MODEL_KEYS__", model_keys)
    html = html.replace("__HITS_BOARD__", hits_html)
    html = html.replace("__MATCHUP_CARDS__", cards)
    html = html.replace("__DATA_JSON__", json.dumps(payload, ensure_ascii=False))
    out = Path(path)
    out.write_text(html, encoding="utf-8")
    # Keep index.html in sync so the stable GitHub Pages root URL never goes stale.
    if out.name != "index.html":
        out.with_name("index.html").write_text(html, encoding="utf-8")


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>K-Matchup — lineup strikeout projections</title>
<meta http-equiv="Cache-Control" content="no-cache, no-store, must-revalidate" />
<meta http-equiv="Pragma" content="no-cache" />
<meta http-equiv="Expires" content="0" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Archivo+Black&family=Manrope:wght@400;500;600;700&display=swap" rel="stylesheet" />
<style>
  :root {
    --bg0: #e8f0e4;
    --bg1: #f7f3ea;
    --ink: #14201a;
    --muted: #5c6b62;
    --line: rgba(20, 32, 26, 0.12);
    --accent: #0f6a4d;
    --warn: #9a5b12;
    --ok: #0f6a4d;
    --panel: rgba(255, 252, 246, 0.92);
    --shadow: 0 18px 50px rgba(20, 32, 26, 0.08);
    --radius: 18px;
    --mono: "Manrope", system-ui, sans-serif;
    --display: "Archivo Black", "Arial Black", sans-serif;
  }
  * { box-sizing: border-box; }
  html {
    height: auto;
    overflow-x: hidden;
    overflow-y: scroll;
    -webkit-overflow-scrolling: touch;
  }
  body {
    margin: 0;
    min-height: 100%;
    height: auto;
    overflow-x: hidden;
    overflow-y: visible;
    color: var(--ink);
    font-family: var(--mono);
    background:
      radial-gradient(1200px 600px at 10% -10%, rgba(15, 106, 77, 0.18), transparent 55%),
      radial-gradient(900px 500px at 100% 0%, rgba(154, 91, 18, 0.12), transparent 50%),
      linear-gradient(165deg, var(--bg0), var(--bg1) 55%, #eef4ea);
  }
  .wrap {
    width: min(1120px, calc(100% - 2rem));
    margin: 0 auto;
    padding: 2.25rem 0 6rem;
    max-width: 100%;
    min-width: 0;
  }
  .board,
  details.matchup,
  .detail,
  .tabs,
  .tab-panel {
    max-width: 100%;
    min-width: 0;
  }
  .hero { display: grid; gap: 0.85rem; margin-bottom: 1.5rem; }
  .brand {
    font-family: var(--display);
    font-size: clamp(2.6rem, 7vw, 4.4rem);
    letter-spacing: -0.03em;
    line-height: 0.92;
    margin: 0;
  }
  .brand span { color: var(--accent); }
  .lede { max-width: 40rem; margin: 0; color: var(--muted); font-size: 1.05rem; line-height: 1.45; }
  .meta { display: flex; flex-wrap: wrap; gap: 0.55rem 0.75rem; }
  .chip {
    display: inline-flex; gap: 0.35rem; align-items: center;
    padding: 0.35rem 0.7rem; border: 1px solid var(--line);
    background: rgba(255,255,255,0.55); border-radius: 999px;
    font-size: 0.82rem; color: var(--muted);
  }
  .chip strong { color: var(--ink); }
  .freshness {
    margin: 0;
    padding: 0.7rem 0.9rem;
    border-radius: 12px;
    border: 1px solid rgba(15, 106, 77, 0.28);
    background: rgba(15, 106, 77, 0.08);
    color: var(--ink);
    font-size: 0.88rem;
    line-height: 1.4;
  }
  .freshness a { color: var(--accent); font-weight: 700; word-break: break-all; }
  .controls {
    display: grid;
    grid-template-columns: 1.4fr repeat(3, auto);
    gap: 0.75rem;
    align-items: end;
    margin-bottom: 1rem;
    position: sticky;
    top: 0;
    z-index: 5;
    padding: 0.75rem 0.85rem;
    border: 1px solid var(--line);
    border-radius: 14px;
    background: rgba(247, 243, 234, 0.94);
    backdrop-filter: blur(8px);
  }
  @media (max-width: 820px) { .controls { grid-template-columns: 1fr 1fr; } }
  @media (max-width: 540px) { .controls { grid-template-columns: 1fr; } }
  label {
    display: grid; gap: 0.35rem; font-size: 0.78rem; font-weight: 600;
    letter-spacing: 0.04em; text-transform: uppercase; color: var(--muted);
  }
  input[type="search"], select {
    width: 100%; appearance: none; border: 1px solid var(--line);
    background: var(--panel); color: var(--ink); border-radius: 12px;
    padding: 0.7rem 0.85rem; font: inherit; font-size: 0.95rem; outline: none;
  }
  .board {
    display: grid;
    gap: 0.65rem;
    overflow: visible;
  }
  .colhead, .summary-grid {
    display: grid;
    grid-template-columns: 3rem minmax(9rem, 1.35fr) minmax(5.5rem, 0.85fr) repeat(4, minmax(4.6rem, 0.85fr)) minmax(5.5rem, 0.9fr);
    gap: 0.75rem 0.9rem;
    align-items: center;
  }
  .colhead {
    padding: 0 0.95rem;
    font-size: 0.72rem; letter-spacing: 0.05em; text-transform: uppercase; color: var(--muted);
  }
  /* Desktop: children flow into the parent 8-col grid. Mobile: own equal row. */
  .stat-row { display: contents; }
  @media (max-width: 900px) {
    .colhead { display: none; }
    .summary-grid {
      grid-template-columns: 2.4rem minmax(0, 1fr) auto;
      column-gap: 0.75rem;
      row-gap: 0.8rem;
      grid-template-areas:
        "rank who badges"
        "rank game game"
        "stats stats stats";
    }
    .summary-grid .rank { grid-area: rank; }
    .summary-grid .who { grid-area: who; }
    .summary-grid .badges { grid-area: badges; justify-self: end; }
    .summary-grid .game { grid-area: game; }
    .summary-grid .stat-row {
      display: grid;
      grid-area: stats;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 0.7rem 1rem;
      width: 100%;
      min-width: 0;
      align-items: start;
    }
    .summary-grid .stat-row .num {
      min-width: 0;
      width: 100%;
      padding-right: 0.15rem;
      box-sizing: border-box;
    }
  }
  details.matchup {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    overflow: visible;
  }
  details.matchup[hidden] { display: none !important; }
  summary {
    list-style: none;
    cursor: pointer;
    padding: 0.9rem 0.95rem;
    border-radius: var(--radius);
  }
  summary::-webkit-details-marker { display: none; }
  summary:hover { background: rgba(15, 106, 77, 0.05); }
  .rank { font-family: var(--display); color: var(--accent); font-size: 1.05rem; }
  .pitcher { font-weight: 700; }
  .hand {
    display: inline-block;
    margin-left: 0.35rem;
    padding: 0.05rem 0.4rem;
    border-radius: 999px;
    border: 1px solid var(--line);
    background: rgba(255,255,255,0.7);
    color: var(--muted);
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.02em;
    vertical-align: middle;
  }
  /* Arsenal / lineup hand separation — L amber · R green · S muted */
  .hand.hand-l {
    background: rgba(154, 91, 18, 0.14);
    border-color: rgba(154, 91, 18, 0.35);
    color: #8a4b0f;
  }
  .hand.hand-r {
    background: rgba(15, 106, 77, 0.14);
    border-color: rgba(15, 106, 77, 0.32);
    color: #0f6a4d;
  }
  .hand.hand-s {
    background: rgba(20, 32, 26, 0.08);
    border-color: rgba(20, 32, 26, 0.18);
    color: var(--muted);
  }
  .pitch-stack .pmeta {
    display: inline-flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.28rem 0.35rem;
  }
  .pitch-stack .pmeta .rate-chip {
    margin: 0;
  }
  /* Platoon usage chips keep good/bad fill + L/R edge for separation */
  .pitch-stack .pmeta .rate-chip.hand-l {
    box-shadow: inset 3px 0 0 #c47a1a;
  }
  .pitch-stack .pmeta .rate-chip.hand-r {
    box-shadow: inset 3px 0 0 #0f6a4d;
  }
  .sub { color: var(--muted); font-size: 0.8rem; margin-top: 0.12rem; }
  .game {
    font-weight: 650;
    line-height: 1.25;
  }
  .gametime {
    display: block;
    margin-top: 0.15rem;
    color: var(--muted);
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.02em;
  }
  .num {
    display: grid;
    justify-items: start;
    gap: 0.18rem;
    min-width: 3.75rem;
    padding-right: 0.25rem;
    font-variant-numeric: tabular-nums;
    font-weight: 700;
    line-height: 1.2;
  }
  .nval {
    display: inline-flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.35rem;
    white-space: nowrap;
  }
  .nlab {
    font-size: 0.62rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--muted);
    white-space: nowrap;
  }
  .ks .nval { font-size: 1.05rem; }
  .grade-low { color: #8c2828; }
  .grade-mid { color: #8a4b0f; }
  .grade-high { color: #0f6a4d; }
  .grade-elite {
    color: #064832;
    background: rgba(15, 106, 77, 0.14);
    border-radius: 8px;
    padding: 0.22rem 0.55rem 0.28rem;
    justify-self: start;
  }
  .grade-elite .nlab { color: rgba(6, 72, 50, 0.72); }
  .grade-legend {
    display: flex;
    flex-wrap: wrap;
    align-items: center;
    gap: 0.45rem 0.7rem;
    margin-top: 0.15rem;
    font-size: 0.78rem;
    color: var(--muted);
  }
  .grade-legend .swatch {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    font-weight: 700;
    font-variant-numeric: tabular-nums;
  }
  .grade-legend .swatch::before {
    content: "";
    width: 0.55rem;
    height: 0.55rem;
    border-radius: 999px;
    background: currentColor;
  }
  .model-keys {
    display: grid;
    gap: 0.45rem;
    margin-top: 0.35rem;
    padding: 0.75rem 0.85rem;
    border: 1px solid var(--line);
    border-radius: 14px;
    background: rgba(255,255,255,0.55);
  }
  .model-keys .keys-title {
    font-size: 0.68rem;
    font-weight: 800;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--muted);
  }
  .model-keys .key-row {
    display: grid;
    grid-template-columns: 6.5rem 1fr;
    gap: 0.55rem 0.75rem;
    align-items: start;
    font-size: 0.82rem;
    line-height: 1.4;
    color: var(--ink);
  }
  @media (max-width: 640px) {
    .model-keys .key-row { grid-template-columns: 1fr; gap: 0.15rem; }
  }
  .model-keys .key-lab {
    font-size: 0.68rem;
    font-weight: 800;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    color: var(--muted);
    padding-top: 0.12rem;
  }
  .model-keys .key-val {
    display: grid;
    gap: 0.3rem;
    font-weight: 600;
    color: var(--ink);
  }
  .model-keys .key-chips {
    display: flex;
    flex-wrap: wrap;
    gap: 0.35rem;
    align-items: center;
  }
  .model-keys .key-note {
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--muted);
    line-height: 1.35;
  }
  .model-keys .key-chip {
    display: inline-flex;
    align-items: center;
    padding: 0.18rem 0.5rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.02em;
    white-space: nowrap;
    border: 1px solid transparent;
  }
  .model-keys .key-chip.ark {
    border-radius: 6px;
    letter-spacing: 0.03em;
  }
  .model-keys .key-bip-whiff {
    background: rgba(15, 106, 77, 0.16);
    color: #064832;
    border-color: rgba(15, 106, 77, 0.28);
  }
  .model-keys .key-bip-league {
    background: rgba(20, 32, 26, 0.08);
    color: var(--muted);
    border-color: rgba(20, 32, 26, 0.16);
  }
  .model-keys .key-bip-contact {
    background: rgba(30, 90, 160, 0.14);
    color: #1a4a7a;
    border-color: rgba(30, 90, 160, 0.28);
  }
  .outlook-trust {
    background: rgba(15, 106, 77, 0.18);
    color: #064832;
  }
  .badge {
    display: inline-flex; padding: 0.22rem 0.55rem; border-radius: 999px;
    font-size: 0.72rem; font-weight: 700;
  }
  .badge.official { background: rgba(15, 106, 77, 0.12); color: var(--ok); }
  .badge.prior { background: rgba(154, 91, 18, 0.14); color: var(--warn); }
  .badge.miss { background: rgba(20, 32, 26, 0.08); color: var(--muted); }
  .badges {
    display: flex; flex-wrap: wrap; gap: 0.3rem; justify-content: flex-end;
    align-items: center;
  }
  .kpct {
    min-width: 5.5rem;
  }
  .rank-chips {
    display: flex;
    flex-direction: column;
    align-items: flex-start;
    gap: 0.2rem;
    margin-bottom: 0.12rem;
  }
  .ark-opp {
    background: rgba(20, 32, 26, 0.10);
    color: var(--ink);
  }
  .kpct-val { font-variant-numeric: tabular-nums; font-weight: 700; }
  .ark {
    display: inline-flex; align-items: center;
    padding: 0.1rem 0.4rem; border-radius: 6px;
    font-size: 0.68rem; font-weight: 700; letter-spacing: 0.02em;
    background: rgba(20, 32, 26, 0.08); color: var(--muted);
  }
  .ark-elite { background: rgba(15, 106, 77, 0.16); color: #064832; }
  .ark-strong { background: rgba(15, 106, 77, 0.10); color: var(--ok); }
  .ark-avg { background: rgba(154, 91, 18, 0.12); color: var(--warn); }
  .ark-soft { background: rgba(140, 40, 40, 0.12); color: #8c2828; }
  .ark-spike {
    background: rgba(154, 40, 18, 0.16);
    color: #8a2410;
    font-weight: 700;
    letter-spacing: 0.03em;
  }
  .style-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.28rem;
    margin-left: 0.4rem;
    padding: 0.12rem 0.5rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 800;
    letter-spacing: 0.04em;
    vertical-align: middle;
    white-space: nowrap;
    border: 1px solid transparent;
  }
  .style-chip-lab {
    opacity: 0.7;
    font-size: 0.62rem;
    letter-spacing: 0.06em;
  }
  .ark-pstyle-whiff, .style-chip.ark-pstyle-whiff {
    background: rgba(15, 106, 77, 0.16);
    color: #064832;
    border-color: rgba(15, 106, 77, 0.28);
  }
  .ark-pstyle-contact_gb, .style-chip.ark-pstyle-contact_gb {
    background: rgba(40, 72, 120, 0.14);
    color: #1e3a5f;
    border-color: rgba(40, 72, 120, 0.28);
  }
  .ark-pstyle-fly_popup, .style-chip.ark-pstyle-fly_popup {
    background: rgba(120, 72, 40, 0.14);
    color: #5c3418;
    border-color: rgba(120, 72, 40, 0.28);
  }
  .ark-pstyle-balanced, .style-chip.ark-pstyle-balanced {
    background: rgba(20, 32, 26, 0.10);
    color: var(--ink);
    border-color: rgba(20, 32, 26, 0.18);
  }
  .meta-pstyle {
    border-color: rgba(40, 72, 120, 0.30);
    background: rgba(40, 72, 120, 0.07);
    grid-column: 1 / -1;
  }
  .ark-abs {
    font-size: 0.62rem;
    letter-spacing: 0.04em;
    min-width: 3.4rem;
    justify-content: center;
  }
  .ark-slate { opacity: 0.85; }
  .risk {
    display: inline-flex; padding: 0.15rem 0.45rem; border-radius: 999px;
    font-size: 0.72rem; font-weight: 700; letter-spacing: 0.02em;
  }
  .risk-clear { background: rgba(15, 106, 77, 0.12); color: var(--ok); }
  .risk-low { background: rgba(154, 91, 18, 0.12); color: var(--warn); }
  .risk-medium { background: rgba(154, 91, 18, 0.18); color: #8a4b0f; }
  .risk-high { background: rgba(140, 40, 40, 0.14); color: #8c2828; }
  .role {
    display: inline-flex; margin-left: 0.35rem; padding: 0.15rem 0.45rem;
    border-radius: 999px; font-size: 0.72rem; font-weight: 700;
  }
  .role-opener_likely { background: rgba(140, 40, 40, 0.14); color: #8c2828; }
  .role-swingman { background: rgba(154, 91, 18, 0.16); color: #8a4b0f; }
  .outlook {
    display: inline-flex; padding: 0.15rem 0.45rem; border-radius: 999px;
    font-size: 0.72rem; font-weight: 700; letter-spacing: 0.02em;
  }
  .outlook-filler { background: rgba(140, 40, 40, 0.14); color: #8c2828; }
  .outlook-spike { background: rgba(154, 40, 18, 0.16); color: #8a2410; }
  .outlook-matchup_ok { background: rgba(15, 106, 77, 0.12); color: var(--ok); }
  .outlook-thin_total { background: rgba(154, 91, 18, 0.16); color: #8a4b0f; }
  .outlook-under_ok { background: rgba(30, 90, 160, 0.14); color: #1a4a7a; }
  .detail {
    padding: 0 1rem 1.15rem;
    border-top: 1px solid var(--line);
    background: rgba(20, 32, 26, 0.03);
    overflow: visible;
    animation: detailIn 0.22s ease-out;
  }
  @keyframes detailIn {
    from { opacity: 0; transform: translateY(-4px); }
    to { opacity: 1; transform: none; }
  }
  .meta-strip {
    display: grid;
    grid-template-columns: 1fr;
    gap: 0.45rem;
    margin: 0.85rem 0 0.75rem;
  }
  .meta-cell {
    padding: 0.55rem 0.7rem;
    border: 1px solid var(--line);
    border-radius: 12px;
    background: rgba(255,255,255,0.7);
    min-width: 0;
  }
  .meta-matchup {
    border-color: rgba(15, 106, 77, 0.28);
    background: rgba(15, 106, 77, 0.06);
  }
  .meta-history {
    border-color: rgba(30, 90, 160, 0.28);
    background: rgba(30, 90, 160, 0.06);
    grid-column: 1 / -1;
  }
  .meta-history .vs-recent {
    display: block;
    margin-top: 0.25rem;
    color: var(--ink);
    font-size: 0.84rem;
    font-weight: 600;
  }
  .meta-label {
    display: block;
    font-size: 0.68rem; font-weight: 700; letter-spacing: 0.06em;
    text-transform: uppercase; color: var(--muted); margin-bottom: 0.25rem;
  }
  .meta-value {
    display: flex; flex-wrap: wrap; align-items: center; gap: 0.3rem;
    font-size: 0.84rem; line-height: 1.4; color: var(--ink); font-weight: 600;
  }
  .meta-value.meta-rates {
    gap: 0.35rem;
  }
  .rate-chip {
    display: inline-flex;
    align-items: baseline;
    gap: 0.22rem;
    padding: 0.16rem 0.45rem;
    border-radius: 999px;
    border: 1px solid rgba(20, 32, 26, 0.14);
    background: rgba(20, 32, 26, 0.06);
    color: var(--ink);
    font-size: 0.78rem;
    font-weight: 700;
    font-variant-numeric: tabular-nums;
    white-space: nowrap;
    line-height: 1.25;
  }
  .rate-chip .rate-lab {
    font-size: 0.68rem;
    font-weight: 800;
    letter-spacing: 0.03em;
    text-transform: uppercase;
    opacity: 0.78;
  }
  .rate-chip .rate-val {
    font-weight: 800;
  }
  .rate-chip.grade-elite {
    background: rgba(15, 106, 77, 0.18);
    color: #064832;
    border-color: rgba(15, 106, 77, 0.32);
  }
  .rate-chip.grade-high {
    background: rgba(15, 106, 77, 0.11);
    color: #0f6a4d;
    border-color: rgba(15, 106, 77, 0.24);
  }
  .rate-chip.grade-mid {
    background: rgba(154, 91, 18, 0.12);
    color: #8a4b0f;
    border-color: rgba(154, 91, 18, 0.26);
  }
  .rate-chip.grade-low {
    background: rgba(140, 40, 40, 0.12);
    color: #8c2828;
    border-color: rgba(140, 40, 40, 0.26);
  }
  .rate-chip.rate-na {
    background: rgba(20, 32, 26, 0.05);
    color: var(--muted);
    border-color: rgba(20, 32, 26, 0.12);
    font-weight: 600;
  }
  .rate-chip.rate-spike {
    background: rgba(154, 40, 18, 0.14);
    color: #8a2410;
    border-color: rgba(154, 40, 18, 0.28);
  }
  .model-keys .key-chip.rate-chip {
    border-radius: 999px;
  }
  .outlook-banner {
    display: grid;
    grid-template-columns: auto 1fr;
    gap: 0.55rem 0.75rem;
    align-items: start;
    margin: 0 0 0.85rem;
    padding: 0.65rem 0.8rem;
    border-radius: 12px;
    border: 1px solid var(--line);
    font-size: 0.84rem; line-height: 1.4;
  }
  .outlook-banner strong {
    font-size: 0.72rem; letter-spacing: 0.05em; text-transform: uppercase;
  }
  .outlook-banner.outlook-filler {
    background: rgba(140, 40, 40, 0.08); border-color: rgba(140, 40, 40, 0.22);
    color: #6e2020;
  }
  .outlook-banner.outlook-spike {
    background: rgba(154, 40, 18, 0.10); border-color: rgba(154, 40, 18, 0.28);
    color: #7a220e;
  }
  .outlook-banner.outlook-matchup_ok {
    background: rgba(15, 106, 77, 0.08); border-color: rgba(15, 106, 77, 0.22);
    color: #0a4a36;
  }
  .outlook-banner.outlook-thin_total {
    background: rgba(154, 91, 18, 0.10); border-color: rgba(154, 91, 18, 0.28);
    color: #6e3a0c;
  }
  .outlook-banner.outlook-under_ok {
    background: rgba(30, 90, 160, 0.08); border-color: rgba(30, 90, 160, 0.24);
    color: #163a5c;
  }
  @media (max-width: 560px) {
    .outlook-banner { grid-template-columns: 1fr; gap: 0.25rem; }
  }
  .tabs {
    display: grid;
    grid-template-columns: 1fr 1fr 1fr;
    gap: 0;
    align-items: stretch;
    width: 100%;
    margin-top: 0.15rem;
    padding: 0.25rem;
    border: 1px solid var(--line);
    border-radius: 14px;
    background: rgba(255,255,255,0.55);
  }
  .tabs > input {
    position: absolute;
    width: 1px; height: 1px;
    margin: -1px; padding: 0; border: 0;
    clip: rect(0 0 0 0);
    overflow: hidden;
    white-space: nowrap;
  }
  .tab {
    display: inline-flex; align-items: center; justify-content: center;
    border: 0; background: transparent;
    color: var(--muted); border-radius: 10px; padding: 0.55rem 0.75rem;
    font-size: 0.86rem; font-weight: 700; cursor: pointer;
    transition: background 0.15s ease, color 0.15s ease, transform 0.15s ease;
  }
  .tab:hover { color: var(--ink); }
  .tab-short { display: none; }
  .tabs > input:checked + .tab {
    background: var(--accent); color: #fff;
    box-shadow: 0 6px 16px rgba(15, 106, 77, 0.22);
  }
  .tab-panel {
    display: none;
    grid-column: 1 / -1;
    margin-top: 0.55rem;
    padding: 0.15rem 0.2rem 0.35rem;
    animation: panelIn 0.18s ease-out;
  }
  @keyframes panelIn {
    from { opacity: 0; transform: translateY(3px); }
    to { opacity: 1; transform: none; }
  }
  .tabs > input[id$="-pitches"]:checked ~ .panel-pitches { display: block; }
  .tabs > input[id$="-lineup"]:checked ~ .panel-lineup { display: block; }
  .tabs > input[id$="-history"]:checked ~ .panel-history { display: block; }
  .vs-summary {
    display: grid;
    gap: 0.55rem;
    margin: 0 0 0.85rem;
    padding: 0.75rem 0.85rem;
    background: rgba(15, 106, 77, 0.06);
    border-radius: 10px;
  }
  .vs-summary .meta-label {
    display: block;
    font-size: 0.72rem;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 0.15rem;
  }
  .vs-summary .meta-value {
    font-size: 0.92rem;
    line-height: 1.35;
  }
  .vs-table {
    display: grid;
    gap: 0.25rem;
    font-size: 0.86rem;
  }
  .vs-head, .vs-row {
    display: grid;
    grid-template-columns: 6.2rem 3.6rem repeat(7, minmax(2rem, 1fr));
    gap: 0.35rem;
    align-items: center;
  }
  .vs-head {
    font-size: 0.7rem;
    text-transform: uppercase;
    letter-spacing: 0.04em;
    color: var(--muted);
    padding: 0.2rem 0;
  }
  .vs-row {
    padding: 0.35rem 0;
    border-top: 1px solid rgba(20, 30, 25, 0.08);
  }
  .site {
    display: inline-block;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.03em;
    padding: 0.12rem 0.4rem;
    border-radius: 999px;
  }
  .site-home { background: rgba(15, 106, 77, 0.14); color: var(--ok); }
  .site-away { background: rgba(154, 91, 18, 0.16); color: var(--warn); }
  @media (max-width: 640px) {
    .vs-head, .vs-row {
      grid-template-columns: 5.4rem 3.2rem repeat(4, minmax(1.6rem, 1fr));
    }
    .vs-head div:nth-child(n+6),
    .vs-row div:nth-child(n+6) { display: none; }
  }

  .batter-grid {
    display: grid; grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 0.45rem 0.75rem;
  }
  .batter {
    display: flex; justify-content: space-between; gap: 0.5rem;
    padding: 0.45rem 0.55rem; border-radius: 10px;
    background: rgba(255,255,255,0.65); border: 1px solid var(--line); font-size: 0.86rem;
  }
  .batter.missing { opacity: 0.55; }
  .batter .slot { color: var(--muted); min-width: 1.2rem; }
  .batter .k {
    font-weight: 800;
    font-variant-numeric: tabular-nums;
    font-size: 0.86rem;
    padding: 0.14rem 0.42rem;
    border-radius: 999px;
    border: 1px solid transparent;
    white-space: nowrap;
  }
  .batter .k.grade-elite,
  .kval.grade-elite,
  .kchip.grade-elite {
    background: rgba(15, 106, 77, 0.18);
    color: #064832;
    border-color: rgba(15, 106, 77, 0.32);
  }
  .batter .k.grade-high,
  .kval.grade-high,
  .kchip.grade-high {
    background: rgba(15, 106, 77, 0.11);
    color: #0f6a4d;
    border-color: rgba(15, 106, 77, 0.24);
  }
  .batter .k.grade-mid,
  .kval.grade-mid,
  .kchip.grade-mid {
    background: rgba(154, 91, 18, 0.12);
    color: #8a4b0f;
    border-color: rgba(154, 91, 18, 0.26);
  }
  .batter .k.grade-low,
  .kval.grade-low,
  .kchip.grade-low {
    background: rgba(140, 40, 40, 0.12);
    color: #8c2828;
    border-color: rgba(140, 40, 40, 0.26);
  }
  .kchip {
    display: inline-flex;
    align-items: center;
    font-weight: 800;
    font-variant-numeric: tabular-nums;
    padding: 0.08rem 0.4rem;
    border-radius: 999px;
    border: 1px solid transparent;
    white-space: nowrap;
  }
  .kchip.rate-na {
    background: rgba(20, 32, 26, 0.05);
    color: var(--muted);
    border-color: rgba(20, 32, 26, 0.12);
    font-weight: 600;
  }
  .hint-amber { color: #8a4b0f; }
  .hint-red { color: #8c2828; }
  .pitch-stack {
    display: grid;
    gap: 0.45rem;
    width: 100%;
    min-width: 0;
  }
  .pitch-block {
    border: 1px solid var(--line);
    border-radius: 12px;
    background: rgba(255,255,255,0.72);
    overflow: hidden;
  }
  .pitch-block > summary {
    list-style: none;
    cursor: pointer;
    display: flex;
    flex-wrap: wrap;
    align-items: baseline;
    gap: 0.25rem 0.65rem;
    padding: 0.65rem 0.8rem;
    line-height: 1.35;
  }
  .pitch-block > summary::-webkit-details-marker { display: none; }
  .pitch-block > summary::before {
    content: "▸";
    color: var(--muted);
    font-size: 0.75rem;
    margin-right: 0.15rem;
  }
  .pitch-block[open] > summary::before { content: "▾"; color: var(--accent); }
  .pitch-block > summary .pname {
    font-weight: 700;
    font-size: 0.92rem;
    color: var(--ink);
  }
  .pitch-block > summary .pmeta {
    color: var(--muted);
    font-size: 0.78rem;
    font-weight: 500;
  }
  .pitch-block[open] > summary {
    border-bottom: 1px solid var(--line);
    background: rgba(15, 106, 77, 0.06);
  }
  .pitch-list {
    display: grid;
    gap: 0;
    padding: 0.15rem 0.8rem 0.55rem;
  }
  .pitch-row {
    display: grid;
    grid-template-columns: minmax(0, 1fr) minmax(6.5rem, 36%) 4.4rem;
    gap: 0.55rem;
    align-items: center;
    padding: 0.5rem 0.15rem;
    border-bottom: 1px solid var(--line);
  }
  .pitch-row:last-child { border-bottom: 0; }
  .pitch-row.avg {
    margin-top: 0.2rem;
    border-top: 1px solid var(--line);
    border-bottom: 0;
    font-weight: 700;
  }
  .pitch-row .who {
    display: flex;
    flex-wrap: wrap;
    align-items: baseline;
    gap: 0.3rem 0.45rem;
    min-width: 0;
  }
  .pitch-row .slot { color: var(--muted); font-weight: 500; font-size: 0.8rem; }
  .pitch-row .name { font-size: 0.9rem; font-weight: 650; }
  .meter {
    height: 0.55rem;
    border-radius: 999px;
    background: rgba(20, 32, 26, 0.08);
    overflow: hidden;
  }
  .bar {
    display: block;
    height: 100%;
    border-radius: inherit;
    min-width: 0;
    transition: width 0.25s ease;
  }
  .kval {
    text-align: right;
    font-variant-numeric: tabular-nums;
    font-weight: 800;
    font-size: 0.82rem;
    padding: 0.12rem 0.4rem;
    border-radius: 999px;
    border: 1px solid transparent;
    white-space: nowrap;
    justify-self: end;
  }
  @media (max-width: 560px) {
    .tab {
      padding: 0.48rem 0.5rem;
      font-size: 0.78rem;
    }
    .tab-full { display: none; }
    .tab-short { display: inline; }
    .pitch-row {
      grid-template-columns: minmax(0, 1fr) 3rem;
      grid-template-rows: auto auto;
    }
    .meter { grid-column: 1 / -1; grid-row: 2; }
    .kval { grid-column: 2; grid-row: 1; }
    .pitch-block > summary {
      padding: 0.55rem 0.65rem;
      gap: 0.15rem 0.45rem;
    }
    .pitch-block > summary .pname { font-size: 0.84rem; }
    .pitch-block > summary .pmeta { font-size: 0.7rem; }
    .pitch-list { padding: 0.1rem 0.65rem 0.45rem; }
  }
  .hint { margin: 0.65rem 0 0; color: var(--muted); font-size: 0.78rem; }
  .hits-meta {
    display: inline-block; margin-left: 0.45rem; color: var(--muted);
    font-size: 0.72rem; font-weight: 500;
  }
  .view-tabs {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 0;
    margin: 0 0 1.15rem;
    padding: 0.25rem;
    border: 1px solid var(--line);
    border-radius: 14px;
    background: rgba(255,255,255,0.55);
  }
  .view-tabs > input {
    position: absolute;
    width: 1px; height: 1px;
    margin: -1px; padding: 0; border: 0;
    clip: rect(0 0 0 0);
    overflow: hidden;
    white-space: nowrap;
  }
  .view-tab {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.4rem;
    border: 0;
    background: transparent;
    color: var(--muted);
    border-radius: 10px;
    padding: 0.65rem 0.85rem;
    font-size: 0.92rem;
    font-weight: 800;
    letter-spacing: 0.02em;
    cursor: pointer;
    transition: background 0.15s ease, color 0.15s ease;
  }
  .view-tab:hover { color: var(--ink); }
  .view-tabs > input:checked + .view-tab {
    background: var(--accent);
    color: #fff;
    box-shadow: 0 6px 16px rgba(15, 106, 77, 0.22);
  }
  .view-tab .tab-count {
    font-size: 0.72rem;
    font-weight: 700;
    opacity: 0.8;
  }
  .view-panel {
    display: none;
    grid-column: 1 / -1;
    margin-top: 0.65rem;
    padding: 0.15rem 0.1rem 0.2rem;
    animation: panelIn 0.18s ease-out;
  }
  .view-tabs > input#view-pitchers:checked ~ .panel-pitchers { display: block; }
  .view-tabs > input#view-hits:checked ~ .panel-hits { display: block; }
  .hits-board {
    margin: 0; padding: 0.85rem 0.95rem 1rem;
    border: 1px solid var(--line); border-radius: 14px;
    background: rgba(255,255,255,0.55);
  }
  .hits-board h2 {
    margin: 0 0 0.25rem; font-family: "Archivo Black", sans-serif;
    font-size: 1.15rem; letter-spacing: -0.02em;
  }
  .hits-board h2 span { color: var(--muted); font-family: Manrope, sans-serif; font-size: 0.75rem; font-weight: 600; }
  .hits-lede { margin: 0 0 0.75rem; color: var(--muted); font-size: 0.8rem; }
  .hits-colhead, .hits-row {
    display: grid;
    grid-template-columns: 2rem minmax(7rem,1.2fr) minmax(9rem,1.4fr) repeat(5, 3.2rem);
    gap: 0.4rem; align-items: center;
  }
  .hits-colhead {
    font-size: 0.68rem; text-transform: uppercase; letter-spacing: 0.04em;
    color: var(--muted); padding: 0 0 0.35rem; border-bottom: 1px solid var(--line);
  }
  .hits-row { padding: 0.35rem 0; border-bottom: 1px solid rgba(0,0,0,0.05); font-size: 0.82rem; }
  .hits-row .rk { color: var(--muted); font-variant-numeric: tabular-nums; }
  .hits-row .name { font-weight: 650; }
  .hits-row .vs { color: var(--muted); font-size: 0.75rem; }
  .hits-row .num { font-variant-numeric: tabular-nums; text-align: right; }
  @media (max-width: 720px) {
    .hits-colhead, .hits-row {
      grid-template-columns: 1.6rem minmax(5rem,1fr) repeat(3, 2.6rem);
    }
    .hits-colhead div:nth-child(3), .hits-row .vs,
    .hits-colhead div:nth-child(7), .hits-colhead div:nth-child(8),
    .hits-row .num:nth-child(7), .hits-row .num:nth-child(8) { display: none; }
  }
  .empty { padding: 1.2rem; text-align: center; color: var(--muted); }
  .footnote { margin-top: 1rem; color: var(--muted); font-size: 0.82rem; line-height: 1.45; }
  .noscript {
    margin: 0 0 1rem; padding: 0.75rem 0.9rem; border-radius: 12px;
    background: rgba(154, 91, 18, 0.12); color: #6b3f0c; font-size: 0.9rem;
  }
</style>
</head>
<body>
  <div class="wrap">
    <header class="hero">
      <h1 class="brand">K-<span>Matchup</span></h1>
      <p class="lede">
        Full-outing K projections from each starter’s arsenal against the opposing
        order. <strong>Arsenal K%</strong> is this pitcher’s mix vs <em>this</em> nine.
        The word chip (<strong>ELITE / STRONG / AVG / SOFT</strong>) is the solo grade
        from absolute K% bands — it does not depend on other pitchers today.
        The numeric <strong>#</strong> is only today’s slate rank (relative).
      </p>
      <div class="meta">__META_CHIPS__</div>
      __FRESHNESS__
      <div class="grade-legend" aria-label="Number color scale">
        Scale
        <span class="swatch grade-low">low / batter-friendly</span>
        <span class="swatch grade-mid">mid</span>
        <span class="swatch grade-high">high / pitcher-friendly</span>
        <span class="swatch grade-elite">elite</span>
        <span>Exp K · IP · Arsenal %s</span>
      </div>
      __MODEL_KEYS__
    </header>

    <noscript>
      <p class="noscript">
        JavaScript is off or blocked — rankings still work.
        Expand any pitcher, open <strong>Arsenal vs lineup</strong>, then open a pitch.
        Use the <strong>Pitchers / Hits</strong> tabs above the boards.
      </p>
    </noscript>

    <section class="view-tabs" aria-label="Board view">
      <input type="radio" name="board-view" id="view-pitchers" checked />
      <label class="view-tab" for="view-pitchers">
        Pitchers <span class="tab-count">K slate</span>
      </label>
      <input type="radio" name="board-view" id="view-hits" />
      <label class="view-tab" for="view-hits">
        Hits <span class="tab-count">props</span>
      </label>

      <div class="view-panel panel-pitchers">
        <section class="controls" id="controls" autocomplete="off">
          <label>Search
            <input id="q" type="search" placeholder="Pitcher, team, game…" autocomplete="off" />
          </label>
          <label>Lineup
            <select id="lineupFilter" autocomplete="off">
              <option value="all" selected>All sources</option>
              <option value="official">Official only</option>
              <option value="prior">Prior only</option>
            </select>
          </label>
          <label>Status
            <select id="statusFilter" autocomplete="off">
              <option value="scored" selected>Scored</option>
              <option value="all">All rows</option>
              <option value="missing">Missing / unresolved</option>
            </select>
          </label>
          <label>Sort
            <select id="sort" autocomplete="off">
              <option value="expected_ks:desc" selected>Expected Ks ↓</option>
              <option value="expected_ks:asc">Expected Ks ↑</option>
              <option value="projected_ip:desc">Proj IP ↓</option>
              <option value="tto:desc">TTO ↓</option>
              <option value="kpct:desc">Arsenal K% ↓</option>
              <option value="rank:asc">Rank</option>
              <option value="pitcher:asc">Pitcher A–Z</option>
            </select>
          </label>
        </section>

        <div class="colhead">
          <div>#</div><div>Pitcher</div><div>Game</div><div>Exp K</div>
          <div>IP</div><div>TTO</div><div>K%</div><div>Flags</div>
        </div>

        <div class="board" id="board">
__MATCHUP_CARDS__
        </div>
        <div class="empty" id="empty" hidden>
          No matchups match these filters.
          <span id="emptyHint"></span>
        </div>

        <p class="footnote">
          Expand a pitcher → <strong>Arsenal vs lineup</strong> for pitch-by-pitch K%,
          or <strong>Batting order</strong> for the nine. Arsenal <strong>#</strong> ranks
          this pitcher vs <em>this</em> lineup (absolute bands). The numeric <strong>#</strong> is
          only today’s slate rank. FILLER / MATCHUP OK flag soft-contact arms.
          Pre-lineup days are all <strong>Prior</strong> — use Lineup <strong>All sources</strong>.
          Switch to the <strong>Hits</strong> tab for Hits / H+R+RBI props.
        </p>
      </div>

      <div class="view-panel panel-hits">
        __HITS_BOARD__
      </div>
    </section>
  </div>

  <script id="data" type="application/json">__DATA_JSON__</script>
  <script>
    (function () {
      const board = document.getElementById("board");
      const empty = document.getElementById("empty");
      const q = document.getElementById("q");
      const lineupFilter = document.getElementById("lineupFilter");
      const statusFilter = document.getElementById("statusFilter");
      const sort = document.getElementById("sort");
      if (!board) return;

      function apply() {
        const query = (q.value || "").trim().toLowerCase();
        let lineup = lineupFilter.value;
        const status = statusFilter.value;
        const [key, dir] = sort.value.split(":");
        const cards = Array.from(board.querySelectorAll("details.matchup"));
        const hasPrior = cards.some((el) => (el.dataset.lineup || "").startsWith("prior"));
        const hasOfficial = cards.some((el) => (el.dataset.lineup || "") === "official");
        // Browsers may restore "Official only" from a prior visit; on pre-lineup
        // slates that hides every card. Reset to All sources in that case.
        if (lineup === "official" && !hasOfficial && hasPrior) {
          lineupFilter.value = "all";
          lineup = "all";
        }
        let visible = 0;
        cards.forEach((el) => {
          const hay = el.dataset.search || "";
          const src = el.dataset.lineup || "";
          const st = el.dataset.status || "";
          let show = true;
          if (query && !hay.includes(query)) show = false;
          if (lineup === "official" && src !== "official") show = false;
          if (lineup === "prior" && !src.startsWith("prior")) show = false;
          if (status === "scored" && st !== "scored") show = false;
          if (status === "missing" && st !== "missing") show = false;
          el.hidden = !show;
          if (show) visible += 1;
        });
        empty.hidden = visible > 0;
        const hint = document.getElementById("emptyHint");
        if (hint) {
          hint.textContent =
            visible === 0 && lineup === "official"
              ? " Official lineups are not posted yet — switch Lineup to All sources."
              : "";
        }

        const attrKey = {
          expected_ks: "expectedKs",
          projected_ip: "projectedIp",
          tto: "tto",
          kpct: "kpct",
          rank: "rank",
          pitcher: "pitcher",
        }[key] || "expectedKs";

        const sorted = cards.slice().sort((a, b) => {
          let av = a.dataset[attrKey];
          let bv = b.dataset[attrKey];
          if (key === "pitcher") {
            av = (av || "").toLowerCase();
            bv = (bv || "").toLowerCase();
            return dir === "asc" ? av.localeCompare(bv) : bv.localeCompare(av);
          }
          const an = av === undefined || av === "" || av === "None" ? null : Number(av);
          const bn = bv === undefined || bv === "" || bv === "None" ? null : Number(bv);
          if (an == null && bn == null) return 0;
          if (an == null) return 1;
          if (bn == null) return -1;
          return dir === "asc" ? an - bn : bn - an;
        });
        sorted.forEach((el) => board.appendChild(el));
      }

      q.addEventListener("input", apply);
      lineupFilter.addEventListener("change", apply);
      statusFilter.addEventListener("change", apply);
      sort.addEventListener("change", apply);
      apply();
    })();
  </script>
</body>
</html>
"""
