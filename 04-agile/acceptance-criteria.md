# Acceptance Criteria (Gherkin)
## Credit Decisioning & Portfolio Insights — product backlog

> Scenario is hypothetical; all data is real LendingClub public data (2007–2018).
> Two acceptance scenarios per story. Each **Then** clause states a measurable outcome — a number,
> a tolerance, or a verifiable state. Paste each story's criteria into its Jira issue description.

---

### E1 — Data Foundation

**US-01** — ingest the accepted file (governed fields). *Traces: FR-001*
- Given the raw accepted file, When ingestion runs, Then exactly the 25 governed fields load And any requested field missing from the header is reported and skipped.
- Given the loaded accepted dataframe, When the row count is checked, Then it equals 2,260,701 before cleaning.

**US-02** — standardize the rejected file. *Traces: FR-002*
- Given the raw rejected file, When standardization runs, Then all column names are snake_case And only the DTI column has its "%" stripped And the date column parses from ISO format.
- Given the standardized rejected dataframe, When the DTI dtype is checked, Then it is float with zero residual "%" characters.

**US-03** — documented cleaning and derived fields. *Traces: FR-003/004*
- Given the raw accepted file, When prepare_data.py runs, Then rows with null loan_amnt are dropped And the dropped count is printed And term and emp_length contain zero residual string values.
- Given the cleaned dataframe, When the derived fields are verified, Then charge_off_flag sums to 269,320 And resolved_flag sums to 1,348,059.

**US-04** — single reproducible script. *Traces: FR-005*
- Given RANDOM_SEED = 42, When the script runs twice, Then the two accepted samples are identical row-for-row.
- Given one script execution, When it completes, Then every sample and aggregate CSV is present in 05-data/samples/.

**US-05** — data-quality report per run. *Traces: FR-006*
- Given a script run, When it completes, Then a data-quality report lists rows in/out, null rates, and the dropped-row count.
- Given the report, When reviewed, Then every dropped or flagged row has a stated reason.

**US-06** — governed KPI dictionary. *Traces: FR-007*
- Given the KPI dictionary, When a dashboard KPI is referenced, Then its name matches a dictionary entry exactly.
- Given the dictionary, When charge-off rate is defined, Then its denominator is stated as resolved loans (fully paid + charged off).

### E2 — Decisioning Rules & Review Workflow

**US-07** — documented rules catalog. *Traces: FR-008*
- Given the rules catalog, When reviewed, Then every rule has an ID, a statement, an action, and a traced FR.
- Given any rule, When its threshold is examined, Then it cites supporting data evidence or is flagged pending the Day 9 analysis.

**US-08** — compute manual_review_flag. *Traces: FR-009*
- Given the cleaned accepted sample, When RULE-02 and RULE-03 are applied, Then manual_review_flag matches an independent pandas recount exactly And the flagged share is reported as a percentage.
- Given manual_review_flag, When dti > 40 OR (grade in E/F/G AND term == 60) holds, Then the flag is 1 (else 0) with no nulls.

**US-09** — rule thresholds backed by evidence. *Traces: FR-012*
- Given any rule, When its threshold is challenged, Then a number computed from the data is cited as justification.
- Given RULE-03, When grade × term charge-off rates are computed, Then the enhanced-review segment's rate exceeds the ~20% portfolio average by a stated margin.

**US-10** — review-queue specification. *Traces: FR-010*
- Given the review-queue specification, When reviewed, Then it lists the queue fields, the sort order, and an estimated weekly volume.
- Given the volume estimate, When compared to capacity, Then the flagged share is stated as a percentage of applications.

### E3 — Dashboard & Reporting

**US-11** — executive overview. *Traces: FR-014/015*
- Given the published dashboard, When a logged-out user opens the link, Then five KPI cards render And selecting year = 2015 updates every card on the tab within 5 seconds.
- Given the executive overview, When the trend is shown, Then it spans 2007–2018 with no missing years.

**US-12** — charge-off views by segment. *Traces: FR-016/018*
- Given the portfolio risk tab, When the grade × term heatmap renders, Then each cell's charge-off rate is computed over resolved loans only.
- Given the vintage view filtered to a grade, When the charge-off rate by issue year is shown, Then it matches a pandas/SQL cross-check within 0.1 pp.

**US-13** — accepted-vs-rejected comparison. *Traces: FR-017*
- Given the comparison view, When accepted and rejected DTI distributions render, Then both populations appear side by side using DTI.
- Given the rejected population, When risk score is considered, Then the view notes Risk_Score is 66.9% null and relies on DTI.

**US-14** — self-serve filters and public link. *Traces: FR-019/020*
- Given the dashboard, When any KPI is reached via filters, Then it takes ≤ 3 clicks from the overview.
- Given the published link, When opened logged-out, Then all tabs are visible and interactive.

**US-15** — walkthrough and UAT support. *Traces: FR-020, BR-10*
- Given the walkthrough, When reviewed, Then it contains three headline insights with exact numbers.
- Given release readiness, When UAT completes, Then every Must-priority requirement has ≥ 1 passing test.

**US-16** — state-level concentration map (added via CR-001). *Traces: FR-021*
- Given the state-concentration map, When it renders, Then all states display And nulls/territories are handled without breaking the map.
- Given the map, When a state is selected, Then its approval rate or funded amount matches a cross-check within 0.1 pp.
