# LendingClub Credit Decisioning & Portfolio Insights

A full business-analysis case study on real LendingClub loan data (2007–2018): from stakeholder
discovery through requirements, agile delivery, a reproducible data pipeline, a published Tableau
dashboard, and UAT-backed closure.

> **Note:** the company, stakeholders, and org scenario are hypothetical. **The dataset and every
> number in this repository are real** and reproducible from the pipeline below.
> Author: **Deepak Nepram** · [GitHub](https://github.com/DeepakNepram) · [LinkedIn](https://linkedin.com/in/deepaknepram)

## Live dashboard
**[View on Tableau Public →](https://public.tableau.com/app/profile/deepak.nepram/viz/LendingClubCreditDecisioningPortfolioInsights)**
Three tabs: Executive Overview · Funnel & Policy · Portfolio Risk.

## Headline findings (full data, independently validated)
- **2.26M** loans funded from **27.6M** applications — a **7.6%** overall approval rate.
- **20.0%** of resolved loans charged off (governed resolved-loan basis).
- **Grade E–G on 60-month terms charge off at 44.2% — 2.2x the portfolio average** (n = 90,183). The lead recommendation.
- Small-business purpose: **29.9%** charge-off (~1.5x average).

## What's in here

| Phase | Folder | Highlights |
|---|---|---|
| Discovery | `00-charter/`, `01-elicitation/`, `02-process-maps/` | Charter, RACI, interview guides + minutes, as-is/to-be process maps |
| Requirements | `03-requirements/` | BRD (11 BRs), FRD (21 FRs + rule catalog with evidence), data dictionary, ERD, PRD, change-request log (CR-001) |
| Agile delivery | `04-agile/` | 16-story backlog, acceptance criteria, 2 sprints (Jira), status report, burndown/velocity |
| Data | `05-data/` | `prepare_data.py` (reproducible pipeline), cleaning report, KPI dictionary, data-quality assessment |
| Dashboard | `06-dashboard/` | Tableau walkthrough + screenshots |
| Testing | `07-testing/` | UAT test cases, RTM (BR→FR→Story→Test), `validate_dashboard.py` + results |
| Closure | `08-closure/` | Business impact summary |

## Reproduce the analysis
```bash
# 1. Download the dataset from Kaggle (accepted + rejected 2007–2018) into data_raw/  (gitignored)
#    https://www.kaggle.com/datasets/wordsforthewise/lending-club
# 2. Run the pipeline (pandas + numpy; RANDOM_SEED = 42)
python 05-data/prepare_data.py
# 3. Independently validate the dashboard KPIs against the cleaning report
python 07-testing/validate_dashboard.py
# 4. Open the four CSVs in 05-data/samples/ as separate Tableau data sources (see dashboard walkthrough)
```

## Methods & governance
- **Governed definitions** live in the KPI dictionary and are enforced identically in the pipeline and
  the dashboard: charge-off rate is computed **on resolved loans only**; `default` is tracked
  separately; FICO bands use a confirmed 660 policy floor.
- **Reproducibility:** one script, fixed seed, full row accounting; the three governed flag sums
  reconcile to the integer and are re-asserted by an independent validation script.
- **Honesty guardrails:** dashboard drill-down uses a stratified sample (labelled); all headline
  figures are full-data. Known limitations (vintage right-censoring, date-basis mismatch, invalid
  rejected DTI) are documented in the data-quality assessment.

## Tools
Python (pandas, numpy) · Tableau Public · Jira · draw.io · dbdiagram.io · Figma · Git
