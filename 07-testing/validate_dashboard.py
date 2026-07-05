"""
validate_dashboard.py - independent UAT evidence for the dashboard KPIs.
Part of the LendingClub Credit Decisioning & Portfolio Insights BA case study.

This is an INDEPENDENT recomputation. It deliberately does NOT import or reuse any
code from 05-data/prepare_data.py - the whole point of UAT is that a second, separate
implementation reproduces the governed numbers. It reads ONLY the sample / aggregate
CSVs in 05-data/samples/ plus 05-data/cleaning-report.txt. It never touches data_raw/.

Each check recomputes a dashboard KPI, compares it to the governed full-data reference
value (from cleaning-report.txt) within a stated tolerance, prints PASS/FAIL, and maps
to a UAT test case. Exit code is 0 only if all HARD checks pass.

pandas + numpy only. Run from the repo root (paths resolve relative to this file):
    python 07-testing/validate_dashboard.py
"""

import os
import sys
import numpy as np
import pandas as pd

# ---------------------------------------------------------------- paths (cwd-independent)
HERE = os.path.dirname(os.path.abspath(__file__))          # 07-testing/
ROOT = os.path.dirname(HERE)                               # repo root
SAMPLES_DIR = os.path.join(ROOT, "05-data", "samples")
REPORT_PATH = os.path.join(ROOT, "05-data", "cleaning-report.txt")
OUT_PATH = os.path.join(HERE, "validation-results.txt")

FICO_BANDS = {"<660", "660-699", "700-739", "740-779", "780+"}

# ---------------------------------------------------------------- output capture
lines = []


def log(line=""):
    print(line)
    lines.append(line)


results = []  # each: dict(uid, desc, expected, actual, tol, status, hard)


def record(uid, desc, expected, actual, tol, status, hard=True):
    results.append(dict(uid=uid, desc=desc, expected=expected, actual=actual,
                        tol=tol, status=status, hard=hard))
    log(f"[{uid}] {desc}")
    log(f"       expected = {expected}")
    log(f"       actual   = {actual}")
    log(f"       tol      = {tol}   -> {status}")
    log("")


def num_check(uid, desc, expected, actual, tol, hard=True):
    status = "PASS" if abs(actual - expected) <= tol else "FAIL"
    record(uid, desc, f"{expected:.6f}", f"{actual:.6f}", f"+/-{tol:g}", status, hard)


def bool_check(uid, desc, expected, actual, ok, hard=True, warn=False):
    if ok:
        status = "PASS"
    else:
        status = "WARN" if warn else "FAIL"
    record(uid, desc, expected, actual, "exact" + (" (warn)" if warn else ""), status, hard)


# ---------------------------------------------------------------- load CSVs
def load_csv(name):
    path = os.path.join(SAMPLES_DIR, name)
    if not os.path.isfile(path):
        sys.exit(f"ERROR: required input not found: {path}")
    return pd.read_csv(path)


def main():
    log("=" * 78)
    log("DASHBOARD KPI VALIDATION - independent recomputation from 05-data/samples/")
    log("(does not import prepare_data.py; reference values from cleaning-report.txt)")
    log("=" * 78)
    log("")

    funnel = load_csv("monthly_funnel.csv")
    dti = load_csv("dti_comparison.csv")
    state = load_csv("state_summary.csv")
    acc = load_csv("accepted_sample.csv")

    # ============================================== 1. TC-04 approval rate (full-data agg)
    approval = funnel["n_accepted"].sum() / funnel["applications"].sum()
    num_check("TC-04", "Overall approval rate = Sn_accepted / Sapplications (monthly_funnel)",
              0.075584, float(approval), 0.0001, hard=True)

    # ============================================== 2. TC-07 state_summary sanity
    n_states = len(state)
    appr_min = float(state["approval_rate"].min())
    appr_max = float(state["approval_rate"].max())
    funded_nulls = int(state["funded_amnt"].isna().sum())
    ok7 = (n_states == 51) and (appr_min >= 0.02) and (appr_max <= 0.12) and (funded_nulls == 0)
    bool_check("TC-07",
               "state_summary: 51 rows; approval_rate in [0.02,0.12]; no null funded_amnt",
               "51 rows; appr in [0.02,0.12]; funded_amnt non-null",
               f"{n_states} rows; appr in [{appr_min:.4f},{appr_max:.4f}]; funded nulls={funded_nulls}",
               ok7, hard=True)

    # ============================================== 3. TC-06 dti_comparison structure + tail
    n_rows = len(dti)
    rej_60 = int(dti[(dti["population"] == "rejected") & (dti["dti_bucket"] == "60+")]["count"].sum())
    ok6_hard = (n_rows == 26) and (rej_60 == 3_108_473)
    bool_check("TC-06",
               "dti_comparison: 26 rows (13 buckets x 2 pops); rejected '60+' = 3,108,473",
               "26 rows; rejected 60+ = 3,108,473",
               f"{n_rows} rows; rejected 60+ = {rej_60:,}",
               ok6_hard, hard=True)

    # TC-06 accepted-total: WARN, not FAIL (user wants to see the real number regardless)
    acc_dti_total = int(dti[dti["population"] == "accepted"]["count"].sum())
    ok6_acc = (acc_dti_total == 2_258_955)
    bool_check("TC-06",
               "dti_comparison: accepted bucketed count total (valid dti)",
               "accepted total = 2,258,955",
               f"accepted total = {acc_dti_total:,}",
               ok6_acc, hard=False, warn=True)

    # ============================================== 4. TC-03 charge-off rate (resolved basis)
    resolved_sum = int(acc["resolved_flag"].sum())
    co_resolved = int(acc.loc[acc["resolved_flag"] == 1, "charge_off_flag"].sum())
    co_rate = co_resolved / resolved_sum
    num_check("TC-03", "Charge-off rate (resolved basis) from accepted_sample",
              0.199784, float(co_rate), 0.005, hard=True)

    # ============================================== 5. TC-05 CO rate | grade EFG AND term==60
    seg = acc["grade"].isin(["E", "F", "G"]) & (acc["term"] == 60)
    seg_resolved = int(acc.loc[seg, "resolved_flag"].sum())
    seg_co = int(acc.loc[seg & (acc["resolved_flag"] == 1), "charge_off_flag"].sum())
    seg_rate = seg_co / seg_resolved if seg_resolved else float("nan")
    num_check("TC-05", f"Pooled CO rate | grade in EFG AND term==60 (resolved n={seg_resolved:,})",
              0.442168, float(seg_rate), 0.02, hard=True)

    # ============================================== 6. TC-11 manual_review_flag share
    manual_share = float(acc["manual_review_flag"].mean())
    num_check("TC-11", "manual_review_flag mean (share of funded book)",
              0.067696, manual_share, 0.005, hard=True)

    # ============================================== 7. SANITY: bands / years / loan_amnt
    band_set = set(acc["fico_band"].dropna().unique())
    yr_min = int(acc["issue_year"].min())
    yr_max = int(acc["issue_year"].max())
    yrs_in_range = bool(acc["issue_year"].between(2007, 2018).all())
    loan_nulls = int(acc["loan_amnt"].isna().sum())
    ok_sanity = (band_set == FICO_BANDS) and (yr_min == 2007) and (yr_max == 2018) \
        and yrs_in_range and (loan_nulls == 0)
    bool_check("SANITY",
               "fico_band set exact; issue_year spans 2007..2018; no null loan_amnt",
               "bands={<660,660-699,700-739,740-779,780+}; years 2007..2018; loan_amnt nulls=0",
               f"bands={sorted(band_set)}; years {yr_min}..{yr_max}; loan_amnt nulls={loan_nulls}",
               ok_sanity, hard=True)

    # ============================================== 8. TC-10 cleaning-report parity string
    report_ok = os.path.isfile(REPORT_PATH)
    has_string = False
    if report_ok:
        with open(REPORT_PATH, "r", encoding="utf-8") as fh:
            has_string = "269,320" in fh.read()
    ok10 = report_ok and has_string
    bool_check("TC-10",
               "cleaning-report.txt exists and contains flag-sum '269,320'",
               "file exists; contains '269,320'",
               f"exists={report_ok}; contains_269320={has_string}",
               ok10, hard=True)

    # ============================================== results table
    log("=" * 78)
    log("RESULTS TABLE")
    log("=" * 78)
    hdr = f"| {'UAT':<7} | {'Check':<44} | {'Expected':<12} | {'Actual':<12} | {'Tol':<9} | {'Result':<6} |"
    sep = "|" + "-" * 9 + "|" + "-" * 46 + "|" + "-" * 14 + "|" + "-" * 14 + "|" + "-" * 11 + "|" + "-" * 8 + "|"
    log(hdr)
    log(sep)
    for r in results:
        desc = r["desc"] if len(r["desc"]) <= 44 else r["desc"][:41] + "..."
        exp = r["expected"] if len(r["expected"]) <= 12 else r["expected"][:12]
        act = r["actual"] if len(r["actual"]) <= 12 else r["actual"][:12]
        tol = r["tol"] if len(r["tol"]) <= 9 else r["tol"][:9]
        log(f"| {r['uid']:<7} | {desc:<44} | {exp:<12} | {act:<12} | {tol:<9} | {r['status']:<6} |")
    log(sep)

    hard = [r for r in results if r["hard"]]
    hard_pass = [r for r in hard if r["status"] == "PASS"]
    warns = [r for r in results if r["status"] == "WARN"]
    fails = [r for r in hard if r["status"] == "FAIL"]
    log("")
    log(f"HARD CHECKS: {len(hard_pass)}/{len(hard)} passed"
        + (f"   WARNINGS: {len(warns)}" if warns else "")
        + (f"   FAILURES: {len(fails)}" if fails else ""))
    all_ok = len(fails) == 0
    log(f"OVERALL: {'ALL HARD CHECKS PASS' if all_ok else 'FAILURES PRESENT'}  (exit {0 if all_ok else 1})")
    log("=" * 78)

    with open(OUT_PATH, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print(f"\nWrote {OUT_PATH}")

    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
