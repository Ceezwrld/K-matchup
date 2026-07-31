# Live board — one bookmark

**Use this link every day (it updates in place):**

https://ceezwrld.github.io/K-matchup/

Hard-refresh before tickets. Check the green **Generated** / **Official lineups** line at the top.

## One-time setup (repo owner)

If that link 404s, enable Pages once:

1. GitHub → **K-matchup** → **Settings** → **Pages**
2. Build source: **Deploy from a branch**
3. Branch: **`gh-pages`** / folder **`/`** (root) → Save  

(or **GitHub Actions** if you prefer the Actions deployer)

After that, the same URL always shows the latest board. No new links.

## Works right now (no setup)

https://raw.githack.com/Ceezwrld/K-matchup/main/index.html

Same idea: always `main`, never a commit SHA.

## Do not use

- Commit-SHA `htmlpreview` links (`…/K-matchup/<sha>/rankings.html`) — those froze Suzuki/Kelly for you
- Any old preview URL someone pasted earlier in the day
