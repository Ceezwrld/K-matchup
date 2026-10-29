"""Prior-season blending so the model works from Opening Day.

Every input the model pulls is current-season only. In early April that means
tiny samples (or none), so starters go unscored and rates swing wildly. This
module tops up each player's current-season sample with last season's data
until the current sample reaches a target, then phases the prior out:

    prior weight f = min(1, max(0, target − n_current) / n_prior)

so last season counts as at most ``target`` PA/BF/pitches and shrinks to zero
as the new season fills in. Rookies with no prior are unchanged. Applied to:

- Savant arsenal + batter pitch-type leaderboards (``blend_long_frame``)
- Statcast pitch-level pulls → pitch mixes, pitch×hand K%, strike zones
  (``fill_pitch_frame``)
- Stats API season stats, FanGraphs, Savant contact quality, hit-prob logs
  (``blend_player_dicts`` / ``blend_totals``)

Recent-form (last 3 starts / last 10 games) is never blended.
"""

from __future__ import annotations

import math
from typing import Any, Iterable

import pandas as pd

# Targets: when the current season reaches these, last season drops out.
# Season-level rates (K%, AVG, BB/9, xwOBA…) stabilize fast → small targets.
TARGET_BATTER_PA = 200.0
TARGET_PITCHER_BF = 250.0
# Pitch-type / pitch-location splits are much noisier → last season keeps
# more weight. Opening-Day test (2027 data empty, 2026 prior): 900-pitch /
# 200-PA caps shrank arsenal K% 18.6 → 16.8; these caps reproduce 18.6.
TARGET_BATTER_PITCH_PA = 600.0
TARGET_BATTER_PITCHES = 2500
TARGET_PITCHER_PITCHES = 2500

CONFIG: dict[str, Any] = {"enabled": False, "prior_year": None}


def configure(prior_year: int | None) -> None:
    CONFIG["enabled"] = prior_year is not None
    CONFIG["prior_year"] = prior_year


def enabled() -> bool:
    return bool(CONFIG.get("enabled")) and CONFIG.get("prior_year") is not None


def prior_year() -> int | None:
    return CONFIG.get("prior_year") if enabled() else None


def _num(v: Any) -> float | None:
    if v is None or isinstance(v, bool):
        return None
    try:
        x = float(v)
    except (TypeError, ValueError):
        return None
    return None if math.isnan(x) else x


def prior_factor(n_cur: float, n_prior: float, target: float) -> float:
    if n_prior <= 0:
        return 0.0
    return max(0.0, min(1.0, (target - max(0.0, n_cur)) / n_prior))


# ---------------------------------------------------------------------------
# Dict-per-player outputs (Stats API / FanGraphs / Savant contact)
# ---------------------------------------------------------------------------


def blend_player_dicts(
    cur: dict[int, dict[str, Any]],
    prev: dict[int, dict[str, Any]],
    *,
    n_key: str,
    target: float,
    count_keys: Iterable[str] = (),
    rate_weights: dict[str, str] | None = None,
    keep_current: Iterable[str] = (),
) -> dict[int, dict[str, Any]]:
    """Blend per-player dicts. Rates are count-weighted; counts are added.

    ``rate_weights`` maps a rate key to the count key that weights it
    (default ``n_key``). ``keep_current`` keys (e.g. recent form) are never
    taken from the prior season.
    """
    if not prev:
        return cur
    count_keys = set(count_keys)
    keep_current = set(keep_current)
    rate_weights = rate_weights or {}
    out: dict[int, dict[str, Any]] = {}
    for pid in set(cur) | set(prev):
        c = dict(cur.get(pid) or {})
        p = prev.get(pid)
        if not p:
            out[pid] = c
            continue
        n_c = _num(c.get(n_key)) or 0.0
        n_p = _num(p.get(n_key)) or 0.0
        f = prior_factor(n_c, n_p, target)
        if f <= 0:
            out[pid] = c
            continue
        merged = dict(c)
        for k, vp in p.items():
            if k in keep_current:
                merged.setdefault(k, None)
                continue
            vc = c.get(k)
            if k in count_keys or k == n_key:
                merged[k] = (_num(vc) or 0.0) + f * (_num(vp) or 0.0)
                continue
            vpn = _num(vp)
            if vpn is None:
                if vc is None:
                    merged[k] = vp
                continue
            wk = rate_weights.get(k, n_key)
            wc = _num(c.get(wk)) or 0.0
            wp = _num(p.get(wk)) or 0.0
            vcn = _num(vc)
            if vcn is None or wc <= 0:
                merged[k] = vpn
            elif wp <= 0:
                merged[k] = vcn
            else:
                merged[k] = (wc * vcn + f * wp * vpn) / (wc + f * wp)
        merged["prior_share"] = round(f * n_p / (n_c + f * n_p), 3) if (n_c + f * n_p) > 0 else 0.0
        out[pid] = merged
    return out


def blend_totals(
    cur: dict[int, dict[str, float]],
    prev: dict[int, dict[str, float]],
    *,
    n_key: str,
    target: float,
) -> dict[int, dict[str, float]]:
    """Counting totals only: cur + f × prev."""
    out: dict[int, dict[str, float]] = {}
    for pid in set(cur) | set(prev):
        c = cur.get(pid) or {}
        p = prev.get(pid) or {}
        f = prior_factor(float(c.get(n_key) or 0), float(p.get(n_key) or 0), target)
        keys = set(c) | set(p)
        out[pid] = {k: float(c.get(k) or 0) + f * float(p.get(k) or 0) for k in keys}
    return out


# ---------------------------------------------------------------------------
# Long Savant leaderboards (player × pitch_type rows)
# ---------------------------------------------------------------------------


def blend_long_frame(
    cur: pd.DataFrame | None,
    prev: pd.DataFrame | None,
    *,
    count_col: str,
    rate_cols: Iterable[str],
    target: float,
    usage_col: str | None = None,
) -> pd.DataFrame:
    """Blend player × pitch_type rows; per-player prior factor on total count.

    Rates are count-weighted. ``usage_col`` (pitch usage %) is recomputed from
    the blended counts.
    """
    if prev is None or prev.empty:
        return cur if cur is not None else pd.DataFrame()
    if cur is None or cur.empty:
        cur = prev.iloc[0:0].copy()
    rate_cols = [c for c in rate_cols if c in prev.columns]
    cur = cur.copy()
    prev = prev.copy()
    for df in (cur, prev):
        df[count_col] = pd.to_numeric(df[count_col], errors="coerce").fillna(0.0)
        for c in rate_cols:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors="coerce")
    n_cur = cur.groupby("player_id")[count_col].sum()
    n_prev = prev.groupby("player_id")[count_col].sum()
    factors = {
        pid: prior_factor(float(n_cur.get(pid, 0.0)), float(npv), target)
        for pid, npv in n_prev.items()
    }
    prev["_w"] = prev["player_id"].map(factors).fillna(0.0) * prev[count_col]
    prev = prev[prev["_w"] > 0]
    cur["_w"] = cur[count_col]
    cur["_src"] = 0
    prev["_src"] = 1
    both = pd.concat([cur, prev], ignore_index=True, sort=False)
    if both.empty:
        return cur.drop(columns=["_w", "_src"], errors="ignore")
    rows = []
    for (pid, pt), g in both.groupby(["player_id", "pitch_type"], sort=False):
        base = g.sort_values("_src").iloc[0].copy()  # current-season row first
        w = g["_w"].astype(float)
        base[count_col] = float(w.sum())
        for c in rate_cols:
            vals = g[c]
            mask = vals.notna() & (w > 0)
            if mask.any():
                base[c] = float((vals[mask] * w[mask]).sum() / w[mask].sum())
        rows.append(base)
    out = pd.DataFrame(rows).drop(columns=["_w", "_src"], errors="ignore")
    if usage_col and usage_col in out.columns:
        tot = out.groupby("player_id")[count_col].transform("sum")
        out[usage_col] = 100.0 * out[count_col] / tot.where(tot > 0)
    out["player_id"] = pd.to_numeric(out["player_id"], errors="coerce").astype("Int64")
    return out.reset_index(drop=True)


# ---------------------------------------------------------------------------
# Statcast pitch-level frames
# ---------------------------------------------------------------------------


def fill_pitch_frame(
    cur: pd.DataFrame | None, prev: pd.DataFrame | None, target: int
) -> pd.DataFrame | None:
    """Top up a thin current-season pitch log with a deterministic sample of
    last season's pitches (up to ``target`` total)."""
    n_cur = 0 if cur is None else len(cur)
    if prev is None or prev.empty or n_cur >= target:
        return cur
    need = min(len(prev), target - n_cur)
    sample = prev.sample(n=need, random_state=7) if need < len(prev) else prev
    if cur is None or cur.empty:
        return sample.reset_index(drop=True)
    return pd.concat([cur, sample], ignore_index=True, sort=False)
