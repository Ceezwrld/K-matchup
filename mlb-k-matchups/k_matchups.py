#!/usr/bin/env python3
"""Rank MLB starters by expected strikeouts vs the opposing starting lineup."""

from __future__ import annotations

import argparse
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rankings_html import write_interactive_html  # noqa: E402

SAVANT_URL = (
    "https://baseballsavant.mlb.com/leaderboard/pitch-arsenal-stats"
    "?type={kind}&year={year}&min={min_pa}&csv=true"
)
SCHEDULE_URL = (
    "https://statsapi.mlb.com/api/v1/schedule"
    "?sportId=1&date={date}&hydrate=probablePitcher,team,lineups"
)
SCHEDULE_RANGE_URL = (
    "https://statsapi.mlb.com/api/v1/schedule"
    "?sportId=1&startDate={start}&endDate={end}&hydrate=lineups,team"
)
PEOPLE_STATS_URL = (
    "https://statsapi.mlb.com/api/v1/people"
    "?personIds={ids}"
    "&hydrate=stats(group=[pitching],type=[season],season={year})"
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

DEFAULT_BATTERS_FACED = 22
DEFAULT_PROJECTED_IP = 5.5
DEFAULT_BF_PER_IP = 4.25
MIN_GS_RELIABLE = 5
MAX_PROJECTED_IP = 7.0
MAX_PROJECTED_BF = 30


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


def parse_innings_pitched(value: Any) -> float | None:
    """Parse MLB Stats API inningsPitched strings like '93.2' (.1=1/3, .2=2/3)."""
    if value is None or (isinstance(value, float) and pd.isna(value)):
        return None
    text = str(value).strip()
    if not text:
        return None
    try:
        if "." in text:
            whole, frac = text.split(".", 1)
            return int(whole) + (int(frac) / 3.0)
        return float(text)
    except (TypeError, ValueError):
        return None


def fetch_pitcher_season_outings(
    player_ids: list[int], year: int, verbose: bool
) -> dict[int, dict[str, float]]:
    """Season pitching totals keyed by player_id: ip, gs, bf, so."""
    ids = sorted({int(pid) for pid in player_ids if pid is not None})
    out: dict[int, dict[str, float]] = {}
    # Stats API accepts comma-separated personIds; keep chunks modest.
    for i in range(0, len(ids), 40):
        chunk = ids[i : i + 40]
        url = PEOPLE_STATS_URL.format(
            ids=",".join(str(x) for x in chunk), year=year
        )
        payload = fetch_json(url, verbose)
        for person in payload.get("people", []):
            pid = person.get("id")
            if pid is None:
                continue
            splits: list[dict[str, Any]] = []
            for block in person.get("stats") or []:
                splits.extend(block.get("splits") or [])
            if not splits:
                continue
            stat = splits[0].get("stat") or {}
            ip = parse_innings_pitched(stat.get("inningsPitched"))
            gs = float(stat.get("gamesStarted") or 0)
            bf = float(stat.get("battersFaced") or 0)
            so = float(stat.get("strikeOuts") or 0)
            out[int(pid)] = {
                "ip": ip if ip is not None else 0.0,
                "gs": gs,
                "bf": bf,
                "so": so,
            }
    return out


def project_starter_outing(
    pitcher_id: int | None,
    season_outings: dict[int, dict[str, float]],
    *,
    ip_override: float | None = None,
    bf_override: float | None = None,
) -> dict[str, Any]:
    """Project IP, BF, and times-through-order for one starter outing.

    Preference:
      1. explicit --batters-faced / --ip overrides
      2. season averages: BF/GS and IP/GS
      3. defaults (5.5 IP × 4.25 BF/IP)
    """
    season = season_outings.get(int(pitcher_id)) if pitcher_id is not None else None
    season_ip = float(season["ip"]) if season else 0.0
    season_gs = float(season["gs"]) if season else 0.0
    season_bf = float(season["bf"]) if season else 0.0

    bf_per_ip = DEFAULT_BF_PER_IP
    if season_ip > 0 and season_bf > 0:
        bf_per_ip = season_bf / season_ip

    source = "default"
    projected_ip: float
    projected_bf: float

    if bf_override is not None:
        projected_bf = float(bf_override)
        projected_ip = (
            float(ip_override)
            if ip_override is not None
            else projected_bf / bf_per_ip
        )
        source = "override_bf"
    elif ip_override is not None:
        projected_ip = float(ip_override)
        projected_bf = projected_ip * bf_per_ip
        source = "override_ip"
    elif season_gs > 0 and season_bf > 0:
        projected_bf = season_bf / season_gs
        projected_ip = season_ip / season_gs if season_ip > 0 else projected_bf / bf_per_ip
        source = "season_avg"
    elif season_gs > 0 and season_ip > 0:
        projected_ip = season_ip / season_gs
        projected_bf = projected_ip * bf_per_ip
        source = "season_ip"
    else:
        projected_ip = DEFAULT_PROJECTED_IP
        projected_bf = projected_ip * DEFAULT_BF_PER_IP
        source = "default"

    # Shrink thin samples toward a typical starter outing, then cap extremes.
    if source.startswith("season") and season_gs < MIN_GS_RELIABLE:
        weight = season_gs / MIN_GS_RELIABLE
        projected_ip = weight * projected_ip + (1.0 - weight) * DEFAULT_PROJECTED_IP
        projected_bf = weight * projected_bf + (1.0 - weight) * (
            DEFAULT_PROJECTED_IP * DEFAULT_BF_PER_IP
        )
        source = "season_shrunk"

    if bf_override is None and ip_override is None:
        projected_ip = min(projected_ip, MAX_PROJECTED_IP)
        projected_bf = min(projected_bf, MAX_PROJECTED_BF)

    projected_bf_rounded = max(1, int(round(projected_bf)))
    times_through = projected_bf_rounded / 9.0

    return {
        "projected_ip": projected_ip,
        "projected_bf": projected_bf_rounded,
        "times_through_order": times_through,
        "outing_source": source,
        "season_ip": season_ip if season_gs else float("nan"),
        "season_gs": season_gs if season_gs else float("nan"),
        "season_bf_per_start": (season_bf / season_gs) if season_gs else float("nan"),
    }


def load_pitcher_arsenal(year: int, min_pa: int, verbose: bool) -> pd.DataFrame:
    url = SAVANT_URL.format(kind="pitcher", year=year, min_pa=min_pa)
    df = fetch_csv(url, verbose)
    df["player_id"] = pd.to_numeric(df["player_id"], errors="coerce").astype("Int64")
    df["pitch_usage"] = pd.to_numeric(df["pitch_usage"], errors="coerce")
    df["pitches"] = pd.to_numeric(df["pitches"], errors="coerce")
    df["team_name_alt"] = df["team_name_alt"].map(normalize_team)
    df["name_last_first"] = df["last_name, first_name"].astype(str).str.strip()
    return df


def load_batter_pitch_rates(year: int, min_pa: int, verbose: bool) -> pd.DataFrame:
    """Per-batter K%/whiff by pitch_type from Savant arsenal leaderboard."""
    url = SAVANT_URL.format(kind="batter", year=year, min_pa=min_pa)
    df = fetch_csv(url, verbose)
    df["player_id"] = pd.to_numeric(df["player_id"], errors="coerce").astype("Int64")
    df["pa"] = pd.to_numeric(df["pa"], errors="coerce")
    df["k_percent"] = pd.to_numeric(df["k_percent"], errors="coerce")
    df["whiff_percent"] = pd.to_numeric(df["whiff_percent"], errors="coerce")
    df["team"] = df["team_name_alt"].map(normalize_team)
    df["name_last_first"] = df["last_name, first_name"].astype(str).str.strip()
    df = df.dropna(subset=["player_id", "pitch_type", "k_percent"])
    return df[
        [
            "player_id",
            "name_last_first",
            "team",
            "pitch_type",
            "pa",
            "k_percent",
            "whiff_percent",
        ]
    ]


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


def _lineup_from_players(players: list[dict[str, Any]] | None) -> list[dict[str, Any]]:
    if not players:
        return []
    out: list[dict[str, Any]] = []
    for i, p in enumerate(players, start=1):
        pid = p.get("id")
        if pid is None:
            continue
        out.append(
            {
                "slot": i,
                "batter_id": int(pid),
                "batter": p.get("fullName") or p.get("useName") or str(pid),
            }
        )
    return out


def _team_lineups_from_game(game: dict[str, Any]) -> dict[str, list[dict[str, Any]]]:
    """Return {team_abbr: [{slot, batter_id, batter}, ...]} for a schedule game."""
    home = game.get("teams", {}).get("home", {})
    away = game.get("teams", {}).get("away", {})
    home_team = normalize_team(home.get("team", {}).get("abbreviation"))
    away_team = normalize_team(away.get("team", {}).get("abbreviation"))
    lu = game.get("lineups") or {}
    out: dict[str, list[dict[str, Any]]] = {}
    if home_team:
        home_lu = _lineup_from_players(lu.get("homePlayers"))
        if home_lu:
            out[home_team] = home_lu
    if away_team:
        away_lu = _lineup_from_players(lu.get("awayPlayers"))
        if away_lu:
            out[away_team] = away_lu
    return out


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
            game_pk = game.get("gamePk")
            posted = _team_lineups_from_game(game)
            for side, opp_team in ((home, away_team), (away, home_team)):
                pp = side.get("probablePitcher") or {}
                if not pp:
                    continue
                team_abbr = normalize_team(side.get("team", {}).get("abbreviation"))
                opp_lineup = posted.get(opp_team or "", [])
                rows.append(
                    {
                        "pitcher": pp.get("fullName"),
                        "pitcher_id": pp.get("id"),
                        "pitcher_team": team_abbr,
                        "opponent": opp_team,
                        "game": game_label,
                        "game_pk": game_pk,
                        "lineup": opp_lineup,
                        "lineup_source": "official" if opp_lineup else None,
                    }
                )
    return pd.DataFrame(rows)


def build_prior_lineups(
    before_date: str, lookback_days: int, verbose: bool
) -> dict[str, tuple[str, list[dict[str, Any]]]]:
    """Most recent starting lineup per team before before_date.

    Returns team -> (lineup_date, lineup_rows).
    """
    end = date.fromisoformat(before_date) - timedelta(days=1)
    start = end - timedelta(days=max(lookback_days, 1) - 1)
    if end < start:
        return {}
    url = SCHEDULE_RANGE_URL.format(start=start.isoformat(), end=end.isoformat())
    payload = fetch_json(url, verbose)
    # Walk newest games first so the first hit is the most recent lineup.
    dated_games: list[tuple[str, dict[str, Any]]] = []
    for day in payload.get("dates", []):
        d = day.get("date") or ""
        for game in day.get("games", []):
            dated_games.append((d, game))
    dated_games.sort(key=lambda x: x[0], reverse=True)

    found: dict[str, tuple[str, list[dict[str, Any]]]] = {}
    for d, game in dated_games:
        for team, lineup in _team_lineups_from_game(game).items():
            if team not in found and lineup:
                found[team] = (d, lineup)
    return found


def resolve_lineup(
    opponent: str | None,
    posted_lineup: list[dict[str, Any]] | None,
    posted_source: str | None,
    prior_lineups: dict[str, tuple[str, list[dict[str, Any]]]],
) -> tuple[list[dict[str, Any]], str | None]:
    if posted_lineup:
        return posted_lineup, posted_source or "official"
    if opponent and opponent in prior_lineups:
        prior_date, lineup = prior_lineups[opponent]
        return lineup, f"prior:{prior_date}"
    return [], None


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
    df["game_pk"] = pd.NA
    df["lineup"] = [[] for _ in range(len(df))]
    df["lineup_source"] = None
    return df[
        [
            "pitcher",
            "opponent",
            "pitcher_id",
            "pitcher_team",
            "game",
            "game_pk",
            "lineup",
            "lineup_source",
        ]
    ]


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


def score_batter_vs_arsenal(
    usage: pd.DataFrame, batter_rates: pd.DataFrame
) -> dict[str, float] | None:
    """Arsenal-weighted K%/whiff for one batter. None if no overlapping pitch types."""
    if batter_rates.empty:
        return None
    by_pitch = batter_rates.set_index("pitch_type")
    exp_k = 0.0
    exp_whiff = 0.0
    covered = 0.0
    for _, row in usage.iterrows():
        pt = row["pitch_type"]
        w = float(row["usage_frac"])
        if pt not in by_pitch.index:
            continue
        exp_k += w * float(by_pitch.loc[pt, "k_percent"])
        wh = by_pitch.loc[pt, "whiff_percent"]
        if pd.notna(wh):
            exp_whiff += w * float(wh)
        else:
            exp_whiff += w * float(by_pitch.loc[pt, "k_percent"])
        covered += w
    if covered <= 0:
        return None
    if covered < 0.999:
        exp_k /= covered
        exp_whiff /= covered
    return {
        "expected_k_pct": exp_k,
        "expected_whiff_pct": exp_whiff,
        "usage_covered": covered,
    }


def score_vs_lineup(
    usage: pd.DataFrame,
    lineup: list[dict[str, Any]],
    batter_df: pd.DataFrame,
    batters_faced: float,
) -> dict[str, Any]:
    """Score starter arsenal vs opposing starting nine over a full outing.

    Per batter: arsenal-weighted K%/whiff from Savant (no league fill-in).

    expected_k_pct       = mean arsenal-weighted K% across lineup batters with data
    expected_ks_1x       = known K expectation for one trip through the order
    expected_ks          = walk batting order for projected BF (innings/TTO based)
    times_through_order  = batters_faced / 9
    """
    batter_scores: list[dict[str, Any]] = []
    missing: list[str] = []

    for slot_row in lineup:
        bid = int(slot_row["batter_id"])
        name = slot_row.get("batter") or str(bid)
        rates = batter_df[batter_df["player_id"] == bid]
        scored = score_batter_vs_arsenal(usage, rates)
        if scored is None:
            missing.append(name)
            batter_scores.append(
                {
                    "slot": slot_row.get("slot"),
                    "batter_id": bid,
                    "batter": name,
                    "expected_k_pct": float("nan"),
                    "status": "missing_rates",
                }
            )
            continue
        batter_scores.append(
            {
                "slot": slot_row.get("slot"),
                "batter_id": bid,
                "batter": name,
                "expected_k_pct": scored["expected_k_pct"],
                "expected_whiff_pct": scored["expected_whiff_pct"],
                "status": "ok",
            }
        )

    ok = [b for b in batter_scores if b["status"] == "ok"]
    n_lineup = len(lineup)
    n_scored = len(ok)
    bf_n = max(0, int(round(float(batters_faced))))
    tto = bf_n / 9.0 if bf_n else float("nan")
    if n_scored == 0 or n_lineup == 0:
        return {
            "expected_k_pct": float("nan"),
            "expected_whiff_pct": float("nan"),
            "expected_ks": float("nan"),
            "expected_ks_1x": float("nan"),
            "lineup_batters": n_lineup,
            "lineup_scored": 0,
            "lineup_coverage": 0.0,
            "bf_scored": 0,
            "times_through_order": tto,
            "missing_batters": "; ".join(missing),
            "batter_detail": batter_scores,
        }

    mean_k = sum(float(b["expected_k_pct"]) for b in ok) / n_scored
    mean_whiff = sum(float(b["expected_whiff_pct"]) for b in ok) / n_scored
    ks_1x = sum(float(b["expected_k_pct"]) for b in ok) / 100.0

    # Full outing: walk the batting order for projected batters faced.
    expected_ks = 0.0
    bf_scored = 0
    for i in range(bf_n):
        b = batter_scores[i % n_lineup]
        if b["status"] != "ok":
            continue
        expected_ks += float(b["expected_k_pct"]) / 100.0
        bf_scored += 1

    return {
        "expected_k_pct": mean_k,
        "expected_whiff_pct": mean_whiff,
        "expected_ks": expected_ks,
        "expected_ks_1x": ks_1x,
        "lineup_batters": n_lineup,
        "lineup_scored": n_scored,
        "lineup_coverage": n_scored / n_lineup if n_lineup else 0.0,
        "bf_scored": bf_scored,
        "times_through_order": tto,
        "missing_batters": "; ".join(missing),
        "batter_detail": batter_scores,
    }


def format_table(df: pd.DataFrame) -> str:
    show = df.copy()
    for col in (
        "expected_k_pct",
        "expected_whiff_pct",
        "expected_ks",
        "expected_ks_1x",
        "projected_ip",
        "times_through_order",
    ):
        if col in show.columns:
            show[col] = show[col].map(
                lambda x: "" if pd.isna(x) else f"{x:.2f}"
            )
    if "lineup_coverage" in show.columns:
        show["lineup_coverage"] = show["lineup_coverage"].map(
            lambda x: "" if pd.isna(x) else f"{100 * float(x):.0f}%"
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
            "expected_ks",
            "projected_ip",
            "times_through_order",
            "projected_bf",
            "expected_k_pct",
            "lineup_source",
            "lineup_coverage",
            "status",
        ]
        if c in show.columns
    ]
    return show[cols].to_string(index=False)


def format_batter_detail(row: dict[str, Any]) -> str:
    """Pretty-print per-batter K expectations for one matchup."""
    detail = row.get("batter_detail") or []
    if not detail:
        return ""
    ip = row.get("projected_ip")
    tto = row.get("times_through_order")
    bf = row.get("projected_bf") or row.get("batters_faced_assumed")
    header = f"  {row.get('pitcher')} vs {row.get('opponent')} ({row.get('lineup_source')})"
    if pd.notna(row.get("expected_ks")):
        header += f" expected_ks={float(row['expected_ks']):.2f}"
    if pd.notna(ip) and pd.notna(tto):
        header += f" | {float(ip):.1f} IP · {float(tto):.2f}× order · BF {bf}"
    lines = [header]
    for b in detail:
        k = b.get("expected_k_pct")
        k_s = f"{float(k):.1f}%" if k is not None and pd.notna(k) else "  n/a"
        lines.append(
            f"    {b.get('slot'):>2}. {b.get('batter'):<22} {k_s}  {b.get('status')}"
        )
    return "\n".join(lines)


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    today = date.today().isoformat()
    p = argparse.ArgumentParser(
        description=(
            "Rank starting pitchers by expected strikeouts against the "
            "opposing starting lineup's pitch-type vulnerability."
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
        "--batters-faced",
        type=float,
        default=None,
        help=(
            "Force a fixed batters-faced for every starter. "
            "Default: each pitcher's season BF per start (else "
            f"{DEFAULT_PROJECTED_IP} IP × {DEFAULT_BF_PER_IP} BF/IP)"
        ),
    )
    p.add_argument(
        "--ip",
        type=float,
        default=None,
        help=(
            "Force projected innings for every starter. "
            "BF is derived from the pitcher's season BF/IP "
            f"(fallback {DEFAULT_BF_PER_IP})"
        ),
    )
    p.add_argument(
        "--lineup-lookback",
        type=int,
        default=14,
        help=(
            "Days to look back for a prior starting lineup when today's "
            "official lineup is not posted (default: 14)"
        ),
    )
    p.add_argument(
        "--require-official-lineup",
        action="store_true",
        help="Skip matchups without an official posted lineup for the date",
    )
    p.add_argument(
        "--detail",
        action="store_true",
        help="Print per-batter K%% vs arsenal under the rankings table",
    )
    p.add_argument(
        "-o",
        "--output",
        metavar="PATH",
        help="Write full rankings CSV to this path",
    )
    p.add_argument(
        "--html",
        metavar="PATH",
        help="Write self-contained interactive HTML rankings to this path",
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

    if args.batters_faced is not None and args.batters_faced <= 0:
        raise SystemExit("--batters-faced must be positive")
    if args.ip is not None and args.ip <= 0:
        raise SystemExit("--ip must be positive")

    if args.matchups:
        matchups = load_matchups_csv(args.matchups)
        ref_year = date.today().year
        game_date = date.today().isoformat()
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
    log(
        args.verbose,
        f"Using Savant year={year}, min_pa={args.min_pa}, "
        f"min_usage={args.min_usage}, "
        f"ip_override={args.ip}, bf_override={args.batters_faced}",
    )

    prior_lineups = build_prior_lineups(
        game_date, args.lineup_lookback, args.verbose
    )

    arsenal = load_pitcher_arsenal(year, args.min_pa, args.verbose)
    batter_df = load_batter_pitch_rates(year, args.min_pa, args.verbose)
    id_to_name, name_to_id = build_pitcher_indexes(arsenal)

    # Resolve pitchers first so we can batch-fetch season outing lengths.
    resolved: list[dict[str, Any]] = []
    pitcher_ids: list[int] = []
    for _, m in matchups.iterrows():
        pid, display, status = resolve_pitcher(
            m.get("pitcher"),
            m.get("pitcher_id"),
            id_to_name,
            name_to_id,
        )
        if pid is not None:
            pitcher_ids.append(int(pid))
        opponent = normalize_team(m.get("opponent"))
        posted = m.get("lineup") or []
        if isinstance(posted, float) and pd.isna(posted):
            posted = []
        lineup, lineup_source = resolve_lineup(
            opponent,
            list(posted) if posted else [],
            m.get("lineup_source"),
            prior_lineups,
        )
        resolved.append(
            {
                "pitcher": display or m.get("pitcher"),
                "pitcher_id": pid if pid is not None else m.get("pitcher_id"),
                "pitcher_team": normalize_team(m.get("pitcher_team")),
                "opponent": opponent,
                "game": m.get("game"),
                "status": status,
                "lineup": lineup,
                "lineup_source": lineup_source,
            }
        )

    season_outings = fetch_pitcher_season_outings(pitcher_ids, year, args.verbose)

    results: list[dict[str, Any]] = []
    for item in resolved:
        pid_raw = item.get("pitcher_id")
        pid: int | None
        try:
            pid = int(pid_raw) if pid_raw is not None and not pd.isna(pid_raw) else None
        except (TypeError, ValueError):
            pid = None

        outing = project_starter_outing(
            pid,
            season_outings,
            ip_override=args.ip,
            bf_override=args.batters_faced,
        )

        row: dict[str, Any] = {
            "pitcher": item.get("pitcher"),
            "pitcher_id": pid if pid is not None else item.get("pitcher_id"),
            "pitcher_team": item.get("pitcher_team"),
            "opponent": item.get("opponent"),
            "game": item.get("game"),
            "status": item.get("status"),
            "lineup_source": item.get("lineup_source"),
            "projected_ip": outing["projected_ip"],
            "projected_bf": outing["projected_bf"],
            "times_through_order": outing["times_through_order"],
            "outing_source": outing["outing_source"],
            "expected_k_pct": float("nan"),
            "expected_whiff_pct": float("nan"),
            "expected_ks": float("nan"),
            "expected_ks_1x": float("nan"),
            "lineup_batters": len(item.get("lineup") or []),
            "lineup_scored": 0,
            "lineup_coverage": float("nan"),
            "bf_scored": 0,
            "missing_batters": "",
            "batters_faced_assumed": outing["projected_bf"],
            "batter_detail": [],
        }

        lineup = item.get("lineup") or []
        lineup_source = item.get("lineup_source")
        status = item.get("status")

        if args.require_official_lineup and lineup_source != "official":
            row["status"] = "missing_official_lineup"
            results.append(row)
            continue

        if not lineup:
            row["status"] = "missing_lineup"
            results.append(row)
            continue

        if status == "ok" and pid is not None:
            usage = pitcher_usage_weights(arsenal, pid, args.min_usage)
            if usage is None:
                row["status"] = "missing_arsenal"
            else:
                scores = score_vs_lineup(
                    usage, lineup, batter_df, outing["projected_bf"]
                )
                detail = scores.pop("batter_detail", [])
                row.update(scores)
                row["batter_detail"] = detail
                if detail:
                    row["lineup_batter_ids"] = ",".join(
                        str(b["batter_id"]) for b in detail
                    )
                    row["lineup_batter_names"] = "; ".join(
                        str(b["batter"]) for b in detail
                    )
                if pd.isna(row["expected_k_pct"]):
                    row["status"] = "insufficient_batter_rates"
                else:
                    row["status"] = "ok"
        elif status == "ok":
            row["status"] = "missing_arsenal"

        results.append(row)

    out = pd.DataFrame(results)
    # Rank scored rows by expected strikeouts vs lineup; unscored sink to bottom.
    out = out.sort_values(
        by=["expected_ks"],
        ascending=False,
        na_position="last",
        kind="mergesort",
    ).reset_index(drop=True)
    ranks: list[Any] = []
    rank_i = 1
    for _, r in out.iterrows():
        if r["status"] == "ok" and pd.notna(r["expected_ks"]):
            ranks.append(rank_i)
            rank_i += 1
        else:
            ranks.append(pd.NA)
    out.insert(0, "rank", ranks)

    print(format_table(out))
    if args.detail:
        print()
        for _, r in out.iterrows():
            if r.get("status") != "ok":
                continue
            block = format_batter_detail(r.to_dict())
            if block:
                print(block)
    if args.output:
        # Drop nested batter_detail from CSV (ids/names columns already stored).
        csv_out = out.drop(columns=["batter_detail"], errors="ignore")
        csv_out.to_csv(args.output, index=False)
        log(True, f"Wrote {args.output}")

    if args.html:
        write_interactive_html(
            args.html,
            out,
            game_date=game_date,
            batters_faced=args.batters_faced,
        )
        log(True, f"Wrote {args.html}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
