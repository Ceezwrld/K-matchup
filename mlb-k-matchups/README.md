# MLB K-Matchups

Rank starting pitchers by **expected strikeouts against the opposing starting lineup**, using each batter’s vulnerability to that starter’s pitch mix.

**Score (per batter)**

```
batter_k_pct = Σ (pitcher_usage_pct × that_batter_K%_vs_that_pitch_type)
```

**Lineup rollup**

```
expected_k_pct = mean(batter_k_pct over lineup batters with Savant rates)
expected_ks    = expected_k_pct / 100 × batters_faced   # default batters_faced=22
expected_ks_1x = Σ batter_k_pct / 100                   # one time through the order
```

No league-average blending: rates come only from the opposing lineup’s batters.

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
python3 mlb-k-matchups/k_matchups.py --date $(date +%F) -o /tmp/rankings.csv
```

Custom matchups CSV (`pitcher,opponent[,pitcher_id,pitcher_team,game]`). Opponent lineup is resolved from the most recent posted starting nine for that team:

```bash
python3 mlb-k-matchups/k_matchups.py --matchups mlb-k-matchups/matchups.example.csv -v
```

Useful flags:

| Flag | Meaning |
|------|---------|
| `--year` | Savant season (default: year of `--date`, else current year) |
| `--min-pa` | Savant leaderboard PA floor (default: 50) |
| `--min-usage` | Drop pitcher pitches below this usage % (default: 5) |
| `--batters-faced` | Assumed BF for `expected_ks` (default: 22) |
| `--lineup-lookback` | Days to search for a prior lineup if today’s isn’t posted (default: 14) |
| `--require-official-lineup` | Skip games without an official lineup for the date |
| `-o/--output` | Write full rankings CSV |
| `-v/--verbose` | Log HTTP fetches |

## Lineups

- Prefer the **official starting lineup** from the MLB Stats API (`hydrate=lineups`) when posted.
- If not posted yet (common earlier in the day), fall back to that team’s **most recent prior starting nine** (`lineup_source=prior:YYYY-MM-DD`).
- Batters without Savant arsenal rows (below `--min-pa`) are excluded from the mean and listed in `missing_batters`; `lineup_coverage` shows how many of the nine were scored. There is **no** league-average fill-in.

## Data sources

- [Baseball Savant Pitch Arsenal Stats](https://baseballsavant.mlb.com/leaderboard/pitch-arsenal-stats) (pitcher + batter CSVs)
- [MLB Stats API schedule](https://statsapi.mlb.com/api/v1/schedule) with `hydrate=probablePitcher,team,lineups`

Pitchers resolve by MLBAM `player_id` first, then name (`First Last` / `Last, First`). Missing arsenals get `missing_arsenal` / `unresolved` instead of crashing.
