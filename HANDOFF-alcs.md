# Handoff — MLB K-matchup / World Series

**Branch:** `cursor/ws-g4-off-fe0c`  
**Goal:** Daily OFF batter leans + zone heatmaps + pitcher K lanes + postgame grades; keep process locks current.

## Paste this into a new Grok 4.6 chat (with @ files below)

> Continue from `@HANDOFF-alcs.md`. Honor locks in `@backtest-lessons.md`. World Series **G4 is OFF**: `@pregame-batter-leans-2026-10-27-ws-g4.md`. May (R) vs Jax (R) at the Trop, official nines. MIL leads 3–0. Next: live if May hooks ≤2 IP; then grade G4. Tools under `mlb-k-matchups/`.

## Done
- ALCS G3–G6 graded; series TB **4–2**
- Order-walk expected hits / RBI traffic
- **WS G1** locked + graded (MIL 3–2): `@backtest-2026-10-23-ws-g1.md`
- **WS G2** locked + graded (MIL 5–4): `@backtest-2026-10-24-ws-g2.md`
- **WS G3** locked + graded (MIL 10–1): `@backtest-2026-10-26-ws-g3.md`
- **WS G4 OFF** locked (2026-10-27): May vs Jax, official nines. `@pregame-batter-leans-2026-10-27-ws-g4.md`

## Process locks (do not re-learn)
1. 2-man: ≥1 leg **CONFIRM** (SEASON_ONLY = singles only)
2. O1.5 / 2+ Hits ≠ O0.5 — Yandy-type multi; `p_ge_2` sizes this
3. Same-bat 2+ Hits + 3+ HRR = correlated nuke
4. UNDER_OK + Stuff+≥105 / WHIFF → no chalk soft under
5. Opener / SP ≤~2 IP → vs-SP incomplete; identify **primary bulk**
6. Opener dump-HOT ≠ 2-man A-ticket
7. Caminero-types COLD on RHP dump → **pass vs that arm**; fire vs LHP (G3 0-fer does not unlearn; G4 May is R — pass)
8. Kwan-types: fade HRR/power, not O0.5 Hits
9. Palacios-types: **pass hard fade**
10. Bailey-type WARM-mid CONFIRM without elite board → tiny
11. **Dump vs that batter’s hand**
12. **expected_hits / rbi_spot size, dump-fit gates**
13. **Kalshi last-leg combo:** 4/5 in + 1 PA vs closer → cash ≥ ~$15. G1 $21 vs Yandy/Megill ($0 if ride).
14. **One anchor bat on one 2-man only**
15. **O0.5 ≠ 2+**
16. **SP hook ~3–4.2 IP** → later box is vs bulk. Grade vs-SP separate from the full box.
17. **ML slight leans are not process locks.** G3 TB ML died on Gasser’s 1-hitter.

## G4 OFF snapshot
- **Jax** Exp **4.28 AVG** · **WHIFF / SPIKE** · **4.3 IP / 18 BF** · MIL Exp H **3.19**. No O5.5+ · no U4.5.
- **May** Exp **3.85 SOFT BAL** · **SPIKE** L3 K9 13.5 · **4.3 IP / 18 BF** · TB Exp H **3.51**. Pass juiced K. Playoff boxes 3/1/3/1 IP — hook ≤2 voids vs-SP.
- TB vs May: **Aranda TUNNEL 1★**. Yandy Hits (heart, COLD dump). **Caminero PASS** (CONFIRM COLD). Hicks tiny TUNNEL. Palacios pass. Simpson TAKE tiny.
- MIL vs Jax: **Contreras** Hits/HRR engine. Yelich / Bauers size down. Frelick 6-hole still **COLD fade**. Pratt only TUNNEL (tiny).
- 2-man: Aranda+Contreras · Yandy+Contreras. **3-man lock:** Aranda Hits + Contreras HRR + Yelich HRR. No Caminero.
- **Win lean:** MIL slightly (fresh pen, Jax into a fried TB pen). Not a hammer.

## Open / next
1. Live: May hook ≤2 IP → void Aranda vs-SP; re-lean MIL pen.
2. Grade G4 after final. If MIL wins, season over.

## Files to @
`@HANDOFF-alcs.md` `@backtest-lessons.md` `@pregame-batter-leans-2026-10-27-ws-g4.md` `@backtest-2026-10-26-ws-g3.md` `@zone-overlap-griffin-jax-2026-10-27.md` `@zone-overlap-dustin-may-2026-10-27.md` `@mlb-k-matchups/README.md`
