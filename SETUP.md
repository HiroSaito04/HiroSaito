# Setup

This is a complete replacement project for your GitHub profile repository.

## Repository settings

- Repository name: `HiroSaito04`
- Visibility: `Public`

## Push steps

If you delete your current local project, extract this ZIP and open the `HiroSaito04` folder in VS Code, then run:

```bash
git init
git branch -M main
git add .
git commit -m "Set up Pixel Pathfinder profile"
git remote add origin https://github.com/HiroSaito04/HiroSaito04.git
git push -u origin main
```

If the repository already exists remotely and already has content, Git may ask you to pull first. If your remote repo is just your old profile project and you want to replace it completely, you can use:

```bash
git push -u origin main --force
```

Use force push only if you are sure you want to overwrite the repo history.

## Files

- `README.md` → profile README
- `assets/boy_down.png` → your profile sprite
- `assets/hero.png` → top banner
- `assets/save-file.png` → save file section
- `assets/pathfinder.gif` → animated map using player sprites
- `assets/contribution-brio.gif` → contribution section using Brio
- `scripts/build_profile.py` → rebuild generated assets locally
- `source_assets/` → local source sprites and tiles copied into the project
