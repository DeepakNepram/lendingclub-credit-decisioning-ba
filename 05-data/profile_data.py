"""
profile_data.py - LendingClub raw-data profiling
Part of the LendingClub Credit Decisioning & Portfolio Insights BA case study.

Reads the raw ACCEPTED and REJECTED files from data_raw/, profiles them, and
writes 05-data/profiling-notes.md. It does NOT modify the raw files.

Run from the repo root:
    python 05-data/profile_data.py
"""

import glob
import os
import sys
import pandas as pd
import numpy as np

# ---------------------------------------------------------------- config
RAW_DIR = "data_raw"
OUT_DIR = "05-data"
NOTES_PATH = os.path.join(OUT_DIR, "profiling-notes.md")

# The 25 governed fields we want from the accepted file (the script verifies
# each one exists in the header and quietly skips any that are missing).
ACCEPTED_USECOLS = [
    "id", "loan_amnt", "funded_amnt", "term", "int_rate", "installment",
    "grade", "sub_grade", "emp_length", "home_ownership", "annual_inc",
    "verification_status", "issue_d", "loan_status", "purpose", "addr_state",
    "dti", "fico_range_low", "fico_range_high", "open_acc", "revol_util",
    "total_acc", "application_type", "total_pymnt", "recoveries",
]

VALUE_COUNT_COLS = ["term", "grade", "loan_status", "emp_length", "purpose"]


# ---------------------------------------------------------------- helpers
def find_file(patterns):
    """Return the first file in data_raw/ matching any of the glob patterns."""
    for pat in patterns:
        hits = sorted(glob.glob(os.path.join(RAW_DIR, pat)))
        if hits:
            return hits[0]
    return None


def md_table(df):
    """Render a dataframe as a markdown table using only pandas (no tabulate)."""
    df = df.reset_index(drop=True)
    cols = [str(c) for c in df.columns]
    lines = ["| " + " | ".join(cols) + " |",
             "| " + " | ".join("---" for _ in cols) + " |"]
    for _, r in df.iterrows():
        lines.append("| " + " | ".join(str(v) for v in r.values) + " |")
    return "\n".join(lines)


def md_table_transposed(df):
    """Field-per-row markdown table - readable when a row has many columns."""
    df = df.reset_index(drop=True)
    lines = ["| field | " + " | ".join(f"row{i+1}" for i in range(len(df))) + " |",
             "| --- | " + " | ".join("---" for _ in range(len(df))) + " |"]
    for c in df.columns:
        vals = " | ".join(str(v) for v in df[c].tolist())
        lines.append(f"| {c} | {vals} |")
    return "\n".join(lines)


def null_pct_table(df):
    """Null count and percentage per column, as a markdown table."""
    n = len(df)
    out = pd.DataFrame({
        "column": df.columns,
        "dtype": [str(t) for t in df.dtypes],
        "nulls": [int(df[c].isna().sum()) for c in df.columns],
    })
    out["null_%"] = (out["nulls"] / n * 100).round(2)
    return md_table(out)


# ---------------------------------------------------------------- main
def main():
    if not os.path.isdir(RAW_DIR):
        sys.exit(f"ERROR: '{RAW_DIR}/' not found. Run this from the repo root "
                 f"(the folder that contains data_raw/ and 05-data/).")
    os.makedirs(OUT_DIR, exist_ok=True)

    accepted_path = find_file(["*accept*.csv.gz", "*accept*.csv"])
    rejected_path = find_file(["*reject*.csv.gz", "*reject*.csv"])

    print("Files found in data_raw/:")
    for f in sorted(glob.glob(os.path.join(RAW_DIR, "*"))):
        print("   ", os.path.basename(f))
    print(f"\n  accepted -> {accepted_path}")
    print(f"  rejected -> {rejected_path}\n")

    if accepted_path is None or rejected_path is None:
        sys.exit("ERROR: could not locate both an accepted and a rejected file "
                 "in data_raw/. Check the filenames above.")

    md = []  # we accumulate the report here, line by line
    md.append("# Profiling notes - LendingClub raw data\n")
    md.append(f"- Accepted file: `{os.path.basename(accepted_path)}`")
    md.append(f"- Rejected file: `{os.path.basename(rejected_path)}`\n")

    flags = []  # data-quality candidates collected across both files

    # ================================================== ACCEPTED file
    print("Reading ACCEPTED file (this loads ~2.26M rows, give it a minute)...")
    header = pd.read_csv(accepted_path, nrows=0, low_memory=False)
    available = [c for c in ACCEPTED_USECOLS if c in header.columns]
    missing = [c for c in ACCEPTED_USECOLS if c not in header.columns]
    if missing:
        print(f"  NOTE: requested columns not in file (skipped): {missing}")

    acc = pd.read_csv(accepted_path, usecols=available, low_memory=False)
    print(f"  accepted rows: {len(acc):,}  cols: {acc.shape[1]}")

    md.append("## Accepted file\n")
    md.append(f"- Rows: **{len(acc):,}**, columns loaded: **{acc.shape[1]}** "
              f"(of {len(ACCEPTED_USECOLS)} requested)")
    if missing:
        md.append(f"- Requested columns NOT present (skipped): "
                  f"`{', '.join(missing)}`")
    md.append("\n### Dtypes and null rates (accepted)\n")
    md.append(null_pct_table(acc))

    # value counts
    md.append("\n### Top value counts (accepted)\n")
    for col in VALUE_COUNT_COLS:
        if col in acc.columns:
            vc = acc[col].value_counts(dropna=False).head(10)
            t = vc.rename_axis(col).reset_index(name="count")
            md.append(f"\n**{col}**\n")
            md.append(md_table(t))

    # issue_d format + range
    if "issue_d" in acc.columns:
        sample_issue = acc["issue_d"].dropna().iloc[0] if acc["issue_d"].notna().any() else "(all null)"
        md.append("\n### issue_d (accepted)\n")
        md.append(f"- Sample raw value: `{sample_issue}`  "
                  f"(string format -> looks like \"{sample_issue}\")")
        # try to parse to get min/max regardless of format
        parsed = pd.to_datetime(acc["issue_d"], format="%b-%Y", errors="coerce")
        if not parsed.notna().any():
            parsed = pd.to_datetime(acc["issue_d"], errors="coerce")
        if parsed.notna().any():
            md.append(f"- Parsed date range: **{parsed.min().date()}** to "
                      f"**{parsed.max().date()}**")

    # sample rows
    md.append("\n### 3 sample rows (accepted, transposed for readability)\n")
    md.append(md_table_transposed(acc.head(3)))

    # ---- data-quality flags (accepted)
    if "id" in acc.columns:
        n = int(acc["id"].isna().sum())
        flags.append(f"Accepted rows with null `id`: **{n:,}**")
    if "loan_amnt" in acc.columns:
        n = int(acc["loan_amnt"].isna().sum())
        flags.append(f"Accepted rows with null `loan_amnt`: **{n:,}**")
    if "term" in acc.columns:
        s = acc["term"].dropna().astype(str)
        n = int((s != s.str.strip()).sum())
        flags.append(f"`term` values with leading/trailing spaces: **{n:,}** "
                     f"(e.g. {acc['term'].dropna().iloc[0]!r})")
    if "dti" in acc.columns:
        n = int(((acc["dti"] < 0) | (acc["dti"] > 100)).sum())
        flags.append(f"`dti` values <0 or >100: **{n:,}**")
    if "loan_status" in acc.columns:
        mask = acc["loan_status"].astype(str).str.startswith("Does not meet the credit policy")
        n = int(mask.sum())
        flags.append(f"`loan_status` starting with 'Does not meet the credit "
                     f"policy': **{n:,}**")
    # '%' characters in any string column
    pct_cols = []
    for c in acc.select_dtypes(include="object").columns:
        if acc[c].astype(str).str.contains("%", regex=False, na=False).any():
            pct_cols.append(c)
    if pct_cols:
        flags.append(f"Accepted string columns containing a '%' character: "
                     f"`{', '.join(pct_cols)}`")
    else:
        flags.append("No accepted string column contains a '%' character "
                     "(int_rate/revol_util already numeric in this dataset).")

    # ================================================== REJECTED file
    print("\nReading REJECTED file in 1M-row chunks (27M rows, be patient)...")
    rej_total = 0
    rej_null = None
    rej_dtypes = None
    rej_cols = None
    rej_head = None
    date_col = None
    date_min = None
    date_max = None
    sample_date_val = None
    pct_string_cols = set()

    reader = pd.read_csv(rejected_path, chunksize=1_000_000, low_memory=False)
    for i, chunk in enumerate(reader):
        if rej_cols is None:
            rej_cols = list(chunk.columns)
            rej_dtypes = chunk.dtypes
            rej_null = chunk.isna().sum()
            rej_head = chunk.head(3).copy()
            # find a date-like column
            for c in chunk.columns:
                if "date" in c.lower():
                    date_col = c
                    break
        else:
            rej_null = rej_null.add(chunk.isna().sum(), fill_value=0)

        rej_total += len(chunk)

        if date_col is not None:
            d = pd.to_datetime(chunk[date_col], errors="coerce")
            if d.notna().any():
                cmin, cmax = d.min(), d.max()
                date_min = cmin if date_min is None else min(date_min, cmin)
                date_max = cmax if date_max is None else max(date_max, cmax)
                if sample_date_val is None:
                    sample_date_val = chunk[date_col].dropna().iloc[0]

        for c in chunk.select_dtypes(include="object").columns:
            if chunk[c].astype(str).str.contains("%", regex=False, na=False).any():
                pct_string_cols.add(c)

        print(f"  ...chunk {i + 1}: cumulative rows {rej_total:,}")

    md.append("\n## Rejected file\n")
    md.append(f"- Rows: **{rej_total:,}**")
    md.append(f"- Exact column names (verbatim): `{rej_cols}`")
    md.append("\n### Dtypes and null counts (rejected)\n")
    rej_summary = pd.DataFrame({
        "column": rej_cols,
        "dtype": [str(rej_dtypes[c]) for c in rej_cols],
        "nulls": [int(rej_null[c]) for c in rej_cols],
    })
    rej_summary["null_%"] = (rej_summary["nulls"] / rej_total * 100).round(2)
    md.append(md_table(rej_summary))

    if date_col is not None:
        md.append("\n### Application date (rejected)\n")
        md.append(f"- Date column: `{date_col}`")
        md.append(f"- Sample raw value: `{sample_date_val}`")
        if date_min is not None:
            md.append(f"- Parsed range: **{date_min.date()}** to **{date_max.date()}**")
    if pct_string_cols:
        flags.append(f"Rejected string columns containing a '%' character: "
                     f"`{', '.join(sorted(pct_string_cols))}` "
                     f"(DTI is typically stored as a '%' string here).")

    md.append("\n### 3 sample rows (rejected)\n")
    md.append(md_table(rej_head))

    # ================================================== flags section
    md.append("\n## Data-quality candidates\n")
    for f in flags:
        md.append(f"- {f}")

    # ================================================== write report
    with open(NOTES_PATH, "w", encoding="utf-8") as fh:
        fh.write("\n".join(md) + "\n")
    print(f"\nWrote {NOTES_PATH}")

    # ================================================== 5 key findings
    print("\n" + "=" * 60)
    print("FIVE MOST IMPORTANT FINDINGS")
    print("=" * 60)
    findings = []
    findings.append(f"Accepted: {len(acc):,} rows x {acc.shape[1]} cols loaded.")
    findings.append(f"Rejected: {rej_total:,} rows x {len(rej_cols)} cols.")
    if "issue_d" in acc.columns and acc['issue_d'].notna().any():
        findings.append(f"Accepted issue_d sample format: "
                        f"{acc['issue_d'].dropna().iloc[0]!r}")
    if date_col is not None and sample_date_val is not None:
        findings.append(f"Rejected date col '{date_col}' sample: {sample_date_val!r}")
    findings.append(f"{len(flags)} data-quality items flagged - see {NOTES_PATH}")
    for i, f in enumerate(findings, 1):
        print(f"{i}. {f}")


if __name__ == "__main__":
    main()
