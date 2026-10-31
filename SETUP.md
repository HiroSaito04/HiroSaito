# Pixel Pathfinder Setup

This repository must remain:

- **Repository name:** `HiroSaito04`
- **Visibility:** Public

## Update your existing profile repo

If your repo already exists locally, replace the old files with the contents of this updated ZIP, then run:

```bash
git add -A
git commit -m "Update profile to Pixel Pathfinder theme"
git push origin main
```

## If the contribution snake does not appear

Go to GitHub:

**Actions** → **Generate Snake Animation** → **Run workflow**

Then refresh your profile.

## Main files

- `README.md` → main GitHub profile content
- `assets/hero.png` → top banner
- `assets/save-file.png` → player/save card
- `assets/pathfinder.gif` → animated pathfinder scene
- `assets/contribution-run.gif` → animated contribution scene with moving sprite
- `.github/workflows/snake.yml` → GitHub contribution snake workflow
- `scripts/build_pathfinder_assets.py` → regenerates the pixel assets
