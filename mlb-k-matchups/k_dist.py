"""Strikeout distribution from PA-level K probs + volume (BF).

Product framing:
  Ks are plate-appearance interactions, not pitcher season K% alone.
  Separate (1) K probability per PA from (2) batters-faced / volume, then
  build a full outing distribution — the shape matters for props.

  Sportsbook lines are a question, not a target. Model edge ≠ true edge.
"""

from __future__ import annotations

from typing import Any

import pandas as pd


def pa_k_probabilities(
    batter_detail: list[dict[str, Any]] | None,
    batters_faced: int | float | None,
) -> list[float]:
    """Walk the batting order for projected BF → one K-prob per PA."""
    if not batter_detail:
        return []
    try:
        bf_n = max(0, int(round(float(batters_faced or 0))))
    except (TypeError, ValueError):
        return []
    if bf_n <= 0:
        return []
    n = len(batter_detail)
    probs: list[float] = []
    for i in range(bf_n):
        b = batter_detail[i % n]
        if str(b.get("status") or "") != "ok":
            continue
        try:
            p = float(b.get("expected_k_pct")) / 100.0
        except (TypeError, ValueError):
            continue
        if p < 0:
            p = 0.0
        if p > 1:
            p = 1.0
        probs.append(p)
    return probs


def scale_probs_to_mean(probs: list[float], target_mean: float) -> list[float]:
    """Preserve relative hitter differences; match final Exp K after overlays."""
    if not probs:
        return []
    cur = sum(probs)
    if cur <= 0 or target_mean is None or pd.isna(target_mean):
        return list(probs)
    target = max(0.0, float(target_mean))
    scale = target / cur
    out: list[float] = []
    for p in probs:
        q = p * scale
        if q < 0:
            q = 0.0
        if q > 1:
            q = 1.0
        out.append(q)
    return out


def poisson_binomial_pmf(probs: list[float]) -> list[float]:
    """Exact PMF for independent Bernoulli trials (different p_i)."""
    if not probs:
        return [1.0]
    pmf = [1.0]
    for p in probs:
        p = float(p)
        nxt = [0.0] * (len(pmf) + 1)
        for k, mass in enumerate(pmf):
            nxt[k] += mass * (1.0 - p)
            nxt[k + 1] += mass * p
        pmf = nxt
    s = sum(pmf) or 1.0
    return [m / s for m in pmf]


def _quantile_from_pmf(pmf: list[float], q: float) -> float:
    if not pmf:
        return float("nan")
    acc = 0.0
    target = min(1.0, max(0.0, float(q)))
    for k, mass in enumerate(pmf):
        acc += mass
        if acc >= target:
            return float(k)
    return float(len(pmf) - 1)


def p_over_line(pmf: list[float], line: float) -> float:
    """P(K > line) for a standard X.5 total (or any real line)."""
    if not pmf or line is None or (isinstance(line, float) and pd.isna(line)):
        return float("nan")
    # For .5 lines, K > 6.5 means K >= 7.
    need = int(float(line) + 1e-9) + 1
    return float(sum(pmf[need:])) if need < len(pmf) else 0.0


def summarize_k_distribution(
    probs: list[float],
    *,
    k_line: float | None = None,
) -> dict[str, Any]:
    """Summary stats + optional book-line over probability."""
    empty = {
        "k_dist_mean": float("nan"),
        "k_dist_sd": float("nan"),
        "k_p10": float("nan"),
        "k_p50": float("nan"),
        "k_p90": float("nan"),
        "k_p_ge_8": float("nan"),
        "k_p_ge_9": float("nan"),
        "k_p_ge_10": float("nan"),
        "k_p_over": float("nan"),
        "k_p_under": float("nan"),
        "k_dist_n_pa": 0,
        "k_dist_shape": "",
    }
    if not probs:
        return empty

    pmf = poisson_binomial_pmf(probs)
    mean = sum(i * m for i, m in enumerate(pmf))
    var = sum((i - mean) ** 2 * m for i, m in enumerate(pmf))
    sd = var**0.5
    p10 = _quantile_from_pmf(pmf, 0.10)
    p50 = _quantile_from_pmf(pmf, 0.50)
    p90 = _quantile_from_pmf(pmf, 0.90)
    p_ge_8 = float(sum(pmf[8:])) if len(pmf) > 8 else 0.0
    p_ge_9 = float(sum(pmf[9:])) if len(pmf) > 9 else 0.0
    p_ge_10 = float(sum(pmf[10:])) if len(pmf) > 10 else 0.0

    # Shape cue: wide right tail vs tight band around the mean.
    span = p90 - p10
    if p_ge_9 >= 0.18 and span >= 5:
        shape = "heavy_right_tail"
    elif span <= 3 and sd <= 1.6:
        shape = "tight"
    else:
        shape = "typical"

    p_over = float("nan")
    p_under = float("nan")
    if k_line is not None and not (isinstance(k_line, float) and pd.isna(k_line)):
        p_over = p_over_line(pmf, float(k_line))
        p_under = 1.0 - p_over

    return {
        "k_dist_mean": round(mean, 3),
        "k_dist_sd": round(sd, 3),
        "k_p10": p10,
        "k_p50": p50,
        "k_p90": p90,
        "k_p_ge_8": round(p_ge_8, 3),
        "k_p_ge_9": round(p_ge_9, 3),
        "k_p_ge_10": round(p_ge_10, 3),
        "k_p_over": round(p_over, 3) if p_over == p_over else float("nan"),
        "k_p_under": round(p_under, 3) if p_under == p_under else float("nan"),
        "k_dist_n_pa": len(probs),
        "k_dist_shape": shape,
    }


def rate_volume_decomposition(
    expected_k_pct: float | None,
    projected_bf: float | None,
    expected_ks: float | None,
) -> dict[str, Any]:
    """Transparent rate × volume vs order-walk / blended Exp K."""
    out = {
        "k_rate_pct": float("nan"),
        "k_volume_bf": float("nan"),
        "expected_ks_rate_x_bf": float("nan"),
        "k_volume_share_note": "",
    }
    try:
        rate = float(expected_k_pct)
        bf = float(projected_bf)
        exp = float(expected_ks) if expected_ks is not None else float("nan")
    except (TypeError, ValueError):
        return out
    if pd.isna(rate) or pd.isna(bf) or bf <= 0:
        return out
    naive = (rate / 100.0) * bf
    out["k_rate_pct"] = round(rate, 2)
    out["k_volume_bf"] = int(round(bf))
    out["expected_ks_rate_x_bf"] = round(naive, 3)
    if not pd.isna(exp):
        # How much of Exp K is “rate environment” vs walking order / overlays.
        out["k_volume_share_note"] = (
            f"rate×BF {naive:.2f} vs Exp {exp:.2f} "
            f"(order-walk + overlays; not pitcher season K% alone)"
        )
    return out


def book_model_read(
    *,
    expected_ks: float | None,
    k_line: float | None,
    k_p_over: float | None = None,
    k_dist_shape: str | None = None,
    expected_k_pct: float | None = None,
    projected_bf: float | None = None,
) -> str:
    """Plain-language book vs model note — question-first, not ticket lock."""
    if expected_ks is None or pd.isna(expected_ks):
        return ""
    if k_line is None or pd.isna(k_line):
        return (
            "No book K line — ask why the pitcher can reach the model total "
            f"({float(expected_ks):.1f} Exp) via PA matchups + volume, not season K% alone."
        )
    exp = float(expected_ks)
    line = float(k_line)
    edge = exp - line
    bits: list[str] = [
        f"Book {line:.1f} vs model {exp:.1f} (edge {edge:+.2f})."
    ]
    if abs(edge) < 0.4:
        bits.append("Aligned — size with lineup K environment + BF/IP, not 'edge'.")
    elif edge >= 1.0:
        bits.append(
            "Book soft vs model — ask why the book is lower (role, pitch count, "
            "platoon, market) before treating this as over edge. Public info ≠ edge."
        )
    elif edge <= -1.0:
        bits.append(
            "Book high vs model — name/SPIKE premium possible; do not soft-under "
            "on Exp alone. Resolve the disagreement first."
        )
    else:
        bits.append("Mild disagree — confirm with PA matchups + volume.")

    if k_p_over is not None and not pd.isna(k_p_over):
        bits.append(f"Model P(over {line:.1f}) ≈ {100 * float(k_p_over):.0f}%.")
    if k_dist_shape == "heavy_right_tail":
        bits.append("Distribution has a heavier right tail (ceiling games more live).")
    elif k_dist_shape == "tight":
        bits.append("Distribution is tighter around the mean (less nuke / floor swing).")
    if expected_k_pct is not None and projected_bf is not None:
        try:
            bits.append(
                f"Why ~{exp:.0f} Ks: lineup K env ~{float(expected_k_pct):.1f}% "
                f"× ~{int(round(float(projected_bf)))} BF (interaction + volume)."
            )
        except (TypeError, ValueError):
            pass
    return " ".join(bits)


def attach_k_distribution_to_row(row: dict[str, Any]) -> dict[str, Any]:
    """Mutate/return row with rate/volume + distribution + book read fields."""
    detail = row.get("batter_detail") or []
    bf = row.get("projected_bf") or row.get("batters_faced_assumed")
    probs = pa_k_probabilities(detail, bf)
    target = row.get("expected_ks")
    if probs and target is not None and not pd.isna(target):
        probs = scale_probs_to_mean(probs, float(target))

    k_line = row.get("k_line")
    try:
        k_line_f = float(k_line) if k_line is not None and not pd.isna(k_line) else None
    except (TypeError, ValueError):
        k_line_f = None

    dist = summarize_k_distribution(probs, k_line=k_line_f)
    decomp = rate_volume_decomposition(
        row.get("expected_k_pct"),
        bf,
        row.get("expected_ks"),
    )
    row.update(dist)
    row.update(decomp)
    row["book_model_note"] = book_model_read(
        expected_ks=row.get("expected_ks"),
        k_line=k_line_f,
        k_p_over=dist.get("k_p_over"),
        k_dist_shape=dist.get("k_dist_shape"),
        expected_k_pct=row.get("expected_k_pct"),
        projected_bf=bf,
    )
    return row


def enrich_dataframe_k_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Apply distribution + book read to every scored row."""
    if df is None or df.empty:
        return df
    out = df.copy()
    notes: list[str] = []
    records = out.to_dict(orient="records")
    enriched: list[dict[str, Any]] = []
    for rec in records:
        if str(rec.get("status") or "") == "ok" and rec.get("expected_ks") == rec.get(
            "expected_ks"
        ):
            attach_k_distribution_to_row(rec)
            note = rec.get("book_model_note") or ""
            if note:
                notes.append(f"{rec.get('pitcher')}: {note}")
        enriched.append(rec)
    out = pd.DataFrame(enriched)
    # Keep column presence stable even if no scored rows.
    for col, default in (
        ("k_dist_mean", pd.NA),
        ("k_dist_sd", pd.NA),
        ("k_p10", pd.NA),
        ("k_p50", pd.NA),
        ("k_p90", pd.NA),
        ("k_p_ge_8", pd.NA),
        ("k_p_ge_9", pd.NA),
        ("k_p_ge_10", pd.NA),
        ("k_p_over", pd.NA),
        ("k_p_under", pd.NA),
        ("k_dist_n_pa", pd.NA),
        ("k_dist_shape", ""),
        ("k_rate_pct", pd.NA),
        ("k_volume_bf", pd.NA),
        ("expected_ks_rate_x_bf", pd.NA),
        ("k_volume_share_note", ""),
        ("book_model_note", ""),
    ):
        if col not in out.columns:
            out[col] = default
    return out
