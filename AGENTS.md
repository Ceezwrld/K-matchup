# AGENTS.md

## Cursor Cloud specific instructions

### What this repo is
A single Python product, **K-matchup** (MLB strikeout matchup projections), living in `mlb-k-matchups/`. It is a stateless batch CLI that pulls live data over HTTP from public MLB APIs and writes a rankings CSV plus a self-contained interactive HTML board (`rankings.html` / `index.html`). There is no backend server, database, cache, or queue. Twice-daily refresh + GitHub Pages deploy are handled by workflows in `.github/workflows/`.

### Run
The update script already installs deps (`pip install -r mlb-k-matchups/requirements.txt`). To generate a board for a date:

```bash
python3 mlb-k-matchups/k_matchups.py --date "$(date -u +%F)" -o rankings.csv --html rankings.html -v
```

`--html` also writes `index.html` (the stable Pages URL). See `mlb-k-matchups/README.md` for all flags. To view the board, serve it and open in a browser (opening the file over `file://` also works since it's self-contained):

```bash
python3 -m http.server 8080   # then browse http://localhost:8080/rankings.html
```

### Non-obvious gotchas
- **Requires network access** to public MLB endpoints (`statsapi.mlb.com`, `baseballsavant.mlb.com`, `fangraphs.com`). No API keys are needed. If those hosts are unreachable, the model produces empty/partial output rather than crashing.
- **Empty-looking board is usually a filter, not a bug.** On pre-lineup days every row is `Prior`; if the board's Lineup filter is set to **Official only** it looks empty — switch to **All sources**.
- **Off-season / far-future dates** may legitimately return few or no probable starters. Use an in-season date to see a full slate.

### Lint / test / build
There is **no** lint config, no automated test suite, and no build step in this repo. Validation is manual: run the CLI, inspect the CSV, and open the HTML board. Do not expect `pytest`/`flake8`/`npm`-style commands to exist.
