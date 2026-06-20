# Meeting Minutes — MoM-02: Operations Manager

> Scenario is hypothetical; all data is real LendingClub public data (2007–2018).

| | |
|---|---|
| **Date** | [date] |
| **Attendees** | [Your name] (BA); Operations Manager |
| **Purpose** | Understand the reporting workflow, definition conflicts, review capacity, and release expectations |

## Key findings
1. When leadership asks for a number, an analyst **pulls from several spreadsheets and reconciles
   by hand** — roughly **1–3 hours per request**, and the figures sometimes disagree between
   teams. (Input for the as-is process map.)
2. The team handles an estimated **8–10 ad-hoc pulls per week**; the biggest cost is
   **reconciliation and re-explaining definitions**, not the query itself. Removing these is the
   primary adoption goal.
3. **Definitions conflict across teams:** Finance and Risk compute **charge-off rate with different
   denominators**, and approval rate is sometimes reported with expired listings excluded. The
   Ops Manager strongly wants **one governed KPI dictionary** that every report uses.
4. **Sustainable manual-review volume is limited** — the team can staff on the order of a few
   hundred reviews per week. A threshold that flags a large share of applications would overwhelm
   them, so the **review-queue size must be forecastable before any rule goes live**.
5. Filters the team would actually use: **year, grade, purpose, term, and state** — wants any KPI
   reachable in **≤ 3 clicks** so analysts stop filing pull requests.
6. Worst failure seen: a **board number that was wrong because two teams used different
   denominators**. Consequently, dashboard numbers must be **validated against an independent
   cross-check before release**, and a **data-quality assessment + data dictionary** must back the
   pipeline.
7. **Conflict captured:** Ops wants **fewer manual reviews / thresholds sized to capacity** — "give
   me rules I can actually staff." (See MoM-01: Credit leans stricter. Resolution path below.)

## Decisions
- KPI definitions to be **centralized in a versioned dictionary** with one governed charge-off
  denominator (resolved loans, per MoM-01).
- Dashboard numbers to be **validated against an independent recomputation before release**.
- The **review-queue volume** to be estimated from the rules **before** launch.

## Action items
- **BA:** produce the **manual-review-flag share** (queue size) for candidate thresholds so volume
  can be checked against capacity.
- **BA:** draft the **KPI dictionary** and a **data-quality assessment** from the profiling
  evidence.

## Open questions
- Where to set thresholds so review volume stays within capacity — to be resolved using the
  charge-off-by-segment evidence from MoM-01's action items.

## Conflict resolution path
Same as MoM-01: thresholds set by **data evidence** (where charge-offs concentrate) and **sized to
the operational queue capacity**, prioritized as a "Should" (BR-06) so evidence precedes raising
review volume — the prioritization story for the BRD.
