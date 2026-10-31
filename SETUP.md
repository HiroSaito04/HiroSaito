# Pixel Quest GitHub Profile — Installation and Update

## Your repository

The profile README appears on your GitHub Overview page only if the public repository is exactly `HiroSaito04`.

- GitHub account: `https://github.com/HiroSaito04`
- Profile repository: `https://github.com/HiroSaito04/HiroSaito04`
- Personal website (source for profile facts): `https://mr-zhiroark-portfolio.vercel.app`

## Update your already-working profile in VS Code

1. Make a backup of any edits you made in the existing repository.
2. Extract this ZIP, then open the contained `HiroSaito04` folder.
3. Copy all of the contents of that folder, including `.github`, into your **existing local repository folder** (the folder containing `.git`). Replace files when prompted. **Do not copy the extracted folder as a nested subfolder.**
4. Open the existing repository folder in VS Code, then run:

```bash
git status
git add -A
git commit -m "Switch GitHub profile to Pixel Quest RPG theme"
git push origin main
```

`git add -A` also stages deletions after you remove any leftover unused files from the previous design.

### Clean up old assets (optional but recommended)

The new README uses only the files in `assets/` listed below. The previous design's unused SVGs and scripts can be deleted from your existing repository after you copy this project in:

- `assets/profile.svg`, `assets/stack.svg`, `assets/focus.svg`, `assets/journey.svg`
- `assets/landscape.svg`, `assets/maze.svg`, `assets/workflow.svg`, `assets/subaru.webp`
- `scripts/build_assets.py`, `scripts/render_profile.py`
- `logo.png`, `subaru.png`, and `reference/architecture-original.md` (if present)

Do not delete `.github/workflows/snake.yml` or the `output` branch.

## Snake workflow

Go to your repository > **Actions** > **Generate Snake Animation** > **Run workflow** to manually regenerate it. Otherwise the workflow runs on pushes to `main` and on a 12-hour schedule.

The workflow writes the SVGs to an `output` branch. The README reads the snake from that branch.

## Edit your details without inventing facts

`profile.json` currently includes only the name and developer title visible in the public page title of your portfolio and the GitHub username used for this repository. The website's detailed sections were not accessible from the provided page fetch, so the package deliberately does not claim any skills, employers, contact addresses, or project names.

When you want to update text, edit `profile.json`, then run:

```bash
python scripts/build_pixel_assets.py
```

No font downloads, npm packages or external graphics libraries are required to regenerate the SVGs. All pixel letters and art are drawn in the Python script.

## Assets

- `assets/hero.svg` — RPG game world + original character sprite + pixel typography
- `assets/character.svg` — standalone original RPG-style developer character
- `assets/save-file.svg` — verified identity in a pixel game save screen
- `assets/quest-board.svg` — navigation quest menu
- `assets/button-portfolio.svg`, `assets/button-github.svg` — pixel link buttons
- `assets/footer.svg` — ending game scene
- `assets/divider.svg` — optional pixel-art separator

GitHub renders SVG assets inside the README; an additional Markdown renderer or web host isn't needed.
