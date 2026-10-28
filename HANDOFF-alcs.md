# Handoff — MLB K-matchup / World Series

**Branch:** `cursor/ws-g4-grade-fe0c`  
**Goal:** Daily OFF batter leans + zone heatmaps + pitcher K lanes + postgame grades; keep process locks current.

## Paste this into a new Grok 4.6 chat (with @ files below)

> Continue from `@HANDOFF-alcs.md`. Honor locks in `@backtest-lessons.md`. World Series **G4 is graded**: `@backtest-2026-10-27-ws-g4.md`. TB 4, MIL 3 in 12. Series **MIL 3–1**. Next: wait official G5 probables and nines; do not lock G5 off G4 maps. Tools under `mlb-k-matchups/`.

## Done
- ALCS G3–G6 graded; series TB **4–2**
- Order-walk expected hits / RBI traffic
- **WS G1** locked + graded (MIL 3–2): `@backtest-2026-10-23-ws-g1.md`
- **WS G2** locked + graded (MIL 5–4): `@backtest-2026-10-24-ws-g2.md`
- **WS G3** locked + graded (MIL 10–1): `@backtest-2026-10-26-ws-g3.md`
- **WS G4 OFF** locked (2026-10-27): May vs Jax, official nines. `@pregame-batter-leans-2026-10-27-ws-g4.md`
- **WS G4 graded** (TB 4–3 in 12): `@backtest-2026-10-27-ws-g4.md`. Process solos **1/5** (Yandy Hits only).

## Process locks (do not re-learn)
1. 2-man: ≥1 leg **CONFIRM** (SEASON_ONLY = singles only)
2. O1.5 / 2+ Hits ≠ O0.5 — Yandy-type multi; `p_ge_2` sizes this
3. Same-bat 2+ Hits + 3+ HRR = correlated nuke
4. UNDER_OK + Stuff+≥105 / WHIFF → no chalk soft under
5. Opener / SP ≤~2 IP → vs-SP incomplete; identify **primary bulk**
6. Opener dump-HOT ≠ 2-man A-ticket
7. Caminero-types COLD on RHP dump → **pass vs that arm**; fire vs LHP (G3 0-fer does not unlearn; G4 1B vs May does not flip the RHP pass)
8. Kwan-types: fade HRR/power, not O0.5 Hits (G4 Simpson 3-5 / HRR 4 is not a nuke lock)
9. Palacios-types: **pass hard fade**
10. Bailey-type WARM-mid CONFIRM without elite board → tiny
11. **Dump vs that batter’s hand**
12. **expected_hits / rbi_spot size, dump-fit gates**
13. **Kalshi last-leg combo:** 4/5 in + 1 PA vs closer → cash ≥ ~$15. G1 $21 vs Yandy/Megill ($0 if ride).
14. **One anchor bat on one 2-man only**
15. **O0.5 ≠ 2+**
16. **SP hook ~3–4.2 IP** → later box is vs bulk. Grade vs-SP separate from the full box. May 3.0 = playoff pattern, not a void of a 2-PA ticket.
17. **ML slight leans are not process locks.** G3 TB ML died; G4 MIL ML died in 12.
18. **7-hole TUNNEL stays tiny.** Pratt G4 4-5 HR is size, not a 1★.
19. **SPIKE no juiced over** even when the K total clears (Jax 6 K / 4.0).
20. **Throw out leftover SP names** when official nines differ. Drohan 12th L/BS ≠ Drohan as starter.

## G4 grade snapshot
- **Jax** 6 K / 4.0 (Exp 4.28 SPIKE). O5.5 would cash — pass is a result miss, not a flip. U4.5 correctly passed.
- **May** 3 K / 3.0 (Exp 3.85 SPIKE). Juiced K pass HIT. Hook matches 3/1/3/1.
- Process solos **1/5**: Yandy Hits HIT (Uribe). Aranda 0-5, Contreras 0-4, Yelich 0-3, Bauers 0-6 MISS.
- 2-man A/B MISS · 3-man MISS · MIL ML MISS.
- Caminero pass result miss (1B vs May). Palacios 0-4 pass HIT. Simpson 3-5 would have cashed 2H+3HRR — still not a lock.

## Open / next
1. **G5 — do not lock.** Wait official probables and nines. Series MIL 3–1 at the Trop unless MLB moves it.
2. Do not copy G4 1★/pass onto an unseen dump.

## Files to @
`@HANDOFF-alcs.md` `@backtest-lessons.md` `@backtest-2026-10-27-ws-g4.md` `@pregame-batter-leans-2026-10-27-ws-g4.md` `@backtest-2026-10-26-ws-g3.md` `@mlb-k-matchups/README.md`
