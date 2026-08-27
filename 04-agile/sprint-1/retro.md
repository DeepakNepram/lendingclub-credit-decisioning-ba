# Sprint 1 — Retrospective

**Start**
- Validating each derived field with a one-line assert (e.g. the `charge_off_flag` sum) before moving on.
- Recording exact row-in / row-out counts in the script output for the data-quality report.
- Committing after each deliverable rather than batching.

**Stop**
- Hand-editing CSVs; all transforms belong in the script.
- Trusting the implementation guide's defaults over the observed data (e.g. the FICO bins, the
  footer-row rule).

**Continue**
- Governing ambiguous definitions in the KPI dictionary as the single source of truth.
- The chunked-read approach for the 27.6M-row rejected file.
- Daily commits with phase-tagged messages.
