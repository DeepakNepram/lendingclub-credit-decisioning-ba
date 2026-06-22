"""
prepare_data.py - LendingClub data cleaning, governed-field derivation, sampling.
Part of the LendingClub Credit Decisioning & Portfolio Insights BA case study.

Reads the RAW accepted and rejected files from data_raw/ (READ-ONLY - never modified),
cleans them, derives the governed fields, writes samples + aggregates to 05-data/samples/,
prints a validation block, and writes 05-data/cleaning-report.txt (satisfies FR-006).

Governed definitions follow CLAUDE.md exactly. The accepted file fits in memory; the
27.6M-row rejected file is processed in 1M-row chunks and is NEVER held fully in memory.

pandas + numpy only. Run from the repo root:
    python 05-data/prepare_data.py
"""

import glob
import os
import sys
import numpy as np
import pandas as pd

# ---------------------------------------------------------------- config
RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

RAW_DIR = "data_raw"
OUT_DIR = "05-data"
SAMPLES_DIR = os.path.join(OUT_DIR, "samples")
REPORT_PATH = os.path.join(OUT_DIR, "cleaning-report.txt")

CHUNK = 1_000_000
# CLAUDE.md hard rule #2: each file in samples/ must be < 25 MB. We target ~300k rows
# but enforce this cap by down-sampling (keeping stratification) until the CSV fits.
MAX_SAMPLE_BYTES = 24 * 1024 * 1024
ACC_SAMPLE_TARGET = 300_000
REJ_SAMPLE_TARGET = 300_000
# Documented rejected row count (profiling-notes.md) - used only to pick a constant
# sampling fraction for the chunked rejected sample. Actual total is recomputed at runtime.
REJ_REFERENCE_TOTAL = 27_648_741

# The same 25 governed fields used by 05-data/profile_data.py.
ACCEPTED_USECOLS = [
    "id", "loan_amnt", "funded_amnt", "term", "int_rate", "installment",
    "grade", "sub_grade", "emp_length", "home_ownership", "annual_inc",
    "verification_status", "issue_d", "loan_status", "purpose", "addr_state",
    "dti", "fico_range_low", "fico_range_high", "open_acc", "revol_util",
    "total_acc", "application_type", "total_pymnt", "recoveries",
]

# Verbatim rejected headers -> snake_case (exact names verified in profiling-notes.md).
REJECTED_RENAME = {
    "Amount Requested": "amount_requested",
    "Application Date": "application_date",
    "Loan Title": "loan_title",
    "Risk_Score": "risk_score",
    "Debt-To-Income Ratio": "dti",
    "Zip Code": "zip_code",
    "State": "state",
    "Employment Length": "emp_length",
    "Policy Code": "policy_code",
}

# Governed loan_status sets (CLAUDE.md).
CHARGE_OFF_STATUSES = {
    "Charged Off",
    "Does not meet the credit policy. Status:Charged Off",
}
RESOLVED_STATUSES = {
    "Fully Paid",
    "Charged Off",
    "Does not meet the credit policy. Status:Fully Paid",
    "Does not meet the credit policy. Status:Charged Off",
}

EMP_LENGTH_MAP = {
    "< 1 year": 0, "1 year": 1, "2 years": 2, "3 years": 3, "4 years": 4,
    "5 years": 5, "6 years": 6, "7 years": 7, "8 years": 8, "9 years": 9,
    "10+ years": 10,
}

# fico_band: GOVERNED 660-based bins (NOT 640-based). right=False so 660 -> "660-699".
FICO_BINS = [-np.inf, 660, 700, 740, 780, np.inf]
FICO_LABELS = ["<660", "660-699", "700-739", "740-779", "780+"]

# dti_comparison: 5-point bins 0-60, plus a "60+" overflow so the tail is not lost.
DTI_BINS = [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, np.inf]
DTI_LABELS = ["0-5", "5-10", "10-15", "15-20", "20-25", "25-30", "30-35",
              "35-40", "40-45", "45-50", "50-55", "55-60", "60+"]


# ---------------------------------------------------------------- helpers
report_lines = []


def emit(line=""):
    """Print to console AND capture for cleaning-report.txt."""
    print(line)
    report_lines.append(line)


def find_file(patterns):
    """First *file* (not directory) in data_raw/ matching any glob pattern."""
    for pat in patterns:
        for hit in sorted(glob.glob(os.path.join(RAW_DIR, pat))):
            if os.path.isfile(hit):
                return hit
    return None


def acc_series(running, new):
    """Accumulate value_counts across chunks (index-aligned add)."""
    return new if running is None else running.add(new, fill_value=0)


def stratified_sample(df, col, frac, seed):
    """Proportional-stratified sample: same fraction drawn within each stratum."""
    if frac >= 1:
        return df
    if col is not None and col in df.columns and df[col].notna().any():
        return df.groupby(col, group_keys=False).sample(frac=frac, random_state=seed)
    return df.sample(frac=frac, random_state=seed)


def write_capped_sample(df, path, target_rows, stratify_col, seed):
    """Write df sampled to ~target_rows, then shrink until the CSV is < 25 MB."""
    n = len(df)
    samp = stratified_sample(df, stratify_col, target_rows / n, seed) if n > target_rows else df
    samp.to_csv(path, index=False)
    while os.path.getsize(path) > MAX_SAMPLE_BYTES and len(samp) > 2000:
        # shrink toward the cap with a little headroom, preserving stratification
        frac = (MAX_SAMPLE_BYTES / os.path.getsize(path)) * 0.95
        samp = stratified_sample(samp, stratify_col, frac, seed)
        samp.to_csv(path, index=False)
    return len(samp), os.path.getsize(path)


def null_pct(series):
    return float(series.isna().mean() * 100)


# ---------------------------------------------------------------- accepted
def clean_accepted(path):
    header = pd.read_csv(path, nrows=0, low_memory=False)
    available = [c for c in ACCEPTED_USECOLS if c in header.columns]
    missing = [c for c in ACCEPTED_USECOLS if c not in header.columns]
    if missing:
        emit(f"  WARNING: requested accepted columns missing from header (skipped): {missing}")

    df = pd.read_csv(path, usecols=available, low_memory=False)
    rows_in = len(df)

    # Drop the 33 footer/garbage rows: keyed on null loan_amnt (their id is NON-null).
    df = df[df["loan_amnt"].notna()].copy()
    rows_out = len(df)
    dropped = rows_in - rows_out

    # term: strip whitespace, extract integer months (36 / 60)
    term_num = df["term"].astype(str).str.strip().str.extract(r"(\d+)")[0]
    df["term"] = pd.to_numeric(term_num, errors="coerce").astype("Int64")

    # emp_length: ordinal 0..10, null -> NaN
    df["emp_length"] = df["emp_length"].map(EMP_LENGTH_MAP).astype("Int64")

    # issue_d: parse "%b-%Y" -> issue_month "YYYY-MM" and issue_year (int)
    issue_dt = pd.to_datetime(df["issue_d"], format="%b-%Y", errors="coerce")
    df["issue_month"] = issue_dt.dt.strftime("%Y-%m")
    df["issue_year"] = issue_dt.dt.year.astype("Int64")

    # fico_mid + governed fico_band
    df["fico_mid"] = df[["fico_range_low", "fico_range_high"]].mean(axis=1)
    df["fico_band"] = pd.cut(df["fico_mid"], bins=FICO_BINS, labels=FICO_LABELS, right=False)

    # governed flags
    ls = df["loan_status"]
    df["charge_off_flag"] = ls.isin(CHARGE_OFF_STATUSES).astype(int)
    df["default_flag"] = (ls == "Default").astype(int)
    df["resolved_flag"] = ls.isin(RESOLVED_STATUSES).astype(int)

    # manual_review_flag = (dti > 40) OR (grade in {E,F,G} AND term == 60)   RULE-02, RULE-03
    cond_dti = (df["dti"] > 40).fillna(False)
    cond_term = (df["term"] == 60).fillna(False)
    cond_grade = df["grade"].isin(["E", "F", "G"])
    df["manual_review_flag"] = (cond_dti | (cond_grade & cond_term)).astype(int)

    # dti_outlier: flag (do NOT delete)
    df["dti_outlier"] = (((df["dti"] < 0) | (df["dti"] > 100)).fillna(False)).astype(int)

    return df, rows_in, dropped, rows_out


# ---------------------------------------------------------------- rejected (chunked)
def process_rejected(path):
    frac = min(1.0, REJ_SAMPLE_TARGET / REJ_REFERENCE_TOTAL)
    rej_total = 0
    month_counts = None        # n_rejected per application_month
    state_counts = None        # rejected applications per state
    dti_bucket_counts = None   # rejected dti distribution
    year_counts = None         # for reporting
    date_unparsed = 0
    dti_null = 0
    dti_excluded = 0           # null + out-of-[0, inf) -> not bucketed
    sample_parts = []

    reader = pd.read_csv(path, chunksize=CHUNK, low_memory=False)
    for i, chunk in enumerate(reader):
        chunk = chunk.rename(columns=REJECTED_RENAME)

        # strip "%" from dti ONLY -> float (loan_title untouched even if it has "%")
        chunk["dti"] = pd.to_numeric(
            chunk["dti"].astype(str).str.replace("%", "", regex=False).str.strip(),
            errors="coerce",
        )

        # application_date: ISO "%Y-%m-%d" -> application_month / application_year
        ad = pd.to_datetime(chunk["application_date"], format="%Y-%m-%d", errors="coerce")
        chunk["application_month"] = ad.dt.strftime("%Y-%m")
        chunk["application_year"] = ad.dt.year.astype("Int64")

        rej_total += len(chunk)
        date_unparsed += int(ad.isna().sum())
        dti_null += int(chunk["dti"].isna().sum())

        month_counts = acc_series(month_counts, chunk["application_month"].value_counts(dropna=True))
        state_counts = acc_series(state_counts, chunk["state"].value_counts(dropna=True))
        year_counts = acc_series(year_counts, chunk["application_year"].value_counts(dropna=True))

        buckets = pd.cut(chunk["dti"], bins=DTI_BINS, labels=DTI_LABELS, right=False)
        dti_excluded += int(buckets.isna().sum())
        dti_bucket_counts = acc_series(dti_bucket_counts, buckets.value_counts())

        sample_parts.append(chunk.sample(frac=frac, random_state=RANDOM_SEED + i)
                            if frac < 1 else chunk)

        print(f"  ...rejected chunk {i + 1}: cumulative rows {rej_total:,}")

    rej_sample = pd.concat(sample_parts, ignore_index=True)
    return {
        "total": rej_total,
        "month_counts": month_counts,
        "state_counts": state_counts,
        "dti_bucket_counts": dti_bucket_counts,
        "year_counts": year_counts,
        "date_unparsed": date_unparsed,
        "dti_null": dti_null,
        "dti_excluded": dti_excluded,
        "sample": rej_sample,
        "sample_frac": frac,
    }


# ---------------------------------------------------------------- main
def main():
    if not os.path.isdir(RAW_DIR):
        sys.exit(f"ERROR: '{RAW_DIR}/' not found. Run from the repo root.")
    os.makedirs(SAMPLES_DIR, exist_ok=True)

    accepted_path = find_file(["*accept*.csv.gz", "*accept*.csv"])
    rejected_path = find_file(["*reject*.csv.gz", "*reject*.csv"])
    if accepted_path is None or rejected_path is None:
        sys.exit("ERROR: could not locate both an accepted and a rejected file in data_raw/.")
    print(f"accepted -> {accepted_path}")
    print(f"rejected -> {rejected_path}\n")

    # ---- accepted
    print("Cleaning ACCEPTED file (~2.26M rows)...")
    acc, acc_rows_in, acc_dropped, acc_rows_out = clean_accepted(accepted_path)
    print(f"  accepted: in={acc_rows_in:,}  dropped={acc_dropped:,}  out={acc_rows_out:,}\n")

    # ---- rejected (chunked, never fully in memory)
    print("Processing REJECTED file in 1M-row chunks (27.6M rows)...")
    rej = process_rejected(rejected_path)
    print(f"  rejected total rows: {rej['total']:,}\n")

    # ================================================== aggregates (FULL data)
    # 3. monthly_funnel
    acc_month = acc.groupby("issue_month").size().rename("n_accepted")
    rej_month = rej["month_counts"].rename("n_rejected")
    rej_month.index = rej_month.index.astype(str)
    funnel = pd.concat([acc_month, rej_month], axis=1).fillna(0)
    funnel[["n_accepted", "n_rejected"]] = funnel[["n_accepted", "n_rejected"]].astype("int64")
    funnel.index.name = "month"
    funnel = funnel.reset_index()
    funnel["applications"] = funnel["n_accepted"] + funnel["n_rejected"]
    funnel["approval_rate"] = funnel["n_accepted"] / funnel["applications"]
    funnel = funnel.sort_values("month")[
        ["month", "n_accepted", "n_rejected", "applications", "approval_rate"]
    ]

    # 4. dti_comparison (population x dti_bucket x count)
    acc_buckets = pd.cut(acc["dti"], bins=DTI_BINS, labels=DTI_LABELS, right=False).value_counts()
    rej_buckets = rej["dti_bucket_counts"]
    rows = []
    for pop, counts in (("accepted", acc_buckets), ("rejected", rej_buckets)):
        for label in DTI_LABELS:
            rows.append((pop, label, int(counts.get(label, 0))))
    dti_comparison = pd.DataFrame(rows, columns=["population", "dti_bucket", "count"])

    # 5. state_summary
    acc_state = acc.groupby("addr_state").agg(
        accepted=("loan_amnt", "size"),
        funded_amnt=("funded_amnt", "sum"),
    )
    acc_state.index.name = "state"
    rej_state = rej["state_counts"].rename("rejected")
    rej_state.index.name = "state"
    state = acc_state.join(rej_state, how="outer")
    state[["accepted", "funded_amnt", "rejected"]] = (
        state[["accepted", "funded_amnt", "rejected"]].fillna(0)
    )
    state["accepted"] = state["accepted"].astype("int64")
    state["rejected"] = state["rejected"].astype("int64")
    state = state.reset_index()
    state["applications"] = state["accepted"] + state["rejected"]
    state["approval_rate"] = state["accepted"] / state["applications"]
    state = state.sort_values("applications", ascending=False)[
        ["state", "applications", "accepted", "approval_rate", "funded_amnt"]
    ]

    # ================================================== write outputs
    funnel.to_csv(os.path.join(SAMPLES_DIR, "monthly_funnel.csv"), index=False)
    dti_comparison.to_csv(os.path.join(SAMPLES_DIR, "dti_comparison.csv"), index=False)
    state.to_csv(os.path.join(SAMPLES_DIR, "state_summary.csv"), index=False)

    acc_sample_rows, acc_sample_bytes = write_capped_sample(
        acc, os.path.join(SAMPLES_DIR, "accepted_sample.csv"),
        ACC_SAMPLE_TARGET, "issue_year", RANDOM_SEED,
    )
    rej_sample_rows, rej_sample_bytes = write_capped_sample(
        rej["sample"], os.path.join(SAMPLES_DIR, "rejected_sample.csv"),
        REJ_SAMPLE_TARGET, "application_year", RANDOM_SEED,
    )

    outputs = [
        ("accepted_sample.csv", acc_sample_rows, acc_sample_bytes),
        ("rejected_sample.csv", rej_sample_rows, rej_sample_bytes),
        ("monthly_funnel.csv", len(funnel), os.path.getsize(os.path.join(SAMPLES_DIR, "monthly_funnel.csv"))),
        ("dti_comparison.csv", len(dti_comparison), os.path.getsize(os.path.join(SAMPLES_DIR, "dti_comparison.csv"))),
        ("state_summary.csv", len(state), os.path.getsize(os.path.join(SAMPLES_DIR, "state_summary.csv"))),
    ]

    # ================================================== computed validation numbers
    co_sum = int(acc["charge_off_flag"].sum())
    resolved_sum = int(acc["resolved_flag"].sum())
    default_sum = int(acc["default_flag"].sum())
    applications_total = acc_rows_out + rej["total"]
    approval_rate = acc_rows_out / applications_total
    resolved_mask = acc["resolved_flag"] == 1
    resolved_co_rate = float(acc.loc[resolved_mask, "charge_off_flag"].mean())
    manual_share = float(acc["manual_review_flag"].mean())

    # rule evidence
    fico_low = acc["fico_range_low"]
    r1_min = float(fico_low.min())
    r1_p1 = float(fico_low.quantile(0.01))
    r1_p5 = float(fico_low.quantile(0.05))
    r2_share = float((acc["dti"] > 40).mean())
    efg60 = resolved_mask & acc["grade"].isin(["E", "F", "G"]) & (acc["term"] == 60)
    r3_rate = float(acc.loc[efg60, "charge_off_flag"].mean()) if int(efg60.sum()) else float("nan")
    r4_share = float(((acc["verification_status"] == "Not Verified") & (acc["loan_amnt"] > 20000)).mean())
    sb_mask = resolved_mask & (acc["purpose"] == "small_business")
    r6_rate = float(acc.loc[sb_mask, "charge_off_flag"].mean()) if int(sb_mask.sum()) else float("nan")

    # ================================================== validation block
    emit("")
    emit("=" * 64)
    emit("VALIDATION BLOCK  (LendingClub prepare_data.py)")
    emit(f"RANDOM_SEED = {RANDOM_SEED}")
    emit("=" * 64)

    emit("\n[ROW ACCOUNTING]")
    emit(f"  accepted rows in     : {acc_rows_in:,}")
    emit(f"  accepted rows dropped: {acc_dropped:,}   (null loan_amnt = footer rows)")
    emit(f"  accepted rows out    : {acc_rows_out:,}")
    emit(f"  rejected total rows  : {rej['total']:,}")
    emit(f"  rejected unparsed dates: {rej['date_unparsed']:,}")
    emit(f"  rejected dti null after clean: {rej['dti_null']:,}")
    emit(f"  rejected dti excluded from buckets (null/neg): {rej['dti_excluded']:,}")

    emit("\n[NULL % AFTER CLEANING - accepted key fields]")
    for col in ["loan_amnt", "term", "emp_length", "dti", "fico_mid", "grade", "issue_month", "addr_state"]:
        emit(f"  {col:<14}: {null_pct(acc[col]):.4f}%")

    emit("\n[GOVERNED FLAG SUMS - accepted]")
    emit(f"  charge_off_flag sum : {co_sum:,}      (expect 269,320)")
    emit(f"  resolved_flag   sum : {resolved_sum:,}    (expect 1,348,059)")
    emit(f"  default_flag    sum : {default_sum:,}          (expect 40)")

    emit("\n[PORTFOLIO RATES]")
    emit(f"  overall approval rate (full data)      : {approval_rate:.4%}")
    emit(f"  resolved charge-off rate (CO|resolved) : {resolved_co_rate:.4%}   (expect ~20%)")
    emit(f"  manual_review_flag share of accepted   : {manual_share:.4%}")

    emit("\n[RULE EVIDENCE]")
    emit(f"  RULE-01 fico_range_low: min={r1_min:.0f}  p1={r1_p1:.0f}  p5={r1_p5:.0f}")
    emit(f"  RULE-02 share dti > 40                       : {r2_share:.4%}")
    emit(f"  RULE-03 CO rate | grade in EFG AND term==60  : {r3_rate:.4%}  (n_resolved={int(efg60.sum()):,})")
    emit(f"  RULE-04 share NotVerified AND loan_amnt>20k  : {r4_share:.4%}")
    emit(f"  RULE-06 CO rate | purpose==small_business    : {r6_rate:.4%}  (n_resolved={int(sb_mask.sum()):,})")
    emit(f"          (portfolio resolved CO rate for ref  : {resolved_co_rate:.4%})")

    emit("\n[OUTPUT FILES - 05-data/samples/]")
    emit(f"  rejected sample fraction used: {rej['sample_frac']:.6f}")
    for name, nrows, nbytes in outputs:
        emit(f"  {name:<22}: {nrows:>8,} rows   {nbytes:>12,} bytes  ({nbytes / 1024 / 1024:6.2f} MB)")
    emit(f"  (CLAUDE.md cap enforced: each file < {MAX_SAMPLE_BYTES / 1024 / 1024:.0f} MB)")
    emit("=" * 64)

    with open(REPORT_PATH, "w", encoding="utf-8") as fh:
        fh.write("\n".join(report_lines) + "\n")
    print(f"\nWrote {REPORT_PATH}")


if __name__ == "__main__":
    main()
