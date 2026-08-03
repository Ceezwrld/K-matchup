# K-prop process lessons (from graded slates)

Living rules. Update after every backtest. Soft lines assume ~0.75+ edge unless noted.

## Every morning routine (do this first)

Run this **every morning** before tickets. Goal: one clear outlook for **every** probable starter.

1. **Refresh the board** (probable starters; usually all prior early):
   ```bash
   TZ=America/Chicago python3 mlb-k-matchups/k_matchups.py \
     --date YYYY-MM-DD \
     -o rankings-YYYY-MM-DD.csv \
     --html rankings.html \
     --hits-output hits-YYYY-MM-DD.csv
   ```
2. **Publish** CSV + `rankings.html` / `index.html` + hits CSV to `main` (GitHub Pages updates the **same** bookmark URL). Note lineup status (`prior` vs `official`).
   - **Bookmark only (interactive tabs):** https://htmlpreview.github.io/?https://raw.githubusercontent.com/Ceezwrld/K-matchup/main/index.html  
   - Optional Pages URL (one Settings enable): https://ceezwrld.github.io/K-matchup/  
   - Never use jsDelivr (plain text) or commit-SHA htmlpreview links.
3. **Deliver the morning outlook** in this exact shape (arsenal-first):

   **Over leans** — solo arsenal grade **ELITE / STRONG** (starter, not opener)  
   **Under leans** — solo arsenal grade **SOFT**  
   **Fade / thin** — FILLER, openers, MATCHUP_OK (thin O3.5 only), high-risk watch list  

   For each arm include: **solo grade**, arsenal K%, vs league / vs opp K%, Exp K, outing risk, game/time.  
   Slate `#` and opp K% `#` are optional context only.  
   Also check **vs Team history** on each card (career K% vs that batting team + recent games with **HOME/AWAY** for the pitcher). Use history to confirm or caution the model side — not to override a clear absolute arsenal gate.  
   Mark the whole board **provisional** until official lineups post.
4. **Re-refresh when lineups confirm** — same report shape, flip prior→official, re-check leans before locking tickets.
5. **Accuracy lock before firing** — official nine in, starter not opener, side matches arsenal vulnerability, line edge still holds.

This morning pack is the daily starting point — not optional.

## Core thesis — pitcher vs batter vulnerability first

**Primary edge = solo arsenal vs this nine** — absolute `expected_k_pct` and **`arsenal_abs_grade`** (ELITE / STRONG / AVG / SOFT).  
That grade is banded on the pitcher’s arsenal-weighted K% vs *this* lineup and **does not move** when other starters are added/removed from the slate.

| Absolute arsenal K% vs lineup | Solo grade | Lean |
|------------------------------|------------|------|
| **≥ 24.0%** | **ELITE** | **OVER** bias |
| **≥ 22.5%** (league K%) | **STRONG** | **OVER** lean |
| **≥ 20.0%** | **AVG** | Neutral / need more |
| **&lt; 20.0%** | **SOFT** | **UNDER** bias |

Also check edges on the card: **vs league** (`expected_k_pct − 22.5`) and **vs opp K%** (mix beats/lags the lineup’s raw K tendency).

**Secondary only:** slate `#` / slate `matchup_grade` / opp lineup K% `#` — “who’s best *today*,” not solo quality.  
Exp K and projected IP size the outing; they do not define the side.

| Solo grade (absolute) | Lean | Why |
|-----------------------|------|-----|
| **ELITE / STRONG** | **OVER** bias | Bats are vulnerable to *this* mix even if Exp K looks soft |
| **SOFT** | **UNDER** bias | Weak pitcher-vs-batter fit caps conversion — soft U6.5+ is live |
| **Mid-pack** | Pass / thin only | No clear vulnerability edge |

### Paired lesson (7/30) — opposite sides, same rule

Use these two together when deciding overs vs unders. **Arsenal matchup decides the side; opp team K% rank is secondary.**

| | **McLean vs MIA** | **Sasaki vs SEA** |
|--|-------------------|-------------------|
| Arsenal matchup | **#17 / soft** | **#3 / elite** |
| Opp lineup K% rank | **#5** (looks juicy) | **~#14** (looks soft) |
| Market line (example) | U6.5 | O5.5 |
| Result | **6 K — under HIT** | **7 K** (through ~5.1 IP, live) — **over cashed** |
| Read | Soft pitcher-vs-batter fit → under, even vs a high-K lineup on paper | Elite pitcher-vs-batter fit → over, even vs a weak team K% rank |

**Decision rule to keep:**  
1. Look at **pitcher arsenal vs that batting nine** first.  
2. If arsenal is soft/bottom → lean **under** (McLean). Don’t let a shiny opp K% rank talk you into the over.  
3. If arsenal is elite/strong (~#1–#3) → lean **over** (Sasaki). A middling/weak opp team K% rank matters less and should not fade a real dominance matchup.  
4. Then size the line (soft vs juice) with risk, IP, discipline, opener tags.

Other cards: **Barnett** (#2 elite / low Exp K) = matchup > mean projection, but opener ≠ full-start over. **Weathers** (#5) = not elite enough for over chalk (7 IP / 4 K).

## Core filters (kept working)

- Prefer **soft O3.5 / O4.5** with edge and **clear/low** outing risk — **only after** arsenal clears the over gate.
- **OVER gate — solo arsenal must be ELITE/STRONG:** fire pitcher K overs when absolute arsenal vs that nine is **ELITE (≥24% K) or STRONG (≥22.5%)**. Thesis: good pitcher-vs-batter fit can push a pitcher **over his projection / O/U line** even when Exp K looks modest. AVG solo grade → no ticket over (O3.5 floor max). Exp K, IP, and slate `#` are secondary.
- **UNDER gate — SOFT solo arsenal is the edge:** when absolute arsenal vs that nine is **SOFT (&lt;20% K)**, lean **unders** (esp. soft **U6.5 / U7.5**) even if opp lineup K% ranks high or Exp K sits near 5–6. McLean proved high opp K% ≠ over juice when the mix is soft vs that nine. Still: **no soft unders on SPIKE arms (K9 ≥ ~10)**; prefer wide edge under the line.
- Prefer **soft U6.5 / U7.5** with wide edge when arsenal is soft; **U5.5** OK if non-SPIKE and edge holds.
- **Fade unders on SPIKE arms (K9 ≥ ~10)** — they can jump a soft under even when proj is mid / arsenal looks soft.
- Fade **openers / uncertain swingmen** for *full-outing* K props (Barnett-style elite arsenal still isn’t a starter O4.5).
- **Medium/high** outing risk → need *more* edge for overs (or pass).
- **Soft-contact / low-K volume arms (K9 ≲ ~7, soft L3 Ks, elev_xFIP):** flag the **profile**, then check arsenal rank.
  - Soft profile + **avg/soft matchup** → **FILLER** — pass or O3.5 on Ks; does not help a K ticket.
  - Soft profile + **strong/elite arsenal matchup** → **MATCHUP_OK** — disclose the soft profile; soft O3.5 / thin O4.5 K only; still never a nuke anchor next to Wheeler-tier legs.
  - **Alt lane — pitcher outs:** when Ks are a poor fit (FILLER, or MATCHUP_OK but you don’t want the K over), consider **pitcher outs** instead if outing length / risk is clear-low and projected IP holds.
  - (7/27 Montero: soft profile + weak matchup → FILLER confirmed **1 K / 4.1 IP / 9 H**.)
- Exact-K MAE ~2 is normal; use **arsenal vulnerability for side**, Exp K for which line.
- **Card size: 2 legs.** Prefer straight 2-mans. 3-legs only when all legs are clear process (no filler/thin/prior). No 4/5/6-mans — correlation and early hooks kill bigger tickets.
- **Daily volume (when slate is full):** several **2-leg** tickets over fewer 3-mans. One chalk/nuke pair max; rest mix pitcher+bat or bat+bat. Cap any single player at **~2 tickets**.
- **Accuracy lock (before firing):** refresh with **official lineups**; only lock a leg if (1) batter is in the posted nine, (2) pitcher role is starter not opener/swingman, (3) **side matches arsenal vulnerability** (over only if ~#1–#3 elite–strong; under lean when soft/bottom-tier), (4) soft line edge holds on the *current* proj, (5) no same-game opposing K-over stack. Prior-lineup tickets are provisional only.
- **Disclose weak links:** if a recommended leg is filler/thin-sample/prior-lineup/SPIKE-capped, state that in the ticket writeup — don’t bury it.
- **Dual-rank read (vulnerability × context):**
  1. **Arsenal matchup rank (primary — decides over vs under)** — pitcher vs *these* batters.
  2. **Opp lineup K% rank (secondary)** — supports stretching an over or warns that a soft-arsenal under is fighting a K-prone nine (still take the under if arsenal is dead soft + line is soft U6.5+).
  3. **Plate discipline** — patient / walk-heavy can suppress K conversion on overs; free-swing helps overs.
  - **Over chalk:** arsenal ~#1–#3 *and* starter (Sasaki). Opp K% top-tier upgrades juice (O5.5+); **weak opp K% does not cancel** an elite arsenal over on a normal line (Sasaki O5.5 vs SEA #14). Still fade opener tags (Barnett).
  - **Under chalk:** arsenal soft/bottom-tier (McLean #17) + non-SPIKE + soft U6.5+; **ignore shiny opp K% rank** as an over reason.
  - **Pass:** mid arsenal, or opener, or SPIKE soft-under.
- **Length ≠ Ks:** full IP without elite arsenal isn’t an over lock (Weathers).
- **FILLER can spike:** Assad (FILLER) 4.23→6. Pass on tickets still correct; never soft-under FILLER either.

## 2026-07-30 partial (MAE ~1.89 on first 8 Final; evening still grading)

Early Final: TEX@TB, KC@MIN, NYY@CWS, CHC@STL. Also Final: MIA@NYM (McLean/Pérez), PIT@CIN, WSH@ATL. Still live: SF@SD, BOS@ATH, SEA@LAD.

| What happened | Lesson |
|---------------|--------|
| **Burke** 7.45→**10** (6 IP / 23 BF, clear) | Volume clear top-board cashed hard — O4.5/O5.5/O6.5 all hit; Burke-tier O5.5+ juice OK when proj ≥ ~7 and clear |
| **Weathers** 5.55→**4** (7 IP / 26 BF; arsenal **#5**, CWS lineup K% **#7**, disc neutral) | Arsenal **#5 fails the over gate** — contact outing, O4.5 miss / O3.5 HIT. Need top arsenal (#1–#3) vs the nine before firing overs |
| **McClanahan** 5.03→**3** (3 IP / 12 BF, clear, elite matchup) | Early hook again — elite K% matchup dead without outs. Outing survival > matchup grade for overs |
| **Cameron** 4.62→**7** (8 IP / 26 BF, clear, soft matchup) | Soft mid-board spiked with length — O3.5/O4.5 cashed; **don’t skinny-under** clear soft-grade arms when IP holds |
| **McLean** 5.47→**6** (6.1 IP; arsenal **#17 / soft**, MIA opp K% **#5**) | **U6.5 HIT.** Soft pitcher-vs-batter vulnerability beat the shiny opp K% rank — primary **under** edge validated |
| **Sasaki** ~5.3–5.6→**7+** (~5.1 IP live; arsenal **#3 / elite**, SEA opp K% **~#14**) | **O5.5 HIT** (user line). Opposite of McLean — elite arsenal cleared a soft/mid line even with weak team K% rank; opp K% mattered less |
| **Pérez** 5.19→**6** (6 IP; arsenal #8, NYM opp K% #2) | Mid arsenal vs elite K nine — cleared soft O4.5/O5.5 but not an arsenal-gate over chalk going in |
| **Ober** FILLER 5.04→**3** (6 IP) | FILLER correctly avoided O4.5; pass/O3.5 lane right |
| **Pallante** FILLER 4.71→**3** (6.1 IP / 7 H) | FILLER + outs alt still the read — K over miss; long outing via BIP |
| **Assad** FILLER 4.23→**6** (4.1 IP) | FILLER can still clear O4.5 — never a ticket *anchor*, but also **never soft-under** FILLER |
| **Winn** opener 1.06→**0** (1 IP) | Opener fade correct again |
| Soft **O3.5** clear/low e≥0.75 → **3/5 (60%)** | Weathers HIT floor; McClanahan + Pallante leaks (hook / FILLER) |
| Soft **O4.5** clear/low e≥0.75 → **1/2 (50%)** | Only Burke; Weathers the length-without-Ks miss |

### Reinforced from 7/30

1. **Paired confidence rule:** McLean (soft arsenal → **under**) and Sasaki (elite arsenal → **over**) are opposite proofs of the same edge — side from pitcher-vs-batter vulnerability first.
2. **Opp lineup K% is secondary** — MIA #5 did not force a McLean over; SEA #14 did not fade a Sasaki over.
3. **Barnett thesis kept:** elite arsenal can beat a tiny Exp K *if* he works as a real starter; opener tag still kills full-outing overs.
4. **FILLER:** Ober/Pallante validated pass; Assad spike warns against soft unders on the same tag.
5. Re-finalize Sasaki/Woo when SEA@LAD is Final; keep using this pair for future O/U decisions.

## 2026-07-27 lessons (MAE ~1.34, n=20 Final; HOU@LAA still live — excluded; CLE@CIN rain postponement)

| What happened | Lesson |
|---------------|--------|
| **Montero** 5.18→**1** (4.1 IP / 9 H), low risk / K9 6.6 | FILLER rule confirmed — O4.5 on soft-contact low-K arms is poison for multis |
| Soft **O3.5** clear/low → **4/6 (67%)** | Floor still usable; Montero+Kirby are the leaks |
| Soft **O4.5** clear/low e≥0.75 → **2/4 (50%)**; e≥1.0 → **1/2** | Weaker O4.5 night — Kirby 3 / Fried 4 (3 IP) both missed |
| **Wheeler** 5.85→**6** in only **3 IP** | SPIKE + clear still clears soft O4.5/O5.5 when hooked early — never soft-under |
| **Tolle** 5.13→**7** (5.1 IP) | Clear mid-board O4.5 cashed; thin O4.5 with real K9 is fine |
| **Fried** 5.40→**4** (3 IP) | Clear + edge died on early exit — outing length > matchup K% |
| **Perkins** 6.80→**4** (5.2 IP, medium) | Top-board swingman/medium risk O5.5+ chalk failed — don’t nuke medium tops |
| **Rocker** 5.29→**7** (6.2 IP) | Volume clear O4.5/O5.5 cashed when IP held |
| **Kelly** 5.30→**6** despite K9 5.6 / high risk | Low-K season ≠ auto-miss if length holds; still FILLER for *tickets* |
| **Yean** 2.51→**0** / **Scherzer** 2.91→**4** (2.2 IP) | Openers/short tags matter more than raw proj for full-outing props |
| CLE@CIN **Postponed** (Burns/Cecconi) | Rain outs void prior-lineup locks — don’t carry provisional tickets overnight |

### 7/27 card scorecard (discussed / late tickets)

- **Montero O4.5** — MISS (1). Correctly flagged FILLER; still burned if used as anchor.
- **Wheeler** — HIT soft overs (6 K / 3 IP).
- **Kirby O4.5** — MISS (3).
- **Fried O4.5** — MISS (4 / 3 IP early hook).
- **Tolle O4.5** — HIT (7).
- **Perkins** top-board — MISS vs high chalk (4 K).
- **HOU@LAA (Imai / Ureña)** — still live; excluded from this grade.

## 2026-07-26 lessons (MAE ~2.09, n=30; NYY@PHI still live at grade)

| What happened | Lesson |
|---------------|--------|
| Soft **O3.5** clear/low e≥0.75 → **11/13 (85%)** | O3.5 floor still the most reliable over lane |
| Soft **O4.5** clear/low e≥0.75 → **5/8 (62%)**; e≥1.0 → **3/6 (50%)** | O4.5 weaker than 7/25 — early hooks (Sánchez 2 IP / 2 K) and SEA@TEX both 4 K |
| **Ashcraft** 6.24→**5** | Soft **O4.5 HIT**, max **O5.5 MISS** — reinforces O5.5 as juice-only even at ~6.2–6.5 |
| **Misiorowski** 6.70→**12** | PP soft **6.5 More** would have cashed; model undershot ceiling. SPIKE + soft COL = smash. Don’t need O4.5 hesitation when board soft is already 6.5 |
| **Gilbert / deGrom** both **4 K** | Same-game opposing K overs both missed — correlation risk was real |
| **Gausman** 5.57→**6** | Avoiding him for “form tilt” left a cashing O4.5; last-start sample ≠ fade with clear edge |
| **Buehler** 3.67→**7** | Soft **U4.5/U5.5** on medium arms still leaky — need wider under lines |
| **Rasmussen** 4.53→**9** / **Messick** 4.04→**6** | Low-mid proj clear arms can still rack Ks in volume outings — don’t skinny-under |
| **Sánchez** 5.74→**2** (2 IP) | Clear + edge died on early exit — outing length risk dominates K overs |
| Bats: **Peña / Chourio** Hits cashed; **Vaughn** 1 H (HRRBI cashed); **Lopez / Walker / Yordan** missed | Prefer Hits on elite vs-hand AVGs; H+R+RBI saved Vaughn-style power nights |

### 7/26 card scorecard (discussed tickets)

- **Ashcraft O4.5** — HIT (5). **Ashcraft O5.5** — MISS.
- **Gilbert O4.5 / deGrom O4.5** — both MISS (4).
- **Misiorowski** — we passed PP 6.5; actual **12** (would have hit every over).
- **Gausman O4.5** — HIT (6); fade was wrong today.
- **Peña Hits O1.5** — HIT (2). **Vaughn Hits** — MISS (1); **H+R+RBI** HIT.
- **Chourio Hits** — HIT. **Yordan / Lopez / Walker** — MISS.
- **NYY@PHI live:** Sánchez **2 K / 2 IP** (O4.5 dead), Warren **2 H** through 2 IP, Marsh **0-1** (in progress).

## 2026-07-25 lessons (MAE ~2.00, n=29; Paredes scratched)

| What happened | Lesson |
|---------------|--------|
| Soft O4.5 edge≥0.75 went **6/7**; clear/low **4/4** | Keep O4.5 clear/low as the primary over lane |
| **Imanaga O4.5** (proj 4.63 → 4) missed | Thin O4.5s (edge under ~1.0, especially medium risk) are **leaks** — need ~1.0+ edge or stick O3.5 |
| **Bibee U4.5** (proj 4.03 → 5) missed | Soft **U4.5** when proj sits ~4.0 is too tight — prefer **U5.5** or pass |
| **Young U5.5** (proj 4.33 → 6) missed | Low-K projection ≠ locked under; leave room or demand wider edge |
| **Pallante** 3.93 → **8** | Clear + soft proj can still spike — don’t skinny-under without cushion |
| **Greene** 6.72 → **3** (medium SPIKE) | Medium-risk SPIKE overs are volatile — need extra edge or pass |
| **Cease / Skenes** crushed overs | SPIKE upside is real — never soft-under them; O3.5 safer than forcing thin O4.5 on SPIKE |
| **Burke** volume / **Yoshi O4.5** (5 K) | Volume+clear O4.5 good; **O5.5 stretch** on Yoshi would have failed — treat O5.5 as juice only |
| **Mayza / short Vásquez** stayed down | Opener/short tags continue to save unders / fade full-outing overs |
| **Paredes scratched** | Confirm probable before betting thin boards |

### Reinforced card rules

1. **O4.5 core:** clear/low, edge ≥ ~1.0 preferred (≥0.75 minimum).
2. **O5.5:** only with proj ≥ ~6.3–6.5 and clear (Burke-tier volume) — not default.
3. **U4.5:** only if proj ≤ ~3.5 and non-SPIKE; otherwise **U5.5+**.
4. **Same-game:** pitcher K over ↔ opposing bats for hits is fine; never pitcher K over + that team’s bats for hits vs him.
5. Log misses into this file after each `backtest-YYYY-MM-DD.csv`.

## 2026-08-02 lessons (MAE ~1.94, n=28 starters)

Stronger night for volume overs; soft unders mixed again (Williams 10 spike).

| Solo grade | n | mean expK → act | Notes |
|------------|---|-----------------|-------|
| **ELITE** | 3 | 5.93 → 6.00 | **Burns 9**, Rea 7 (MATCHUP_OK cashed floor+); Keller 2 / 2 IP early hook |
| **STRONG** | 6 | 5.67 → 6.33 | **Misio 10**, Lambert 8, Freeland 8; Wheeler 3 / 2 IP early exit |
| **AVG** | 6 | 4.83 → 4.33 | Mostly quiet; Jax 8 upside |
| **SOFT** | 13 | 4.31 → 4.92 | 9/13 under 6; **Williams 10** and Liberatore/Ureña/Roupp spiked |

### Outlook report card

| Lean | Actual | Result |
|------|--------|--------|
| **O Misiorowski** | 10 K / 7 IP | **HIT** — volume strong/elite path |
| **O Burns** | 9 K / 6 IP | **HIT** — elite mix + length |
| **O Lambert / Freeland** | 8 / 8 | **HIT** — strong solo cashed |
| **O Wheeler** | 3 K / 2 IP | **MISS** — early exit (Completed Early) |
| **O Jump** | 5 K / 3.2 IP | thin / short |
| **U Bradish / Kay / Bennett** | 3 / 3 / 4 | **HIT** soft unders |
| **U Williams** | **10 K** | **MISS** — soft flip spiked (like 8/1 Rasmussen) |
| **U Rocker / Alcantara** | 5 / 5 | pushy vs U6 |

### Reinforced

1. **Volume + STRONG/ELITE + IP** is the over lane (Misio/Burns/Lambert).
2. **Early exits kill overs** even on strong mix (Wheeler, Keller).
3. **SOFT under still not locked** — Williams 10 after soft flip; prefer U6.5+ or low Exp K soft (Bennett/Kay/Bradish worked).
4. **MATCHUP_OK Rea 7** — floor over can cash, still not a nuke anchor thesis.
5. **Hart opener** 2 K / 3 IP — opener fade correct for full-outing overs.

## 2026-08-02 lessons (MAE ~1.98, n=30 modeled; BOS@LAD still In Progress)

Strong/elite overs cashed when they got length; soft unders mixed again — Williams **10** and Liberatore/Ureña/Roupp all cleared 6.

| Solo grade | n | mean expK → act | notes |
|------------|---|-----------------|-------|
| **ELITE** | 3 | 5.93 → 6.00 | Burns **9**, Rea **7**; Keller **2**/2 IP early hook |
| **STRONG** | 7 | 5.02 → 5.71 | Misio **10**, Lambert **8**, Freeland **8**; Wheeler rain short (3/2 IP) |
| **AVG** | 6 | 4.83 → 4.33 | Jax spiked **8**; Kirby/Bradley/Cavalli soft unders vs chalk |
| **SOFT** | 13 | 4.31 → **4.92** | **4/13 ≥6 K** — Williams **10**, Liberatore **7**, Ureña **7**, Roupp **6**; Kay/Bradish/Bennett/Montero under lane OK |

### Report-card style

| Lean type | Result | Note |
|-----------|--------|------|
| **O Misio / Burns / Lambert / Freeland** | 10 / 9 / 8 / 8 | Strong/elite + length — overs cashed |
| **O Wheeler / Keller** | 3 / 2 | Rain / early hook — IP killed overs |
| **O Rea MATCHUP_OK** | 7 K / 6 IP | Soft-contact + elite solo worked with length |
| **U Kay / Bradish / Bennett / Montero** | 3 / 3 / 4 / 2 | Soft under lane held |
| **U Williams (soft)** | **10 K** | Soft spike — never auto-U6 on soft with mid Exp K |
| **U Liberatore / Ureña / Roupp** | 7 / 7 / 6 | Soft cleared 6 again — prefer U6.5+ or low Exp K |

### Reinforced / adjusted

1. **SOFT still not automatic U6** (2nd straight night of spikes after 8/1) — require Exp K ≤ ~4.2 or line U6.5+, else pass.
2. **STRONG/ELITE + clear IP** remains the over path (Misio/Burns/Freeland); rain/early hooks (Wheeler/Keller) still kill.
3. **MATCHUP_OK with length** can cash (Rea 7) — still thin O3.5/O4.5 only without Exp K cushion.
4. **Sheehan / Bennett** still In Progress at grading — treat partial; don’t lock process lessons on unfinished outs.
5. **SPIKE reminder:** Williams soft→10 K — no soft unders on arms that can run K9 ≥ ~10.

## 2026-08-01 lessons (MAE ~2.21, n=23 starters)

Tough night for absolute SOFT unders — several soft-mix arms spiked Ks. Elite overs mostly short-outing misses.

| Solo grade | n | mean expK → act | vs O6 |
|------------|---|-----------------|-------|
| **ELITE** | 6 | 5.64 → 4.33 | 1/6 cleared O6 (Peterson 8); deGrom 3 / 3.1 IP, Abbott 1 |
| **STRONG** | 4 | 4.62 → 3.75 | 0/4 cleared O6 |
| **AVG** | 8 | 4.73 → **5.88** | Sánchez **11**, Mahle **9**, upside again |
| **SOFT** | 5 | 4.46 → **6.20** | **Failed under lane** — Rasmussen 10, Fried 7, Tolle 7, Messick 6; only Buehler 1 |

### Early outlook report card

| Lean | Result | Note |
|------|--------|------|
| **O Peterson** | **8 K** HIT path | Elite + length — only elite O6-style cash |
| **O Ashcraft / Prielipp** | 5 / 5 | Mix OK, no O6 |
| **O deGrom** | 3 K / 3.1 IP | Early hook — SPIKE/elite still needs IP |
| **O Gausman / Abbott** | 4 / 1 | Misses; Abbott high-risk flagged |
| **U Buehler** | **1 K** HIT | Clean soft under |
| **U Tolle / Fried / Messick / Rasmussen** | 7 / 7 / 6 / **10** | Soft solo **spiked** — do not treat soft as locked U6 |

### Reinforced / adjusted

1. **SOFT ≠ automatic under** after 8/1 — demand wider lines (U6.5+) or pass when Exp K ≥ ~5 or K9 is mid/high (Rasmussen/Fried/Tolle).
2. **ELITE still needs outing length** — deGrom 3.1 IP killed the over; prefer clear + IP ≥ ~5.5 for O5.5+.
3. **AVG upside continues** (Sánchez 11, Mahle 9) — not under chalk.
4. **Yamamoto / Baz → AVG fade** was correct vs forcing overs (3 K / 4 K).
5. **Phillips swingman MATCHUP_OK** (3 K) — fade full-outing chalk still right.

## 2026-07-31 lessons (MAE ~1.40, n=27 starters)

Solo absolute grade (`arsenal_abs_grade`) first full graded night.

| Solo grade | n | mean expK → act | vs U/O 6 |
|------------|---|-----------------|----------|
| **ELITE** | 7 | 5.19 → 4.71 | only 1/7 cleared O6; short outings (Skenes 7 K / 4 IP) |
| **STRONG** | 7 | 4.98 → 3.86 | 1/7 cleared O6 — strong ≠ automatic O6 |
| **AVG** | 6 | 4.87 → **6.17** | upside bucket (Warren 7, Cease 7, Wacha 7, Matthews **10**) |
| **SOFT** | 7 | 3.89 → 3.43 | **0/7 cleared O6**; 6/7 ≤5 K — best under lane |

### User ticket (Brown U6 / Eovaldi O6 / Sugano O3.5 / Drohan O6) → **2/4**

| Leg | Actual | Result | Lesson |
|-----|--------|--------|--------|
| **Brown U6** | 5 K / 5.2 IP | **HIT** | SOLO SOFT under with room under 6 — on-model |
| **Eovaldi O6** | 5 K / 5.0 IP | **MISS** | SOLO STRONG but Exp K ~6.1 → O6 is **zero-edge**; need O5.5 or more cushion |
| **Sugano O3.5** | 2 K / 6.2 IP | **MISS** | MATCHUP_OK / soft-contact floor over failed — disclose is not a cash |
| **Drohan O6** | 7 K / 6.0 IP | **HIT** | Cashed, but Friday lock was solo **AVG** (process pass) — result ≠ process proof |

Also: **same-game** Brown U + Eovaldi O (TEX@HOU) — both finished 5 K; correlated script risk.

### Reinforced

1. **SOFT solo = under lane** (esp. U6): 0/7 soft arms reached 6 K.
2. **ELITE/STRONG solo ≠ O6 chalk** — prefer O4.5/O5.5 unless Exp K ≥ ~6.8–7 + length.
3. **MATCHUP_OK O3.5** still fails (Sugano 2) — thin floor, not a 4-leg anchor.
4. **AVG solo overs** can spike (Matthews 10, Warren 7) — don’t treat AVG as under chalk either.
5. **Suarez 2 K** — sheet-green / solo-SOFT under thesis cashed; mix > season form.
6. **Fedde 6 K** — SOFT FILLER still spiked to 6; U6 on soft arms needs the cushion (prefer when Exp K ≤ ~4.5 or line U6.5+).

## Prior days (short)

- **7/26:** MAE ~2.09; O3.5 strong / O4.5 mixed; Ashcraft O5.5 miss; Misio 12; Sánchez early hook; Gausman fade wrong.
- **7/24:** Soft O3.5 ~76%, O4.5 ~67%; Miller 0 K killed multis; Manaea swingman fade / Way opener correct.
- **7/23:** MAE ~2.03; Sale U7 failed (SPIKE/high K night) — don’t soft-under elite K arms.

## Model upgrades (2026-07-27)

- **Outing survival:** `bf_risk_factor` now also haircuts for short recent IP and HR/xFIP+BB exit risk (floor 0.82).
- **Opp. lineup offense:** recent (else season) lineup K%/AVG → mild ±7% `offense_factor` on matchup Ks before form blend.
- Next: optional batter barrel/hard-hit layer for Hits props (not for pitcher K mean).

- **Hits board (2026-07-27):** barrel% / hard-hit% / xwOBA + AVG vs hand → `hits_score` / `hr_rbi_score` only. Explicitly isolated from `expected_ks`.

- **Ticket outlook (2026-07-28):** FILLER is no longer pitcher-only. Soft-contact profile is gated by opposing lineup **arsenal rank** (`expected_k_pct` percentile → `MATCHUP_OK` vs `FILLER`).
- **Plate discipline (2026-07-28):** opposing lineup **BB%** + K% shape → `discipline_grade` / `pitch_count_risk`. Patient/walk-heavy nines trim BF/IP and soften K projections (beyond raw batter K%).
