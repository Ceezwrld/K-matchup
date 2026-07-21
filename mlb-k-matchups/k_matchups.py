#!/usr/bin/env python3
"""Rank MLB starters by opposing-team strikeout vulnerability to their pitch arsenal."""

from __future__ import annotations

import argparse
import sys
from datetime import date, datetime
from typing import Any

import pandas as pd
import requests

SAVANT_URL = (
    "https://baseballsavant.mlb.com/leaderboard/pitch-arsenal-stats"
    "?type={kind}&year={year}&min={min_pa}&csv=true"
)
SCHEDULE_URL = (
    "https://statsapi.mlb.com/api/v1/schedule"
    "?sportId=1&date={date}&hydrate=probablePitcher,team"
)

USER_AGENT = (
    "mlb-k-matchups/1.0 (+https://github.com; research; "
    "contact: local-cli)"
)

# Normalize common MLB abbreviations to Baseball Savant / Stats API forms.
TEAM_ALIASES = {
    "OAK": "ATH",
    "ATH": "ATH",
    "ARI": "AZ",
    "AZ": "AZ",
    "CHW": "CWS",
    "CWS": "CWS",
    "WAS": "WSH",
    "WSH": "WSH",
    "TBR": "TB",
    "TBD": "TB",
    "TB": "TB",
    "KCR": "KC",
    "KC": "KC",
    "SDP": "SD",
    "SD": "SD",
    "SFG": "SF",
    "SF": "SF",
    "ANA": "LAA",
    "LAA": "LAA",
    "FLA": "MIA",
    "MIA": "MIA",
    "NY": "NYY",  # ambiguous; prefer explicit NYY/NYM in inputs
}


def log(verbose: bool, msg: str) -> None:
    if verbose:
        print(msg, file=sys.stderr)


def normalize_team(abbrev: str | None) -> str | None:
    if abbrev is None or (isinstance(abbrev, float) and pd.isna(abbrev)):
        return None
    key = str(abbrev).strip().upper()
    if not key:
        return None
    return TEAM_ALIASES.get(key, key)


def fetch_csv(url: str, verbose: bool = False) -> pd.DataFrame:
    log(verbose, f"GET {url}")
    resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=60)
    resp.raise_for_status()
    # Savant CSVs may include a UTF-8 BOM.
    text = resp.content.decode("utf-8-sig")
    from io import StringIO

    df = pd.read_csv(StringIO(text))
    return df


def fetch_json(url: str, verbose: bool = False) -> dict[str, Any]:
    log(verbose, f"GET {url}")
    resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=60)
    resp.raise_for_status()
    return resp.json()


def load_pitcher_arsenal(year: int, min_pa: int, verbose: bool) -> pd.DataFrame:
    url = SAVANT_URL.format(kind="pitcher", year=year, min_pa=min_pa)
    df = fetch_csv(url, verbose)
    df["player_id"] = pd.to_numeric(df["player_id"], errors="coerce").astype("Int64")
    df["pitch_usage"] = pd.to_numeric(df["pitch_usage"], errors="coerce")
    df["pitches"] = pd.to_numeric(df["pitches"], errors="coerce")
    df["team_name_alt"] = df["team_name_alt"].map(normalize_team)
    df["name_last_first"] = df["last_name, first_name"].astype(str).str.strip()
    return df


def load_team_batter_rates(
    year: int, min_pa: int, verbose: bool
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Return (team_rates, league_rates) indexed by pitch_type.

    team_rates columns: team, pitch_type, k_pct, whiff_pct, pa
    league_rates columns: pitch_type, k_pct, whiff_pct, pa
    Both K%/whiff are PA-weighted averages across batters.
    """
    url = SAVANT_URL.format(kind="batter", year=year, min_pa=min_pa)
    df = fetch_csv(url, verbose)
    df["pa"] = pd.to_numeric(df["pa"], errors="coerce")
    df["k_percent"] = pd.to_numeric(df["k_percent"], errors="coerce")
    df["whiff_percent"] = pd.to_numeric(df["whiff_percent"], errors="coerce")
    df["team"] = df["team_name_alt"].map(normalize_team)
    df = df.dropna(subset=["team", "pitch_type", "pa", "k_percent"])
    df = df[df["pa"] > 0]

    df = df.copy()
    df["k_pa"] = df["k_percent"] * df["pa"]
    df["whiff_pa"] = df["whiff_percent"] * df["pa"]

    def agg_rates(frame: pd.DataFrame, keys: list[str]) -> pd.DataFrame:
        g = frame.groupby(keys, as_index=False)[["k_pa", "whiff_pa", "pa"]].sum()
        g["k_pct"] = g["k_pa"] / g["pa"]
        g["whiff_pct"] = g["whiff_pa"] / g["pa"]
        return g.drop(columns=["k_pa", "whiff_pa"])

    team_rates = agg_rates(df, ["team", "pitch_type"])
    league_rates = agg_rates(df, ["pitch_type"])
    return team_rates, league_rates


def parse_name_variants(name: str) -> set[str]:
    """Return normalized name keys for matching First Last / Last, First."""
    raw = " ".join(str(name).strip().split())
    if not raw:
        return set()
    keys = {raw.lower()}
    if "," in raw:
        last, first = [p.strip() for p in raw.split(",", 1)]
        if first and last:
            keys.add(f"{first} {last}".lower())
            keys.add(f"{last}, {first}".lower())
    else:
        parts = raw.split()
        if len(parts) >= 2:
            first, last = parts[0], " ".join(parts[1:])
            keys.add(f"{last}, {first}".lower())
            keys.add(f"{first} {last}".lower())
    return keys


def build_pitcher_indexes(arsenal: pd.DataFrame) -> tuple[dict[int, str], dict[str, int]]:
    """Map player_id -> display name and name_key -> player_id."""
    id_to_name: dict[int, str] = {}
    name_to_id: dict[str, int] = {}
    for _, row in arsenal.drop_duplicates("player_id").iterrows():
        pid = int(row["player_id"])
        last_first = str(row["name_last_first"])
        # Display as First Last
        if "," in last_first:
            last, first = [p.strip() for p in last_first.split(",", 1)]
            display = f"{first} {last}".strip()
        else:
            display = last_first
        id_to_name[pid] = display
        for key in parse_name_variants(last_first) | parse_name_variants(display):
            name_to_id.setdefault(key, pid)
    return id_to_name, name_to_id


def resolve_pitcher(
    pitcher: str | None,
    pitcher_id: Any,
    id_to_name: dict[int, str],
    name_to_id: dict[str, int],
) -> tuple[int | None, str | None, str]:
    """Resolve to (player_id, display_name, status). status ok|missing_arsenal|unresolved."""
    pid: int | None = None
    if pitcher_id is not None and not (isinstance(pitcher_id, float) and pd.isna(pitcher_id)):
        try:
            pid = int(float(str(pitcher_id).strip()))
        except (TypeError, ValueError):
            pid = None

    if pid is not None:
        if pid in id_to_name:
            return pid, id_to_name[pid], "ok"
        # Known id but no arsenal rows (e.g. rookies below min PA).
        display = None
        if pitcher:
            display = str(pitcher).strip() or None
        return pid, display, "missing_arsenal"

    if pitcher:
        for key in parse_name_variants(pitcher):
            if key in name_to_id:
                found = name_to_id[key]
                return found, id_to_name[found], "ok"
        return None, str(pitcher).strip(), "unresolved"

    return None, None, "unresolved"


def fetch_probable_matchups(game_date: str, verbose: bool) -> pd.DataFrame:
    payload = fetch_json(SCHEDULE_URL.format(date=game_date), verbose)
    rows: list[dict[str, Any]] = []
    for day in payload.get("dates", []):
        for game in day.get("games", []):
            home = game.get("teams", {}).get("home", {})
            away = game.get("teams", {}).get("away", {})
            home_team = normalize_team(home.get("team", {}).get("abbreviation"))
            away_team = normalize_team(away.get("team", {}).get("abbreviation"))
            game_label = f"{away_team}@{home_team}"
            for side, opp_team in ((home, away_team), (away, home_team)):
                pp = side.get("probablePitcher") or {}
                if not pp:
                    continue
                team_abbr = normalize_team(side.get("team", {}).get("abbreviation"))
                rows.append(
                    {
                        "pitcher": pp.get("fullName"),
                        "pitcher_id": pp.get("id"),
                        "pitcher_team": team_abbr,
                        "opponent": opp_team,
                        "game": game_label,
                    }
                )
    return pd.DataFrame(rows)


def load_matchups_csv(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df = df.rename(columns={c: c.strip().lower() for c in df.columns})
    required = {"pitcher", "opponent"}
    missing = required - set(df.columns)
    if missing:
        raise SystemExit(f"--matchups CSV missing columns: {sorted(missing)}")
    if "pitcher_id" not in df.columns:
        df["pitcher_id"] = pd.NA
    if "pitcher_team" not in df.columns:
        df["pitcher_team"] = pd.NA
    if "game" not in df.columns:
        df["game"] = pd.NA
    df["opponent"] = df["opponent"].map(normalize_team)
    df["pitcher_team"] = df["pitcher_team"].map(normalize_team)
    return df[["pitcher", "opponent", "pitcher_id", "pitcher_team", "game"]]


def pitcher_usage_weights(
    arsenal: pd.DataFrame, player_id: int, min_usage: float
) -> pd.DataFrame | None:
    """Return pitch_type / usage_frac rows summing to 1.0, or None if missing."""
    subset = arsenal[arsenal["player_id"] == player_id].copy()
    if subset.empty:
        return None
    subset = subset[subset["pitch_usage"].fillna(0) >= min_usage]
    if subset.empty:
        return None
    total = subset["pitch_usage"].sum()
    if total <= 0:
        return None
    subset["usage_frac"] = subset["pitch_usage"] / total
    return subset[["pitch_type", "usage_frac", "pitch_usage"]]


def score_matchup(
    usage: pd.DataFrame,
    opponent: str,
    team_rates: pd.DataFrame,
    league_rates: pd.DataFrame,
) -> dict[str, float]:
    """Compute expected K%/whiff and vs-league deltas for one arsenal."""
    team = team_rates[team_rates["team"] == opponent].set_index("pitch_type")
    league = league_rates.set_index("pitch_type")

    exp_k = 0.0
    exp_whiff = 0.0
    lg_k = 0.0
    lg_whiff = 0.0
    covered = 0.0

    for _, row in usage.iterrows():
        pt = row["pitch_type"]
        w = float(row["usage_frac"])
        if pt in team.index:
            k = float(team.loc[pt, "k_pct"])
            wh = float(team.loc[pt, "whiff_pct"])
        elif pt in league.index:
            # Fall back to league average when team lacks sample vs this pitch.
            k = float(league.loc[pt, "k_pct"])
            wh = float(league.loc[pt, "whiff_pct"])
        else:
            continue
        if pt in league.index:
            lk = float(league.loc[pt, "k_pct"])
            lw = float(league.loc[pt, "whiff_pct"])
        else:
            lk, lw = k, wh

        exp_k += w * k
        exp_whiff += w * wh
        lg_k += w * lk
        lg_whiff += w * lw
        covered += w

    if covered <= 0:
        return {
            "expected_k_pct": float("nan"),
            "expected_whiff_pct": float("nan"),
            "vs_league_k": float("nan"),
            "vs_league_whiff": float("nan"),
            "usage_covered": 0.0,
        }

    # Re-normalize if some pitch types had no rates at all.
    if covered < 0.999:
        exp_k /= covered
        exp_whiff /= covered
        lg_k /= covered
        lg_whiff /= covered

    return {
        "expected_k_pct": exp_k,
        "expected_whiff_pct": exp_whiff,
        "vs_league_k": exp_k - lg_k,
        "vs_league_whiff": exp_whiff - lg_whiff,
        "usage_covered": covered,
    }


def format_table(df: pd.DataFrame) -> str:
    show = df.copy()
    for col in ("expected_k_pct", "expected_whiff_pct", "vs_league_k", "vs_league_whiff"):
        if col in show.columns:
            show[col] = show[col].map(
                lambda x: "" if pd.isna(x) else f"{x:.2f}"
            )
    if "rank" in show.columns:
        show["rank"] = show["rank"].map(lambda x: "" if pd.isna(x) else int(x))
    cols = [
        c
        for c in [
            "rank",
            "pitcher",
            "pitcher_team",
            "opponent",
            "game",
            "expected_k_pct",
            "vs_league_k",
            "expected_whiff_pct",
            "vs_league_whiff",
            "status",
        ]
        if c in show.columns
    ]
    return show[cols].to_string(index=False)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    today = date.today().isoformat()
    p = argparse.ArgumentParser(
        description=(
            "Rank starting pitchers by how vulnerable the opposing lineup is "
            "to strikeouts against that starter's pitch mix."
        )
    )
    src = p.add_mutually_exclusive_group()
    src.add_argument(
        "--date",
        default=None,
        help=f"Score probable starters for this date (YYYY-MM-DD). Default: {today}",
    )
    src.add_argument(
        "--matchups",
        metavar="PATH",
        help="CSV of matchups: pitcher,opponent[,pitcher_id,pitcher_team,game]",
    )
    p.add_argument(
        "--year",
        type=int,
        default=None,
        help="Savant season year (default: year of --date, else current year)",
    )
    p.add_argument(
        "--min-pa",
        type=int,
        default=50,
        help="Minimum PA filter for Savant arsenal leaderboards (default: 50)",
    )
    p.add_argument(
        "--min-usage",
        type=float,
        default=5.0,
        help="Ignore pitcher pitches below this usage %% (default: 5)",
    )
    p.add_argument(
        "-o",
        "--output",
        metavar="PATH",
        help="Write full rankings CSV to this path",
    )
    p.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Log data fetches to stderr",
    )
    return p.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    if args.matchups:
        matchups = load_matchups_csv(args.matchups)
        ref_year = date.today().year
    else:
        game_date = args.date or date.today().isoformat()
        try:
            datetime.strptime(game_date, "%Y-%m-%d")
        except ValueError:
            raise SystemExit(f"Invalid --date: {game_date!r} (expected YYYY-MM-DD)")
        matchups = fetch_probable_matchups(game_date, args.verbose)
        ref_year = int(game_date[:4])
        if matchups.empty:
            print(f"No probable pitchers found for {game_date}.", file=sys.stderr)
            return 1

    year = args.year or ref_year
    log(args.verbose, f"Using Savant year={year}, min_pa={args.min_pa}, min_usage={args.min_usage}")

    arsenal = load_pitcher_arsenal(year, args.min_pa, args.verbose)
    team_rates, league_rates = load_team_batter_rates(year, args.min_pa, args.verbose)
    id_to_name, name_to_id = build_pitcher_indexes(arsenal)

    results: list[dict[str, Any]] = []
    for _, m in matchups.iterrows():
        pid, display, status = resolve_pitcher(
            m.get("pitcher"),
            m.get("pitcher_id"),
            id_to_name,
            name_to_id,
        )
        opponent = normalize_team(m.get("opponent"))
        row: dict[str, Any] = {
            "pitcher": display or m.get("pitcher"),
            "pitcher_id": pid if pid is not None else m.get("pitcher_id"),
            "pitcher_team": normalize_team(m.get("pitcher_team")),
            "opponent": opponent,
            "game": m.get("game"),
            "status": status,
            "expected_k_pct": float("nan"),
            "expected_whiff_pct": float("nan"),
            "vs_league_k": float("nan"),
            "vs_league_whiff": float("nan"),
            "usage_covered": float("nan"),
        }

        if status == "ok" and pid is not None and opponent:
            usage = pitcher_usage_weights(arsenal, pid, args.min_usage)
            if usage is None:
                row["status"] = "missing_arsenal"
            else:
                scores = score_matchup(usage, opponent, team_rates, league_rates)
                row.update(scores)
                if pd.isna(row["expected_k_pct"]):
                    row["status"] = "insufficient_rates"
                else:
                    row["status"] = "ok"
        elif status == "ok" and not opponent:
            row["status"] = "missing_opponent"

        results.append(row)

    out = pd.DataFrame(results)
    # Rank scored rows by vs_league_k descending; unscored rows sink to the bottom.
    out = out.sort_values(
        by=["vs_league_k"],
        ascending=False,
        na_position="last",
        kind="mergesort",
    ).reset_index(drop=True)
    ranks: list[Any] = []
    rank_i = 1
    for _, r in out.iterrows():
        if r["status"] == "ok" and pd.notna(r["vs_league_k"]):
            ranks.append(rank_i)
            rank_i += 1
        else:
            ranks.append(pd.NA)
    out.insert(0, "rank", ranks)

    print(format_table(out))
    if args.output:
        out.to_csv(args.output, index=False)
        log(True, f"Wrote {args.output}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
