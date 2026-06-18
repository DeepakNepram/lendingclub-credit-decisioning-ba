# Profiling notes - LendingClub raw data

- Accepted file: `accepted_2007_to_2018Q4.csv.gz`
- Rejected file: `rejected_2007_to_2018Q4.csv.gz`

## Accepted file

- Rows: **2,260,701**, columns loaded: **25** (of 25 requested)

### Dtypes and null rates (accepted)

| column | dtype | nulls | null_% |
| --- | --- | --- | --- |
| id | object | 0 | 0.0 |
| loan_amnt | float64 | 33 | 0.0 |
| funded_amnt | float64 | 33 | 0.0 |
| term | object | 33 | 0.0 |
| int_rate | float64 | 33 | 0.0 |
| installment | float64 | 33 | 0.0 |
| grade | object | 33 | 0.0 |
| sub_grade | object | 33 | 0.0 |
| emp_length | object | 146940 | 6.5 |
| home_ownership | object | 33 | 0.0 |
| annual_inc | float64 | 37 | 0.0 |
| verification_status | object | 33 | 0.0 |
| issue_d | object | 33 | 0.0 |
| loan_status | object | 33 | 0.0 |
| purpose | object | 33 | 0.0 |
| addr_state | object | 33 | 0.0 |
| dti | float64 | 1744 | 0.08 |
| fico_range_low | float64 | 33 | 0.0 |
| fico_range_high | float64 | 33 | 0.0 |
| open_acc | float64 | 62 | 0.0 |
| revol_util | float64 | 1835 | 0.08 |
| total_acc | float64 | 62 | 0.0 |
| total_pymnt | float64 | 33 | 0.0 |
| recoveries | float64 | 33 | 0.0 |
| application_type | object | 33 | 0.0 |

### Top value counts (accepted)


**term**

| term | count |
| --- | --- |
|  36 months | 1609754 |
|  60 months | 650914 |
| nan | 33 |

**grade**

| grade | count |
| --- | --- |
| B | 663557 |
| C | 650053 |
| A | 433027 |
| D | 324424 |
| E | 135639 |
| F | 41800 |
| G | 12168 |
| nan | 33 |

**loan_status**

| loan_status | count |
| --- | --- |
| Fully Paid | 1076751 |
| Current | 878317 |
| Charged Off | 268559 |
| Late (31-120 days) | 21467 |
| In Grace Period | 8436 |
| Late (16-30 days) | 4349 |
| Does not meet the credit policy. Status:Fully Paid | 1988 |
| Does not meet the credit policy. Status:Charged Off | 761 |
| Default | 40 |
| nan | 33 |

**emp_length**

| emp_length | count |
| --- | --- |
| 10+ years | 748005 |
| 2 years | 203677 |
| < 1 year | 189988 |
| 3 years | 180753 |
| 1 year | 148403 |
| nan | 146940 |
| 5 years | 139698 |
| 4 years | 136605 |
| 6 years | 102628 |
| 7 years | 92695 |

**purpose**

| purpose | count |
| --- | --- |
| debt_consolidation | 1277877 |
| credit_card | 516971 |
| home_improvement | 150457 |
| other | 139440 |
| major_purchase | 50445 |
| medical | 27488 |
| small_business | 24689 |
| car | 24013 |
| vacation | 15525 |
| moving | 15403 |

### issue_d (accepted)

- Sample raw value: `Dec-2015`  (string format -> looks like "Dec-2015")
- Parsed date range: **2007-06-01** to **2018-12-01**

### 3 sample rows (accepted, transposed for readability)

| field | row1 | row2 | row3 |
| --- | --- | --- | --- |
| id | 68407277 | 68355089 | 68341763 |
| loan_amnt | 3600.0 | 24700.0 | 20000.0 |
| funded_amnt | 3600.0 | 24700.0 | 20000.0 |
| term |  36 months |  36 months |  60 months |
| int_rate | 13.99 | 11.99 | 10.78 |
| installment | 123.03 | 820.28 | 432.66 |
| grade | C | C | B |
| sub_grade | C4 | C1 | B4 |
| emp_length | 10+ years | 10+ years | 10+ years |
| home_ownership | MORTGAGE | MORTGAGE | MORTGAGE |
| annual_inc | 55000.0 | 65000.0 | 63000.0 |
| verification_status | Not Verified | Not Verified | Not Verified |
| issue_d | Dec-2015 | Dec-2015 | Dec-2015 |
| loan_status | Fully Paid | Fully Paid | Fully Paid |
| purpose | debt_consolidation | small_business | home_improvement |
| addr_state | PA | SD | IL |
| dti | 5.91 | 16.06 | 10.78 |
| fico_range_low | 675.0 | 715.0 | 695.0 |
| fico_range_high | 679.0 | 719.0 | 699.0 |
| open_acc | 7.0 | 22.0 | 6.0 |
| revol_util | 29.7 | 19.2 | 56.2 |
| total_acc | 13.0 | 38.0 | 18.0 |
| total_pymnt | 4421.723916800001 | 25679.66 | 22705.9242938784 |
| recoveries | 0.0 | 0.0 | 0.0 |
| application_type | Individual | Individual | Joint App |

## Rejected file

- Rows: **27,648,741**
- Exact column names (verbatim): `['Amount Requested', 'Application Date', 'Loan Title', 'Risk_Score', 'Debt-To-Income Ratio', 'Zip Code', 'State', 'Employment Length', 'Policy Code']`

### Dtypes and null counts (rejected)

| column | dtype | nulls | null_% |
| --- | --- | --- | --- |
| Amount Requested | float64 | 0 | 0.0 |
| Application Date | object | 0 | 0.0 |
| Loan Title | object | 1305 | 0.0 |
| Risk_Score | float64 | 18497630 | 66.9 |
| Debt-To-Income Ratio | object | 0 | 0.0 |
| Zip Code | object | 293 | 0.0 |
| State | object | 22 | 0.0 |
| Employment Length | object | 951355 | 3.44 |
| Policy Code | float64 | 918 | 0.0 |

### Application date (rejected)

- Date column: `Application Date`
- Sample raw value: `2007-05-26`
- Parsed range: **2007-05-26** to **2018-12-31**

### 3 sample rows (rejected)

| Amount Requested | Application Date | Loan Title | Risk_Score | Debt-To-Income Ratio | Zip Code | State | Employment Length | Policy Code |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1000.0 | 2007-05-26 | Wedding Covered but No Honeymoon | 693.0 | 10% | 481xx | NM | 4 years | 0.0 |
| 1000.0 | 2007-05-26 | Consolidating Debt | 703.0 | 10% | 010xx | MA | < 1 year | 0.0 |
| 11000.0 | 2007-05-27 | Want to consolidate my debt | 715.0 | 10% | 212xx | MD | 1 year | 0.0 |

## Data-quality candidates

- Accepted rows with null `id`: **0**
- Accepted rows with null `loan_amnt`: **33**
- `term` values with leading/trailing spaces: **2,260,668** (e.g. ' 36 months')
- `dti` values <0 or >100: **2,563**
- `loan_status` starting with 'Does not meet the credit policy': **2,749**
- No accepted string column contains a '%' character (int_rate/revol_util already numeric in this dataset).
- Rejected string columns containing a '%' character: `Debt-To-Income Ratio, Loan Title` (DTI is typically stored as a '%' string here).
