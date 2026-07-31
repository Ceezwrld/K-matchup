# K-matchup

MLB starter strikeout matchup board — arsenal-weighted K projections vs the opposing lineup.

## Live board (bookmark this)

https://raw.githack.com/Ceezwrld/K-matchup/main/index.html

Same URL every day. Refresh after lineup updates — do **not** use old commit / htmlpreview links.

Optional Pages URL (after one Settings enable): https://ceezwrld.github.io/K-matchup/

See [BOARD.md](BOARD.md) and [backtest-lessons.md](backtest-lessons.md).

## CLI

```bash
python3 mlb-k-matchups/k_matchups.py \
  --date YYYY-MM-DD \
  -o rankings-YYYY-MM-DD.csv \
  --html rankings.html \
  --hits-output hits-YYYY-MM-DD.csv
```

Writes `rankings.html` and `index.html` (stable entrypoint on `main` / `gh-pages`).
