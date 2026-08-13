#!/usr/bin/env python3
"""Rank MLB starters by expected strikeouts vs the opposing starting lineup."""

from __future__ import annotations

import argparse
import os
import sys
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Any
from zoneinfo import ZoneInfo

import pandas as pd
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from rankings_html import write_interactive_html  # noqa: E402
from sharpen import (  # noqa: E402
    apply_lineup_discipline_overlay,
    apply_lineup_offense_overlay,
    apply_attack_plate_stuff_bump,
    apply_pitcher_advanced_metrics,
    apply_pitcher_stuff_overlay,
    apply_recent_form_overlay,
    apply_ticket_outlook,
    arsenal_from_mixes,
    build_hits_board,
    build_savant_pitcher_stuff,
    classify_outing_risk,
    effective_bat_side,
    enrich_lineup_hits_props,
    fetch_batter_contact_quality,
    fetch_batter_hand_k_rates,
    fetch_batter_offense_profiles,
    fetch_batter_pitch_k_vs_hand,
    fetch_fangraphs_batting,
    fetch_fangraphs_pitching,
    fetch_pitcher_hand_mixes,
    fetch_pitcher_rate_stats,
    fetch_pitcher_recent_form,
    fetch_savant_pitcher_expected,
    merge_risk_metrics,
    platoon_adjust_k_pct,
    summarize_lineup_offense,
    usage_for_batter_side,
)
from odds import (  # noqa: E402
    DEFAULT_MARKETS,
    enrich_dataframe_odds,
    format_american,
    resolve_api_key,
)
from vs_team_history import (  # noqa: E402
    enrich_dataframe_vs_team_history,
    format_vs_team_console,
)

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
PEOPLE_URL = "https://statsapi.mlb.com/api/v1/people?personIds={ids}"

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
# Opener / swingman: total IP÷GS is inflated by relief work.
MIN_APPEARANCES_FOR_ROLE = 10
OPENER_START_SHARE = 0.25  # GS/G below this → opener candidate
SWINGMAN_START_SHARE = 0.50  # GS/G below this → contaminated IP/GS
OPENER_PROJECTED_IP = 1.5
OPENER_EST_START_IP = 2.5  # est start IP below this → treat as opener
RELIEF_IP_PER_APP = 1.0  # assume ~1 IP per non-start when backing out start IP
SWINGMAN_PROJECTED_IP = 3.0  # fallback only if start IP can't be estimated
DEFAULT_MIN_PA_BATTER = 1


CENTRAL_TZ = ZoneInfo("America/Chicago")


def format_game_time_ct(game_date_iso: Any, *, start_tbd: bool = False) -> str | None:
    """Format MLB Stats API gameDate (UTC ISO) as Central Time, e.g. '12:05 PM CT'."""
    if start_tbd:
        return "TBD CT"
    if game_date_iso is None or (isinstance(game_date_iso, float) and pd.isna(game_date_iso)):
        return None
    text = str(game_date_iso).strip()
    if not text:
        return None
    try:
        if text.endswith("Z"):
            dt = datetime.fromisoformat(text.replace("Z", "+00:00"))
        else:
            dt = datetime.fromisoformat(text)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=ZoneInfo("UTC"))
        local = dt.astimezone(CENTRAL_TZ)
        # Platform-safe 12h clock without leading zero quirks.
        hour = local.strftime("%I").lstrip("0") or "12"
        return f"{hour}:{local.strftime('%M %p')} CT"
    except (TypeError, ValueError):
        return None


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


def fetch_people_profiles(
    player_ids: list[int], verbose: bool
) -> dict[int, dict[str, Any]]:
    """Handedness + name keyed by player_id."""
    ids = sorted({int(pid) for pid in player_ids if pid is not None})
    out: dict[int, dict[str, Any]] = {}
    for i in range(0, len(ids), 50):
        chunk = ids[i : i + 50]
        url = PEOPLE_URL.format(ids=",".join(str(x) for x in chunk))
        payload = fetch_json(url, verbose)
        for person in payload.get("people", []):
            pid = person.get("id")
            if pid is None:
                continue
            pitch = person.get("pitchHand") or {}
            bat = person.get("batSide") or {}
            out[int(pid)] = {
                "full_name": person.get("fullName"),
                "pitch_hand": pitch.get("code"),
                "pitch_hand_desc": pitch.get("description"),
                "bat_side": bat.get("code"),
                "bat_side_desc": bat.get("description"),
            }
    return out


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
            g = float(stat.get("gamesPlayed") or 0)
            bf = float(stat.get("battersFaced") or 0)
            so = float(stat.get("strikeOuts") or 0)
            out[int(pid)] = {
                "ip": ip if ip is not None else 0.0,
                "gs": gs,
                "g": g,
                "bf": bf,
                "so": so,
            }
    return out


def estimate_start_ip(season_ip: float, season_gs: float, season_g: float) -> float | None:
    """Estimate IP per start when season totals include relief appearances.

    Backs out ~1 IP per non-start so IP÷GS is not inflated by bullpen work.
    """
    if season_gs <= 0:
        return None
    if season_g <= season_gs:
        return season_ip / season_gs
    relief_g = max(0.0, season_g - season_gs)
    est_relief_ip = min(season_ip, relief_g * RELIEF_IP_PER_APP)
    return max(0.5, (season_ip - est_relief_ip) / season_gs)


def classify_outing_role(
    season_gs: float,
    season_g: float,
    season_ip: float,
    *,
    est_start_ip: float | None = None,
) -> str:
    """starter | swingman | opener_likely from season appearance mix."""
    if season_g < MIN_APPEARANCES_FOR_ROLE or season_g <= 0:
        return "starter"
    start_share = season_gs / season_g
    ip_per_g = season_ip / season_g if season_g > 0 else 0.0
    est = est_start_ip if est_start_ip is not None else estimate_start_ip(
        season_ip, season_gs, season_g
    )
    # True openers: rarely start, and estimated start length is short.
    if (
        start_share < OPENER_START_SHARE
        and est is not None
        and est < OPENER_EST_START_IP
    ):
        return "opener_likely"
    # Few "starts" with a heavy relief workload — treat as opener even if
    # IP÷GS is contaminated (e.g. Legumina 2 GS / 33 G listed as probable).
    if (
        season_gs <= 3
        and season_g >= MIN_APPEARANCES_FOR_ROLE
        and start_share < SWINGMAN_START_SHARE
    ):
        return "opener_likely"
    if (
        start_share < SWINGMAN_START_SHARE
        and ip_per_g < 2.0
        and (est is None or est < OPENER_EST_START_IP)
    ):
        return "opener_likely"
    if start_share < SWINGMAN_START_SHARE:
        return "swingman"
    return "starter"


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
      2. opener short-outing when role is opener_likely
      3. season averages (with relief-backed-out start IP when G > GS)
      4. defaults (5.5 IP × 4.25 BF/IP)

    Note: raw season IP÷GS is unreliable for openers/swingmen because relief
    innings inflate the numerator.
    """
    season = season_outings.get(int(pitcher_id)) if pitcher_id is not None else None
    season_ip = float(season["ip"]) if season else 0.0
    season_gs = float(season["gs"]) if season else 0.0
    season_g = float(season.get("g") or 0.0) if season else 0.0
    season_bf = float(season["bf"]) if season else 0.0
    est_start_ip = estimate_start_ip(season_ip, season_gs, season_g)
    outing_role = classify_outing_role(
        season_gs, season_g, season_ip, est_start_ip=est_start_ip
    )

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
    elif outing_role == "opener_likely":
        projected_ip = OPENER_PROJECTED_IP
        projected_bf = projected_ip * bf_per_ip
        source = "opener_profile"
    elif est_start_ip is not None and season_gs > 0:
        # Prefer relief-adjusted start IP whenever we have GS (fixes G>GS inflation).
        projected_ip = float(est_start_ip)
        if season_bf > 0 and season_ip > 0:
            # Scale BF with the same relief adjustment ratio when possible.
            raw_ip_gs = season_ip / season_gs
            raw_bf_gs = season_bf / season_gs
            if raw_ip_gs > 0:
                projected_bf = raw_bf_gs * (projected_ip / raw_ip_gs)
            else:
                projected_bf = projected_ip * bf_per_ip
        else:
            projected_bf = projected_ip * bf_per_ip
        source = (
            "season_start_est"
            if season_g > season_gs
            else "season_avg"
        )
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
    # Skip for openers — those already use role-based short outings.
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
        "outing_role": outing_role,
        "season_ip": season_ip if season_gs else float("nan"),
        "season_gs": season_gs if season_gs else float("nan"),
        "season_g": season_g if season_g else float("nan"),
        "season_bf_per_start": (season_bf / season_gs) if season_gs else float("nan"),
        "est_start_ip": est_start_ip if est_start_ip is not None else float("nan"),
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
    cols = [
        "player_id",
        "name_last_first",
        "team",
        "pitch_type",
        "pa",
        "k_percent",
        "whiff_percent",
    ]
    if "pitch_name" in df.columns:
        cols.insert(4, "pitch_name")
    return df[cols]


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
            status = game.get("status") or {}
            game_time_ct = format_game_time_ct(
                game.get("gameDate"),
                start_tbd=bool(status.get("startTimeTBD")),
            )
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
                        "game_time_utc": game.get("gameDate"),
                        "game_time_ct": game_time_ct,
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
    df["game_time_utc"] = pd.NA
    df["game_time_ct"] = pd.NA
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
            "game_time_utc",
            "game_time_ct",
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
    cols = ["pitch_type", "usage_frac", "pitch_usage"]
    if "pitch_name" in subset.columns:
        cols.insert(1, "pitch_name")
    return subset[cols]


def build_pitch_reference_rates(
    batter_df: pd.DataFrame,
    people: dict[int, dict[str, Any]] | None = None,
) -> tuple[dict[str, dict[str, float]], dict[tuple[str, str], dict[str, float]]]:
    """PA-weighted league K%/whiff by pitch, and by (bat_side, pitch)."""
    people = people or {}
    df = batter_df.copy()
    df["pa"] = pd.to_numeric(df["pa"], errors="coerce")
    df["k_percent"] = pd.to_numeric(df["k_percent"], errors="coerce")
    df["whiff_percent"] = pd.to_numeric(df["whiff_percent"], errors="coerce")
    df = df.dropna(subset=["pitch_type", "pa", "k_percent"])
    df = df[df["pa"] > 0]
    df["bat_side"] = df["player_id"].map(
        lambda pid: (people.get(int(pid)) or {}).get("bat_side")
        if pd.notna(pid)
        else None
    )

    def _agg(frame: pd.DataFrame) -> dict[str, float]:
        pa = float(frame["pa"].sum())
        k = float((frame["k_percent"] * frame["pa"]).sum() / pa)
        wh = frame.dropna(subset=["whiff_percent"])
        if wh.empty:
            whiff = k
        else:
            whiff = float(
                (wh["whiff_percent"] * wh["pa"]).sum() / float(wh["pa"].sum())
            )
        return {"k_percent": k, "whiff_percent": whiff, "pa": pa}

    league_pitch: dict[str, dict[str, float]] = {}
    for pt, g in df.groupby("pitch_type"):
        league_pitch[str(pt)] = _agg(g)

    league_side_pitch: dict[tuple[str, str], dict[str, float]] = {}
    sided = df.dropna(subset=["bat_side"])
    if not sided.empty:
        for (side, pt), g in sided.groupby(["bat_side", "pitch_type"]):
            league_side_pitch[(str(side), str(pt))] = _agg(g)

    return league_pitch, league_side_pitch


def score_batter_vs_arsenal(
    usage: pd.DataFrame,
    batter_rates: pd.DataFrame,
    *,
    bat_side: str | None = None,
    pitcher_hand: str | None = None,
    pitch_k_vs_hand: dict[str, dict[str, dict[str, float]]] | None = None,
    league_pitch: dict[str, dict[str, float]] | None = None,
    league_side_pitch: dict[tuple[str, str], dict[str, float]] | None = None,
) -> dict[str, Any] | None:
    """Arsenal-weighted K%/whiff for one batter, plus per-pitch K breakdown.

    Preference order per arsenal pitch:
      1. batter's true K% vs that pitch against this pitcher hand (Statcast)
      2. batter's overall Savant K% vs that pitch
      3. same-handed league-average K% vs that pitch
      4. overall league vs that pitch

    Never copy another pitch's K% from the same batter — that skews rare/unseen
    pitches.
    """
    league_pitch = league_pitch or {}
    league_side_pitch = league_side_pitch or {}
    by_pitch = (
        batter_rates.set_index("pitch_type")
        if not batter_rates.empty
        else pd.DataFrame()
    )
    hand_key = str(pitcher_hand).upper() if pitcher_hand else None
    hand_pitch_rates = (
        (pitch_k_vs_hand or {}).get(hand_key) if hand_key in {"L", "R"} else None
    )
    hand_source = (
        f"pitch_vs_{hand_key.lower()}hp" if hand_key in {"L", "R"} else None
    )

    exp_k = 0.0
    exp_whiff = 0.0
    covered = 0.0
    hand_covered = 0.0
    pitch_breakdown: list[dict[str, Any]] = []
    for _, row in usage.iterrows():
        pt = str(row["pitch_type"])
        w = float(row["usage_frac"])
        pitch_name = (
            str(row["pitch_name"])
            if "pitch_name" in row.index and pd.notna(row.get("pitch_name"))
            else pt
        )
        entry: dict[str, Any] = {
            "pitch_type": pt,
            "pitch_name": pitch_name,
            "usage_pct": float(row["pitch_usage"]) if "pitch_usage" in row.index else w * 100.0,
            "usage_frac": w,
            "k_percent": None,
            "whiff_percent": None,
            "pa": None,
            "k_source": None,
        }

        hand_hit = hand_pitch_rates.get(pt) if hand_pitch_rates else None
        if hand_hit is not None and float(hand_hit.get("pa") or 0) > 0:
            entry["k_percent"] = float(hand_hit["k_percent"])
            entry["pa"] = float(hand_hit["pa"])
            entry["k_source"] = hand_source
            # Whiff not derived from PA endings; fall back to overall pitch whiff.
            if not by_pitch.empty and pt in by_pitch.index:
                wh = by_pitch.loc[pt, "whiff_percent"]
                entry["whiff_percent"] = float(wh) if pd.notna(wh) else None
            hand_covered += w
        elif not by_pitch.empty and pt in by_pitch.index:
            k = float(by_pitch.loc[pt, "k_percent"])
            wh = by_pitch.loc[pt, "whiff_percent"]
            pa = by_pitch.loc[pt, "pa"] if "pa" in by_pitch.columns else None
            entry["k_percent"] = k
            entry["whiff_percent"] = float(wh) if pd.notna(wh) else None
            entry["pa"] = float(pa) if pa is not None and pd.notna(pa) else None
            entry["k_source"] = "pitch"
        else:
            ref = None
            source = None
            if bat_side and (str(bat_side), pt) in league_side_pitch:
                ref = league_side_pitch[(str(bat_side), pt)]
                source = "league_platoon"
            elif pt in league_pitch:
                ref = league_pitch[pt]
                source = "league_pitch"
            if ref is not None:
                entry["k_percent"] = float(ref["k_percent"])
                entry["whiff_percent"] = float(ref["whiff_percent"])
                entry["pa"] = float(ref.get("pa") or 0.0)
                entry["k_source"] = source

        if entry["k_percent"] is not None:
            k = float(entry["k_percent"])
            wh = entry["whiff_percent"]
            exp_k += w * k
            exp_whiff += w * float(wh if wh is not None else k)
            covered += w
        pitch_breakdown.append(entry)

    if covered <= 0:
        return None
    if covered < 0.999:
        exp_k /= covered
        exp_whiff /= covered
    return {
        "expected_k_pct": exp_k,
        "expected_whiff_pct": exp_whiff,
        "usage_covered": covered,
        "hand_pitch_coverage": hand_covered / covered if covered else 0.0,
        "pitch_breakdown": pitch_breakdown,
        "used_league_fill": any(
            p.get("k_source") in {"league_pitch", "league_platoon"}
            for p in pitch_breakdown
        ),
    }


def score_vs_lineup(
    usage: pd.DataFrame,
    lineup: list[dict[str, Any]],
    batter_df: pd.DataFrame,
    batters_faced: float,
    people: dict[int, dict[str, Any]] | None = None,
    *,
    pitcher_hand: str | None = None,
    hand_mixes: dict[str, Any] | None = None,
    batter_hand_rates: dict[int, dict[str, Any]] | None = None,
    batter_pitch_k_vs_hand: dict[int, dict[str, dict[str, dict[str, float]]]]
    | None = None,
) -> dict[str, Any]:
    """Score starter arsenal vs opposing starting nine over a full outing.

    Prefer each batter's true pitch-type K% vs this pitcher hand, then overall
    Savant pitch rates. Missing samples use same-handed league-average K% vs
    that pitch (else overall league), so every heatmap cell can show a rate.

    When Statcast hand mixes are available, each batter is scored against the
    pitcher's usage vs that batter's stand (switch-hitters use the platoon
    stand). Soft overall batter-hand K% adjust is skipped when pitch×hand
    rates already cover most of the arsenal.

    expected_k_pct       = mean arsenal-weighted K% across lineup batters with data
    expected_ks_1x       = known K expectation for one trip through the order
    expected_ks          = walk batting order for projected BF (innings/TTO based)
    times_through_order  = batters_faced / 9
    """
    people = people or {}
    batter_hand_rates = batter_hand_rates or {}
    batter_pitch_k_vs_hand = batter_pitch_k_vs_hand or {}
    league_pitch, league_side_pitch = build_pitch_reference_rates(batter_df, people)
    batter_scores: list[dict[str, Any]] = []
    missing: list[str] = []

    def _finalize_batter_k(
        raw_k: float,
        bid: int,
        hand_pitch_coverage: float,
    ) -> tuple[float, float | None, str]:
        # Avoid double-counting platoon when pitch×hand rates already dominate.
        if hand_pitch_coverage >= 0.60:
            return raw_k, None, "pitch_vs_hand"
        return platoon_adjust_k_pct(
            raw_k, batter_hand_rates.get(bid), pitcher_hand
        )

    for slot_row in lineup:
        bid = int(slot_row["batter_id"])
        profile = people.get(bid) or {}
        name = slot_row.get("batter") or profile.get("full_name") or str(bid)
        bat_side = profile.get("bat_side")
        stand = effective_bat_side(bat_side, pitcher_hand)
        batter_usage, usage_source = usage_for_batter_side(hand_mixes, usage, stand)
        if batter_usage is None:
            missing.append(name)
            batter_scores.append(
                {
                    "slot": slot_row.get("slot"),
                    "batter_id": bid,
                    "batter": name,
                    "bat_side": bat_side,
                    "stand_used": stand,
                    "usage_source": usage_source,
                    "expected_k_pct": float("nan"),
                    "status": "missing_arsenal",
                    "pitches": [],
                }
            )
            continue

        rates = batter_df[batter_df["player_id"] == bid]
        scored = score_batter_vs_arsenal(
            batter_usage,
            rates,
            bat_side=stand or bat_side,
            pitcher_hand=pitcher_hand,
            pitch_k_vs_hand=batter_pitch_k_vs_hand.get(bid),
            league_pitch=league_pitch,
            league_side_pitch=league_side_pitch,
        )
        if scored is None:
            # Last resort: still emit league pitch cells when possible.
            empty_pitches = []
            for _, row in batter_usage.iterrows():
                pt = str(row["pitch_type"])
                ref = None
                source = None
                side_key = stand or bat_side
                if side_key and (str(side_key), pt) in league_side_pitch:
                    ref = league_side_pitch[(str(side_key), pt)]
                    source = "league_platoon"
                elif pt in league_pitch:
                    ref = league_pitch[pt]
                    source = "league_pitch"
                empty_pitches.append(
                    {
                        "pitch_type": pt,
                        "pitch_name": (
                            str(row["pitch_name"])
                            if "pitch_name" in row.index and pd.notna(row.get("pitch_name"))
                            else pt
                        ),
                        "usage_pct": float(row["pitch_usage"]),
                        "usage_frac": float(row["usage_frac"]),
                        "k_percent": None if ref is None else float(ref["k_percent"]),
                        "whiff_percent": (
                            None if ref is None else float(ref["whiff_percent"])
                        ),
                        "pa": None if ref is None else float(ref.get("pa") or 0.0),
                        "k_source": source,
                    }
                )
            known = [p for p in empty_pitches if p["k_percent"] is not None]
            if known:
                mean_k = sum(
                    float(p["usage_frac"]) * float(p["k_percent"]) for p in known
                ) / sum(float(p["usage_frac"]) for p in known)
                adj_k, platoon_factor, platoon_src = _finalize_batter_k(mean_k, bid, 0.0)
                batter_scores.append(
                    {
                        "slot": slot_row.get("slot"),
                        "batter_id": bid,
                        "batter": name,
                        "bat_side": bat_side,
                        "stand_used": stand,
                        "usage_source": usage_source,
                        "expected_k_pct": adj_k,
                        "expected_k_pct_raw": mean_k,
                        "platoon_factor": platoon_factor,
                        "platoon_source": platoon_src,
                        "hand_pitch_coverage": 0.0,
                        "expected_whiff_pct": mean_k,
                        "status": "ok",
                        "pitches": empty_pitches,
                    }
                )
            else:
                missing.append(name)
                batter_scores.append(
                    {
                        "slot": slot_row.get("slot"),
                        "batter_id": bid,
                        "batter": name,
                        "bat_side": bat_side,
                        "stand_used": stand,
                        "usage_source": usage_source,
                        "expected_k_pct": float("nan"),
                        "status": "missing_rates",
                        "pitches": empty_pitches,
                    }
                )
            continue
        hand_cov = float(scored.get("hand_pitch_coverage") or 0.0)
        adj_k, platoon_factor, platoon_src = _finalize_batter_k(
            float(scored["expected_k_pct"]), bid, hand_cov
        )
        batter_scores.append(
            {
                "slot": slot_row.get("slot"),
                "batter_id": bid,
                "batter": name,
                "bat_side": bat_side,
                "stand_used": stand,
                "usage_source": usage_source,
                "expected_k_pct": adj_k,
                "expected_k_pct_raw": float(scored["expected_k_pct"]),
                "platoon_factor": platoon_factor,
                "platoon_source": platoon_src,
                "hand_pitch_coverage": hand_cov,
                "expected_whiff_pct": scored["expected_whiff_pct"],
                "status": "ok",
                "pitches": scored.get("pitch_breakdown") or [],
            }
        )

    ok = [b for b in batter_scores if b["status"] == "ok"]
    n_lineup = len(lineup)
    n_scored = len(ok)
    bf_n = max(0, int(round(float(batters_faced))))
    tto = bf_n / 9.0 if bf_n else float("nan")

    arsenal_pitches = arsenal_from_mixes(hand_mixes, usage)

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
            "arsenal": arsenal_pitches,
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

    # Lineup-average K% vs each arsenal pitch (batters with that pitch rate only).
    pitch_lineup_avg: list[dict[str, Any]] = []
    for pitch in arsenal_pitches:
        pt = pitch["pitch_type"]
        vals = []
        for b in ok:
            for pb in b.get("pitches") or []:
                if pb.get("pitch_type") == pt and pb.get("k_percent") is not None:
                    vals.append(float(pb["k_percent"]))
        pitch_lineup_avg.append(
            {
                **pitch,
                "lineup_k_pct": (sum(vals) / len(vals)) if vals else None,
                "batters_with_rate": len(vals),
            }
        )

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
        "arsenal": arsenal_pitches,
        "pitch_lineup_avg": pitch_lineup_avg,
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
    for col in (
        "last3_ks",
        "bb9",
        "hr9",
        "xfip",
        "lineup_k_pct",
        "lineup_bb_pct",
        "lineup_bip_pct",
        "offense_factor",
        "pitcher_k_pct",
        "pitcher_gb_pct",
        "pitcher_contact_pct",
    ):
        if col in show.columns:
            show[col] = show[col].map(
                lambda x: "" if pd.isna(x) or x is None else f"{float(x):.2f}"
            )
    if "lineup_avg" in show.columns:
        show["lineup_avg"] = show["lineup_avg"].map(
            lambda x: "" if pd.isna(x) or x is None else f"{float(x):.3f}"
        )
    cols = [
        c
        for c in [
            "rank",
            "pitcher",
            "pitch_hand",
            "pitcher_team",
            "opponent",
            "game",
            "game_time_ct",
            "expected_ks",
            "projected_ip",
            "times_through_order",
            "projected_bf",
            "expected_k_pct",
            "lineup_k_pct",
            "lineup_bip_pct",
            "contact_grade",
            "lineup_bb_pct",
            "offense_factor",
            "last3_ks",
            "bb9",
            "hr9",
            "xfip",
            "outing_risk",
            "outing_role",
            "ticket_outlook",
            "arsenal_abs_grade",
            "stuff_grade",
            "stuff_whiff_pct",
            "spike_risk",
            "pitcher_style",
            "pitcher_k_pct",
            "pitcher_gb_pct",
            "matchup_grade",
            "arsenal_matchup_rank",
            "arsenal_vs_league",
            "discipline_grade",
            "pitch_count_risk",
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
    hand = row.get("pitch_hand")
    hand_s = f" ({hand}HP)" if hand else ""
    header = (
        f"  {row.get('pitcher')}{hand_s} vs {row.get('opponent')} "
        f"({row.get('lineup_source')})"
    )
    if pd.notna(row.get("expected_ks")):
        header += f" expected_ks={float(row['expected_ks']):.2f}"
    if pd.notna(ip) and pd.notna(tto):
        header += f" | {float(ip):.1f} IP · {float(tto):.2f}× order · BF {bf}"
    lines = [header]
    for b in detail:
        k = b.get("expected_k_pct")
        k_s = f"{float(k):.1f}%" if k is not None and pd.notna(k) else "  n/a"
        side = b.get("bat_side")
        side_s = f" ({side}HB)" if side else ""
        hits = b.get("hits_score")
        hits_s = f" hits={float(hits):.0f}" if hits is not None else ""
        brl = b.get("barrel_pct")
        hh = b.get("hard_hit_pct")
        contact_s = ""
        if brl is not None or hh is not None:
            contact_s = (
                f" brl={'' if brl is None else f'{float(brl):.1f}%'}"
                f" hh={'' if hh is None else f'{float(hh):.1f}%'}"
            )
        lines.append(
            f"    {b.get('slot'):>2}. {b.get('batter')}{side_s:<6} "
            f"{k_s}{hits_s}{contact_s}  {b.get('status')}"
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
        help="Minimum PA filter for Savant pitcher arsenal leaderboard (default: 50)",
    )
    p.add_argument(
        "--min-pa-batter",
        type=int,
        default=DEFAULT_MIN_PA_BATTER,
        help=(
            "Minimum PA filter for Savant batter pitch rates "
            f"(default: {DEFAULT_MIN_PA_BATTER}; lower = more complete heatmaps)"
        ),
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
        "--hits-output",
        metavar="PATH",
        help=(
            "Write Hits-prop board CSV (barrel/hard-hit/xwOBA scores). "
            "Does not affect expected_ks. Default: beside -o as hits-YYYY-MM-DD.csv"
        ),
    )
    p.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Log data fetches to stderr",
    )
    p.add_argument(
        "--odds",
        action=argparse.BooleanOptionalAction,
        default=True,
        help=(
            "Join live book lines from The Odds API using ODDS_API_KEY / "
            "THE_ODDS_API_KEY (default: on when key present; --no-odds skips)"
        ),
    )
    p.add_argument(
        "--odds-key",
        metavar="KEY",
        help="Odds API key (default: ODDS_API_KEY or THE_ODDS_API_KEY env)",
    )
    p.add_argument(
        "--odds-markets",
        metavar="LIST",
        default=",".join(DEFAULT_MARKETS),
        help=(
            "Comma-separated Odds API markets. Default is credit-lite "
            f"({','.join(DEFAULT_MARKETS)} = 3 credits/game). "
            "Add pitcher_walks,pitcher_outs only when needed."
        ),
    )
    p.add_argument(
        "--odds-force",
        action="store_true",
        help="Bypass on-disk odds cache (normally reuses pulls for ~120 minutes)",
    )
    p.add_argument(
        "--odds-include-finished",
        action="store_true",
        help="Also fetch props for games that started >4.5h ago (default: skip)",
    )
    p.add_argument(
        "--odds-daily-budget",
        type=int,
        metavar="N",
        help=(
            "Max estimated odds credits per America/Chicago day "
            "(default: ODDS_DAILY_BUDGET or 500; 0 = unlimited). "
            "Over budget → reuse stale cache instead of fetching."
        ),
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
        f"Using Savant year={year}, min_pa_pitcher={args.min_pa}, "
        f"min_pa_batter={args.min_pa_batter}, min_usage={args.min_usage}, "
        f"ip_override={args.ip}, bf_override={args.batters_faced}",
    )

    prior_lineups = build_prior_lineups(
        game_date, args.lineup_lookback, args.verbose
    )

    arsenal = load_pitcher_arsenal(year, args.min_pa, args.verbose)
    savant_pitcher_stuff = build_savant_pitcher_stuff(arsenal)
    batter_df = load_batter_pitch_rates(year, args.min_pa_batter, args.verbose)
    id_to_name, name_to_id = build_pitcher_indexes(arsenal)

    # Resolve pitchers first so we can batch-fetch season outing lengths + hands.
    resolved: list[dict[str, Any]] = []
    pitcher_ids: list[int] = []
    batter_ids: list[int] = []
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
        for b in lineup:
            try:
                batter_ids.append(int(b["batter_id"]))
            except (KeyError, TypeError, ValueError):
                pass
        resolved.append(
            {
                "pitcher": display or m.get("pitcher"),
                "pitcher_id": pid if pid is not None else m.get("pitcher_id"),
                "pitcher_team": normalize_team(m.get("pitcher_team")),
                "opponent": opponent,
                "game": m.get("game"),
                "game_time_utc": m.get("game_time_utc"),
                "game_time_ct": m.get("game_time_ct"),
                "status": status,
                "lineup": lineup,
                "lineup_source": lineup_source,
            }
        )

    season_outings = fetch_pitcher_season_outings(pitcher_ids, year, args.verbose)
    people = fetch_people_profiles(pitcher_ids + batter_ids, args.verbose)

    # Sharpening layers: hand mixes, batter platoon K%, recent form, risk rates.
    hand_mixes = fetch_pitcher_hand_mixes(
        pitcher_ids, year, args.min_usage, args.verbose, log
    )
    # Returning / low-PA starters often miss the Savant arsenal board (min PA).
    # Statcast fallback is required — retry any pitcher the batch mix fetch dropped
    # (transient Savant blanks previously left arms like Javier unscored).
    missing_mix_ids = [
        pid
        for pid in pitcher_ids
        if pitcher_usage_weights(arsenal, pid, args.min_usage) is None
        and not (
            pid in hand_mixes and hand_mixes[pid].get("usage_all") is not None
        )
    ]
    if missing_mix_ids:
        log(
            True,
            f"Retrying Statcast pitch mixes for {len(missing_mix_ids)} "
            f"arsenal-missing pitcher(s): {missing_mix_ids}",
        )
        hand_mixes.update(
            fetch_pitcher_hand_mixes(
                missing_mix_ids, year, args.min_usage, args.verbose, log
            )
        )
    batter_k_vs_hand = fetch_batter_hand_k_rates(
        batter_ids, year, args.verbose, log
    )
    batter_pitch_k_vs_hand = fetch_batter_pitch_k_vs_hand(
        batter_ids, year, args.verbose, log
    )
    recent_form = fetch_pitcher_recent_form(
        pitcher_ids, year, args.verbose, log
    )
    fangraphs = fetch_fangraphs_pitching(year, args.verbose, log)
    fangraphs_batting = fetch_fangraphs_batting(year, args.verbose, log)
    savant_pitcher_expected = fetch_savant_pitcher_expected(year, args.verbose, log)
    api_rates = fetch_pitcher_rate_stats(pitcher_ids, year, args.verbose, log)
    batter_offense = fetch_batter_offense_profiles(
        batter_ids, year, args.verbose, log
    )
    # Hits-prop contact quality (barrel/hard-hit/xwOBA). Display-only vs K model.
    batter_contact = fetch_batter_contact_quality(year, args.verbose, log)

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
        pitcher_hand = (people.get(pid) or {}).get("pitch_hand") if pid is not None else None
        risk_metrics = merge_risk_metrics(pid, fangraphs, api_rates)
        form = recent_form.get(pid) if pid is not None else None
        # Survival haircut uses BB/HR/xFIP plus short recent IP.
        risk = classify_outing_risk(
            risk_metrics.get("bb9"),
            risk_metrics.get("hr9"),
            risk_metrics.get("xfip"),
            form=form,
            projected_ip=outing.get("projected_ip"),
        )
        # Mild BF haircut for early-exit / survival risk on overs.
        projected_bf = float(outing["projected_bf"]) * float(risk["bf_risk_factor"])
        if args.batters_faced is None and args.ip is None:
            projected_bf = min(projected_bf, float(MAX_PROJECTED_BF))
        projected_ip = float(outing["projected_ip"])
        if risk["bf_risk_factor"] < 1.0 and args.ip is None and args.batters_faced is None:
            projected_ip = projected_ip * float(risk["bf_risk_factor"])
        offense_summary = summarize_lineup_offense(
            item.get("lineup") or [],
            batter_offense,
            hand_rates=batter_k_vs_hand,
            pitcher_hand=pitcher_hand,
            fangraphs_batting=fangraphs_batting,
        )
        # Patient / walk-heavy lineups trim BF/IP before walking the order.
        if args.ip is None and args.batters_faced is None:
            _, projected_bf, projected_ip, discipline_meta = (
                apply_lineup_discipline_overlay(
                    0.0, projected_bf, projected_ip, offense_summary
                )
            )
        else:
            _, _, _, discipline_meta = apply_lineup_discipline_overlay(
                0.0, projected_bf, projected_ip, offense_summary
            )
        tto = projected_bf / 9.0 if projected_bf else float("nan")

        row: dict[str, Any] = {
            "pitcher": item.get("pitcher"),
            "pitcher_id": pid if pid is not None else item.get("pitcher_id"),
            "pitcher_team": item.get("pitcher_team"),
            "pitch_hand": pitcher_hand,
            "opponent": item.get("opponent"),
            "game": item.get("game"),
            "game_time_ct": item.get("game_time_ct"),
            "game_time_utc": item.get("game_time_utc"),
            "status": item.get("status"),
            "lineup_source": item.get("lineup_source"),
            "projected_ip": projected_ip,
            "projected_bf": int(round(projected_bf)),
            "times_through_order": tto,
            "outing_source": outing["outing_source"],
            "outing_role": outing.get("outing_role") or "starter",
            "expected_k_pct": float("nan"),
            "expected_whiff_pct": float("nan"),
            "expected_ks": float("nan"),
            "expected_ks_model": float("nan"),
            "expected_ks_1x": float("nan"),
            "lineup_batters": len(item.get("lineup") or []),
            "lineup_scored": 0,
            "lineup_coverage": float("nan"),
            "bf_scored": 0,
            "missing_batters": "",
            "batters_faced_assumed": int(round(projected_bf)),
            "bb9": risk_metrics.get("bb9"),
            "hr9": risk_metrics.get("hr9"),
            "k9": risk_metrics.get("k9"),
            "xfip": risk_metrics.get("xfip"),
            "fip": risk_metrics.get("fip"),
            "siera": risk_metrics.get("siera"),
            "xera": risk_metrics.get("xera"),
            "stuff_plus": risk_metrics.get("stuff_plus"),
            "location_plus": risk_metrics.get("location_plus"),
            "pitching_plus": risk_metrics.get("pitching_plus"),
            "pitcher_k_pct": risk_metrics.get("pitcher_k_pct"),
            "pitcher_contact_pct": risk_metrics.get("pitcher_contact_pct"),
            "z_contact_pct": risk_metrics.get("z_contact_pct"),
            "pitcher_gb_pct": risk_metrics.get("pitcher_gb_pct"),
            "pitcher_fb_pct": risk_metrics.get("pitcher_fb_pct"),
            "pitcher_iffb_pct": risk_metrics.get("pitcher_iffb_pct"),
            "pitcher_soft_pct": risk_metrics.get("pitcher_soft_pct"),
            "swstr_pct": risk_metrics.get("swstr_pct"),
            "csw_pct": risk_metrics.get("csw_pct"),
            "o_swing_pct": risk_metrics.get("o_swing_pct"),
            "strike_pct": risk_metrics.get("strike_pct"),
            "f_strike_pct": risk_metrics.get("f_strike_pct"),
            "zone_pct": risk_metrics.get("zone_pct"),
            "pitches": risk_metrics.get("pitches"),
            "strikes": risk_metrics.get("strikes"),
            "stuff_ceiling_bump": 0.0,
            "stuff_ceiling_note": "",
            "pitcher_style": risk_metrics.get("pitcher_style") or "",
            "pitcher_style_flags": risk_metrics.get("pitcher_style_flags") or "",
            "outing_risk": risk.get("outing_risk"),
            "risk_flags": risk.get("risk_flags") or "",
            "bf_risk_factor": risk.get("bf_risk_factor"),
            "survival_flags": risk.get("survival_flags") or "",
            "last3_ks": None if not form else form.get("last3_ks"),
            "last3_k9": None if not form else form.get("last3_k9"),
            "last3_ip": None if not form else form.get("last3_ip"),
            "last3_ks_adj": None if not form else form.get("last3_ks_adj"),
            "last3_k9_adj": None if not form else form.get("last3_k9_adj"),
            "last3_opp_k_pct": None if not form else form.get("last3_opp_k_pct"),
            "form_opp_factor": None if not form else form.get("form_opp_factor"),
            "form_opp_note": "" if not form else (form.get("form_opp_note") or ""),
            "form_ks": None,
            "form_weight": None,
            "lineup_k_pct": offense_summary.get("lineup_k_pct"),
            "lineup_k_pct_vs_lhp": offense_summary.get("lineup_k_pct_vs_lhp"),
            "lineup_k_pct_vs_rhp": offense_summary.get("lineup_k_pct_vs_rhp"),
            "lineup_k_pct_vs_hand": offense_summary.get("lineup_k_pct_vs_hand"),
            "lineup_k_vs_hand_side": offense_summary.get("lineup_k_vs_hand_side"),
            "lineup_k_vs_hand_pa": offense_summary.get("lineup_k_vs_hand_pa"),
            "lineup_k_vs_hand_n": offense_summary.get("lineup_k_vs_hand_n"),
            "lineup_k_vs_hand_source": offense_summary.get("lineup_k_vs_hand_source"),
            "lineup_avg": offense_summary.get("lineup_avg"),
            "lineup_bb_pct": offense_summary.get("lineup_bb_pct"),
            "lineup_bip_pct": offense_summary.get("lineup_bip_pct"),
            "lineup_woba": offense_summary.get("lineup_woba"),
            "lineup_wrc_plus": offense_summary.get("lineup_wrc_plus"),
            "lineup_iso": offense_summary.get("lineup_iso"),
            "lineup_quality_n": offense_summary.get("lineup_quality_n"),
            "lineup_quality_source": offense_summary.get("lineup_quality_source"),
            "contact_grade": offense_summary.get("contact_grade") or "",
            "offense_source": offense_summary.get("offense_source"),
            "offense_factor": None,
            "discipline_grade": discipline_meta.get("discipline_grade"),
            "discipline_ks_factor": discipline_meta.get("discipline_ks_factor"),
            "discipline_bf_factor": discipline_meta.get("discipline_bf_factor"),
            "pitch_count_risk": discipline_meta.get("pitch_count_risk"),
            "hand_mix_pitches_l": None
            if pid is None or pid not in hand_mixes
            else hand_mixes[pid].get("pitches_l"),
            "hand_mix_pitches_r": None
            if pid is None or pid not in hand_mixes
            else hand_mixes[pid].get("pitches_r"),
            "arsenal": [],
            "pitch_lineup_avg": [],
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

        if pid is not None and status in ("ok", "missing_arsenal"):
            usage = pitcher_usage_weights(arsenal, pid, args.min_usage)
            mixes = hand_mixes.get(pid)
            used_statcast_mix = False
            # Last-chance single-pitcher Statcast pull before marking unscored.
            if usage is None and not (mixes and mixes.get("usage_all") is not None):
                retry = fetch_pitcher_hand_mixes(
                    [pid], year, args.min_usage, args.verbose, log
                )
                if pid in retry:
                    hand_mixes[pid] = retry[pid]
                    mixes = retry[pid]
            if usage is None and not (mixes and mixes.get("usage_all") is not None):
                row["status"] = "missing_arsenal"
            else:
                # Prefer Savant arsenal board; fall back to Statcast pitch-level
                # when the board drops low-sample / returning starters (e.g. Javier).
                if usage is None and mixes is not None:
                    usage = mixes.get("usage_all")
                    used_statcast_mix = True
                scores = score_vs_lineup(
                    usage,
                    lineup,
                    batter_df,
                    projected_bf,
                    people=people,
                    pitcher_hand=pitcher_hand,
                    hand_mixes=mixes,
                    batter_hand_rates=batter_k_vs_hand,
                    batter_pitch_k_vs_hand=batter_pitch_k_vs_hand,
                )
                detail = scores.pop("batter_detail", [])
                enrich_lineup_hits_props(
                    detail,
                    pitcher_hand,
                    contact=batter_contact,
                    hand_rates=batter_k_vs_hand,
                    offense=batter_offense,
                )
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
                    matchup_ks = float(row["expected_ks"])
                    offense_ks, offense_factor, offense_meta = (
                        apply_lineup_offense_overlay(matchup_ks, offense_summary)
                    )
                    row["offense_factor"] = offense_factor
                    row["lineup_k_pct"] = offense_meta.get("lineup_k_pct")
                    row["lineup_k_pct_vs_lhp"] = offense_meta.get("lineup_k_pct_vs_lhp")
                    row["lineup_k_pct_vs_rhp"] = offense_meta.get("lineup_k_pct_vs_rhp")
                    row["lineup_k_pct_vs_hand"] = offense_meta.get("lineup_k_pct_vs_hand")
                    row["lineup_k_vs_hand_side"] = offense_meta.get(
                        "lineup_k_vs_hand_side"
                    )
                    row["lineup_k_vs_hand_pa"] = offense_meta.get("lineup_k_vs_hand_pa")
                    row["lineup_k_vs_hand_n"] = offense_meta.get("lineup_k_vs_hand_n")
                    row["lineup_k_vs_hand_source"] = offense_meta.get(
                        "lineup_k_vs_hand_source"
                    )
                    row["lineup_avg"] = offense_meta.get("lineup_avg")
                    row["lineup_bb_pct"] = offense_meta.get("lineup_bb_pct")
                    row["lineup_bip_pct"] = offense_meta.get("lineup_bip_pct")
                    row["lineup_woba"] = offense_meta.get("lineup_woba")
                    row["lineup_wrc_plus"] = offense_meta.get("lineup_wrc_plus")
                    row["lineup_iso"] = offense_meta.get("lineup_iso")
                    row["lineup_quality_n"] = offense_meta.get("lineup_quality_n")
                    row["lineup_quality_source"] = offense_meta.get(
                        "lineup_quality_source"
                    )
                    row["contact_grade"] = offense_meta.get("contact_grade") or ""
                    row["offense_source"] = offense_meta.get("offense_source")
                    row["discipline_grade"] = (
                        offense_meta.get("discipline_grade")
                        or row.get("discipline_grade")
                    )
                    # Discipline K haircut (BF already trimmed before the lineup walk).
                    ks_factor = row.get("discipline_ks_factor")
                    if ks_factor is None:
                        ks_factor = 1.0
                    disciplined_ks = float(offense_ks) * float(ks_factor)
                    # expected_ks_model = matchup + offense + discipline, before form
                    row["expected_ks_model"] = float(disciplined_ks)
                    blended, form_ks, form_w = apply_recent_form_overlay(
                        float(disciplined_ks), projected_ip, form
                    )
                    row["expected_ks"] = blended
                    row["form_ks"] = form_ks
                    row["form_weight"] = form_w
                    if used_statcast_mix:
                        row["arsenal_source"] = "statcast_fallback"
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

    # Pitcher-own velo/whiff ceiling (SPIKE) — before ticket outlook notes.
    out = apply_pitcher_stuff_overlay(out, savant_pitcher_stuff, hand_mixes)
    # FIP/SIERA/Stuff+/xStats + per-pitch run value — confirm-only display.
    out = apply_pitcher_advanced_metrics(
        out,
        fangraphs=fangraphs,
        savant_expected=savant_pitcher_expected,
    )
    # Tiny Exp K bump for full attack-plate stacks only; re-rank after.
    out = apply_attack_plate_stuff_bump(out)
    out = out.sort_values(
        by=["expected_ks"],
        ascending=False,
        na_position="last",
        kind="mergesort",
    ).reset_index(drop=True)
    ranks = []
    rank_i = 1
    for _, r in out.iterrows():
        if r["status"] == "ok" and pd.notna(r["expected_ks"]):
            ranks.append(rank_i)
            rank_i += 1
        else:
            ranks.append(pd.NA)
    out["rank"] = ranks

    # Soft-contact FILLER gated by opposing lineup arsenal rank on this slate.
    out = apply_ticket_outlook(out)

    # Career + recent pitcher-vs-opposing-team history (home/away in game logs).
    try:
        out = enrich_dataframe_vs_team_history(out)
    except Exception as exc:  # pragma: no cover - network / API soft-fail
        log(True, f"vs-team history skipped: {exc}")

    # Live book lines (The Odds API) — display-only; never moves expected_ks.
    if args.odds:
        markets = tuple(
            m.strip() for m in str(args.odds_markets or "").split(",") if m.strip()
        ) or DEFAULT_MARKETS
        key = resolve_api_key(args.odds_key)
        if not key:
            log(
                True,
                "Odds skipped: set ODDS_API_KEY_NEW / ODDS_API_KEY / "
                "THE_ODDS_API_KEY (or pass --odds-key)",
            )
        else:
            if args.odds_daily_budget is not None:
                os.environ["ODDS_DAILY_BUDGET"] = str(int(args.odds_daily_budget))
            try:
                out = enrich_dataframe_odds(
                    out,
                    api_key=key,
                    markets=markets,
                    slate_date=str(args.date or game_date),
                    skip_finished=not bool(args.odds_include_finished),
                    force_refresh=bool(args.odds_force),
                    verbose=args.verbose,
                )
            except Exception as exc:  # pragma: no cover
                log(True, f"Odds enrich failed: {exc}")
    else:
        log(args.verbose, "Odds skipped (--no-odds)")

    print(format_table(out))
    # Live K lines vs Exp K (when odds joined).
    if "k_line" in out.columns and out["k_line"].notna().any():
        print("\nBook K lines (Odds API — display only)")
        shown = out[out["k_line"].notna()].sort_values(
            "k_edge", ascending=False, na_position="last"
        )
        for _, r in shown.iterrows():
            edge = r.get("k_edge")
            edge_s = (
                f"{float(edge):+.2f}"
                if edge is not None and not (isinstance(edge, float) and pd.isna(edge))
                else "—"
            )
            print(
                f"  {r.get('pitcher')}: Exp {float(r['expected_ks']):.2f} vs "
                f"O/U {float(r['k_line']):.1f} "
                f"({format_american(r.get('k_over_price'))}/"
                f"{format_american(r.get('k_under_price'))} "
                f"{r.get('k_book') or '?'}) · edge {edge_s}"
            )
    # Print ticket outlook for flagged arms (FILLER / MATCHUP_OK / SPIKE /
    # THIN_TOTAL / UNDER_OK).
    flagged = out[out["ticket_outlook"].astype(str).str.len() > 0]
    if not flagged.empty:
        print("\nTicket outlook (profile / SPIKE / total-trust / under-confirm)")
        for _, r in flagged.iterrows():
            print(
                f"  {r.get('ticket_outlook'):<11} {r.get('pitcher')}: "
                f"{r.get('ticket_note')}"
            )
    # Stuff / SPIKE watch + attack-plate bumps (tiny Exp K only on full stacks).
    if "spike_risk" in out.columns:
        spikes = out[out["status"].eq("ok") & out["spike_risk"].astype(bool)]
        if not spikes.empty:
            print("\nSPIKE / stuff ceiling watch (no soft U6)")
            for _, r in spikes.iterrows():
                wh = r.get("stuff_whiff_pct")
                velo = r.get("stuff_fb_velo")
                wh_s = "" if wh is None or pd.isna(wh) else f"{float(wh):.1f}%"
                velo_s = (
                    ""
                    if velo is None or pd.isna(velo)
                    else f"{r.get('stuff_fb_pitch') or 'FB'} {float(velo):.1f}"
                )
                print(
                    f"  {r.get('pitcher')}: solo={r.get('arsenal_abs_grade')} "
                    f"stuff={r.get('stuff_grade') or '?'} whiff {wh_s} "
                    f"{velo_s} · {r.get('spike_flags')}"
                )
    if "stuff_ceiling_bump" in out.columns:
        bumped = out[
            out["status"].eq("ok")
            & out["stuff_ceiling_bump"].fillna(0).astype(float).gt(0)
        ]
        if not bumped.empty:
            print("\nAttack-plate stuff bump (capped Exp K add)")
            for _, r in bumped.iterrows():
                print(
                    f"  {r.get('pitcher')}: +{float(r.get('stuff_ceiling_bump')):.2f} "
                    f"→ Exp K {float(r.get('expected_ks')):.2f} · "
                    f"{r.get('stuff_ceiling_note')}"
                )
    # Discipline / pitch-count watch list.
    if "discipline_grade" in out.columns:
        watch = out[
            out["status"].eq("ok")
            & out["discipline_grade"].isin(["patient", "three_true"])
        ]
        if not watch.empty:
            print("\nPlate discipline watch (patient / walk-heavy lineups)")
            for _, r in watch.iterrows():
                bb = r.get("lineup_bb_pct")
                bb_s = "" if bb is None or pd.isna(bb) else f"{float(bb):.1f}"
                print(
                    f"  {r.get('discipline_grade'):<11} vs {r.get('opponent')}: "
                    f"{r.get('pitcher')} · opp BB% {bb_s} · "
                    f"pitch-count {r.get('pitch_count_risk')} · "
                    f"bf×{r.get('discipline_bf_factor')} ks×{r.get('discipline_ks_factor')}"
                )
    # Contact / BIP environment (high BIP trims Exp K; whiff-prone boosts).
    if "contact_grade" in out.columns:
        contact = out[
            out["status"].eq("ok")
            & out["contact_grade"].isin(["contact_heavy", "whiff_prone"])
        ]
        if not contact.empty:
            print("\nLineup contact / BIP watch")
            for _, r in contact.sort_values("lineup_bip_pct", ascending=False).iterrows():
                bip = r.get("lineup_bip_pct")
                kk = r.get("lineup_k_pct")
                bip_s = "" if bip is None or pd.isna(bip) else f"{float(bip):.1f}%"
                kk_s = "" if kk is None or pd.isna(kk) else f"{float(kk):.1f}%"
                off = r.get("offense_factor")
                off_s = "" if off is None or pd.isna(off) else f"off×{float(off):.3f}"
                print(
                    f"  {r.get('contact_grade'):<14} vs {r.get('opponent')}: "
                    f"{r.get('pitcher')} · BIP {bip_s} · opp K% {kk_s} · {off_s}"
                )
    # Pitcher out-getting style (K-first vs GB/fly contact outs) — confirmation only.
    if "pitcher_style" in out.columns:
        styles = out[
            out["status"].eq("ok")
            & out["pitcher_style"].astype(str).str.len().gt(0)
        ]
        if not styles.empty:
            print("\nPitcher style (outs via Ks vs GB / fly-popup)")
            order = {"whiff": 0, "contact_gb": 1, "fly_popup": 2, "balanced": 3}
            styles = styles.copy()
            styles["_style_ord"] = styles["pitcher_style"].map(
                lambda s: order.get(str(s), 9)
            )
            for _, r in styles.sort_values(
                ["_style_ord", "expected_ks"], ascending=[True, False]
            ).iterrows():
                pk = r.get("pitcher_k_pct")
                gb = r.get("pitcher_gb_pct")
                fb = r.get("pitcher_fb_pct")
                iff = r.get("pitcher_iffb_pct")
                con = r.get("pitcher_contact_pct")
                bits = []
                if pk is not None and not (isinstance(pk, float) and pd.isna(pk)):
                    bits.append(f"K% {float(pk):.1f}")
                if con is not None and not (isinstance(con, float) and pd.isna(con)):
                    bits.append(f"Con% {float(con):.1f}")
                if gb is not None and not (isinstance(gb, float) and pd.isna(gb)):
                    bits.append(f"GB% {float(gb):.1f}")
                if fb is not None and not (isinstance(fb, float) and pd.isna(fb)):
                    bits.append(f"FB% {float(fb):.1f}")
                if iff is not None and not (isinstance(iff, float) and pd.isna(iff)):
                    bits.append(f"IFFB% {float(iff):.1f}")
                print(
                    f"  {str(r.get('pitcher_style') or ''):<11} {r.get('pitcher')}: "
                    f"{' · '.join(bits) or (r.get('pitcher_style_flags') or '')}"
                )
    if args.detail:
        print()
        for _, r in out.iterrows():
            if r.get("status") != "ok":
                continue
            block = format_batter_detail(r.to_dict())
            if block:
                print(block)
            hist = format_vs_team_console(r.to_dict())
            if hist:
                print(hist)

    hits_rows = build_hits_board(out.to_dict(orient="records"))
    if hits_rows:
        print("\nHits board (display-only; does not affect expected_ks)")
        print(
            f"{'rk':>3} {'batter':22} {'vs':3} {'pitcher':18} "
            f"{'hits':>5} {'hrbi':>5} {'avgH':>5} {'brl':>5} {'hh':>5}"
        )
        for r in hits_rows[:8]:
            avg_s = (
                ""
                if r.get("avg_vs_hand") is None
                else f"{float(r['avg_vs_hand']):.3f}"
            )
            brl_s = (
                ""
                if r.get("barrel_pct") is None
                else f"{float(r['barrel_pct']):.1f}"
            )
            hh_s = (
                ""
                if r.get("hard_hit_pct") is None
                else f"{float(r['hard_hit_pct']):.1f}"
            )
            print(
                f"{r['rank']:>3} {str(r.get('batter') or '')[:22]:22} "
                f"{str(r.get('pitch_hand') or '?'):>3} "
                f"{str(r.get('pitcher') or '')[:18]:18} "
                f"{float(r['hits_score']):5.1f} "
                f"{float(r['hr_rbi_score'] or 0):5.1f} "
                f"{avg_s:>5} {brl_s:>5} {hh_s:>5}"
            )

    if args.output:
        # Drop nested objects from CSV (kept in HTML JSON payload).
        csv_out = out.drop(
            columns=[
                "batter_detail",
                "arsenal",
                "pitch_lineup_avg",
                "vs_team_games_detail",
            ],
            errors="ignore",
        )
        csv_out.to_csv(args.output, index=False)
        log(True, f"Wrote {args.output}")

    hits_path = args.hits_output
    if hits_path is None and args.output:
        out_p = Path(args.output)
        name = out_p.name
        if name.startswith("rankings-") and name.endswith(".csv"):
            hits_path = str(out_p.with_name("hits-" + name[len("rankings-") :]))
        else:
            hits_path = str(out_p.with_name(out_p.stem + "-hits.csv"))
    if hits_path and hits_rows:
        pd.DataFrame(hits_rows).to_csv(hits_path, index=False)
        log(True, f"Wrote {hits_path}")

    if args.html:
        write_interactive_html(
            args.html,
            out,
            game_date=game_date,
            batters_faced=args.batters_faced,
            hits_board=hits_rows,
        )
        log(True, f"Wrote {args.html}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
