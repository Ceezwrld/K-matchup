"""Fit + backtest the Hits / H+R+RBI / RBI probabilities on saved boards.

For every rankings-YYYY-MM-DD.csv, each opposing lineup batter (slot = order in
``lineup_batter_ids``) is scored with season-to-date stats as of that morning,
then graded against his box score. Writes ``hits-calibration.json`` (read by
hit_probs.py) and ``graded-hits-history.csv``; prints a hold-out test
(fit before --split, test on/after) and reliability tables.

Usage (repo root):
  python3 mlb-k-matchups/grade_hits.py
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

from hit_probs import (
    DEFAULT_CAL,
    HIT_LINES,
    HRR_LINES,
    K_BAT_RR,
    LEAGUE_R_PA,
    LEAGUE_RBI_PA,
    RBI_LINES,
    _shrink,
    batter_prop_probs,
    fetch_gamelogs,
)

ROOT = Path(__file__).resolve().parent.parent


def load_lineups() -> pd.DataFrame:
    rows = []
    today = date.today().isoformat()
    for f in sorted(glob.glob(str(ROOT / "rankings-*.csv"))):
        d = Path(f).name[len("rankings-") : len("rankings-") + 10]
        if d >= today:
            continue
        df = pd.read_csv(f)
        if "lineup_batter_ids" not in df.columns:
            continue
        for _, r in df[df["status"].eq("ok")].iterrows():
            ids = str(r.get("lineup_batter_ids") or "")
            if not ids or ids == "nan":
                continue
            for slot, bid in enumerate(ids.split(","), start=1):
                if slot > 9 or not bid.strip():
                    continue
                rows.append(
                    {
                        "date": d,
                        "pitcher_id": int(r["pitcher_id"]),
                        "projected_bf": float(r.get("projected_bf") or 22),
                        "lineup_source": str(r.get("lineup_source") or ""),
                        "batter_id": int(float(bid)),
                        "slot": slot,
                    }
                )
    return pd.DataFrame(rows)


def build_dataset(lu: pd.DataFrame) -> pd.DataFrame:
    year = int(lu["date"].min()[:4])
    bat_logs = fetch_gamelogs(lu["batter_id"].unique(), year, "hitting")
    pit_logs = fetch_gamelogs(lu["pitcher_id"].unique(), year, "pitching")
    # Actual: first game of the day.
    actual = bat_logs.drop_duplicates(["player_id", "date"], keep="first").rename(
        columns={"player_id": "batter_id", "pa": "act_pa", "h": "act_h", "r": "act_r", "rbi": "act_rbi", "hr": "act_hr"}
    )[["batter_id", "date", "act_pa", "act_h", "act_r", "act_rbi", "act_hr"]]
    df = lu.merge(actual, on=["batter_id", "date"], how="inner")
    df = df[df["act_pa"] > 0].copy()

    # Season-to-date totals (strictly before the slate date) via cumulative sums.
    def cum(logs: pd.DataFrame) -> pd.DataFrame:
        g = logs.groupby(["player_id", "date"])[["pa", "h", "r", "rbi", "hr"]].sum().reset_index()
        g = g.sort_values(["player_id", "date"])
        for c in ("pa", "h", "r", "rbi", "hr"):
            g[f"cum_{c}"] = g.groupby("player_id")[c].cumsum() - g[c]
        return g

    bc = cum(bat_logs)
    pc = cum(pit_logs)
    df = df.sort_values("date")
    bc = bc.sort_values("date")
    pc = pc.sort_values("date")
    # Batter's to-date = cumulative before his game that day (he played that day).
    df = df.merge(
        bc[["player_id", "date", "cum_pa", "cum_h", "cum_r", "cum_rbi"]].rename(
            columns={"player_id": "batter_id", "cum_pa": "b_pa", "cum_h": "b_h", "cum_r": "b_r", "cum_rbi": "b_rbi"}
        ),
        on=["batter_id", "date"],
        how="left",
    )
    # Pitcher's to-date: last cumulative row on/before the date (asof).
    pc = pc.assign(p_pa=pc["cum_pa"] + pc["pa"], p_h=pc["cum_h"] + pc["h"])
    df["date_dt"] = pd.to_datetime(df["date"])
    pc["date_dt"] = pd.to_datetime(pc["date"])
    pc_shift = pc[["player_id", "date_dt", "p_pa", "p_h"]].rename(columns={"player_id": "pitcher_id"})
    pc_shift["date_dt"] = pc_shift["date_dt"] + pd.Timedelta(days=1)  # totals usable from next day
    df = pd.merge_asof(
        df.sort_values("date_dt"),
        pc_shift.sort_values("date_dt"),
        on="date_dt",
        by="pitcher_id",
        direction="backward",
    )
    return df.fillna({"b_pa": 0, "b_h": 0, "b_r": 0, "b_rbi": 0, "p_pa": 0, "p_h": 0})


def slot_pa_dist(df: pd.DataFrame) -> dict:
    off = df[df["lineup_source"].eq("official")]
    out = {}
    for s, g in off.groupby("slot"):
        vc = g["act_pa"].clip(1, 7).value_counts(normalize=True).sort_index()
        out[int(s)] = {int(k): round(float(v), 4) for k, v in vc.items()}
    return out


def score(df: pd.DataFrame, cal: dict) -> pd.DataFrame:
    recs = []
    for r in df.itertuples(index=False):
        p = batter_prop_probs(
            slot=int(r.slot),
            bat={"pa": r.b_pa, "h": r.b_h, "r": r.b_r, "rbi": r.b_rbi},
            pit={"pa": r.p_pa, "h": r.p_h},
            starter_bf=float(r.projected_bf),
            cal=cal,
        )
        p["rr_pa"] = _shrink(r.b_r, r.b_pa, LEAGUE_R_PA, K_BAT_RR) + _shrink(r.b_rbi, r.b_pa, LEAGUE_RBI_PA, K_BAT_RR)
        p["rbi_pa"] = _shrink(r.b_rbi, r.b_pa, LEAGUE_RBI_PA, K_BAT_RR)
        recs.append(p)
    return pd.concat([df.reset_index(drop=True), pd.DataFrame(recs)], axis=1)


def _nb_ll(y, mu, r):
    lg = np.vectorize(math.lgamma)
    return float(np.sum(lg(y + r) - lg(r) - lg(y + 1) + r * np.log(r / (r + mu)) + y * np.log(mu / (r + mu))))


def fit(train: pd.DataFrame, slot_pa: dict) -> dict:
    cal = json.loads(json.dumps(DEFAULT_CAL))
    cal["slot_pa"] = slot_pa
    s0 = score(train, cal)
    cal["hit_scale"] = round(float(train["act_h"].sum() / s0["exp_hits"].sum()), 4)
    s1 = score(train, cal)
    grid = [1.5, 2, 3, 4, 6, 8, 12, 20, 40, 100]
    # H+R+RBI mean: a + b_h * E[H] + b_rr * E[PA] * (R+RBI)/PA
    y = (train["act_h"] + train["act_r"] + train["act_rbi"]).to_numpy(float)
    X = np.column_stack([np.ones(len(s1)), s1["exp_hits"], s1["exp_pa"] * s1["rr_pa"]])
    a, bh, brr = np.linalg.lstsq(X, y, rcond=None)[0]
    mu = np.clip(X @ np.array([a, bh, brr]), 0.05, None)
    r_hrr = max(grid, key=lambda r: _nb_ll(y, mu, r))
    cal["hrr"] = {"a": round(float(a), 4), "b_h": round(float(bh), 4), "b_rr": round(float(brr), 4), "r": r_hrr}
    y2 = train["act_rbi"].to_numpy(float)
    X2 = np.column_stack([np.ones(len(s1)), s1["exp_pa"] * s1["rbi_pa"]])
    a2, b2 = np.linalg.lstsq(X2, y2, rcond=None)[0]
    mu2 = np.clip(X2 @ np.array([a2, b2]), 0.02, None)
    r_rbi = max(grid, key=lambda r: _nb_ll(y2, mu2, r))
    cal["rbi"] = {"a": round(float(a2), 4), "b": round(float(b2), 4), "r": r_rbi}
    # Per-line logistic calibration on log(mean).
    cal["hrr_lines"] = {str(n): _logit_fit(np.log(mu), (y >= n).astype(float)) for n in HRR_LINES}
    cal["rbi_lines"] = {str(n): _logit_fit(np.log(mu2), (y2 >= n).astype(float)) for n in RBI_LINES}
    return cal


def _logit_fit(x: np.ndarray, y: np.ndarray, iters: int = 30) -> list[float]:
    """Two-parameter logistic regression (Newton)."""
    X = np.column_stack([np.ones(len(x)), x])
    w = np.zeros(2)
    for _ in range(iters):
        p = 1 / (1 + np.exp(-(X @ w)))
        g = X.T @ (y - p)
        H = (X * (p * (1 - p))[:, None]).T @ X + 1e-6 * np.eye(2)
        step = np.linalg.solve(H, g)
        w += step
        if np.abs(step).max() < 1e-8:
            break
    return [round(float(w[0]), 4), round(float(w[1]), 4)]


def report(s: pd.DataFrame, label: str) -> None:
    hrr = s["act_h"] + s["act_r"] + s["act_rbi"]
    print(f"\n{label}: {len(s)} batter-games")
    checks = [(f"p_h{n}", s["act_h"] >= n, f"Hits {n}+") for n in HIT_LINES]
    checks += [(f"p_hrr{n}", hrr >= n, f"H+R+RBI {n}+") for n in HRR_LINES]
    checks += [(f"p_rbi{n}", s["act_rbi"] >= n, f"RBI {n}+") for n in RBI_LINES]
    for col, hit, name in checks:
        p = s[col].to_numpy(float)
        h = hit.to_numpy(float)
        base = h.mean()
        brier = np.mean((p - h) ** 2)
        brier0 = np.mean((base - h) ** 2)
        skill = 1 - brier / brier0
        bins = pd.cut(p, [0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 1.0])
        t = pd.DataFrame({"pred": p, "act": h, "bin": bins}).groupby("bin", observed=True).agg(
            n=("act", "size"), pred=("pred", "mean"), act=("act", "mean")
        )
        t = t[t["n"] >= 30]
        rel = " ".join(f"{r.pred:.2f}→{r.act:.2f}(n{int(r.n)})" for r in t.itertuples())
        print(f"  {name:12s} pred {p.mean():.3f} act {base:.3f} · Brier skill {100 * skill:+.1f}% · {rel}")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--split", default="2026-09-01", help="Hold-out test starts here")
    ap.add_argument("--no-write", action="store_true")
    args = ap.parse_args()
    lu = load_lineups()
    df = build_dataset(lu)
    print(f"{len(df)} graded batter-games ({df['date'].min()} → {df['date'].max()})")
    slot_pa = slot_pa_dist(df)
    tr = df[df["date"] < args.split]
    te = df[df["date"] >= args.split]
    cal_tr = fit(tr, slot_pa)
    report(score(te, cal_tr), f"HOLD-OUT test (fit < {args.split}, test ≥ {args.split})")
    cal = fit(df, slot_pa)
    cal["n"] = int(len(df))
    cal["fit_from"] = str(df["date"].min())
    cal["fit_through"] = str(df["date"].max())
    full = score(df, cal)
    report(full, "In-sample (final fit, all slates)")
    print("\nCalibration:", json.dumps({k: v for k, v in cal.items() if k != "slot_pa"}))
    if not args.no_write:
        (ROOT / "hits-calibration.json").write_text(json.dumps(cal, indent=2) + "\n", encoding="utf-8")
        keep = ["date", "batter_id", "pitcher_id", "slot", "lineup_source", "act_pa", "act_h", "act_r",
                "act_rbi", "act_hr", "exp_hits", "p_h1", "p_h2", "exp_hrr", "p_hrr1", "p_hrr2", "p_hrr3", "p_rbi1"]
        full[keep].to_csv(ROOT / "graded-hits-history.csv", index=False)
        print(f"Wrote {ROOT / 'hits-calibration.json'} and graded-hits-history.csv")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
