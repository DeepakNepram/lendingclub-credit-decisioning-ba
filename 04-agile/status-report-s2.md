# Status Report — Sprint 2 (to the Sponsor)

> Scenario is hypothetical; all data is real LendingClub public data (2007–2018).

**Status: 🟢 GREEN** · Period: Sprint 2 (of 2)

**Accomplished**
- Risk-review rules catalog documented (RULE-01…06); `manual_review_flag` computed and validated.
- Full 3-tab dashboard built (Executive Overview, Funnel & Policy, Portfolio Risk).
- CR-001 (state-level concentration map) approved and absorbed; US-09 (Could) deferred to backlog.
- Sprint 2 closed at **29 points delivered**; velocity **28 → 29**.

**Next**
- UAT against independent cross-checks — every Must requirement gets ≥ 1 passing test.
- Dashboard release and sign-off.

**Risks / Issues**
- `Risk_Score` is 66.9% null in the rejected file — the accepted-vs-rejected comparison uses DTI
  instead (mitigated). See the RAID log in the charter.

**Decisions needed**
- Sponsor sign-off on the charge-off denominator (resolved-loans basis) for release — recommended, as
  it is already governed in the KPI dictionary.
