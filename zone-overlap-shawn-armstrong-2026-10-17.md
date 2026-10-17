# Zone overlap — vs Shawn Armstrong (2026 Statcast)

**Game:** TB@CLE
**Pitcher:** Shawn Armstrong (RHP, id 542888) · n=798 pitches
**Windows:** season + **last 30d** (pitcher recent n=91)

Catcher’s view. Display-only — does not change Exp K or hits scores. HOT/WARM/COLD use **season** pitcher location × batter damage; **recent** confirms or flags conflict. `LOW_SAMPLE_*` = FYI — size down, don’t veto automatically.

**Mix:** ST 31% / FF 30% / FC 22% / SI 18%
**Velo:** FC ~89.9, FF ~93.4, SI ~93.6, ST ~84.4

## Where the pitcher throws

### vs LHB — in-zone 56% · heart 7% · mean px=-0.15 (neg=3B) pz=2.64

- Top zones: OUT-UP-3B 23%, OUT-DN-1B 11%, HI-IN (3B) 10%, HI-MID 10%, MID-IN 9%, HEART 7%
- **Usage vs this hand:** FF 38%, FC 29%, ST 25%, SI 8%
- **FC lands:** OUT-DN-1B 21%, HI-MID 11%, OUT-UP-1B 11%
- **FF lands:** OUT-UP-3B 36%, HI-IN (3B) 16%, HI-MID 11%
- **SI lands:** OUT-UP-3B 37%, OUT-DN-3B 13%, LO-IN 10%
- **ST lands:** OUT-DN-1B 16%, MID-IN 15%, OUT-UP-3B 13%
- **Zone → pitch mix:** OUT-UP-3B (23% throws → FF 61%+ST 14%); OUT-DN-1B (11% throws → FC 54%+ST 37%); HI-IN (3B) (10% throws → FF 62%+ST 16%); HI-MID (9% throws → FF 46%+FC 34%)

### vs RHB — in-zone 49% · heart 7% · mean px=0.467 (neg=3B) pz=2.312

- Top zones: OUT-DN-1B 28%, OUT-UP-3B 10%, MID-AWAY 10%, OUT-UP-1B 10%, HEART 7%, LO-AWAY 7%
- **Usage vs this hand:** ST 35%, SI 26%, FF 22%, FC 16%
- **FC lands:** OUT-DN-1B 24%, MID-AWAY 17%, HEART 13%
- **FF lands:** OUT-UP-3B 25%, OUT-UP-1B 14%, OUT-DN-1B 9%
- **SI lands:** OUT-DN-1B 26%, OUT-UP-3B 12%, MID-AWAY 12%
- **ST lands:** OUT-DN-1B 45%, LO-AWAY 9%, OUT-UP-1B 8%
- **Zone → pitch mix:** OUT-DN-1B (28% throws → ST 55%+SI 24%); OUT-UP-3B (10% throws → FF 55%+SI 32%); MID-AWAY (10% throws → SI 30%+ST 28%); OUT-UP-1B (10% throws → FF 31%+ST 29%)

## Batter heat vs opposing hand → overlap

### Junior Caminero (stand R, vs RHP, season n=2092, recent n=174)
- Swing 46.2% · whiff/swing 23.8%
- **Top swing (season):** MID-IN 75.7%; HEART 74.2%; HI-IN (3B) 72.2%; LO-IN 65.3%
- **Top damage season (xwOBA BIP):** HI-MID 0.535 (EV 100.0, brl 26.1%, BIP 23); HI-AWAY (1B) 0.532 (EV 102.9, brl 30.0%, BIP 10); OUT-UP-1B 0.474 (EV 89.8, brl 16.7%, BIP 24); HEART 0.470 (EV 98.3, brl 21.4%, BIP 56)
- **Top damage recent (30d):** OUT-DN-1B 0.048 (BIP 6)
- **HOT/WARM overlap:** HOT OUT-UP-1B (W 9.8%, xwOBA 0.474, recent — xwOBA nan BIP 1 · SEASON_ONLY); WARM MID-AWAY (W 10.1%, xwOBA 0.368 · SEASON_ONLY); HOT HEART (W 7.2%, xwOBA 0.47, recent — xwOBA nan BIP 0 · SEASON_ONLY); HOT HI-AWAY (1B) (W 6.3%, xwOBA 0.532, recent — xwOBA nan BIP 0 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM HI-MID (W 5.4%, xwOBA 0.535, recent — xwOBA 0.144 BIP 3 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-DN-1B (W 28.5%, xwOBA 0.195, recent COLD · CONFIRM)
- **Season ∩ recent CONFIRM:** COLD OUT-DN-1B

### Yandy Díaz (stand R, vs RHP, season n=1991, recent n=144)
- Swing 47.6% · whiff/swing 13.0%
- **Top swing (season):** MID-IN 77.7%; HI-MID 77.1%; HI-IN (3B) 66.3%; HEART 65.8%
- **Top damage season (xwOBA BIP):** HEART 0.658 (EV 101.0, brl 27.0%, BIP 37); HI-AWAY (1B) 0.475 (EV 98.9, brl 23.1%, BIP 13); HI-MID 0.472 (EV 96.6, brl 25.0%, BIP 20); HI-IN (3B) 0.438 (EV 88.6, brl 0.0%, BIP 12)
- **HOT/WARM overlap:** HOT HEART (W 7.2%, xwOBA 0.658, recent HOT xwOBA 0.612 BIP 3 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; HOT HI-AWAY (1B) (W 6.3%, xwOBA 0.475, recent — xwOBA nan BIP 1 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM HI-MID (W 5.4%, xwOBA 0.472 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-DN-1B (W 28.5%, xwOBA 0.278, recent — · SEASON_ONLY); OUT-UP-3B (W 10.3%, xwOBA 0.161, recent — · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** HOT HEART

### Jonathan Aranda (stand L, vs RHP, season n=2050, recent n=146)
- Swing 48.0% · whiff/swing 19.5%
- **Top swing (season):** LO-MID 79.1%; HI-MID 74.1%; HEART 72.9%; MID-AWAY 72.3%
- **Top damage season (xwOBA BIP):** LO-AWAY 0.563 (EV 94.8, brl 15.0%, BIP 20); OUT-DN-1B 0.562 (EV 92.3, brl 17.2%, BIP 29); HI-MID 0.559 (EV 98.2, brl 15.0%, BIP 20); LO-MID 0.534 (EV 96.3, brl 17.6%, BIP 51)
- **HOT/WARM overlap:** HOT MID-IN (W 8.6%, xwOBA 0.452, recent HOT xwOBA 0.895 BIP 3 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; HOT OUT-DN-1B (W 11.1%, xwOBA 0.562, recent — xwOBA nan BIP 0 · SEASON_ONLY); HOT HI-MID (W 9.5%, xwOBA 0.559, recent — xwOBA nan BIP 2 · SEASON_ONLY); WARM HI-IN (3B) (W 10.0%, xwOBA 0.396, recent — xwOBA nan BIP 2 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT LO-AWAY (W 6.8%, xwOBA 0.563 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-UP-3B (W 22.7%, xwOBA 0.13, recent — · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** HOT MID-IN

### Liam Hicks (stand L, vs RHP, season n=1710, recent n=125)
- Swing 42.0% · whiff/swing 10.4%
- **Top swing (season):** HI-MID 73.3%; HEART 68.4%; LO-AWAY 65.1%; HI-AWAY (1B) 61.7%
- **Top damage season (xwOBA BIP):** OUT-DN-1B 0.535 (EV 86.7, brl 11.1%, BIP 9); LO-MID 0.434 (EV 91.7, brl 11.1%, BIP 36); HEART 0.369 (EV 90.1, brl 9.8%, BIP 61); MID-IN 0.353 (EV 92.2, brl 0.0%, BIP 40)
- **Top damage recent (30d):** HI-MID 0.384 (BIP 8)
- **HOT/WARM overlap:** HOT OUT-DN-1B (W 11.1%, xwOBA 0.535, recent — xwOBA nan BIP 0 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM MID-IN (W 8.6%, xwOBA 0.353, recent — xwOBA nan BIP 1 · SEASON_ONLY); WARM HEART (W 7.3%, xwOBA 0.369, recent — xwOBA 0.343 BIP 3 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-UP-3B (W 22.7%, xwOBA 0.206, recent — · SEASON_ONLY); HI-IN (3B) (W 10.0%, xwOBA 0.228 · SEASON_ONLY)

### Victor Mesa Jr. (stand L, vs RHP, season n=775, recent n=114)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- Swing 56.0% · whiff/swing 24.0%
- **Top swing (season):** HEART 90.9%; HI-MID 86.4%; MID-IN 80.0%; HI-AWAY (1B) 78.8%
- **Top damage season (xwOBA BIP):** OUT-DN-1B 0.637 (EV 95.5, brl 25.0%, BIP 12); HEART 0.583 (EV 94.3, brl 29.4%, BIP 17); OUT-DN-3B 0.429 (EV 86.4, brl 5.0%, BIP 20); LO-AWAY 0.425 (EV 85.3, brl 15.4%, BIP 13)
- **HOT/WARM overlap:** HOT OUT-DN-1B (W 11.1%, xwOBA 0.637, recent — xwOBA nan BIP 0 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT HEART (W 7.3%, xwOBA 0.583, recent — xwOBA nan BIP 2 · SEASON_ONLY); HOT HI-MID (W 9.5%, xwOBA 0.418, recent — xwOBA nan BIP 1 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT LO-AWAY (W 6.8%, xwOBA 0.425 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT HI-IN (3B) (W 10.0%, xwOBA 0.416 · SEASON_ONLY) [LOW_SAMPLE_ZONE]
- **COLD vs his tunnel:** MID-IN (W 8.6%, xwOBA 0.133, recent — · SEASON_ONLY)

### Chandler Simpson (stand L, vs RHP, season n=1408, recent n=52)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- Swing 47.9% · whiff/swing 9.1%
- **Top swing (season):** HI-AWAY (1B) 91.4%; HI-MID 72.9%; HEART 72.8%; MID-AWAY 66.7%
- **Top damage season (xwOBA BIP):** HEART 0.355 (EV 86.0, brl 0.0%, BIP 44); LO-MID 0.324 (EV 80.7, brl 0.0%, BIP 36); MID-IN 0.323 (EV 80.2, brl 0.0%, BIP 38); OUT-DN-1B 0.319 (EV 76.7, brl 0.0%, BIP 9)
- **HOT/WARM overlap:** WARM HEART (W 7.3%, xwOBA 0.355 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-UP-3B (W 22.7%, xwOBA 0.211 · SEASON_ONLY); HI-MID (W 9.5%, xwOBA 0.264 · SEASON_ONLY)

### Richie Palacios (stand L, vs RHP, season n=1421, recent n=99)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- Swing 45.9% · whiff/swing 17.9%
- **Top swing (season):** HI-MID 78.2%; HEART 74.4%; MID-AWAY 73.4%; HI-AWAY (1B) 68.8%
- **Top damage season (xwOBA BIP):** LO-IN 0.395 (EV 89.3, brl 0.0%, BIP 17); MID-AWAY 0.382 (EV 83.8, brl 0.0%, BIP 21); HI-IN (3B) 0.343 (EV 92.4, brl 0.0%, BIP 19); OUT-UP-3B 0.343 (EV 88.1, brl 0.0%, BIP 21)
- **COLD vs his tunnel:** OUT-DN-1B (W 11.1%, xwOBA 0.263, recent — · SEASON_ONLY)

### Jonny DeLuca (stand R, vs RHP, season n=919, recent n=122)
- Swing 51.8% · whiff/swing 20.4%
- **Top swing (season):** HI-IN (3B) 78.0%; MID-AWAY 76.1%; HI-MID 75.4%; MID-IN 73.8%
- **Top damage season (xwOBA BIP):** HI-MID 0.497 (EV 93.8, brl 18.8%, BIP 16); LO-MID 0.415 (EV 94.6, brl 5.0%, BIP 20); MID-AWAY 0.329 (EV 91.8, brl 3.7%, BIP 27); MID-IN 0.310 (EV 79.3, brl 5.9%, BIP 17)
- **Top damage recent (30d):** MID-AWAY 0.299 (BIP 6); LO-AWAY 0.271 (BIP 5); HEART 0.229 (BIP 5)
- **HOT/WARM overlap:** WARM HI-MID (W 5.4%, xwOBA 0.497, recent WARM xwOBA 0.35 BIP 3 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]
- **COLD vs his tunnel:** HEART (W 7.2%, xwOBA 0.216, recent COLD · CONFIRM); OUT-DN-1B (W 28.5%, xwOBA 0.224, recent — · SEASON_ONLY); OUT-UP-1B (W 9.8%, xwOBA 0.259, recent — · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** WARM HI-MID, COLD HEART

### Taylor Walls (stand L, vs RHP, season n=1221, recent n=91)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- Swing 42.1% · whiff/swing 22.8%
- **Top swing (season):** HEART 74.0%; HI-MID 67.1%; MID-IN 64.6%; HI-IN (3B) 60.9%
- **Top damage season (xwOBA BIP):** MID-IN 0.387 (EV 86.9, brl 16.7%, BIP 24); HI-IN (3B) 0.373 (EV 86.1, brl 5.9%, BIP 17); MID-AWAY 0.350 (EV 81.2, brl 10.0%, BIP 10); OUT-UP-3B 0.343 (EV 75.1, brl 0.0%, BIP 17)
- **HOT/WARM overlap:** WARM HI-IN (3B) (W 10.0%, xwOBA 0.373 · SEASON_ONLY); WARM MID-IN (W 8.6%, xwOBA 0.387 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-DN-1B (W 11.1%, xwOBA 0.175, recent COLD · CONFIRM)
- **Season ∩ recent CONFIRM:** COLD OUT-DN-1B

## Hits / H+R+RBI board (same slate)

| Slot | Batter | Hits | HR/RBI | AVG vs hand | Barrel | HH | Zone note |
|------|--------|------|--------|-------------|--------|----|-----------|
| 4 | Junior Caminero | 59.5 | 60.3 | 0.272 | 13.1% | 49.7% | CONFIRM COLD OUT-DN-1B; COLD OUT-DN-1B |
| 1 | Yandy Díaz | 59.0 | 57.1 | 0.305 | 7.1% | 48.1% | CONFIRM HOT HEART; COLD OUT-DN-1B |
| 2 | Jonathan Aranda | 57.0 | 56.1 | 0.284 | 9.9% | 46.0% | CONFIRM HOT MID-IN; COLD OUT-UP-3B |
| 5 | Liam Hicks | 52.1 | 47.6 | 0.309 | 3.7% | 27.1% | HOT OUT-DN-1B; COLD OUT-UP-3B |
| 6 | Victor Mesa Jr. | 51.0 | 52.2 | 0.234 | 10.8% | 42.2% | HOT OUT-DN-1B/HEART; COLD MID-IN; LOW_SAMPLE_RECENT |
| 3 | Chandler Simpson | 46.2 | 39.2 | 0.318 | 0.0% | 13.6% | WARM HEART; COLD OUT-UP-3B; LOW_SAMPLE_RECENT |
| 8 | Richie Palacios | 45.6 | 43.8 | 0.250 | 3.9% | 28.8% | COLD OUT-DN-1B; LOW_SAMPLE_RECENT |
| 7 | Jonny DeLuca | 45.3 | 41.9 | 0.267 | 3.6% | 30.2% | CONFIRM WARM HI-MID/COLD HEART; COLD HEART |
| 9 | Taylor Walls | 38.1 | 35.1 | 0.233 | 2.1% | 21.9% | CONFIRM COLD OUT-DN-1B; COLD OUT-DN-1B; LOW_SAMPLE_RECENT |

*Generated by `mlb-k-matchups/zone_overlap.py` — re-run on future slates with `--hits` + `--pitcher`. Prefer CONFIRM HOTs; treat `LOW_SAMPLE_*` as sizing FYI.*
