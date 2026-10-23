# Zone overlap — vs Nick Martinez (2026 Statcast)

**Game:** TB@MIL
**Pitcher:** Nick Martinez (RHP, id 607259) · n=2928 pitches
**Windows:** season + **last 30d** (pitcher recent n=192)

Catcher’s view. Display-only — does not change Exp K or hits scores. HOT/WARM/COLD use **season** pitcher location × batter **damage**; **dump fit** adds where they **swing** on his LHB/RHB tunnel. **recent** confirms or flags conflict. `LOW_SAMPLE_*` = FYI — size down, don’t veto automatically.

**Mix:** SI 30% / CH 26% / FC 22% / FF 13% / SL 5% / CU 4% / PO 0%
**Velo:** CH ~78.2, CU ~79.9, FC ~89.2, FF ~92.7, PO ~93.2, SI ~92.4, SL ~85.2

## Where the pitcher throws

### vs LHB — in-zone 54% · heart 8% · mean px=-0.026 (neg=3B) pz=2.397

- Top zones: OUT-DN-3B 14%, OUT-UP-1B 12%, OUT-UP-3B 11%, OUT-DN-1B 10%, HEART 8%, MID-AWAY 7%
- **Usage vs this hand:** CH 29%, SI 24%, FC 23%, FF 15%, SL 5%, CU 4%, PO 0%
- **CH lands:** OUT-DN-3B 35%, OUT-UP-3B 15%, LO-IN 10%
- **CU lands:** OUT-UP-3B 17%, OUT-DN-3B 17%, OUT-DN-1B 17%
- **FC lands:** OUT-UP-1B 19%, OUT-DN-1B 15%, MID-AWAY 14%
- **FF lands:** OUT-UP-3B 21%, OUT-UP-1B 14%, MID-IN 10%
- **SI lands:** OUT-UP-1B 19%, HI-AWAY (1B) 15%, MID-AWAY 13%
- **SL lands:** OUT-DN-3B 22%, OUT-DN-1B 16%, HEART 13%
- **Zone → pitch mix:** OUT-DN-3B (14% throws → CH 75%+SL 8%); OUT-UP-1B (11% throws → SI 40%+FC 37%); OUT-UP-3B (11% throws → CH 41%+FF 28%); OUT-DN-1B (10% throws → FC 33%+CH 26%)
- **Dump (ticket tunnel):** OUT-DN-3B 13.8% CH+SL · chase; OUT-UP-1B 11.5% SI+FC · chase

### vs RHB — in-zone 51% · heart 8% · mean px=-0.028 (neg=3B) pz=2.187

- Top zones: OUT-DN-1B 18%, OUT-UP-3B 13%, OUT-DN-3B 12%, HEART 8%, LO-MID 7%, LO-AWAY 6%
- **Usage vs this hand:** SI 38%, CH 22%, FC 21%, FF 11%, SL 4%, CU 4%
- **CH lands:** OUT-DN-3B 33%, OUT-DN-1B 24%, OUT-UP-3B 7%
- **CU lands:** OUT-DN-1B 21%, OUT-DN-3B 21%, OUT-UP-3B 19%
- **FC lands:** OUT-DN-1B 31%, MID-AWAY 15%, HEART 11%
- **FF lands:** OUT-UP-1B 29%, OUT-UP-3B 22%, HI-MID 12%
- **SI lands:** OUT-UP-3B 19%, MID-IN 10%, HI-IN (3B) 10%
- **SL lands:** OUT-DN-1B 52%, LO-AWAY 12%, LO-MID 10%
- **Zone → pitch mix:** OUT-DN-1B (18% throws → FC 36%+CH 29%); OUT-UP-3B (13% throws → SI 58%+FF 19%); OUT-DN-3B (12% throws → CH 59%+SI 30%); HEART (8% throws → SI 47%+FC 32%)
- **Dump (ticket tunnel):** OUT-DN-1B 17.9% FC+CH · chase; OUT-UP-3B 12.6% SI+FF · chase

## Dump × swing (vs LHB / RHB)

Pitcher’s #1 throw pocket vs that batter’s hand, crossed with whether they **swing** there. TUNNEL = Hits location. MISTAKE = hunt middle, not the dump. CHASE/TAKE = not a Hits lean on the tunnel (K / take).

| Batter | Stand | Dump | Throw | Swing | Whiff | xwOBA | Fit |
|--------|-------|------|-------|-------|-------|-------|-----|
| Jake Bauers | L | OUT-DN-3B | 13.8% CH+SL | 21.3 | 63.0 | 0.247 | **MISTAKE** |
| Garrett Mitchell | L | OUT-DN-3B | 13.8% CH+SL | 33.9 | 59.5 | 0.197 | **MISTAKE** |
| Jackson Chourio | R | OUT-DN-1B | 17.9% FC+CH | 26.6 | 68.7 | 0.255 | **MISTAKE** |
| Brice Turang | L | OUT-DN-3B | 13.8% CH+SL | 31.2 | 32.5 | 0.293 | **MISTAKE** |
| William Contreras | R | OUT-DN-1B | 17.9% FC+CH | 22.5 | 59.6 | 0.277 | **MISTAKE** |
| Cooper Pratt | R | OUT-DN-1B | 17.9% FC+CH | 26.7 | 48.4 | 0.398 | **TUNNEL** |
| Christian Yelich | L | OUT-DN-3B | 13.8% CH+SL | 33.5 | 50.8 | 0.226 | **MISTAKE** |
| David Hamilton | L | OUT-DN-3B | 13.8% CH+SL | 34.1 | 50.0 | 0.194 | **MISTAKE** |
| Sal Frelick | L | OUT-DN-3B | 13.8% CH+SL | 32.7 | 8.8 | 0.187 | **COLD** |

## Batter heat vs opposing hand → overlap

### Jake Bauers (stand L, vs RHP, season n=1956, recent n=158)
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-DN-3B; HOT in-zone HEART/HI-MID (swing 21.3% · whiff 63.0% · xwOBA 0.247)
- Swing 39.2% · whiff/swing 28.6%
- **Top swing (season):** HEART 77.4%; HI-MID 73.6%; MID-AWAY 62.8%; HI-AWAY (1B) 61.1%
- **Top damage season (xwOBA BIP):** OUT-UP-1B 0.764 (EV 84.9, brl 20.0%, BIP 10); HI-MID 0.644 (EV 101.6, brl 24.0%, BIP 25); HI-AWAY (1B) 0.566 (EV 83.5, brl 36.4%, BIP 11); MID-IN 0.506 (EV 98.1, brl 16.7%, BIP 30)
- **HOT/WARM overlap:** HOT HEART (W 8.1%, xwOBA 0.447, recent HOT xwOBA 0.426 BIP 3 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; HOT OUT-UP-1B (W 11.5%, xwOBA 0.764, recent — xwOBA nan BIP 0 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT HI-MID (W 6.8%, xwOBA 0.644, recent — xwOBA nan BIP 1 · SEASON_ONLY); HOT HI-AWAY (1B) (W 6.2%, xwOBA 0.566, recent — xwOBA nan BIP 2 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT MID-IN (W 6.3%, xwOBA 0.506, recent — xwOBA nan BIP 2 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-DN-3B (W 13.8%, xwOBA 0.247, recent — · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** HOT HEART

### Garrett Mitchell (stand L, vs RHP, season n=1819, recent n=128)
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-DN-3B; HOT in-zone MID-IN/LO-MID (swing 33.9% · whiff 59.5% · xwOBA 0.197)
- Swing 45.6% · whiff/swing 33.9%
- **Top swing (season):** HEART 80.2%; HI-MID 79.0%; MID-IN 69.7%; HI-AWAY (1B) 67.1%
- **Top damage season (xwOBA BIP):** LO-AWAY 0.652 (EV 97.8, brl 11.8%, BIP 17); HI-MID 0.625 (EV 100.2, brl 26.7%, BIP 15); HEART 0.586 (EV 99.8, brl 19.1%, BIP 47); MID-IN 0.554 (EV 97.2, brl 11.1%, BIP 27)
- **Top damage recent (30d):** LO-IN 0.372 (BIP 6)
- **HOT/WARM overlap:** HOT MID-IN (W 6.3%, xwOBA 0.554, recent WARM xwOBA 0.456 BIP 3 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; WARM LO-MID (W 5.4%, xwOBA 0.481, recent HOT xwOBA 0.412 BIP 3 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; HOT OUT-UP-1B (W 11.5%, xwOBA 0.611, recent — xwOBA nan BIP 0 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT HEART (W 8.1%, xwOBA 0.586 · SEASON_ONLY); HOT OUT-DN-1B (W 10.3%, xwOBA 0.421, recent — xwOBA nan BIP 0 · SEASON_ONLY) [LOW_SAMPLE_ZONE]
- **COLD vs his tunnel:** OUT-DN-3B (W 13.8%, xwOBA 0.197, recent — · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** HOT MID-IN, WARM LO-MID

### Jackson Chourio (stand R, vs RHP, season n=1727, recent n=125)
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-DN-1B; HOT in-zone HEART/MID-IN (swing 26.6% · whiff 68.7% · xwOBA 0.255)
- Swing 48.9% · whiff/swing 24.1%
- **Top swing (season):** MID-IN 77.1%; HI-IN (3B) 74.6%; HEART 72.4%; HI-MID 69.1%
- **Top damage season (xwOBA BIP):** HEART 0.651 (EV 98.6, brl 26.2%, BIP 42); MID-IN 0.548 (EV 96.1, brl 24.3%, BIP 37); HI-MID 0.501 (EV 98.2, brl 22.7%, BIP 22); LO-IN 0.441 (EV 96.5, brl 10.0%, BIP 20)
- **Top damage recent (30d):** LO-AWAY 0.387 (BIP 5)
- **HOT/WARM overlap:** HOT HEART (W 7.7%, xwOBA 0.651 · SEASON_ONLY); WARM OUT-UP-3B (W 12.6%, xwOBA 0.358, recent COLD xwOBA 0.197 BIP 3 · CONFLICT) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; HOT MID-IN (W 6.2%, xwOBA 0.548, recent — xwOBA 0.575 BIP 4 · SEASON_ONLY); WARM HI-MID (W 5.4%, xwOBA 0.501 · SEASON_ONLY); HOT LO-IN (W 6.0%, xwOBA 0.441 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-DN-1B (W 17.9%, xwOBA 0.255, recent — · SEASON_ONLY); OUT-DN-3B (W 12.2%, xwOBA 0.194, recent — · SEASON_ONLY)
- **Season vs recent CONFLICT:** OUT-UP-3B (WARM→COLD)

### Brice Turang (stand L, vs RHP, season n=2199, recent n=144)
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-DN-3B; HOT in-zone LO-MID/MID-IN (swing 31.2% · whiff 32.5% · xwOBA 0.293)
- Swing 44.1% · whiff/swing 19.0%
- **Top swing (season):** HI-MID 74.1%; HI-AWAY (1B) 71.4%; MID-AWAY 71.3%; HEART 68.8%
- **Top damage season (xwOBA BIP):** LO-AWAY 0.554 (EV 97.0, brl 17.2%, BIP 29); HEART 0.553 (EV 95.8, brl 17.1%, BIP 41); OUT-DN-1B 0.517 (EV 92.9, brl 7.7%, BIP 13); LO-MID 0.504 (EV 89.6, brl 9.3%, BIP 54)
- **HOT/WARM overlap:** WARM LO-MID (W 5.4%, xwOBA 0.504, recent HOT xwOBA 0.511 BIP 3 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; WARM MID-IN (W 6.3%, xwOBA 0.375, recent WARM xwOBA 0.414 BIP 3 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; HOT OUT-DN-1B (W 10.3%, xwOBA 0.517, recent — xwOBA nan BIP 0 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT HEART (W 8.1%, xwOBA 0.553, recent — xwOBA nan BIP 2 · SEASON_ONLY); WARM OUT-UP-1B (W 11.5%, xwOBA 0.351, recent — xwOBA nan BIP 1 · SEASON_ONLY) [LOW_SAMPLE_ZONE]
- **COLD vs his tunnel:** OUT-UP-3B (W 10.9%, xwOBA 0.262, recent — · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** WARM LO-MID, WARM MID-IN

### William Contreras (stand R, vs RHP, season n=1766, recent n=131)
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-DN-1B; HOT in-zone HEART/LO-AWAY (swing 22.5% · whiff 59.6% · xwOBA 0.277)
- Swing 47.8% · whiff/swing 17.5%
- **Top swing (season):** HI-MID 80.6%; HEART 76.3%; MID-IN 74.3%; HI-IN (3B) 73.6%
- **Top damage season (xwOBA BIP):** OUT-DN-3B 0.487 (EV 90.6, brl 7.1%, BIP 14); HI-IN (3B) 0.453 (EV 91.6, brl 20.6%, BIP 34); OUT-UP-1B 0.430 (EV 83.5, brl 16.7%, BIP 12); LO-AWAY 0.428 (EV 90.2, brl 3.7%, BIP 27)
- **HOT/WARM overlap:** HOT OUT-DN-3B (W 12.2%, xwOBA 0.487 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; WARM HEART (W 7.7%, xwOBA 0.395, recent — xwOBA nan BIP 2 · SEASON_ONLY); HOT LO-AWAY (W 6.2%, xwOBA 0.428, recent — xwOBA nan BIP 2 · SEASON_ONLY); HOT OUT-UP-1B (W 6.1%, xwOBA 0.43 · SEASON_ONLY) [LOW_SAMPLE_ZONE]; HOT LO-IN (W 6.0%, xwOBA 0.425 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-DN-1B (W 17.9%, xwOBA 0.277, recent HOT · CONFLICT); OUT-UP-3B (W 12.6%, xwOBA 0.211, recent — · SEASON_ONLY)
- **Season vs recent CONFLICT:** OUT-DN-1B (COLD→HOT)

### Cooper Pratt (stand R, vs RHP, season n=975, recent n=120)
- **Dump fit `TUNNEL`** — damages his dump OUT-DN-1B (W 17.9% FC+CH) (swing 26.7% · whiff 48.4% · xwOBA 0.398)
- Swing 45.2% · whiff/swing 17.0%
- **Top swing (season):** HEART 77.3%; HI-MID 68.1%; MID-IN 64.6%; LO-MID 63.5%
- **Top damage season (xwOBA BIP):** OUT-DN-1B 0.398 (EV 82.0, brl 0.0%, BIP 17); HEART 0.370 (EV 95.1, brl 4.0%, BIP 25); MID-AWAY 0.368 (EV 91.8, brl 4.5%, BIP 22); HI-IN (3B) 0.358 (EV 80.3, brl 6.7%, BIP 15)
- **Top damage recent (30d):** LO-MID 0.249 (BIP 5)
- **HOT/WARM overlap:** WARM OUT-DN-1B (W 17.9%, xwOBA 0.398, recent — xwOBA nan BIP 2 · SEASON_ONLY); WARM HEART (W 7.7%, xwOBA 0.37, recent COLD xwOBA 0.19 BIP 4 · CONFLICT) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; WARM HI-IN (3B) (W 5.5%, xwOBA 0.358 · SEASON_ONLY); WARM MID-AWAY (W 5.3%, xwOBA 0.368, recent — xwOBA 0.285 BIP 3 · SEASON_ONLY); HOT OUT-UP-3B (W 12.6%, xwOBA 0.574, recent — xwOBA nan BIP 0 · SEASON_ONLY) [LOW_SAMPLE_ZONE]
- **COLD vs his tunnel:** OUT-DN-3B (W 12.2%, xwOBA 0.104 · SEASON_ONLY)
- **Season vs recent CONFLICT:** HEART (WARM→COLD)

### Christian Yelich (stand L, vs RHP, season n=1732, recent n=107)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-DN-3B; HOT in-zone LO-MID/HEART (swing 33.5% · whiff 50.8% · xwOBA 0.226)
- Swing 45.2% · whiff/swing 29.9%
- **Top swing (season):** HEART 75.4%; LO-MID 70.6%; HI-AWAY (1B) 70.5%; LO-AWAY 70.3%
- **Top damage season (xwOBA BIP):** HEART 0.635 (EV 95.4, brl 20.0%, BIP 30); MID-IN 0.560 (EV 98.6, brl 19.0%, BIP 21); HI-MID 0.500 (EV 82.0, brl 30.8%, BIP 13); LO-MID 0.493 (EV 96.6, brl 18.8%, BIP 32)
- **HOT/WARM overlap:** WARM LO-MID (W 5.4%, xwOBA 0.493, recent HOT xwOBA 0.774 BIP 4 · CONFIRM) [LOW_SAMPLE_ZONE,LOW_SAMPLE_RECENT]; HOT HEART (W 8.1%, xwOBA 0.635 · SEASON_ONLY); HOT MID-IN (W 6.3%, xwOBA 0.56 · SEASON_ONLY); HOT HI-MID (W 6.8%, xwOBA 0.5 · SEASON_ONLY) [LOW_SAMPLE_ZONE]
- **COLD vs his tunnel:** OUT-DN-3B (W 13.8%, xwOBA 0.226, recent — · SEASON_ONLY); OUT-DN-1B (W 10.3%, xwOBA 0.236, recent — · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** WARM LO-MID

### David Hamilton (stand L, vs RHP, season n=1446, recent n=71)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `MISTAKE`** — COLD/take on dump OUT-DN-3B; HOT in-zone HEART (swing 34.1% · whiff 50.0% · xwOBA 0.194)
- Swing 45.5% · whiff/swing 17.3%
- **Top swing (season):** MID-AWAY 76.1%; HI-MID 76.0%; HEART 70.1%; HI-AWAY (1B) 67.9%
- **Top damage season (xwOBA BIP):** LO-AWAY 0.475 (EV 96.4, brl 11.8%, BIP 17); HEART 0.432 (EV 85.7, brl 18.4%, BIP 38); LO-IN 0.363 (EV 73.9, brl 0.0%, BIP 10); MID-AWAY 0.342 (EV 87.0, brl 8.3%, BIP 36)
- **HOT/WARM overlap:** HOT HEART (W 8.1%, xwOBA 0.432 · SEASON_ONLY)
- **COLD vs his tunnel:** OUT-UP-3B (W 10.9%, xwOBA 0.231, recent COLD · CONFIRM); OUT-DN-3B (W 13.8%, xwOBA 0.194 · SEASON_ONLY); OUT-DN-1B (W 10.3%, xwOBA 0.185, recent — · SEASON_ONLY)
- **Season ∩ recent CONFIRM:** COLD OUT-UP-3B

### Sal Frelick (stand L, vs RHP, season n=1320, recent n=108)
- **FYI sample:** LOW_SAMPLE_RECENT — thin MLB / recent sample; inform size, don’t auto-fade
- **Dump fit `COLD`** — COLD on dump OUT-DN-3B — pass Hits vs this tunnel (swing 32.7% · whiff 8.8% · xwOBA 0.187)
- Swing 43.0% · whiff/swing 7.6%
- **Top swing (season):** LO-MID 67.5%; MID-AWAY 66.7%; HI-MID 64.0%; HI-AWAY (1B) 62.3%
- **Top damage season (xwOBA BIP):** LO-IN 0.324 (EV 82.3, brl 0.0%, BIP 17); OUT-UP-3B 0.317 (EV 87.7, brl 9.1%, BIP 11); HI-IN (3B) 0.314 (EV 89.1, brl 0.0%, BIP 16); HEART 0.312 (EV 90.9, brl 2.7%, BIP 37)
- **COLD vs his tunnel:** OUT-DN-3B (W 13.8%, xwOBA 0.187, recent — · SEASON_ONLY); OUT-DN-1B (W 10.3%, xwOBA 0.244, recent — · SEASON_ONLY); OUT-UP-1B (W 11.5%, xwOBA 0.189, recent — · SEASON_ONLY)

## Hits / H+R+RBI board (same slate)

| Slot | Batter | Hits | HR/RBI | AVG vs hand | Barrel | HH | Zone note |
|------|--------|------|--------|-------------|--------|----|-----------|
| 4 | Jake Bauers | 59.4 | 60.7 | 0.266 | 13.9% | 51.9% | MISTAKE OUT-DN-3B; CONFIRM HOT HEART; COLD OUT-DN-3B |
| 6 | Garrett Mitchell | 58.7 | 59.3 | 0.271 | 11.7% | 52.7% | MISTAKE OUT-DN-3B; CONFIRM HOT MID-IN/WARM LO-MID; COLD OUT-DN-3B |
| 1 | Jackson Chourio | 57.7 | 57.8 | 0.274 | 12.3% | 47.0% | MISTAKE OUT-DN-1B; HOT HEART/MID-IN; COLD OUT-DN-1B; CONFLICT OUT-UP-3B |
| 2 | Brice Turang | 55.8 | 54.0 | 0.291 | 7.7% | 41.6% | MISTAKE OUT-DN-3B; CONFIRM WARM LO-MID/WARM MID-IN; COLD OUT-UP-3B |
| 3 | William Contreras | 54.4 | 53.8 | 0.270 | 8.5% | 44.1% | MISTAKE OUT-DN-1B; HOT OUT-DN-3B/LO-AWAY; COLD OUT-DN-1B; CONFLICT OUT-DN-1B |
| 7 | Cooper Pratt | 51.5 | 47.2 | 0.306 | 3.2% | 27.4% | TUNNEL OUT-DN-1B; HOT OUT-UP-3B; COLD OUT-DN-3B; CONFLICT HEART |
| 5 | Christian Yelich | 50.2 | 50.3 | 0.244 | 9.6% | 42.9% | MISTAKE OUT-DN-3B; CONFIRM WARM LO-MID; COLD OUT-DN-3B; LOW_SAMPLE_RECENT |
| 9 | David Hamilton | 43.5 | 41.0 | 0.250 | 3.4% | 27.9% | MISTAKE OUT-DN-3B; CONFIRM COLD OUT-UP-3B; COLD OUT-UP-3B; LOW_SAMPLE_RECENT |
| 8 | Sal Frelick | 42.3 | 40.3 | 0.239 | 2.3% | 26.8% | COLD OUT-DN-3B; COLD OUT-DN-3B; LOW_SAMPLE_RECENT |

*Generated by `mlb-k-matchups/zone_overlap.py` — re-run on future slates with `--hits` + `--pitcher`. Prefer CONFIRM **TUNNEL** HOTs; MISTAKE = heart/in-zone, not the dump. Treat `LOW_SAMPLE_*` as sizing FYI.*
