# Data Quality Assessment
## Credit Decisioning & Portfolio Insights

> Scenario is hypothetical; all data is real LendingClub public data (2007–2018) from Kaggle.

## Scope
Assessment of the two raw source files — **accepted** (2,260,701 rows × ~150 cols, 25 governed fields
ingested) and **rejected** (27,648,741 rows × 9 cols) — as profiled (`05-data/profiling-notes.md`) and
cleaned (`05-data/prepare_data.py`, validated in `05-data/cleaning-report.txt`). Every magnitude below
cites those printouts; no figure is asserted from memory.

## Findings

| # | Issue | Field(s) | Magnitude (source) | Decision & rationale | Traces |
|---|---|---|---|---|---|
| 1 | Footer / note rows carrying no loan data | `loan_amnt`, `id` | 33 rows (validation block) | Dropped on **null `loan_amnt`**, not null `id` — the footers carry a non-null `id`, so keying on `id` would miss them | FR-003 |
| 2 | Mixed-type columns warning on load | multiple (accepted) | `DtypeWarning` (profiling) | Read with `low_memory=False` and explicit casts; no silent coercion | FR-001/003 |
| 3 | `term` stored with a leading space (" 36 months") | `term` | ~all accepted rows (profiling) | Whitespace stripped, integer months extracted (36 / 60) | FR-003 |
| 4 | `emp_length` missing values | `emp_length` | 6.50% of cleaned accepted (validation) | Mapped to ordinal 0–10; nulls kept as NaN and excluded from ordinal stats, not imputed | FR-003 |
| 5 | `dti` nulls and out-of-range values | `dti` (accepted) | 0.08% null (~1,711) + 2,563 values < 0 or > 100 (validation / profiling) | Out-of-range values flagged `dti_outlier`, **not deleted** — preserves row counts and surfaces the issue | FR-004 |
| 6 | Legacy "Does not meet the credit policy. Status:…" statuses | `loan_status` | 1,988 Fully Paid + 761 Charged Off legacy (profiling) | Folded into `resolved_flag`; the Charged Off variant into `charge_off_flag`; **"Default" (40) kept separate** as `default_flag` | FR-004 |
| 7 | Rejected `Risk_Score` heavily null | `risk_score` (rejected) | 66.9% null = 18,497,630 rows (profiling) | Accepted-vs-rejected comparison uses **DTI** (present on both sides), not risk score | FR-017, BR-06 |
| 8 | Rejected `dti` negative / invalid after "%" strip | `dti` (rejected) | 1,203,063 rows ≈ 4.35% (validation) | Excluded from the 0–60 comparison buckets as out-of-range; valid-DTI rows still compared | FR-002/017 |
| 9 | Self-reported income extremes | `annual_inc` | qualitative; +4 genuine nulls (profiling) | Income used descriptively; extreme values retained and flagged for awareness, not trimmed | FR-006 |
| 10 | Date-basis mismatch between files | `issue_d` vs `application_date` | structural | Accepted counted by `issue_month`, rejected by `application_month`; monthly approval rate is directional, overall is exact | FR-002/015 |

## Residual risks
- **Monthly approval rate is approximate.** The issue-vs-application date basis means the month-level
  figure should be read as a trend, not a precise monthly rate; the overall 7.56% is exact.
- **Rejected DTI distribution covers valid rows only.** The 4.35% negative/invalid DTI is excluded;
  the comparison describes the ~95.6% with usable values.
- **Risk-score-based policy comparison is not possible** given 66.9% sparsity; DTI is the substitute lens.
- **Dashboard recomputation uses a 113,565-row stratified sample**, so the smallest cells (e.g. grade G)
  carry minor sampling noise. All authoritative figures (rule evidence, headline rates) are computed on
  **full data** in `prepare_data.py`, not the sample.

## Confidence
Cleaning is fully reproducible (single script, `RANDOM_SEED = 42`, pinned to the governed definitions
in `CLAUDE.md`). The three governed flag sums reconcile to the integer against the loan_status counts,
and post-clean null rates reconcile with the pre-clean profile minus the 33 dropped rows — independent
confirmation the pipeline behaved as specified.
