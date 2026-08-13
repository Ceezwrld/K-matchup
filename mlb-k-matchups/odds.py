"""Live book lines from The Odds API (display-only — never moves expected_ks).

Env:
  ODDS_API_KEY or THE_ODDS_API_KEY — required to fetch; missing key → no-op.

Typical markets (US books):
  pitcher_strikeouts, pitcher_hits_allowed, pitcher_earned_runs,
  pitcher_walks, pitcher_outs (+ optional *_alternate).
"""

from __future__ import annotations

import os
import re
import unicodedata
from typing import Any

import pandas as pd
import requests

ODDS_API_BASE = "https://api.the-odds-api.com/v4"
SPORT_KEY = "baseball_mlb"

# Preferred books in order (first match wins when lines disagree).
DEFAULT_BOOKS = ("draftkings", "fanduel", "betmgm", "caesars", "fanatics")

DEFAULT_MARKETS = (
    "pitcher_strikeouts",
    "pitcher_hits_allowed",
    "pitcher_earned_runs",
    "pitcher_walks",
    "pitcher_outs",
)

# Odds API full team name → our board abbreviations.
TEAM_NAME_TO_ABBR: dict[str, str] = {
    "arizona diamondbacks": "AZ",
    "atlanta braves": "ATL",
    "baltimore orioles": "BAL",
    "boston red sox": "BOS",
    "chicago cubs": "CHC",
    "chicago white sox": "CWS",
    "cincinnati reds": "CIN",
    "cleveland guardians": "CLE",
    "colorado rockies": "COL",
    "detroit tigers": "DET",
    "houston astros": "HOU",
    "kansas city royals": "KC",
    "los angeles angels": "LAA",
    "los angeles dodgers": "LAD",
    "miami marlins": "MIA",
    "milwaukee brewers": "MIL",
    "minnesota twins": "MIN",
    "new york mets": "NYM",
    "new york yankees": "NYY",
    "athletics": "ATH",
    "oakland athletics": "ATH",
    "philadelphia phillies": "PHI",
    "pittsburgh pirates": "PIT",
    "san diego padres": "SD",
    "san francisco giants": "SF",
    "seattle mariners": "SEA",
    "st. louis cardinals": "STL",
    "st louis cardinals": "STL",
    "tampa bay rays": "TB",
    "texas rangers": "TEX",
    "toronto blue jays": "TOR",
    "washington nationals": "WSH",
}

MARKET_PREFIX = {
    "pitcher_strikeouts": "k",
    "pitcher_strikeouts_alternate": "k_alt",
    "pitcher_hits_allowed": "hits",
    "pitcher_hits_allowed_alternate": "hits_alt",
    "pitcher_earned_runs": "er",
    "pitcher_earned_runs_alternate": "er_alt",
    "pitcher_walks": "bb",
    "pitcher_walks_alternate": "bb_alt",
    "pitcher_outs": "outs",
    "pitcher_outs_alternate": "outs_alt",
}


def resolve_api_key(explicit: str | None = None) -> str | None:
    """Prefer an explicit key, then a replacement env, then the standard names.

    ODDS_API_KEY_NEW wins over ODDS_API_KEY so a fresh key can be used without
    waiting for the exhausted one to be removed from the environment.
    """
    raw = (explicit or "").strip() or (
        os.environ.get("ODDS_API_KEY_NEW")
        or os.environ.get("ODDS_API_KEY")
        or os.environ.get("THE_ODDS_API_KEY")
        or ""
    ).strip()
    return raw or None


def _norm_name(s: str | None) -> str:
    if not s:
        return ""
    text = unicodedata.normalize("NFKD", str(s))
    text = "".join(c for c in text if not unicodedata.combining(c))
    text = text.lower().replace(".", " ")
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    # Drop common generational suffixes for matching.
    parts = [p for p in text.split() if p not in {"jr", "sr", "ii", "iii", "iv"}]
    return " ".join(parts)


def _team_abbr(name: str | None) -> str | None:
    if not name:
        return None
    key = re.sub(r"\s+", " ", str(name).strip().lower())
    return TEAM_NAME_TO_ABBR.get(key)


def _log(verbose: bool, msg: str) -> None:
    if verbose:
        print(msg, file=__import__("sys").stderr)


def _get_json(
    path: str,
    *,
    api_key: str,
    params: dict[str, Any] | None = None,
    verbose: bool = False,
    timeout: int = 45,
) -> Any:
    url = f"{ODDS_API_BASE}{path}"
    q = dict(params or {})
    q["apiKey"] = api_key
    _log(verbose, f"GET {url} params={ {k: v for k, v in q.items() if k != 'apiKey'} }")
    resp = requests.get(url, params=q, timeout=timeout)
    remaining = resp.headers.get("x-requests-remaining")
    used = resp.headers.get("x-requests-used")
    if remaining is not None or used is not None:
        _log(verbose, f"Odds API quota used={used} remaining={remaining}")
    if resp.status_code == 401:
        raise RuntimeError("Odds API key rejected (401)")
    if resp.status_code == 429:
        raise RuntimeError("Odds API rate limit / quota exceeded (429)")
    resp.raise_for_status()
    return resp.json()


def fetch_mlb_events(api_key: str, *, verbose: bool = False) -> list[dict[str, Any]]:
    data = _get_json(
        f"/sports/{SPORT_KEY}/events",
        api_key=api_key,
        verbose=verbose,
    )
    return list(data or [])


def fetch_event_odds(
    api_key: str,
    event_id: str,
    *,
    markets: tuple[str, ...] | list[str] = DEFAULT_MARKETS,
    regions: str = "us",
    verbose: bool = False,
) -> dict[str, Any]:
    data = _get_json(
        f"/sports/{SPORT_KEY}/events/{event_id}/odds",
        api_key=api_key,
        params={
            "regions": regions,
            "markets": ",".join(markets),
            "oddsFormat": "american",
        },
        verbose=verbose,
    )
    return data or {}


def _pick_line(
    bookmakers: list[dict[str, Any]],
    market_key: str,
    player_norm: str,
    preferred_books: tuple[str, ...] | list[str],
) -> dict[str, Any] | None:
    """Return best {line, over, under, book} for one player/market."""
    # book -> (line, over_price, under_price)
    by_book: dict[str, tuple[float, int | None, int | None]] = {}
    for book in bookmakers or []:
        bkey = str(book.get("key") or "").lower()
        for market in book.get("markets") or []:
            if market.get("key") != market_key:
                continue
            over_p = under_p = None
            point = None
            for oc in market.get("outcomes") or []:
                desc = _norm_name(oc.get("description"))
                if desc != player_norm:
                    continue
                name = str(oc.get("name") or "").lower()
                pt = oc.get("point")
                price = oc.get("price")
                if pt is None:
                    continue
                try:
                    point = float(pt)
                except (TypeError, ValueError):
                    continue
                try:
                    price_i = int(price) if price is not None else None
                except (TypeError, ValueError):
                    price_i = None
                if name == "over":
                    over_p = price_i
                elif name == "under":
                    under_p = price_i
            if point is not None and (over_p is not None or under_p is not None):
                by_book[bkey] = (point, over_p, under_p)

    if not by_book:
        return None

    # Prefer listed books; else any.
    ordered = [b for b in preferred_books if b in by_book]
    if not ordered:
        ordered = sorted(by_book.keys())

    # Consensus = median of preferred books' lines; then take first book at that line.
    lines = sorted(by_book[b][0] for b in ordered)
    mid = lines[len(lines) // 2]
    for b in ordered:
        line, over_p, under_p = by_book[b]
        if line == mid:
            return {
                "line": line,
                "over_price": over_p,
                "under_price": under_p,
                "book": b,
            }
    line, over_p, under_p = by_book[ordered[0]]
    return {
        "line": line,
        "over_price": over_p,
        "under_price": under_p,
        "book": ordered[0],
    }


def _empty_odds_cols() -> dict[str, Any]:
    cols: dict[str, Any] = {
        "odds_status": "skipped_no_key",
        "odds_updated": pd.NA,
        "odds_event_id": pd.NA,
    }
    for prefix in ("k", "hits", "er", "bb", "outs"):
        cols[f"{prefix}_line"] = pd.NA
        cols[f"{prefix}_over_price"] = pd.NA
        cols[f"{prefix}_under_price"] = pd.NA
        cols[f"{prefix}_book"] = pd.NA
    cols["k_edge"] = pd.NA
    return cols


def _commence_date_ct(ev: dict[str, Any]) -> str | None:
    """YYYY-MM-DD in America/Chicago from event commence_time.

    Late CT evening games commence on the next UTC date — matching the slate
    calendar day (not UTC) keeps SEA@NYY / KC@LAD on the right card.
    """
    raw = str(ev.get("commence_time") or "").strip()
    if not raw:
        return None
    try:
        from datetime import datetime
        from zoneinfo import ZoneInfo

        if raw.endswith("Z"):
            raw = raw[:-1] + "+00:00"
        dt = datetime.fromisoformat(raw)
        if dt.tzinfo is None:
            from datetime import timezone

            dt = dt.replace(tzinfo=timezone.utc)
        return dt.astimezone(ZoneInfo("America/Chicago")).strftime("%Y-%m-%d")
    except Exception:  # noqa: BLE001
        return raw[:10] if len(raw) >= 10 else None


def _index_events_by_game(
    events: list[dict[str, Any]],
    *,
    slate_date: str | None = None,
) -> dict[str, dict[str, Any]]:
    """Map away@home (and flipped) → event.

    When the same club pair appears on multiple days (e.g. SEA@NYY tonight and
    tomorrow), prefer the event whose commence_time **CT calendar date** matches
    ``slate_date`` (YYYY-MM-DD). Falls back to the soonest commence_time.
    """
    buckets: dict[str, list[dict[str, Any]]] = {}
    for ev in events:
        away = _team_abbr(ev.get("away_team"))
        home = _team_abbr(ev.get("home_team"))
        if not away or not home:
            continue
        for key in (f"{away}@{home}", f"{home}@{away}"):
            buckets.setdefault(key, []).append(ev)

    target = (slate_date or "").strip()[:10] or None
    event_by_game: dict[str, dict[str, Any]] = {}
    for key, evs in buckets.items():
        # Dedupe by event id while preserving order.
        seen: set[str] = set()
        uniq: list[dict[str, Any]] = []
        for ev in evs:
            eid = str(ev.get("id") or "")
            if not eid or eid in seen:
                continue
            seen.add(eid)
            uniq.append(ev)

        picked: dict[str, Any] | None = None
        if target:
            dated = [e for e in uniq if _commence_date_ct(e) == target]
            if dated:
                dated.sort(key=lambda e: str(e.get("commence_time") or ""))
                picked = dated[0]
        if picked is None:
            uniq.sort(key=lambda e: str(e.get("commence_time") or ""))
            picked = uniq[0] if uniq else None
        if picked is not None:
            event_by_game[key] = picked
    return event_by_game


def enrich_dataframe_odds(
    df: pd.DataFrame,
    *,
    api_key: str | None = None,
    markets: tuple[str, ...] | list[str] = DEFAULT_MARKETS,
    books: tuple[str, ...] | list[str] = DEFAULT_BOOKS,
    regions: str = "us",
    slate_date: str | None = None,
    verbose: bool = False,
) -> pd.DataFrame:
    """Join live prop lines onto the rankings frame. Never modifies expected_ks."""
    out = df.copy()
    base = _empty_odds_cols()
    for col, val in base.items():
        if col not in out.columns:
            out[col] = val

    key = resolve_api_key(api_key)
    if not key:
        _log(verbose, "Odds: no ODDS_API_KEY / THE_ODDS_API_KEY — skipping")
        out["odds_status"] = "skipped_no_key"
        return out

    if out.empty:
        out["odds_status"] = "no_rows"
        return out

    try:
        events = fetch_mlb_events(key, verbose=verbose)
    except Exception as exc:  # noqa: BLE001 — board should still publish
        _log(verbose, f"Odds: events fetch failed: {exc}")
        out["odds_status"] = f"error:{exc}"
        return out

    # Infer slate date from rows when not passed (game_time_utc / explicit).
    if not slate_date and "game_time_utc" in out.columns:
        for raw in out["game_time_utc"].dropna().astype(str):
            if len(raw) >= 10 and raw[4] == "-":
                slate_date = raw[:10]
                break

    event_by_game = _index_events_by_game(events, slate_date=slate_date)
    if verbose and slate_date:
        _log(verbose, f"Odds: slate_date={slate_date} indexed {len(event_by_game)} game keys")

    # Unique slate games → fetch odds once each.
    games = sorted(
        {
            str(g).strip()
            for g in out.get("game", pd.Series(dtype=str)).dropna().unique()
            if str(g).strip()
        }
    )
    odds_by_event: dict[str, dict[str, Any]] = {}
    for game in games:
        ev = event_by_game.get(game)
        if not ev:
            # Try rebuild from pitcher_team/opponent if game missing.
            continue
        eid = str(ev.get("id") or "")
        if not eid or eid in odds_by_event:
            continue
        try:
            odds_by_event[eid] = fetch_event_odds(
                key,
                eid,
                markets=markets,
                regions=regions,
                verbose=verbose,
            )
        except Exception as exc:  # noqa: BLE001
            _log(verbose, f"Odds: event {eid} ({game}) failed: {exc}")
            odds_by_event[eid] = {"_error": str(exc)}

    # Also map via team pairs from pitcher_team + opponent when game string absent.
    matched = 0
    for idx, row in out.iterrows():
        game = str(row.get("game") or "").strip()
        p_team = str(row.get("pitcher_team") or "").strip().upper()
        opp = str(row.get("opponent") or "").strip().upper()
        ev = event_by_game.get(game)
        if ev is None and p_team and opp:
            ev = event_by_game.get(f"{p_team}@{opp}") or event_by_game.get(
                f"{opp}@{p_team}"
            )
        if ev is None:
            out.at[idx, "odds_status"] = "no_event"
            continue
        eid = str(ev.get("id") or "")
        payload = odds_by_event.get(eid) or {}
        if payload.get("_error"):
            out.at[idx, "odds_status"] = f"error:{payload['_error']}"
            continue
        out.at[idx, "odds_event_id"] = eid
        books_payload = payload.get("bookmakers") or []
        updated = None
        for b in books_payload:
            for m in b.get("markets") or []:
                updated = m.get("last_update") or updated
        out.at[idx, "odds_updated"] = updated

        player = _norm_name(row.get("pitcher"))
        got_any = False
        for market in markets:
            if "_alternate" in market:
                continue  # primary lines only in this scaffold
            prefix = MARKET_PREFIX.get(market)
            if prefix not in {"k", "hits", "er", "bb", "outs"}:
                continue
            pick = _pick_line(books_payload, market, player, books)
            if not pick:
                continue
            got_any = True
            out.at[idx, f"{prefix}_line"] = pick["line"]
            out.at[idx, f"{prefix}_over_price"] = pick["over_price"]
            out.at[idx, f"{prefix}_under_price"] = pick["under_price"]
            out.at[idx, f"{prefix}_book"] = pick["book"]

        # k_edge = Exp K − line (positive → model higher than book → over lean cue)
        exp = row.get("expected_ks")
        k_line = out.at[idx, "k_line"]
        exp_ok = exp is not None and not pd.isna(exp)
        line_ok = k_line is not None and not pd.isna(k_line)
        if exp_ok and line_ok:
            out.at[idx, "k_edge"] = float(exp) - float(k_line)
        else:
            out.at[idx, "k_edge"] = pd.NA

        out.at[idx, "odds_status"] = "ok" if got_any else "no_player_props"
        if got_any:
            matched += 1

    _log(verbose, f"Odds: matched props for {matched}/{len(out)} pitchers")
    return out


def format_american(price: Any) -> str:
    if price is None or (isinstance(price, float) and pd.isna(price)):
        return "—"
    try:
        p = int(price)
    except (TypeError, ValueError):
        return "—"
    return f"+{p}" if p > 0 else str(p)
