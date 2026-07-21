# MLB K-Matchups

Rank starting pitchers by **expected strikeouts against the opposing starting lineup**, using each batter’s vulnerability to that starter’s pitch mix over a projected full outing (innings / times through the order).

**Score (per batter)**

```
batter_k_pct = Σ (pitcher_usage_pct × that_batter_K%_vs_that_pitch_type)
```

**Outing length**

```
projected_ip = season_IP / games_started          # per starter (Stats API)
projected_bf = season_BF / games_started          # batters faced per start
times_through_order = projected_bf / 9
```

Fallbacks: `--ip` / `--batters-faced` overrides, else `5.5 IP × 4.25 BF/IP`.

**Lineup rollup**

```
expected_k_pct = mean(batter_k_pct over lineup batters with Savant rates)
expected_ks    = Σ batter_k_pct/100 while walking the batting order for projected_bf
expected_ks_1x = Σ batter_k_pct/100 for one trip through the nine (reference only)
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

Specific date + CSV + interactive HTML:

```bash
python3 mlb-k-matchups/k_matchups.py --date $(date +%F) \
  -o rankings.csv --html rankings.html
```

Open `rankings.html` in a browser. Re-run the same command after lineups post — official nines replace prior-day fallbacks automatically.

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
| `--ip` | Force the same projected IP for every starter |
| `--batters-faced` | Force a fixed BF for every starter (skips season BF/GS) |
| `--lineup-lookback` | Days to search for a prior lineup if today’s isn’t posted (default: 14) |
| `--require-official-lineup` | Skip games without an official lineup for the date |
| `--detail` | Print each lineup batter’s arsenal-weighted K% |
| `-o/--output` | Write full rankings CSV |
| `--html` | Write self-contained interactive HTML rankings |
| `-v/--verbose` | Log HTTP fetches |

## Lineups

- Prefer the **official starting lineup** from the MLB Stats API (`hydrate=lineups`) when posted.
- If not posted yet (common earlier in the day), fall back to that team’s **most recent prior starting nine** (`lineup_source=prior:YYYY-MM-DD`).
- Batters without Savant arsenal rows (below `--min-pa`) are excluded from the mean and listed in `missing_batters`; `lineup_coverage` shows how many of the nine were scored. There is **no** league-average fill-in.

## Data sources

- [Baseball Savant Pitch Arsenal Stats](https://baseballsavant.mlb.com/leaderboard/pitch-arsenal-stats) (pitcher + batter CSVs)
- [MLB Stats API schedule](https://statsapi.mlb.com/api/v1/schedule) with `hydrate=probablePitcher,team,lineups`
- [MLB Stats API people](https://statsapi.mlb.com/api/v1/people) season pitching splits for IP / BF per start

Pitchers resolve by MLBAM `player_id` first, then name (`First Last` / `Last, First`). Missing arsenals get `missing_arsenal` / `unresolved` instead of crashing.
