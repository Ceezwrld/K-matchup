# Zone overlap — vs Dustin May (2026 Statcast)

**Game:** MIL@TB
**Pitcher:** Dustin May (RHP, id 669160) · n=2705 pitches
**Windows:** season + **last 30d** (pitcher recent n=122)

Catcher’s view. Display-only — does not change Exp K or hits scores. HOT/WARM/COLD use **season** pitcher location × batter **damage**; **dump fit** adds where they **swing** on his LHB/RHB tunnel. **recent** confirms or flags conflict. `LOW_SAMPLE_*` = FYI — size down, don’t veto automatically.

**Mix:** FF 24% / FC 24% / SI 21% / ST 18% / CU 8% / CH 6% / PO 0%
**Velo:** CH ~90.3, CU ~83.7, FC ~93.4, FF ~97.0, PO ~95.7, SI ~96.7, ST ~86.1

## Where the pitcher throws

### vs LHB — in-zone 47% · heart 7% · mean px=0.061 (neg=3B) pz=2.411

- Top zones: OUT-DN-1B 20%, OUT-UP-3B 18%, OUT-UP-1B 8%, HEART 7%, HI-MID 7%, OUT-DN-3B 7%
- **Usage vs this hand:** FC 29%, FF 28%, ST 16%, CU 11%, CH 10%, SI 7%
- **CH lands:** OUT-DN-3B 27%, OUT-UP-3B 19%, OUT-DN-1B 16%
- **CU lands:** OUT-DN-1B 35%, OUT-UP-3B 15%, OUT-DN-3B 12%
- **FC lands:** OUT-DN-1B 23%, OUT-UP-1B 13%, OUT-UP-3B 11%
- **FF lands:** OUT-UP-3B 27%, OUT-UP-1B 13%, HI-MID 11%
- **SI lands:** OUT-UP-3B 18%, OUT-DN-3B 16%, OUT-DN-1B 13%
- **ST lands:** OUT-DN-1B 31%, OUT-UP-3B 17%, LO-MID 9%
- **Zone → pitch mix:** OUT-DN-1B (20% throws → FC 33%+ST 24%); OUT-UP-3B (18% throws → FF 41%+FC 17%); OUT-UP-1B (8% throws → FC 49%+FF 47%); HEART (7% throws → FF 32%+FC 28%)
- **Dump (ticket tunnel):** OUT-DN-1B 20.2% FC+ST · chase; OUT-UP-3B 18.1% FF+FC · chase

### vs RHB — in-zone 51% · heart 8% · mean px=0.201 (neg=3B) pz=2.294

- Top zones: OUT-DN-1B 24%, OUT-UP-3B 12%, LO-MID 8%, OUT-UP-1B 8%, HEART 8%, MID-AWAY 7%
- **Usage vs this hand:** SI 42%, ST 21%, FF 19%, FC 16%, CU 2%, CH 0%, PO 0%
- **FC lands:** OUT-DN-1B 31%, OUT-UP-1B 10%, MID-AWAY 10%
- **FF lands:** OUT-UP-1B 24%, OUT-UP-3B 14%, MID-AWAY 11%
- **SI lands:** OUT-UP-3B 17%, OUT-DN-1B 14%, LO-MID 13%
- **ST lands:** OUT-DN-1B 49%, LO-AWAY 8%, HEART 8%
- **Zone → pitch mix:** OUT-DN-1B (24% throws → ST 42%+SI 25%); OUT-UP-3B (12% throws → SI 57%+FF 21%); LO-MID (8% throws → SI 69%+ST 18%); HEART (8% throws → SI 43%+ST 21%)
- **Dump (ticket tunnel):** OUT-DN-1B 24.2% ST+SI · chase; OUT-UP-3B 12.4% SI+FF · chase

## Dump × swing (vs LHB / RHB)

Pitcher’s #1 throw pocket vs that batter’s hand, crossed with whether they **swing** there. TUNNEL = Hits location. MISTAKE = hunt middle, not the dump. CHASE/TAKE = not a Hits lean on the tunnel (K / take).

| Batter | Stand | Dump | Throw | Swing | Whiff | xwOBA | Fit |
|--------|-------|------|-------|-------|-------|-------|-----|
| Junior Caminero | R | OUT-DN-1B | 24.2% ST+SI | 27.1 | 52.2 | 0.197 | **MISTAKE** |
| Yandy Díaz | R | OUT-DN-1B | 24.2% ST+SI | 26.6 | 21.8 | 0.266 | **MISTAKE** |
| Jonathan Aranda | L | OUT-DN-1B | 20.2% FC+ST | 42.5 | 37.0 | 0.547 | **TUNNEL** |
| Liam Hicks | L | OUT-DN-1B | 20.2% FC+ST | 23.7 | 52.5 | 0.535 | **TUNNEL** |
| Chandler Simpson | L | OUT-DN-1B | 20.2% FC+ST | 16.5 | 28.2 | 0.311 | **TAKE** |
| Ryan Vilade | R | OUT-DN-1B | 24.2% ST+SI | 16.9 | 70.8 | 0.293 | **MISTAKE** |
| Richie Palacios | L | OUT-DN-1B | 20.2% FC+ST | 35.7 | 42.0 | 0.263 | **MISTAKE** |
| Jonny DeLuca | R | OUT-DN-1B | 24.2% ST+SI | 34.1 | 49.4 | 0.221 | **MISTAKE** |
| Taylor Walls | L | OUT-DN-1B | 20.2% FC+ST | 22.7 | 48.9 | 0.175 | **TAKE** |

## Batter heat vs opposing hand → overlap

### Junior Caminero (stand R, vs RHP, season n=2151, recent n=146)
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-DN-1B; HOT in-zone LO-MID/HEART (swing 27.1% · whiff 52.2% · xwOBA 0.197)
- Swing 46.4% · whiff/swing 23.6%
- **Top swing (season):** MID-IN 76.4%; HEART 74.2%; HI-IN (3B) 71.6%; MID-AWAY 63.8%
- **Top damage season (xwOBA BIP):** HI-MID 0.535 (EV 100.0, brl 26.1%, BIP 23); HI-AWAY (1B) 0.532 (EV 102.9, brl 30.0%, BIP 10); OUT-UP-1B 0.502 (EV 90.5, brl 20.0%, BIP 25); HEART 0.470 (EV 98.1, brl 22.4%, BIP 58)
- **HOT/WARM overlap:** HOT OUT-UP-1B (W 7.5%, xwOBA 0.502, recent — xwOBA nan BIP 2 · SEASON_ONLY); HOT LO-MID (W 7.8%, xwOBA 0.458 · SEASON_ONLY); HOT HEART (W 7.5%, xwOBA 0.47, recent — xwOBA nan BIP 2 · SEASON_ONLY); WARM HI-MID (W 5.1%, xwOBA 0.535 · SEASON_ONLY); WARM MID-AWAY (W 6.8%, xwOBA 0.36, recent — xwOBA nan BIP 2 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-DN-1B (W 24.2%, xwOBA 0.197, recent COLD · CONFIRM)
- **Season ∩ recent CONFIRM:** COLD OUT-DN-1B

### Yandy Díaz (stand R, vs RHP, season n=2073, recent n=154)
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-DN-1B; HOT in-zone HEART/LO-MID (swing 26.6% · whiff 21.8% · xwOBA 0.266)
- Swing 47.9% · whiff/swing 13.2%
- **Top swing (season):** HI-MID 77.3%; MID-IN 77.1%; HI-IN (3B) 67.8%; HEART 66.5%
- **Top damage season (xwOBA BIP):** HEART 0.640 (EV 100.5, brl 26.3%, BIP 38); HI-AWAY (1B) 0.496 (EV 98.4, brl 21.4%, BIP 14); HI-MID 0.472 (EV 96.6, brl 25.0%, BIP 20); LO-IN 0.426 (EV 93.8, brl 9.5%, BIP 42)
- **Top damage recent (30d):** OUT-DN-1B 0.219 (BIP 5)
- **HOT/WARM overlap:** HOT HEART (W 7.5%, xwOBA 0.64, recent — xwOBA nan BIP 2 · SEASON_ONLY); HOT LO-MID (W 7.8%, xwOBA 0.408 · SEASON_ONLY); WARM HI-MID (W 5.1%, xwOBA 0.472 · SEASON_ONLY); WARM HI-IN (3B) (W 5.3%, xwOBA 0.403 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM MID-IN (W 5.0%, xwOBA 0.376, recent — xwOBA nan BIP 2 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-DN-1B (W 24.2%, xwOBA 0.266, recent COLD · CONFIRM); OUT-UP-3B (W 12.4%, xwOBA 0.158, recent — · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** COLD OUT-DN-1B

### Jonathan Aranda (stand L, vs RHP, season n=2118, recent n=135)
- **Dump fit `TUNNEL`** — damages his dump OUT-DN-1B (W 20.2% FC+ST) (swing 42.5% · whiff 37.0% · xwOBA 0.547)
- Swing 48.4% · whiff/swing 19.3%
- **Top swing (season):** LO-MID 79.5%; HI-MID 75.0%; HEART 72.2%; MID-AWAY 72.2%
- **Top damage season (xwOBA BIP):** OUT-DN-1B 0.547 (EV 92.5, brl 16.7%, BIP 30); LO-AWAY 0.540 (EV 94.2, brl 13.6%, BIP 22); LO-MID 0.531 (EV 95.9, brl 17.0%, BIP 53); HI-MID 0.520 (EV 95.5, brl 13.0%, BIP 23)
- **Top damage recent (30d):** HI-MID 0.299 (BIP 5)
- **HOT/WARM overlap:** HOT HEART (W 7.0%, xwOBA 0.499, recent HOT xwOBA 0.517 BIP 3 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; WARM LO-MID (W 5.1%, xwOBA 0.531, recent WARM xwOBA 0.597 BIP 3 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; HOT OUT-DN-1B (W 20.2%, xwOBA 0.547, recent — xwOBA nan BIP 1 · SEASON_ONLY); HOT HI-MID (W 6.9%, xwOBA 0.52, recent — xwOBA 0.299 BIP 5 · SEASON_ONLY); WARM LO-AWAY (W 5.7%, xwOBA 0.54 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-UP-1B (W 7.5%, xwOBA 0.224, recent — · SEASON_ONLY); OUT-UP-3B (W 18.1%, xwOBA 0.13, recent — · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** HOT HEART, WARM LO-MID

### Liam Hicks (stand L, vs RHP, season n=1736, recent n=65)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `TUNNEL`** — damages his dump OUT-DN-1B (W 20.2% FC+ST) (swing 23.7% · whiff 52.5% · xwOBA 0.535)
- Swing 42.1% · whiff/swing 10.4%
- **Top swing (season):** HI-MID 73.6%; HEART 68.8%; LO-AWAY 64.1%; HI-AWAY (1B) 62.5%
- **Top damage season (xwOBA BIP):** OUT-DN-1B 0.535 (EV 86.7, brl 11.1%, BIP 9); LO-MID 0.434 (EV 91.7, brl 11.1%, BIP 36); HEART 0.369 (EV 90.2, brl 10.8%, BIP 65); MID-IN 0.353 (EV 91.8, brl 0.0%, BIP 41)
- **Top damage recent (30d):** HI-MID 0.213 (BIP 6)
- **HOT/WARM overlap:** WARM HEART (W 7.0%, xwOBA 0.369, recent WARM xwOBA 0.363 BIP 4 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; HOT OUT-DN-1B (W 20.2%, xwOBA 0.535, recent — xwOBA nan BIP 0 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM LO-MID (W 5.1%, xwOBA 0.434 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-UP-3B (W 18.1%, xwOBA 0.206, recent — · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** WARM HEART

### Chandler Simpson (stand L, vs RHP, season n=1470, recent n=89)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `TAKE`** — takes dump OUT-DN-1B (swing 16.5%) — not a Hits lean on that pitch (swing 16.5% · whiff 28.2% · xwOBA 0.311)
- Swing 48.0% · whiff/swing 9.4%
- **Top swing (season):** HI-AWAY (1B) 90.0%; HEART 74.2%; HI-MID 73.2%; MID-AWAY 65.4%
- **Top damage season (xwOBA BIP):** HEART 0.347 (EV 84.6, brl 0.0%, BIP 49); LO-MID 0.324 (EV 80.7, brl 0.0%, BIP 36); MID-IN 0.320 (EV 80.3, brl 0.0%, BIP 39); OUT-DN-1B 0.311 (EV 78.7, brl 0.0%, BIP 11)
- **COLD vs his tunnel:** OUT-UP-3B (W 18.1%, xwOBA 0.205, recent — · SEASON_ONLY); OUT-UP-1B (W 7.5%, xwOBA 0.197, recent — · SEASON_ONLY)

### Ryan Vilade (stand R, vs RHP, season n=583, recent n=4)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-DN-1B; HOT in-zone HEART/LO-MID (swing 16.9% · whiff 70.8% · xwOBA 0.293)
- Swing 45.8% · whiff/swing 20.2%
- **Top swing (season):** HEART 82.1%; LO-MID 75.9%; HI-MID 75.8%; MID-IN 74.2%
- **Top damage season (xwOBA BIP):** HEART 0.542 (EV 98.1, brl 11.8%, BIP 17); LO-MID 0.480 (EV 93.2, brl 16.7%, BIP 12); MID-AWAY 0.450 (EV 90.7, brl 12.5%, BIP 8); MID-IN 0.336 (EV 85.2, brl 7.1%, BIP 14)
- **HOT/WARM overlap:** HOT HEART (W 7.5%, xwOBA 0.542 · SEASON_ONLY); HOT LO-MID (W 7.8%, xwOBA 0.48 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT MID-AWAY (W 6.8%, xwOBA 0.45 · SEASON_ONLY) [LOW_SAMPLE_ZONE]
- **COLD vs his tunnel:** OUT-UP-3B (W 12.4%, xwOBA 0.143 · SEASON_ONLY)

### Richie Palacios (stand L, vs RHP, season n=1431, recent n=59)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-DN-1B; HOT in-zone MID-AWAY (swing 35.7% · whiff 42.0% · xwOBA 0.263)
- Swing 46.0% · whiff/swing 18.1%
- **Top swing (season):** HI-MID 78.2%; HEART 74.4%; MID-AWAY 73.4%; HI-AWAY (1B) 67.6%
- **Top damage season (xwOBA BIP):** LO-IN 0.395 (EV 89.3, brl 0.0%, BIP 17); MID-AWAY 0.382 (EV 83.8, brl 0.0%, BIP 21); LO-MID 0.348 (EV 82.5, brl 5.3%, BIP 19); HI-IN (3B) 0.343 (EV 92.4, brl 0.0%, BIP 19)
- **HOT/WARM overlap:** WARM MID-AWAY (W 6.0%, xwOBA 0.382 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-DN-1B (W 20.2%, xwOBA 0.263, recent — · SEASON_ONLY); OUT-UP-1B (W 7.5%, xwOBA 0.244 · SEASON_ONLY)

### Jonny DeLuca (stand R, vs RHP, season n=946, recent n=84)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-DN-1B; HOT in-zone LO-MID/HI-MID (swing 34.1% · whiff 49.4% · xwOBA 0.221)
- Swing 51.8% · whiff/swing 20.6%
- **Top swing (season):** HI-IN (3B) 78.0%; HI-MID 75.8%; HEART 75.0%; MID-AWAY 75.0%
- **Top damage season (xwOBA BIP):** HI-MID 0.473 (EV 94.2, brl 17.6%, BIP 17); LO-MID 0.381 (EV 94.3, brl 4.5%, BIP 22); MID-AWAY 0.329 (EV 91.8, brl 3.7%, BIP 27); MID-IN 0.310 (EV 79.3, brl 5.9%, BIP 17)
- **Top damage recent (30d):** HEART 0.301 (BIP 5)
- **HOT/WARM overlap:** WARM LO-MID (W 7.8%, xwOBA 0.381 · SEASON_ONLY); WARM HI-MID (W 5.1%, xwOBA 0.473 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-DN-1B (W 24.2%, xwOBA 0.221, recent — · SEASON_ONLY); OUT-UP-1B (W 7.5%, xwOBA 0.259, recent — · SEASON_ONLY); HEART (W 7.5%, xwOBA 0.226, recent — · SEASON_ONLY)

### Taylor Walls (stand L, vs RHP, season n=1262, recent n=81)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `TAKE`** — takes dump OUT-DN-1B (swing 22.7%) — not a Hits lean on that pitch (swing 22.7% · whiff 48.9% · xwOBA 0.175)
- Swing 41.8% · whiff/swing 22.5%
- **Top swing (season):** HEART 73.4%; MID-IN 65.2%; HI-MID 64.6%; HI-IN (3B) 60.6%
- **Top damage season (xwOBA BIP):** MID-IN 0.387 (EV 86.9, brl 16.7%, BIP 24); HI-IN (3B) 0.373 (EV 86.1, brl 5.9%, BIP 17); LO-MID 0.345 (EV 78.2, brl 10.0%, BIP 20); OUT-UP-3B 0.343 (EV 72.3, brl 0.0%, BIP 18)
- **COLD vs his tunnel:** OUT-DN-1B (W 20.2%, xwOBA 0.175, recent — · SEASON_ONLY); OUT-UP-1B (W 7.5%, xwOBA 0.193 · SEASON_ONLY)

## Hits / H+R+RBI board (same slate)

| Slot | Batter | Hits | Exp H | P(1+) | PA | RBI | HR/RBI | Zone note |
|------|--------|------|-------|-------|----|-----|--------|-----------|
| 3 | Junior Caminero | 59.5 | 0.40 | 36% | 2 | good | 60.3 | MISTAKE OUT-DN-1B; CONFIRM COLD OUT-DN-1B; COLD OUT-DN-1B |
| 1 | Yandy Díaz | 59.0 | 0.45 | 40% | 2 | thin | 57.1 | MISTAKE OUT-DN-1B; CONFIRM COLD OUT-DN-1B; COLD OUT-DN-1B |
| 2 | Jonathan Aranda | 57.0 | 0.37 | 34% | 2 | good | 56.1 | TUNNEL OUT-DN-1B; CONFIRM HOT HEART/WARM LO-MID; COLD OUT-UP-1B |
| 4 | Liam Hicks | 52.1 | 0.46 | 41% | 2 | good | 47.6 | TUNNEL OUT-DN-1B; CONFIRM WARM HEART; COLD OUT-UP-3B; LOW_SAMPLE_RECENT |
| 6 | Chandler Simpson | 46.2 | 0.49 | 43% | 2 | thin | 39.2 | TAKE OUT-DN-1B; COLD OUT-UP-3B; LOW_SAMPLE_RECENT |
| 7 | Ryan Vilade | 45.6 | 0.29 | 27% | 2 | thin | 47.7 | MISTAKE OUT-DN-1B; HOT HEART/LO-MID; COLD OUT-UP-3B; LOW_SAMPLE_RECENT |
| 8 | Richie Palacios | 45.6 | 0.37 | 34% | 2 | thin | 43.8 | MISTAKE OUT-DN-1B; WARM MID-AWAY; COLD OUT-DN-1B; LOW_SAMPLE_RECENT |
| 5 | Jonny DeLuca | 45.3 | 0.38 | 35% | 2 | good | 41.9 | MISTAKE OUT-DN-1B; WARM LO-MID/HI-MID; COLD OUT-DN-1B; LOW_SAMPLE_RECENT |
| 9 | Taylor Walls | 38.1 | 0.29 | 27% | 2 | thin | 35.1 | TAKE OUT-DN-1B; COLD OUT-DN-1B; LOW_SAMPLE_RECENT |

*Generated by `mlb-k-matchups/zone_overlap.py` — re-run on future slates with `--hits` + `--pitcher`. Prefer CONFIRM **TUNNEL** HOTs; MISTAKE = heart/in-zone, not the dump. Treat `LOW_SAMPLE_*` as sizing FYI.*
