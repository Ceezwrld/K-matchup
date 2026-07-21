# MLB K-Matchups

Rank starting pitchers by how vulnerable the opposing team is to strikeouts against that starter’s pitch mix.

**Score**

```
expected_k_pct = Σ (pitcher_usage_pct × opposing_team_K%_vs_that_pitch_type)
```

`vs_league_k` / `vs_league_whiff` compare that arsenal-weighted expectation to the same mix against league-average batter rates. Positive means the opponent is more K-/whiff-prone than average against that arsenal.

## Setup

```bash
pip install -r mlb-k-matchups/requirements.txt
```

## Usage

Today’s probable starters (default):

```bash
python3 mlb-k-matchups/k_matchups.py
```

Specific date + CSV export:

```bash
python3 mlb-k-matchups/k_matchups.py --date 2026-07-21 -o /tmp/rankings.csv
```

Custom matchups CSV (`pitcher,opponent[,pitcher_id,pitcher_team,game]`):

```bash
python3 mlb-k-matchups/k_matchups.py --matchups mlb-k-matchups/matchups.example.csv -v
```

Useful flags:

| Flag | Meaning |
|------|---------|
| `--year` | Savant season (default: year of `--date`, else current year) |
| `--min-pa` | Savant leaderboard PA floor (default: 50) |
| `--min-usage` | Drop pitcher pitches below this usage % (default: 5) |
| `-o/--output` | Write full rankings CSV |
| `-v/--verbose` | Log HTTP fetches |

## Data sources

- [Baseball Savant Pitch Arsenal Stats](https://baseballsavant.mlb.com/leaderboard/pitch-arsenal-stats) (pitcher + batter CSVs)
- [MLB Stats API schedule](https://statsapi.mlb.com/api/v1/schedule) with `hydrate=probablePitcher,team`

Pitchers resolve by MLBAM `player_id` first, then name (`First Last` / `Last, First`). Missing arsenals (e.g. rookies under `--min-pa`) get a clear `missing_arsenal` / `unresolved` status instead of crashing.
