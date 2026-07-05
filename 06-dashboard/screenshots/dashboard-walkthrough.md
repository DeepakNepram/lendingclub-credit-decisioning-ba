# Dashboard Walkthrough
## LendingClub Credit Decisioning & Portfolio Insights

> Scenario is hypothetical; all data is real LendingClub public data (2007–2018) from Kaggle.

**Live dashboard:** https://public.tableau.com/app/profile/deepak.nepram/viz/LendingClubCreditDecisioningPortfolioInsights
**Author:** Deepak Nepram · **Built with:** Tableau Public (Desktop Edition) · **Data:** outputs of `05-data/prepare_data.py` (RANDOM_SEED = 42)

---

## What this dashboard is for

Three questions, one tab each (FR-014…FR-021):

1. **How big is the book and how healthy is it?** → Tab 1, Executive Overview
2. **What does the approval funnel look like, and do the policy rules hold up?** → Tab 2, Funnel & Policy
3. **Where does credit risk concentrate?** → Tab 3, Portfolio Risk

## Data architecture (why four sources)

The workbook connects **four separate CSVs** rather than one joined table, because they sit at
different grains — joining them would fan out rows and corrupt counts:

| Source | Grain | Basis | Drives |
|---|---|---|---|
| `accepted_sample.csv` | loan (113,565 rows) | stratified sample | BANs (sample-basis), purpose mix, all of Tab 3 |
| `monthly_funnel.csv` | month (140 rows) | **full data** | approval-rate BAN, issuance trend, yearly funnel |
| `dti_comparison.csv` | DTI bucket (26 rows) | **full data** | accepted-vs-rejected comparison |
| `state_summary.csv` | state (51 rows) | **full data** | CR-001 state concentration map |

Headline figures (2.26M loans, 7.6% approval, 20.0% resolved charge-off, 44.2% E–G/60m) are
computed on **full data** in the pipeline and quoted in titles/annotations; the sample only powers
in-tool recomputation. Cards computed on the sample are labelled accordingly (e.g. funded amount).

**Filter scope note (deliberate):** Tableau filters apply per data source. The four global filters
(year, grade, purpose, term) live on `accepted_sample` and drive every Tab 3 view simultaneously
(FR-019, ≤3 clicks). They intentionally do not reach the pre-aggregated full-data sources — Tabs 1–2
are whole-book views; Tab 3 is where you slice.

---

## Tab 1 — Executive Overview

**Layout:** five KPI cards across the top; issuance & approval-rate trend (dual axis, full-data
monthly_funnel); loan mix by purpose.

**How to read it:** the book grew from a niche 2007 platform to ~1M applications/quarter by 2018
while the approval rate tightened toward mid-single digits — growth with discipline, not loosening.
Roughly 1 in 5 resolved loans charged off (20.0%), the headline risk figure the sponsor accepted in
Sprint 1. Debt consolidation + credit card dominate the mix, which frames the portfolio as
refinancing-led.

**Detail:** the approval-rate line is volatile pre-2012 because monthly volumes were tiny
(denominator effect); read the early years as directional.

## Tab 2 — Funnel & Policy

**Layout:** yearly applications vs accepted; DTI distribution accepted-vs-rejected (side-by-side
bars); CR-001 state map.

**How to read it:** ~27.6M applications resolve to 2.26M funded loans (≈7.6% overall). The DTI
comparison is the policy-validation chart — accepted loans concentrate at DTI 10–25 while rejected
applications spread far wider, with a heavy 60+ tail (3.1M applications). That separation is the
empirical support for **RULE-02 (DTI > 40 ⇒ manual review)**: the rejected mass above 40 shows the
screen already binds at application. The comparison uses **DTI, not Risk_Score**, because Risk_Score
is 66.9% null in the rejected file (see data-quality assessment) — an evidence-driven substitution
agreed in MoM-02.

**CR-001 state map:** approval rate by state (3.0%–9.9%), funded volume in tooltip — the
geographic-concentration view Compliance requested mid-Sprint 2, delivered by absorbing US-16 and
deferring US-09 (see change-request log).

## Tab 3 — Portfolio Risk

**Layout:** grade × term charge-off heatmap (headline view); vintage charge-off line; sub-grade
rate-vs-charge-off scatter; four global filters.

**How to read the heatmap:** risk rises monotonically A→G and 36→60 within every grade — from 6.0%
(A/36) to ~50% in the E–G/60 block. That block is **RULE-03**: full-data resolved charge-off of
**44.2% vs the 20.0% portfolio average (2.2×, n = 90,183 resolved loans)** — the single strongest
policy finding in the project and the basis of the closure recommendation.

**Vintage line caveat (important):** the 2007–2008 spike (~30%) is real — crisis-era vintages on tiny
volume. The **decline at 2017–2018 is a survivorship artifact, not improving credit**: those vintages
are young, so only their fast-resolving loans (mostly early payoffs) have resolved; their charge-offs
haven't fully developed. Read the middle vintages (2010–2015) as the steady-state ~15–23% band.

**Scatter:** average interest rate vs charge-off rate by sub-grade forms a tight monotonic band from
A1 (~5% rate, ~3% CO) to G5 (~28%, ~50%) — pricing tracks realized risk, i.e. the grade model is
doing its job; the E–G/60 problem is a term-interaction concentration, not mispricing.

---

## Reproducing this dashboard

1. `python 05-data/prepare_data.py` (needs `data_raw/`; seed 42) → regenerates all four CSVs
2. Connect the four CSVs in Tableau as separate data sources
3. Calculated fields: `Approval Rate % = SUM([n_accepted])/SUM([applications])` (monthly_funnel);
   `Charge-off Rate (resolved) = SUM(IF [resolved_flag]=1 THEN [charge_off_flag] END)/SUM([resolved_flag])`
   (accepted_sample); `Month = DATEPARSE("yyyy-MM",[month])`
4. Formatting conventions: rates stored 0–1 → Percentage format; `int_rate`/`dti` are pre-multiplied →
   Number + "%" suffix; approval rate shown to 1 decimal everywhere

## Known limitations

- Funded-amount and loan-count cards on Tab 1 are sample-basis (labelled); full-data equivalents are
  2,260,668 loans / see cleaning report
- Monthly approval rate is directional (issue-month vs application-month basis mismatch)
- Rejected DTI excludes 1.2M invalid negative values (~4.4%) — documented in the data-quality assessment
- 2017–2018 vintage charge-off is right-censored (survivorship) — do not read as credit improvement
