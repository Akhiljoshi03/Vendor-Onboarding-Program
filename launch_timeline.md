# Launch Timeline: Batch Onboarding of 12 New Vendors (Festive Season Prep)

**Context:** Ahead of a major sale event, 12 new apparel vendors need to be
onboarded in parallel rather than one at a time, without breaking the SLA
defined in `SOP_vendor_onboarding.md`. This is the Program Management
artifact — tracking a multi-workstream launch with real dependencies and
blockers, not just a single vendor's happy path.

## Timeline (10 business days, Days 1–10)

```
Day:        1    2    3    4    5    6    7    8    9    10
Vendor      |----submission window (5d)----|
submission

Automated             |--QC--|
QC (per                (same day
vendor,                 as submission,
staggered)               staggered by
                          submission day)

Manual QC                   |----review (2d)----|
resolution

Pricing                            |--review (1d)--|
sign-off

Staging                                  |--spot check (1d)--|
push +
check

Go-live                                        |-------GO-LIVE WINDOW-------|
                                                  (staggered, not all at once)
```

## Key Program Management Decisions

1. **Staggered submission, not a single deadline.** All 12 vendors given
   the same Day-5 deadline creates a Day-6 bottleneck at Cataloging Ops (12
   catalogs to QC at once). Instead, submission slots are assigned across
   Days 1–5 so QC load is spread evenly — a scheduling choice that protects
   the downstream SLA.

2. **Go-live is staggered, not simultaneous**, for two reasons:
   - Limits blast radius if a post-launch findability issue appears — a
     problem in one vendor's catalog doesn't get missed in a wall of 12
     simultaneous launches.
   - Matches the sale event's own phased category launches, so vendor
     go-live aligns with when their category actually needs to be live.

3. **Explicit blocker log**, updated daily, rather than relying on status
   meetings:

| Vendor | Current step | Status | Blocker (if any) | Owner to unblock |
|---|---|---|---|---|
| Vendor A | Manual QC | On track | — | — |
| Vendor B | Pricing sign-off | **At risk** | Pricing Ops backlog from 3 other launches | Escalated to Pricing Ops lead (Day 6) |
| Vendor C | Staging | On track | — | — |
| ... | ... | ... | ... | ... |

This table is the actual day-to-day artifact a PM keeps live during a
multi-vendor launch — not a static Gantt chart nobody updates, but a
working blocker log tied to the RACI so escalation ownership is never
ambiguous.

## Stakeholder Communication Cadence
- **Daily async update** (Slack, 5 lines): vendors on track / at risk /
  blocked, any escalations raised.
- **Day 5 checkpoint:** all submissions in — go/no-go read on whether the
  Day-10 target is still realistic; if not, decide now which vendors slip
  to the next batch rather than compressing QC quality under deadline
  pressure.
- **Post-launch retro (Day 12):** which step caused the most delay across
  the 12 vendors, feeding back into the SOP's change log.
