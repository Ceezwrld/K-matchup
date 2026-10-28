"""Grade every saved rankings-YYYY-MM-DD.csv against actual strikeouts.

Writes:
  graded-history.csv   one row per scored starter with actual K / BF / IP
  k-calibration.json   mu = a + b * expected_ks, negative-binomial size r
                       (read by k_probs.py for the K-line ladder)

Prints a calibration table plus results by ticket outlook so the tags can be
checked against real outcomes.

Usage (repo root):
  python3 mlb-k-matchups/grade_history.py
  python3 mlb-k-matchups/grade_history.py --since 2026-09-01
"""

from __future__ import annotations

import argparse
import glob
import json
import math
from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd
import requests

ROOT = Path(__file__).resolve().parent.parent
GAMELOG_URL = (
    "https://statsapi.mlb.com/api/v1/people?personIds={ids}"
    "&hydrate=stats(group=[pitching],type=[gameLog],season={year},gameType=[{gt}])"
)
GAME_TYPES = ("R", "F", "D", "L", "W")  # regular + every postseason round


def load_rankings(since: str | None) -> pd.DataFrame:
    frames = []
    for f in sorted(glob.glob(str(ROOT / "rankings-*.csv"))):
        d = Path(f).name[len("rankings-") : len("rankings-") + 10]
        if since and d < since:
            continue
        df = pd.read_csv(f)
        df["date"] = d
        frames.append(df)
    if not frames:
        raise SystemExit("No rankings-*.csv files found")
    out = pd.concat(frames, ignore_index=True)
    out = out[out["status"].eq("ok") & out["expected_ks"].notna()]
    out = out[out["date"] < date.today().isoformat()]  # only finished slates
    return out


def fetch_starts(pitcher_ids: list[int], years: set[int]) -> pd.DataFrame:
    rows = []
    for year in sorted(years):
        for gt in GAME_TYPES:
            for i in range(0, len(pitcher_ids), 40):
                ids = ",".join(str(x) for x in pitcher_ids[i : i + 40])
                url = GAMELOG_URL.format(ids=ids, year=year, gt=gt)
                data = requests.get(url, timeout=60).json()
                for p in data.get("people", []):
                    for st in p.get("stats", []):
                        for s in st.get("splits", []):
                            stat = s.get("stat", {})
                            if int(stat.get("gamesStarted") or 0) < 1:
                                continue
                            rows.append(
                                {
                                    "pitcher_id": int(p["id"]),
                                    "date": s.get("date"),
                                    "actual_ks": stat.get("strikeOuts"),
                                    "actual_bf": stat.get("battersFaced"),
                                    "actual_ip": stat.get("inningsPitched"),
                                }
                            )
    df = pd.DataFrame(rows)
    if df.empty:
        return df
    # Doubleheaders: keep the first start of the day.
    return df.drop_duplicates(["pitcher_id", "date"], keep="first")


def _nb_loglik(y: np.ndarray, mu: np.ndarray, r: float) -> float:
    lg = np.vectorize(math.lgamma)
    return float(
        np.sum(
            lg(y + r)
            - lg(r)
            - lg(y + 1)
            + r * np.log(r / (r + mu))
            + y * np.log(mu / (r + mu))
        )
    )


def fit_calibration(g: pd.DataFrame) -> dict:
    e = g["expected_ks"].to_numpy(float)
    y = g["actual_ks"].to_numpy(float)
    b, a = np.polyfit(e, y, 1)
    mu = np.clip(a + b * e, 0.3, None)
    grid = [5, 8, 12, 16, 20, 25, 30, 37, 45, 55, 70, 90, 120, 200]
    best_r = max(grid, key=lambda r: _nb_loglik(y, mu, r))
    return {
        "a": round(float(a), 3),
        "b": round(float(b), 3),
        "r": float(best_r),
        "n": int(len(g)),
        "fit_through": str(g["date"].max()),
        "fit_from": str(g["date"].min()),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("--since", help="Only grade slates on/after YYYY-MM-DD")
    ap.add_argument("--no-write", action="store_true", help="Print only")
    args = ap.parse_args()

    preds = load_rankings(args.since)
    ids = sorted(preds["pitcher_id"].dropna().astype(int).unique().tolist())
    years = {int(d[:4]) for d in preds["date"]}
    starts = fetch_starts(ids, years)
    g = preds.merge(starts, on=["pitcher_id", "date"], how="inner")
    g = g[g["actual_ks"].notna()].copy()
    g["actual_ks"] = g["actual_ks"].astype(int)
    g["err"] = g["actual_ks"] - g["expected_ks"]
    print(f"Graded {len(g)} of {len(preds)} scored starts ({g['date'].min()} → {g['date'].max()})")
    print(
        f"  mean Exp K {g['expected_ks'].mean():.2f} · mean actual {g['actual_ks'].mean():.2f} · "
        f"MAE {g['err'].abs().mean():.2f}"
    )

    g["bucket"] = pd.cut(g["expected_ks"], [0, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 20])
    print("\nCalibration by Exp K bucket")
    print(
        g.groupby("bucket", observed=True)
        .agg(n=("actual_ks", "size"), exp_k=("expected_ks", "mean"), actual=("actual_ks", "mean"))
        .round(2)
        .to_string()
    )
    if "ticket_outlook" in g.columns:
        t = g.copy()
        t["ticket_outlook"] = t["ticket_outlook"].fillna("(none)")
        print("\nBy ticket outlook")
        print(
            t.groupby("ticket_outlook")
            .agg(n=("actual_ks", "size"), exp_k=("expected_ks", "mean"), actual=("actual_ks", "mean"))
            .round(2)
            .to_string()
        )
    if "arsenal_abs_grade" in g.columns:
        print("\nBy solo arsenal grade")
        print(
            g.groupby(g["arsenal_abs_grade"].fillna("(none)"))
            .agg(n=("actual_ks", "size"), exp_k=("expected_ks", "mean"), actual=("actual_ks", "mean"))
            .round(2)
            .to_string()
        )

    cal = fit_calibration(g)
    print(f"\nCalibration: mu = {cal['a']} + {cal['b']} × Exp K, NB r = {cal['r']}")

    if not args.no_write:
        keep = [
            c
            for c in [
                "date", "pitcher", "pitcher_id", "pitcher_team", "opponent", "game",
                "expected_ks", "expected_k_pct", "projected_ip", "arsenal_abs_grade",
                "pitcher_style", "ticket_outlook", "actual_ks", "actual_bf", "actual_ip", "err",
            ]
            if c in g.columns
        ]
        g[keep].to_csv(ROOT / "graded-history.csv", index=False)
        (ROOT / "k-calibration.json").write_text(json.dumps(cal, indent=2) + "\n", encoding="utf-8")
        print(f"Wrote {ROOT / 'graded-history.csv'} and {ROOT / 'k-calibration.json'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
