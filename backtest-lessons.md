# K-prop process lessons (from graded slates)

Living rules. Soft lines assume ~0.75+ edge unless noted.

## Learn from every miss (non-negotiable)

**Every mistake updates the routine before the next ticket.** Not only end-of-night grades — mid-slate misses count (Young 13 outs / 98 pitches → Zone%/efficiency now in Step 5).

When a locked leg loses or a lean is clearly wrong:
1. **What broke?** (side / total / length / efficiency / line / role)
2. **Write the rule** into this file (ticket lock + same-day note).
3. **Apply on the next card** — do not repeat the same miss.
4. Full-slate grade still runs after finals (`backtest-YYYY-MM-DD.csv`) and folds into the same living rules.

Hits reinforce; misses rewrite the checklist. No silent losses.

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

   For each arm include: **solo grade**, arsenal K%, vs league / vs opp K%, Exp K, outing risk, game/time, plus the **info lean** (3b).  
   Slate `#` and opp K% `#` are optional context only.  
   Also check **vs Team history** on each card (career K% vs that batting team + recent games with **HOME/AWAY** for the pitcher). Use history to confirm or caution the model side — not to override a clear absolute arsenal gate.  
   Mark the whole board **provisional** until official lineups post.

3b. **Info lean (default on every arm — not a full essay):** stack signals so outs-type is visible at a glance:
   - **Solo grade** → can the mix K *this* nine?
   - **STYLE** (WHIFF / GB / FLY / BAL) → does he usually get outs via Ks or BIP?
   - **Opp BIP / contact** (whiff_prone / neutral / contact_heavy) → will the nine help or fight Ks?
   - **Strike% / Zone%** (optional confirm) → does he attack the plate? High Strike% (≥~65) + Zone% supports WHIFF overs; low Strike% alone does **not** lock an under (SPIKE can still clear).

   One-glance combos: ELITE+WHIFF+whiff-prone = strong K info · ELITE+FLY/GB = matchup OK, don’t overweight K total · SOFT+GB/FLY+contact_heavy = strong under info · SOFT+WHIFF/SPIKE = soft grade but K ceiling live · AVG+WHIFF+juiced line = Cam-rule under info · WHIFF+Strike%≥65 = command confirms the K script.

3c. **Full thesis / essay (on request only):** when asked for a specific pitcher (or a short list), expand to Littell/Skubal depth — table of arsenal / opp BIP / STYLE / stuff·SPIKE / IP·risk, then answer “can we trust the K total?” and line-sizing. Do **not** essay the whole slate unless asked. Same daily routine, deeper read on demand.
4. **Re-refresh when lineups confirm** — same report shape, flip prior→official, re-check leans before locking tickets.
5. **Accuracy lock before firing** — official nine in, starter not opener, side matches arsenal vulnerability, line edge still holds.

This morning pack is the daily starting point — not optional.

## How to read the board on your own (60-second card)

Open a pitcher card and answer **four questions in order**. Do not start at Exp K.

| Step | Look at | Question | What it decides |
|------|---------|----------|-----------------|
| 1 | **ELITE / STRONG / AVG / SOFT** chip | Can his mix K *this* nine? | **Side** (over vs under bias) |
| 2 | **STYLE** chip (WHIFF / GB / FLY / BAL) next to name | Does he get outs via Ks or BIP? | Whether to **trust the total** |
| 3 | **Opp BIP** (whiff_prone / contact_heavy in meta) | Will the nine help or fight Ks? | Confirmation / line size |
| 4 | **SPIKE / THIN_TOTAL / UNDER_OK / MATCHUP_OK / FILLER** | Any veto or size cap? | Ticket legality |
| 5 | **Strike% / Zone%** (Rates row) | Does he attack the plate? | Command confirm — **not** a side flip |

**One-glance recipes**

| Stack | Read | Ticket move |
|-------|------|-------------|
| ELITE/STRONG + **WHIFF** + Exp K ≥5.5 | **Trust total** | Soft O4.5 / O5.5 OK if IP clear |
| ELITE/STRONG + **WHIFF** + Strike% ≥~65 | Attack-plate confirm | Size up over confidence if IP clear |
| ELITE/STRONG + **GB/FLY** + Exp K ≥5.5 | **THIN_TOTAL** | O3.5 / thin O4.5 only |
| ELITE/STRONG + **BAL** + Exp K ≥5.5 | Total caution | Prefer O4.5 floor; don’t juice O6.5 |
| SOFT + **UNDER_OK** (2+ confirms) | Preferred under | Soft U6 / BIP under |
| SOFT + SPIKE / WHIFF | Ceiling live | No soft U6; Cam U7+ or pass |
| MATCHUP_OK | Soft profile + good mix | Thin O3.5 only — never nuke |
| FILLER / opener | Bad K fit or short role | Pass K overs; outs alt maybe |

Also check: **Official** vs Prior · projected IP · outing risk · vs-team history (confirm only).

## Ticket lock routine (USE THIS before every card)

**User-locked 8/5–8/6.** Run this full path before recommending or firing any over/under. Exp K and slate `#` come last. Goal = find edge or pass.

### Step 0 — Setup
1. Refresh board; hard-refresh the link.
2. Filter **Official only** (prior = scouting only — do not lock).
3. Skip **openers / swingmen / unscored**.
4. Note the book line for that pitcher.

### Step 1 — Solo arsenal (picks the side)
| Grade | Edge bias |
|-------|-----------|
| ELITE / STRONG | **Over** |
| SOFT | **Under** |
| AVG | Usually pass / Cam-rule only |

This is the edge. Everything else confirms or sizes it.

### Step 2 — STYLE (trust the total?)
| STYLE | Meaning |
|-------|---------|
| **WHIFF** | Outs via Ks → juiced totals OK |
| **GB / FLY** | BIP outs → **THIN_TOTAL** (O3.5 / thin O4.5 only) |
| **BAL** | Caution — don’t juice O6.5 |

Good mix + wrong style ≠ nuke over.

### Step 3 — Opp BIP / K%
| Opp look | Helps |
|----------|-------|
| **whiff_prone** (BIP ≤~64%) | Overs |
| **contact_heavy** (BIP ≥~71%) | Unders |
| **neutral** | No extra edge |

Confirm only — does not flip solo grade alone.

### Step 4 — Outlook chip (legal / illegal)
| Chip | Move |
|------|------|
| **TRUST** | Over live if IP clear |
| **THIN_TOTAL** | Thin over only — not a nuke |
| **UNDER_OK** | Preferred soft under |
| **SPIKE** | **No soft U6** |
| **MATCHUP_OK** | O3.5 / thin O4.5 only |
| **FILLER** | Pass K overs **and** soft unders |

If the chip vetoes → stop.

### Step 5 — Strike% / Zone% (command + outs efficiency)
Compare Rates row to slate **Avg Strike%** (~64%).
| Read | Use |
|------|-----|
| Strike% **≥~65** + WHIFF/TRUST | Size **up** K-over confidence |
| High Zone% + high Strike% | Attacks the plate — K script more live; **outs overs OK** |
| Zone% **&lt;~40–41** (soft / nibble) | **Outs over caution** — pitches burn without banking outs |
| Zone% **≥~43** + clear/low risk | Outs over efficiency confirm |
| Low Strike% + UNDER_OK stack | Soft K under OK |
| Low Strike% + SPIKE/WHIFF | **Do not** auto K-under |

**Outs efficiency (8/6 Young — always apply on outs O/U):**
- Soft Zone% + high pitches-per-out → shortens outs even when outing risk reads “low” (Young **13 outs / 98 pitches** vs ~17 proj).
- **Outs over:** prefer GB length; on FLY/THIN_TOTAL require Zone% ≥~43 **or** ≥~3 outs of cushion vs line. Pass thin FLY O14.5-type spots when Zone% is soft.
- **Outs under:** soft Zone% / medium-high risk / short recent IP **helps** the under (inefficiency = fewer outs). Still need line cushion; don’t fade chalk O0.5–O2.5 promos.
- Promo chalk (O0.5 / O2.5 outs) = length not required — separate from full-outing outs overs.

Command confirms the script. It does **not** create the K side.

### Step 6 — Length & risk
- Projected IP supports the line?
- Outing risk / early-exit flags?
- Exp K / proj outs vs line still has edge?
- **Cam rule:** name/SPIKE juiced ~1.0–1.5 above Exp K → under can be live on AVG/SOFT.

Short IP kills TRUST K overs and full-outing outs overs.

### Step 7 — Pre-ticket checklist (all must pass — read before every fire)
Use this as the comfort gate. If any box fails → **no ticket**.

**Setup**
- [ ] Board refreshed; line confirmed
- [ ] **Official** nine (promo chalk O0.5 OK on prior only if starter confirmed)
- [ ] **Starter** (not opener / swingman)

**Side / lane**
- [ ] Solo grade picks the K side (ELITE/STRONG over · SOFT under · AVG usually pass)
- [ ] Chip does not veto (TRUST / THIN / UNDER_OK / SPIKE / MATCHUP_OK / FILLER)
- [ ] Lane chosen: **Ks** or **outs** (not forcing the wrong prop)

**Confirms**
- [ ] STYLE fits the total (WHIFF→K juice OK · GB/FLY→thin K / outs lane)
- [ ] Opp BIP agrees enough (whiff_prone helps K overs · contact_heavy helps unders)
- [ ] Strike% / **Zone% efficiency** checked (soft Zone% → caution outs *overs*; can help outs *unders*)
- [ ] IP / risk / proj outs support the **posted line** (cushion holds)

**Card rules**
- [ ] Default **2-leg**; no same-game opposing K overs
- [ ] Arm on ≤2 tickets today; one nuke/chalk pair max
- [ ] Comfortable saying the lean in one sentence — if not, pass

### Where the edge is
- **K over edge:** OFF + ELITE/STRONG + WHIFF + (TRUST or clear IP) + (whiff_prone **or** Strike% ≥~65)
- **Attack-plate over pack (8/5 locked):** prefer arms that stack **ELITE/STRONG + WHIFF + Strike% ≥~65 / Zone% ≥~43** (Harrison 10, Rogers 9, Lopez 9, Skenes 6). Length still required (Detmers attack profile but 5 K / 4 IP). Skip THIN_TOTAL / MATCHUP_OK / BAL as nuke K overs even if Exp K is high.
- **K under edge:** OFF + SOFT + UNDER_OK (≥2 of GB/FLY · contact_heavy · Exp K ≤~4.2) + not SPIKE · line needs real cushion (pass flat U4.0 when Exp ~3.5)
- **Outs over edge (co-equal lane — 8/6 locked):** OFF + starter + projected IP holds (~≥5.5 → ~16.5+ outs) + outing risk **clear/low** + STYLE **GB/FLY** (or THIN_TOTAL / MATCHUP_OK / FILLER where Ks are the wrong prop) + **Zone% efficiency** (see Step 5). Length is the product — high risk / short IP / openers / soft-Zone% FLY = pass full-outing outs overs.
- **Outs under edge:** short/high-risk or soft Zone% inefficiency + line cushion; not vs chalk promos.
- **No edge (pass):** AVG mush on Ks · THIN_TOTAL *K nukes* · FILLER K overs · openers · SPIKE soft U6 · prior lineups (except tiny promo chalk) · outs overs on high-risk hooks · thin FLY outs overs with soft Zone%

### Dual ticket lanes (Ks **or** outs)
Every probable gets both reads. Chip decides the lane:
| Chip / stack | K ticket | Outs ticket |
|--------------|----------|-------------|
| TRUST / attack-plate WHIFF | **K over** | usually pass (Ks are the product) |
| THIN_TOTAL / FLY or GB + length + Zone% OK | thin K only | **outs over** preferred |
| THIN_TOTAL / FLY + soft Zone% | thin K only | **pass** thin outs over (Young) |
| MATCHUP_OK / FILLER + clear-low IP + Zone% OK | pass / O3.5 K | **outs over** if IP holds |
| UNDER_OK | **K under** (line cushion) | outs under if short/high-risk or soft Zone% |
| SPIKE soft solo | no soft K under | outs OK if length + efficiency clear |
| Promo chalk O0.5 outs | — | **fire** if he starts (pair with real leg) |

Pair across lanes freely (e.g. Ashcraft K over + Peterson outs over). Still default **2-leg**; no same-game opposing *K* overs.

### Fast edge test
> Solo says over or under → does STYLE allow that total → Ks or outs lane? → Zone% efficiency OK for outs? → does BIP agree → does the chip allow the ticket → does Strike%/IP support it?

Any **no** → **no edge** → pass.

### 8/5 attack-plate pack (remember for future cards)
User target overs that fit the new lens: **Harrison / Rogers / Detmers / Skenes / Lopez**.
Actuals: 10 / 9 / 5 / 6 / 9. Four clear cashes on soft O4.5+; Detmers only if line ≤4.5 (short IP). Apply this same filter on the next slate before locking overs.

## Better tickets (habit)

1. **Default = 2-leg.** K over + K under, **or** K over + outs over, or two outs overs. No 6-legs.
2. **Build from outlook chips, not Exp K rank.** Top of board ≠ best bet (Dobbins). Chip picks **Ks vs outs**.
3. **Pair complementary scripts:** attack-plate K over + THIN_TOTAL/GB outs over works; also TRUST K + UNDER_OK K. Avoid same-game opposing K overs.
4. **Line sizing:** K overs need IP + trust; K unders need confirms or U6.5+; outs overs need clear/low risk + proj outs vs line. Cam rule: if book juices name/SPIKE above Exp K by ~1.0–1.5 on AVG/SOFT, K under is live.
5. **Accuracy lock:** run the **Ticket lock routine** above — do not skip steps.
6. **Cap:** any arm on ≤2 tickets; one nuke/chalk pair max per day.

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

**Stuff ceiling (velo/whiff by pitch)** — separate from solo grade. Usage-weighted pitcher-own whiff% + primary FB velo → `stuff_grade` / **SPIKE** chip. Soft solo **+ SPIKE** = do **not** auto-under (U6.5+ or pass). Does not move Exp K.

**Lineup contact / BIP** — opposing nine’s balls-in-play rate (`lineup_bip_pct`) + `contact_grade` (`whiff_prone` / `neutral` / `contact_heavy`). Contact-heavy BIP trims Exp K; whiff-prone (high K% / low BIP) boosts it. Secondary to solo arsenal grade — sizes the number, doesn’t flip the side.

**Pitcher style (Ks vs BIP outs)** — season FanGraphs K%/Contact%/GB%/FB%/IFFB → `pitcher_style` chips (`P-WHIFF` / `P-GB` / `P-FLY` / `P-BAL`). Confirmation only (no Exp K move). WHIFF confirms overs / SPIKE caution on soft unders; GB/FLY = outs via contact — soft matchup strengthens under; don’t force huge overs on elite mix + contact style without length.

**Total-trust gate (THIN_TOTAL) — added after 8/4:** ELITE/STRONG with Exp K ≥ ~**5.5** only **fully trusts** the juiced total when STYLE is **WHIFF**. STYLE **GB/FLY** → board outlook **THIN_TOTAL** (O3.5 / thin O4.5 only — Dobbins 7.7→4). STYLE **BAL** → soft “total caution” note (prefer O4.5 floor; Manaea 6.8→7 still OK). Mix side can still be a thin over; the *total* is the leak on BIP-out styles.

**Under confirmation (UNDER_OK) — added after 8/4:** SOFT non-SPIKE needs ≥**2 of 3**: GB/FLY style · opp **contact_heavy** BIP · Exp K ≤ ~**4.2**. Passes → **UNDER_OK**. Fewer → weak under (prefer U6.5+ or pass). SPIKE still vetoes soft U6. Best 8/4 lane: Dobnak/Assad (SOFT+GB+contact-heavy).

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
- **Good-pitcher unders (line vs Exp K) — Cam rule:** books often set lines off **name / K9 / SPIKE ceiling**, not arsenal vs *this* nine. Edge = **Exp K well under the posted line** even on WHIFF/SPIKE arms.
  1. Exp K (fair) vs book line (ask) — want ~**1.0–1.5+ K** of cushion for unders.
  2. Solo grade **SOFT or AVG** vs that nine (ELITE/STRONG → not an under).
  3. STYLE/SPIKE size the *line*, not the side: **SOFT+SPIKE+WHIFF** → only **wide** unders (Cam U7 with Exp K ~5.4); non-SPIKE soft/avg → U6.5 OK if edge holds.
  4. Opp **contact_heavy** BIP strengthens the under; whiff-prone opp fights it (need extra line cushion).
  - **Cam 8/3:** Exp K ~5.4, STYLE WHIFF + SPIKE, book **7** → U7 edge; actual **6** in 3 IP cashed.
  - **Javier 8/3:** Exp K ~2.9, SOFT + TOR contact_heavy → under vs juiced name line; actual **2**.
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

## 2026-08-06 in-progress (outs lane)

| Leg | Model | Actual | Result |
|-----|-------|--------|--------|
| **Young O14.5 outs** (THIN_TOTAL / FLY · proj ~17 outs · risk low · Zone% 40.1) | Length alt vs K nuke | **13 outs / 98 pitches** (~4.1 IP) | **MISS** — inefficient outing; pitch count maxed before outs |
| **Peterson O16.5 outs** (GB · proj ~17.3 · risk low · Zone% 41.8 · flags elev_bb, **short_recent_ip**) | Preferred GB outs lane | **15 outs / 5.0 IP / 89 pitches** (3 BB, 7 H, Strike% .600) | **MISS by 1** — thin cushion; L3 length warned |

**Lessons locked:**
1. **Zone% + pitch efficiency** (Young) — soft Zone% / high pitches-per-out kills outs overs even when risk reads low.
2. **Line cushion + recent IP** (Peterson) — ~17.3 proj vs **O16.5** is only ~0.8 outs of edge; need ~**2+ outs** cushion when `short_recent_ip` / elev_bb / soft-mid Zone% is on the card. Respect **L3 IP** (his was ~4.7) — don’t fully trust season IP for outs overs.
3. Prefer GB length still, but **thin GB outs overs fail the same way** (traffic → 5.0 IP pull). Never fade O0.5 / soft promo chalk.

Live / next: Ashcraft O2.5 leg status · **Buehler O0.5 + Miller O3.5** · Suarez O10.5 later (non-promo pair).

## 2026-08-05 lessons (MAE ~2.21, n=23 Final scored; 6 still live at grade)

First night with **TRUST / UNDER_OK / THIN_TOTAL** + new **Strike%/Zone%** on the board. Model **understated** Ks (bias **+1.01**); whiff_prone nines and several soft/SPIKE arms ran hot.

| Solo grade | n | mean expK → act | Notes |
|------------|---|-----------------|-------|
| **ELITE** | 4 | 5.42 → **7.00** | Harrison **10**, Pérez **9**; Detmers TRUST 5 / 4 IP short; Whisenhunt 4 |
| **STRONG** | 3 | 5.25 → **7.00** | Lopez **9**, Imanaga **6**; Skenes TRUST **6** (nail) |
| **AVG** | 6 | 4.69 → 5.50 | Rogers **9**, Gray **8**, Scott **7**; Lauer FILLER **1** |
| **SOFT** | 10 | 4.21 → 4.90 | Bibee FILLER **10**, Cameron **9**, Brown SPIKE **8**; UNDER_OK lane held |

### Ticket leans (Final)

| Lean | Actual | Result |
|------|--------|--------|
| **TRUST Detmers** | 5 K / 4 IP | Soft miss — mix OK, length died |
| **TRUST Skenes** | **6 K** / 5 IP | **HIT** — chalk trust total |
| **UNDER_OK Sugano / Lowder / Irvin** | 3 / 3 / 3 | **HIT** — all ≤ Exp K, contact-heavy soft |
| **SPIKE Brown** (no soft U6) | **8 K** | Veto **correct** — soft under would have died |
| **SPIKE Burke** | 4 K | Soft side OK; SPIKE still right to block auto-U6 |
| **FILLER Bibee** | **10 K** | Never soft-under FILLER; never K-over anchor |
| **ELITE Harrison** (thin IP ~4.6) | **10 K** / 5 IP | Volume spike — Strike% 66.5 confirmed attack |

### Strike% / Zone% (new layer) — did it help?

Raw corr vs actual Ks was near **zero** alone (Strike% +0.07, Zone% +0.00) — **not a solo predictor**. Useful as **command confirm on WHIFF / over scripts**:

| Stack | Read from 8/5 |
|-------|----------------|
| **WHIFF + Strike% ≥65** | Harrison 10, Detmers 5 (short), Burke 4 — ceiling live when SPIKE/ELITE; length still required |
| **High Strike% + Zone% (attack plate)** | Rogers 68.6/44.4 → **9**; Harrison 66.5/42.8 → **10** — home-plate attack helped K conversion |
| **Low Strike% ≠ auto under** | Brown **59.6** Zone 37.6 → **8** (SPIKE/WHIFF); Lopez **60.3** → **9** |
| **UNDER_OK + low-mid Strike%** | Sugano/Lowder/Irvin ~61–62.5 → all **3 K** — command soft + contact-heavy stacked |

**Process add:** after solo → STYLE → BIP, glance **Strike%/Zone%**. If WHIFF/TRUST over and Strike% ≥ ~65 (slate avg was **64.0%**), trust the K script more. If Strike% is soft, do **not** flip a SPIKE/WHIFF arm to under — use it only to size UNDER_OK / pass juiced overs on nibble arms.

### Reinforced

1. **TRUST** works when IP holds (Skenes); short outing kills Detmers-tier totals.
2. **UNDER_OK** 3/3 — keep as preferred soft-under badge.
3. **SPIKE veto** on Brown saved the soft-under trap.
4. **FILLER can spike** (Bibee 10) — pass both K overs and soft unders.
5. **Strike%/Zone% = confirm, not side** — attack-the-plate helps WHIFF overs; does not invent unders.

## 2026-08-04 lessons (MAE ~1.61, n=24 Final; 6 still live at grade)

Process night for STYLE / BIP / SPIKE. ELITE totals overstated without WHIFF; contact-heavy soft unders were the clean lane.

| Solo grade | n | mean expK → act | Notes |
|------------|---|-----------------|-------|
| **ELITE** | 7 | 5.81 → **4.14** | **−1.66 bias** — Dobbins 7.7→4, Tidwell 6.8→3, Yesavage 0 / 2 IP |
| **STRONG** | 2 | 5.97 → 6.00 | Manaea **7**, Cantillo **5** — held |
| **AVG** | 6 | 4.58 → 5.17 | Henderson **8** SPIKE upside; Ryan soft |
| **SOFT** | 9 | 3.93 → 3.67 | Non-SPIKE under lane OK; Luzardo/Weathers SPIKE cleared 6+ |

| Layer | Signal |
|-------|--------|
| **contact_heavy** (n=4 Final) | mean act **~2.0** — Dobnak 1, Assad 3, Palmquist 0 |
| **whiff_prone** | mixed — Manaea/GRod OK; did **not** save Tidwell total |
| **STYLE WHIFF** | +0.5 bias; **GB** −0.9 (BIP outs) |
| **SOFT+SPIKE** | Luzardo **7**, Weathers **6** — SPIKE veto correct |
| **MATCHUP_OK** | Povich **7** / Tidwell **3** — thin-only rule kept |

### Reinforced / shipped

1. **THIN_TOTAL** — ELITE/STRONG + Exp K ≥5.5 + non-WHIFF → thin overs only (Dobbins/Tidwell).
2. **UNDER_OK** — SOFT non-SPIKE needs ≥2 of GB/FLY · contact-heavy · Exp K ≤4.2 (Dobnak/Assad).
3. SPIKE still blocks soft U6; MATCHUP_OK stays O3.5 / thin O4.5; 2-leg default.
4. Do **not** retune BIP ±7% or move STYLE into Exp K off one night.

### Discussed legs (partial)

| Leg path | Actual | Note |
|----------|--------|------|
| Dobbins high Exp K over | 4 K / 6.1 IP | THIN_TOTAL prototype (ELITE+GB) |
| Cantillo over | 5 K | STRONG+WHIFF floor OK |
| Dobnak under / floor | 1 K | UNDER_OK stack cashed |
| Luzardo soft under | 7 K / 8 IP | SPIKE veto — pass was right |
| Tidwell MATCHUP_OK nuke | 3 K | thin-only validated |
| Singer soft under | 6 K | weak under (no contact-heavy) |

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
