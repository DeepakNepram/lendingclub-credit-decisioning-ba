# Sprint 1 — Standup log

### Standup — Day 3
- **Yesterday:** profiled both raw files; confirmed `issue_d` is a `%b-%Y` string and captured the
  rejected file's verbatim column names; rejected-file chunked ingest working.
- **Today:** cleaning rules and derived fields (term strip, emp_length ordinal, charge_off_flag).
- **Blocker:** 33 footer rows have null `loan_amnt` but a non-null `id` — adjusting the drop rule to
  key on `loan_amnt`, not `id`.

### Standup — Day 7
- **Yesterday:** derived fields done; `charge_off_flag` sums to 269,320 and `resolved_flag` to
  1,348,059 (validated against the loan_status counts).
- **Today:** wiring the stratified sample into the KPI dictionary and the Executive Overview v1.
- **Blocker:** none; on track to close all 28 points.
