# K-matchup

MLB starter strikeout matchup board — arsenal-weighted K projections vs the opposing lineup.

## Live board (bookmark this)

https://cdn.statically.io/gh/Ceezwrld/K-matchup/main/index.html

Interactive HTML with tabs. Same URL every day — do **not** use jsDelivr or old commit / htmlpreview links.

See [BOARD.md](BOARD.md) and [backtest-lessons.md](backtest-lessons.md).

## CLI

```bash
python3 mlb-k-matchups/k_matchups.py \
  --date YYYY-MM-DD \
  -o rankings-YYYY-MM-DD.csv \
  --html rankings.html \
  --hits-output hits-YYYY-MM-DD.csv
```
