# Handoff — MLB K-matchup / ALCS playoff workflow

**Branch:** `cursor/alcs-g6-grade-g7-fe0c` (continues `cursor/playoff-slate-2026-10-15-2f1e` / PR 21)  
**Goal:** Daily OFF batter leans + zone heatmaps + pitcher K lanes + postgame grades; keep process locks current.

## Paste this into a new Grok 4.6 chat (with @ files below)

> Continue the MLB K-matchup workflow from `@HANDOFF-alcs.md`. Honor locks in `@backtest-lessons.md` (incl. ALCS G6). ALCS is over — TB beat CLE **4–2** in G6. Next live slate: World Series / NLCS remainder. Tools live under `mlb-k-matchups/`. Grade any remaining live series the same way: official lineups → zone overlaps → locked card → postgame `backtest-YYYY-MM-DD-*.md` + lessons.

## Done (committed on branch)
- Season ∩ recent heatmaps in `mlb-k-matchups/zone_overlap.py` (`CONFIRM` / `SEASON_ONLY` / `LOW_SAMPLE_*`)
- Living rules: `backtest-lessons.md` (G3–G6 ALCS locks)
- Graded: `backtest-2026-10-17-alcs-g4.md` · `backtest-2026-10-18-alcs-g5.md` · **`backtest-2026-10-19-alcs-g6.md`**
- G6 OFF lock (historical): `pregame-batter-leans-2026-10-19-alcs-g6-off.md`
- Heatmaps: `zone-overlap-freddy-peralta-2026-10-19.md` · `zone-overlap-shawn-armstrong-2026-10-19.md`
- **No G7 card** — TB 7, CLE 3 · series over 4–2 · Oct 20 MLB schedule empty for this series

## Process locks to honor (do not re-learn)
1. 2-man: ≥1 leg **CONFIRM** (SEASON_ONLY = singles only)
2. O1.5 / 2+ Hits ≠ O0.5 — need multi profile (Yandy-type)
3. Same-bat 2+ Hits + 3+ HRR = correlated **nuke** — 1-hit HR can cash HRR and miss 2+
4. UNDER_OK + Stuff+≥105 / WHIFF → no chalk soft under (Peralta Stuff+97 is below the veto)
5. Opener ≤~2 IP → vs-SP grade incomplete; identify **primary bulk** live
6. **Opener dump-HOT ≠ 2-man A-ticket** (Aranda G6) — tiny O0.5 vs that arm only
7. Caminero-types **COLD on opener dump** → pass Hits vs opener; fire on LHP bulk
8. Kwan-types: fade HRR/power, not O0.5 Hits
9. Palacios-types: **pass hard fade** on mid/utility COLD (G4 inverse + G6 smash)
10. Bailey-type WARM-mid CONFIRM without elite board → tiny / not a 2-man
11. Post-exit bottom-order fades void when SP hooks early

## G6 grade snapshot (locked)
- Peralta 3 K / 5.1 W — Exp 3.98 · pass juiced over HIT · U5.5+ would cash
- Armstrong 0 K / 1.0 L — pass K HIT · Cantillo 1.2 LHP primary bulk
- CLE process 2-man **DeLauter + Adell = 2/2**
- TB process 2-man **Aranda + Yandy = 1/2** (Aranda 0-4)
- User dual same-bat nuke **1/4** (only Yandy 3+ HRR)
- Caminero 2-3 HR / HRR 6 after live LHP swap · Palacios pass-fade 2-4 2 RBI

## Series state
- **Final: TB wins ALCS 4–2** (G6 TB 7, CLE 3 at Tropicana)
- Williams unused (was the G7 hypothetical)

## Open / next
1. World Series / remaining NLCS: same OFF routine (`--require-official-lineup` + zone overlaps)
2. Always: re-run zone overlaps on lineup changes
3. Do not build ALCS G7

## Files to @ in new chat
`@HANDOFF-alcs.md` `@backtest-lessons.md` `@backtest-2026-10-19-alcs-g6.md` `@mlb-k-matchups/README.md`
