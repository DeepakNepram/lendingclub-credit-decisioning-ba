# Meeting Minutes — MoM-01: Head of Credit

> Scenario is hypothetical; all data is real LendingClub public data (2007–2018).

| | |
|---|---|
| **Date** | [date] |
| **Attendees** | [Your name] (BA); Head of Credit (Sponsor) |
| **Purpose** | Elicit portfolio-insight gaps, risk-metric definitions, and adoption criteria |

## Key findings
1. The question that takes longest today is **where charge-offs are concentrating by segment** —
   it currently requires a manual pull stitched across several spreadsheets, so it is answered
   slowly and inconsistently. A **single dashboard for funnel, portfolio, and risk** would remove
   this.
2. Segments of greatest concern: **lower grades (E–G)** and **60-month terms**, plus the
   **small-business purpose**. The sponsor believes these run materially higher charge-offs but
   has **no unified view to confirm it** — wants portfolio risk visible by **grade, term, purpose,
   and vintage**.
3. **Charge-off rate is defined over resolved loans only** — i.e. fully paid + charged off;
   open/current loans are excluded from the denominator. This is to be the governed definition.
4. The sponsor will trust a number only if its **definition is documented once and the value is
   cross-checked against an independent recomputation before release** — and wants the
   **approval-rate trend** (applications vs approvals over time) visible alongside risk.
5. On manual review, the sponsor initially favors **strict triggers**: a low DTI cutoff and routing
   **all grade E–G, 60-month** applications to review, and is interested in **validating thresholds
   against the accepted-vs-rejected applicant profile** before finalizing.
6. **Conflict captured:** the sponsor leans toward stricter thresholds *even if review volume
   rises* — "I'd rather review more than miss a bad cohort." (See MoM-02: Ops needs review volume
   bounded by capacity. Resolution path below.)
7. 90-day success = the team **self-serves segment drill-downs** and the sponsor has a
   **rules catalog they can defend to the board**.

## Decisions
- Charge-off rate denominator = **resolved loans** (fully paid + charged off).
- The dashboard is to be the **single source of truth**; risk-review thresholds must be
  **evidence-based**, justified against the historical data.

## Action items
- **BA:** quantify charge-off rate by **grade × term** and by **purpose** to evidence the segments
  of concern.
- **BA:** size the **manual-review queue** implied by candidate thresholds (the review-flag share),
  for the capacity discussion with Ops.

## Open questions
- Exact DTI cutoff (40% vs lower?) — to be set from observed charge-off evidence.
- The rejected-side **`Risk_Score` is largely unavailable**, so accepted-vs-rejected policy
  validation will rely on **DTI** rather than risk score — confirm this is acceptable.

## Conflict resolution path
Credit wants stricter thresholds (catch more risk); Ops wants fewer reviews (capacity). Resolution:
**validate where charge-offs actually concentrate** (DTI + observed segment charge-off rates),
set thresholds by that evidence, and **size them to the queue capacity** — captured as a "Should"
priority (BR-06) so evidence precedes any increase in review volume.
