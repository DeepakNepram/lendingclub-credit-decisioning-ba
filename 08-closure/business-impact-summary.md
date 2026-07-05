# Business Impact Summary
## LendingClub Credit Decisioning & Portfolio Insights

> Scenario is hypothetical; all data is real LendingClub public data (2007–2018) from Kaggle.
> Prepared by Deepak Nepram (Business Analyst) · Closure memo for the Head of Credit (sponsor)

---

## 1. The ask

The credit organization funded 2.26M loans across 2007–2018 but lacked a governed, self-serve view of
portfolio health and no documented, evidence-backed basis for its manual-review rules. This project
delivered a reproducible data pipeline, governed KPI definitions, a documented rule set, and a
published three-tab dashboard — so that approval, funding, and credit-risk questions can be answered
consistently and defensibly.

## 2. What the data says (all figures full-data unless noted)

- **Scale & selectivity.** 27.6M applications resolved to 2.26M funded loans — an overall approval
  rate of **7.6%**. Approvals tightened over time even as volume grew ~1000x, indicating disciplined
  scaling rather than loosening standards.
- **Headline risk.** Across resolved loans, **20.0% charged off** (269,320 of 1,348,059). This is the
  governed portfolio risk KPI, defined on resolved loans only.
- **The strongest concentration — the basis for the lead recommendation.** Loans graded **E–G on
  60-month terms charge off at 44.2%**, versus the 20.0% portfolio average — **2.2x the book**, on
  90,183 resolved loans. Risk rises monotonically A→G and 36→60 within every grade.
- **Purpose signal.** Small-business loans charge off at **29.9%** (~1.5x the average); the book is
  otherwise dominated by debt-consolidation and credit-card refinancing.
- **Policy validation.** Rejected applicants show a far wider DTI spread than accepted (heavy 60+
  tail, 3.1M applications), empirically supporting the DTI-based review screen. (Comparison uses DTI,
  not Risk_Score, which is 66.9% null in the rejected file.)

## 3. Recommendations

1. **Formalize enhanced review for the grade E–G / 60-month segment.** At 44.2% vs 20.0%, this is the
   clearest, highest-conviction risk concentration in the book. Treat it as the priority rule
   (RULE-03), with either tighter pricing, reduced exposure, or mandatory secondary review.
2. **Keep the DTI > 40% screen; it is doing work.** The accepted-vs-rejected DTI contrast shows the
   screen already binds at application. Retain it and monitor the ~1.2% of funded loans that still
   exceed it.
3. **Add heightened monitoring for small-business purpose** (29.9% charge-off). Smaller in volume but
   materially riskier per dollar.
4. **Operationalize the manual-review queue at ~6.8% of applications.** The governed
   `manual_review_flag` flags 6.77% of the funded book — a capacity figure Ops can plan against.
5. **Adopt the governed KPI definitions as the single source of truth.** Charge-off on a resolved-loan
   basis, default tracked separately — this stops the definitional drift that motivated the project.

## 4. How the work was delivered (BA practice)

- **Discovery & requirements:** charter, RACI, two elicitation cycles with a documented Credit-vs-Ops
  conflict resolved by evidence; 11 business requirements → 21 functional requirements.
- **Agile delivery:** 16 stories over two sprints in Jira (velocity 28 → 29), including a mid-project
  change request (**CR-001**) for a state-concentration map — absorbed by deferring a lower-priority
  story to protect the sprint goal.
- **Data & analysis:** one reproducible pipeline (`prepare_data.py`, seed 42) over 2.26M accepted and
  27.6M rejected records, with governed derived fields and a data-quality assessment.
- **Visualization:** a published three-tab Tableau dashboard (executive, funnel/policy, risk).
- **Testing & governance:** 12 UAT cases and a full BR→FR→Story→Test traceability matrix, plus an
  independent validation script asserting every dashboard KPI against the pipeline within tolerance.

## 5. Honesty notes (limitations carried into the recommendations)

- Dashboard drill-down runs on a 113,565-row stratified sample; **all headline figures above are
  full-data** and independently re-validated.
- The 2017–2018 vintage charge-off is right-censored (young loans) — not read as improving credit.
- Monthly approval rate is directional (issue-month vs application-month basis); the overall rate is exact.

---

*Company and stakeholders are hypothetical; the dataset and every number above are real and reproducible
from this repository.*
