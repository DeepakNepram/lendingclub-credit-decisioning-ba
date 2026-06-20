# Stakeholder Register & RACI

> Scenario is hypothetical; all data is real LendingClub public data (2007–2018).

## Stakeholder register
| Role | Interest | Influence | Needs from the project |
|---|---|---|---|
| **Head of Credit** (Sponsor) | High | High | Risk concentrations made visible; rules defensible to the board |
| **Credit Risk Analyst** | High | Medium | Segment drill-downs; trustworthy, governed definitions |
| **Operations Manager** | High | Medium | Fewer ad-hoc data pulls; clear, sustainable review-queue criteria |
| **Compliance Officer** | Medium | High | Auditable definitions; geographic-concentration visibility |
| **Data / IT Lead** | Medium | Medium | A reproducible pipeline; no shadow datasets |
| **Investor Relations** | Low | Medium | Portfolio-quality talking points for investors |

## RACI — key decisions
R = Responsible · A = Accountable · C = Consulted · I = Informed

| Decision | BA (you) | Head of Credit | Compliance | Ops Manager | Risk Analyst | Data/IT |
|---|---|---|---|---|---|---|
| Sign off BRD | R | A | C | C | C | I |
| Approve business rules | R | A | C | I | C | I |
| Approve dashboard release | R | A | C | I | I | C |
| UAT sign-off | R | A | C | C | C | I |
| Change-control decisions | R | A | C | I | I | I |

**Notes**
- The Head of Credit is **Accountable** on every gate as sponsor; Deepak Nepram (the BA) are **Responsible**
  for driving each to a decision.
- Compliance is **Consulted** on the rules and the dashboard release (auditability and geographic
  concentration — the latter is the driver behind change request CR-001 later in the project).
- The built-in tension between Credit (wants stricter review thresholds) and Ops (wants fewer manual
  reviews) is captured during elicitation and resolved through evidence in the BRD's prioritization
  of BR-06.
