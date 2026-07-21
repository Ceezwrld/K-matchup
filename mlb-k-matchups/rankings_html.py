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
                    "expected_k_pct": _json_safe(b.get("expected_k_pct")),
                    "expected_whiff_pct": _json_safe(b.get("expected_whiff_pct")),
                    "status": b.get("status"),
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
                "status": r.get("status"),
                "lineup_source": r.get("lineup_source"),
                "expected_ks": _json_safe(r.get("expected_ks")),
                "expected_k_pct": _json_safe(r.get("expected_k_pct")),
                "expected_ks_1x": _json_safe(r.get("expected_ks_1x")),
                "expected_whiff_pct": _json_safe(r.get("expected_whiff_pct")),
                "projected_ip": _json_safe(r.get("projected_ip")),
                "projected_bf": _json_safe(r.get("projected_bf")),
                "times_through_order": _json_safe(r.get("times_through_order")),
                "outing_source": r.get("outing_source"),
                "lineup_batters": _json_safe(r.get("lineup_batters")),
                "lineup_scored": _json_safe(r.get("lineup_scored")),
                "lineup_coverage": _json_safe(r.get("lineup_coverage")),
                "bf_scored": _json_safe(r.get("bf_scored")),
                "batters_faced_assumed": _json_safe(r.get("batters_faced_assumed")),
                "missing_batters": r.get("missing_batters") or "",
                "arsenal": clean_arsenal,
                "pitch_lineup_avg": clean_pitch_avg,
                "batters": clean_detail,
            }
        )
    return rows


def _render_pitch_matrix(row: dict[str, Any]) -> str:
    arsenal = row.get("pitch_lineup_avg") or row.get("arsenal") or []
    if not arsenal:
        return '<p class="hint">No arsenal pitch breakdown available.</p>'

    chips = []
    for p in arsenal:
        avg_k = p.get("lineup_k_pct")
        avg_txt = f"{_fmt(avg_k, 1)}% lineup K" if avg_k is not None else "no lineup sample"
        chips.append(
            "<div class='arsenal-chip'>"
            f"<span class='name'>{_esc(p.get('pitch_name') or p.get('pitch_type'))}</span>"
            f"<span class='meta'>{_fmt(p.get('usage_pct'), 1)}% usage · {_esc(avg_txt)}</span>"
            "</div>"
        )

    head_cells = ["<th>Batter</th>"]
    for p in arsenal:
        head_cells.append(
            "<th>"
            f"{_esc(p.get('pitch_name') or p.get('pitch_type'))}"
            f"<span class='usage'>{_fmt(p.get('usage_pct'), 1)}% usage</span>"
            "</th>"
        )
    head_cells.append("<th>vs arsenal</th>")

    body_rows = []
    for b in row.get("batters") or []:
        side = _hand_label(b.get("bat_side"), "B")
        side_html = f" <span class='hand'>{_esc(side)}</span>" if side else ""
        cells = [
            "<td class='batter-cell'>"
            f"<span class='slot'>{_esc(b.get('slot'))}.</span>{_esc(b.get('batter') or '—')}"
            f"{side_html}"
            "</td>"
        ]
        pitches = {p.get("pitch_type"): p for p in (b.get("pitches") or [])}
        for p in arsenal:
            hit = pitches.get(p.get("pitch_type")) or {}
            k = hit.get("k_percent")
            src = hit.get("k_source") or ""
            marker = ""
            if src in {"league_pitch", "league_platoon"}:
                marker = "†"
            title = (
                "No Savant sample vs this pitch"
                if k is None
                else (
                    f"K% {_fmt(k, 1)} · whiff {_fmt(hit.get('whiff_percent'), 1)}% "
                    f"· PA {hit.get('pa') if hit.get('pa') is not None else '—'} "
                    f"· source {src or 'pitch'}"
                )
            )
            cells.append(
                f"<td class='heat' style='{_heat_style(k)}' title='{_esc(title)}'>"
                f"{'—' if k is None else _fmt(k, 1)}{marker}"
                "</td>"
            )
        vs = (
            f"{_fmt(b.get('expected_k_pct'), 1)}%"
            if b.get("status") == "ok"
            else "n/a"
        )
        cells.append(f"<td class='heat'>{vs}</td>")
        body_rows.append("<tr>" + "".join(cells) + "</tr>")

    avg_cells = ["<td class='batter-cell'>Lineup avg</td>"]
    for p in arsenal:
        k = p.get("lineup_k_pct")
        avg_cells.append(
            f"<td class='heat' style='{_heat_style(k)}'>"
            f"{'—' if k is None else _fmt(k, 1)}"
            "</td>"
        )
    avg_cells.append(f"<td class='heat'>{_fmt(row.get('expected_k_pct'), 1)}%</td>")
    body_rows.append("<tr class='avg-row'>" + "".join(avg_cells) + "</tr>")

    return (
        f"<div class='arsenal-strip'>{''.join(chips)}</div>"
        "<div class='matrix-wrap'><table class='matrix'>"
        f"<thead><tr>{''.join(head_cells)}</tr></thead>"
        f"<tbody>{''.join(body_rows)}</tbody>"
        "</table></div>"
        "<p class='hint'>Heat map = each batter’s strikeout rate vs that pitch type. "
        "Darker green = more K-prone. <code>†</code> = no direct sample vs that pitch, "
        "so same-handed league-average K% vs that pitch is used (more accurate than "
        "copying another pitch from the same batter). "
        "Handedness shown as LHB/RHB next to each batter.</p>"
    )


def _render_lineup_panel(row: dict[str, Any]) -> str:
    cards = []
    for b in row.get("batters") or []:
        miss = b.get("status") != "ok"
        k = "n/a" if miss else f"{_fmt(b.get('expected_k_pct'), 1)}%"
        side = _hand_label(b.get("bat_side"), "B")
        side_html = f" <span class='hand'>{_esc(side)}</span>" if side else ""
        cards.append(
            f"<div class='batter {'missing' if miss else ''}'>"
            f"<span><span class='slot'>{_esc(b.get('slot'))}.</span> "
            f"{_esc(b.get('batter') or '—')}{side_html}</span>"
            f"<span class='k'>{k}</span>"
            "</div>"
        )
    if not cards:
        return "<div class='empty'>No batter detail</div>"
    return (
        f"<div class='batter-grid'>{''.join(cards)}</div>"
        "<p class='hint'>Values are arsenal-weighted K% for each batter vs this "
        "starter’s pitch mix.</p>"
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
    search = " ".join(
        str(x)
        for x in [
            row.get("pitcher"),
            pitcher_hand,
            row.get("pitcher_team"),
            row.get("opponent"),
            row.get("game"),
            row.get("lineup_source"),
            status,
        ]
        if x
    ).lower()

    uid = f"m{idx}"
    summary = (
        "<div class='summary-grid'>"
        f"<div class='rank'>{_esc(row.get('rank') if row.get('rank') is not None else '—')}</div>"
        "<div class='who'>"
        f"<div class='pitcher'>{_esc(row.get('pitcher') or '—')}{hand_html}</div>"
        f"<div class='sub'>{_esc(row.get('pitcher_team') or '?')} vs "
        f"{_esc(row.get('opponent') or '?')}"
        f"{'' if status in ('', 'ok') else ' · ' + _esc(status)}</div>"
        "</div>"
        f"<div class='game'>{_esc(row.get('game') or '—')}</div>"
        f"<div class='num ks'>{_fmt(row.get('expected_ks'))}</div>"
        f"<div class='num'>{_fmt(row.get('projected_ip'), 1)}</div>"
        f"<div class='num'>{tto_s}</div>"
        f"<div class='num'>{_fmt(row.get('expected_k_pct'))}</div>"
        f"<div><span class='badge {kind}'>{_esc(label)}</span></div>"
        "</div>"
    )

    head = (
        "<p class='detail-head'>"
        f"Projected outing {_fmt(row.get('projected_ip'), 1)} IP · "
        f"{tto_s} through order · "
        f"BF {row.get('projected_bf') if row.get('projected_bf') is not None else row.get('batters_faced_assumed') or '—'} "
        f"({_esc(row.get('outing_source') or 'n/a')}) · "
        f"lineup cover "
        f"{'—' if row.get('lineup_coverage') is None else str(int(round(100 * float(row['lineup_coverage'])))) + '%'}"
        "</p>"
    )

    # CSS-only tabs via radio buttons (works with JS disabled).
    tabs = (
        f"<div class='tabs'>"
        f"<input type='radio' name='tab-{uid}' id='tab-{uid}-pitches' checked />"
        f"<label class='tab' for='tab-{uid}-pitches'>Pitch weaknesses</label>"
        f"<input type='radio' name='tab-{uid}' id='tab-{uid}-lineup' />"
        f"<label class='tab' for='tab-{uid}-lineup'>Lineup K%</label>"
        f"<div class='tab-panel panel-pitches'>{_render_pitch_matrix(row)}</div>"
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
) -> None:
    rows = rows_for_html(df)
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
    }

    html = HTML_TEMPLATE
    html = html.replace("__META_CHIPS__", meta_html)
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
  body {
    margin: 0;
    min-height: 100vh;
    color: var(--ink);
    font-family: var(--mono);
    background:
      radial-gradient(1200px 600px at 10% -10%, rgba(15, 106, 77, 0.18), transparent 55%),
      radial-gradient(900px 500px at 100% 0%, rgba(154, 91, 18, 0.12), transparent 50%),
      linear-gradient(165deg, var(--bg0), var(--bg1) 55%, #eef4ea);
  }
  .wrap { width: min(1120px, calc(100% - 2rem)); margin: 0 auto; padding: 2.25rem 0 4rem; }
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
    display: grid; gap: 0.65rem;
  }
  .colhead, .summary-grid {
    display: grid;
    grid-template-columns: 3rem minmax(9rem, 1.4fr) minmax(5rem, 0.8fr) repeat(4, minmax(3.4rem, 0.7fr)) minmax(5.5rem, 0.9fr);
    gap: 0.55rem;
    align-items: center;
  }
  .colhead {
    padding: 0 0.85rem;
    font-size: 0.72rem; letter-spacing: 0.05em; text-transform: uppercase; color: var(--muted);
  }
  @media (max-width: 900px) {
    .colhead { display: none; }
    .summary-grid {
      grid-template-columns: 2.2rem 1fr auto;
      grid-template-areas:
        "rank who badge"
        "rank game game"
        "ks ip tto";
    }
    .summary-grid .rank { grid-area: rank; }
    .summary-grid .who { grid-area: who; }
    .summary-grid .game { grid-area: game; }
    .summary-grid .ks { grid-area: ks; }
    .summary-grid .num:nth-of-type(2) { grid-area: ip; }
    .summary-grid .num:nth-of-type(3) { grid-area: tto; }
  }
  details.matchup {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    overflow: hidden;
  }
  details.matchup[hidden] { display: none !important; }
  summary {
    list-style: none;
    cursor: pointer;
    padding: 0.9rem 0.95rem;
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
  .num { font-variant-numeric: tabular-nums; font-weight: 700; }
  .ks { color: var(--accent); font-size: 1.05rem; }
  .badge {
    display: inline-flex; padding: 0.22rem 0.55rem; border-radius: 999px;
    font-size: 0.72rem; font-weight: 700;
  }
  .badge.official { background: rgba(15, 106, 77, 0.12); color: var(--ok); }
  .badge.prior { background: rgba(154, 91, 18, 0.14); color: var(--warn); }
  .badge.miss { background: rgba(20, 32, 26, 0.08); color: var(--muted); }
  .detail {
    padding: 0 1rem 1.1rem;
    border-top: 1px solid var(--line);
    background: rgba(20, 32, 26, 0.03);
  }
  .detail-head {
    margin: 0.85rem 0 0.75rem;
    font-size: 0.78rem; letter-spacing: 0.04em; text-transform: uppercase;
    color: var(--muted); line-height: 1.45;
  }
  .tabs {
    display: grid;
    grid-template-columns: repeat(2, max-content);
    gap: 0.4rem 0.45rem;
    align-items: center;
  }
  .tabs > input { position: absolute; opacity: 0; pointer-events: none; }
  .tab {
    display: inline-flex; align-items: center;
    border: 1px solid var(--line); background: rgba(255,255,255,0.65);
    color: var(--muted); border-radius: 999px; padding: 0.4rem 0.85rem;
    font-size: 0.82rem; font-weight: 700; cursor: pointer;
  }
  .tabs > input:checked + .tab {
    background: var(--accent); border-color: var(--accent); color: #fff;
  }
  .tab-panel {
    display: none;
    grid-column: 1 / -1;
    margin-top: 0.35rem;
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
  .batter .k { font-weight: 700; color: var(--accent); }
  .arsenal-strip { display: flex; flex-wrap: wrap; gap: 0.45rem; margin-bottom: 0.75rem; }
  .arsenal-chip {
    display: inline-flex; flex-direction: column; gap: 0.1rem; min-width: 5.5rem;
    padding: 0.45rem 0.6rem; border-radius: 12px; border: 1px solid var(--line);
    background: rgba(255,255,255,0.7);
  }
  .arsenal-chip .name { font-weight: 700; font-size: 0.82rem; }
  .arsenal-chip .meta { color: var(--muted); font-size: 0.72rem; }
  .matrix-wrap {
    overflow-x: auto; border: 1px solid var(--line); border-radius: 14px;
    background: rgba(255,255,255,0.55);
  }
  table.matrix { width: 100%; border-collapse: collapse; min-width: 520px; }
  table.matrix th, table.matrix td {
    padding: 0.55rem 0.6rem; border-bottom: 1px solid var(--line);
    border-right: 1px solid var(--line); font-size: 0.82rem; text-align: center;
    white-space: nowrap;
  }
  table.matrix th:last-child, table.matrix td:last-child { border-right: none; }
  table.matrix thead th {
    background: rgba(248, 244, 236, 0.96); text-align: center; color: var(--ink);
    font-size: 0.78rem;
  }
  table.matrix thead th .usage {
    display: block; color: var(--muted); font-weight: 500; font-size: 0.7rem; margin-top: 0.15rem;
  }
  table.matrix td.batter-cell { text-align: left; font-weight: 600; min-width: 9rem; }
  table.matrix td.batter-cell .slot { color: var(--muted); font-weight: 500; margin-right: 0.25rem; }
  table.matrix td.heat { font-weight: 700; font-variant-numeric: tabular-nums; }
  table.matrix tr.avg-row td { background: rgba(15, 106, 77, 0.06); font-weight: 700; }
  .hint { margin: 0.65rem 0 0; color: var(--muted); font-size: 0.78rem; }
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
        Full-outing strikeout projections from each starter’s pitch mix against the
        opposing batting order. Open a pitcher to see pitch-by-pitch K weaknesses.
      </p>
      <div class="meta">__META_CHIPS__</div>
    </header>

    <noscript>
      <p class="noscript">
        JavaScript is off or blocked — rankings and heatmaps still work.
        Expand any pitcher below, then use the <strong>Pitch weaknesses</strong> tab.
      </p>
    </noscript>

    <section class="controls" id="controls">
      <label>Search
        <input id="q" type="search" placeholder="Pitcher, team, game…" />
      </label>
      <label>Lineup
        <select id="lineupFilter">
          <option value="all">All sources</option>
          <option value="official">Official only</option>
          <option value="prior">Prior only</option>
        </select>
      </label>
      <label>Status
        <select id="statusFilter">
          <option value="scored">Scored</option>
          <option value="all">All rows</option>
          <option value="missing">Missing / unresolved</option>
        </select>
      </label>
      <label>Sort
        <select id="sort">
          <option value="expected_ks:desc">Expected Ks ↓</option>
          <option value="expected_ks:asc">Expected Ks ↑</option>
          <option value="projected_ip:desc">Proj IP ↓</option>
          <option value="tto:desc">TTO ↓</option>
          <option value="kpct:desc">Lineup K% ↓</option>
          <option value="rank:asc">Rank</option>
          <option value="pitcher:asc">Pitcher A–Z</option>
        </select>
      </label>
    </section>

    <div class="colhead">
      <div>#</div><div>Pitcher</div><div>Game</div><div>Exp. Ks</div>
      <div>Proj IP</div><div>TTO</div><div>Lineup K%</div><div>Lineup</div>
    </div>

    <div class="board" id="board">
__MATCHUP_CARDS__
    </div>
    <div class="empty" id="empty" hidden>No matchups match these filters.</div>

    <p class="footnote">
      Expand a pitcher, then open <strong>Pitch weaknesses</strong> to see each batter’s
      K% vs every pitch in that starter’s arsenal (darker green = more K-prone).
      If this page opened as plain text from GitHub raw, download the file and open it
      locally, or use the HTML preview link in the README/PR.
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
        const lineup = lineupFilter.value;
        const status = statusFilter.value;
        const [key, dir] = sort.value.split(":");
        const cards = Array.from(board.querySelectorAll("details.matchup"));
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
