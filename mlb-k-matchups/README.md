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

**Opener / swingman guard** — raw IP÷GS is unreliable when appearances include relief (relief IP inflates the numerator). The model:

1. Estimates start IP by backing out ~1 IP per non-start appearance
2. Labels **opener_likely** when starts are rare *and* estimated start length is short → project **1.5 IP**
3. Labels **swingman** when start share is mixed but length looks starter-ish (uses the relief-adjusted start IP)

These show as `outing_role` / `outing_source` in the CSV and HTML.

**Lineup rollup**

```
expected_k_pct = mean(batter_k_pct over lineup batters with Savant rates)
expected_ks    = Σ batter_k_pct/100 while walking the batting order for projected_bf
expected_ks_1x = Σ batter_k_pct/100 for one trip through the nine (reference only)
```

No league-average blending: rates come only from the opposing lineup’s batters.

**Sharpening layers**

1. **Pitch mix vs LHB/RHB** — Statcast pitch-level usage by batter stand; each lineup batter is scored with the mix that pitcher actually throws to that side (switch-hitters take the platoon stand).
2. **Batter pitch-type K% vs LHP/RHP** — Statcast PA-ending K% by pitch against lefties/righties (min 15 PA); falls back to overall pitch K% then league fill.
3. **Batter K% vs pitcher hand** — Stats API `vl`/`vr` hitting splits softly adjust arsenal-weighted K% when pitch×hand coverage is thin (skipped when ≥60% of usage already uses pitch×hand rates).
4. **Outing survival / early-exit** — BB/9 haircut plus short recent IP and high HR/xFIP+BB flags shrink projected BF/IP (`bf_risk_factor`, `survival_flags`).
5. **Opposing lineup offense / contact form** — lineup **K%** and **balls-in-play %** (`lineup_bip_pct` ≈ (AB−SO)/PA; prefer last ~10 games when sample is enough, else season) apply a mild ±7% overlay on matchup Ks (`offense_factor`). High-K / low-BIP (**whiff_prone**) nines nudge Exp K up; contact-heavy / high-BIP nines trim Exp K. AVG is a small secondary cue.
6. **Plate discipline / pitch counts** — lineup BB% + K% shape → `discipline_grade` (`patient`, `three_true`, `free_swing`, …). Patient/walk-heavy nines trim projected BF/IP (`discipline_bf_factor`, `pitch_count_risk`) before the order walk and mildly soften `expected_ks` (`discipline_ks_factor`).
7. **Recent form** — last 3 starts’ K/9 blended into `expected_ks` (~30% weight when available); `expected_ks_model` keeps the pre-form (post-offense/discipline) number.
8. **Outing risk** — BB/9, HR/9, xFIP (FanGraphs, Stats API fallback) → `outing_risk` flags.
9. **Ticket outlook (FILLER vs MATCHUP_OK)** — soft-contact / low-K **profile** (K9 / soft L3 / elev_xFIP) is gated by **absolute** arsenal-vs-lineup quality (`expected_k_pct` → `arsenal_abs_grade`: elite≥24 / strong≥22.5 / avg≥20 / soft&lt;20). Soft profile + avg/soft solo grade = **FILLER**; soft profile + strong/elite solo grade = **MATCHUP_OK** (disclose; O3.5 / thin O4.5 K only). Slate `#` / `matchup_grade` remain secondary “today’s relative” context. When Ks are a poor fit, notes also flag **pitcher outs** as an alt ticket lane if outing length / risk supports it.
10. **Pitcher stuff ceiling (velo / whiff by pitch)** — Savant pitcher-arsenal **whiff%** (usage-weighted) + Statcast **release velo** on the primary fastball. Surfaces as `stuff_whiff_pct` / `stuff_fb_velo` / `stuff_grade` and a **SPIKE** flag when K9≥~10 or stuff whiff is elite (or strong whiff + ≥95 mph FB). **Does not change `expected_ks`** — it blocks soft-under autopilot when the mix-vs-lineup grade is SOFT but the arm still has swing-and-miss stuff. Soft solo + SPIKE → ticket outlook **SPIKE**.
11. **Pitcher out-getting style (Ks vs BIP)** — FanGraphs season **K% / Contact% / GB% / FB% / IFFB%** (Stats API K%/GB% fallback) → `pitcher_style`: **whiff** (K-first), **contact_gb** (ground-ball / in-play outs), **fly_popup** (fly + popup), or **balanced**. Board chips `P-WHIFF` / `P-GB` / `P-FLY` / `P-BAL`. **Confirmation only — does not change `expected_ks`** (arsenal matchup already prices K upside). Use WHIFF to confirm overs / SPIKE caution on soft unders; GB/FLY styles flag pitchers who get outs on contact (soft matchup strengthens under; elite mix alone is not a nuke over without length).
12. **Total-trust gate (THIN_TOTAL)** — ELITE/STRONG with Exp K ≥ ~5.5 only fully trusts the **juiced total** when STYLE is **WHIFF**. STYLE **GB/FLY** → outlook **THIN_TOTAL** (O3.5 / thin O4.5 only). STYLE **BAL** → soft total-caution note (O4.5 floor). Mix side can still be over; the *number* is not a nuke on BIP-out styles (8/4 Dobbins). Does not change Exp K.
13. **Under confirmation (UNDER_OK)** — SOFT non-SPIKE needs ≥2 of: **GB/FLY style**, **opp contact-heavy BIP**, **Exp K ≤ ~4.2**. Passes → outlook **UNDER_OK**. Fewer confirms → weak under (U6.5+ or pass). SPIKE still vetoes soft U6.

**Hits props (separate board — does not affect `expected_ks`)**

Barrel%, hard-hit% (EV95%), xwOBA/xBA from Savant plus AVG vs pitcher hand feed `hits_score` / `hr_rbi_score` on each batter. Written to `hits-YYYY-MM-DD.csv` beside rankings and shown in the HTML Hits board / lineup panel for Hits and H+R+RBI tickets only.

If a starter is missing from the Savant arsenal board (common for returning arms below the default `min` PA filter), the model falls back to **Statcast pitch-level usage** for that pitcher instead of leaving them unscored.

## Daily automation (GitHub Actions)

After this workflow is on `main`, rankings refresh automatically **twice a day** (no Cursor tokens used):

| When (approx. ET) | Cron (UTC) | Purpose |
|-------------------|------------|---------|
| ~7:00 AM | `0 11 * * *` | Morning probable starters |
| ~4:00 PM | `0 20 * * *` | Refresh after lineups post |

It writes `rankings.html` and `rankings-YYYY-MM-DD.csv`, then commits to the default branch.

**Manual run:** GitHub → **Actions** → **Daily K-matchup rankings** → **Run workflow** (optional date).

**Note:** Scheduled workflows only run from the repo default branch (`main`). Merge the PR that adds `.github/workflows/daily-rankings.yml` first. If push is blocked, allow GitHub Actions write access under repo **Settings → Actions → General**.

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

Open `rankings.html` in a browser (**download the file and open it locally** — GitHub’s raw view serves plain text and blocks scripts).

`htmlpreview.github.io` is unreliable for this file; prefer a local open. On pre-lineup days every row is **Prior** — if the Lineup filter is set to **Official only**, the board will look empty. Use **All sources**.

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
| `--odds` / `--no-odds` | Join live book lines from The Odds API (default: on when key present) |
| `--odds-key` | Odds API key (else `ODDS_API_KEY_NEW` / `ODDS_API_KEY` / `THE_ODDS_API_KEY`) |
| `--odds-markets` | Comma-separated markets (default: **lite** = K / hits / ER = 3 credits/game) |
| `--odds-force` | Bypass on-disk cache (normally reuses pulls ~120 min) |
| `--odds-include-finished` | Also fetch props for games started >4.5h ago (default: skip) |
| `--odds-daily-budget N` | Cap estimated credits per CT day (default: 500; 0 = unlimited) |
| `-v/--verbose` | Log HTTP fetches |

## Live odds (The Odds API)

Display-only book lines join onto the board as `k_line` / `k_edge` (Exp K − line), plus hits / ER (and BB / outs when requested). **Never changes `expected_ks`.**

```bash
export ODDS_API_KEY_NEW="your_32_char_hex_key"   # preferred; else ODDS_API_KEY
python3 mlb-k-matchups/k_matchups.py --date $(date +%F) -o rankings.csv --html rankings.html -v
# model-only (0 odds credits):  ... --no-odds
```

### Stretching ~20k credits for a month

Cost model: `/events` is **free**. Each `/events/{id}/odds` costs **markets × regions**. Default is **3 markets × 1 region = 3 credits per live game**. Cache hits, stale reuse, and skipped finished games cost **0**.

**Month math (target):** 20,000 ÷ 30 ≈ **667 credits/day**. Soft cap defaults to **500/day** (`ODDS_DAILY_BUDGET`) → ~15k/month with ~5k buffer for spikes.

| Habit | Approx cost |
| --- | --- |
| Full slate lite pull (~15 live games) | ~45 credits |
| Same board again within ~120 min (cache) | ~0 |
| Over daily budget | stale cache / skip network |
| CI morning publish | **0** (`--no-odds`) |
| CI afternoon publish | ~1 lite pull |
| Local intentional Line/Edge pulls | aim **2–4 / day** |
| Full markets (K+hits+ER+BB+outs) | 5 credits/game — avoid |
| `--odds-force` every refresh | burns a full pull — avoid |

Sustainable day (~180–225 credits): morning pack + lineup lock + pre-first-pitch (3 × ~45), plus CI afternoon. That is well under the 500 cap and leaves headroom for ~30 days.

Tips:
- Put the key in `.env` as `ODDS_API_KEY_NEW=…` (gitignored). Prefer the dashboard **API Key** (32-char hex), not the account UUID.
- Refresh Savant/lineups with `--no-odds`; only pull odds when you need Line / Edge.
- Over budget, the client reuses **stale** cache instead of spending — raise `ODDS_DAILY_BUDGET` only if you must.
- Opt into walks/outs only when needed:  
  `--odds-markets pitcher_strikeouts,pitcher_hits_allowed,pitcher_earned_runs,pitcher_walks,pitcher_outs`

For GitHub Actions, add repo secret `ODDS_API_KEY` (or `ODDS_API_KEY_NEW`). Morning cron skips odds; afternoon cron spends one lite pull.

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
- [The Odds API](https://the-odds-api.com/) for live pitcher prop lines (optional; `ODDS_API_KEY`)

Pitchers resolve by MLBAM `player_id` first, then name (`First Last` / `Last, First`). Missing arsenals get `missing_arsenal` / `unresolved` instead of crashing.
