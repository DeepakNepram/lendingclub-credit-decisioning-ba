# Data Dictionary
## Credit Decisioning & Portfolio Insights

> **Scenario note:** Hypothetical company; real LendingClub public data (2007–2018) from Kaggle.

| | |
|---|---|
| **Document** | Data Dictionary · v1 |
| **Author** | Deepak Nepram, Business Analyst |
| **Scope** | The 25 governed fields ingested from the accepted file by `05-data/profile_data.py`, plus 7 derived fields. |
| **Traceability** | Field set traces to **FR-001** (ingest 25 governed fields) and **FR-004** (derive governed fields). Cleaning rules trace to **FR-003**. |

### Provenance of definitions
- No `LCDataDictionary` file is present in this repo. Definitions below are **paraphrased to one line from the standard LendingClub field semantics** (not quoted verbatim) and **corroborated against the runtime evidence** in [`05-data/profiling-notes.md`](../05-data/profiling-notes.md).
- A definition that rests **only** on observed data (no canonical source) is tagged **(empirical)**.
- **Type** and **Quality notes** are taken directly from `profiling-notes.md` (dtype, null counts/%, value counts, out-of-range counts). Row base for all percentages: **2,260,701** accepted rows.
- ⚠ marks a field where the **observed data contradicts / deviates from the official definition or expected format** — see the [contradictions summary](#observed-vs-official-contradictions) below the table.

### The "33 footer rows"
33 accepted rows are footnote/garbage rows: `loan_amnt` (and effectively all numeric fields) is null while `id` holds a **text footnote**. They are the `nan` bucket in the term/grade/loan_status value counts. **Drop them on null `loan_amnt`, not on null `id`** (FR-003). This is why almost every field shows a baseline of 33 nulls; counts above 33 indicate genuine missing values.

---

## Field table

| Field | Type | Definition (one line) | Quality notes | Source |
|---|---|---|---|---|
| `id` | object (string) | Unique LendingClub identifier for the loan listing. | **0 nulls**, but ⚠ on the 33 footer rows `id` holds a **text footnote**, not a numeric key — `id` is non-null *exactly* where `loan_amnt` is null. Do not use null-`id` to drop footer rows. | accepted file |
| `loan_amnt` | float64 | Amount of the loan applied for by the borrower. | 33 nulls (0.0%) = footer rows; null-`loan_amnt` is the canonical drop key. | accepted file |
| `funded_amnt` | float64 | Total amount committed to the loan at issuance. | 33 nulls (0.0%); equals `loan_amnt` in the sampled rows. | accepted file |
| `term` | object (string) | Number of monthly payments — 36 or 60 months. | 33 nulls. ⚠ **Leading space on 2,260,668 rows** (`' 36 months'` / `' 60 months'`) → strip and cast to integer months (FR-003). | accepted file |
| `int_rate` | float64 | Interest rate on the loan (annual, %). | 33 nulls. ⚠ Already a **numeric float** here (no `%` suffix), unlike the classic LC `%`-string format. | accepted file |
| `installment` | float64 | Monthly payment owed if the loan originates. | 33 nulls (0.0%). | accepted file |
| `grade` | object (string) | LendingClub assigned credit grade A–G. | 33 nulls. Distribution: B 663,557 · C 650,053 · A 433,027 · D 324,424 · E 135,639 · F 41,800 · G 12,168. | accepted file |
| `sub_grade` | object (string) | LendingClub assigned sub-grade (A1–G5). | 33 nulls (0.0%). | accepted file |
| `emp_length` | object (string) | Borrower employment length, `< 1 year` … `10+ years`. | **146,940 nulls (6.5%)** — largest gap among governed fields; map to an ordinal (FR-003). | accepted file |
| `home_ownership` | object (string) | Home ownership status (MORTGAGE / RENT / OWN / …). | 33 nulls (0.0%). | accepted file |
| `annual_inc` | float64 | Self-reported annual income. | **37 nulls** = 33 footer + **4 genuine** missing values. | accepted file |
| `verification_status` | object (string) | Whether income was verified (Verified / Source Verified / Not Verified). | 33 nulls (0.0%). Drives RULE-04. | accepted file |
| `issue_d` | object (string) | Month the loan was funded. | 33 nulls. ⚠ Stored as a **STRING in `%b-%Y`** (e.g. `Dec-2015`), **not a date**; range Jun-2007 → Dec-2018. Parse before any time analysis. | accepted file |
| `loan_status` | object (string) | Current status of the loan. | 33 nulls. 9 statuses; includes **legacy** `Does not meet the credit policy. Status:Fully Paid` (1,988) / `…Charged Off` (761) and `Default` (40). Basis for the resolved/charge-off/default flags. | accepted file |
| `purpose` | object (string) | Borrower-stated reason for the loan. | 33 nulls. Dominated by `debt_consolidation` (1,277,877) and `credit_card` (516,971); `small_business` = 24,689 (RULE-06). | accepted file |
| `addr_state` | object (string) | Borrower state (2-letter US code). | 33 nulls (0.0%). | accepted file |
| `dti` | float64 | Monthly debt payments ÷ monthly income (excl. mortgage), as a %. | 1,744 nulls (0.08%). ⚠ **2,563 values <0 or >100** (out of range) → flag `dti_outlier`, **do not delete** (FR-003). Threshold for RULE-02. | accepted file |
| `fico_range_low` | float64 | Lower bound of the borrower's FICO range at application. | 33 nulls (0.0%). Parent of `fico_mid`. | accepted file |
| `fico_range_high` | float64 | Upper bound of the borrower's FICO range at application. | 33 nulls (0.0%). Parent of `fico_mid`. | accepted file |
| `open_acc` | float64 | Number of open credit lines in the borrower's file. | **62 nulls** = 33 footer + 29 genuine. | accepted file |
| `revol_util` | float64 | Revolving line utilization rate (%). | 1,835 nulls (0.08%). ⚠ Already a **numeric float** here (no `%` suffix). | accepted file |
| `total_acc` | float64 | Total number of credit lines in the borrower's file. | **62 nulls** = 33 footer + 29 genuine. | accepted file |
| `application_type` | object (string) | Individual vs joint application (`Individual` / `Joint App`). | 33 nulls (0.0%). | accepted file |
| `total_pymnt` | float64 | Payments received to date for the total amount funded. | 33 nulls (0.0%). | accepted file |
| `recoveries` | float64 | Post-charge-off gross recovery. | 33 nulls (0.0%); non-zero mainly on charged-off loans. | accepted file |
| `fico_mid` | float64 | Midpoint FICO used as the single borrower score. **Formula:** `mean(fico_range_low, fico_range_high)`. | Inherits the 33 footer nulls from its parents; basis for `fico_band` and the RULE-01 floor check (≈660). | **derived** |
| `fico_band` | category (ordinal) | FICO tier bucket of `fico_mid`. **Formula (empirical):** bin `fico_mid` → `<660` (below policy floor, RULE-01) · `660–699` · `700–739` · `740–779` · `780+`. | **(empirical)** — cut points are **not yet governed in CLAUDE.md**; governed in CLAUDE.md; 660 floor to be confirmed against the FICO distribution in Day 9. | **derived** |
| `issue_month` | datetime (month start) | Funding month as a real date. **Formula:** `to_datetime(issue_d, format="%b-%Y")` → first-of-month. | Range 2007-06-01 → 2018-12-01; resolves the `issue_d` string-not-date issue. | **derived** |
| `charge_off_flag` | int (0/1) | Loan charged off. **Formula:** `1` if `loan_status` ∈ {`Charged Off`, `Does not meet the credit policy. Status:Charged Off`}. | Includes the **legacy** variant → **269,320** loans. `Default` (40) is excluded (see `default_flag`). | **derived** |
| `resolved_flag` | int (0/1) | Loan reached terminal outcome (denominator for charge-off rate). **Formula:** `1` if `loan_status` ∈ {`Fully Paid`, `Charged Off`, + both legacy `Does not meet…` variants}. | **1,348,059** resolved loans → resolved charge-off rate ≈ **20.0%**. Charge-off rate is computed over resolved loans only. | **derived** |
| `default_flag` | int (0/1) | Loan in `Default` status. **Formula:** `1` if `loan_status == "Default"`. | **40** loans; kept **separate** from `charge_off_flag` per governed definition. | **derived** |
| `manual_review_flag` | int (0/1) | Application routed to manual review. **Formula:** `1` if `dti > 40` **OR** (`grade` ∈ {E,F,G} **AND** `term == 60`). (RULE-02, RULE-03) | Depends on cleaned `dti` (out-of-range flagged) and stripped integer `term`. | **derived** |

---

## Observed-vs-official contradictions

Fields where the data does not match the official definition or the commonly distributed format (⚠ in the table):

1. **`id`** — Official: a unique numeric loan-listing identifier. Observed: `object` dtype and, on the 33 footer rows, the field carries a **text footnote** rather than an ID. `id` has **zero nulls**, so it cannot be used to detect the garbage rows — use null `loan_amnt` instead.
2. **`dti`** — Official: a bounded debt-to-income ratio. Observed: **2,563 values fall below 0 or above 100**, which is impossible for a true ratio. Flagged as `dti_outlier`, retained (not deleted).
3. **`int_rate` and `revol_util`** — The widely distributed LendingClub CSVs store these as `%`-suffixed **strings** (e.g. `13.99%`). In **this** dataset they are already **numeric floats**, so the usual "strip `%`" cleaning step must **not** be applied to them (it is needed only for the rejected file's `Debt-To-Income Ratio`).
4. **`term`** — Values match the official 36/60-month meaning, but are stored as a **leading-space string** (`' 36 months'`) on **2,260,668** rows rather than a clean integer/categorical — strip and cast.
5. **`issue_d`** — Documented as the loan issue month, but stored as a **non-parseable string** (`%b-%Y`), not a date. Derived `issue_month` resolves this.

Genuine missing data beyond the 33 footer rows (not a definition contradiction, but worth noting for cleaning): `annual_inc` (+4), `open_acc` (+29), `total_acc` (+29).
