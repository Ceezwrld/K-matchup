"""Turn Exp K into strikeout-line probabilities (Kalshi-style "N+ strikeouts").

The model's ``expected_ks`` is first recalibrated against graded history
(``mu = a + b * expected_ks``), then a negative binomial with dispersion ``r``
gives P(K >= N). Parameters live in ``k-calibration.json`` at the repo root and
are refit by ``grade_history.py``; the defaults below are the 2026 fit
(1,868 graded starts, 7/21–10/27).

Fair price in cents = 100 × P. On Kalshi, buying YES below the fair price (or
NO below 100 − fair) is the edge. Display / sizing only — Exp K is unchanged.
"""

from __future__ import annotations

import json
import math
from pathlib import Path
from typing import Any

import pandas as pd

DEFAULT_CALIBRATION = {"a": 0.552, "b": 0.874, "r": 37.0, "n": 1868, "fit_through": "2026-10-27"}
CALIBRATION_PATH = Path(__file__).resolve().parent.parent / "k-calibration.json"
K_LINES = (3, 4, 5, 6, 7, 8, 9)


def load_calibration(path: Path | str | None = None) -> dict[str, Any]:
    p = Path(path) if path else CALIBRATION_PATH
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
        if all(k in data for k in ("a", "b", "r")):
            return data
    except (OSError, ValueError):
        pass
    return dict(DEFAULT_CALIBRATION)


def _nb_pmf_list(mu: float, r: float, kmax: int) -> list[float]:
    """Negative binomial pmf 0..kmax (mean mu, size r) via stable recursion."""
    p = r / (r + mu)
    q = 1.0 - p
    pmf = [math.exp(r * math.log(p))]
    for k in range(1, kmax + 1):
        pmf.append(pmf[-1] * (k - 1 + r) / k * q)
    return pmf


def k_line_probs(expected_ks: Any, cal: dict[str, Any] | None = None) -> dict[str, Any]:
    """{'k_mu': calibrated mean, 'p_k3': P(K>=3), …, 'k_median': int}."""
    out: dict[str, Any] = {"k_mu": None, "k_median": None}
    for n in K_LINES:
        out[f"p_k{n}"] = None
    try:
        e = float(expected_ks)
    except (TypeError, ValueError):
        return out
    if math.isnan(e):
        return out
    cal = cal or DEFAULT_CALIBRATION
    mu = max(0.3, float(cal["a"]) + float(cal["b"]) * e)
    pmf = _nb_pmf_list(mu, float(cal["r"]), 25)
    cdf = 0.0
    median = None
    cum: list[float] = []
    for k, pk in enumerate(pmf):
        cdf += pk
        cum.append(cdf)
        if median is None and cdf >= 0.5:
            median = k
    out["k_mu"] = round(mu, 2)
    out["k_median"] = median
    for n in K_LINES:
        out[f"p_k{n}"] = round(1.0 - cum[n - 1], 4)
    return out


def apply_k_probs(df: pd.DataFrame, cal: dict[str, Any] | None = None) -> pd.DataFrame:
    cal = cal or load_calibration()
    rows = [k_line_probs(v, cal) for v in df["expected_ks"].tolist()]
    probs = pd.DataFrame(rows, index=df.index)
    for col in probs.columns:
        df[col] = probs[col]
    return df


def ladder(row: dict[str, Any]) -> list[dict[str, Any]]:
    """[{n, line, p, fair_yes, fair_no}] for display."""
    out = []
    for n in K_LINES:
        p = row.get(f"p_k{n}")
        if p is None or (isinstance(p, float) and math.isnan(p)):
            continue
        out.append(
            {
                "n": n,
                "line": f"O{n - 0.5:g}",
                "p": float(p),
                "fair_yes": int(round(100 * float(p))),
                "fair_no": int(round(100 * (1 - float(p)))),
            }
        )
    return out
