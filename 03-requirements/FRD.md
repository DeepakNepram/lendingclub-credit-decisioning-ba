# Functional Requirements Document (FRD)
## Credit Decisioning & Portfolio Insights

> **Scenario note:** Hypothetical company; real LendingClub public data (2007–2018) from Kaggle.

| | |
|---|---|
| **Document** | FRD · v1 |
| **Author** | [Your name], Business Analyst |
| **Audience** | Data/IT Lead, Credit Risk Analyst, Operations Manager, Head of Credit |
| **Traceability** | Every functional requirement traces to a business requirement in `BRD.md`. The full BR → FR → Story → Test chain is maintained in `07-testing/rtm.xlsx`. |

---

## 1. Introduction
This document specifies the functional requirements for the Credit Decisioning & Portfolio Insights
solution. Requirements are organized into three modules — **M1 Data Foundation**, **M2 Decisioning
Rules & Review Workflow**, and **M3 Dashboard & Reporting** — and each is traced to a business
requirement. Business rules and non-functional requirements follow the functional list.

## 2. Functional requirements

### M1 — Data Foundation
| ID | Functional requirement | BR |
|---|---|---|
| **FR-001** | Ingest the accepted dataset restricted to the 25 governed fields | BR-08 |
| **FR-002** | Ingest the rejected dataset with column standardization: snake_case the verbatim headers (`Amount Requested`, `Application Date`, `Risk_Score`, `Debt-To-Income Ratio`, …), strip the "%" from the DTI column only, and parse dates | BR-03 |
| **FR-003** | Apply documented cleaning rules: drop rows with null `loan_amnt` (the 33 footer rows), strip the leading space from `term` and cast to integer months, map `emp_length` to an ordinal | BR-08 |
| **FR-004** | Derive governed fields: `fico_mid`, `fico_band`, `issue_month`, `charge_off_flag`, `resolved_flag`, `default_flag` | BR-02 |
| **FR-005** | Produce reproducible outputs (samples + aggregates) from a single script with a fixed random seed | BR-10 |
| **FR-006** | Emit a data-quality report (row counts, null rates, dropped-row log) on every run | BR-08 |
| **FR-007** | Maintain KPI definitions in a versioned dictionary; the dashboard must use these names | BR-02 |

### M2 — Decisioning Rules & Review Workflow
| ID | Functional requirement | BR |
|---|---|---|
| **FR-008** | Maintain a machine-readable business-rules catalog (the rules table below) | BR-04 |
| **FR-009** | Compute `manual_review_flag` per application from the rules catalog | BR-04 |
| **FR-010** | Provide a review-queue specification (fields, sort order, daily volume estimate) | BR-04 |
| **FR-011** | Rule thresholds are changeable only via a change-control record | BR-04 |
| **FR-012** | Every rule is documented with the data evidence supporting its threshold | BR-06 |
| **FR-013** | Log requirement for review overrides (who, when, why) in the to-be design | BR-04 |

### M3 — Dashboard & Reporting
| ID | Functional requirement | BR |
|---|---|---|
| **FR-014** | Executive overview: 5 headline KPIs (funded $, loans, approval rate, charge-off rate, avg interest rate) | BR-01 |
| **FR-015** | Issuance and approval-rate trend views with year filtering | BR-03 |
| **FR-016** | Charge-off heatmap by grade × term and by purpose | BR-05 |
| **FR-017** | Accepted-vs-rejected DTI distribution comparison (DTI, not risk score — see risk note in BRD) | BR-06 |
| **FR-018** | Vintage-year charge-off development view | BR-07 |
| **FR-019** | Global filters (year, grade, purpose, term) reaching any KPI in ≤ 3 clicks | BR-09 |
| **FR-020** | Published public dashboard link plus a written walkthrough | BR-01 |

## 3. Business-rules catalog
Each rule routes an application to a review action. Thresholds change only via change control (FR-011)
and each must be backed by data evidence (FR-012). The **evidence** column is completed from the Day 9
analysis — values below are placeholders pending that computation, never asserted from memory.

| ID | Rule statement | Action | Data evidence (confirm in Day 9 analysis) | Traces |
|---|---|---|---|---|
| **RULE-01** | FICO below the policy floor (≈ 660) | Outside credit policy | Verify the floor visibly in the accepted `fico_range` distribution before asserting it | FR-008 |
| **RULE-02** | DTI > 40% | Route to manual review | Compute flagged share; `dti` present, 2,563 out-of-range values flagged not deleted | FR-009 |
| **RULE-03** | Grade E–G **and** term = 60 months | Enhanced review | Justify with charge-off rate by grade × term; grades E/F/G = 135,639 / 41,800 / 12,168 loans | FR-009 |
| **RULE-04** | Income unverified **and** loan_amnt > $20,000 | Income verification | Size the affected share; `verification_status` present | FR-009 |
| **RULE-05** | Segment with vintage charge-off > 1.5× portfolio average | Threshold review | Portfolio resolved charge-off ≈ 20% → ≈ 30% trigger; compute per vintage | FR-008 |
| **RULE-06** | Small-business purpose | Heightened monitoring | Compute its charge-off rate; small_business = 24,689 loans | FR-008 |

## 4. Non-functional requirements
| ID | Non-functional requirement |
|---|---|
| **NFR-01** | Monthly data-refresh cadence |
| **NFR-02** | Filter response under 5 seconds |
| **NFR-03** | KPI names governed by the dictionary (single source) |
| **NFR-04** | Full reproducibility: one script, pinned versions, fixed seed |
| **NFR-05** | Public artifacts contain samples/aggregates only — no raw data |
| **NFR-06** | Auditability via Git history |
| **NFR-07** | Usability: chart titles phrased as insights, not labels |
| **NFR-08** | Accuracy: dashboard matches independent cross-check within 0.1 pp |
| **NFR-09** | Works logged-out in a browser (Tableau Public) |
| **NFR-10** | Accessibility-conscious, color-blind-safe palette |

## 5. Traceability note
This FRD establishes the FR → BR linkage. Each functional requirement is realized by one or more user
stories in `04-agile/product-backlog.csv` and verified by a test case in `07-testing/uat-test-cases.xlsx`;
the complete chain is consolidated in the RTM.
