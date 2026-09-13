# RACI: New Vendor Catalog Onboarding

R = Responsible · A = Accountable · C = Consulted · I = Informed

| Activity | PM (Intern) | Cataloging Ops | Pricing Ops | Procurement | Engineering | Vendor |
|---|---|---|---|---|---|---|
| Kickoff & timeline communication | A/R | I | I | C | — | I |
| Bulk catalog submission | I | A | — | — | — | R |
| Automated QC run | I | R | — | — | A (tooling owner) | — |
| Manual QC resolution | C | A/R | — | — | — | C |
| Pricing sanity check | I | I | A/R | — | — | — |
| Staging spot-check | R | A | C | — | — | — |
| Go-live approval | A/R | C | C | I | — | I |
| Post-launch findability check | A/R | C | — | — | C | — |
| SLA breach escalation | A/R | I | I | I | — | I |

## Why this matters for the role
The JD's Program Management stream calls out "coordinate across
Engineering, Design and QA, track timelines and blockers." A RACI is a
lightweight tool that makes escalation unambiguous — when Step 4 (Pricing
sanity check) slips, it's immediately clear who's accountable (Pricing Ops)
and who owns raising it (PM), instead of a vague "someone should look into
this."

## Common failure mode this prevents
Without a RACI, "go-live approval" tends to informally default to
whoever's most senior in the room, which slows decisions down. Naming the
PM as accountable for go-live (with Cataloging Ops consulted, not blocking)
keeps the process moving while still requiring sign-off from the team that
owns data quality.
