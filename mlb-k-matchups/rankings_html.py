"""Self-contained interactive HTML export for K-matchup rankings.

Heatmaps and matchup detail are server-rendered into the HTML so they work
even when the file is opened from a host that blocks JavaScript (e.g. GitHub
raw). Light JS only enhances search / sort / filter.
"""

from __future__ import annotations

import html as html_lib
import json
from datetime import datetime, timezone
from typing import Any

import pandas as pd


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


def _fmt(value: Any, digits: int = 2) -> str:
    v = _json_safe(value)
    if v is None:
        return "—"
    try:
        return f"{float(v):.{digits}f}"
    except (TypeError, ValueError):
        return "—"


def _heat_style(k: Any) -> str:
    v = _json_safe(k)
    if v is None:
        return "background:transparent;color:var(--muted)"
    t = max(0.0, min(1.0, (float(v) - 8.0) / 32.0))
    alpha = 0.12 + t * 0.55
    color = "#063828" if t > 0.55 else "var(--ink)"
    return f"background:rgba(15,106,77,{alpha:.3f});color:{color}"


def _grade_band(value: Any, low: float, mid: float, high: float) -> str | None:
    """Map a numeric value onto low / mid / high / elite."""
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


def _grade_for(metric: str, value: Any) -> str | None:
    """Color-grade key projection metrics for the HTML board."""
    if metric == "expected_ks":
        return _grade_band(value, 4.0, 5.0, 6.0)
    if metric == "expected_k_pct":
        return _grade_band(value, 18.0, 21.0, 24.0)
    if metric == "projected_ip":
        return _grade_band(value, 5.0, 5.75, 6.5)
    if metric == "tto":
        return _grade_band(value, 2.2, 2.6, 3.0)
    if metric == "batter_k_pct":
        return _grade_band(value, 15.0, 20.0, 25.0)
    return None


def _grade_class(metric: str, value: Any) -> str:
    band = _grade_for(metric, value)
    return f" grade-{band}" if band else ""


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
                "expected_ks_p25": _json_safe(r.get("expected_ks_p25")),
                "expected_ks_p75": _json_safe(r.get("expected_ks_p75")),
                "expected_ks_sigma": _json_safe(r.get("expected_ks_sigma")),
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
                "outing_risk": r.get("outing_risk"),
                "risk_flags": r.get("risk_flags") or "",
                "bf_risk_factor": _json_safe(r.get("bf_risk_factor")),
                "survival_flags": r.get("survival_flags") or "",
                "hook_risk": r.get("hook_risk") or "",
                "hook_flags": r.get("hook_flags") or "",
                "hook_score": _json_safe(r.get("hook_score")),
                "last3_ks": _json_safe(r.get("last3_ks")),
                "last3_k9": _json_safe(r.get("last3_k9")),
                "form_ks": _json_safe(r.get("form_ks")),
                "form_weight": _json_safe(r.get("form_weight")),
                "lineup_k_pct": _json_safe(r.get("lineup_k_pct")),
                "lineup_avg": _json_safe(r.get("lineup_avg")),
                "lineup_bb_pct": _json_safe(r.get("lineup_bb_pct")),
                "lineup_chase_pct": _json_safe(r.get("lineup_chase_pct")),
                "lineup_whiff_pct": _json_safe(r.get("lineup_whiff_pct")),
                "offense_source": r.get("offense_source"),
                "offense_factor": _json_safe(r.get("offense_factor")),
                "whiff_chase_factor": _json_safe(r.get("whiff_chase_factor")),
                "discipline_grade": r.get("discipline_grade") or "",
                "discipline_ks_factor": _json_safe(r.get("discipline_ks_factor")),
                "discipline_bf_factor": _json_safe(r.get("discipline_bf_factor")),
                "pitch_count_risk": r.get("pitch_count_risk") or "",
                "soft_contact_profile": bool(r.get("soft_contact_profile")),
                "profile_flags": r.get("profile_flags") or "",
                "spike_arm": bool(r.get("spike_arm")),
                "spike_flags": r.get("spike_flags") or "",
                "under_ban": bool(r.get("under_ban")),
                "arsenal_matchup_rank": _json_safe(r.get("arsenal_matchup_rank")),
                "arsenal_matchup_pctile": _json_safe(r.get("arsenal_matchup_pctile")),
                "matchup_grade": r.get("matchup_grade") or "",
                "ticket_outlook": r.get("ticket_outlook") or "",
                "ticket_note": r.get("ticket_note") or "",
                "arsenal": clean_arsenal,
                "pitch_lineup_avg": clean_pitch_avg,
                "batters": clean_detail,
            }
        )
    return rows


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
        avg_txt = (
            f"{_fmt(avg_k, 1)}% lineup avg" if avg_k is not None else "no lineup avg"
        )
        vs_l = p.get("usage_vs_lhb")
        vs_r = p.get("usage_vs_rhb")
        hand_txt = ""
        if vs_l is not None or vs_r is not None:
            hand_txt = (
                f" · vs L {_fmt(vs_l, 0) if vs_l is not None else '—'}%"
                f" / vs R {_fmt(vs_r, 0) if vs_r is not None else '—'}%"
            )
        open_attr = " open" if i == 0 else ""

        rows_html: list[str] = []
        for b in batters:
            side = _hand_label(b.get("bat_side"), "B")
            side_html = f" <span class='hand'>{_esc(side)}</span>" if side else ""
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
            rows_html.append(
                "<div class='pitch-row'>"
                "<div class='who'>"
                f"<span class='slot'>{_esc(b.get('slot'))}.</span>"
                f"<span class='name'>{_esc(b.get('batter') or '—')}{side_html}</span>"
                "</div>"
                "<div class='meter'>"
                f"<span class='bar' style='width:{width:.0f}%;{_heat_style(k)}'></span>"
                "</div>"
                f"<div class='kval{k_grade}' "
                f"title='source {_esc(src or 'pitch')} · PA {_esc(pa_txt)}'>"
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
            f"<div class='kval{avg_grade}'>"
            f"{'—' if avg_k is None else _fmt(avg_k, 1) + '%'}</div>"
            "</div>"
        )
        blocks.append(
            f"<details class='pitch-block'{open_attr}>"
            "<summary>"
            f"<span class='pname'>{_esc(pname)}</span>"
            f"<span class='pmeta'>{_fmt(p.get('usage_pct'), 1)}% overall"
            f"{_esc(hand_txt)} · {_esc(avg_txt)}</span>"
            "</summary>"
            f"<div class='pitch-list'>{''.join(rows_html)}</div>"
            "</details>"
        )

    return (
        "<div class='pitch-stack'>"
        f"{''.join(blocks)}"
        "<p class='hint'>"
        "Open a pitch to see each batter’s K% vs that pitch. "
        "Rates prefer true K% vs this pitcher’s hand when sample ≥15 PA; "
        "else overall pitch K%; "
        "<code>†</code> = same-handed league average. "
        "Longer/darker bar = more K-prone."
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
        side = _hand_label(b.get("bat_side"), "B")
        side_html = f" <span class='hand'>{_esc(side)}</span>" if side else ""
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
        cards.append(
            f"<div class='batter {'missing' if miss else ''}'>"
            f"<span><span class='slot'>{_esc(b.get('slot'))}.</span> "
            f"{_esc(b.get('batter') or '—')}{side_html}{hits_html}</span>"
            f"<span class='k{k_grade}'>{k}</span>"
            "</div>"
        )
    if not cards:
        return "<div class='empty'>No batter detail</div>"
    return (
        f"<div class='batter-grid'>{''.join(cards)}</div>"
        "<p class='hint'>Right-side values are arsenal-weighted <strong>K%</strong> vs this "
        "starter. Hits / barrel / hard-hit scores are a separate Hits-prop layer and "
        "<strong>do not</strong> change expected strikeouts.</p>"
    )


def _render_hits_board(hits_board: list[dict[str, Any]] | None) -> str:
    if not hits_board:
        return ""
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
    hand_html = (
        f" <span class='hand'>{_esc(pitcher_hand)}</span>" if pitcher_hand else ""
    )
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
            "spike" if row.get("spike_arm") or outlook == "SPIKE" else "",
            "under_ban" if row.get("under_ban") else "",
            row.get("hook_risk"),
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
    elif row.get("under_ban"):
        badge_html += (
            "<span class='outlook outlook-spike' title='Soft unders blocked'>"
            "NO SOFT UNDER</span>"
        )
    hook = (row.get("hook_risk") or "").strip()
    if hook in ("medium", "high"):
        badge_html += (
            f"<span class='outlook outlook-hook-{_esc(hook)}'>"
            f"HOOK {_esc(hook.upper())}</span>"
        )
    # Arsenal matchup rank = pitcher-vs-lineup K% slate rank (starting-pitcher matchup #).
    # Opp lineup K% rank = how K-prone the opposing batting team is on today's slate.
    ark = row.get("arsenal_matchup_rank")
    opp_rank = row.get("opp_lineup_k_rank")
    chips: list[str] = []
    if opp_rank is not None and scored:
        chips.append(
            f"<span class='ark ark-opp' "
            f"title='Opposing batting-team K% rank on slate "
            f"(#1 = highest opp lineup K%)'>#{_esc(opp_rank)}</span>"
        )
    if ark is not None and scored:
        grade = (row.get("matchup_grade") or "").strip()
        chips.append(
            f"<span class='ark ark-{_esc(grade or 'avg')}' "
            f"title='Starting-pitcher arsenal matchup rank "
            f"(slate rank of pitcher K% vs this lineup)'>#{_esc(ark)}</span>"
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

    p25 = row.get("expected_ks_p25")
    p75 = row.get("expected_ks_p75")
    band_title = "Expected strikeouts"
    if p25 is not None and p75 is not None:
        band_title = (
            f"Expected strikeouts · P25–P75 band {_fmt(p25, 1)}–{_fmt(p75, 1)}"
        )
    ks_value = _fmt(row.get("expected_ks"))
    if p25 is not None and p75 is not None and scored:
        ks_value = (
            f"{_fmt(row.get('expected_ks'))}"
            f"<span class='band'>{_fmt(p25, 1)}–{_fmt(p75, 1)}</span>"
        )

    summary = (
        "<div class='summary-grid'>"
        f"<div class='rank'>{_esc(row.get('rank') if row.get('rank') is not None else '—')}</div>"
        "<div class='who'>"
        f"<div class='pitcher'>{_esc(row.get('pitcher') or '—')}{hand_html}</div>"
        f"<div class='sub'>{_esc(row.get('pitcher_team') or '?')} vs "
        f"{_esc(row.get('opponent') or '?')}"
        f"{'' if status in ('', 'ok') else ' · ' + _esc(status)}</div>"
        "</div>"
        f"{game_html}"
        "<div class='stat-row'>"
        f"{_stat(f'ks{ks_grade}', ks_value, 'Exp K', band_title)}"
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
    rates_val = (
        f"BB/9 {_fmt(row.get('bb9'), 2)} · HR/9 {_fmt(row.get('hr9'), 2)} · "
        f"xFIP {_fmt(row.get('xfip'), 2)} · K9 {_fmt(row.get('k9'), 1)}"
    )
    form_bits = []
    if row.get("last3_ks") is not None:
        form_bits.append(f"L3 {_fmt(row.get('last3_ks'), 1)} K")
    if row.get("last3_k9") is not None:
        form_bits.append(f"{_fmt(row.get('last3_k9'), 1)} K/9")
    form_val = " · ".join(form_bits) if form_bits else "no L3 form"

    opp = row.get("opponent") or "opp"
    matchup_bits = []
    if ark is not None:
        matchup_bits.append(f"#{_esc(ark)} vs {_esc(opp)} on slate")
    if row.get("matchup_grade"):
        matchup_bits.append(_esc(row.get("matchup_grade")))
    if row.get("expected_k_pct") is not None:
        matchup_bits.append(f"arsenal K% {_fmt(row.get('expected_k_pct'), 1)}")
    if row.get("lineup_k_pct") is not None:
        src = row.get("offense_source") or ""
        matchup_bits.append(
            f"opp K% {_fmt(row.get('lineup_k_pct'), 1)}"
            f"{'' if not src else ' (' + _esc(src) + ')'}"
        )
    if row.get("lineup_bb_pct") is not None:
        matchup_bits.append(f"opp BB% {_fmt(row.get('lineup_bb_pct'), 1)}")
    if row.get("lineup_chase_pct") is not None:
        matchup_bits.append(f"chase {_fmt(row.get('lineup_chase_pct'), 1)}%")
    if row.get("expected_whiff_pct") is not None:
        matchup_bits.append(f"whiff {_fmt(row.get('expected_whiff_pct'), 1)}%")
    grade = (row.get("discipline_grade") or "").strip()
    if grade:
        matchup_bits.append(_esc(grade.replace("_", " ")))
    pc = (row.get("pitch_count_risk") or "").strip()
    if pc and pc not in ("neutral", "low"):
        matchup_bits.append(f"pitch-count {_esc(pc)}")
    matchup_val = " · ".join(matchup_bits) if matchup_bits else "—"

    risk_chip = (
        f"<span class='risk risk-{_esc(risk)}'>risk {_esc(risk)}"
        f"{'' if not risk_flags else ' · ' + _esc(risk_flags)}</span>"
    )
    hook_flags = row.get("hook_flags") or ""
    if hook in ("low", "medium", "high"):
        risk_chip += (
            f" <span class='risk risk-hook-{_esc(hook)}'>hook {_esc(hook)}"
            f"{'' if not hook_flags else ' · ' + _esc(hook_flags)}</span>"
        )

    head = (
        "<div class='meta-strip'>"
        "<div class='meta-cell'>"
        "<span class='meta-label'>Outing</span>"
        f"<span class='meta-value'>{outing_val}{role_html}</span>"
        "</div>"
        "<div class='meta-cell'>"
        "<span class='meta-label'>Rates / form</span>"
        f"<span class='meta-value'>{_esc(rates_val)} · {_esc(form_val)} {risk_chip}</span>"
        "</div>"
        "<div class='meta-cell meta-matchup'>"
        "<span class='meta-label'>Arsenal matchup</span>"
        f"<span class='meta-value'>{matchup_val}</span>"
        "</div>"
        "</div>"
    )
    ticket_note = (row.get("ticket_note") or "").strip()
    # Banner for FILLER / MATCHUP_OK / SPIKE (soft-under ban).
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
        f"<div class='tab-panel panel-pitches'>{_render_pitch_matrix(row, uid)}</div>"
        f"<div class='tab-panel panel-lineup'>{_render_lineup_panel(row)}</div>"
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

    # Prefer scored first, then missing — same as CLI rank order already in df.
    cards = "\n".join(_render_matchup_card(r, i) for i, r in enumerate(rows))
    hits_html = _render_hits_board(hits_board)

    meta_bits = [
        ("Date", game_date),
        ("Generated", datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")),
        ("Avg proj IP", _fmt(avg_ip, 1) if avg_ip is not None else "—"),
        ("Avg TTO", f"{_fmt(avg_tto)}×" if avg_tto is not None else "—"),
        ("Scored", str(len(scored))),
        ("Official lineups", f"{official}/{len(scored)}"),
    ]
    meta_html = "".join(
        f"<span class='chip'>{_esc(k)}: <strong>{_esc(v)}</strong></span>"
        for k, v in meta_bits
    )

    payload = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "game_date": game_date,
        "batters_faced_override": batters_faced,
        "avg_projected_ip": avg_ip,
        "avg_times_through": avg_tto,
        "row_count": len(rows),
        "hits_board_count": len(hits_board or []),
    }

    html = HTML_TEMPLATE
    html = html.replace("__META_CHIPS__", meta_html)
    html = html.replace("__HITS_BOARD__", hits_html)
    html = html.replace("__MATCHUP_CARDS__", cards)
    html = html.replace("__DATA_JSON__", json.dumps(payload, ensure_ascii=False))
    with open(path, "w", encoding="utf-8") as f:
        f.write(html)


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>K-Matchup — lineup strikeout projections</title>
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
  .grade-low { color: #6a7a72; }
  .grade-mid { color: var(--ink); }
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
  .outlook-matchup_ok { background: rgba(15, 106, 77, 0.12); color: var(--ok); }
  .outlook-spike { background: rgba(154, 91, 18, 0.18); color: #8a4b0f; }
  .outlook-hook-medium { background: rgba(154, 91, 18, 0.14); color: #8a4b0f; }
  .outlook-hook-high { background: rgba(140, 40, 40, 0.14); color: #8c2828; }
  .risk-hook-low { background: rgba(15, 106, 77, 0.10); color: var(--ok); }
  .risk-hook-medium { background: rgba(154, 91, 18, 0.14); color: #8a4b0f; }
  .risk-hook-high { background: rgba(140, 40, 40, 0.14); color: #8c2828; }
  .num .band {
    display: block;
    font-size: 0.68rem;
    font-weight: 600;
    color: var(--muted);
    letter-spacing: 0.01em;
    margin-top: 0.1rem;
  }
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
    grid-template-columns: repeat(3, minmax(0, 1fr));
    gap: 0.55rem;
    margin: 0.85rem 0 0.75rem;
  }
  @media (max-width: 820px) {
    .meta-strip { grid-template-columns: 1fr; gap: 0.4rem; }
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
  .meta-label {
    display: block;
    font-size: 0.68rem; font-weight: 700; letter-spacing: 0.06em;
    text-transform: uppercase; color: var(--muted); margin-bottom: 0.25rem;
  }
  .meta-value {
    display: flex; flex-wrap: wrap; align-items: center; gap: 0.3rem;
    font-size: 0.84rem; line-height: 1.4; color: var(--ink); font-weight: 600;
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
  .outlook-banner.outlook-matchup_ok {
    background: rgba(15, 106, 77, 0.08); border-color: rgba(15, 106, 77, 0.22);
    color: #0a4a36;
  }
  .outlook-banner.outlook-spike {
    background: rgba(154, 91, 18, 0.10); border-color: rgba(154, 91, 18, 0.28);
    color: #6e3a0c;
  }
  @media (max-width: 560px) {
    .outlook-banner { grid-template-columns: 1fr; gap: 0.25rem; }
  }
  .tabs {
    display: grid;
    grid-template-columns: 1fr 1fr;
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
  .batter .k { font-weight: 700; }
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
    grid-template-columns: minmax(0, 1fr) minmax(6.5rem, 36%) 3.6rem;
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
    font-weight: 700;
    font-size: 0.88rem;
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
  .hits-board {
    margin: 0 0 1.25rem; padding: 1rem 1.1rem 1.15rem;
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
        order. <strong>Arsenal K%</strong> is pitcher-vs-lineup whiff rate;
        the <strong>#</strong> next to it is that matchup’s slate rank (not the opponent alone).
      </p>
      <div class="meta">__META_CHIPS__</div>
      <div class="grade-legend" aria-label="Number color scale">
        Scale
        <span class="swatch grade-low">low</span>
        <span class="swatch grade-mid">mid</span>
        <span class="swatch grade-high">high</span>
        <span class="swatch grade-elite">elite</span>
        <span>Exp K · IP · Arsenal K%</span>
      </div>
    </header>

    <noscript>
      <p class="noscript">
        JavaScript is off or blocked — rankings still work.
        Expand any pitcher, open <strong>Arsenal vs lineup</strong>, then open a pitch.
      </p>
    </noscript>

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

    __HITS_BOARD__

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
      this pitcher-vs-lineup matchup on today’s slate. FILLER / MATCHUP OK flag soft-contact
      arms; <strong>SPIKE</strong> hard-blocks soft unders. Exp K shows a P25–P75 band.
      If this opened as plain text from GitHub raw, download and open locally.
      Pre-lineup days are all <strong>Prior</strong> — use Lineup <strong>All sources</strong>.
    </p>
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
