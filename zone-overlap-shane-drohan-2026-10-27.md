# Zone overlap — vs Shane Drohan (2026 Statcast)

**Game:** MIL@TB
**Pitcher:** Shane Drohan (LHP, id 675660) · n=2244 pitches
**Windows:** season + **last 30d** (pitcher recent n=46)

Catcher’s view. Display-only — does not change Exp K or hits scores. HOT/WARM/COLD use **season** pitcher location × batter **damage**; **dump fit** adds where they **swing** on his LHB/RHB tunnel. **recent** confirms or flags conflict. `LOW_SAMPLE_*` = FYI — size down, don’t veto automatically.

**Mix:** FF 28% / SL 21% / SI 20% / CU 12% / FC 12% / CH 6%
**Velo:** CH ~85.8, CU ~80.6, FC ~90.7, FF ~94.9, SI ~94.9, SL ~86.3

## Where the pitcher throws

### vs LHB — in-zone 51% · heart 8% · mean px=-0.333 (neg=3B) pz=2.095

- Top zones: OUT-DN-3B 29%, LO-IN 9%, LO-MID 9%, HEART 8%, OUT-UP-3B 7%, OUT-UP-1B 7%
- **Usage vs this hand:** SL 38%, SI 27%, FF 24%, FC 11%, CU 1%, CH 0%
- **FC lands:** OUT-DN-3B 28%, OUT-UP-3B 12%, HEART 11%
- **FF lands:** OUT-UP-3B 19%, OUT-DN-3B 16%, OUT-UP-1B 12%
- **SI lands:** OUT-DN-3B 20%, HEART 13%, OUT-DN-1B 11%
- **SL lands:** OUT-DN-3B 44%, LO-IN 14%, LO-MID 12%
- **Zone → pitch mix:** OUT-DN-3B (29% throws → SL 56%+SI 19%); LO-IN (9% throws → SL 56%+SI 23%); LO-MID (9% throws → SL 49%+SI 26%); HEART (8% throws → SI 40%+SL 30%)
- **Dump (ticket tunnel):** OUT-DN-3B 29.1% SL+SI · chase

### vs RHB — in-zone 47% · heart 7% · mean px=-0.045 (neg=3B) pz=2.187

- Top zones: OUT-DN-3B 22%, OUT-UP-1B 13%, OUT-DN-1B 11%, HEART 7%, OUT-UP-3B 7%, LO-MID 7%
- **Usage vs this hand:** FF 30%, SI 18%, CU 18%, SL 14%, FC 13%, CH 8%
- **CH lands:** OUT-DN-1B 27%, OUT-DN-3B 26%, OUT-UP-1B 22%
- **CU lands:** OUT-DN-3B 37%, OUT-DN-1B 16%, LO-MID 9%
- **FC lands:** OUT-DN-3B 25%, OUT-UP-3B 10%, MID-IN 10%
- **FF lands:** OUT-UP-1B 20%, OUT-UP-3B 18%, HI-MID 11%
- **SI lands:** OUT-DN-3B 17%, LO-MID 13%, MID-AWAY 12%
- **SL lands:** OUT-DN-3B 32%, OUT-DN-1B 21%, LO-IN 8%
- **Zone → pitch mix:** OUT-DN-3B (22% throws → CU 29%+SL 21%); OUT-UP-1B (13% throws → FF 48%+CH 14%); OUT-DN-1B (11% throws → SL 27%+CU 26%); HEART (7% throws → FF 30%+SI 25%)
- **Dump (ticket tunnel):** OUT-DN-3B 22.2% CU+SL · chase; OUT-UP-1B 12.7% FF+CH · chase

## Dump × swing (vs LHB / RHB)

Pitcher’s #1 throw pocket vs that batter’s hand, crossed with whether they **swing** there. TUNNEL = Hits location. MISTAKE = hunt middle, not the dump. CHASE/TAKE = not a Hits lean on the tunnel (K / take).

| Batter | Stand | Dump | Throw | Swing | Whiff | xwOBA | Fit |
|--------|-------|------|-------|-------|-------|-------|-----|
| Victor Mesa Jr. | L | OUT-DN-3B | 29.1% SL+SI | 32.9 | 46.4 | 0.179 | **MISTAKE** |
| Junior Caminero | R | OUT-DN-3B | 22.2% CU+SL | 22.2 | 29.4 | 0.555 | **TUNNEL** |
| Yandy Díaz | R | OUT-DN-3B | 22.2% CU+SL | 28.2 | 18.2 | 0.541 | **TUNNEL** |
| Ryan Vilade | R | OUT-DN-3B | 22.2% CU+SL | 34.1 | 43.2 | 0.497 | **TUNNEL** |
| Jonny DeLuca | R | OUT-DN-3B | 22.2% CU+SL | 47.3 | 38.6 | 0.334 | **MISTAKE** |
| Nick Fortes | R | OUT-DN-3B | 22.2% CU+SL | 23.8 | 56.0 | nan | **MISTAKE** |
| Chandler Simpson | L | OUT-DN-3B | 29.1% SL+SI | 21.6 | 48.5 | 0.294 | **TAKE** |
| Ben Williamson | R | OUT-DN-3B | 22.2% CU+SL | 27.2 | 47.1 | 0.35 | **TUNNEL** |
| Taylor Walls | R | OUT-DN-3B | 22.2% CU+SL | 15.7 | 38.5 | nan | **TAKE** |

## Batter heat vs opposing hand → overlap

### Victor Mesa Jr. (stand L, vs LHP, season n=329, recent n=103)
- **FYI sample:** LOW_SAMPLE_BATTER, LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-DN-3B; HOT in-zone HEART (swing 32.9% · whiff 46.4% · xwOBA 0.179)
- Swing 54.4% · whiff/swing 20.1%
- **Top swing (season):** HEART 85.7%; MID-IN 66.7%; OUT-UP-1B 33.3%; OUT-DN-3B 32.9%
- **Top damage season (xwOBA BIP):** HEART 0.396 (EV 87.9, brl 8.3%, BIP 12); OUT-DN-3B 0.179 (EV 71.1, brl 0.0%, BIP 8)
- **HOT/WARM overlap:** WARM HEART (W 8.4%, xwOBA 0.396 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM OUT-UP-1B (W 6.9%, xwOBA 0.364 · SEASON_ONLY) [LOW_SAMPLE_ZONE]
- **COLD vs his tunnel:** OUT-DN-3B (W 29.1%, xwOBA 0.179, recent COLD · CONFIRM); LO-MID (W 9.0%, xwOBA 0.17 · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** COLD OUT-DN-3B

### Junior Caminero (stand R, vs LHP, season n=842, recent n=66)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `TUNNEL`** — damages his dump OUT-DN-3B (W 22.2% CU+SL) (swing 22.2% · whiff 29.4% · xwOBA 0.555)
- Swing 41.4% · whiff/swing 19.2%
- **Top swing (season):** HEART 70.0%; MID-AWAY 69.2%; HI-MID 68.9%; HI-IN (3B) 65.4%
- **Top damage season (xwOBA BIP):** HI-MID 0.818 (EV 103.0, brl 33.3%, BIP 12); OUT-UP-1B 0.734 (EV 99.8, brl 33.3%, BIP 9); MID-AWAY 0.425 (EV 96.2, brl 21.4%, BIP 14); OUT-UP-3B 0.401 (EV 86.9, brl 12.5%, BIP 8)
- **HOT/WARM overlap:** HOT OUT-DN-3B (W 22.2%, xwOBA 0.555, recent — xwOBA None BIP 0 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT OUT-UP-1B (W 12.7%, xwOBA 0.734, recent — xwOBA None BIP 2 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM OUT-DN-1B (W 11.2%, xwOBA 0.352, recent — xwOBA None BIP 2 · SEASON_ONLY); HOT OUT-UP-3B (W 7.1%, xwOBA 0.401 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM HEART (W 7.3%, xwOBA 0.377 · SEASON_ONLY)
- **COLD vs his tunnel:** LO-MID (W 7.0%, xwOBA 0.25 · SEASON_ONLY)

### Yandy Díaz (stand R, vs LHP, season n=830, recent n=54)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `TUNNEL`** — damages his dump OUT-DN-3B (W 22.2% CU+SL) (swing 28.2% · whiff 18.2% · xwOBA 0.541)
- Swing 48.1% · whiff/swing 11.5%
- **Top swing (season):** HI-MID 78.0%; MID-AWAY 77.8%; HI-AWAY (1B) 71.8%; MID-IN 69.8%
- **Top damage season (xwOBA BIP):** OUT-DN-3B 0.541 (EV 96.0, brl 14.3%, BIP 14); HEART 0.461 (EV 98.6, brl 16.0%, BIP 25); HI-AWAY (1B) 0.449 (EV 101.3, brl 22.2%, BIP 9); MID-AWAY 0.372 (EV 95.9, brl 0.0%, BIP 14)
- **HOT/WARM overlap:** HOT OUT-DN-3B (W 22.2%, xwOBA 0.541, recent — xwOBA None BIP 1 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT HEART (W 7.3%, xwOBA 0.461 · SEASON_ONLY); WARM LO-MID (W 7.0%, xwOBA 0.359 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM MID-AWAY (W 6.1%, xwOBA 0.372 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM MID-IN (W 5.5%, xwOBA 0.36 · SEASON_ONLY)

### Ryan Vilade (stand R, vs LHP, season n=779, recent n=54)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `TUNNEL`** — damages his dump OUT-DN-3B (W 22.2% CU+SL) (swing 34.1% · whiff 43.2% · xwOBA 0.497)
- Swing 49.2% · whiff/swing 20.9%
- **Top swing (season):** HI-MID 88.1%; LO-AWAY 84.8%; HI-IN (3B) 84.6%; HEART 81.0%
- **Top damage season (xwOBA BIP):** HI-MID 0.661 (EV 92.1, brl 12.5%, BIP 8); LO-MID 0.615 (EV 94.4, brl 15.4%, BIP 13); MID-IN 0.524 (EV 89.4, brl 10.0%, BIP 20); OUT-DN-3B 0.497 (EV 85.2, brl 11.1%, BIP 9)
- **HOT/WARM overlap:** HOT OUT-DN-3B (W 22.2%, xwOBA 0.497 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT OUT-DN-1B (W 11.2%, xwOBA 0.416 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT LO-MID (W 7.0%, xwOBA 0.615 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM MID-IN (W 5.5%, xwOBA 0.524 · SEASON_ONLY)
- **COLD vs his tunnel:** HEART (W 7.3%, xwOBA 0.275 · SEASON_ONLY)

### Jonny DeLuca (stand R, vs LHP, season n=691, recent n=80)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-DN-3B; HOT in-zone LO-MID/HEART (swing 47.3% · whiff 38.6% · xwOBA 0.334)
- Swing 55.0% · whiff/swing 21.8%
- **Top swing (season):** HI-MID 81.0%; LO-AWAY 80.6%; HEART 78.3%; LO-MID 77.5%
- **Top damage season (xwOBA BIP):** LO-MID 0.477 (EV 95.2, brl 7.1%, BIP 14); HI-MID 0.453 (EV 82.3, brl 6.2%, BIP 16); HEART 0.368 (EV 94.8, brl 0.0%, BIP 11); MID-IN 0.347 (EV 75.8, brl 0.0%, BIP 12)
- **HOT/WARM overlap:** HOT LO-MID (W 7.0%, xwOBA 0.477 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM HEART (W 7.3%, xwOBA 0.368 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM LO-IN (W 5.4%, xwOBA 0.444 · SEASON_ONLY) [LOW_SAMPLE_ZONE]
- **COLD vs his tunnel:** OUT-UP-1B (W 12.7%, xwOBA 0.125, recent — · SEASON_ONLY)

### Nick Fortes (stand R, vs LHP, season n=635, recent n=14)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-DN-3B; HOT in-zone LO-MID (swing 23.8% · whiff 56.0% · xwOBA nan)
- Swing 51.5% · whiff/swing 16.2%
- **Top swing (season):** HI-IN (3B) 80.0%; HI-MID 76.7%; MID-IN 76.7%; MID-AWAY 69.6%
- **Top damage season (xwOBA BIP):** LO-MID 0.420 (EV 100.2, brl 12.5%, BIP 8); OUT-UP-3B 0.413 (EV 67.0, brl 0.0%, BIP 8); HI-AWAY (1B) 0.348 (EV 92.7, brl 0.0%, BIP 9); HI-MID 0.317 (EV 75.4, brl 0.0%, BIP 13)
- **HOT/WARM overlap:** HOT LO-MID (W 7.0%, xwOBA 0.42 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT OUT-UP-3B (W 7.1%, xwOBA 0.413 · SEASON_ONLY) [LOW_SAMPLE_ZONE]
- **COLD vs his tunnel:** HEART (W 7.3%, xwOBA 0.215 · SEASON_ONLY)

### Chandler Simpson (stand L, vs LHP, season n=717, recent n=49)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `TAKE`** — takes dump OUT-DN-3B (swing 21.6%) — not a Hits lean on that pitch (swing 21.6% · whiff 48.5% · xwOBA 0.294)
- Swing 50.9% · whiff/swing 10.1%
- **Top swing (season):** HI-MID 81.6%; MID-AWAY 79.2%; LO-AWAY 75.8%; HI-IN (3B) 69.2%
- **Top damage season (xwOBA BIP):** HI-IN (3B) 0.297 (EV 77.9, brl 0.0%, BIP 12); HEART 0.290 (EV 84.2, brl 0.0%, BIP 28); OUT-DN-1B 0.283 (EV 71.4, brl 0.0%, BIP 9); MID-AWAY 0.271 (EV 89.4, brl 0.0%, BIP 25)
- **COLD vs his tunnel:** LO-IN (W 9.1%, xwOBA 0.258 · SEASON_ONLY); LO-MID (W 9.0%, xwOBA 0.242 · SEASON_ONLY); OUT-UP-3B (W 7.2%, xwOBA 0.088 · SEASON_ONLY)

### Ben Williamson (stand R, vs LHP, season n=666, recent n=59)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `TUNNEL`** — damages his dump OUT-DN-3B (W 22.2% CU+SL) (swing 27.2% · whiff 47.1% · xwOBA 0.35)
- Swing 45.2% · whiff/swing 16.9%
- **Top swing (season):** HI-IN (3B) 73.3%; HI-MID 71.0%; LO-AWAY 67.6%; MID-IN 63.2%
- **Top damage season (xwOBA BIP):** HI-IN (3B) 0.456 (EV 90.7, brl 11.1%, BIP 9); MID-IN 0.368 (EV 91.8, brl 15.4%, BIP 13); HI-MID 0.366 (EV 88.4, brl 0.0%, BIP 9); HEART 0.325 (EV 93.0, brl 0.0%, BIP 22)
- **HOT/WARM overlap:** WARM OUT-DN-3B (W 22.2%, xwOBA 0.35, recent — xwOBA nan BIP 1 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM MID-IN (W 5.5%, xwOBA 0.368 · SEASON_ONLY) [LOW_SAMPLE_ZONE]
- **COLD vs his tunnel:** LO-MID (W 7.0%, xwOBA 0.186 · SEASON_ONLY); OUT-UP-3B (W 7.1%, xwOBA 0.193 · SEASON_ONLY)

### Taylor Walls (stand R, vs LHP, season n=648, recent n=64)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `TAKE`** — takes dump OUT-DN-3B (swing 15.7%) — not a Hits lean on that pitch (swing 15.7% · whiff 38.5% · xwOBA nan)
- Swing 46.0% · whiff/swing 18.5%
- **Top swing (season):** HI-MID 76.9%; MID-AWAY 70.6%; HEART 70.0%; HI-IN (3B) 69.2%
- **Top damage season (xwOBA BIP):** OUT-UP-1B 0.265 (EV 71.3, brl 0.0%, BIP 13); HI-IN (3B) 0.245 (EV 76.5, brl 0.0%, BIP 8); HI-MID 0.235 (EV 84.0, brl 0.0%, BIP 14); LO-MID 0.225 (EV 83.2, brl 0.0%, BIP 14)
- **COLD vs his tunnel:** OUT-UP-1B (W 12.7%, xwOBA 0.265, recent — · SEASON_ONLY); HEART (W 7.3%, xwOBA 0.218 · SEASON_ONLY); LO-MID (W 7.0%, xwOBA 0.225 · SEASON_ONLY)

## Hits / H+R+RBI board (same slate)

| Slot | Batter | Hits | Exp H | P(1+) | PA | RBI | HR/RBI | Zone note |
|------|--------|------|-------|-------|----|-----|--------|-----------|
| 7 | Victor Mesa Jr. | 61.0 | 0.48 | 42% | 2 | thin | 57.2 | MISTAKE OUT-DN-3B; CONFIRM COLD OUT-DN-3B; COLD OUT-DN-3B; LOW_SAMPLE_BATTER+LOW_SAMPLE_RECENT |
| 4 | Junior Caminero | 60.9 | 0.62 | 50% | 3 | prime | 61.0 | TUNNEL OUT-DN-3B; HOT OUT-DN-3B/OUT-UP-1B; COLD LO-MID; LOW_SAMPLE_RECENT |
| 1 | Yandy Díaz | 54.9 | 0.60 | 49% | 3 | thin | 55.0 | TUNNEL OUT-DN-3B; HOT OUT-DN-3B/HEART; LOW_SAMPLE_RECENT |
| 2 | Ryan Vilade | 52.5 | 0.50 | 42% | 3 | good | 51.2 | TUNNEL OUT-DN-3B; HOT OUT-DN-3B/OUT-DN-1B; COLD HEART; LOW_SAMPLE_RECENT |
| 6 | Jonny DeLuca | 45.0 | 0.35 | 32% | 2 | thin | 41.7 | MISTAKE OUT-DN-3B; HOT LO-MID; COLD OUT-UP-1B; LOW_SAMPLE_RECENT |
| 8 | Nick Fortes | 44.8 | 0.38 | 35% | 2 | thin | 42.6 | MISTAKE OUT-DN-3B; HOT LO-MID/OUT-UP-3B; COLD HEART; LOW_SAMPLE_RECENT |
| 3 | Chandler Simpson | 42.9 | 0.65 | 52% | 3 | good | 37.5 | TAKE OUT-DN-3B; COLD LO-IN; LOW_SAMPLE_RECENT |
| 5 | Ben Williamson | 42.1 | 0.51 | 43% | 3 | good | 41.4 | TUNNEL OUT-DN-3B; WARM OUT-DN-3B/MID-IN; COLD LO-MID; LOW_SAMPLE_RECENT |
| 9 | Taylor Walls | 35.1 | 0.26 | 25% | 2 | thin | 33.6 | TAKE OUT-DN-3B; COLD OUT-UP-1B; LOW_SAMPLE_RECENT |

*Generated by `mlb-k-matchups/zone_overlap.py` — re-run on future slates with `--hits` + `--pitcher`. Prefer CONFIRM **TUNNEL** HOTs; MISTAKE = heart/in-zone, not the dump. Treat `LOW_SAMPLE_*` as sizing FYI.*
