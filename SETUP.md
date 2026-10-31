# EDITABLE PIXEL PROFILE CARD — REVIEW PROJECT

**No GitHub actions have been taken. Do not delete your existing `.git` folder or force-push.** This is a separate preview copy so your recovered commit history stays intact.

## Easiest: live editor (no installation or server)

1. Unzip this package into a **separate folder** (`HiroSaito04-editable-review`).
2. Double-click `editor.html`, or right-click it and choose **Open With → Chrome/Edge**.
3. Change **GitHub username, display name, role, tagline, GitHub caption, accent color**. All update live.
4. Click **Choose File** to replace the avatar with a new transparent PNG/JPG/WebP. The border/frame stays the same.
5. Click **EXPORT SVG FOR GITHUB**. Your downloaded `profile-card.svg` contains the pixel typography, border, background and embedded portrait.
6. If you like the result, put the exported file in your existing repository as `assets/profile-card.svg` (replacing the old file). The README already references that filename.
7. For later edits, reopen `editor.html`, click **REOPEN EXPORTED SVG**, and choose your last exported `profile-card.svg`. Both the text and your embedded portrait return to the editor. You can swap the portrait again and export a new version.
8. Optional: click **SAVE CONFIG JSON** to save the editable text values separately. Use **IMPORT CONFIG** to restore them.

**No `npm install`, Python server, or web access is needed for the browser editor.**

## Alternative: edit source files in VS Code and rebuild

1. Edit `profile.json` (all text fields and theme color).
2. Replace `assets/boy_down.png` with the portrait of your choice, or adjust `"avatar"` in `profile.json` to any PNG/JPG/WebP file within the project.
3. In the project directory run:

```powershell
node scripts/build-card.js
```

Node.js is the only requirement for this method. The script regenerates `assets/profile-card.svg` and refreshes the editor's default configuration. No external fonts, images or packages are downloaded.

## How the design works

- `scripts/card-renderer.js` is the complete **code-based design**. Every shape and every letter of the pixel font is authored as SVG geometry. You can edit the colors, layout, corner shapes, font, forest and frame there.
- `profile.json` holds editable text and image path.
- `assets/boy_down.png` is the default portrait. Keep transparency for best results.
- `assets/profile-card.svg` is the finished card to display on GitHub.
- `editor.html` is the local visual editor and SVG/PNG/config exporter. This is **not** embedded in your GitHub README; GitHub does not run interactive editor scripts inside a README.
- `assets/pathfinder.gif` and `assets/contribution-brio.gif` are retained unchanged; Pathfinder uses Player and Contribution uses Brio.

## Preview only

Open `README.md` in VS Code and press **Ctrl+Shift+V** to check the profile preview. No Git commands are necessary to inspect it. Later, when you approve the update, copy the files into your already cloned repo with its original `.git` folder still present and create a **normal commit/push**.
