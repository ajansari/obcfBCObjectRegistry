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
| AL for Functional Consultants HOL | `392ac19f-2ffe-45f8-9eee-e9a4a0efc4f9` | 50010–50012 | PTE | — | <a href="https://github.com/ajansari/ALForFunctionalConsultantsHOL" target="_blank" rel="noopener"><code>ALForFunctionalConsultantsHOL</code></a> | Public | — |
| POPrintRestriction | `a121a71e-63fa-4b5d-923a-3e0215697800` | 50090–50091 | PTE | — | <a href="https://github.com/ajansari/AL-POPrintRestriction" target="_blank" rel="noopener"><code>AL-POPrintRestriction</code></a> | Public | — |
| ALAddNewField | `7da7777d-0bb4-4630-8889-5f89a5bf8df5` | 50100–50149 | PTE | Custom Sales Invoice Report | <a href="https://github.com/ajansari/AL-AddFieldToItemTable" target="_blank" rel="noopener"><code>AL-AddFieldToItemTable</code></a> | Private | — |
| Custom Sales Invoice Report | `87d8b66c-35e7-4a13-a37d-1957342c1ba5` | 50100–50149 | PTE | ALAddNewField | <a href="https://github.com/ajansari/ReportDemoProject1" target="_blank" rel="noopener"><code>ReportDemoProject1</code></a> | Private | — |
| BBB Rating Insights | `9aabe937-d408-4190-b533-1440665a9ed6` | 50601–50620; 50621–50650 | PTE | — | <a href="https://github.com/ajansari/claudeCodeMobileDevTest" target="_blank" rel="noopener"><code>claudeCodeMobileDevTest</code></a> | Public | — |
| TestProject001 - Pending | `—` | 60000–60019 | PTE | — | — | — | 2026-09-29 |
| Sam s Demo Project - Pending | `—` | 60020–60042 | PTE | — | — | — | 2026-09-29 |
| NAICS Classification | `4a23d365-3cd3-4dd0-8d0b-005c3143e0cf` | 60470–60499 | PTE | — | <a href="https://github.com/ajansari/NAICSClassificationApp" target="_blank" rel="noopener"><code>NAICSClassificationApp</code></a> | Public | — |
| Bootcamp Registration Tracking | `f53b57ed-efc7-47dc-b3df-0bf7a34f7708` | 60800–60899 | PTE | — | <a href="https://github.com/ajansari/BootcampRegistrationApp" target="_blank" rel="noopener"><code>BootcampRegistrationApp</code></a> | Public | — |
| Summit 2023 AL Project | `04de3c47-4c0b-4b03-843d-d7332e0f4573` | 70100–70102; 70200–70202 | PTE | — | <a href="https://github.com/ajansari/Summit2023Proj" target="_blank" rel="noopener"><code>Summit2023Proj</code></a> | Private | — |
| SIC Code Classification | `da5e7455-f969-4f2c-8e50-a05aff3284c0` | 77071–77099 | PTE | — | <a href="https://github.com/ajansari/SICCodeClassificationApp" target="_blank" rel="noopener"><code>SICCodeClassificationApp</code></a> | Public | — |
| General Journal Copilot | `d14f792f-90ff-4084-8ba7-edfe4327df4b` | 78700–78799 | PTE | — | <a href="https://github.com/ajansari/GLEntryCopilot" target="_blank" rel="noopener"><code>GLEntryCopilot</code></a> | Private | — |
| DBA Tracker | `00e74a82-47db-4186-ae79-85b3aa726260` | 79990–79999 | PTE | — | <a href="https://github.com/ajansari/DBA" target="_blank" rel="noopener"><code>DBA</code></a> | Public | — |
| BCandSki RC App | `794794a0-40e2-4f32-9aef-2ef4f3ecde0b` | 80000–80149 | PTE | DSWi API Page Example | <a href="https://github.com/ajansari/RoleTailoring" target="_blank" rel="noopener"><code>RoleTailoring</code></a> | Public | — |
| DSWi API Page Example | `6059ae9f-ef71-4af5-9e3c-1c656cf8e3a6` | 80100–80110 | PTE | BCandSki RC App | <a href="https://github.com/ajansari/AL-APIsAndPermissions" target="_blank" rel="noopener"><code>AL-APIsAndPermissions</code></a> | Public | — |
| IP Tracking | `8bf69fdd-4440-48d7-b7b4-7608ac2e9266` | 80300–80339 | PTE | — | <a href="https://github.com/ajansari/intellectualPropertyTracker" target="_blank" rel="noopener"><code>intellectualPropertyTracker</code></a> | Public | — |
| Member & Chapter Manager | `a037882e-070b-47e4-ab4e-f6497d9eb05b` | 80700–80799 | PTE | — | <a href="https://github.com/ajansari/MemberAndChapterManager" target="_blank" rel="noopener"><code>MemberAndChapterManager</code></a> | Public | — |
| SummitNADay1 | `a40b796a-cf2d-4810-9c79-2b94d4ca88e6` | 80890–80899 | PTE | AJ's Copilot | <a href="https://github.com/ajansari/al-instructorworkshopsample" target="_blank" rel="noopener"><code>al-instructorworkshopsample</code></a> | Public | — |
| AJ's Copilot | `30c37d64-2af0-4ff2-b933-608b4bde8ef5` | 80895–80899 | PTE | SummitNADay1 | <a href="https://github.com/ajansari/addyourcopilottobc" target="_blank" rel="noopener"><code>addyourcopilottobc</code></a> | Public | — |
| Metropak Coupa Agent Extension | `4e5def94-9194-4f4d-945c-e7c84b5ef4d7` | 80980–80999 | PTE | — | <a href="https://github.com/ajansari/mpkAmazonBcPte" target="_blank" rel="noopener"><code>mpkAmazonBcPte</code></a> | Private | — |
| OnlyBCFans Support Manager | `12345678-1234-1234-1234-123456789012` | 88800–88899 | PTE | Support Manager | <a href="https://github.com/ajansari/OLD-DNU-alsupportcasemanager" target="_blank" rel="noopener"><code>OLD-DNU-alsupportcasemanager</code></a> | Private | — |
| Support Manager | `12345678-1234-1234-1234-123456789012` | 88800–88899 | PTE | OnlyBCFans Support Manager | <a href="https://github.com/ajansari/OnlyBCFansSupportManager" target="_blank" rel="noopener"><code>OnlyBCFansSupportManager</code></a> | Private | — |
| Business Central API Collection | `06a0b195-0da7-49be-9f55-63fedf76fa1a` | 90500–90599 | PTE | — | <a href="https://github.com/ajansari/OLD-DNU-al-OnlyBCFans-apiMiniLibrary" target="_blank" rel="noopener"><code>OLD-DNU-al-OnlyBCFans-apiMiniLibrary</code></a> | Private | — |
| OBCF APIs v3 | `855299b2-5650-41ce-80c1-b130b89af4b4` | 90800–91099 | PTE | — | <a href="https://github.com/ajansari/obcfBCAPIsV3" target="_blank" rel="noopener"><code>obcfBCAPIsV3</code></a> | Public | — |

## Notes

- Every app currently registered declares ranges within 50000–99999, so all are typed `PTE`. No app has an AppSource range (70000000+) yet.
- `50100–50149` is declared by both `ALAddNewField` and `Custom Sales Invoice Report`.
- `80100–80110` overlaps with the broader `80000–80149` range declared by `BCandSki RC App`.
- `80895–80899` is contained within `80890–80899`.
- Both Support Manager repositories use the same placeholder app ID: `12345678-1234-1234-1234-123456789012`.
- Repos prefixed `OLD-DNU-` are retired (do not use). Their rows are kept so the ranges remain visible as historically allocated.
- The ranges are manifest allocations. They do not by themselves prove that every ID in each range is currently used or that the app is installed in a Business Central tenant.

## Free ranges (50000–99999)

Gaps between the allocations above, for picking a new range. Computed by `build.py`; re-check before reserving.

| Free range |
|---:|
| 50000–50009 |
| 50013–50089 |
| 50092–50099 |
| 50150–50600 |
| 50651–59999 |
| 60043–60469 |
| 60500–60799 |
| 60900–70099 |
| 70103–70199 |
| 70203–77070 |
| 77100–78699 |
| 78800–79989 |
| 80150–80299 |
| 80340–80699 |
| 80800–80889 |
| 80900–80979 |
| 81000–88799 |
| 88900–90499 |
| 90600–90799 |
| 91100–99999 |
