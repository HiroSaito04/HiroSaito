# Pixel Pathfinder — Review & Setup

## Review FIRST — no Git commands needed

1. Extract the ZIP into a NEW folder, such as `D:\HiroSaito04-MapStudio-REVIEW`.
2. Double-click **`preview.html`** to see the updated profile, map, and contribution preview.
3. Open **`editor.html`** to change text, accent color, and avatar in the **code-generated SVG** profile card. Export SVG for GitHub.
4. No upload or push has been done.

## Edit the village MAP visually in Tiled

Tiled is a tile-map editor, not a terminal emulator. Download it at https://www.mapeditor.org/ .

1. Open `maps/village.tmx` in the **Tiled** desktop application.
2. Select an existing *tile layer* to repaint grass, roads, water, or other terrain. Use the tilesets panel; they are included in this project with valid relative image paths.
3. Add, move, and delete buildings and props in the existing object layers.
4. In **Layers**, show/select **`Player Route [edit polyline]`**. The object **`Player Walk Path`** is a multi-point polyline. Use Tiled's *Edit Polygons* tool to move, insert, or delete path points. The avatar follows this polyline; its route is not hardcoded in Python.
5. Save with **Ctrl+S**.
6. Open terminal in project root and run:

```powershell
python -m pip install -r requirements.txt
python scripts/render_map.py
```

Your edited route and tiles now appear in `assets/pathfinder.gif`. Open `preview.html` and refresh. Use `assets/village-map-full.png` to inspect the full tilemap.

**Technical note:** This is based on the user's actual `village.tmx` with CSV tile layers and Tiled objects; the missing tileset image references from the supplied ZIP were repaired. Keep `maps/`, `tiles/`, and `tiles&objects/` together. The sprite and route use the same TMX coordinates.

## Brio over the REAL GitHub contribution calendar

The ZIP includes a **public GitHub snapshot for `HiroSaito04`**, covering daily counts through **October 31, 2026** (205 contributions for the preceding year). These daily counts are real, while the archived snapshot’s color intensity bands are approximate. Brio moves through the same GitHub-shaped 53-week calendar, not a made-up 6-row game board.

To download **your actual HiroSaito04 public GitHub contribution levels** and regenerate locally (internet required), double-click `GENERATE_REAL_BRIO.bat` on Windows, or use:

```powershell
python scripts/render_contributions.py --fetch
```

When published to GitHub, `.github/workflows/update-contributions.yml` can update the GIF and cached levels once daily after you manually run it the first time under **Actions**. GitHub Actions may need read/write workflow permissions. Failed fetches do **not** overwrite saved real data.

For a sample-only redraw:

```powershell
python scripts/render_contributions.py --preview
```

## Editable card

- `editor.html`: offline browser editor (text, palette, portrait, export SVG)
- `profile.json`: editable text / palette / image path
- `scripts/card-renderer.js`: code for all pixel typography and vector card art
- `node scripts/build-card.js`: rebuild `assets/profile-card.svg` after changing `profile.json`

## Protect your Git history

This ZIP deliberately **does not contain a `.git` directory**. When you approve the design, copy the changed files into your EXISTING `D:\HiroSaito04` repo folder and use an ordinary commit and push. **Do not run `git init` again and do not force-push.**


## Editable star collectibles

Open `maps/village.tmx` in Tiled and use the object layer named `Collectible Stars [edit positions]`.
Move, delete, or duplicate the star objects to control where the player collects stars during the Pathfinder animation.
Then rerun:

```bash
python scripts/render_map.py
```


## Change Brio walking speed

The updated default is **185 frames × 200 milliseconds** = approximately **37 seconds per loop** (previously about 6.5 seconds). This is roughly 5.7× slower.

Use `--frame-ms` to change timing, and `--frames` to adjust the smoothness:

```powershell
python scripts/render_contributions.py --fetch --frame-ms 260 --frames 185
```

`--fetch` uses your live public GitHub contribution levels; `--preview` uses explicitly labeled sample values for testing motion only. If network fetching fails, it will not overwrite your saved real data. `data/contributions.json` contains the archived snapshot until the first successful live fetch.

**No automatic push from this review ZIP.** The included GitHub Actions workflow only works after you intentionally publish the files.
