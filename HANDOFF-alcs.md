# Handoff — MLB K-matchup / World Series

**Branch:** `cursor/ws-g3-grade-fe0c`  
**Goal:** Daily OFF batter leans + zone heatmaps + pitcher K lanes + postgame grades; keep process locks current.

## Paste this into a new Grok 4.6 chat (with @ files below)

> Continue from `@HANDOFF-alcs.md`. Honor locks in `@backtest-lessons.md`. World Series **G3 is graded**: `@backtest-2026-10-26-ws-g3.md` (MIL 10–1). Next: G4 Tue 10/27 at the Trop — wait official nines. Tools under `mlb-k-matchups/`.

## Done
- ALCS G3–G6 graded; series TB **4–2**
- Order-walk expected hits / RBI traffic
- **WS G1** locked + graded (MIL 3–2): `@backtest-2026-10-23-ws-g1.md`
- **WS G2** locked + graded (MIL 5–4): `@backtest-2026-10-24-ws-g2.md`
- **WS G3** locked + graded (MIL 10–1): `@backtest-2026-10-26-ws-g3.md`

## Process locks (do not re-learn)
1. 2-man: ≥1 leg **CONFIRM** (SEASON_ONLY = singles only)
2. O1.5 / 2+ Hits ≠ O0.5 — Yandy-type multi; `p_ge_2` sizes this
3. Same-bat 2+ Hits + 3+ HRR = correlated nuke
4. UNDER_OK + Stuff+≥105 / WHIFF → no chalk soft under
5. Opener / SP ≤~2 IP → vs-SP incomplete; identify **primary bulk**
6. Opener dump-HOT ≠ 2-man A-ticket
7. Caminero-types COLD on RHP dump → pass vs that arm; **fire vs LHP** (G3 0-fer does not unlearn)
8. Kwan-types: fade HRR/power, not O0.5 Hits
9. Palacios-types: **pass hard fade**
10. Bailey-type WARM-mid CONFIRM without elite board → tiny
11. **Dump vs that batter’s hand**
12. **expected_hits / rbi_spot size, dump-fit gates**
13. **Kalshi last-leg combo:** 4/5 in + 1 PA vs closer → cash ≥ ~$15. G1 $21 vs Yandy/Megill ($0 if ride).
14. **One anchor bat on one 2-man only** (G1/G2 Bauers A HIT / Yandy B MISS; G3 Caminero A MISS / Yandy B HIT).
15. **O0.5 ≠ 2+** — G2 Yelich/Yandy both HRR 1. Process 0.5 HIT; user 2+ MISS.
16. **SP hook ~3–4.2 IP** → later box is vs bulk. Grade vs-SP separate from the full box.
17. **ML slight leans are not process locks.** G3 TB ML died on Gasser’s 1-hitter.

## G3 grade snapshot (MIL 10–1)
- Process solos **3/6 HIT**: Contreras 3-5 HRR 5 · Yelich 2-3 HRR 4 · Yandy 2-4. **Caminero 0-3 MISS** (1★) · Vilade 0-2 · Bauers 0-4 Hits (HRR 0.5 would HIT).
- 2-man **A MISS** (Caminero) · **B HIT** (Yandy+Contreras). **TB ML MISS**.
- Gasser **6.0 IP, 1 H, 0 R, 3 K** (Exp 3.83, Exp H 4.48). Peralta **4.2 IP, 5 ER, 4 K** then Booser 0.0 IP 4 R.
- Passes: Mesa 0-2 HIT · Simpson 0-3 HIT · Williamson 0-3 HIT · Frelick fade miss vs Booser, not vs Peralta.
- Yandy Hits finally printed (0-for-9 then 2-4). Still not 1★ / not 2+.

## Open / next
1. **G4 OFF lock** when both nines post. Tue 10/27 Trop. Likely Drohan (L) vs leftover TB. Drohan NLCS **1.0 IP** → vs-SP incomplete if that repeats; re-lean first long arm.
2. Keep Caminero vs LHP if Drohan/Gasser-shape starts. Do not pass from the G3 0-fer.

## Files to @
`@HANDOFF-alcs.md` `@backtest-lessons.md` `@backtest-2026-10-26-ws-g3.md` `@pregame-batter-leans-2026-10-26-ws-g3.md` `@mlb-k-matchups/README.md`
