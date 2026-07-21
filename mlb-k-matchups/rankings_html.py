"""Self-contained interactive HTML export for K-matchup rankings."""

from __future__ import annotations

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
                    }
                )
            clean_detail.append(
                {
                    "slot": _json_safe(b.get("slot")),
                    "batter_id": _json_safe(b.get("batter_id")),
                    "batter": b.get("batter"),
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


def write_interactive_html(
    path: str,
    df: pd.DataFrame,
    *,
    game_date: str,
    batters_faced: float | None = None,
) -> None:
    scored = df[df["status"].eq("ok") & df["expected_ks"].notna()] if "status" in df else df
    avg_ip = float(scored["projected_ip"].mean()) if "projected_ip" in scored and len(scored) else None
    avg_tto = (
        float(scored["times_through_order"].mean())
        if "times_through_order" in scored and len(scored)
        else None
    )
    payload = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
        "game_date": game_date,
        "batters_faced_override": batters_faced,
        "avg_projected_ip": avg_ip,
        "avg_times_through": avg_tto,
        "rows": rows_for_html(df),
    }
    data_json = json.dumps(payload, ensure_ascii=False)

    html = HTML_TEMPLATE.replace("__DATA_JSON__", data_json)
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
    --accent-2: #1a8f68;
    --warn: #9a5b12;
    --ok: #0f6a4d;
    --panel: rgba(255, 252, 246, 0.82);
    --shadow: 0 18px 50px rgba(20, 32, 26, 0.08);
    --radius: 18px;
    --mono: "Manrope", system-ui, sans-serif;
    --display: "Archivo Black", "Arial Black", sans-serif;
  }

  * { box-sizing: border-box; }
  html { scroll-behavior: smooth; }
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

  .wrap {
    width: min(1120px, calc(100% - 2rem));
    margin: 0 auto;
    padding: 2.25rem 0 4rem;
  }

  .hero {
    display: grid;
    gap: 0.85rem;
    margin-bottom: 1.75rem;
    animation: rise 0.7s ease both;
  }
  .brand {
    font-family: var(--display);
    font-size: clamp(2.6rem, 7vw, 4.4rem);
    letter-spacing: -0.03em;
    line-height: 0.92;
    margin: 0;
  }
  .brand span { color: var(--accent); }
  .lede {
    max-width: 38rem;
    margin: 0;
    color: var(--muted);
    font-size: 1.05rem;
    line-height: 1.45;
  }
  .meta {
    display: flex;
    flex-wrap: wrap;
    gap: 0.55rem 0.75rem;
    margin-top: 0.35rem;
  }
  .chip {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.35rem 0.7rem;
    border: 1px solid var(--line);
    background: rgba(255,255,255,0.55);
    border-radius: 999px;
    font-size: 0.82rem;
    color: var(--muted);
  }
  .chip strong { color: var(--ink); font-weight: 700; }

  .controls {
    display: grid;
    grid-template-columns: 1.4fr repeat(3, auto);
    gap: 0.75rem;
    align-items: end;
    margin-bottom: 1rem;
    animation: rise 0.8s ease both;
    animation-delay: 0.08s;
  }
  @media (max-width: 820px) {
    .controls { grid-template-columns: 1fr 1fr; }
  }
  @media (max-width: 540px) {
    .controls { grid-template-columns: 1fr; }
  }
  label {
    display: grid;
    gap: 0.35rem;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: var(--muted);
  }
  input[type="search"], select {
    width: 100%;
    appearance: none;
    border: 1px solid var(--line);
    background: var(--panel);
    color: var(--ink);
    border-radius: 12px;
    padding: 0.7rem 0.85rem;
    font: inherit;
    font-size: 0.95rem;
    outline: none;
    transition: border-color 0.2s ease, box-shadow 0.2s ease;
  }
  input[type="search"]:focus, select:focus {
    border-color: rgba(15, 106, 77, 0.45);
    box-shadow: 0 0 0 3px rgba(15, 106, 77, 0.12);
  }

  .board {
    background: var(--panel);
    border: 1px solid var(--line);
    border-radius: var(--radius);
    box-shadow: var(--shadow);
    overflow: hidden;
    backdrop-filter: blur(10px);
    animation: rise 0.85s ease both;
    animation-delay: 0.14s;
  }

  table {
    width: 100%;
    border-collapse: collapse;
  }
  thead th {
    position: sticky;
    top: 0;
    z-index: 2;
    background: rgba(248, 244, 236, 0.96);
    text-align: left;
    font-size: 0.72rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: var(--muted);
    padding: 0.85rem 0.9rem;
    border-bottom: 1px solid var(--line);
    cursor: pointer;
    user-select: none;
    white-space: nowrap;
  }
  thead th:hover { color: var(--ink); }
  thead th .arrow { opacity: 0.35; margin-left: 0.25rem; }
  thead th.active .arrow { opacity: 1; color: var(--accent); }

  tbody tr.matchup {
    cursor: pointer;
    transition: background 0.18s ease;
  }
  tbody tr.matchup:hover { background: rgba(15, 106, 77, 0.06); }
  tbody tr.matchup.open { background: rgba(15, 106, 77, 0.09); }
  td {
    padding: 0.85rem 0.9rem;
    border-bottom: 1px solid var(--line);
    vertical-align: middle;
    font-size: 0.95rem;
  }
  .rank {
    font-family: var(--display);
    font-size: 1.05rem;
    color: var(--accent);
    width: 3rem;
  }
  .pitcher { font-weight: 700; }
  .sub {
    display: block;
    margin-top: 0.15rem;
    color: var(--muted);
    font-size: 0.8rem;
    font-weight: 500;
  }
  .num { font-variant-numeric: tabular-nums; font-weight: 700; }
  .ks { color: var(--accent); font-size: 1.05rem; }
  .badge {
    display: inline-flex;
    align-items: center;
    padding: 0.22rem 0.55rem;
    border-radius: 999px;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.02em;
  }
  .badge.official {
    background: rgba(15, 106, 77, 0.12);
    color: var(--ok);
  }
  .badge.prior {
    background: rgba(154, 91, 18, 0.14);
    color: var(--warn);
  }
  .badge.miss {
    background: rgba(20, 32, 26, 0.08);
    color: var(--muted);
  }

  tr.detail-row td {
    padding: 0;
    background: rgba(20, 32, 26, 0.03);
  }
  .detail {
    display: none;
    padding: 0.85rem 1rem 1.1rem 1.1rem;
    animation: expand 0.28s ease both;
  }
  tr.open + tr.detail-row .detail { display: block; }
  .detail-head {
    margin: 0 0 0.75rem;
    font-size: 0.78rem;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: var(--muted);
    line-height: 1.45;
  }
  .tabs {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    margin-bottom: 0.85rem;
  }
  .tab {
    border: 1px solid var(--line);
    background: rgba(255,255,255,0.65);
    color: var(--muted);
    border-radius: 999px;
    padding: 0.4rem 0.85rem;
    font: inherit;
    font-size: 0.82rem;
    font-weight: 700;
    cursor: pointer;
    transition: background 0.15s ease, color 0.15s ease, border-color 0.15s ease;
  }
  .tab:hover { color: var(--ink); border-color: rgba(15, 106, 77, 0.35); }
  .tab.active {
    background: var(--accent);
    border-color: var(--accent);
    color: #fff;
  }
  .tab-panel { display: none; }
  .tab-panel.active { display: block; animation: expand 0.25s ease both; }

  .batter-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
    gap: 0.45rem 0.75rem;
  }
  .batter {
    display: flex;
    justify-content: space-between;
    gap: 0.5rem;
    padding: 0.45rem 0.55rem;
    border-radius: 10px;
    background: rgba(255,255,255,0.65);
    border: 1px solid var(--line);
    font-size: 0.86rem;
  }
  .batter.missing { opacity: 0.55; }
  .batter .slot {
    color: var(--muted);
    font-variant-numeric: tabular-nums;
    min-width: 1.2rem;
  }
  .batter .k { font-weight: 700; color: var(--accent); }

  .arsenal-strip {
    display: flex;
    flex-wrap: wrap;
    gap: 0.45rem;
    margin-bottom: 0.75rem;
  }
  .arsenal-chip {
    display: inline-flex;
    flex-direction: column;
    gap: 0.1rem;
    min-width: 5.5rem;
    padding: 0.45rem 0.6rem;
    border-radius: 12px;
    border: 1px solid var(--line);
    background: rgba(255,255,255,0.7);
  }
  .arsenal-chip .name { font-weight: 700; font-size: 0.82rem; }
  .arsenal-chip .meta { color: var(--muted); font-size: 0.72rem; }

  .matrix-wrap {
    overflow-x: auto;
    border: 1px solid var(--line);
    border-radius: 14px;
    background: rgba(255,255,255,0.55);
  }
  table.matrix {
    width: 100%;
    border-collapse: collapse;
    min-width: 520px;
  }
  table.matrix th, table.matrix td {
    padding: 0.55rem 0.6rem;
    border-bottom: 1px solid var(--line);
    border-right: 1px solid var(--line);
    font-size: 0.82rem;
    text-align: center;
    white-space: nowrap;
  }
  table.matrix th:last-child, table.matrix td:last-child { border-right: none; }
  table.matrix thead th {
    position: static;
    background: rgba(248, 244, 236, 0.96);
    cursor: default;
    text-transform: none;
    letter-spacing: 0;
    font-size: 0.78rem;
    color: var(--ink);
  }
  table.matrix thead th .usage {
    display: block;
    color: var(--muted);
    font-weight: 500;
    font-size: 0.7rem;
    margin-top: 0.15rem;
  }
  table.matrix td.batter-cell {
    text-align: left;
    font-weight: 600;
    min-width: 9rem;
  }
  table.matrix td.batter-cell .slot {
    color: var(--muted);
    font-weight: 500;
    margin-right: 0.25rem;
  }
  table.matrix td.heat {
    font-weight: 700;
    font-variant-numeric: tabular-nums;
  }
  table.matrix tr.avg-row td {
    background: rgba(15, 106, 77, 0.06);
    font-weight: 700;
  }
  .hint {
    margin: 0.65rem 0 0;
    color: var(--muted);
    font-size: 0.78rem;
  }

  .empty {
    padding: 2rem 1rem;
    text-align: center;
    color: var(--muted);
  }

  .footnote {
    margin-top: 1rem;
    color: var(--muted);
    font-size: 0.82rem;
    line-height: 1.45;
  }

  @keyframes rise {
    from { opacity: 0; transform: translateY(14px); }
    to { opacity: 1; transform: translateY(0); }
  }
  @keyframes expand {
    from { opacity: 0; transform: translateY(-6px); }
    to { opacity: 1; transform: translateY(0); }
  }
</style>
</head>
<body>
  <div class="wrap">
    <header class="hero">
      <h1 class="brand">K-<span>Matchup</span></h1>
      <p class="lede">
        Full-outing strikeout projections: each starter’s pitch mix against the
        opposing batting order for their projected innings / times through the order.
      </p>
      <div class="meta" id="meta"></div>
    </header>

    <section class="controls">
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
          <option value="times_through_order:desc">TTO ↓</option>
          <option value="expected_k_pct:desc">Lineup K% ↓</option>
          <option value="rank:asc">Rank</option>
          <option value="pitcher:asc">Pitcher A–Z</option>
        </select>
      </label>
    </section>

    <div class="board">
      <table>
        <thead>
          <tr>
            <th data-key="rank"># <span class="arrow">↕</span></th>
            <th data-key="pitcher">Pitcher <span class="arrow">↕</span></th>
            <th data-key="game">Game <span class="arrow">↕</span></th>
            <th data-key="expected_ks">Exp. Ks <span class="arrow">↕</span></th>
            <th data-key="projected_ip">Proj IP <span class="arrow">↕</span></th>
            <th data-key="times_through_order">TTO <span class="arrow">↕</span></th>
            <th data-key="expected_k_pct">Lineup K% <span class="arrow">↕</span></th>
            <th data-key="lineup_source">Lineup <span class="arrow">↕</span></th>
          </tr>
        </thead>
        <tbody id="tbody"></tbody>
      </table>
      <div class="empty" id="empty" hidden>No matchups match these filters.</div>
    </div>

    <p class="footnote">
      <strong>Exp. Ks</strong> walks the opposing nine for the starter’s projected
      batters faced (from season IP &amp; BF per start unless overridden).
      Expand a pitcher for <strong>Pitch weaknesses</strong> (batter K% vs each arsenal pitch)
      or overall lineup K%. Re-run
      <code>python3 mlb-k-matchups/k_matchups.py --date YYYY-MM-DD --html rankings.html</code>
      after lineups post to refresh.
    </p>
  </div>

  <script id="data" type="application/json">__DATA_JSON__</script>
  <script>
    const DATA = JSON.parse(document.getElementById("data").textContent);
    const state = {
      q: "",
      lineup: "all",
      status: "scored",
      sortKey: "expected_ks",
      sortDir: "desc",
      openId: null,
      tabById: {},
    };

    const el = {
      meta: document.getElementById("meta"),
      tbody: document.getElementById("tbody"),
      empty: document.getElementById("empty"),
      q: document.getElementById("q"),
      lineupFilter: document.getElementById("lineupFilter"),
      statusFilter: document.getElementById("statusFilter"),
      sort: document.getElementById("sort"),
    };

    function fmt(n, d = 2) {
      if (n === null || n === undefined || Number.isNaN(n)) return "—";
      return Number(n).toFixed(d);
    }
    function pct(n) {
      if (n === null || n === undefined || Number.isNaN(n)) return "—";
      return `${Math.round(n * 100)}%`;
    }
    function lineupKind(src) {
      if (!src) return "miss";
      if (src === "official") return "official";
      if (String(src).startsWith("prior")) return "prior";
      return "miss";
    }
    function lineupLabel(src) {
      if (!src) return "none";
      if (src === "official") return "official";
      if (String(src).startsWith("prior:")) return `prior ${src.slice(6)}`;
      return String(src);
    }
    function rowId(r, i) {
      return `${r.pitcher_id || r.pitcher}-${r.opponent}-${i}`;
    }

    function renderMeta() {
      const rows = DATA.rows || [];
      const scored = rows.filter(r => r.status === "ok" && r.expected_ks != null);
      const official = scored.filter(r => r.lineup_source === "official").length;
      const avgIp = DATA.avg_projected_ip != null ? Number(DATA.avg_projected_ip).toFixed(1) : "—";
      const avgTto = DATA.avg_times_through != null ? Number(DATA.avg_times_through).toFixed(2) + "×" : "—";
      el.meta.innerHTML = [
        chip("Date", DATA.game_date),
        chip("Generated", DATA.generated_at),
        chip("Avg proj IP", avgIp),
        chip("Avg TTO", avgTto),
        chip("Scored", scored.length),
        chip("Official lineups", `${official}/${scored.length}`),
      ].join("");
    }
    function chip(label, value) {
      return `<span class="chip">${label}: <strong>${value}</strong></span>`;
    }

    function filtered() {
      let rows = [...(DATA.rows || [])];
      const q = state.q.trim().toLowerCase();
      if (q) {
        rows = rows.filter(r =>
          [r.pitcher, r.pitcher_team, r.opponent, r.game, r.lineup_source, r.status]
            .join(" ")
            .toLowerCase()
            .includes(q)
        );
      }
      if (state.lineup === "official") {
        rows = rows.filter(r => r.lineup_source === "official");
      } else if (state.lineup === "prior") {
        rows = rows.filter(r => String(r.lineup_source || "").startsWith("prior"));
      }
      if (state.status === "scored") {
        rows = rows.filter(r => r.status === "ok" && r.expected_ks != null);
      } else if (state.status === "missing") {
        rows = rows.filter(r => !(r.status === "ok" && r.expected_ks != null));
      }

      const dir = state.sortDir === "asc" ? 1 : -1;
      const key = state.sortKey;
      rows.sort((a, b) => {
        const av = a[key];
        const bv = b[key];
        if (av == null && bv == null) return 0;
        if (av == null) return 1;
        if (bv == null) return -1;
        if (typeof av === "string" || typeof bv === "string") {
          return String(av).localeCompare(String(bv)) * dir;
        }
        return (av - bv) * dir;
      });
      return rows;
    }

    function heatStyle(k) {
      if (k == null || Number.isNaN(k)) {
        return { bg: "transparent", color: "var(--muted)" };
      }
      // Map ~8%–40% K into a green heat scale.
      const t = Math.max(0, Math.min(1, (Number(k) - 8) / 32));
      const alpha = 0.12 + t * 0.55;
      return {
        bg: `rgba(15, 106, 77, ${alpha.toFixed(3)})`,
        color: t > 0.55 ? "#063828" : "var(--ink)",
      };
    }

    function renderLineupPanel(r) {
      const batters = (r.batters || []).map(b => {
        const miss = b.status !== "ok";
        return `<div class="batter ${miss ? "missing" : ""}">
          <span><span class="slot">${b.slot ?? ""}.</span> ${b.batter || "—"}</span>
          <span class="k">${miss ? "n/a" : fmt(b.expected_k_pct, 1) + "%"}</span>
        </div>`;
      }).join("");
      return `<div class="batter-grid">${batters || "<div class='empty'>No batter detail</div>"}</div>
        <p class="hint">Values are arsenal-weighted K% for each batter vs this starter’s pitch mix.</p>`;
    }

    function renderPitchPanel(r) {
      const arsenal = r.arsenal || r.pitch_lineup_avg || [];
      if (!arsenal.length) {
        return `<div class="empty">No arsenal pitch breakdown available.</div>`;
      }
      const chips = arsenal.map(p => {
        const avg = (r.pitch_lineup_avg || []).find(x => x.pitch_type === p.pitch_type);
        const avgK = avg && avg.lineup_k_pct != null ? `${fmt(avg.lineup_k_pct, 1)}% lineup K` : "no lineup sample";
        return `<div class="arsenal-chip">
          <span class="name">${p.pitch_name || p.pitch_type}</span>
          <span class="meta">${fmt(p.usage_pct, 1)}% usage · ${avgK}</span>
        </div>`;
      }).join("");

      const head = `
        <tr>
          <th>Batter</th>
          ${arsenal.map(p => `<th>${p.pitch_name || p.pitch_type}<span class="usage">${fmt(p.usage_pct, 1)}% usage</span></th>`).join("")}
          <th>vs arsenal</th>
        </tr>`;

      const body = (r.batters || []).map(b => {
        const cells = arsenal.map(p => {
          const hit = (b.pitches || []).find(x => x.pitch_type === p.pitch_type);
          const k = hit ? hit.k_percent : null;
          const style = heatStyle(k);
          const title = k == null
            ? "No Savant sample vs this pitch"
            : `K% ${fmt(k, 1)} · whiff ${fmt(hit.whiff_percent, 1)}% · PA ${hit.pa ?? "—"}`;
          return `<td class="heat" style="background:${style.bg};color:${style.color}" title="${title}">${k == null ? "—" : fmt(k, 1)}</td>`;
        }).join("");
        const vs = b.status === "ok" ? fmt(b.expected_k_pct, 1) + "%" : "n/a";
        return `<tr>
          <td class="batter-cell"><span class="slot">${b.slot ?? ""}.</span>${b.batter || "—"}</td>
          ${cells}
          <td class="heat">${vs}</td>
        </tr>`;
      }).join("");

      const avgRow = `<tr class="avg-row">
        <td class="batter-cell">Lineup avg</td>
        ${arsenal.map(p => {
          const avg = (r.pitch_lineup_avg || []).find(x => x.pitch_type === p.pitch_type);
          const k = avg ? avg.lineup_k_pct : null;
          const style = heatStyle(k);
          return `<td class="heat" style="background:${style.bg};color:${style.color}">${k == null ? "—" : fmt(k, 1)}</td>`;
        }).join("")}
        <td class="heat">${fmt(r.expected_k_pct, 1)}%</td>
      </tr>`;

      return `
        <div class="arsenal-strip">${chips}</div>
        <div class="matrix-wrap">
          <table class="matrix">
            <thead>${head}</thead>
            <tbody>${body}${avgRow}</tbody>
          </table>
        </div>
        <p class="hint">
          Heat map = each batter’s strikeout rate vs that pitch type. Darker green = more K-prone.
          Columns are only pitches this starter throws (≥ min usage).
        </p>`;
    }

    function render() {
      const rows = filtered();
      el.empty.hidden = rows.length > 0;
      el.tbody.innerHTML = rows.map((r, i) => {
        const id = rowId(r, i);
        const open = state.openId === id ? "open" : "";
        const kind = lineupKind(r.lineup_source);
        const tab = state.tabById[id] || "pitches";
        return `
          <tr class="matchup ${open}" data-id="${id}">
            <td class="rank">${r.rank ?? "—"}</td>
            <td>
              <span class="pitcher">${r.pitcher || "—"}</span>
              <span class="sub">${r.pitcher_team || "?"} vs ${r.opponent || "?"}${r.status && r.status !== "ok" ? " · " + r.status : ""}</span>
            </td>
            <td>${r.game || "—"}</td>
            <td class="num ks">${fmt(r.expected_ks)}</td>
            <td class="num">${fmt(r.projected_ip, 1)}</td>
            <td class="num">${r.times_through_order == null ? "—" : fmt(r.times_through_order) + "×"}</td>
            <td class="num">${fmt(r.expected_k_pct)}</td>
            <td><span class="badge ${kind}">${lineupLabel(r.lineup_source)}</span></td>
          </tr>
          <tr class="detail-row">
            <td colspan="8">
              <div class="detail">
                <p class="detail-head">
                  Projected outing ${fmt(r.projected_ip, 1)} IP ·
                  ${r.times_through_order == null ? "—" : fmt(r.times_through_order) + "×"} through order ·
                  BF ${r.projected_bf ?? r.batters_faced_assumed ?? "—"}
                  (${r.outing_source || "n/a"}) ·
                  lineup cover ${pct(r.lineup_coverage)}
                </p>
                <div class="tabs" data-id="${id}">
                  <button type="button" class="tab ${tab === "pitches" ? "active" : ""}" data-tab="pitches">Pitch weaknesses</button>
                  <button type="button" class="tab ${tab === "lineup" ? "active" : ""}" data-tab="lineup">Lineup K%</button>
                </div>
                <div class="tab-panel ${tab === "pitches" ? "active" : ""}" data-panel="pitches">
                  ${renderPitchPanel(r)}
                </div>
                <div class="tab-panel ${tab === "lineup" ? "active" : ""}" data-panel="lineup">
                  ${renderLineupPanel(r)}
                </div>
              </div>
            </td>
          </tr>`;
      }).join("");

      document.querySelectorAll("thead th").forEach(th => {
        th.classList.toggle("active", th.dataset.key === state.sortKey);
      });
    }

    el.tbody.addEventListener("click", (e) => {
      const tabBtn = e.target.closest(".tab");
      if (tabBtn) {
        e.stopPropagation();
        const tabs = tabBtn.closest(".tabs");
        const id = tabs.dataset.id;
        state.tabById[id] = tabBtn.dataset.tab;
        state.openId = id;
        render();
        return;
      }
      const tr = e.target.closest("tr.matchup");
      if (!tr) return;
      const id = tr.dataset.id;
      state.openId = state.openId === id ? null : id;
      if (state.openId && !state.tabById[state.openId]) {
        state.tabById[state.openId] = "pitches";
      }
      render();
    });

    el.q.addEventListener("input", () => { state.q = el.q.value; render(); });
    el.lineupFilter.addEventListener("change", () => { state.lineup = el.lineupFilter.value; render(); });
    el.statusFilter.addEventListener("change", () => { state.status = el.statusFilter.value; render(); });
    el.sort.addEventListener("change", () => {
      const [k, d] = el.sort.value.split(":");
      state.sortKey = k;
      state.sortDir = d;
      render();
    });
    document.querySelectorAll("thead th").forEach(th => {
      th.addEventListener("click", () => {
        const key = th.dataset.key;
        if (state.sortKey === key) {
          state.sortDir = state.sortDir === "asc" ? "desc" : "asc";
        } else {
          state.sortKey = key;
          state.sortDir = key === "pitcher" || key === "game" || key === "rank" ? "asc" : "desc";
        }
        el.sort.value = `${state.sortKey}:${state.sortDir}`;
        render();
      });
    });

    renderMeta();
    render();
  </script>
</body>
</html>
"""
