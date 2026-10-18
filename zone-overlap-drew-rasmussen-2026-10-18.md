# Zone overlap — vs Drew Rasmussen (2026 Statcast)

**Game:** TB@CLE
**Pitcher:** Drew Rasmussen (RHP, id 656876) · n=3065 pitches
**Windows:** season + **last 30d** (pitcher recent n=306)

Catcher’s view. Display-only — does not change Exp K or hits scores. HOT/WARM/COLD use **season** pitcher location × batter damage; **recent** confirms or flags conflict. `LOW_SAMPLE_*` = FYI — size down, don’t veto automatically.

**Mix:** FC 29% / FF 28% / SI 23% / CH 13% / CU 3% / ST 2%
**Velo:** CH ~89.5, CU ~80.1, FC ~89.9, FF ~95.8, SI ~95.2, ST ~84.5

## Where the pitcher throws

### vs LHB — in-zone 50% · heart 9% · mean px=0.102 (neg=3B) pz=2.389

- Top zones: OUT-DN-1B 18%, OUT-UP-3B 13%, OUT-UP-1B 9%, OUT-DN-3B 9%, HEART 9%, MID-AWAY 7%
- **Usage vs this hand:** FF 32%, FC 28%, CH 18%, SI 17%, CU 5%, ST 0%
- **CH lands:** OUT-DN-3B 38%, OUT-DN-1B 16%, OUT-UP-3B 12%
- **CU lands:** OUT-UP-3B 21%, OUT-DN-1B 18%, OUT-DN-3B 15%
- **FC lands:** OUT-DN-1B 38%, LO-AWAY 11%, MID-AWAY 11%
- **FF lands:** OUT-UP-3B 25%, OUT-UP-1B 16%, HI-MID 10%
- **SI lands:** OUT-UP-1B 15%, OUT-DN-1B 14%, HI-AWAY (1B) 10%
- **Zone → pitch mix:** OUT-DN-1B (18% throws → FC 59%+CH 16%); OUT-UP-3B (13% throws → FF 60%+CH 16%); OUT-UP-1B (9% throws → FF 55%+SI 27%); OUT-DN-3B (9% throws → CH 72%+FC 10%)

### vs RHB — in-zone 50% · heart 8% · mean px=0.201 (neg=3B) pz=2.198

- Top zones: OUT-DN-1B 24%, OUT-UP-3B 9%, OUT-UP-1B 9%, OUT-DN-3B 8%, HEART 8%, LO-AWAY 7%
- **Usage vs this hand:** SI 34%, FC 31%, FF 22%, CH 6%, ST 6%, CU 0%
- **CH lands:** OUT-DN-1B 47%, OUT-DN-3B 29%, LO-MID 10%
- **FC lands:** OUT-DN-1B 43%, LO-AWAY 12%, MID-AWAY 8%
- **FF lands:** OUT-UP-1B 27%, OUT-UP-3B 12%, OUT-DN-1B 10%
- **SI lands:** OUT-UP-3B 16%, OUT-DN-3B 15%, HEART 11%
- **ST lands:** OUT-DN-1B 36%, OUT-DN-3B 10%, HEART 8%
- **Zone → pitch mix:** OUT-DN-1B (24% throws → FC 57%+CH 13%); OUT-UP-3B (9% throws → SI 61%+FF 31%); OUT-UP-1B (9% throws → FF 66%+FC 23%); OUT-DN-3B (9% throws → SI 60%+CH 22%)

## Batter heat vs opposing hand → overlap

### Chase DeLauter (stand L, vs RHP, season n=1674, recent n=182)
- Swing 41.9% · whiff/swing 12.0%
- **Top swing (season):** HI-AWAY (1B) 94.7%; HEART 82.5%; MID-AWAY 75.7%; HI-MID 75.4%
- **Top damage season (xwOBA BIP):** HI-AWAY (1B) 0.481 (EV 86.2, brl 7.7%, BIP 13); LO-AWAY 0.457 (EV 96.4, brl 13.3%, BIP 30); MID-AWAY 0.456 (EV 92.7, brl 10.3%, BIP 29); LO-MID 0.442 (EV 97.3, brl 11.5%, BIP 52)
- **Top damage recent (30d):** HEART 0.390 (BIP 6)
- **HOT/WARM overlap:** HOT MID-AWAY (W 7.3%, xwOBA 0.456, recent HOT xwOBA 0.403 BIP 3 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; WARM HI-MID (W 6.3%, xwOBA 0.397, recent WARM xwOBA 0.398 BIP 4 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; WARM OUT-DN-1B (W 17.7%, xwOBA 0.37, recent — xwOBA nan BIP 0 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM OUT-UP-3B (W 13.4%, xwOBA 0.37, recent — xwOBA nan BIP 1 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT LO-AWAY (W 6.2%, xwOBA 0.457, recent — xwOBA nan BIP 1 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-DN-3B (W 9.3%, xwOBA 0.222, recent — · SEASON_ONLY); OUT-UP-1B (W 9.4%, xwOBA 0.2, recent — · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** HOT MID-AWAY, WARM HI-MID

### Nathaniel Lowe (stand L, vs RHP, season n=1792, recent n=144)
- Swing 45.5% · whiff/swing 19.1%
- **Top swing (season):** HI-MID 77.5%; HEART 73.9%; HI-AWAY (1B) 72.5%; MID-AWAY 63.9%
- **Top damage season (xwOBA BIP):** HEART 0.596 (EV 96.7, brl 19.5%, BIP 41); HI-IN (3B) 0.507 (EV 96.1, brl 11.8%, BIP 17); MID-IN 0.502 (EV 95.4, brl 13.6%, BIP 22); LO-AWAY 0.470 (EV 95.1, brl 13.6%, BIP 22)
- **Top damage recent (30d):** MID-AWAY 0.348 (BIP 6)
- **HOT/WARM overlap:** HOT HEART (W 8.6%, xwOBA 0.596, recent — xwOBA 0.29 BIP 3 · SEASON_ONLY); WARM OUT-DN-3B (W 9.3%, xwOBA 0.373 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT MID-AWAY (W 7.3%, xwOBA 0.448, recent — xwOBA 0.348 BIP 6 · SEASON_ONLY); HOT LO-AWAY (W 6.2%, xwOBA 0.47, recent — xwOBA 0.476 BIP 4 · SEASON_ONLY); WARM HI-IN (3B) (W 5.1%, xwOBA 0.507, recent — xwOBA nan BIP 1 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-UP-3B (W 13.4%, xwOBA 0.135, recent — · SEASON_ONLY); OUT-UP-1B (W 9.4%, xwOBA 0.164, recent — · SEASON_ONLY)

### Travis Bazzana (stand L, vs RHP, season n=1532, recent n=142)
- Swing 45.6% · whiff/swing 21.5%
- **Top swing (season):** MID-AWAY 85.7%; HEART 82.9%; LO-AWAY 79.7%; HI-AWAY (1B) 78.1%
- **Top damage season (xwOBA BIP):** MID-AWAY 0.497 (EV 94.1, brl 15.8%, BIP 19); HEART 0.429 (EV 96.2, brl 12.0%, BIP 50); MID-IN 0.348 (EV 86.9, brl 6.9%, BIP 29); HI-MID 0.324 (EV 91.9, brl 13.0%, BIP 23)
- **Top damage recent (30d):** LO-IN 0.341 (BIP 6); HEART 0.290 (BIP 8)
- **HOT/WARM overlap:** HOT HEART (W 8.6%, xwOBA 0.429, recent — xwOBA 0.29 BIP 8 · SEASON_ONLY); HOT MID-AWAY (W 7.3%, xwOBA 0.497 · SEASON_ONLY); WARM HI-IN (3B) (W 5.1%, xwOBA 0.43, recent — xwOBA nan BIP 2 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT OUT-UP-1B (W 9.4%, xwOBA 0.53, recent — xwOBA nan BIP 0 · SEASON_ONLY) [LOW_SAMPLE_ZONE]
- **COLD vs his tunnel:** OUT-DN-3B (W 9.3%, xwOBA 0.247, recent — · SEASON_ONLY); OUT-UP-3B (W 13.4%, xwOBA 0.192, recent — · SEASON_ONLY)

### Jo Adell (stand R, vs RHP, season n=2085, recent n=184)
- Swing 52.9% · whiff/swing 25.6%
- **Top swing (season):** HEART 83.0%; LO-MID 75.2%; MID-AWAY 74.8%; MID-IN 73.6%
- **Top damage season (xwOBA BIP):** HI-AWAY (1B) 0.470 (EV 99.3, brl 0.0%, BIP 15); LO-MID 0.462 (EV 97.8, brl 11.8%, BIP 34); OUT-DN-3B 0.445 (EV 88.2, brl 15.4%, BIP 13); MID-AWAY 0.434 (EV 95.0, brl 13.2%, BIP 38)
- **Top damage recent (30d):** HEART 0.189 (BIP 9)
- **HOT/WARM overlap:** HOT LO-AWAY (W 7.4%, xwOBA 0.403, recent HOT xwOBA 0.494 BIP 3 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; HOT MID-AWAY (W 6.2%, xwOBA 0.434, recent HOT xwOBA 0.656 BIP 3 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; HOT OUT-DN-3B (W 8.5%, xwOBA 0.445 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT LO-MID (W 6.5%, xwOBA 0.462, recent — xwOBA nan BIP 1 · SEASON_ONLY); WARM HI-MID (W 5.0%, xwOBA 0.43, recent — xwOBA nan BIP 2 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-UP-3B (W 9.1%, xwOBA 0.2, recent COLD · CONFIRM)
- **Season ∩ recent CONFIRM:** HOT LO-AWAY, HOT MID-AWAY, COLD OUT-UP-3B

### Steven Kwan (stand L, vs RHP, season n=2069, recent n=212)
- Swing 36.0% · whiff/swing 5.2%
- **Top swing (season):** HEART 62.2%; LO-IN 58.7%; MID-IN 55.5%; HI-MID 55.3%
- **Top damage season (xwOBA BIP):** LO-AWAY 0.439 (EV 87.5, brl 0.0%, BIP 16); HI-MID 0.350 (EV 82.9, brl 0.0%, BIP 36); LO-MID 0.348 (EV 89.4, brl 0.0%, BIP 46); LO-IN 0.345 (EV 85.1, brl 0.0%, BIP 32)
- **Top damage recent (30d):** HEART 0.494 (BIP 7); MID-IN 0.266 (BIP 5)
- **HOT/WARM overlap:** WARM HI-MID (W 6.3%, xwOBA 0.35, recent HOT xwOBA 0.46 BIP 4 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; HOT LO-AWAY (W 6.2%, xwOBA 0.439, recent — xwOBA 0.38 BIP 3 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-UP-3B (W 13.4%, xwOBA 0.242, recent COLD · CONFIRM); OUT-DN-3B (W 9.3%, xwOBA 0.275, recent COLD · CONFIRM); OUT-DN-1B (W 17.7%, xwOBA 0.208, recent — · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** COLD OUT-UP-3B, COLD OUT-DN-3B, WARM HI-MID

### Brayan Rocchio (stand L, vs RHP, season n=1758, recent n=141)
- Swing 47.5% · whiff/swing 19.5%
- **Top swing (season):** HI-AWAY (1B) 76.0%; HEART 73.6%; HI-MID 72.9%; LO-MID 71.3%
- **Top damage season (xwOBA BIP):** HI-IN (3B) 0.410 (EV 90.0, brl 5.0%, BIP 20); LO-MID 0.330 (EV 95.1, brl 4.8%, BIP 42); LO-AWAY 0.330 (EV 89.5, brl 9.1%, BIP 11); OUT-UP-1B 0.316 (EV 71.0, brl 0.0%, BIP 9)
- **Top damage recent (30d):** MID-IN 0.099 (BIP 5)
- **HOT/WARM overlap:** WARM HI-IN (3B) (W 5.1%, xwOBA 0.41, recent — xwOBA nan BIP 2 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-DN-1B (W 17.7%, xwOBA 0.28, recent — · SEASON_ONLY); OUT-UP-3B (W 13.4%, xwOBA 0.231, recent — · SEASON_ONLY)

### Patrick Bailey (stand L, vs RHP, season n=1275, recent n=140)
- Swing 51.2% · whiff/swing 23.7%
- **Top swing (season):** HI-MID 84.7%; MID-IN 73.8%; HEART 72.2%; HI-AWAY (1B) 71.9%
- **Top damage season (xwOBA BIP):** HI-MID 0.645 (EV 93.7, brl 21.7%, BIP 23); HEART 0.526 (EV 94.8, brl 19.4%, BIP 36); HI-IN (3B) 0.498 (EV 95.6, brl 0.0%, BIP 11); MID-AWAY 0.442 (EV 91.4, brl 6.2%, BIP 16)
- **Top damage recent (30d):** HI-MID 0.743 (BIP 5); OUT-DN-3B 0.507 (BIP 5)
- **HOT/WARM overlap:** HOT HI-MID (W 6.3%, xwOBA 0.645, recent HOT xwOBA 0.743 BIP 5 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; WARM OUT-UP-3B (W 13.4%, xwOBA 0.373, recent — xwOBA nan BIP 0 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT HEART (W 8.6%, xwOBA 0.526, recent — xwOBA nan BIP 1 · SEASON_ONLY); HOT MID-AWAY (W 7.3%, xwOBA 0.442 · SEASON_ONLY); WARM HI-IN (3B) (W 5.1%, xwOBA 0.498 · SEASON_ONLY) [LOW_SAMPLE_ZONE]
- **COLD vs his tunnel:** OUT-UP-1B (W 9.4%, xwOBA 0.203 · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** HOT HI-MID

### Petey Halpin (stand L, vs RHP, season n=660, recent n=97)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- Swing 58.0% · whiff/swing 21.7%
- **Top swing (season):** HI-MID 90.3%; MID-IN 86.8%; HEART 85.2%; LO-AWAY 81.6%
- **Top damage season (xwOBA BIP):** OUT-DN-3B 0.525 (EV 84.5, brl 6.7%, BIP 15); MID-AWAY 0.497 (EV 85.9, brl 7.7%, BIP 13); MID-IN 0.470 (EV 90.5, brl 22.2%, BIP 9); LO-IN 0.404 (EV 87.7, brl 7.1%, BIP 14)
- **HOT/WARM overlap:** HOT OUT-UP-3B (W 13.4%, xwOBA 0.533, recent — xwOBA None BIP 1 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT OUT-DN-3B (W 9.3%, xwOBA 0.525, recent — xwOBA None BIP 1 · SEASON_ONLY); HOT MID-AWAY (W 7.3%, xwOBA 0.497 · SEASON_ONLY) [LOW_SAMPLE_ZONE]
- **COLD vs his tunnel:** OUT-DN-1B (W 17.7%, xwOBA 0.211 · SEASON_ONLY)

### José Ramírez (stand L, vs RHP, season n=1852, recent n=190)
- Swing 44.8% · whiff/swing 14.8%
- **Top swing (season):** HEART 73.6%; HI-MID 72.5%; LO-MID 67.2%; LO-IN 65.9%
- **Top damage season (xwOBA BIP):** OUT-UP-3B 0.484 (EV 91.8, brl 16.7%, BIP 18); LO-AWAY 0.400 (EV 83.6, brl 7.7%, BIP 13); MID-IN 0.388 (EV 94.5, brl 2.6%, BIP 38); OUT-DN-1B 0.352 (EV 80.4, brl 0.0%, BIP 13)
- **Top damage recent (30d):** LO-MID 0.592 (BIP 5); HEART 0.309 (BIP 5); MID-IN 0.220 (BIP 6); LO-IN 0.126 (BIP 7)
- **HOT/WARM overlap:** HOT OUT-UP-3B (W 13.4%, xwOBA 0.484, recent — xwOBA nan BIP 1 · SEASON_ONLY); WARM OUT-DN-1B (W 17.7%, xwOBA 0.352, recent — xwOBA nan BIP 2 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT LO-AWAY (W 6.2%, xwOBA 0.4, recent — xwOBA nan BIP 1 · SEASON_ONLY) [LOW_SAMPLE_ZONE]
- **COLD vs his tunnel:** OUT-UP-1B (W 9.4%, xwOBA 0.25, recent COLD · CONFIRM); OUT-DN-3B (W 9.3%, xwOBA 0.232, recent COLD · CONFIRM); MID-AWAY (W 7.3%, xwOBA 0.23, recent — · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** COLD OUT-UP-1B, COLD OUT-DN-3B

## Hits / H+R+RBI board (same slate)

| Slot | Batter | Hits | HR/RBI | AVG vs hand | Barrel | HH | Zone note |
|------|--------|------|--------|-------------|--------|----|-----------|
| 3 | Chase DeLauter | 54.5 | 54.2 | 0.269 | 6.3% | 46.3% | CONFIRM HOT MID-AWAY/WARM HI-MID; COLD OUT-DN-3B |
| 5 | Nathaniel Lowe | 54.1 | 53.3 | 0.271 | 8.3% | 41.4% | HOT HEART/MID-AWAY; COLD OUT-UP-3B |
| 6 | Travis Bazzana | 49.3 | 46.6 | 0.274 | 5.2% | 36.2% | HOT HEART/MID-AWAY; COLD OUT-DN-3B |
| 4 | Jo Adell | 48.3 | 50.7 | 0.209 | 8.9% | 44.9% | CONFIRM HOT LO-AWAY/HOT MID-AWAY; COLD OUT-UP-3B |
| 1 | Steven Kwan | 47.7 | 42.3 | 0.306 | 0.4% | 10.5% | CONFIRM COLD OUT-UP-3B/COLD OUT-DN-3B; COLD OUT-UP-3B |
| 9 | Brayan Rocchio | 47.1 | 44.0 | 0.272 | 2.8% | 30.0% | WARM HI-IN (3B); COLD OUT-DN-1B |
| 7 | Patrick Bailey | 47.1 | 48.0 | 0.221 | 7.6% | 42.4% | CONFIRM HOT HI-MID; COLD OUT-UP-1B |
| 8 | Petey Halpin | 46.4 | 44.1 | 0.259 | 5.4% | 25.5% | HOT OUT-UP-3B/OUT-DN-3B; COLD OUT-DN-1B; LOW_SAMPLE_RECENT |
| 2 | José Ramírez | 45.2 | 46.5 | 0.212 | 4.1% | 38.8% | CONFIRM COLD OUT-UP-1B/COLD OUT-DN-3B; COLD OUT-UP-1B |

*Generated by `mlb-k-matchups/zone_overlap.py` — re-run on future slates with `--hits` + `--pitcher`. Prefer CONFIRM HOTs; treat `LOW_SAMPLE_*` as sizing FYI.*
