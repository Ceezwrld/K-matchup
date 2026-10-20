# Handoff — MLB K-matchup / World Series

**Branch:** `cursor/alcs-g6-grade-g7-fe0c`  
**Goal:** Daily OFF batter leans + zone heatmaps + pitcher K lanes + postgame grades; keep process locks current.

## Paste this into a new Grok 4.6 chat (with @ files below)

> Continue from `@HANDOFF-alcs.md`. Honor locks in `@backtest-lessons.md` (incl. ALCS G6). ALCS over — TB beat CLE **4–2**. World Series is **TB vs MIL**. Series preview: `@pregame-world-series-2026-tb-mil.md`. First: when G1 probables post (Fri 10/23 TB @ MIL), refresh with `--require-official-lineup` + zone overlaps and lock a G1 OFF card. Tools under `mlb-k-matchups/`.

## Done
- ALCS G3–G6 graded; G6 final TB 7–CLE 3 · series 4–2 · no G7
- WS preview scored (8 arms vs last nines): `rankings-2026-ws-preview.csv` · `hits-2026-ws-preview.csv`
- Series card: `pregame-world-series-2026-tb-mil.md`

## Process locks (do not re-learn)
1. 2-man: ≥1 leg **CONFIRM** (SEASON_ONLY = singles only)
2. O1.5 / 2+ Hits ≠ O0.5 — Yandy-type multi
3. Same-bat 2+ Hits + 3+ HRR = correlated nuke (1-hit HR can cash HRR and miss 2+)
4. UNDER_OK + Stuff+≥105 / WHIFF → no chalk soft under
5. Opener / SP ≤~2 IP → vs-SP incomplete; identify **primary bulk**
6. Opener dump-HOT ≠ 2-man A-ticket
7. Caminero-types COLD on RHP dump → pass vs that arm; **fire vs LHP** (Gasser/Drohan)
8. Kwan-types: fade HRR/power, not O0.5 Hits
9. Palacios-types: **pass hard fade**
10. Bailey-type WARM-mid CONFIRM without elite board → tiny

## WS snapshot (provisional — prior nines)
- **Peralta vs MIL flips to STRONG** Exp 5.51 (was UNDER_OK vs CLE) — O4.5 floor, not O6.5 (BAL)
- **Misiorowski SPIKE** Stuff+128 Exp 4.38 vs TB G6 — no soft U6; NLCS 5 K / 4.1
- **Gasser L UNDER_OK** Exp 3.77 · TB **Caminero + Mesa** vs LHP
- **Martinez UNDER_OK** vs MIL whiff_prone — U6.5+ or MIL Hits (Bauers)
- **Rasmussen** SOFT but Stuff+110 WHIFF — no chalk under
- Bauers is MIL #1 Hits vs every TB RHP
- G1 Fri 10/23 7:00 CT at Milwaukee · no probables yet

## Open / next
1. **G1 OFF card** when probables + lineups post (likely Misi vs Rasmussen/Jax)
2. Zone overlaps on both G1 SPs (`zone_overlap.py --images`) — 4-panel gallery (throws / **swing** / damage / overlap) + dump-fit table (`TUNNEL`/`MISTAKE`/`CHASE`/`TAKE`/`OFFER`/`COLD`). Display-only; does not retune HOT or Exp K.
3. If TB names Peralta G1, move the STRONG K game up and re-slot Trop G3

## Files to @
`@HANDOFF-alcs.md` `@backtest-lessons.md` `@pregame-world-series-2026-tb-mil.md` `@backtest-2026-10-19-alcs-g6.md` `@mlb-k-matchups/README.md`
