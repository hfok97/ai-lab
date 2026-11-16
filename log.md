## 2026-11-16 — Lab inventory and LTC projection scoping

### Done
- Reviewed the repo. It has one commit ("Set up lab folders"), an empty `log.md`, an empty `projects/` folder, and `data/`, which is untracked.
- Identified the two files in `data/` from their SOA metadata:
  - `t2581.xls`: SOA table 2581, 2012 IAM Period Table, **Male** (inferred; the table-name cell wasn't read directly).
  - `t2582.xls`: SOA table 2582, 2012 IAM Period Table, **Female** (inferred).
  - Source: 2000–2004 Individual Payout Annuity study, projected to 2012 with Scale G2, capped at q = 0.400 at the oldest ages.
- Checked tooling: Python 3.15 is installed; pandas and xlrd are not.
- Listed what an LTC projection needs beyond these tables: active-life mortality and improvement (Scale G2, SOA tables 2583/2584), claim incidence, claim termination, benefit utilization, lapse, economic and product assumptions, policy data, and a projection engine.

### Next
- [ ] Decide what the projection is for: pricing, reserves, a rate-increase analysis, or learning.
- [ ] Decide on assumptions: real ones (for example, the SOA LTC Intercompany Experience Study tables) or illustrative placeholders.
- [x] Install pandas, numpy and xlrd.
- [x] Convert t2581/t2582 to clean CSVs in `data/` and confirm male/female. (Committing `data/` is still open.)
- [ ] Build a one-policy LTC model in `projects/ltc/`, then extend it to a block of policies.

## 2026-11-16 — Tooling and table conversion

### Done
- Installed pandas 3.1.1, numpy 2.5.5 and xlrd 2.0.2 (Python 3.15.2).
- Read the table-name cells directly. This **corrects** the earlier entry: the tables are the **2012 IAM Basic** tables (age nearest birthday, ages 0–120), not "Period" tables.
  - `t2581.xls`: 2012 IAM Basic Table – Male, ANB (confirmed).
  - `t2582.xls`: 2012 IAM Basic Table – Female, ANB (confirmed).
  - They are 2012 base rates. Generational mortality would apply Scale G2 (tables 2583/2584) from 2012 onward.
- Added `projects/tools/soa_xls_to_csv.py`. It parses an SOA .xls export, checks that the ages are contiguous and the rates fall in [0, 1], and writes `age,<col>`.
- Wrote `data/iam2012_basic_male_anb.csv` and `data/iam2012_basic_female_anb.csv` (121 rows each, columns `age,qx`).
- Sanity checks: female q is below male q at every age except 0–1. q at 65 is 0.009007 (M) and 0.006829 (F). Rates reach the 0.400 cap at age 105 (M) and 107 (F).

### Next
- [ ] Decide what the projection is for: pricing, reserves, a rate-increase analysis, or learning.
- [ ] Decide on assumptions: real ones (SOA LTC Intercompany Experience Study) or illustrative placeholders.
- [ ] Get Scale G2 (SOA 2583/2584) if generational mortality is needed.
- [ ] Commit `data/`, `projects/tools/` and `log.md`.
- [ ] Build a one-policy LTC model in `projects/ltc/`, then extend it to a block of policies.
