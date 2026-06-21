# Sprint 1 — Planning

**Goal:** clean, documented, reproducible dataset + Executive Overview v1.

## Scope and rationale
| Story | Pts | Why this sprint |
|---|---|---|
| US-01 — ingest accepted (governed fields) | 5 | Foundation; everything reads from here |
| US-02 — standardize rejected | 5 | Needed for the approval funnel |
| US-03 — cleaning + derived fields | 5 | Trustworthy, reproducible numbers |
| US-04 — single reproducible script (seed) | 3 | One rebuildable pipeline |
| US-05 — data-quality report | 3 | Make known issues visible |
| US-06 — governed KPI dictionary | 2 | Stop definitions drifting |
| US-11 — Executive Overview v1 | 5 | Early tangible value for the sponsor |
| **Total** | **28** | |

## Risks
- The accepted file is ~2.26M rows and the rejected file ~27.6M — memory and load time; mitigated by
  chunked reads and a stratified sample for the dashboard.
- Mixed-dtype columns on load (DtypeWarning) — mitigated with explicit handling (`low_memory=False`).
- The charge-off denominator must be settled before US-06, or KPI numbers diverge — resolved as
  resolved-loans only (per MoM-01).
