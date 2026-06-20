# Lean PRD — Decisioning & Portfolio Insights Dashboard

> **Scenario note:** Hypothetical company; real LendingClub public data (2007–2018) from Kaggle.

| | |
|---|---|
| **Document** | Lean PRD · v1 (one page) |
| **Author** | Deepak Nepram, Business Analyst |
| **Feature** | The Credit Decisioning & Portfolio Insights dashboard |

## Problem
Credit and portfolio insight lives in ad-hoc spreadsheets with inconsistent definitions. Leadership
cannot quickly answer what the approval-rate trend is, where charge-offs concentrate, or which
segments warrant manual review — so decisions are slow and numbers disagree between teams.

## Target users
- **Head of Credit** (sponsor) — board-ready portfolio health and risk concentrations at a glance.
- **Credit Risk Analyst** — self-serve drill-down into segments (grade, term, purpose, vintage).
- **Operations Manager** — a forecastable manual-review queue sized to capacity.

## Solution
A 3-tab Tableau Public dashboard — **Executive Overview**, **Funnel & Policy**, **Portfolio Risk** —
backed by a governed KPI dictionary and a documented, evidence-based risk-review rules catalog, built
on the historical loan book (2.26M funded, 27.6M declined; 2007–2018).

## Success metrics
- **Adoption** — replaces the recurring ad-hoc data pulls.
- **Trust** — every published number matches an independent cross-check within 0.1 pp (UAT gate).
- **Speed** — any KPI reachable in ≤ 3 clicks.

## Out of scope
Machine-learning credit scoring; real-time decisioning systems; changes to pricing or live credit
policy.

## Risks
- Definition disputes recur and erode trust → mitigated by one governed KPI dictionary.
- The rejected-file `Risk_Score` is 66.9% null → accepted-vs-rejected comparison uses **DTI**, not risk score.
- Tableau Public applies filters per data source → documented in the dashboard walkthrough.

## Open questions
- The manual-review thresholds (the DTI cutoff; which grade/term combinations) — to be set from the
  Day 9 charge-off-by-segment evidence, then governed via change control.
- The FICO policy floor (≈ 660) — to be confirmed against the actual accepted FICO distribution in Day 9.
- *(Settled: charge-off rate is computed over resolved loans only — fully paid + charged off.)*

## Wireframes
Mid-fidelity wireframes for the three views: **https://www.figma.com/proto/bbSCes8ulusVqQIUenSRko/Untitled?node-id=6-263&t=nlwjgp7DPI7fPuHr-1**
