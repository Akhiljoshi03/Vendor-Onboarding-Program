# Vendor Onboarding Program

An SOP-driven system for onboarding new apparel vendors' product catalogs
into an e-commerce storefront — from signed vendor agreement to live SKUs
— with a Python engine that automates SLA tracking, catalog QA, and
stakeholder reporting across a multi-vendor pipeline.

## The problem

Onboarding a vendor's catalog isn't one step, it's five (submission → QC →
manual review → pricing sign-off → go-live), each with a different owner
and a different SLA. Run this for one vendor and it's manageable by memory.
Run it for twelve vendors in parallel — as happens ahead of a sale event —
and without a system, work silently stalls: a vendor sits stuck in
"metadata enrichment" for a week and nobody notices until launch day.

This project defines the process, assigns clear ownership per stage, and
then automates the tracking so blockers surface on their own instead of
depending on someone remembering to check.

## What's in this repo

| File | What it is |
|---|---|
| `SOP_vendor_onboarding.md` | The standard 7-step process: owner, SLA, and exit criteria for each step |
| `RACI_matrix.md` | Who's Responsible / Accountable / Consulted / Informed at each step |
| `launch_timeline.md` | Scaling the SOP to 12 vendors onboarding in parallel, with a blocker log |
| `stakeholder_comms_plan.md` | How progress gets communicated to 6 different stakeholder groups |
| `engine/vendor_onboarding_engine.py` | Python engine that runs the SOP's rules programmatically |

## How the engine works

The engine encodes the SOP as data and rules rather than a document nobody
reads:

- **`OnboardingStage`** — the 5 pipeline stages, matching the SOP
- **`SLA_THRESHOLDS`** — how many days each stage is allowed to take
- **`OWNERSHIP_MAP`** — which team owns each stage, matching the RACI
- **`Vendor` / `CatalogItem`** — a vendor and its SKU catalog, each item
  checked against mandatory fields (images, fabric composition)
- **`VendorOnboardingEngine.evaluate_slas()`** — flags a vendor `AT_RISK`
  or `BLOCKED` based on how long they've sat in their current stage vs.
  the SLA
- **`run_catalog_qa_gate()`** — the automated QC gate: if more than 5% of
  a vendor's SKUs fail validation, the vendor is blocked and bounced back
  rather than allowed to proceed with bad data
- **`generate_stakeholder_report()`** — produces the weekly status update:
  vendor counts by stage, and a called-out list of blocked vendors with
  owner and reason, so escalation is unambiguous

## Run it

```bash
cd engine
python3 vendor_onboarding_engine.py
```

Sample output (simulating 12 vendors mid-pipeline, with some SLA breaches
injected for demonstration):

```
==================================================
VENDOR ONBOARDING: WEEKLY STAKEHOLDER UPDATE
==================================================
Total Vendors in Pipeline: 12
Successfully Live: 1
Blocked: 4 | At Risk: 3

--- ACTION REQUIRED (BLOCKED) ---
[!] UrbanStyle | Owner: AI Cataloging System | Time in Stage: 10 days
    Reason: SLA Breach: Stuck in Metadata Enrichment for 10 days.
[!] DenimPro | Owner: Data Ops Team | Time in Stage: 10 days
    Reason: SLA Breach: Stuck in Raw Data Ingestion for 10 days.
...

--- PIPELINE DISTRIBUTION ---
 - Vendor Initiated: 3 vendors
 - Raw Data Ingestion: 4 vendors
 - Metadata Enrichment: 3 vendors
 - Quality Assurance: 1 vendors
 - Live on Storefront: 1 vendors
==================================================
```

The "owner" on each blocked vendor comes straight from the RACI — the
report tells you not just *what's* stuck, but *whose desk it's on*.

## Design decisions worth noting

- **QA is a gate, not a warning.** A vendor above the 5% error-rate
  threshold is blocked automatically rather than allowed through with a
  flag — bad catalog data reaching the storefront is worse than a delayed
  launch.
- **SLA breach has two levels.** `AT_RISK` (over SLA) and `BLOCKED` (over
  SLA + 2-day grace period) — this distinguishes "worth watching" from
  "needs escalation now," so the report doesn't cry wolf on every minor
  delay.
- **The report is generated, not written.** Stakeholder updates are a
  known failure point in fast processes — they get stale or skipped. Here
  the update is a byproduct of the same data the engine uses to run the
  pipeline, so it can't drift out of sync with reality.

## Extending this

This is a simulation (`simulate_pipeline()` generates mock vendors and
catalogs) rather than connected to a real database or vendor-facing
upload tool. The natural next steps would be: swap the mock catalog
generator for a real bulk-upload parser, persist vendor state instead of
re-simulating it each run, and post `generate_stakeholder_report()`
straight to Slack on a schedule.
