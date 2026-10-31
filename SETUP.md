# Setup Guide for `HiroSaito04`

This repository is your **GitHub profile repository**, so the repository name must be exactly:

`HiroSaito04`

and it must be **Public**.

## If you already pushed the previous version

Since your repository is already working, you only need to replace the files with this updated concept and push again.

## Steps in VS Code

Open the project folder in VS Code and use the terminal:

```bash
git status
```

If you copied the updated files into the same project folder, commit and push them:

```bash
git add .
git commit -m "Redesign profile concept and assets"
git push origin main
```

## If the snake is not yet updating

Go to:

`Actions` → `Generate Snake Animation` → `Run workflow`

After it finishes, refresh your GitHub profile.

## Editable files

- `README.md` → main content of your profile
- `profile.json` → text used for the generated SVG assets
- `assets/*.svg` → generated visuals
- `scripts/build_assets.py` → regenerates the SVG assets if you change `profile.json`

## Regenerate assets after editing profile.json

```bash
python scripts/build_assets.py
```
