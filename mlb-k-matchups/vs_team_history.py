"""Pitcher vs opposing batting-team history from MLB Stats API.

Career totals (vsTeamTotal) plus recent game logs with home/away for the
pitcher, used as a secondary confirmation layer next to arsenal matchup rank.
"""

from __future__ import annotations

from typing import Any

import pandas as pd
import requests

PEOPLE_STATS_URL = "https://statsapi.mlb.com/api/v1/people/{pid}/stats"
USER_AGENT = (
    "mlb-k-matchups/1.0 (+https://github.com; research; contact: local-cli)"
)

# Stats API team ids keyed by our normalized abbreviations.
TEAM_IDS: dict[str, int] = {
    "AZ": 109,
    "ATL": 144,
    "BAL": 110,
    "BOS": 111,
    "CHC": 112,
    "CWS": 145,
    "CIN": 113,
    "CLE": 114,
    "COL": 115,
    "DET": 116,
    "HOU": 117,
    "KC": 118,
    "LAA": 108,
    "LAD": 119,
    "MIA": 146,
    "MIL": 158,
    "MIN": 142,
    "NYM": 121,
    "NYY": 147,
    "ATH": 133,
    "PHI": 143,
    "PIT": 134,
    "SD": 135,
    "SF": 137,
    "SEA": 136,
    "STL": 138,
    "TB": 139,
    "TEX": 140,
    "TOR": 141,
    "WSH": 120,
}


def _session() -> requests.Session:
    s = requests.Session()
    s.headers.update({"User-Agent": USER_AGENT, "Accept": "application/json"})
    return s


def fetch_vs_team_total(
    pitcher_id: int | str,
    opponent_abbr: str,
    *,
    session: requests.Session | None = None,
) -> dict[str, Any] | None:
    """Career regular-season pitching totals for pitcher vs opposing team."""
    opp_id = TEAM_IDS.get(str(opponent_abbr or "").upper())
    if not opp_id or pitcher_id is None or (isinstance(pitcher_id, float) and pd.isna(pitcher_id)):
        return None
    sess = session or _session()
    r = sess.get(
        PEOPLE_STATS_URL.format(pid=int(pitcher_id)),
        params={
            "stats": "vsTeamTotal",
            "group": "pitching",
            "opposingTeamId": opp_id,
        },
        timeout=30,
    )
    r.raise_for_status()
    splits = (r.json().get("stats") or [{}])[0].get("splits") or []
    if not splits:
        return None
    st = splits[0].get("stat") or {}
    pa = float(st.get("plateAppearances") or 0)
    ks = float(st.get("strikeOuts") or 0)
    return {
        "vs_team_games": int(st.get("gamesPlayed") or 0),
        "vs_team_ks": int(ks),
        "vs_team_pa": int(pa),
        "vs_team_bb": int(st.get("baseOnBalls") or 0),
        "vs_team_hr": int(st.get("homeRuns") or 0),
        "vs_team_hits": int(st.get("hits") or 0),
        "vs_team_avg": st.get("avg"),
        "vs_team_ops": st.get("ops"),
        "vs_team_k_pct": (100.0 * ks / pa) if pa else None,
    }


def fetch_game_logs_vs_team(
    pitcher_id: int | str,
    opponent_abbr: str,
    *,
    seasons: tuple[int, ...] = (2023, 2024, 2025, 2026),
    session: requests.Session | None = None,
) -> list[dict[str, Any]]:
    """Game-by-game pitching lines vs opponent, with pitcher home/away."""
    opp_id = TEAM_IDS.get(str(opponent_abbr or "").upper())
    if not opp_id or pitcher_id is None or (isinstance(pitcher_id, float) and pd.isna(pitcher_id)):
        return []
    sess = session or _session()
    games: list[dict[str, Any]] = []
    for season in seasons:
        r = sess.get(
            PEOPLE_STATS_URL.format(pid=int(pitcher_id)),
            params={
                "stats": "gameLog",
                "group": "pitching",
                "season": season,
                "sportId": 1,
            },
            timeout=30,
        )
        if not r.ok:
            continue
        for sp in (r.json().get("stats") or [{}])[0].get("splits") or []:
            opp = sp.get("opponent") or {}
            if opp.get("id") != opp_id:
                continue
            st = sp.get("stat") or {}
            is_home = bool(sp.get("isHome"))
            games.append(
                {
                    "date": sp.get("date"),
                    "season": season,
                    "site": "H" if is_home else "A",
                    "is_home": is_home,
                    "games_started": int(st.get("gamesStarted") or 0),
                    "ip": st.get("inningsPitched"),
                    "ks": int(st.get("strikeOuts") or 0),
                    "bb": int(st.get("baseOnBalls") or 0),
                    "hits": int(st.get("hits") or 0),
                    "er": int(st.get("earnedRuns") or 0),
                    "hr": int(st.get("homeRuns") or 0),
                    "bf": int(st.get("battersFaced") or 0),
                }
            )
    games.sort(key=lambda g: g.get("date") or "", reverse=True)
    return games


def _site_split(games: list[dict[str, Any]]) -> dict[str, Any]:
    home = [g for g in games if g.get("is_home")]
    away = [g for g in games if not g.get("is_home")]

    def pack(subset: list[dict[str, Any]]) -> dict[str, Any]:
        return {
            "g": len(subset),
            "ks": sum(int(g.get("ks") or 0) for g in subset),
            "avg_ks": (
                sum(int(g.get("ks") or 0) for g in subset) / len(subset)
                if subset
                else None
            ),
        }

    return {"home": pack(home), "away": pack(away)}


def summarize_vs_team_history(
    pitcher_id: int | str,
    opponent_abbr: str,
    *,
    recent_n: int = 8,
    seasons: tuple[int, ...] = (2023, 2024, 2025, 2026),
    session: requests.Session | None = None,
) -> dict[str, Any]:
    """Combine career vs-team totals + recent H/A game log for one matchup."""
    sess = session or _session()
    career = fetch_vs_team_total(pitcher_id, opponent_abbr, session=sess) or {}
    games = fetch_game_logs_vs_team(
        pitcher_id, opponent_abbr, seasons=seasons, session=sess
    )
    recent = games[:recent_n]
    split = _site_split(games)
    recent_bits = []
    for g in recent:
        recent_bits.append(
            f"{g.get('date')} {g.get('site')}: {g.get('ip')}IP {g.get('ks')}K"
        )
    out: dict[str, Any] = {
        **career,
        "vs_team_home_g": split["home"]["g"],
        "vs_team_home_ks": split["home"]["ks"],
        "vs_team_home_avg_ks": split["home"]["avg_ks"],
        "vs_team_away_g": split["away"]["g"],
        "vs_team_away_ks": split["away"]["ks"],
        "vs_team_away_avg_ks": split["away"]["avg_ks"],
        "vs_team_recent": "; ".join(recent_bits),
        "vs_team_games_detail": recent,
    }
    return out


def enrich_dataframe_vs_team_history(
    df: pd.DataFrame,
    *,
    recent_n: int = 8,
    seasons: tuple[int, ...] = (2023, 2024, 2025, 2026),
) -> pd.DataFrame:
    """Attach vs-team history columns to a rankings DataFrame."""
    if df.empty:
        return df
    sess = _session()
    records: list[dict[str, Any]] = []
    for _, row in df.iterrows():
        try:
            hist = summarize_vs_team_history(
                row.get("pitcher_id"),
                row.get("opponent"),
                recent_n=recent_n,
                seasons=seasons,
                session=sess,
            )
        except Exception:
            hist = {"vs_team_games_detail": []}
        records.append(hist)
    hist_df = pd.DataFrame(records)
    out = df.copy().reset_index(drop=True)
    for col in hist_df.columns:
        out[col] = hist_df[col]
    return out


def format_vs_team_console(row: dict[str, Any]) -> str:
    """One-line + recent H/A lines for --detail output."""
    opp = row.get("opponent") or "?"
    g = row.get("vs_team_games")
    if g is None or (isinstance(g, float) and pd.isna(g)) or int(g or 0) == 0:
        detail = row.get("vs_team_games_detail") or []
        if not detail:
            return f"  vs {opp} history: none"
    k_pct = row.get("vs_team_k_pct")
    k_pct_s = "" if k_pct is None or (isinstance(k_pct, float) and pd.isna(k_pct)) else f"{float(k_pct):.1f}%"
    lines = [
        f"  vs {opp} career: {int(row.get('vs_team_games') or 0)} G · "
        f"{int(row.get('vs_team_ks') or 0)} K / {int(row.get('vs_team_pa') or 0)} PA"
        f"{'' if not k_pct_s else ' · K% ' + k_pct_s} · "
        f"AVG {row.get('vs_team_avg') or '—'} · OPS {row.get('vs_team_ops') or '—'}"
    ]
    hg = int(row.get("vs_team_home_g") or 0)
    ag = int(row.get("vs_team_away_g") or 0)
    if hg or ag:
        h_avg = row.get("vs_team_home_avg_ks")
        a_avg = row.get("vs_team_away_avg_ks")
        h_s = "—" if h_avg is None else f"{float(h_avg):.1f} K/G"
        a_s = "—" if a_avg is None else f"{float(a_avg):.1f} K/G"
        lines.append(
            f"    site split (game logs): HOME {hg} G · {int(row.get('vs_team_home_ks') or 0)} K ({h_s}) · "
            f"AWAY {ag} G · {int(row.get('vs_team_away_ks') or 0)} K ({a_s})"
        )
    for g in (row.get("vs_team_games_detail") or [])[:6]:
        site = g.get("site") or ("H" if g.get("is_home") else "A")
        site_word = "HOME" if site == "H" else "AWAY"
        lines.append(
            f"    {g.get('date')} {site_word}: {g.get('ip')} IP · {g.get('ks')} K · "
            f"{g.get('bb')} BB · {g.get('hits')} H · {g.get('er')} ER · BF {g.get('bf')}"
        )
    return "\n".join(lines)
