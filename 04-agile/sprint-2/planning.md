# Sprint 2 — Planning

**Goal:** risk rules documented + full 3-tab dashboard released.

## Scope and rationale (planned)
| Story | Pts | Why this sprint |
|---|---|---|
| US-07 — documented rules catalog | 3 | Defensible review criteria |
| US-08 — compute manual_review_flag | 5 | Forecastable queue volume |
| US-09 — rule thresholds backed by evidence (Could) | 3 | Strengthens rules; lowest priority |
| US-10 — review-queue specification | 3 | Buildable future tool |
| US-12 — charge-off views (grade × term, purpose, vintage) | 5 | The sponsor's top Sprint-1 ask |
| US-13 — accepted-vs-rejected comparison | 3 | Validates policy thresholds |
| US-14 — filters + public link | 3 | Self-serve, ≤3 clicks |
| US-15 — walkthrough + UAT support | 2 | Release sign-off ready |
| **Total planned** | **27** | |

## Risks
- A change request could arrive (Compliance has a standing geographic-concentration ask) — handle via
  change control, not silent scope creep.
- `Risk_Score` is 66.9% null in the rejected file — the accepted-vs-rejected comparison (US-13) must
  use DTI, not risk score.
- Tableau Public applies filters per data source — note it in the walkthrough.
