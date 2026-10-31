# Pixel Pathfinder — Review copy

**This package has not been pushed to GitHub.** It is for your approval first.

## Check locally in VS Code

1. Extract the ZIP into a separate folder, such as `HiroSaito04-review`.
2. Open that folder in VS Code.
3. Open `README.md`, then press `Ctrl+Shift+V` for Markdown Preview.
4. Open `assets/profile-card.png` to inspect the redesigned card at full size.
5. Open `assets/pathfinder.gif` and `assets/contribution-brio.gif` to inspect the animations.

## Changed design

- New pixel-font `assets/profile-card.png` matches the provided dark-neon-green reference.
- The card uses the exact `boy_down.png` avatar.
- The Pathfinder uses the supplied `player1.png` ... `player12.png` frames.
- The single Contribution section uses `brio1.png` ... `brio12.png` frames.
- All generated visual labels now use pixelated bitmap lettering.
- The animated contribution grid is decorative; it is not a real GitHub activity count.

## Regeneration

The project includes the source scripts and sprites:

```bash
python scripts/render_card.py
python scripts/build_profile.py
```

These scripts require Python and Pillow (`python -m pip install pillow`).

## IMPORTANT: preserve your old Git history

Do not delete the `.git` folder from your existing repo. Do not run `git init` or `git push --force` to update this project. After you approve the preview, copy the new files into your *existing tracked folder*, and make a normal commit/push. For now, no push is needed.
