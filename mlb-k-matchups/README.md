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
Thin samples (`GS < 5`) shrink toward that default; uncapped season averages are limited to **7.0 IP / 30 BF** so projections stay in a realistic starter range.

**Lineup rollup**

```
expected_k_pct = mean(batter_k_pct over lineup batters with Savant rates)
expected_ks    = Σ batter_k_pct/100 while walking the batting order for projected_bf
expected_ks_1x = Σ batter_k_pct/100 for one trip through the nine (reference only)
```

No league-average blending: rates come only from the opposing lineup’s batters.

**Sharpening layers**

1. **Pitch mix vs LHB/RHB** — Statcast pitch-level usage by batter stand; each lineup batter is scored with the mix that pitcher actually throws to that side (switch-hitters take the platoon stand).
2. **Batter K% vs pitcher hand** — Stats API `vl`/`vr` hitting splits softly adjust arsenal-weighted K% (shrunk by sample size).
3. **Recent form** — last 3 starts’ K/9 blended into `expected_ks` (~30% weight when available); `expected_ks_model` keeps the pre-form number.
4. **Outing risk** — BB/9, HR/9, xFIP (FanGraphs, Stats API fallback) → `outing_risk` flags; elevated BB/9 mildly shortens projected BF/IP for overs.

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

Open `rankings.html` in a browser (**download the file and open it locally** — GitHub’s raw view blocks scripts and may show plain text).

Interactive preview (renders in-browser):

https://htmlpreview.github.io/?https://github.com/Ceezwrld/K-matchup/blob/cursor/interactive-rankings-html-106c/rankings.html

Expand any pitcher → **Pitch weaknesses** shows each pitch (overall + vs L/R usage) and batter K%s. Re-run after lineups post to refresh.

Custom matchups CSV (`pitcher,opponent[,pitcher_id,pitcher_team,game]`). Opponent lineup is resolved from the most recent posted starting nine for that team:

```bash
python3 mlb-k-matchups/k_matchups.py --matchups mlb-k-matchups/matchups.example.csv -v
```

Useful flags:

| Flag | Meaning |
|------|---------|
| `--year` | Savant season (default: year of `--date`, else current year) |
| `--min-pa` | Savant PA floor for **pitcher** arsenal (default: 50) |
| `--min-pa-batter` | Savant PA floor for **batter** pitch K% (default: 1; lower = fuller heatmaps) |
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
- Batters without Savant arsenal rows (below `--min-pa-batter`) still appear in the heat map using **same-handed league-average K% vs that pitch** (marked `†`). There is no “copy this batter’s other pitch” fill-in.

## Data sources

- [Baseball Savant Pitch Arsenal Stats](https://baseballsavant.mlb.com/leaderboard/pitch-arsenal-stats) (pitcher + batter CSVs)
- [Baseball Savant Statcast Search](https://baseballsavant.mlb.com/statcast_search) (pitch-level mixes vs LHB/RHB)
- [MLB Stats API schedule](https://statsapi.mlb.com/api/v1/schedule) with `hydrate=probablePitcher,team,lineups`
- [MLB Stats API people](https://statsapi.mlb.com/api/v1/people) season pitching, game logs, and hitting `vl`/`vr` splits
- [FanGraphs pitching leaders](https://www.fangraphs.com/) for xFIP / BB/9 / HR/9

Pitchers resolve by MLBAM `player_id` first, then name (`First Last` / `Last, First`). Missing arsenals get `missing_arsenal` / `unresolved` instead of crashing.
