# Project Charter — Credit Decisioning & Portfolio Insights

> **Scenario note:** The company and its stakeholders are hypothetical. All data is **real
> LendingClub public data (2007–2018)** from Kaggle. This charter is written as though for an
> internal initiative at a marketplace lender.

| | |
|---|---|
| **Project** | Credit Decisioning & Portfolio Insights Dashboard |
| **Sponsor** | Head of Credit |
| **Business Analyst** | [Your name] |
| **Date** | [date] |
| **Status** | Initiated |

## 1. Background
The company is a marketplace lender connecting individual borrowers with investors who fund their
loans. Applicants are screened against a credit policy, assigned a grade (A–G) with a corresponding
interest rate, and — if funded — repay over a 36- or 60-month term; the business earns origination
and servicing fees. Its historical loan book comprises **2.26M funded loans and 27.6M declined
applications (2007–2018)**. Today, insight into that book lives in scattered, ad-hoc spreadsheets
with inconsistent definitions.

## 2. Problem statement
Credit and portfolio insight is fragmented across manual spreadsheets. Leadership cannot quickly or
consistently answer three recurring questions: *What is our approval-rate trend? Where are
charge-offs concentrating? Which segments warrant manual review?* The result is slow decisions,
conflicting numbers between teams, and risk concentrations that surface late.

## 3. Objectives (SMART)
- **O1 —** Deliver one governed dashboard covering funnel, portfolio, and risk KPIs, released by the
  end of Sprint 2.
- **O2 —** Produce a documented, evidence-based risk-review rules catalog, approved by the Head of
  Credit, with every threshold justified against the historical data.
- **O3 —** Enable self-serve segment drill-down (year, grade, purpose, term, state), reaching any
  KPI in ≤ 3 clicks.

## 4. Scope
**In scope:** historical loan-book analysis (2007–2018); KPI definitions; the risk-review rules
catalog; the dashboard; and UAT validation against independent cross-checks.
**Out of scope:** machine-learning credit scoring; real-time decisioning systems; changes to pricing
or live credit policy; any personally identifiable data.

## 5. RAID (summary)
| Type | Item |
|---|---|
| **Risk** | The rejected-applications file's `Risk_Score` is **66.9% null**, so accepted-vs-rejected risk comparison will rely on **DTI** (present on both sides) rather than risk score. |
| **Assumption** | The public 2007–2018 book adequately represents the loan portfolio for definition and trend purposes. |
| **Issue** | KPI definitions — especially the charge-off denominator — are inconsistent across teams today; to be resolved in the KPI dictionary. |
| **Dependency** | Kaggle dataset availability; Tableau Public for hosting; stakeholder availability for elicitation and UAT sign-off. |

## 6. Success measures
- A single source of truth adopted in place of ad-hoc pulls (O1).
- Rules catalog approved with data-backed thresholds (O2).
- Any KPI reachable in ≤ 3 clicks; dashboard figures match independent cross-checks within 0.1 pp
  (O3, BR-10).

## 7. High-level approach
Two-sprint delivery: discovery & requirements → Sprint 1 (data foundation + executive overview) →
Sprint 2 (risk rules + full 3-tab dashboard) → UAT & release.
