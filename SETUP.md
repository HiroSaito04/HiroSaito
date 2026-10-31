# HiroSaito04 GitHub profile — complete VS Code setup

This package combines the Ryo2702 pixel-terminal profile artwork, sections,
animations and generator with the MD Abu Kayser **Contribution Activity snake only**.
The username and snake URLs are preconfigured for **HiroSaito04**.

## Step 1 — Create the special repository

1. Open https://github.com/new and sign in as **HiroSaito04**.
2. **Repository name:** `HiroSaito04` (must match your GitHub username).
3. **Visibility:** Public.
4. Leave **Add a README**, **.gitignore**, and **license** unchecked, because these
   files will come from the ZIP. (No existing commit makes pushing easiest.)
5. Click **Create repository**. Leave the resulting GitHub page open.

Do **not** create a `mike-dev` repository for the special profile README.
It can exist as a separate project, but it will not appear automatically on your profile.

## Step 2 — Extract and open the project in VS Code

1. Extract `HiroSaito04.zip` to a folder named `HiroSaito04`.
2. Open VS Code > **File > Open Folder** > select that extracted `HiroSaito04` folder.
3. Check that `README.md`, `profile.json`, `assets/`, and `.github/` are directly inside
   the opened folder (not hidden in a second nested directory).
4. Open **Terminal > New Terminal**. All commands below are run **from that folder**.

## Step 3 — Push using the VS Code terminal (PowerShell or Bash)

Check that Git is installed, then copy these commands **one by one**:

```powershell
git --version
git init
git branch -M main
git add .
git commit -m "Create GitHub profile README and contribution snake"
git remote add origin https://github.com/HiroSaito04/HiroSaito04.git
git push -u origin main
```

If `git commit` says **Author identity unknown**, configure your own Git commit
identity and retry the commit (use your actual preferred name and GitHub account email
or GitHub no-reply address):

```powershell
git config --global user.name "YOUR NAME"
git config --global user.email "YOUR GITHUB EMAIL"
git commit -m "Create GitHub profile README and contribution snake"
git push -u origin main
```

If `error: remote origin already exists` appears, run:

```powershell
git remote set-url origin https://github.com/HiroSaito04/HiroSaito04.git
git push -u origin main
```

When Git asks you to authenticate, complete the GitHub sign-in in your browser.
Do not paste your GitHub password directly into terminal commands.

**If you already created the GitHub repository WITH a README**, your push could be
rejected because the remote has a separate first commit. Safest approach: clone the
existing GitHub repository into a NEW empty folder, then copy the extracted project
files (including `.github`) into that cloned folder, replacing its `README.md`. Run
`git add .`, `git commit -m "Add custom profile and snake"`, and `git push` from the
cloned folder. Do not force-push over your existing work.

## Step 4 — Make the snake appear

1. Open https://github.com/HiroSaito04/HiroSaito04/actions
2. If GitHub asks to enable Actions, enable them for this repository.
3. Select **Generate Snake Animation** in the left-hand list.
4. Select **Run workflow**, choose `main`, and confirm **Run workflow**.
   The first push to `main` may already have started a run automatically.
5. After the run completes successfully, an `output` branch will contain the SVG/GIF files.
6. Refresh https://github.com/HiroSaito04 (the **Overview** tab, not **Stars**).

The animation is generated from **HiroSaito04's** public contribution history and
refreshes automatically every 12 hours. Your main branch is not overwritten.

If the workflow fails with `403`/`Resource not accessible by integration`, open
**Repository Settings > Actions > General** and check Actions permissions and that
workflows can write the repository contents. The YAML itself requests
`permissions: contents: write`. Organization-level policies may also apply.

## Step 5 — Customize the content

- `README.md` — visible text and section layout. The title `MIKE` can be edited here.
- `profile.json` — change the display name, role and tagline for the large graphic.
- `assets/subaru.webp` — original illustrative character art from the source template.
- To update the profile art after editing `profile.json`, run:

```powershell
python scripts/render_profile.py
```

If `python` is unavailable on Windows, try `py scripts/render_profile.py`.
This SVG generator requires Python 3 and no additional packages.

Then push your edits:

```powershell
git add .
git commit -m "Update GitHub profile"
git push
```

## File layout

```
HiroSaito04/
├── .github/workflows/snake.yml  # automatic snake workflow
├── assets/                      # profile and animations
├── scripts/render_profile.py   # editable SVG generator
├── README.md                   # shown on the GitHub profile
├── profile.json                # editable hero values
├── SETUP.md                    # this guide
├── CREDITS.md                  # attribution and source notes
├── reference/                  # additional reference from Ryo
├── logo.png                    # retained source asset
└── subaru.png                  # retained source asset
```

**Attribution:** The Ryo source archive contains no license. Before publicly
redistributing the included original character imagery/artwork, verify the
creator's permission or replace it with artwork you have rights to use.
