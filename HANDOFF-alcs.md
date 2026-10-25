# Handoff — MLB K-matchup / World Series

**Branch:** `cursor/ws-g2-card-fe0c`  
**Goal:** Daily OFF batter leans + zone heatmaps + pitcher K lanes + postgame grades; keep process locks current.

## Paste this into a new Grok 4.6 chat (with @ files below)

> Continue from `@HANDOFF-alcs.md`. Honor locks in `@backtest-lessons.md`. World Series **G2 is graded**: `@backtest-2026-10-24-ws-g2.md` (MIL 5–4). Next: G3 Mon 10/26 at the Trop — wait official nines. Tools under `mlb-k-matchups/`.

## Done
- ALCS G3–G6 graded; series TB **4–2**
- Order-walk expected hits / RBI traffic
- **WS G1** locked + graded (MIL 3–2): `@backtest-2026-10-23-ws-g1.md`
- **WS G2** locked + graded (MIL 5–4): `@backtest-2026-10-24-ws-g2.md`

## Process locks (do not re-learn)
1. 2-man: ≥1 leg **CONFIRM** (SEASON_ONLY = singles only)
2. O1.5 / 2+ Hits ≠ O0.5 — Yandy-type multi; `p_ge_2` sizes this
3. Same-bat 2+ Hits + 3+ HRR = correlated nuke
4. UNDER_OK + Stuff+≥105 / WHIFF → no chalk soft under
5. Opener / SP ≤~2 IP → vs-SP incomplete; identify **primary bulk**
6. Opener dump-HOT ≠ 2-man A-ticket
7. Caminero-types COLD on RHP dump → pass vs that arm; **fire vs LHP**
8. Kwan-types: fade HRR/power, not O0.5 Hits
9. Palacios-types: **pass hard fade**
10. Bailey-type WARM-mid CONFIRM without elite board → tiny
11. **Dump vs that batter’s hand**
12. **expected_hits / rbi_spot size, dump-fit gates**
13. **Kalshi last-leg combo:** 4/5 in + 1 PA vs closer → cash ≥ ~$15. G1 $21 vs Yandy/Megill ($0 if ride).
14. **One anchor bat on one 2-man only** (G1/G2 Bauers A HIT, Yandy B MISS both nights).
15. **O0.5 ≠ 2+** — G2 Yelich/Yandy both HRR 1. Process 0.5 HIT; user 2+ MISS.
16. **SP hook ~3 IP** → later box is vs bulk. Grade vs-SP separate from the full box.

## G2 grade snapshot (MIL 5–4)
- Process solos **4/5 HIT**: Aranda 1-4 2B · Bauers 1-3 · Contreras 2-5 HRR 3 · Yelich 1-4. **Yandy 0-5 MISS** (run makes HRR 0.5 a HIT).
- 2-man **A HIT** · **B MISS** (Yandy) · 3-man **HIT**. User 2+/3+ slip **1/3** (Contreras only); ride **$0**.
- Passes: Palacios 0-3 HIT · Simpson tiny printed 1-4 HRR 3 · Caminero pass result-miss (1-4 RBI vs Henderson; do not flip) · Frelick fade miss vs Seymour, not vs Ras.
- Both SPs hooked ~3 IP. Henderson 4 K / 3.0 would cash a soft under — SPIKE veto stands.

## Open / next
1. G3 Mon 10/26 at Trop — likely Peralta vs Gasser (LHP Caminero/Mesa window). **Do not lock** until official nines.
2. Yandy Hits lean stays Hits-not-HRR; do not 1★ him until he prints (0-4, 0-5).

## Files to @
`@HANDOFF-alcs.md` `@backtest-lessons.md` `@backtest-2026-10-24-ws-g2.md` `@pregame-batter-leans-2026-10-24-ws-g2.md` `@backtest-2026-10-23-ws-g1.md` `@mlb-k-matchups/README.md`
