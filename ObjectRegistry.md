# Business Central Object Registry

Master register of Business Central AL apps maintained by AJ Ansari for OnlyBCFans (OBCF), with the object ID range(s) each app declares in its `app.json`.

Repository visibility reflects the GitHub repository metadata retrieved on **September 29, 2026**.

**Type** is `PTE` (Per-Tenant Extension, object IDs 50000–99999) or `AppSource` (object IDs 70000000 and above).

**Repo name** links to the OnlyBCFans repository on GitHub. Links are written as HTML anchors with `target="_blank"` so they open in a new tab wherever the renderer allows it; github.com strips that attribute and opens them in the same tab.

**Overlaps with** lists every other app whose declared range(s) intersect this app's range(s). Computed by `build.py`.

> The webpage reads this file, so a commit here updates the page. To remove or edit an app, edit this file, then update the Free ranges table or run the Update Free Range action. For the sortable view open <a href="index.html" target="_blank" rel="noopener"><code>index.html</code></a>.

## Registry

| App name | App ID | Object range(s) | Type | Overlaps with | Repo name | Visibility | Issued |
|---|---|---:|---|---|---|---|---|
| XYZ Super Duper App - Pending | `—` | 50000–50022 | PTE | — | — | — | 2026-10-02 |
| Kurt s Awesome BC Project - Pending | `—` | 50023–50045 | PTE | — | — | — | 2026-10-05 |
| Demo Warehouse Labels | `d1000001-0000-4000-8000-000000000001` | 50100–50119 | PTE | — | <code>demo-warehouse-labels</code> | Public | 2026-09-29 |
| Demo Customer Portal | `d1000002-0000-4000-8000-000000000002` | 50200–50249 | PTE | — | <code>demo-customer-portal</code> | Private | 2026-09-29 |
| Demo Sales Pricing | `d1000003-0000-4000-8000-000000000003` | 51000–51029 | PTE | Demo Price Exceptions | <code>demo-sales-pricing</code> | Public | 2026-09-29 |
| Demo Price Exceptions | `d1000004-0000-4000-8000-000000000004` | 51020–51039 | PTE | Demo Sales Pricing | <code>demo-price-exceptions</code> | Private | 2026-09-29 |
| Demo Vendor Approvals | `d1000005-0000-4000-8000-000000000005` | 52000–52009 | PTE | — | <code>demo-vendor-approvals</code> | Public | — |
| Demo Lot Tracking | `d1000006-0000-4000-8000-000000000006` | 53000–53049; 53060–53099 | PTE | — | <code>demo-lot-tracking</code> | Private | 2026-09-29 |
| Demo Shop Floor | `d1000007-0000-4000-8000-000000000007` | 54000–54049 | PTE | — | — | — | — |
| Demo Expense Entry | `d1000008-0000-4000-8000-000000000008` | 55000–55019 | PTE | — | <code>demo-expense-entry</code> | Public | 2026-09-29 |
| Demo Service Dispatch | `d1000009-0000-4000-8000-000000000009` | 56000–56039 | PTE | — | <code>demo-service-dispatch</code> | Private | — |
| Demo Rebate Accrual | `d1000010-0000-4000-8000-000000000010` | 57000–57014 | PTE | — | <code>demo-rebate-accrual</code> | Public | 2026-09-29 |
| Demo Bank Rec Helper | `d1000011-0000-4000-8000-000000000011` | 58000–58009 | PTE | — | — | — | — |
| Demo Intercompany Posting | `d1000012-0000-4000-8000-000000000012` | 60000–60049 | PTE | — | <code>demo-intercompany-posting</code> | Private | 2026-09-29 |
| Demo AppSource Payments | `d1000013-0000-4000-8000-000000000013` | 70000000–70000049 | AppSource | — | <code>demo-appsource-payments</code> | Public | 2026-09-29 |
| Demo AppSource Tax Connector | `d1000014-0000-4000-8000-000000000014` | 70100000–70100019 | AppSource | — | <code>demo-appsource-tax</code> | Public | — |
| Demo AppSource EDI | `d1000015-0000-4000-8000-000000000015` | 70200000–70200099 | AppSource | — | <code>demo-appsource-edi</code> | Private | 2026-09-29 |

## Notes

- These 15 rows are demo data so you can try the registry, the webpage, and the Actions. Replace them with your own apps.
- Demo Sales Pricing and Demo Price Exceptions overlap on 51020–51029 on purpose.
- Demo Lot Tracking has two ranges, with 53050–53059 left free between them.
- AppSource ranges start at 70000000, so they do not change the Free ranges table.

## Free ranges (50000–99999)

Gaps between the allocations above, for picking a new range. Computed by `build.py`; re-check before reserving.

| Free range |
|---:|
| 50046–50099 |
| 50120–50199 |
| 50250–50999 |
| 51040–51999 |
| 52010–52999 |
| 53050–53059 |
| 53100–53999 |
| 54050–54999 |
| 55020–55999 |
| 56040–56999 |
| 57015–57999 |
| 58010–59999 |
| 60050–99999 |
