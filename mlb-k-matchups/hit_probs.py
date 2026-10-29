"""Hits / H+R+RBI / RBI probabilities for each lineup batter (Kalshi "N+" style).

Per-PA hit chance vs the starter = log5(batter H/PA, starter H/BF, league), both
season-to-date and shrunk toward league. PAs vs the starter come from the
batter's slot and the starter's projected BF (slot s sees him
ceil((BF - (s-1)) / 9) times); the rest are vs a league-average bullpen.
Hits = starter-binomial + bullpen-binomial, mixed over the slot's PA count.

H+R+RBI and RBI: a mean fit on graded history, then each line (1+, 2+, …)
gets its own logistic calibration on log(mean) because those counts are
lumpier than any single count distribution (``grade_hits.py`` →
``hits-calibration.json``). Display only — never feeds
``expected_ks`` or ``hits_score``.
"""

from __future__ import annotations

import json
import math
from datetime import date as _date
from pathlib import Path
from typing import Any, Iterable

import pandas as pd
import requests

import prior_season

GAMELOG_URL = (
    "https://statsapi.mlb.com/api/v1/people?personIds={ids}"
    "&hydrate=stats(group=[{group}],type=[gameLog],season={year},gameType=[{gt}])"
)
GAME_TYPES = ("R", "F", "D", "L", "W")
CALIBRATION_PATH = Path(__file__).resolve().parent.parent / "hits-calibration.json"

LEAGUE_H_PA = 0.222
LEAGUE_R_PA = 0.118
LEAGUE_RBI_PA = 0.113
K_BAT_H = 80.0  # PA of league prior for batter H/PA
K_BAT_RR = 120.0  # PA of league prior for R/PA and RBI/PA
K_PIT_H = 150.0  # BF of league prior for pitcher H/BF

# Plate appearances per game by lineup slot (2026 graded history) — overwritten
# by hits-calibration.json when present.
DEFAULT_SLOT_PA = {
    1: {3: 0.06, 4: 0.50, 5: 0.40, 6: 0.04},
    2: {3: 0.08, 4: 0.55, 5: 0.34, 6: 0.03},
    3: {3: 0.10, 4: 0.58, 5: 0.30, 6: 0.02},
    4: {3: 0.14, 4: 0.60, 5: 0.25, 6: 0.01},
    5: {3: 0.18, 4: 0.62, 5: 0.19, 6: 0.01},
    6: {3: 0.24, 4: 0.60, 5: 0.15, 6: 0.01},
    7: {3: 0.32, 4: 0.56, 5: 0.12},
    8: {3: 0.40, 4: 0.51, 5: 0.09},
    9: {3: 0.48, 4: 0.45, 5: 0.07},
}
DEFAULT_CAL = {
    "hit_scale": 1.0,
    "hrr": {"a": 0.0, "b_h": 1.0, "b_rr": 1.0, "r": 6.0},
    "rbi": {"a": 0.0, "b": 1.0, "r": 3.0},
}
HIT_LINES = (1, 2, 3)
HRR_LINES = (1, 2, 3, 4)
RBI_LINES = (1, 2)


# ---------------------------------------------------------------------------
# Data
# ---------------------------------------------------------------------------


def fetch_gamelogs(
    ids: Iterable[int], year: int, group: str, *, timeout: int = 60
) -> pd.DataFrame:
    """One row per (player, game) with counting stats, regular + postseason."""
    ids = sorted({int(x) for x in ids if x is not None and not pd.isna(x)})
    rows: list[dict[str, Any]] = []
    for gt in GAME_TYPES:
        for i in range(0, len(ids), 40):
            chunk = ",".join(str(x) for x in ids[i : i + 40])
            url = GAMELOG_URL.format(ids=chunk, group=group, year=year, gt=gt)
            try:
                data = requests.get(url, timeout=timeout).json()
            except Exception:  # noqa: BLE001 - soft-fail one chunk
                continue
            for p in data.get("people", []):
                for st in p.get("stats", []):
                    for s in st.get("splits", []):
                        stat = s.get("stat", {})
                        rows.append(
                            {
                                "player_id": int(p["id"]),
                                "date": s.get("date"),
                                "game_pk": (s.get("game") or {}).get("gamePk"),
                                "pa": int(stat.get("plateAppearances") or stat.get("battersFaced") or 0),
                                "h": int(stat.get("hits") or 0),
                                "r": int(stat.get("runs") or 0),
                                "rbi": int(stat.get("rbi") or 0),
                                "hr": int(stat.get("homeRuns") or 0),
                                "gs": int(stat.get("gamesStarted") or 0),
                            }
                        )
    df = pd.DataFrame(rows)
    if df.empty:
        return df
    return df.drop_duplicates(["player_id", "game_pk"]).sort_values(["player_id", "date"])


def to_date_totals(logs: pd.DataFrame, before: str) -> dict[int, dict[str, float]]:
    """Season totals from games strictly before ``before`` (YYYY-MM-DD)."""
    if logs is None or logs.empty:
        return {}
    prior = logs[logs["date"] < before]
    agg = prior.groupby("player_id")[["pa", "h", "r", "rbi", "hr"]].sum()
    return {int(pid): row.to_dict() for pid, row in agg.iterrows()}


# ---------------------------------------------------------------------------
# Math
# ---------------------------------------------------------------------------


def _shrink(num: float, den: float, prior: float, k: float) -> float:
    return (num + k * prior) / (den + k)


def log5(pb: float, pp: float, pl: float) -> float:
    a = pb * pp / pl
    b = (1 - pb) * (1 - pp) / (1 - pl)
    return a / (a + b)


def _binom_pmf(n: int, p: float) -> list[float]:
    return [math.comb(n, k) * p**k * (1 - p) ** (n - k) for k in range(n + 1)]


def _convolve(a: list[float], b: list[float]) -> list[float]:
    out = [0.0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i + j] += x * y
    return out


def _nb_sf(mu: float, r: float, n: int) -> float:
    """P(X >= n) for negative binomial with mean mu, size r."""
    if mu <= 0:
        return 0.0 if n > 0 else 1.0
    p = r / (r + mu)
    q = 1 - p
    pmf = math.exp(r * math.log(p))
    cdf = pmf
    for k in range(1, n):
        pmf *= (k - 1 + r) / k * q
        cdf += pmf
    return max(0.0, 1.0 - cdf)


def _sigmoid(x: float) -> float:
    return 1.0 / (1.0 + math.exp(-x))


def pa_vs_starter(slot: int, total_pa: int, starter_bf: float) -> int:
    if starter_bf is None or not math.isfinite(starter_bf):
        starter_bf = 22.0
    n = max(0, math.ceil((float(starter_bf) - (slot - 1)) / 9.0))
    return min(total_pa, n)


def batter_prop_probs(
    *,
    slot: int,
    bat: dict[str, float] | None,
    pit: dict[str, float] | None,
    starter_bf: float,
    cal: dict[str, Any] | None = None,
) -> dict[str, Any]:
    cal = cal or DEFAULT_CAL
    slot_pa = {int(k): {int(a): float(b) for a, b in v.items()} for k, v in (cal.get("slot_pa") or DEFAULT_SLOT_PA).items()}
    bat = bat or {}
    pit = pit or {}
    pb = _shrink(bat.get("h", 0.0), bat.get("pa", 0.0), LEAGUE_H_PA, K_BAT_H)
    pp = _shrink(pit.get("h", 0.0), pit.get("pa", 0.0), LEAGUE_H_PA, K_PIT_H)
    scale = float(cal.get("hit_scale", 1.0))
    p_sp = min(0.6, log5(pb, pp, LEAGUE_H_PA) * scale)
    p_pen = min(0.6, pb * scale)
    dist = slot_pa.get(int(slot)) or slot_pa[5]
    hits_pmf = [0.0] * 8
    exp_pa = 0.0
    exp_h = 0.0
    for n_pa, w in dist.items():
        n_sp = pa_vs_starter(int(slot), n_pa, starter_bf)
        pmf = _convolve(_binom_pmf(n_sp, p_sp), _binom_pmf(n_pa - n_sp, p_pen))
        for k, v in enumerate(pmf[: len(hits_pmf)]):
            hits_pmf[k] += w * v
        exp_pa += w * n_pa
        exp_h += w * (n_sp * p_sp + (n_pa - n_sp) * p_pen)
    out: dict[str, Any] = {
        "exp_pa": round(exp_pa, 2),
        "exp_hits": round(exp_h, 3),
        "p_hit_pa_sp": round(p_sp, 3),
    }
    for n in HIT_LINES:
        out[f"p_h{n}"] = round(max(0.0, 1.0 - sum(hits_pmf[:n])), 4)

    r_pa = _shrink(bat.get("r", 0.0), bat.get("pa", 0.0), LEAGUE_R_PA, K_BAT_RR)
    rbi_pa = _shrink(bat.get("rbi", 0.0), bat.get("pa", 0.0), LEAGUE_RBI_PA, K_BAT_RR)
    hc = cal.get("hrr") or DEFAULT_CAL["hrr"]
    mu_hrr = max(0.05, hc["a"] + hc["b_h"] * exp_h + hc["b_rr"] * exp_pa * (r_pa + rbi_pa))
    out["exp_hrr"] = round(mu_hrr, 3)
    hl = cal.get("hrr_lines") or {}
    for n in HRR_LINES:
        coef = hl.get(str(n))
        if coef:
            p = _sigmoid(coef[0] + coef[1] * math.log(mu_hrr))
        else:
            p = _nb_sf(mu_hrr, float(hc["r"]), n)
        out[f"p_hrr{n}"] = round(p, 4)
    rc = cal.get("rbi") or DEFAULT_CAL["rbi"]
    mu_rbi = max(0.02, rc["a"] + rc["b"] * exp_pa * rbi_pa)
    out["exp_rbi"] = round(mu_rbi, 3)
    rl = cal.get("rbi_lines") or {}
    for n in RBI_LINES:
        coef = rl.get(str(n))
        if coef:
            p = _sigmoid(coef[0] + coef[1] * math.log(mu_rbi))
        else:
            p = _nb_sf(mu_rbi, float(rc["r"]), n)
        out[f"p_rbi{n}"] = round(p, 4)
    return out


def load_calibration(path: Path | str | None = None) -> dict[str, Any]:
    p = Path(path) if path else CALIBRATION_PATH
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        if "hit_scale" in data:
            return data
    except (OSError, ValueError):
        pass
    return dict(DEFAULT_CAL)


# ---------------------------------------------------------------------------
# Live board
# ---------------------------------------------------------------------------


def enrich_board_hit_probs(
    rows: list[dict[str, Any]],
    game_date: str,
    *,
    log=None,
) -> None:
    """Add p_h1/p_h2/p_hrr2/... to each batter in each scored row (in place)."""
    year = int(game_date[:4])
    bat_ids: set[int] = set()
    pit_ids: set[int] = set()
    for row in rows:
        if row.get("status") != "ok":
            continue
        try:
            pit_ids.add(int(row.get("pitcher_id")))
        except (TypeError, ValueError):
            pass
        for b in row.get("batter_detail") or []:
            try:
                bat_ids.add(int(b.get("batter_id")))
            except (TypeError, ValueError):
                pass
    if not bat_ids:
        return
    cal = load_calibration()
    bat_logs = fetch_gamelogs(bat_ids, year, "hitting")
    pit_logs = fetch_gamelogs(pit_ids, year, "pitching")
    bat_tot = to_date_totals(bat_logs, game_date)
    pit_tot = to_date_totals(pit_logs, game_date)
    py = prior_season.prior_year()
    if py is not None:
        # Early season: top up thin season-to-date totals with last season.
        prev_b = fetch_gamelogs(bat_ids, py, "hitting")
        prev_p = fetch_gamelogs(pit_ids, py, "pitching")
        bat_tot = prior_season.blend_totals(
            bat_tot, to_date_totals(prev_b, f"{py + 1}-01-01"),
            n_key="pa", target=prior_season.TARGET_BATTER_PA,
        )
        pit_tot = prior_season.blend_totals(
            pit_tot, to_date_totals(prev_p, f"{py + 1}-01-01"),
            n_key="pa", target=prior_season.TARGET_PITCHER_BF,
        )
    for row in rows:
        if row.get("status") != "ok":
            continue
        try:
            pid = int(row.get("pitcher_id"))
        except (TypeError, ValueError):
            pid = None
        bf = row.get("projected_bf")
        for idx, b in enumerate(row.get("batter_detail") or [], start=1):
            try:
                bid = int(b.get("batter_id"))
            except (TypeError, ValueError):
                continue
            slot = b.get("slot")
            try:
                slot = int(slot)
            except (TypeError, ValueError):
                slot = idx
            probs = batter_prop_probs(
                slot=max(1, min(9, slot)),
                bat=bat_tot.get(bid),
                pit=pit_tot.get(pid) if pid is not None else None,
                starter_bf=float(bf) if bf is not None else 22.0,
                cal=cal,
            )
            b.update(probs)
    if log:
        log(True, f"hit probabilities: {len(bat_tot)} batters with season-to-date logs")


def today() -> str:
    return _date.today().isoformat()
