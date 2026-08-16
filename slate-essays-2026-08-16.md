# 2026-08-16 slate — OFF pitcher essays

**Skip 8/15 entirely** (per request). Soft Odds API pull is **blocked** this run (no `ODDS_API_KEY` / `ODDS_API_KEY_NEW` on the VM). Board refreshed with `--no-odds`: **28 official / 2 prior** (SEA@HOU: Woo / Brown still prior).

**Book “why” below** is market-structure reasoning from Exp K, name brand, SPIKE/UNDER chips, and length — not a live line snap. Re-run with `--odds-force` once the key is restored to attach real `k_line` / `k_edge`.

Process reminder: Ks = PA × volume; fat model edge ≠ ticket; never soft-under SPIKE; MATCHUP_OK = O3.5 + length; UNDER_OK needs Stuff+ check before chalk under.

---

## Snapshot (OFF, by Exp K)

| Arm | Exp | Solo / Style | Chip | IP / BF | Standout |
|-----|-----|--------------|------|---------|----------|
| Dobbins | 7.03 | elite / BAL | caution | 7.0 / 30 | Volume ceiling, not whiff |
| Cameron | 6.63 | elite / BAL | caution · whiff_prone LAA | 5.8 / 25 | Free-swing LAA |
| Cease | 6.39 | elite / WHIFF | TRUST · SPIKE stuff | 5.6 / 22 | K9 13.1 / SwStr 14.7 |
| Eury | 6.21 | elite / WHIFF | TRUST | 5.5 / 22 | Stuff+116 · 98 mph |
| D. Anderson | 6.18 | strong / WHIFF | TRUST · swingman | 6.6 / 28 | Volume vs CWS |
| Bachar | 5.82 | elite / WHIFF | TRUST · swingman · HR risk | 5.5 / 22 | Stuff whiff 32% |
| Skubal | 5.56 | strong / WHIFF | TRUST · attack bump | 5.7 / 22 | Stuff+118 · Strike% 68 |
| Lopez | 5.49 | elite / FLY | high risk BB/HR | 4.2 / 19 | Rate without length |
| Sandoval | 5.42 | elite / BAL | elev BB | 4.6 / 22 | PIT K% vs LHP |
| Painter | 5.15 | elite / BAL | high HR | 4.9 / 22 | vs soft MIN K% |
| Bradford | 5.11 | elite solo · soft profile | **MATCHUP_OK** | 5.6 / 23 | Soft stuff, elite PA |
| Rogers | 5.06 | avg / FLY | elev xFIP | 5.5 / 23 | Soft vs TB LHP |
| Hughes | 4.94 | strong / BAL | Stuff soft | 5.4 / 23 | SF contact-heavy |
| Henderson | 4.87 | avg / WHIFF | elev HR | 5.1 / 20 | Stuff vs LAD |
| Peralta | 4.80 | elite / BAL | elev BB/HR | 4.8 / 22 | BAL K% vs RHP |
| Weathers | 4.62 | avg / WHIFF | elev HR | 5.5 / 23 | TOR soft vs LHP |
| Scott | 4.57 | avg / WHIFF | elev BB · short IP | 4.4 / 19 | Stuff > volume |
| Burke | 4.57 | soft solo / WHIFF | **SPIKE** | 6.4 / 26 | K9 10.1 vs soft matchup |
| Soroka | 4.35 | avg / BAL | short recent IP | 5.0 / 20 | Neutral ATL |
| Lodolo | 4.25 | strong / BAL | high risk HR/BB | 4.7 / 21 | Damage lane live |
| Bibee | 4.06 | soft / BAL | **UNDER_OK** | 5.7 / 23 | Soft vs patient SD |
| Irvin | 3.96 | avg / FLY | high risk | 4.2 / 19 | Short + HR |
| Elder | 3.81 | soft / BAL | **UNDER_OK** | 5.7 / 24 | Soft vs AZ BIP |
| Cabrera | 3.70 | soft solo | **SPIKE** | 4.8 / 20 | 96 SI + whiff, soft PA |
| Mize | 3.59 | soft / FLY | **UNDER_OK** | 5.1 / 21 | CLE patient |
| Kremer | 3.01 | soft / BAL | high HR | 4.6 / 18 | PHI patient / BIP |
| R. Johnson | 2.88 | soft / BAL | **UNDER_OK** · high risk | 4.0 / 18 | Soft + blowup flags |
| Tidwell | 1.55 | elite / FLY | **opener** | 1.5 / 6 | Rate without BF |

**PRIOR (skip ticket lock):** Woo Exp 5.20 · Brown Exp 3.76 (**SPIKE**) — SEA@HOU ~6:20 PM CT.

---

## Essays (confirmed lineups)

### Hunter Dobbins (STL @ CHC) — Exp 7.0 · elite solo · BAL · caution
**Standout:** Top Exp on the board on **volume** (≈7 IP / 30 BF, 3× order), not elite stuff (Stuff+97, SwStr 9.4%). Arsenal K% 25.4 vs CHC’s OFF 1–9 is elite (+3.3 vs opp K%).
**Vulnerability:** `elev_hr` + BAL style — CHC can punish mistakes (PCA / Suzuki / Bregman). Not a WHIFF profile; contact stays in play.
**Matchup:** Good if he stays ahead and works deep; CHC K% vs RHP ~22% is workable, not a free-swing feast.
**Book why:** Books usually hang a **high 5s / low 6s** on long-outing mid-rotation arms with soft brand — Exp 7.0 is volume-led, so if the line is soft vs Exp it’s length pricing, not “ace K%.” Prefer O4.5 floor over juiced O6.5 until line snaps.

### Noah Cameron (KC @ LAA) — Exp 6.6 · elite · whiff_prone LAA · caution
**Standout:** Elite arsenal (26.6%) into a **free-swing** Angels card (lineup K% 30.6 / vs LHP 26.4). Location+105, clear outing.
**Vulnerability:** Stuff+97 / BAL style — Exp is matchup-inflated; if LAA slows down or he loses zone, rate collapses toward season K% (~21%).
**Matchup:** Best K lean of the late slate on PA quality (Trout / Neto / Siri mix still offers whiffs).
**Book why:** Market typically prices LAA K overs up on **opponent K% brand**; if they sit ~5.5–6.5 it’s that free-swing premium. Caution chip says don’t treat Exp 6.6 as nuke O6.5 without WHIFF style.

### Dylan Cease (TOR vs NYY) — Exp 6.4 · TRUST · WHIFF · SPIKE stuff
**Standout:** Elite stack — Stuff+107, K% 36, SwStr 14.7, L3 K9 13.0, whiff_prone NYY card. Season K brand is the product.
**Vulnerability:** `elev_bb` + Zone% 36.6 — walks eat BF and can shorten; three-true NYY (Rice / García / Ramos) will take if he nibbles.
**Matchup:** Excellent K matchup when he’s attacking; NYY still K’s enough vs RHP (~23%) for overs if volume holds ~22 BF.
**Book why:** Cease is a **name premium** — books set high (often 6.5+) on K9/L3 ceiling even when Exp is “only” mid-6s. SPIKE rule: never soft-under. TRUST overs confirm when line ≤ Exp.

### Eury Pérez (MIA @ CIN) — Exp 6.2 · TRUST · WHIFF · Stuff+116
**Standout:** Best pure stuff on the early slate (98 mph, stuff whiff 29%, Strike% 64). Elite solo vs CIN.
**Vulnerability:** Location+94 — when command wobbles, CIN’s power (EDLC / Suárez / Toglia) flips to damage. Not a walk flag today, but HR contact is live.
**Matchup:** Strong — CIN K% vs RHP ~25% and vs-team history hot (34% K in sample). Clear outing.
**Book why:** Books price Eury on **Stuff+/velo brand** into mid-6s; Exp≈that lane. Soft under forbidden on SPIKE-ish stuff ceiling even if line looks high.

### Drew Anderson (DET vs CWS) — Exp 6.2 · TRUST · WHIFF · swingman
**Standout:** Volume path (6.6 IP / 28 BF) + whiff_prone CWS + K9 10.3 / stuff whiff 29%. Exp rides length × rate.
**Vulnerability:** `short_recent_ip` + swingman role + `elev_hr` — leash risk; L3 only 4.2 IP / 3 K avg. Three-true CWS (walks) can pad pitch count.
**Matchup:** Good K/volume vs CWS if he’s stretched; don’t chalk full-outing outs blindly.
**Book why:** Non-ace brand → books often **soft** (4.5–5.5) vs Exp 6+ volume. Fat edge = question until role/IP confirm mid-game; O4.5 floor > juice.

### Lake Bachar (PIT vs BOS) — Exp 5.8 · TRUST · WHIFF · swingman · HR risk
**Standout:** Elite stuff whiff 32% / L3 K9 12.8 into elite solo grade vs patient BOS.
**Vulnerability:** `high_hr` / `exit_hr` / medium outing / short recent IP (2.1 L3) — BOS patient (BB% 11.8) will extend ABs; HR leash is the kill shot.
**Matchup:** Rate matchup is real (+3.4 vs opp K%); length is not.
**Book why:** Swingman + PIT brand → soft total; books may sit **4.5–5.5** while Exp says 5.8 on rate. Size O4.5 / thin O5.5; fade full-outing chalk.

### Tarik Skubal (LAD vs MIL) — Exp 5.6 · TRUST · WHIFF · Stuff+118
**Standout:** Attack-plate bump (+0.35): Strike% 68, Zone% 43, stuff whiff 31%, BB/9 1.5. Ace process with clear outing.
**Vulnerability:** MIL vs LHP K% only ~20% and **three_true** (patient walks) — Exp is tempered vs season K% 30.5. Relative matchup only avg.
**Matchup:** Still good because stuff dominates plate discipline when he’s in the zone; not a soft K card.
**Book why:** Ace tax — books set **high** (often 6.5+) on Skubal name even when Exp is 5.6 vs patient MIL. Book-high → size down / fade juice; TRUST floor still live on O4.5–O5.5.

### Jacob Lopez (ATH vs TEX) — Exp 5.5 · elite rate · high risk · short IP
**Standout:** Slate #2 arsenal K% 27.9 (+5.4 vs lg) — PA matchup screams Ks.
**Vulnerability:** Projected **4.2 IP / 19 BF**, `high_bb`/`high_hr`/`high_xfip` — rate without volume. FLY/popup + exit flags = damage co-path.
**Matchup:** Excellent K% vs TEX LHP card; terrible length/survival.
**Book why:** Books often split the difference — **mid-4s** — because ATH/Lopez blowup risk caps volume even when matchup K% is elite. Don’t juice overs past volume; hits/ER co-live.

### Patrick Sandoval (BOS @ PIT) — Exp 5.4 · elite solo · elev BB
**Standout:** Stuff+103 + PIT lineup K% 28.5 / vs LHP 26.3 — real whiff_prone opponent.
**Vulnerability:** Medium risk, elev BB/xFIP, only ~4.6 IP — walks vs a free-K PIT card still burn BF.
**Matchup:** One of the cleaner K overs on PA quality if he throws strikes.
**Book why:** Mid-rotation LHP vs high-K PIT → books usually **5.5-ish**. Exp≈aligned; edge comes from PIT K% not Sandoval brand.

### Andrew Painter (PHI @ MIN) — Exp 5.2 · elite solo · high HR
**Standout:** Elite arsenal (24.6%) vs soft MIN K% vs RHP (~19.6) — +5 vs opp. FF 96.5 / Stuff+101.
**Vulnerability:** `high_hr`/`exit_hr`/`elev_xfip` — MIN’s contact can go deep; medium outing; season K% only 19%.
**Matchup:** Good for K *rate* if he misses bats early; damage lane is co-equal.
**Book why:** Prospect/young-arm premium can push books **high** vs soft MIN K profile. Soft matchup solo is elite; don’t confuse with “safe ace.” Prefer O4.5; watch HR exits.

### Cody Bradford (TEX @ ATH) — Exp 5.1 · **MATCHUP_OK**
**Standout:** Soft-contact profile (K9 4.8, Stuff+84) but **elite solo arsenal K% 24.5** into aggressive ATH (BIP 72%, low BB%). Location+110 carries him.
**Vulnerability:** Soft stuff / high xFIP — Ks are PA-driven, not swing-and-miss. ATH contact-heavy can BIP him to death if zone fails.
**Matchup:** Classic MATCHUP_OK — disclose soft profile; O3.5 / thin O4.5 only.
**Book why:** Soft brand → books often **3.5–4.5**. Fat Exp-vs-line gaps are matchup K%, not TRUST. Size O3.5 floor; outs over if IP holds.

### Trevor Rogers (BAL @ TB) — Exp 5.1 · avg solo · FLY · elev xFIP
**Standout:** Length path (~5.5 IP) + L3 K9 10.7 spike flag; TB aggressive BIP (75%).
**Vulnerability:** Soft relative matchup (arsenal 20.6, opp K% vs LHP ~18%). Contact-heavy TB wants BIP outs, not Ks. FLY/popup = HR risk in Trop.
**Matchup:** Mediocre K; better outs/BIP if you need a prop lane.
**Book why:** Books price Rogers as mid-4s/5s on name + IP; Exp 5.1 is length, not elite rate. Soft over only if line ≤4.5.

### Gabriel Hughes (COL @ SF) — Exp 4.9 · strong solo · soft stuff
**Standout:** Arsenal +4.4 vs SF’s soft K% vs RHP (~18.7); clear outing; park helps pitcher.
**Vulnerability:** Stuff+86 / stuff whiff 20% — SF aggressive contact (BIP 72%) will put balls in play. Season K% ~22% needs volume.
**Matchup:** Mild positive on PA; not a whiff feast.
**Book why:** COL arm + soft stuff → soft book (often **3.5–4.5**). Exp 4.9 needs BF; don’t juice O5.5.

### Logan Henderson (MIL @ LAD) — Exp 4.9 · WHIFF · elev HR
**Standout:** Season K% 32 / Stuff+105 / L3 K9 ~11 into Dodger Stadium — stuff is real.
**Vulnerability:** Only ~20 BF / elev HR vs LAD wRC+ 117 — damage risk; relative matchup only avg (opp K% vs RHP ~20%).
**Matchup:** Neutral-to-soft for K overs; WHIFF style keeps SPIKE caution on soft unders if line is juiced.
**Book why:** Young WHIFF arm vs LAD → books may sit **5.5** on stuff brand while Exp is 4.9 (book-high fade zone). Prefer pass / O4.5 max.

### Freddy Peralta (TB vs BAL) — Exp 4.8 · elite solo · elev BB/HR
**Standout:** Elite arsenal grade vs BAL K% vs RHP ~25%; stuff whiff 26%.
**Vulnerability:** Medium risk triple flag (BB/HR/xFIP) + ~4.8 IP — BAL neutral discipline still takes walks.
**Matchup:** Solid K PA; length/command are the brakes.
**Book why:** Peralta brand often **5.5+**; Exp 4.8 = possible book-high. Size down overs; damage co-live.

### Ryan Weathers (NYY @ TOR) — Exp 4.6 · WHIFF · avg matchup
**Standout:** Stuff+103 / stuff whiff 28% / clear-low outing; TOR soft vs LHP (~18% K).
**Vulnerability:** Opp doesn’t whiff enough — Exp sits avg despite WHIFF style. `elev_hr` vs TOR contact.
**Matchup:** Stuff > opponent K%; overs need him to miss over the heart.
**Book why:** Yankee starter brand can inflate line above Exp. If book ≥5.5 with Exp 4.6, fade juice / prefer unders only if not SPIKE (not flagged).

### Christian Scott (NYM vs WSH) — Exp 4.6 · WHIFF · short IP
**Standout:** Stuff+107 / K9 11.3 / L3 K9 high — pure stuff.
**Vulnerability:** Soft relative matchup + only **4.4 IP / 19 BF** + elev BB — volume dies first.
**Matchup:** WSH K% vs RHP soft (~19%); rate needs chase that may not come.
**Book why:** Prospect stuff premium → book often **high** vs Exp. Classic book-high / length fade on K overs.

### Sean Burke (CWS @ DET) — Exp 4.6 · **SPIKE** · soft solo
**Standout:** K9 10.1 + WHIFF style + **6.4 IP / 26 BF** volume — SPIKE despite soft arsenal vs DET (17.4% expected K%).
**Vulnerability:** DET contact-heavy BIP (72%); solo soft — Exp is volume floor, not matchup K%.
**Matchup:** Poor PA K%; good length. Never soft-under SPIKE (Ashcraft lesson).
**Book why:** Soft CWS brand → books may hang **4.5–5.5** while SPIKE stuff can clear 6+. Unders only U6.5+ or pass.

### Michael Soroka (AZ @ ATL) — Exp 4.4 · avg / avg
**Standout:** Location+106, BB/9 2.1, aggressive ATL (chase). Clean-ish profile.
**Vulnerability:** Short recent IP; Stuff+94; no real K edge vs ATL (~22% vs RHP).
**Matchup:** Neutral — neither TRUST over nor UNDER_OK.
**Book why:** Mid-4s chalk. Exp≈aligned; no fat edge story.

### Nick Lodolo (CIN vs MIA) — Exp 4.3 · strong solo · high risk
**Standout:** Stuff+106 + strong absolute grade vs MIA.
**Vulnerability:** `elev_bb`/`high_hr`/`exit_hr`/high outing risk — damage thesis louder than Ks. ~4.7 IP.
**Matchup:** OK K%; better hits/ER lane if flags print.
**Book why:** Name + Stuff can push **5.5**; Exp 4.3 + HR flags = book-high / prefer damage overs on hits-ER.

### Tanner Bibee (CLE vs SD) — Exp 4.1 · **UNDER_OK** · soft
**Standout:** Soft arsenal (16.6%) vs patient SD (BB% 9.6, BIP 70%). Soft-contact profile + elev HR/xFIP.
**Vulnerability:** Stuff+103 keeps a floor — don’t chalk U3.5. Rain delay risk today (Delayed Start).
**Matchup:** Poor K matchup; UNDER_OK with 2 confirms.
**Book why:** Bibee brand often **5.5**; Exp 4.1 = book-high under lean if Stuff+ check OK (it is ~103 — size carefully, not nuke under).

### Jake Irvin (WSH @ NYM) — Exp 4.0 · FLY · high risk
**Standout:** Little on K side — avg solo, soft relative, short IP.
**Vulnerability:** High BB/HR/xFIP + exit_hr — Mets can punish fly balls.
**Matchup:** Weak K; damage live.
**Book why:** Soft WSH brand → low-4s. Aligned thin total; prefer pass / damage.

### Bryce Elder (ATL vs AZ) — Exp 3.8 · **UNDER_OK** · soft
**Standout:** Soft solo 16.8% / Stuff+85 / contact-heavy vs AZ BIP. Length (~5.7 IP) without Ks.
**Vulnerability:** elev HR — AZ power (Carroll / Marte) can end outing; UNDER_OK is K lane, not “good game.”
**Matchup:** Clear under profile on K props.
**Book why:** Elder often **4.5**; Exp 3.8 supports under if line ≥4.5. Stuff soft confirms UNDER_OK.

### Edward Cabrera (CHC vs STL) — Exp 3.7 · **SPIKE** · soft solo
**Standout:** SPIKE from **96 SI + 26.5% stuff whiff** despite soft PA grade vs STL contact-heavy.
**Vulnerability:** elev BB / high HR / exit_hr / medium risk — STL can BIP + walk him into short outing.
**Matchup:** Soft K%; SPIKE forbids soft under.
**Book why:** Cabrera velo brand → books may still hang **5.5** (book-high vs Exp 3.7). Fade K overs; no soft U4.5 — use U6.5+ or pass.

### Casey Mize (SD @ CLE) — Exp 3.6 · **UNDER_OK** · FLY
**Standout:** Soft solo vs patient CLE (BB% 11.9). FLY/popup out-getter; clear outing.
**Vulnerability:** Stuff only 89 — UNDER_OK OK, but CLE ISO/power still HR risk.
**Matchup:** Soft K; BIP outs > Ks.
**Book why:** Mize mid-rotation brand ~4.5; Exp 3.6 = mild under if line ≥4.5.

### Dean Kremer (MIN vs PHI) — Exp 3.0 · soft · high HR
**Standout:** Softest early Exp among full starters — PHI patient (BB% 13.4) + soft arsenal 16.9%.
**Vulnerability:** `high_hr`/`exit_hr` vs Schwarber/Harper — short leash; only 18 BF.
**Matchup:** Bad K; damage preferred.
**Book why:** Soft MIN brand → low-4s; Exp 3.0 still under-lean if ≥4.5, but HR exit can also kill unders via early hook (volume variance).

### Ryan Johnson (LAA vs KC) — Exp 2.9 · **UNDER_OK** · high risk
**Standout:** Soft-contact + soft solo + Exp ≤4.2 confirms UNDER_OK.
**Vulnerability:** `high_bb`/`high_hr`/`high_xfip`/`exit_*` — blowup shortens; KC can feast. Only ~4 IP.
**Matchup:** Poor K; chaos outing.
**Book why:** Soft LAA arm → **3.5–4.5**. UNDER_OK on K; prefer pass on outs. Damage co-path if you need action.

### Blade Tidwell (SF vs COL) — Exp 1.5 · **opener_likely** · elite rate
**Standout:** #1 arsenal K% 30% / Stuff+108 vs aggressive COL — rate is elite for one trip.
**Vulnerability:** **1.5 IP / 6 BF** — no full-outing K product. Opener_likely.
**Matchup:** Great for a short burst; useless for O3.5+ chalk.
**Book why:** If books post a starter line, it’s a trap — market sometimes mis-tags openers. Only micro O0.5/O1.5 style if offered; fade full-start overs.

---

## PRIOR — SEA @ HOU (~6:20 PM CT)

Wait for OFF before ticket lock.

- **Bryan Woo** — Exp 5.2 · Stuff+109 · avg matchup vs HOU. Ace-ish control (BB/9 1.9). Book will price name high; confirm HOU 1–9 first.
- **Hunter Brown** — Exp 3.8 · **SPIKE** · soft solo · `high_bb`. Never soft-under; OFF may move Exp hard.

---

## Process lanes (no live book)

| Lane | Arms |
|------|------|
| TRUST / K-first (size with line) | Cease, Eury, Skubal (floor), Bachar/Anderson (O4.5 / role check) |
| MATCHUP_OK (O3.5 only) | Bradford |
| SPIKE (no soft under) | Burke, Cabrera, (+ Brown PRIOR) |
| UNDER_OK | Bibee, Elder, Mize, R. Johnson |
| Damage / hits-ER co-path | Lodolo, Lopez, Painter, Irvin, Kremer, Peralta |
| Opener / no full K | Tidwell |
| Volume caution (BAL / soft brand) | Dobbins, Cameron |

*Re-pull soft lite odds (`--odds-force`) when `ODDS_API_KEY_NEW` is available — then rewrite book-why with real `k_line` / `k_edge`.*
