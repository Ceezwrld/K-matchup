"""Strike-zone layer: pitcher location maps, batter zone profiles, zone fit.

Display / Hits-prop context only — nothing here changes ``expected_ks``.

Grid: 5x5 cells in the catcher's view. The middle 3x3 is the rulebook zone
(plate width ±0.83 ft incl. ball radius; height normalized per pitch with
``sz_bot``/``sz_top``). The outer ring is the chase / shadow band; anything
further out folds into the nearest ring cell. Cell index = row * 5 + col,
row 0 = top (high), col 0 = catcher's left (third-base side).

Batter cells are shrunk toward the batter's own baseline so thin cells read
neutral instead of noisy:
    cell_all  = (sum_all  + K * batter_overall) / (n_all  + K)
    cell_hand = (sum_hand + K * cell_all)       / (n_hand + K)
where "hand" = pitches from today's pitcher's throwing hand.
"""

from __future__ import annotations

import math
from typing import Any

import numpy as np
import pandas as pd

from sharpen import (
    STATCAST_FRAMES,
    SWING_DESCS,
    WHIFF_DESCS,
    effective_bat_side,
)

GRID = 5
CELLS = GRID * GRID
HALF_PLATE_FT = 0.83
X_EDGES = np.array(
    [-HALF_PLATE_FT, -HALF_PLATE_FT / 3.0, HALF_PLATE_FT / 3.0, HALF_PLATE_FT]
)
Z_EDGES = np.array([0.0, 1.0 / 3.0, 2.0 / 3.0, 1.0])  # normalized height
INNER = frozenset(r * GRID + c for r in range(1, 4) for c in range(1, 4))

# League-ish baselines used only as the top-level shrink target.
LEAGUE_XBA_CON = 0.330
LEAGUE_XWOBA_CON = 0.370
LEAGUE_WHIFF = 0.25
LEAGUE_SWING = 0.47

K_CONTACT = 20.0  # batted balls
K_SWING = 20.0  # pitches (swing rate) / swings (whiff rate)
K_BASELINE = 40.0  # batter overall vs hand → all-hands

# Zone-fit labels on xwOBA-on-contact delta (pitcher locations vs batter baseline).
FIT_HOT = 0.015
FIT_COLD = -0.015
HOT_CELL_MARGIN = 0.040
MIN_PITCHER_PITCHES = 150
MIN_BATTER_PITCHES = 200


def _cell_index(df: pd.DataFrame) -> pd.Series:
    x = pd.to_numeric(df["plate_x"], errors="coerce")
    z = pd.to_numeric(df["plate_z"], errors="coerce")
    top = pd.to_numeric(df.get("sz_top"), errors="coerce")
    bot = pd.to_numeric(df.get("sz_bot"), errors="coerce")
    # Fallback zone height when sz_* are missing (rare).
    top = top.fillna(3.4)
    bot = bot.fillna(1.6)
    height = (top - bot).where((top - bot) > 0.5, 1.8)
    zn = (z - bot) / height
    col = np.searchsorted(X_EDGES, x.to_numpy(), side="right")
    # Row 0 is high: invert normalized height.
    row = GRID - 1 - np.searchsorted(Z_EDGES, zn.to_numpy(), side="right")
    idx = pd.Series(row * GRID + col, index=df.index, dtype="float")
    idx[x.isna() | z.isna()] = np.nan
    return idx


def _prep(df: pd.DataFrame | None) -> pd.DataFrame | None:
    if df is None or df.empty:
        return None
    work = df.copy()
    work["cell"] = _cell_index(work)
    work = work[work["cell"].notna()].copy()
    if work.empty:
        return None
    work["cell"] = work["cell"].astype(int)
    desc = work.get("description")
    desc = (
        desc.astype(str).str.lower()
        if desc is not None
        else pd.Series("", index=work.index)
    )
    work["is_swing"] = desc.isin(SWING_DESCS)
    work["is_whiff"] = desc.isin(WHIFF_DESCS)
    typ = work.get("type")
    work["is_bip"] = (
        typ.astype(str).str.upper().eq("X")
        if typ is not None
        else pd.Series(False, index=work.index)
    )
    for col in ("estimated_ba_using_speedangle", "estimated_woba_using_speedangle"):
        if col in work.columns:
            work[col] = pd.to_numeric(work[col], errors="coerce")
        else:
            work[col] = np.nan
    for col in ("stand", "p_throws"):
        if col in work.columns:
            work[col] = work[col].astype(str).str.upper()
        else:
            work[col] = ""
    return work


def _round_list(values: np.ndarray, digits: int) -> list[float | None]:
    out: list[float | None] = []
    for v in values:
        out.append(None if v is None or not np.isfinite(v) else round(float(v), digits))
    return out


# ---------------------------------------------------------------------------
# Pitcher side
# ---------------------------------------------------------------------------


def pitcher_location_maps(pitcher_id: int | None) -> dict[str, Any] | None:
    """Share of pitches per cell vs LHB / RHB (+ his whiff% by cell)."""
    if pitcher_id is None:
        return None
    work = _prep(STATCAST_FRAMES.get(("pitcher", int(pitcher_id))))
    if work is None:
        return None
    out: dict[str, Any] = {}
    for side in ("L", "R"):
        sub = work[work["stand"] == side]
        n = int(len(sub))
        if n < MIN_PITCHER_PITCHES:
            out[side] = None
            continue
        counts = np.bincount(sub["cell"], minlength=CELLS)[:CELLS].astype(float)
        swings = np.bincount(
            sub["cell"], weights=sub["is_swing"].astype(float), minlength=CELLS
        )[:CELLS]
        whiffs = np.bincount(
            sub["cell"], weights=sub["is_whiff"].astype(float), minlength=CELLS
        )[:CELLS]
        with np.errstate(invalid="ignore", divide="ignore"):
            whiff = np.where(swings >= 8, whiffs / swings, np.nan)
        share = counts / counts.sum()
        out[side] = {
            "pitches": n,
            "share": _round_list(share, 4),
            "whiff": _round_list(whiff, 3),
            "in_zone_pct": round(100.0 * float(share[list(INNER)].sum()), 1),
        }
    if not out.get("L") and not out.get("R"):
        return None
    return out


# ---------------------------------------------------------------------------
# Batter side
# ---------------------------------------------------------------------------


def _shrunk_rates(
    sub: pd.DataFrame,
    prior: np.ndarray | float,
    num_col: str | None,
    den_mask: str | None,
    k: float,
    *,
    mean_of: str | None = None,
) -> tuple[np.ndarray, np.ndarray]:
    """Per-cell shrunk rate. Either a ratio (num/den masks) or mean of a column."""
    prior_arr = np.broadcast_to(np.asarray(prior, dtype=float), (CELLS,))
    if sub is None or sub.empty:
        return prior_arr.copy(), np.zeros(CELLS)
    if mean_of is not None:
        vals = sub[sub["is_bip"] & sub[mean_of].notna()]
        n = np.bincount(vals["cell"], minlength=CELLS)[:CELLS].astype(float)
        s = np.bincount(vals["cell"], weights=vals[mean_of], minlength=CELLS)[:CELLS]
    else:
        base = sub[sub[den_mask]] if den_mask else sub
        n = np.bincount(base["cell"], minlength=CELLS)[:CELLS].astype(float)
        s = np.bincount(
            base["cell"], weights=base[num_col].astype(float), minlength=CELLS
        )[:CELLS]
    return (s + k * prior_arr) / (n + k), n


def _overall(sub: pd.DataFrame, league: float, *, mean_of=None, num=None, den=None) -> float:
    if sub is None or sub.empty:
        return league
    if mean_of is not None:
        vals = sub.loc[sub["is_bip"], mean_of].dropna()
        n, s = float(len(vals)), float(vals.sum())
    else:
        base = sub[sub[den]] if den else sub
        n, s = float(len(base)), float(base[num].sum())
    return (s + K_BASELINE * league) / (n + K_BASELINE)


def batter_zone_profile(
    batter_id: int | None, pitcher_hand: str | None
) -> dict[str, Any] | None:
    """Per-cell xBA / xwOBA on contact, swing% and whiff% vs this pitcher's hand."""
    if batter_id is None:
        return None
    work = _prep(STATCAST_FRAMES.get(("batter", int(batter_id))))
    if work is None or len(work) < MIN_BATTER_PITCHES:
        return None
    hand = (pitcher_hand or "").upper()
    hsub = work[work["p_throws"] == hand] if hand in ("L", "R") else work

    metrics = {
        "xba": dict(mean_of="estimated_ba_using_speedangle", league=LEAGUE_XBA_CON, k=K_CONTACT),
        "xwoba": dict(mean_of="estimated_woba_using_speedangle", league=LEAGUE_XWOBA_CON, k=K_CONTACT),
        "swing": dict(num="is_swing", den=None, league=LEAGUE_SWING, k=K_SWING),
        "whiff": dict(num="is_whiff", den="is_swing", league=LEAGUE_WHIFF, k=K_SWING),
    }
    profile: dict[str, Any] = {
        "pitches_vs_hand": int(len(hsub)),
        "pitches_all": int(len(work)),
        "hand": hand or "all",
    }
    for key, spec in metrics.items():
        mean_of = spec.get("mean_of")
        num, den = spec.get("num"), spec.get("den")
        all_base = _overall(work, spec["league"], mean_of=mean_of, num=num, den=den)
        hand_base = (
            _overall(hsub, all_base, mean_of=mean_of, num=num, den=den)
            if len(hsub)
            else all_base
        )
        cell_all, _ = _shrunk_rates(work, all_base, num, den, spec["k"], mean_of=mean_of)
        cell_hand, n_hand = _shrunk_rates(hsub, cell_all, num, den, spec["k"], mean_of=mean_of)
        profile[key] = cell_hand
        profile[f"{key}_base"] = hand_base
        profile[f"{key}_n"] = n_hand
    return profile


# ---------------------------------------------------------------------------
# Fit: pitcher locations x batter zones
# ---------------------------------------------------------------------------


def zone_fit(loc_share: list[float | None], profile: dict[str, Any]) -> dict[str, Any]:
    """Expected contact quality / whiff where *this* pitcher puts the ball.

    Contact weight per cell = pitcher share × batter swing% × (1 − whiff%), so
    waste pitches the batter never offers at don't move the read.
    """
    loc = np.array([0.0 if v is None else float(v) for v in loc_share])
    swing = profile["swing"]
    whiff = profile["whiff"]
    contact_w = loc * swing * (1.0 - whiff)
    swing_w = loc * swing
    out: dict[str, Any] = {}
    for key in ("xba", "xwoba"):
        base = float(profile[f"{key}_base"])
        if contact_w.sum() > 0:
            val = float((contact_w * profile[key]).sum() / contact_w.sum())
        else:
            val = base
        out[f"zone_{key}"] = round(val, 3)
        out[f"zone_{key}_base"] = round(base, 3)
        out[f"zone_{key}_delta"] = round(val - base, 3)
    wbase = float(profile["whiff_base"])
    wval = float((swing_w * whiff).sum() / swing_w.sum()) if swing_w.sum() > 0 else wbase
    out["zone_whiff_pct"] = round(100.0 * wval, 1)
    out["zone_whiff_base_pct"] = round(100.0 * wbase, 1)
    out["zone_whiff_delta"] = round(100.0 * (wval - wbase), 1)
    hot = [
        i
        for i in range(CELLS)
        if profile["xwoba"][i] - float(profile["xwoba_base"]) >= HOT_CELL_MARGIN
        and profile["xwoba_n"][i] >= 3
    ]
    out["zone_hot_cells"] = hot
    out["zone_hot_share"] = round(100.0 * float(loc[hot].sum()), 1) if hot else 0.0
    d = out["zone_xwoba_delta"]
    out["zone_fit"] = "hot" if d >= FIT_HOT else ("cold" if d <= FIT_COLD else "neutral")
    return out


def enrich_lineup_zones(
    batter_detail: list[dict[str, Any]],
    pitcher_id: int | None,
    pitcher_hand: str | None,
) -> dict[str, Any] | None:
    """Attach zone profile + fit to each batter; return the pitcher's maps."""
    maps = pitcher_location_maps(pitcher_id)
    for b in batter_detail or []:
        try:
            bid = int(b.get("batter_id"))
        except (TypeError, ValueError):
            continue
        profile = batter_zone_profile(bid, pitcher_hand)
        if profile is None:
            continue
        side = effective_bat_side(b.get("bat_side"), pitcher_hand) or "R"
        b["zone_side"] = side
        b["zone_profile"] = {
            "xba": _round_list(profile["xba"], 3),
            "xwoba": _round_list(profile["xwoba"], 3),
            "whiff": _round_list(profile["whiff"], 3),
            "xba_base": round(float(profile["xba_base"]), 3),
            "xwoba_base": round(float(profile["xwoba_base"]), 3),
            "whiff_base": round(float(profile["whiff_base"]), 3),
            "pitches_vs_hand": profile["pitches_vs_hand"],
            "hand": profile["hand"],
        }
        side_map = (maps or {}).get(side)
        if side_map:
            b["zone_loc"] = side_map["share"]
            b.update(zone_fit(side_map["share"], profile))
    return maps


def fmt_delta(value: Any, digits: int = 3) -> str:
    if value is None or (isinstance(value, float) and math.isnan(value)):
        return "—"
    v = float(value)
    s = f"{abs(v):.{digits}f}".lstrip("0") if digits == 3 else f"{abs(v):.{digits}f}"
    return ("+" if v >= 0 else "−") + s
