# K-matchup guardrails (read before any change)

This repo is also maintained from Claude. The 2026-10-28 upgrades below are
validated against graded history and must not be lost.

## Always
1. **Start every session with `git pull origin main`.** Never edit, run, or
   commit from a stale checkout — your local copy may predate these features.
2. **Never force-push** (`git push --force` / `--force-with-lease`), and never
   reset, rebase, or rewrite `main` history. If a push is rejected, pull and
   merge; on conflicts keep the incoming `main` version of protected code.
3. **Do not publish the board from a local run.** GitHub Actions
   (`.github/workflows/daily-rankings.yml`) regrades history and publishes
   `rankings.html` / `index.html` / CSVs twice a day. Only run the model locally
   to inspect output; if you must publish, pull first and use the current code.
4. Changes are **additive**. Ask the user before removing, renaming, or
   replacing any protected feature below.

## Protected — do not delete, revert, or rewrite
- `mlb-k-matchups/zones.py` — strike-zone heatmaps + zone fit
- `mlb-k-matchups/k_probs.py` — K ladder (P(K ≥ N), tag-adjusted)
- `mlb-k-matchups/hit_probs.py` — 1+H / 2+H / H+R+RBI / RBI chances
- `mlb-k-matchups/grade_history.py`, `mlb-k-matchups/grade_hits.py` — graders
- `mlb-k-matchups/prior_season.py` — last-season blending (needed on Opening Day)
- `k-calibration.json`, `hits-calibration.json`, `graded-history.csv`,
  `graded-hits-history.csv` — written by the graders; never hand-edit
- In `rankings_html.py`: the **Strike zone** tab, the **K ladder**, the Hits
  board probability columns and its sort by 1+ hit chance
- In `sharpen.py`: `STATCAST_FRAMES` / `_remember_frame`, and the
  `build_hits_board` sort by `p_h1` (the old `hits_score` order backtested
  worse than random — do not switch back)
- In `k_matchups.py`: the `enrich_lineup_zones`, `apply_k_probs`, and
  `enrich_board_hit_probs` calls
- The no-game-day check and grading steps in `.github/workflows/daily-rankings.yml`

## Before committing any model change
Run `python3 mlb-k-matchups/k_matchups.py --date YYYY-MM-DD -o /tmp/r.csv --html /tmp/r.html`
and confirm the HTML still contains the Strike zone tab, the K ladder, and the
Hits board % columns. Never commit `rankings.html` from that test run.
