# Business Requirements Document (BRD)
## Credit Decisioning & Portfolio Insights

> **Scenario note:** The company and stakeholders are hypothetical. All data is real LendingClub
> public data (2007–2018) from Kaggle.

| | |
|---|---|
| **Document** | BRD · v1 (draft for sign-off) |
| **Author** | Deepak Nepram, Business Analyst |
| **Sponsor** | Head of Credit |
| **Sources** | MoM-01 (Head of Credit), MoM-02 (Operations Manager), as-is / to-be process maps |

---

## 1. Executive summary
The Credit team has no single, governed view of the loan book. Approval-rate trends, charge-off
concentrations, and review criteria live in ad-hoc spreadsheets with definitions that differ
between teams. This initiative delivers one governed dashboard plus a documented risk-review rules
catalog, built on the company's historical book of **2.26M funded loans and 27.6M declined
applications (2007–2018)**, across two Scrum sprints and validated through UAT before release.

## 2. Problem and gap
Leadership cannot quickly or consistently answer three recurring questions: *What is our
approval-rate trend? Where are charge-offs concentrating? Which segments warrant manual review?*
As the as-is process map (`02-process-maps/`) shows, the current flow produces decisions and
outcomes but **no governed insight layer** — there is no unified approval-rate view, charge-off
concentrations are invisible until they are large, and KPI definitions are undocumented and
inconsistent across Finance, Risk, and Ops. The to-be map closes these gaps with a Data & Analytics
lane feeding a governed dashboard.

## 3. Objectives and success metrics
| Objective | Success metric |
|---|---|
| **O1** — One governed dashboard for funnel, portfolio, and risk KPIs | Released by end of Sprint 2; adopted in place of ad-hoc pulls |
| **O2** — Documented, evidence-based risk-review rules catalog | Approved by the Head of Credit; every threshold justified against the data |
| **O3** — Self-serve segment drill-down | Any KPI reachable in ≤ 3 clicks; numbers match cross-checks within 0.1 pp |

## 4. Scope
**In scope:** historical loan-book analysis (2007–2018); KPI definitions; the risk-review rules
catalog; the dashboard; UAT validation.
**Out of scope:** machine-learning credit scoring; real-time decisioning systems; changes to pricing
or live credit policy; any personally identifiable data.

## 5. Stakeholders
Six roles, detailed in `00-charter/stakeholder-register-raci.md`. The Head of Credit is sponsor and
Accountable on every approval gate; Compliance is Consulted on the rules and release; the Credit
Risk Analyst, Operations Manager, Data/IT Lead, and Investor Relations are the remaining roles.

## 6. Business requirements
MoSCoW priority. Every requirement traces to a source interview (MoM).

| ID | Business requirement | MoSCoW | Rationale | Source |
|---|---|---|---|---|
| **BR-01** | A single governed dashboard for funnel, portfolio, and risk KPIs | Must | Removes the slow manual stitching across spreadsheets; the highest-value need | MoM-01 |
| **BR-02** | Standardized, documented KPI definitions in one dictionary | Must | Ends cross-team definition conflicts (e.g. the charge-off denominator) that produced a wrong board number | MoM-01 / 02 |
| **BR-03** | Visibility of application-vs-approval volumes and approval-rate trend | Must | A core question leadership cannot currently answer quickly | MoM-01 |
| **BR-04** | Rule-based criteria routing high-risk applications/segments to manual review | Must | Makes review criteria explicit and defensible to the board | MoM-01 |
| **BR-05** | Portfolio risk view by grade, term, purpose, and vintage | Must | Surfaces the segment concentrations the sponsor suspects but cannot confirm today | MoM-01 |
| **BR-06** | Comparison of accepted vs rejected applicant profiles to validate policy | Should | *Should, not Must — validates thresholds with evidence before raising review volume, resolving the Credit-vs-Ops conflict* | MoM-01 |
| **BR-07** | Cohort/vintage monitoring of charge-off development | Should | Early detection of deteriorating vintages; valuable but secondary to the headline risk view | MoM-01 |
| **BR-08** | Documented data-quality assessment and data dictionary | Must | Trustworthy numbers require documented data handling; also underpins auditability | MoM-02 |
| **BR-09** | Self-serve filtering for the Credit team (≤ 3 clicks to any KPI) | Should | Eliminates the recurring ad-hoc-pull burden; the dashboard delivers value even before full self-serve polish | MoM-02 |
| **BR-10** | Dashboard numbers validated against independent cross-checks before release | Must | Directly prevents the "wrong board number" failure; the release gate | MoM-02 |

**Note on BR-06 (the prioritization decision):** Credit wants stricter review thresholds; Ops needs
review volume bounded by capacity. Rather than pick a side, BR-06 is prioritized as a **Should** so
that thresholds are first **validated with evidence** — where charge-offs actually concentrate,
using DTI and observed segment charge-off rates — and **sized to the operational queue** before any
increase in manual-review volume. This is the conflict-resolution rationale carried into the FRD and
the rules catalog.

## 7. Assumptions and constraints
- The public 2007–2018 book adequately represents the loan portfolio for definition and trend purposes.
- Public artifacts contain **samples and aggregates only**; raw multi-GB files are never committed.
- The dashboard is hosted on Tableau Public; filters apply per data source (a known constraint,
  documented in the dashboard walkthrough).
- The pipeline is fully reproducible: one script, a fixed random seed, pinned versions.

## 8. Risks
| Risk | Mitigation |
|---|---|
| The rejected-file `Risk_Score` is **66.9% null**, limiting accepted-vs-rejected risk comparison | Use **DTI** (present on both sides) as the comparison basis instead of risk score |
| Self-reported income and out-of-range DTI values distort segment metrics | Flag and document outliers in the data-quality assessment rather than silently dropping them |
| Definition disputes (charge-off denominator) recur and erode trust | Settle one governed definition (resolved loans) in the KPI dictionary; gate release on cross-checks (BR-10) |

## 9. Sign-off
| Role | Name | Date | Signature |
|---|---|---|---|
| Head of Credit (Sponsor) | | | |
| Compliance Officer | | | |
| Operations Manager | | | |
