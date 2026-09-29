# Business Central Object Registry

Master register of Business Central AL apps maintained by AJ Ansari for OnlyBCFans (OBCF), with the object ID range(s) each app declares in its `app.json`.

Repository visibility reflects the GitHub repository metadata retrieved on **September 28, 2026**.

**Type** is `PTE` (Per-Tenant Extension, object IDs 50000–99999) or `AppSource` (object IDs 70000000 and above).

**Repo name** links to the OnlyBCFans repository on GitHub. Links are written as HTML anchors with `target="_blank"` so they open in a new tab wherever the renderer allows it; github.com strips that attribute and opens them in the same tab.

**Overlaps with** lists every other app whose declared range(s) intersect this app's range(s). Computed by `build.py`.

> The webpage reads this file, so a commit here updates the page. To remove or edit an app, edit this file, then update the Free ranges table or run the Update Free Range action. For the sortable view open <a href="index.html" target="_blank" rel="noopener"><code>index.html</code></a>.

## Registry

| App name | App ID | Object range(s) | Type | Overlaps with | Repo name | Visibility | Issued |
|---|---|---:|---|---|---|---|---|

## Notes

- Registry data was cleared. Every data row was removed from the Registry table. The Free ranges table lists 50000–99999, because that whole range is available again. This wipe cannot be reversed from the current files.

## Free ranges (50000–99999)

Gaps between the allocations above, for picking a new range. Computed by `build.py`; re-check before reserving.

| Free range |
|---:|
| 50000–99999 |
