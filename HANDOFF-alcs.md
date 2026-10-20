# Handoff — MLB K-matchup / ALCS playoff workflow

**Branch:** `cursor/playoff-slate-2026-10-15-2f1e` · **PR:** https://github.com/Ceezwrld/K-matchup/pull/21  
**Goal:** Daily OFF batter leans + zone heatmaps + pitcher K lanes + postgame grades; keep process locks current.

## Paste this into a new Grok 4.6 chat (with @ files below)

> Continue the MLB K-matchup / ALCS workflow from `@HANDOFF-alcs.md`. Honor locks in `@backtest-lessons.md`. Current locked card: `@pregame-batter-leans-2026-10-19-alcs-g6-off.md`. Tools live under `mlb-k-matchups/`. First: grade G6 final box → write `backtest-2026-10-19-alcs-g6.md` and fold any new locks into lessons; if series continues, build G7 OFF card with `--require-official-lineup` + zone overlaps.

## Done (committed on branch)
- Season ∩ recent heatmaps in `mlb-k-matchups/zone_overlap.py` (`CONFIRM` / `SEASON_ONLY` / `LOW_SAMPLE_*`)
- Living rules: `backtest-lessons.md` (incl. G4 + G5 locks)
- Graded: `backtest-2026-10-17-alcs-g4.md` · `backtest-2026-10-18-alcs-g5.md`
- G6 OFF lock: `pregame-batter-leans-2026-10-19-alcs-g6-off.md`
- Heatmaps: `zone-overlap-freddy-peralta-2026-10-19.md` · `zone-overlap-shawn-armstrong-2026-10-19.md`
- Gallery: `/opt/cursor/artifacts/alcs-g6/visual/heatmap-gallery.html`

## Process locks to honor (do not re-learn)
1. 2-man: ≥1 leg **CONFIRM** (SEASON_ONLY = singles only)
2. O1.5 / 2+ Hits ≠ O0.5 — need multi profile (Yandy-type)
3. Same-bat 2+ Hits + 3+ HRR = correlated **nuke**
4. UNDER_OK + Stuff+≥105 / WHIFF → no chalk soft under
5. Opener ≤~2 IP → vs-SP grade incomplete; identify **primary bulk** live
6. Caminero-types **COLD on opener dump** → pass Hits vs opener; fire on LHP bulk
7. Kwan-types: fade HRR/power, not O0.5 Hits
8. Post-exit bottom-order fades void when SP hooks early

## G6 locked ticket sheet (as of OFF)
- TB: Aranda Hits · Yandy Hits (best 2+) · Hicks Hits · Mesa Hits · Caminero only if Cantillo LHP
- CLE: DeLauter Hits O0.5 · Adell Hits · Bailey Hits
- Clean 2-mans: Aranda+Yandy · DeLauter+Adell · cross Aranda+DeLauter
- Nuke: Yandy 2+ + DeLauter 2+ (cross) · or Yandy 2+/3HRR + Aranda 2+/3HRR (dual same-bat)

## Series state
- After G5: TB led 3–2 · G6 at Tropicana · Peralta vs Armstrong opener + CLE bullpen game
- User ran dual same-bat nuke (Yandy+Aranda 2H and 3HRR) and asked live refreshes

## Open / next
1. Grade G6 final when complete → `backtest-2026-10-19-alcs-g6.md` + fold locks into `backtest-lessons.md`
2. If series continues: G7 OFF card (Williams likely CLE)
3. Always: refresh with `--require-official-lineup`, re-run zone overlaps on lineup changes

## Moving forward — operating cadence

**Every slate (no shortcuts):**
1. OFF lineup → `k_matchups.py` + hits board (`--require-official-lineup`)
2. `zone_overlap.py` **images on** for every listed SP **and** likely primary bulk (opener games)
3. Write BEST/GOOD/FADE card where every BEST/GOOD cites **zone tag + pitch tunnel + CONFIRM/SEASON_ONLY** — board score alone is not enough
4. Ship `pregame-visual-leans-*.md` + gallery HTML so heatmaps are visible in chat (not just md paths)
5. Ticket sheet only after maps: 2-man ≥1 CONFIRM · O0.5 vs 2+ gated by multi profile · nuke only on true engines
6. Live: ID primary bulk early → re-lean + re-map if hand flips; incomplete vs-opener grades
7. Postgame: grade vs-SP separate from full box → update `backtest-lessons.md` before next card

## Do better (heatmap-first gaps to close)
| Gap | Fix |
|-----|-----|
| Board-first leans, map as footnote | **Map gates the tier** — no BEST without HOT/WARM on real dump or elite board + disclosed dump-COLD |
| Opener maps only | Always pre-map **Cantillo / Bibee / Cecconi / Williams**-class bulk when bullpen game |
| SEASON_ONLY treated like CONFIRM | Singles only; never 2-man anchor |
| Volume (2+/3HRR) on CONFIRM O0.5 bats | Separate multi-profile check (Yandy-type) |
| Heatmaps hard to see in chat | Always attach PNGs + `heatmap-gallery.html` in artifacts; visual leans card required |
| Early-exit fades still live | Void bottom-order fades; re-run vs long reliever |
| K lane mixed into Hits card | Keep pitcher UNDER_OK / SPIKE separate from batter map card |

## Files to @ in new chat
`@HANDOFF-alcs.md` `@backtest-lessons.md` `@pregame-batter-leans-2026-10-19-alcs-g6-off.md` `@mlb-k-matchups/README.md`
