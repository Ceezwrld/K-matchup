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
        clean_detail = []
        for b in detail:
            clean_detail.append(
                {
                    "slot": _json_safe(b.get("slot")),
                    "batter_id": _json_safe(b.get("batter_id")),
                    "batter": b.get("batter"),
                    "expected_k_pct": _json_safe(b.get("expected_k_pct")),
                    "expected_whiff_pct": _json_safe(b.get("expected_whiff_pct")),
                    "status": b.get("status"),
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
    padding: 0.85rem 1rem 1.1rem 3.4rem;
    animation: expand 0.28s ease both;
  }
  tr.open + tr.detail-row .detail { display: block; }
  .detail h3 {
    margin: 0 0 0.55rem;
    font-size: 0.78rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: var(--muted);
  }
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
      TTO = times through the order. Click a row for each batter’s arsenal-weighted K%.
      Re-run
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

    function render() {
      const rows = filtered();
      el.empty.hidden = rows.length > 0;
      el.tbody.innerHTML = rows.map((r, i) => {
        const id = rowId(r, i);
        const open = state.openId === id ? "open" : "";
        const kind = lineupKind(r.lineup_source);
        const batters = (r.batters || []).map(b => {
          const miss = b.status !== "ok";
          return `<div class="batter ${miss ? "missing" : ""}">
            <span><span class="slot">${b.slot ?? ""}.</span> ${b.batter || "—"}</span>
            <span class="k">${miss ? "n/a" : fmt(b.expected_k_pct, 1) + "%"}</span>
          </div>`;
        }).join("");
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
                <h3>
                  Projected outing ${fmt(r.projected_ip, 1)} IP ·
                  ${r.times_through_order == null ? "—" : fmt(r.times_through_order) + "×"} through order ·
                  BF ${r.projected_bf ?? r.batters_faced_assumed ?? "—"}
                  (${r.outing_source || "n/a"}) ·
                  lineup cover ${pct(r.lineup_coverage)} ·
                  1× reference ${fmt(r.expected_ks_1x)} Ks
                </h3>
                <div class="batter-grid">${batters || "<div class='empty'>No batter detail</div>"}</div>
              </div>
            </td>
          </tr>`;
      }).join("");

      document.querySelectorAll("thead th").forEach(th => {
        th.classList.toggle("active", th.dataset.key === state.sortKey);
      });
    }

    el.tbody.addEventListener("click", (e) => {
      const tr = e.target.closest("tr.matchup");
      if (!tr) return;
      const id = tr.dataset.id;
      state.openId = state.openId === id ? null : id;
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
