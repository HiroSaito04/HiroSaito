# Contribution data provenance and refresh

`data/contributions.json` contains an archived daily-count snapshot derived from the public GitHub contributions calendar at:

- https://github.com/users/HiroSaito04/contributions
- Username: `HiroSaito04`
- Snapshot includes Sunday, October 26, 2025 through Saturday, October 31, 2026
- Total observed over that captured year: **205 public contributions**
- Recorded at the start of November 2026; this snapshot is **not live**

The daily **counts** in this snapshot match the publicly indexed activity calendar. The saved 0–4 **color levels are estimated from those counts**, not extracted directly from GitHub’s HTML. The next live fetch replaces them with exact GitHub-provided `data-level` values.

## Get your current exact GitHub levels

On Windows, double-click `GENERATE_REAL_BRIO.bat` (Python and internet access required), or run:

```powershell
python -m pip install -r requirements.txt
python scripts/render_contributions.py --fetch
```

The command retrieves the entire public calendar, writes it to `data/contributions.json`, and regenerates `assets/contribution-brio.gif`. When you publish the project intentionally, the included GitHub Actions workflow refreshes the GIF daily.

No files are pushed automatically by this local review project.
