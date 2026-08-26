# Change Request Log

> Scenario is hypothetical; all data is real LendingClub public data (2007–2018).

## CR-001 — State-level concentration view

| Field | Detail |
|---|---|
| **Raised by** | Compliance Officer |
| **Date** | Mid-Sprint 2 |
| **Status** | Approved (absorbed) |

**Request:** Add a state-level concentration view to the dashboard for regulatory reporting.

**Business justification:** Geographic concentration is a standing board and regulator question,
currently answered manually. A visible state-level view of approval rate and funded volume closes an
audit gap (Compliance is Consulted on the dashboard release per the RACI).

**Impact analysis:**
- New business requirement **BR-11** (geographic concentration reporting) → new functional requirement
  **FR-021** (state-level concentration map).
- New story **US-16** (5 pts), mapped to **VEL-19**.
- Sprint 2 scope would rise from 27 to **32 pts** against a Sprint 1 velocity of 28 — not sustainable
  as committed.
- Dashboard layout change on **Tab 2 (Funnel & Policy)** to add the state map.
- Data: requires the `state_summary` aggregate (state, applications, accepted, approval_rate,
  funded_amnt) from the pipeline.

**Options considered:**
- (a) **Reject** — leaves the audit gap open.
- (b) **Defer** US-16 to a future sprint / the backlog.
- (c) **Absorb** US-16 now by deferring the lowest-priority in-sprint story.

**Decision (Sponsor + BA):** Option (c). Absorb US-16; defer **US-09** ("each rule's threshold backed
by evidence", a Could, 3 pts) to the backlog. Revised Sprint 2 delivered total: **29 pts** (27 − 3 + 5).

**Artifacts updated:** BRD (+BR-11), FRD (+FR-021), product backlog (+US-16), RTM (updated), dashboard
Tab 2 (state map added).
