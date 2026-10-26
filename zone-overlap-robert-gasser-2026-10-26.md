# Zone overlap — vs Robert Gasser (2026 Statcast)

**Game:** MIL@TB
**Pitcher:** Robert Gasser (LHP, id 688107) · n=2150 pitches
**Windows:** season + **last 30d** (pitcher recent n=128)

Catcher’s view. Display-only — does not change Exp K or hits scores. HOT/WARM/COLD use **season** pitcher location × batter **damage**; **dump fit** adds where they **swing** on his LHB/RHB tunnel. **recent** confirms or flags conflict. `LOW_SAMPLE_*` = FYI — size down, don’t veto automatically.

**Mix:** ST 25% / SI 24% / FF 22% / FC 17% / CH 10% / SL 0%
**Velo:** CH ~88.4, FC ~88.6, FF ~93.0, SI ~92.8, SL ~83.9, ST ~80.7

## Where the pitcher throws

### vs LHB — in-zone 52% · heart 9% · mean px=-0.299 (neg=3B) pz=2.27

- Top zones: OUT-DN-3B 26%, LO-IN 10%, HEART 9%, OUT-UP-1B 8%, OUT-UP-3B 8%, MID-IN 7%
- **Usage vs this hand:** SI 32%, ST 29%, FC 19%, FF 17%, CH 1%, SL 1%
- **FC lands:** OUT-DN-3B 35%, LO-IN 9%, HEART 9%
- **FF lands:** OUT-UP-3B 25%, OUT-UP-1B 14%, HI-MID 12%
- **SI lands:** OUT-DN-3B 20%, LO-IN 11%, HEART 11%
- **ST lands:** OUT-DN-3B 37%, LO-IN 13%, OUT-DN-1B 8%
- **Zone → pitch mix:** OUT-DN-3B (26% throws → ST 41%+FC 26%); LO-IN (10% throws → ST 38%+SI 37%); HEART (9% throws → SI 41%+ST 20%); OUT-UP-3B (8% throws → FF 51%+FC 18%)
- **Dump (ticket tunnel):** OUT-DN-3B 26.1% ST+FC · chase

### vs RHB — in-zone 52% · heart 8% · mean px=0.013 (neg=3B) pz=2.258

- Top zones: OUT-DN-3B 17%, OUT-UP-1B 13%, OUT-DN-1B 12%, HEART 8%, LO-MID 7%, LO-IN 7%
- **Usage vs this hand:** FF 24%, ST 23%, SI 21%, FC 16%, CH 15%, SL 0%
- **CH lands:** OUT-DN-1B 31%, OUT-DN-3B 21%, OUT-UP-1B 8%
- **FC lands:** OUT-DN-3B 22%, MID-IN 11%, HEART 11%
- **FF lands:** OUT-UP-1B 24%, OUT-UP-3B 14%, HI-MID 10%
- **SI lands:** OUT-DN-3B 15%, OUT-UP-1B 13%, HEART 10%
- **ST lands:** OUT-DN-3B 23%, OUT-DN-1B 18%, LO-MID 10%
- **Zone → pitch mix:** OUT-DN-3B (17% throws → ST 31%+FC 21%); OUT-UP-1B (13% throws → FF 46%+SI 21%); OUT-DN-1B (12% throws → CH 38%+ST 36%); HEART (8% throws → SI 26%+FF 23%)
- **Dump (ticket tunnel):** OUT-DN-3B 17.2% ST+FC · chase; OUT-UP-1B 13.0% FF+SI · chase

## Dump × swing (vs LHB / RHB)

Pitcher’s #1 throw pocket vs that batter’s hand, crossed with whether they **swing** there. TUNNEL = Hits location. MISTAKE = hunt middle, not the dump. CHASE/TAKE = not a Hits lean on the tunnel (K / take).

| Batter | Stand | Dump | Throw | Swing | Whiff | xwOBA | Fit |
|--------|-------|------|-------|-------|-------|-------|-----|
| Victor Mesa Jr. | L | OUT-DN-3B | 26.1% ST+FC | 34.6 | 46.4 | 0.179 | **MISTAKE** |
| Junior Caminero | R | OUT-DN-3B | 17.2% ST+FC | 22.5 | 29.4 | 0.555 | **TUNNEL** |
| Yandy Díaz | R | OUT-DN-3B | 17.2% ST+FC | 28.6 | 18.2 | 0.541 | **TUNNEL** |
| Ryan Vilade | R | OUT-DN-3B | 17.2% ST+FC | 34.6 | 43.2 | 0.497 | **TUNNEL** |
| Jonny DeLuca | R | OUT-DN-3B | 17.2% ST+FC | 47.8 | 38.6 | 0.334 | **MISTAKE** |
| Nick Fortes | R | OUT-DN-3B | 17.2% ST+FC | 23.8 | 56.0 | nan | **MISTAKE** |
| Chandler Simpson | L | OUT-DN-3B | 26.1% ST+FC | 21.7 | 48.5 | 0.294 | **TAKE** |
| Ben Williamson | R | OUT-DN-3B | 17.2% ST+FC | 26.6 | 48.5 | 0.35 | **TUNNEL** |
| Taylor Walls | R | OUT-DN-3B | 17.2% ST+FC | 15.7 | 38.5 | nan | **TAKE** |

## Batter heat vs opposing hand → overlap

### Victor Mesa Jr. (stand L, vs LHP, season n=319, recent n=96)
- **FYI sample:** LOW_SAMPLE_BATTER, LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-DN-3B; HOT in-zone HEART/HI-MID (swing 34.6% · whiff 46.4% · xwOBA 0.179)
- Swing 54.9% · whiff/swing 20.0%
- **Top swing (season):** HEART 85.2%; MID-IN 66.7%; OUT-DN-3B 34.6%; OUT-UP-1B 33.3%
- **Top damage season (xwOBA BIP):** HEART 0.396 (EV 87.9, brl 8.3%, BIP 12); OUT-DN-3B 0.179 (EV 71.1, brl 0.0%, BIP 8)
- **HOT/WARM overlap:** WARM HEART (W 8.9%, xwOBA 0.396 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM HI-MID (W 5.9%, xwOBA 0.451 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM OUT-UP-1B (W 8.3%, xwOBA 0.364 · SEASON_ONLY) [LOW_SAMPLE_ZONE]
- **COLD vs his tunnel:** OUT-DN-3B (W 26.1%, xwOBA 0.179, recent COLD · CONFIRM)
- **Season ∩ recent CONFIRM:** COLD OUT-DN-3B

### Junior Caminero (stand R, vs LHP, season n=834, recent n=58)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `TUNNEL`** — damages his dump OUT-DN-3B (W 17.2% ST+FC) (swing 22.5% · whiff 29.4% · xwOBA 0.555)
- Swing 41.5% · whiff/swing 19.4%
- **Top swing (season):** HEART 70.0%; MID-AWAY 69.2%; HI-MID 68.9%; LO-MID 65.7%
- **Top damage season (xwOBA BIP):** HI-MID 0.818 (EV 103.0, brl 33.3%, BIP 12); OUT-UP-1B 0.734 (EV 99.8, brl 33.3%, BIP 9); MID-AWAY 0.425 (EV 96.2, brl 21.4%, BIP 14); OUT-UP-3B 0.401 (EV 86.9, brl 12.5%, BIP 8)
- **HOT/WARM overlap:** HOT OUT-UP-1B (W 13.0%, xwOBA 0.734, recent — xwOBA None BIP 2 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT OUT-DN-3B (W 17.2%, xwOBA 0.555 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM HI-MID (W 5.9%, xwOBA 0.818 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM OUT-DN-1B (W 11.8%, xwOBA 0.382, recent — xwOBA None BIP 0 · SEASON_ONLY); WARM HEART (W 8.1%, xwOBA 0.377 · SEASON_ONLY)

### Yandy Díaz (stand R, vs LHP, season n=824, recent n=53)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `TUNNEL`** — damages his dump OUT-DN-3B (W 17.2% ST+FC) (swing 28.6% · whiff 18.2% · xwOBA 0.541)
- Swing 48.2% · whiff/swing 11.6%
- **Top swing (season):** HI-MID 78.0%; MID-AWAY 77.8%; HI-AWAY (1B) 71.8%; MID-IN 69.8%
- **Top damage season (xwOBA BIP):** OUT-DN-3B 0.541 (EV 96.0, brl 14.3%, BIP 14); HEART 0.461 (EV 98.6, brl 16.0%, BIP 25); HI-AWAY (1B) 0.449 (EV 101.3, brl 22.2%, BIP 9); MID-AWAY 0.372 (EV 95.9, brl 0.0%, BIP 14)
- **HOT/WARM overlap:** HOT OUT-DN-3B (W 17.2%, xwOBA 0.541, recent — xwOBA None BIP 1 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT HEART (W 8.1%, xwOBA 0.461 · SEASON_ONLY); WARM MID-IN (W 6.5%, xwOBA 0.36 · SEASON_ONLY); WARM MID-AWAY (W 6.0%, xwOBA 0.372 · SEASON_ONLY) [LOW_SAMPLE_ZONE]

### Ryan Vilade (stand R, vs LHP, season n=768, recent n=43)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `TUNNEL`** — damages his dump OUT-DN-3B (W 17.2% ST+FC) (swing 34.6% · whiff 43.2% · xwOBA 0.497)
- Swing 49.2% · whiff/swing 20.9%
- **Top swing (season):** HI-MID 90.0%; HI-IN (3B) 84.6%; LO-AWAY 84.4%; HEART 80.6%
- **Top damage season (xwOBA BIP):** HI-MID 0.661 (EV 92.1, brl 12.5%, BIP 8); LO-MID 0.615 (EV 94.4, brl 15.4%, BIP 13); MID-IN 0.524 (EV 89.4, brl 10.0%, BIP 20); OUT-DN-3B 0.497 (EV 85.2, brl 11.1%, BIP 9)
- **HOT/WARM overlap:** HOT OUT-DN-3B (W 17.2%, xwOBA 0.497 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT OUT-DN-1B (W 11.8%, xwOBA 0.416 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT LO-MID (W 6.9%, xwOBA 0.615 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM HI-MID (W 5.9%, xwOBA 0.661 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT MID-IN (W 6.5%, xwOBA 0.524 · SEASON_ONLY)

### Jonny DeLuca (stand R, vs LHP, season n=685, recent n=74)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-DN-3B; HOT in-zone LO-MID/HEART (swing 47.8% · whiff 38.6% · xwOBA 0.334)
- Swing 55.0% · whiff/swing 22.0%
- **Top swing (season):** HI-MID 81.0%; LO-AWAY 80.0%; LO-MID 79.5%; HEART 78.3%
- **Top damage season (xwOBA BIP):** LO-MID 0.477 (EV 95.2, brl 7.1%, BIP 14); HI-MID 0.453 (EV 82.3, brl 6.2%, BIP 16); HEART 0.368 (EV 94.8, brl 0.0%, BIP 11); MID-IN 0.347 (EV 75.8, brl 0.0%, BIP 12)
- **HOT/WARM overlap:** HOT LO-MID (W 6.9%, xwOBA 0.477 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM HEART (W 8.1%, xwOBA 0.368 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM HI-MID (W 5.9%, xwOBA 0.453 · SEASON_ONLY); HOT LO-IN (W 6.7%, xwOBA 0.444 · SEASON_ONLY) [LOW_SAMPLE_ZONE]
- **COLD vs his tunnel:** OUT-DN-1B (W 11.8%, xwOBA 0.267, recent WARM · CONFLICT); OUT-UP-1B (W 13.0%, xwOBA 0.125, recent — · SEASON_ONLY)
- **Season vs recent CONFLICT:** OUT-DN-1B (COLD→WARM)

### Nick Fortes (stand R, vs LHP, season n=628, recent n=7)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-DN-3B; HOT in-zone LO-MID (swing 23.8% · whiff 56.0% · xwOBA nan)
- Swing 51.8% · whiff/swing 16.3%
- **Top swing (season):** HI-IN (3B) 80.0%; HI-MID 76.7%; MID-IN 76.7%; MID-AWAY 72.7%
- **Top damage season (xwOBA BIP):** LO-MID 0.420 (EV 100.2, brl 12.5%, BIP 8); OUT-UP-3B 0.413 (EV 67.0, brl 0.0%, BIP 8); HI-AWAY (1B) 0.348 (EV 92.7, brl 0.0%, BIP 9); HI-MID 0.317 (EV 75.4, brl 0.0%, BIP 13)
- **HOT/WARM overlap:** HOT LO-MID (W 6.9%, xwOBA 0.42 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM OUT-UP-3B (W 5.4%, xwOBA 0.413 · SEASON_ONLY) [LOW_SAMPLE_ZONE]
- **COLD vs his tunnel:** HEART (W 8.1%, xwOBA 0.215 · SEASON_ONLY)

### Chandler Simpson (stand L, vs LHP, season n=709, recent n=41)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `TAKE`** — takes dump OUT-DN-3B (swing 21.7%) — not a Hits lean on that pitch (swing 21.7% · whiff 48.5% · xwOBA 0.294)
- Swing 50.9% · whiff/swing 10.2%
- **Top swing (season):** HI-MID 81.6%; MID-AWAY 79.2%; LO-AWAY 75.8%; HI-IN (3B) 69.2%
- **Top damage season (xwOBA BIP):** HI-IN (3B) 0.297 (EV 77.9, brl 0.0%, BIP 12); HEART 0.290 (EV 83.8, brl 0.0%, BIP 27); OUT-DN-1B 0.283 (EV 71.4, brl 0.0%, BIP 9); MID-AWAY 0.271 (EV 89.4, brl 0.0%, BIP 25)
- **COLD vs his tunnel:** LO-IN (W 9.8%, xwOBA 0.258 · SEASON_ONLY); OUT-UP-1B (W 8.3%, xwOBA 0.26 · SEASON_ONLY); OUT-UP-3B (W 8.3%, xwOBA 0.088 · SEASON_ONLY)

### Ben Williamson (stand R, vs LHP, season n=654, recent n=47)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `TUNNEL`** — damages his dump OUT-DN-3B (W 17.2% ST+FC) (swing 26.6% · whiff 48.5% · xwOBA 0.35)
- Swing 45.3% · whiff/swing 17.2%
- **Top swing (season):** HI-IN (3B) 73.3%; HI-MID 73.3%; LO-AWAY 66.7%; MID-IN 63.2%
- **Top damage season (xwOBA BIP):** HI-IN (3B) 0.456 (EV 90.7, brl 11.1%, BIP 9); MID-IN 0.368 (EV 91.8, brl 15.4%, BIP 13); HI-MID 0.366 (EV 88.4, brl 0.0%, BIP 9); HEART 0.325 (EV 93.0, brl 0.0%, BIP 22)
- **HOT/WARM overlap:** WARM OUT-DN-3B (W 17.2%, xwOBA 0.35 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM MID-IN (W 6.5%, xwOBA 0.368 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM HI-MID (W 5.9%, xwOBA 0.366 · SEASON_ONLY) [LOW_SAMPLE_ZONE]

### Taylor Walls (stand R, vs LHP, season n=641, recent n=61)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `TAKE`** — takes dump OUT-DN-3B (swing 15.7%) — not a Hits lean on that pitch (swing 15.7% · whiff 38.5% · xwOBA nan)
- Swing 46.2% · whiff/swing 18.6%
- **Top swing (season):** HI-MID 76.9%; MID-AWAY 70.6%; HEART 70.0%; HI-IN (3B) 69.2%
- **Top damage season (xwOBA BIP):** OUT-UP-1B 0.253 (EV 69.7, brl 0.0%, BIP 12); HI-IN (3B) 0.245 (EV 76.5, brl 0.0%, BIP 8); HI-MID 0.235 (EV 84.0, brl 0.0%, BIP 14); LO-MID 0.225 (EV 83.2, brl 0.0%, BIP 14)
- **COLD vs his tunnel:** OUT-UP-1B (W 13.0%, xwOBA 0.253, recent — · SEASON_ONLY); HEART (W 8.1%, xwOBA 0.218 · SEASON_ONLY); OUT-DN-1B (W 11.8%, xwOBA 0.121, recent — · SEASON_ONLY)

## Hits / H+R+RBI board (same slate)

| Slot | Batter | Hits | Exp H | P(1+) | PA | RBI | HR/RBI | Zone note |
|------|--------|------|-------|-------|----|-----|--------|-----------|
| 7 | Victor Mesa Jr. | 61.0 | 0.52 | 45% | 2 | thin | 57.2 | MISTAKE OUT-DN-3B; CONFIRM COLD OUT-DN-3B; COLD OUT-DN-3B; LOW_SAMPLE_BATTER+LOW_SAMPLE_RECENT |
| 4 | Junior Caminero | 60.9 | 0.66 | 52% | 3 | prime | 61.0 | TUNNEL OUT-DN-3B; HOT OUT-UP-1B/OUT-DN-3B; LOW_SAMPLE_RECENT |
| 1 | Yandy Díaz | 54.9 | 0.62 | 50% | 3 | thin | 55.0 | TUNNEL OUT-DN-3B; HOT OUT-DN-3B/HEART; LOW_SAMPLE_RECENT |
| 2 | Ryan Vilade | 52.5 | 0.53 | 44% | 3 | good | 51.2 | TUNNEL OUT-DN-3B; HOT OUT-DN-3B/OUT-DN-1B; LOW_SAMPLE_RECENT |
| 6 | Jonny DeLuca | 45.0 | 0.33 | 31% | 2 | thin | 41.7 | MISTAKE OUT-DN-3B; HOT LO-MID/LO-IN; COLD OUT-DN-1B; CONFLICT OUT-DN-1B; LOW_SAMPLE_RECENT |
| 8 | Nick Fortes | 44.8 | 0.39 | 35% | 2 | thin | 42.6 | MISTAKE OUT-DN-3B; HOT LO-MID; COLD HEART; LOW_SAMPLE_RECENT |
| 3 | Chandler Simpson | 42.9 | 0.68 | 54% | 3 | good | 37.5 | TAKE OUT-DN-3B; COLD LO-IN; LOW_SAMPLE_RECENT |
| 5 | Ben Williamson | 42.1 | 0.49 | 41% | 3 | good | 41.4 | TUNNEL OUT-DN-3B; WARM OUT-DN-3B/MID-IN; LOW_SAMPLE_RECENT |
| 9 | Taylor Walls | 35.1 | 0.27 | 25% | 2 | thin | 33.6 | TAKE OUT-DN-3B; COLD OUT-UP-1B; LOW_SAMPLE_RECENT |

*Generated by `mlb-k-matchups/zone_overlap.py` — re-run on future slates with `--hits` + `--pitcher`. Prefer CONFIRM **TUNNEL** HOTs; MISTAKE = heart/in-zone, not the dump. Treat `LOW_SAMPLE_*` as sizing FYI.*
