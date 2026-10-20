# World Series preview — TB vs MIL · 2026

**Provisional** until G1 probables + OFF nines. Not a ticket lock.  
Model: `rankings-2026-ws-preview.csv` · `hits-2026-ws-preview.csv` · matchups `matchups-2026-ws-preview.csv`  
Lineups: **MIL prior 10/15 (NLCS G4)** · **TB prior 10/19 (ALCS G6 OFF)**. Re-run with `--require-official-lineup` when G1 posts.

Series: **TB @ MIL G1–G2** (Fri 10/23, Sat 10/24) · off Sun · **MIL @ TB G3–G5** (Mon 10/26–Wed 10/28). G6–G7 would return to Milwaukee if needed. G1 first pitch **7:00 PM CT** (2026-10-24T00:00:00Z). No probables posted yet.

Honor G4–G6 locks: CONFIRM 2-man · O1.5 ≠ O0.5 · opener dump-HOT ≠ A-ticket · SPIKE / Stuff+≥105 blocks chalk soft under · Caminero fires vs LHP bulk · Palacios pass-fade · Kwan-type fade power not O0.5 Hits.

---

## What the series is

| Side | How they got here | Rest into G1 |
|------|-------------------|--------------|
| **MIL** | Swept LAD **4–0**. Bullpen closed it (Romero / Ashby / Hall / Megill). Starters were short: Misi **4.1**, Henderson **4.0**, Gasser **5.0**, Drohan **1.0**. | **~8 days** (last pitch 10/15 night) |
| **TB** | Beat CLE **4–2**. Length + Hits: Rasmussen **7 IP G5**, Peralta **W in G2 + G6** at the Trop. Bullpen leaked the G6 8th; Baker closed. | **~3 days** (G6 10/19) |

**Script:** Milwaukee is lined up and rust-risk; Tampa is hotter with a shorter turn. Expect **MIL SPIKE short outings** (then a real bullpen) vs **TB length / Trop Peralta**. Do not copy ALCS opener tickets onto this series — Milwaukee is not running Armstrong-style openers except the Drohan G4 mess.

Home field is Milwaukee (G1–G2, G6–G7). Tampa’s edge is G3–G5 at the Trop, where Peralta already went **6 IP 6 K 0 ER** (G2) and **5.1 IP 3 K W** (G6).

---

## Likely rotations (not announced)

**MIL — NLCS order, all extra rest**

| Game | Arm | Last | NLCS box | Rest into that WS game |
|------|-----|------|----------|------------------------|
| G1 @ MIL | **Jacob Misiorowski (R)** | NLCS G1 10/11 | 4.1 IP · **5 K** · 5 H · 1 ER · 3 BB · 94p | 12 days |
| G2 @ MIL | **Logan Henderson (R)** | NLCS G2 10/12 | 4.0 IP · **2 K** · 3 H · 2 ER | 12 days |
| G3 @ TB | **Robert Gasser (L)** | NLCS G3 10/14 | 5.0 IP · 3 K · 3 H · **0 ER** | 12 days |
| G4 @ TB | **Shane Drohan (L)** | NLCS G4 10/15 | **1.0 IP** · 1 K · 2 BB · May ate 3 | 11 days |

Two lefties in Tampa (G3–G4) is the **Caminero / Mesa LHP** window.

**TB — most rested first; Peralta Trop G3 is the other live branch**

| Game | Arm | Last | ALCS box | Rest |
|------|-----|------|----------|------|
| G1 @ MIL | **Rasmussen (R)** *or* Jax (R) | Ras G5 10/18 · Jax G3 10/15 | Ras **7 IP 6 K W** · Jax **4 IP 2 K L** | 5 / 8 days |
| G2 @ MIL | **Martinez (R)** *or* Jax | G4 10/17 | 5.1 IP · 3 K · W | 6–9 days |
| G3 @ TB | **Peralta (R)** | G6 10/19 | 5.1 IP · 3 K · **W** (G2 was 6 IP 6 K 0 ER) | 7 days if skipped G1 |
| G4 @ TB | leftover of Jax / Martinez / Ras | | | |

**G1 toss-up:** Rasmussen is the LCS stopper; Jax has the rest but the G3 dud. Peralta on 4 days *could* go G1 ace-vs-ace vs Misiorowski — that *worsens* his Trop G3 rest. Until announced, treat **Misi vs Rasmussen** as the base G1 and **Peralta G3 at home** as the TB K game.

---

## Pitcher K matrix (model vs last nines)

Solo grade decides the side. SPIKE / Stuff+ / STYLE size the number. MIL is **whiff_prone** (BIP 59.8 · K% 27.4 · three_true). TB G6 is **neutral** (BIP 70.1 · K% 20.5).

| Arm | Exp K | Solo | STYLE | Stuff | Chip | LCS K/IP | Series read |
|-----|-------|------|-------|-------|------|----------|-------------|
| **Peralta vs MIL** | **5.51** | **STRONG** 23.8% | BAL | Stuff+97 | total caution | 6 K/6 + 3 K/5.1 | **Flip from ALCS.** Vs CLE he was SOFT/UNDER_OK Exp ~4. Vs this Brewers nine he is the only **STRONG** arm. **O4.5 floor** — not O6.5 (BAL, not WHIFF). Medium risk / Zone% still soft. |
| **Rasmussen vs MIL** | 4.65 | **SOFT** 18.7% | **WHIFF** | **Stuff+110** | weak under (0 confirms) | 7 K/6 + **6 K/7** | G5 lock applies: **no chalk soft under**. WHIFF + Stuff+110 + MIL K-prone. Length is the TB G1 path. Hits vs him, not U4.5. |
| **Misiorowski vs TB** | 4.38 | **SOFT** 17.9% | **WHIFF** | **Stuff+128** · FF 100.6 · whiff 37% | **SPIKE** | **5 K / 4.1** vs LAD | Cam/Williams rule. **Never U6.** Exp 4.4 vs a juiced name line → only wide U6.5+ or pass. Short NLCS outing → TB Hits **after exit** are incomplete vs-SP. |
| **Jax vs MIL** | 4.28 | AVG 22.1% (shy of STRONG) | WHIFF | elite / SPIKE | no over gate | 2 K / 4.0 vs CLE | Elite stuff, **4.3 IP proj**. Thin total. Don’t nuke O5.5. |
| **Martinez vs MIL** | 4.20 | **SOFT** 17.7% | **FLY** | soft · K9 5.5 | **UNDER_OK** | 3 K / 5.1 | McLean vs a shiny opp K%: mix is still under. MIL **whiff_prone fights it** — **U6.5+ or pass**, not U4.5. FILLER on K overs. Prefer **MIL Hits**. |
| **Drohan vs TB** | 4.13 | SOFT | BAL | strong | weak under | **1.0 IP** NLCS G4 | Pass juiced K. If he lasts 1 IP again, TB leans vs him are **incomplete**. Hits vs LHP if he works as a starter. |
| **Henderson vs TB** | 4.04 | SOFT | WHIFF | SPIKE · K9 10.1 | **SPIKE** | **2 K / 4.0** vs LAD | SPIKE veto on soft U6 even though NLCS Ks didn’t print. Short outing → TB Hits vs pen. |
| **Gasser vs TB** | **3.77** | SOFT | **FLY** | Stuff+106 | **UNDER_OK** | 3 K / 5.0 0 ER | Legal under **U5.5+** (Exp 3.77, FLY). Stuff+106 is *below the WHIFF veto shape* but not a skinny U3.5. **TB Hits vs LHP are the better ticket** (Caminero / Mesa). |

### K tickets to expect (not locked)

1. **Peralta O4.5** when he starts vs MIL — only STRONG / over-gate arm in the series. Size down if book juices O5.5+.  
2. **No soft under on Misi / Henderson / Rasmussen / Jax.** SPIKE or Stuff+110.  
3. **Martinez / Gasser** are the under *labels* — Gasser U5.5+ if he starts; Martinez only wide (U6.5+) because MIL Ks.  
4. **Drohan:** pass K; live-lean the first long arm if he hooks.

---

## Batter leans (series-long)

### TB vs MIL righties (Misi / Henderson — likely G1–G2)

Board vs R: **Caminero 59.5 / Yandy 59.0 / Aranda 57.0 / Hicks 52.1 / Mesa 51.0**.

| Tier | Bat | Prop | Why | Lock reminder |
|------|-----|------|-----|----------------|
| **BEST** | **Yandy** | Hits O0.5; 2+ only if multi tape | CONFIRM-style heart / multi. Cashed ALCS G5 3-5 and G6 1-hit HR (O0.5 HIT / 2+ MISS) | O1.5 ≠ O0.5 |
| **BEST** | **Aranda** | Hits O0.5 | Board + LHB. Not a 2-man A vs a 4-IP SPIKE | Opener dump-HOT lesson: **tiny vs that arm**, full-game 2-man = Yandy/CONFIRM |
| **GOOD** | **Caminero** | Hits vs RHP only if dump isn’t COLD | Elite board. ALCS: COLD on Armstrong dump → pass vs opener; smashed LHP/late | Wait for zone overlap on Misi |
| **GOOD** | Hicks / Mesa | Hits O0.5 | G6 OFF upgrades. Hicks cashed; Mesa 0-3 | Size tiny until G1 maps |
| Pass fade | Palacios | — | G4 inverse + G6 2-4 2 RBI | **Pass hard fade** |
| Fade power | Simpson | not O0.5 Hits | 0 barrel · Kwan-type | Fade HRR/power only |

**If Misi/Henderson exit ≤2 IP:** void vs-SP fades; re-lean vs the **first long arm** (May / Hall / Romero). Incomplete heatmap.

### TB vs MIL lefties (Gasser / Drohan — likely G3–G4 **at the Trop**)

Board vs L: **Mesa 61.0 / Caminero 60.9 / Yandy 54.9 / Aranda 53.6**.

| Tier | Bat | Prop | Why |
|------|-----|------|-----|
| **BEST** | **Caminero** | Hits + HRR | ALCS lock: fire vs LHP. Vs Gasser K% only ~12.5. |
| **BEST** | **Mesa Jr.** | Hits / HRR | G6 add is the **#1 vs LHP** board (AVG .333 vs L). |
| **GOOD** | Yandy | Hits | Still the multi vs L; slightly softer than vs R. |
| Live | If Drohan is 1 IP again | Caminero/Mesa vs **May / next L or R bulk** | Don’t 2-man the opener PA |

**2-man vs LHP:** Caminero + Mesa (or Caminero + Yandy). Need ≥1 CONFIRM on G3 maps.

### MIL vs TB righties (all four TB starters)

Board (same vs Ras/Peralta/Jax/Martinez): **Bauers 59.4 / Mitchell 58.7 / Chourio 57.7 / Turang 55.8 / Contreras 54.4**. Frelick 42.3.

| Tier | Bat | Prop | Why |
|------|-----|------|-----|
| **BEST** | **Jake Bauers** | Hits / HRR | Series #1 vs TB R. NLCS G4 GOOD+ cashed **2B 2 RBI vs Glasnow** when dump-HOT Mitchell slept. |
| **GOOD** | **Mitchell / Turang** | Hits O0.5 | Glasnow KC-dump HOTs — **do not copy onto Peralta** (FF/CH dumps 3B side). Re-map G1/G3. |
| **GOOD** | Chourio | Hits O0.5 | Heart/mistake. Not 2+ without multi tape. |
| **GOOD** | Contreras | Hits | Contact, low K% vs R (~11–16). |
| **FADE** | **Frelick** | — | Soft board. Glasnow COLD fade held (0 H). |
| Careful | Yelich | tiny | Mid board 50. |

**Vs Peralta (STRONG):** size MIL Hits as O0.5, not 2+ stacks. He can still give a 5.1–6 IP night. Bauers is the process bat; Mitchell 2+ is G5-style volume variance.

**Vs Martinez (UNDER_OK / FLY):** upgrade MIL Hits. Bauers + Mitchell is the 2-man if maps CONFIRM.

**Vs Rasmussen (Stuff+110 WHIFF):** same as G5 vs CLE — CONFIRM pack can go quiet. Prefer Bauers O0.5; don’t 4-man 2+/3+ HRR.

---

## Series 2-mans (process, still provisional)

| When | Ticket | Why |
|------|--------|-----|
| G1-ish vs Misi | **Yandy Hits + Bauers Hits** (cross) | Multi TB + MIL #1; opposite scripts |
| Vs Gasser LHP | **Caminero Hits + Mesa Hits** | LHP window at Trop |
| Peralta start | **Peralta O4.5 + Bauers Hits O0.5** | Only if G3 maps don’t COLD Bauers on the CH dump |
| Martinez start | **Bauers Hits + Mitchell Hits** | UNDER_OK FLY · MIL Hits > skinny K under |
| Avoid | Aranda 2-man A vs 4-IP SPIKE · same-bat 2H+3HRR nuke · Frelick · Palacios hard fade · Misi U5.5 | G4–G6 locks |

---

## How to watch it (live)

1. **G1 probables** — if TB names Peralta, the STRONG K game moves up and Trop G3 becomes someone else.  
2. **Misiorowski pitch count** — 94p in 4.1 NLCS. Hook → TB Hits vs first long arm (not vs the leftover 1 PA).  
3. **Gasser/Drohan posted** — flip TB card to Caminero + Mesa. Drohan 1 IP → incomplete.  
4. **Peralta CH on OUT-DN-3B** — if he’s landing it, MIL dump-COLD bats (need the maps) stay faded.  
5. Don’t fire G1 tickets on **prior** nines. Official lock + zone overlaps the morning of.

---

## One-glance

| Question | Answer |
|----------|--------|
| Who has the K over? | **Peralta vs MIL** (STRONG, Exp 5.5, O4.5 not O6.5) |
| Who is SPIKE / no under? | **Misiorowski, Henderson, Jax, Rasmussen** (Stuff+110) |
| Who is UNDER_OK? | **Gasser vs TB** (U5.5+) · **Martinez vs MIL** (U6.5+ / Hits) |
| TB Hits vs R | Yandy + Aranda O0.5; Caminero if dump isn’t COLD |
| TB Hits vs L | **Caminero + Mesa** (Trop G3–G4) |
| MIL Hits vs TB R | **Bauers** then Mitchell/Chourio; fade Frelick |
| Series shape | MIL rest + SPIKE shorts + elite pen · TB length + Trop Peralta + LHP bats in G3–G4 |

*Next: when G1 probables post, refresh with official nines + `zone_overlap.py --images` on both SPs and lock a real card.*
