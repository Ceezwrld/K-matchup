# Zone overlap — vs Logan Henderson (2026 Statcast)

**Game:** TB@MIL
**Pitcher:** Logan Henderson (RHP, id 701656) · n=1720 pitches
**Windows:** season + **last 30d** (pitcher recent n=136)

Catcher’s view. Display-only — does not change Exp K or hits scores. HOT/WARM/COLD use **season** pitcher location × batter **damage**; **dump fit** adds where they **swing** on his LHB/RHB tunnel. **recent** confirms or flags conflict. `LOW_SAMPLE_*` = FYI — size down, don’t veto automatically.

**Mix:** FF 47% / CH 35% / FC 15% / ST 3% / SL 0% / CU 0%
**Velo:** CH ~83.1, CU ~77.4, FC ~87.9, FF ~93.2, SL ~79.9, ST ~81.1

## Where the pitcher throws

### vs LHB — in-zone 52% · heart 9% · mean px=-0.255 (neg=3B) pz=2.352

- Top zones: OUT-DN-3B 18%, OUT-UP-3B 16%, HEART 9%, OUT-DN-1B 8%, MID-IN 7%, HI-MID 6%
- **Usage vs this hand:** FF 48%, CH 40%, FC 11%, ST 1%, SL 0%, CU 0%
- **CH lands:** OUT-DN-3B 37%, OUT-DN-1B 11%, MID-IN 8%
- **FC lands:** HEART 16%, OUT-UP-3B 14%, OUT-DN-1B 11%
- **FF lands:** OUT-UP-3B 23%, HEART 10%, HI-MID 10%
- **Zone → pitch mix:** OUT-DN-3B (18% throws → CH 82%+FF 14%); OUT-UP-3B (16% throws → FF 68%+CH 19%); HEART (9% throws → FF 54%+CH 23%); OUT-DN-1B (8% throws → CH 53%+FF 27%)
- **Dump (ticket tunnel):** OUT-DN-3B 17.6% CH+FF · chase; OUT-UP-3B 16.3% FF+CH · chase

### vs RHB — in-zone 56% · heart 10% · mean px=0.159 (neg=3B) pz=2.316

- Top zones: OUT-DN-1B 18%, HEART 10%, OUT-UP-3B 10%, OUT-UP-1B 10%, MID-AWAY 8%, OUT-DN-3B 7%
- **Usage vs this hand:** FF 46%, CH 27%, FC 21%, ST 6%, SL 0%
- **CH lands:** OUT-DN-1B 25%, OUT-DN-3B 17%, LO-MID 11%
- **FC lands:** OUT-DN-1B 23%, OUT-UP-1B 15%, MID-AWAY 12%
- **FF lands:** OUT-UP-3B 14%, OUT-UP-1B 14%, HEART 12%
- **ST lands:** OUT-DN-1B 45%, LO-MID 15%, HI-MID 10%
- **Zone → pitch mix:** OUT-DN-1B (18% throws → CH 37%+FC 26%); HEART (10% throws → FF 57%+CH 23%); OUT-UP-3B (10% throws → FF 68%+CH 19%); OUT-UP-1B (9% throws → FF 67%+FC 33%)
- **Dump (ticket tunnel):** OUT-DN-1B 18.3% CH+FC · chase

## Dump × swing (vs LHB / RHB)

Pitcher’s #1 throw pocket vs that batter’s hand, crossed with whether they **swing** there. TUNNEL = Hits location. MISTAKE = hunt middle, not the dump. CHASE/TAKE = not a Hits lean on the tunnel (K / take).

| Batter | Stand | Dump | Throw | Swing | Whiff | xwOBA | Fit |
|--------|-------|------|-------|-------|-------|-------|-----|
| Junior Caminero | R | OUT-DN-1B | 18.3% CH+FC | 26.8 | 51.4 | 0.197 | **MISTAKE** |
| Yandy Díaz | R | OUT-DN-1B | 18.3% CH+FC | 26.5 | 21.3 | 0.269 | **MISTAKE** |
| Jonathan Aranda | L | OUT-DN-3B | 17.6% CH+FF | 45.3 | 17.1 | 0.324 | **MISTAKE** |
| Liam Hicks | L | OUT-DN-3B | 17.6% CH+FF | 31.0 | 26.4 | 0.283 | **MISTAKE** |
| Victor Mesa Jr. | L | OUT-DN-3B | 17.6% CH+FF | 43.2 | 22.0 | 0.429 | **TUNNEL** |
| Chandler Simpson | L | OUT-DN-3B | 17.6% CH+FF | 30.6 | 34.1 | 0.16 | **COLD** |
| Richie Palacios | L | OUT-DN-3B | 17.6% CH+FF | 36.2 | 35.2 | 0.308 | **MISTAKE** |
| Jonny DeLuca | R | OUT-DN-1B | 18.3% CH+FC | 34.3 | 49.4 | 0.221 | **MISTAKE** |
| Taylor Walls | L | OUT-DN-3B | 17.6% CH+FF | 28.3 | 41.7 | nan | **MISTAKE** |

## Batter heat vs opposing hand → overlap

### Junior Caminero (stand R, vs RHP, season n=2127, recent n=157)
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-DN-1B; HOT in-zone MID-AWAY/HEART (swing 26.8% · whiff 51.4% · xwOBA 0.197)
- Swing 46.2% · whiff/swing 23.6%
- **Top swing (season):** MID-IN 75.9%; HEART 74.8%; HI-IN (3B) 71.2%; LO-IN 64.5%
- **Top damage season (xwOBA BIP):** HI-MID 0.535 (EV 100.0, brl 26.1%, BIP 23); HI-AWAY (1B) 0.532 (EV 102.9, brl 30.0%, BIP 10); OUT-UP-1B 0.502 (EV 90.5, brl 20.0%, BIP 25); HEART 0.470 (EV 98.1, brl 22.4%, BIP 58)
- **Top damage recent (30d):** OUT-DN-1B 0.081 (BIP 6)
- **HOT/WARM overlap:** WARM MID-AWAY (W 8.0%, xwOBA 0.36, recent HOT xwOBA 0.468 BIP 4 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; HOT OUT-UP-1B (W 9.5%, xwOBA 0.502, recent — xwOBA nan BIP 2 · SEASON_ONLY); HOT HEART (W 10.0%, xwOBA 0.47, recent — xwOBA nan BIP 2 · SEASON_ONLY); HOT HI-MID (W 6.2%, xwOBA 0.535, recent — xwOBA nan BIP 2 · SEASON_ONLY); HOT LO-MID (W 6.5%, xwOBA 0.469 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-DN-1B (W 18.3%, xwOBA 0.197, recent COLD · CONFIRM)
- **Season ∩ recent CONFIRM:** COLD OUT-DN-1B, WARM MID-AWAY

### Yandy Díaz (stand R, vs RHP, season n=2041, recent n=159)
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-DN-1B; HOT in-zone LO-MID/MID-IN (swing 26.5% · whiff 21.3% · xwOBA 0.269)
- Swing 47.7% · whiff/swing 13.2%
- **Top swing (season):** HI-MID 76.9%; MID-IN 76.9%; HI-IN (3B) 67.0%; HEART 66.2%
- **Top damage season (xwOBA BIP):** HEART 0.658 (EV 101.0, brl 27.0%, BIP 37); HI-AWAY (1B) 0.496 (EV 98.4, brl 21.4%, BIP 14); HI-MID 0.472 (EV 96.6, brl 25.0%, BIP 20); LO-IN 0.426 (EV 93.8, brl 9.5%, BIP 42)
- **HOT/WARM overlap:** HOT LO-MID (W 6.5%, xwOBA 0.408, recent HOT xwOBA 0.552 BIP 4 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; WARM MID-IN (W 6.0%, xwOBA 0.376, recent WARM xwOBA 0.397 BIP 4 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; HOT HEART (W 10.0%, xwOBA 0.658, recent — xwOBA nan BIP 2 · SEASON_ONLY); HOT HI-MID (W 6.2%, xwOBA 0.472 · SEASON_ONLY); WARM HI-IN (3B) (W 5.4%, xwOBA 0.403, recent — xwOBA nan BIP 1 · SEASON_ONLY) [LOW_SAMPLE_ZONE]
- **COLD vs his tunnel:** OUT-DN-1B (W 18.3%, xwOBA 0.269, recent COLD · CONFIRM); OUT-UP-3B (W 9.6%, xwOBA 0.161, recent — · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** COLD OUT-DN-1B, HOT LO-MID, WARM MID-IN

### Jonathan Aranda (stand L, vs RHP, season n=2091, recent n=130)
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-DN-3B; HOT in-zone LO-MID/HEART (swing 45.3% · whiff 17.1% · xwOBA 0.324)
- Swing 48.2% · whiff/swing 19.3%
- **Top swing (season):** LO-MID 79.1%; HI-MID 75.0%; HEART 72.3%; MID-AWAY 71.6%
- **Top damage season (xwOBA BIP):** LO-AWAY 0.565 (EV 95.2, brl 14.3%, BIP 21); OUT-DN-1B 0.547 (EV 92.5, brl 16.7%, BIP 30); LO-MID 0.531 (EV 95.9, brl 17.0%, BIP 53); HI-MID 0.520 (EV 95.5, brl 13.0%, BIP 23)
- **Top damage recent (30d):** HI-MID 0.299 (BIP 5)
- **HOT/WARM overlap:** HOT LO-MID (W 6.4%, xwOBA 0.531, recent HOT xwOBA 0.597 BIP 3 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; HOT HEART (W 9.0%, xwOBA 0.495, recent — xwOBA 0.293 BIP 3 · SEASON_ONLY); HOT OUT-DN-1B (W 8.0%, xwOBA 0.547, recent — xwOBA nan BIP 1 · SEASON_ONLY); HOT HI-MID (W 6.5%, xwOBA 0.52, recent — xwOBA 0.299 BIP 5 · SEASON_ONLY); HOT MID-IN (W 7.0%, xwOBA 0.452, recent — xwOBA nan BIP 2 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-UP-3B (W 16.3%, xwOBA 0.13, recent — · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** HOT LO-MID

### Liam Hicks (stand L, vs RHP, season n=1730, recent n=101)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-DN-3B; HOT in-zone HEART/LO-MID (swing 31.0% · whiff 26.4% · xwOBA 0.283)
- Swing 42.0% · whiff/swing 10.3%
- **Top swing (season):** HI-MID 73.6%; HEART 68.6%; LO-AWAY 64.1%; HI-AWAY (1B) 62.5%
- **Top damage season (xwOBA BIP):** OUT-DN-1B 0.535 (EV 86.7, brl 11.1%, BIP 9); LO-MID 0.434 (EV 91.7, brl 11.1%, BIP 36); HEART 0.358 (EV 90.0, brl 9.4%, BIP 64); MID-IN 0.353 (EV 92.2, brl 0.0%, BIP 40)
- **Top damage recent (30d):** HI-MID 0.200 (BIP 7)
- **HOT/WARM overlap:** HOT OUT-DN-1B (W 8.0%, xwOBA 0.535, recent — xwOBA nan BIP 0 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM HEART (W 9.0%, xwOBA 0.358, recent COLD xwOBA 0.257 BIP 4 · CONFLICT) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; HOT LO-MID (W 6.4%, xwOBA 0.434, recent — xwOBA 0.349 BIP 3 · SEASON_ONLY); WARM MID-IN (W 7.0%, xwOBA 0.353, recent — xwOBA nan BIP 1 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-UP-3B (W 16.3%, xwOBA 0.206, recent — · SEASON_ONLY)
- **Season vs recent CONFLICT:** HEART (WARM→COLD)

### Victor Mesa Jr. (stand L, vs RHP, season n=805, recent n=112)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `TUNNEL`** — damages his dump OUT-DN-3B (W 17.6% CH+FF) (swing 43.2% · whiff 22.0% · xwOBA 0.429)
- Swing 56.1% · whiff/swing 24.6%
- **Top swing (season):** HEART 89.8%; MID-AWAY 88.9%; HI-MID 87.0%; MID-IN 80.5%
- **Top damage season (xwOBA BIP):** OUT-DN-1B 0.637 (EV 95.5, brl 25.0%, BIP 12); HEART 0.567 (EV 94.8, brl 25.0%, BIP 20); OUT-DN-3B 0.429 (EV 86.4, brl 5.0%, BIP 20); LO-AWAY 0.425 (EV 85.3, brl 15.4%, BIP 13)
- **Top damage recent (30d):** HEART 0.492 (BIP 5)
- **HOT/WARM overlap:** HOT HEART (W 9.0%, xwOBA 0.567, recent HOT xwOBA 0.492 BIP 5 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; HOT OUT-DN-3B (W 17.6%, xwOBA 0.429, recent COLD xwOBA 0.274 BIP 3 · CONFLICT) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; HOT OUT-DN-1B (W 8.0%, xwOBA 0.637, recent — xwOBA nan BIP 0 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT HI-MID (W 6.5%, xwOBA 0.418, recent — xwOBA nan BIP 1 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT LO-MID (W 6.4%, xwOBA 0.402 · SEASON_ONLY)
- **COLD vs his tunnel:** MID-IN (W 7.0%, xwOBA 0.138 · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** HOT HEART
- **Season vs recent CONFLICT:** OUT-DN-3B (HOT→COLD)

### Chandler Simpson (stand L, vs RHP, season n=1456, recent n=84)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `COLD`** — COLD on dump OUT-DN-3B — pass Hits vs this tunnel (swing 30.6% · whiff 34.1% · xwOBA 0.16)
- Swing 47.9% · whiff/swing 9.3%
- **Top swing (season):** HI-AWAY (1B) 90.0%; HEART 73.9%; HI-MID 73.2%; MID-AWAY 65.4%
- **Top damage season (xwOBA BIP):** HEART 0.349 (EV 84.4, brl 0.0%, BIP 48); OUT-DN-1B 0.329 (EV 77.2, brl 0.0%, BIP 10); LO-MID 0.324 (EV 80.7, brl 0.0%, BIP 36); MID-IN 0.323 (EV 80.2, brl 0.0%, BIP 38)
- **COLD vs his tunnel:** OUT-UP-3B (W 16.3%, xwOBA 0.21, recent COLD · CONFIRM); OUT-DN-3B (W 17.6%, xwOBA 0.16 · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** COLD OUT-UP-3B

### Richie Palacios (stand L, vs RHP, season n=1427, recent n=72)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-DN-3B; HOT in-zone MID-AWAY/LO-IN (swing 36.2% · whiff 35.2% · xwOBA 0.308)
- Swing 46.0% · whiff/swing 17.8%
- **Top swing (season):** HI-MID 78.2%; HEART 74.4%; MID-AWAY 73.4%; HI-AWAY (1B) 69.7%
- **Top damage season (xwOBA BIP):** LO-IN 0.395 (EV 89.3, brl 0.0%, BIP 17); MID-AWAY 0.382 (EV 83.8, brl 0.0%, BIP 21); LO-MID 0.348 (EV 82.5, brl 5.3%, BIP 19); HI-IN (3B) 0.343 (EV 92.4, brl 0.0%, BIP 19)
- **HOT/WARM overlap:** WARM MID-AWAY (W 5.5%, xwOBA 0.382 · SEASON_ONLY); WARM LO-IN (W 5.1%, xwOBA 0.395 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-DN-1B (W 8.0%, xwOBA 0.263, recent — · SEASON_ONLY)

### Jonny DeLuca (stand R, vs RHP, season n=936, recent n=114)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-DN-1B; HOT in-zone HI-MID/LO-MID (swing 34.3% · whiff 49.4% · xwOBA 0.221)
- Swing 51.8% · whiff/swing 20.6%
- **Top swing (season):** HI-IN (3B) 78.0%; HI-MID 75.8%; MID-AWAY 75.0%; HEART 73.8%
- **Top damage season (xwOBA BIP):** HI-MID 0.473 (EV 94.2, brl 17.6%, BIP 17); LO-MID 0.393 (EV 94.6, brl 4.8%, BIP 21); MID-AWAY 0.329 (EV 91.8, brl 3.7%, BIP 27); MID-IN 0.310 (EV 79.3, brl 5.9%, BIP 17)
- **Top damage recent (30d):** HEART 0.301 (BIP 5); MID-AWAY 0.299 (BIP 6); LO-AWAY 0.237 (BIP 5)
- **HOT/WARM overlap:** HOT HI-MID (W 6.2%, xwOBA 0.473, recent WARM xwOBA 0.389 BIP 3 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; WARM LO-MID (W 6.5%, xwOBA 0.393 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-DN-1B (W 18.3%, xwOBA 0.221, recent — · SEASON_ONLY); OUT-UP-1B (W 9.5%, xwOBA 0.259, recent — · SEASON_ONLY); HEART (W 10.0%, xwOBA 0.226, recent — · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** HOT HI-MID

### Taylor Walls (stand L, vs RHP, season n=1255, recent n=106)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-DN-3B; HOT in-zone MID-IN/HI-IN (3B) (swing 28.3% · whiff 41.7% · xwOBA nan)
- Swing 41.9% · whiff/swing 22.6%
- **Top swing (season):** HEART 73.4%; MID-IN 65.2%; HI-MID 64.6%; HI-IN (3B) 61.5%
- **Top damage season (xwOBA BIP):** MID-IN 0.387 (EV 86.9, brl 16.7%, BIP 24); HI-IN (3B) 0.373 (EV 86.1, brl 5.9%, BIP 17); LO-MID 0.345 (EV 81.0, brl 10.5%, BIP 19); OUT-UP-3B 0.343 (EV 72.3, brl 0.0%, BIP 18)
- **HOT/WARM overlap:** WARM MID-IN (W 7.0%, xwOBA 0.387 · SEASON_ONLY); WARM HI-IN (3B) (W 6.0%, xwOBA 0.373 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-DN-1B (W 8.0%, xwOBA 0.175, recent — · SEASON_ONLY)

## Hits / H+R+RBI board (same slate)

| Slot | Batter | Hits | Exp H | P(1+) | PA | RBI | HR/RBI | Zone note |
|------|--------|------|-------|-------|----|-----|--------|-----------|
| 4 | Junior Caminero | 59.5 | 0.37 | 34% | 2 | good | 60.3 | MISTAKE OUT-DN-1B; CONFIRM COLD OUT-DN-1B/WARM MID-AWAY; COLD OUT-DN-1B |
| 1 | Yandy Díaz | 59.0 | 0.59 | 48% | 3 | thin | 57.1 | MISTAKE OUT-DN-1B; CONFIRM COLD OUT-DN-1B/HOT LO-MID; COLD OUT-DN-1B |
| 2 | Jonathan Aranda | 57.0 | 0.56 | 47% | 3 | good | 56.1 | MISTAKE OUT-DN-3B; CONFIRM HOT LO-MID; COLD OUT-UP-3B |
| 5 | Liam Hicks | 52.1 | 0.44 | 39% | 2 | good | 47.6 | MISTAKE OUT-DN-3B; HOT OUT-DN-1B/LO-MID; COLD OUT-UP-3B; CONFLICT HEART; LOW_SAMPLE_RECENT |
| 8 | Victor Mesa Jr. | 51.0 | 0.32 | 29% | 2 | thin | 52.2 | TUNNEL OUT-DN-3B; CONFIRM HOT HEART; COLD MID-IN; CONFLICT OUT-DN-3B; LOW_SAMPLE_RECENT |
| 3 | Chandler Simpson | 46.2 | 0.71 | 56% | 3 | good | 39.2 | COLD OUT-DN-3B; CONFIRM COLD OUT-UP-3B; COLD OUT-UP-3B; LOW_SAMPLE_RECENT |
| 6 | Richie Palacios | 45.6 | 0.35 | 32% | 2 | thin | 43.8 | MISTAKE OUT-DN-3B; WARM MID-AWAY/LO-IN; COLD OUT-DN-1B; LOW_SAMPLE_RECENT |
| 7 | Jonny DeLuca | 45.3 | 0.38 | 34% | 2 | thin | 41.9 | MISTAKE OUT-DN-1B; CONFIRM HOT HI-MID; COLD OUT-DN-1B; LOW_SAMPLE_RECENT |
| 9 | Taylor Walls | 38.1 | 0.27 | 25% | 2 | thin | 35.1 | MISTAKE OUT-DN-3B; WARM MID-IN/HI-IN (3B); COLD OUT-DN-1B; LOW_SAMPLE_RECENT |

*Generated by `mlb-k-matchups/zone_overlap.py` — re-run on future slates with `--hits` + `--pitcher`. Prefer CONFIRM **TUNNEL** HOTs; MISTAKE = heart/in-zone, not the dump. Treat `LOW_SAMPLE_*` as sizing FYI.*
