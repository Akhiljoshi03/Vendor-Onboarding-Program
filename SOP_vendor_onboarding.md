# SOP: New Vendor Catalog Onboarding
**Focus area:** Supply Chain — Inbound (Procurement, Cataloging, Pricing & Promotions)
**Work stream:** Product Operations
**Owner:** PM Intern (Inbound Supply Chain) · **Last updated:** [date]

## Purpose
Standardize how a new apparel vendor's product catalog moves from signed
vendor agreement to live-on-site, so the process doesn't depend on tribal
knowledge, and so any team member (or new intern) can run it consistently.

## Trigger
A new vendor agreement is signed by Procurement and the vendor is marked
"Ready for Onboarding" in the vendor management system.

## Process

| # | Step | Owner | SLA | Exit criteria |
|---|---|---|---|---|
| 1 | Vendor submits product catalog (images, sizes, MRP, category tags) via bulk upload template | Vendor + Cataloging Ops | 5 business days from kickoff | Template received, row count matches agreed SKU count |
| 2 | Automated QC: image resolution, mandatory field completeness, category-tag validity | Cataloging tooling (automated) | Same day as submission | QC report generated, <2% error rate |
| 3 | Manual review of flagged rows (failed QC) | Cataloging Ops | 2 business days | All flagged rows resolved or rejected with reason |
| 4 | Pricing & Promotions review: MRP sanity check vs. category benchmarks | Pricing Ops | 1 business day | Pricing sign-off logged |
| 5 | Catalog pushed to staging; sample of 20 SKUs spot-checked on staging site | Cataloging Ops + PM | 1 business day | Spot-check checklist 100% passed |
| 6 | Go-live: catalog pushed to production, vendor notified | Cataloging Ops | Same day | SKUs visible and purchasable on site |
| 7 | Post-launch check: search visibility, category placement correctness | PM | Day 1 and Day 7 post-launch | No "0 findable" SKUs; category placement matches taxonomy |

**Total target cycle time: 10 business days**, kickoff to live.

## Exception Handling
- **QC error rate >2%:** loop back to vendor with a specific error report
  (not a generic rejection) — include row numbers and field names so the
  vendor can fix and resubmit without a full re-upload.
- **Pricing sign-off delayed >1 day:** auto-escalate to Pricing Ops lead;
  this is the most common bottleneck historically and shouldn't silently
  slip the whole timeline.
- **Vendor misses Day-5 submission deadline:** PM sends a check-in; if no
  response in 3 more days, vendor onboarding is paused and Procurement is
  notified (avoids catalog slots sitting half-finished indefinitely).

## Roles Reference
- **Cataloging Ops:** owns data quality and the catalog pipeline
- **Pricing Ops:** owns MRP/promotion sanity checks
- **PM (this role):** owns end-to-end SLA tracking, exception escalation,
  and is the single point of contact for the vendor during onboarding

## Change Log
| Version | Change | Reason |
|---|---|---|
| v1.0 | Initial SOP | Baseline process definition |

*(In a live setting this SOP would evolve based on observed bottlenecks —
e.g., if Step 4 consistently slips, that's a signal to add capacity or
automate more of the pricing sanity check.)*
