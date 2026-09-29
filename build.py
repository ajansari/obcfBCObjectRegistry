#!/usr/bin/env python3
"""Render ObjectRegistry.md from registry.json.

Usage:  python3 build.py
Edit registry.json, run this, commit both files.
index.html is static and reads ObjectRegistry.md at runtime.
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent
data = json.loads((ROOT / "registry.json").read_text(encoding="utf-8"))
apps = data["apps"]
PTE_LOW, PTE_HIGH = 50000, 99999


def repo_url(app):
    """GitHub URL for the app's OnlyCopilotFans repo. githubOwner is the account path in the URL; an app may set "owner" to override it."""
    return f"https://github.com/{app.get('owner', data['githubOwner'])}/{app['repo']}"


def has_repo(app):
    repo = (app.get("repo") or "").strip()
    return bool(repo) and repo != "—"


def repo_cell(app):
    if not has_repo(app):
        return "—"
    return f'<a href="{repo_url(app)}" target="_blank" rel="noopener"><code>{app["repo"]}</code></a>'


def fmt_ranges(ranges):
    return "; ".join(f"{a}–{b}" for a, b in ranges)


def free_ranges():
    used = sorted((a, b) for app in apps for a, b in app["ranges"] if b >= PTE_LOW and a <= PTE_HIGH)
    free, cursor = [], PTE_LOW
    for a, b in used:
        if a > cursor:
            free.append((cursor, a - 1))
        cursor = max(cursor, b + 1)
    if cursor <= PTE_HIGH:
        free.append((cursor, PTE_HIGH))
    return free


def overlaps(app):
    """Names of other apps whose ranges intersect this app's ranges."""
    hits = []
    for other in apps:
        if other is app:
            continue
        if any(a <= d and c <= b for a, b in app["ranges"] for c, d in other["ranges"]):
            hits.append(other["name"])
    return hits


# ---------- Markdown ----------
md = [
    "# Business Central Object Registry",
    "",
    "Master register of Business Central AL apps maintained by AJ Ansari for OnlyCopilotFans (OCPF), "
    "with the object ID range(s) each app declares in its `app.json`.",
    "",
    f"Repository visibility reflects the GitHub repository metadata retrieved on **{data['asOf']}**.",
    "",
    "**Type** is `PTE` (Per-Tenant Extension, object IDs 50000–99999) or `AppSource` (object IDs 70000000 and above).",
    "",
    "**Repo name** links to the OnlyCopilotFans repository on GitHub. Links are written as HTML anchors with `target=\"_blank\"` so "
    "they open in a new tab wherever the renderer allows it; github.com strips that attribute and opens them in the same tab.",
    "",
    "**Overlaps with** lists every other app whose declared range(s) intersect this app's range(s). Computed by `build.py`.",
    "",
    '> Generated from <a href="registry.json" target="_blank" rel="noopener"><code>registry.json</code></a> by `build.py`. '
    'Edit the JSON, not this file. For a sortable, filterable view open '
    '<a href="index.html" target="_blank" rel="noopener"><code>index.html</code></a>.',
    "",
    "## Registry",
    "",
    "| App name | App ID | Object range(s) | Type | Overlaps with | Repo name | Visibility | Issued |",
    "|---|---|---:|---|---|---|---|---|",
]
for app in sorted(apps, key=lambda x: x["ranges"][0][0]):
    md.append(
        f"| {app['name']} | `{app['appId']}` | {fmt_ranges(app['ranges'])} | {app['type']} | "
        f"{'; '.join(overlaps(app)) or '—'} | {repo_cell(app)} | {app['visibility']} | {app.get('issued') or '—'} |"
    )
md += ["", "## Notes", ""]
md += [f"- {n}" for n in data["notes"]]
md += [
    "",
    "## Free ranges (50000–99999)",
    "",
    "Gaps between the allocations above, for picking a new range. Computed by `build.py`; re-check before reserving.",
    "",
    "| Free range |",
    "|---:|",
]
md += [f"| {a}–{b} |" for a, b in free_ranges()]
(ROOT / "ObjectRegistry.md").write_text("\n".join(md) + "\n", encoding="utf-8")
print(f"Rendered {len(apps)} apps → ObjectRegistry.md")
