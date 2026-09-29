# OCPF Business Central Object Register

A master registry of Microsoft Dynamics 365 Business Central AL extensions and the object ID ranges each one declares. Its purpose is to make it easy to see, in one place, which object ranges are already allocated across every app so that new projects can pick a free range and avoid collisions.

Maintained by **AJ Ansari** for **OnlyCopilotFans (OCPF)**.

## What is in this repo

| File | Purpose |
|---|---|
| [README.md](README.md) | This overview. |
| [registry.json](registry.json) | **Source of truth.** One entry per app with its App ID, declared object range(s), type (PTE or AppSource), source repo, and repo visibility. All repos are OnlyCopilotFans repos; the top-level `githubOwner` is only the account path used to build the GitHub links. Edit this file. |
| [ObjectRegistry.md](ObjectRegistry.md) | Generated Markdown view of the registry, readable directly on GitHub. Includes a computed "Overlaps with" column, notes, and a list of free ranges. |
| [index.html](index.html) | Static interactive view. It reads `ObjectRegistry.md` at runtime, so it has no data of its own. Click column headers to sort; filter by text, type, visibility, overlap status, or hide retired repos. |
| [build.py](build.py) | Renders `ObjectRegistry.md` from `registry.json`. Needs only Python 3, no packages. |
| [.github/workflows/allocate-object-range.yml](.github/workflows/allocate-object-range.yml) | Manual GitHub Action that reserves the next free contiguous object range for a new project. |

GitHub-flavored Markdown cannot sort or filter tables, which is why the interactive view is a separate HTML file.

### Opening the interactive view

Browsers block a page opened from disk (`file://`) from reading other local files, so `index.html` needs to be served over HTTP:

```sh
python3 -m http.server 8000
# then open http://localhost:8000/
```

If you open `index.html` directly instead, it shows a file picker so you can load `ObjectRegistry.md` by hand.

## Reserve a range for a new project

Use the **Allocate object range** workflow when you know how many object IDs the next app needs but do not have a repo yet:

1. Open the repository **Actions** tab, choose **Allocate object range**, and run it from `main`.
2. Enter the range size (for example `10`, `20`, or `50`) and a placeholder project name.
3. The workflow reads `ObjectRegistry.md` on `main`, takes the first contiguous free block of that size between **60000** and **99999**, and writes the assigned range (for example `60000-60009`) to the job summary.
4. It appends a registry row named `{project} - Pending` with that range and the UTC issue date, then commits the change to `main`.

## How the registry is used

1. **Before starting a new app**, run **Allocate object range** (or check the free-range list and add an entry to `registry.json`).
2. **When an app's manifest changes** (new range added, range widened, app renamed or retired), update its entry the same day.
3. **When a repo is archived or renamed**, keep the entry but update the repo name and prefix it `OLD-DNU-` so the range stays visible as historically allocated.
4. **After any edit**, regenerate and commit both files:

   ```sh
   python3 build.py
   git add registry.json ObjectRegistry.md
   git commit -m "Register <app name>"
   ```

## Conventions

- Object ranges are taken from each app's `app.json` `idRanges` and are recorded as inclusive `from–to` pairs. Multiple ranges for one app are separated by semicolons.
- The **Type** column records `PTE` for Per-Tenant Extensions (object IDs 50000–99999) and `AppSource` for apps in the AppSource range (70000000+).
- The **Visibility** column reflects the GitHub repository metadata on the date shown at the top of the registry.
- A range in the registry is a manifest allocation. It does not prove every ID in the range is in use, or that the app is installed in any Business Central tenant.
- Overlaps and shared placeholder App IDs are called out in the registry's Notes section rather than silently resolved.

## Related

- [AJ Ansari - OnlyCopilotFans](https://github.com/ajansari) on GitHub
- OCPF AL Development Standards Guide (object ID allocation rules)
