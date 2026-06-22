# KPI Dictionary
## Credit Decisioning & Portfolio Insights

> Scenario is hypothetical; all data is real LendingClub public data (2007–2018) from Kaggle.

This is the single governed source of KPI definitions (NFR-03, BR-02). The dashboard must use these
exact names and formulas. The **charge-off rate denominator is resolved loans only** — the definition
dispute this dictionary exists to settle. Reference values come from the full-data validation run
(`prepare_data.py` → `05-data/cleaning-report.txt`), not the Tableau sample. Field names match
`03-requirements/data-dictionary.md`.

| # | KPI | Governed formula | Grain | Owner | Reference value / target |
|---|---|---|---|---|---|
| 1 | **Approval Rate** | `n_accepted ÷ applications`, where `applications = n_accepted + n_rejected` | month → year → overall | Credit | **7.56%** overall (full data); track trend by vintage |
| 2 | **Funded Amount** | `Σ loan_amnt` over funded loans | month / year / segment | Finance | report on sample basis; annotate full-data total |
| 3 | **Avg Interest Rate** | `mean(int_rate)` | grade, sub_grade | Credit | rises monotonically A → G |
| 4 | **Charge-off Rate (resolved)** | `Σ charge_off_flag ÷ Σ resolved_flag` | portfolio; vintage; segment | Risk | **19.98%** overall (full data) — headline risk KPI |
| 5 | **Charge-off by Grade × Term** | charge-off rate (as #4) within each grade × term cell | grade × term | Risk | heatmap; E–G / 60-month = **44.2%** |
| 6 | **Default-in-progress Share** | `Σ default_flag ÷ loans not yet resolved` | month / segment | Risk | secondary monitor; 40 loans flagged Default |
| 7 | **Manual-review Share** | `Σ manual_review_flag ÷ applications` (funded book as proxy) | month | Ops | **6.77%** of funded book — capacity planning |
| 8 | **DTI Gap (accepted vs rejected)** | `mean(dti | accepted) − mean(dti | rejected, valid only)` | population | Credit | policy validation; rejected excludes invalid (negative) DTI |

## Denominator notes (the part interviewers probe)
- **Charge-off rate uses resolved loans only** — `resolved_flag = 1` (Fully Paid + Charged Off,
  including the legacy "Does not meet the credit policy. Status:…" variants). Loans still **Current**
  or in late/grace status are excluded because their final outcome is unknown; including them would
  understate the true charge-off rate. Governed value: 269,320 ÷ 1,348,059 = **19.98%**.
- **Default is separate from charge-off.** `default_flag` (40 loans, status "Default") is tracked
  apart from `charge_off_flag` as a leading/secondary signal, not part of the headline rate.
- **Approval-rate denominator** approximates applications as accepted + rejected. Accepted loans are
  counted by `issue_month` and rejected by `application_month`, so the monthly figure is directional;
  the overall 7.56% is exact.
- **Manual-review share** is computed on the funded book as a proxy for the application stream (the
  rules apply at application; the public data exposes funded loans). Used for review-queue capacity
  planning, not as a precise application-level rate.
