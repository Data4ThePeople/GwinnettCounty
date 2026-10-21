# Why did Gwinnett's renter income lag its neighbors?

October 21, 2026. Numbers come from `scripts/12_renter_income.py` (output in
`research/renter-income-output.txt`), using ACS microdata person records for
renter households (`DATASETS.md` section 11) and BLS QCEW pay (section 12).
Dollars are 2024 dollars. The rules were written before the run. Nothing here
has had an independent tie-out yet.

**Check.** In the microdata, Gwinnett's renter median rose 6.8% (plus or
minus 2.9), close to the 8.3% from the published table.

## The short version

Two things, both about income rather than who lives there.
- **Pay.** Full-time, year-round renter workers living in Gwinnett earned 3%
  less after inflation in 2020-24 than in 2005-09. In Cobb they earned 7%
  more. Jobs located in Gwinnett had the smallest rise in average pay of the
  eight counties.
- **A smaller shift toward higher-earning households.** Renter households
  everywhere shifted toward more workers, older householders and more college
  degrees, which raised incomes. That shift was smaller in Gwinnett than in
  Fulton, DeKalb, Cherokee and Henry.

Gwinnett's renters did not lose workers, and the county did not fill up with
lower-earning kinds of households.

## R1. The mix of renter households

**Rule.** Reweight Gwinnett's 2020-24 renter households to the 2005-09 mix of
households by workers (0, 1, 2+), householder age and householder education.
If that raises Gwinnett's growth by 3.75 points or more, the mix is a main
factor.

**Result: not a factor by the rule.** Reweighting lowers growth, from +6.8% to
-2.8%. The mix moved toward higher-earning households, not lower.

**Found after the rule was set.** The shift helped every county, but by
different amounts. The "mix effect" below is how much of each county's growth
came from the shift:

| County | Income change | Same mix as 2005-09 | Mix effect |
|---|---|---|---|
| Fulton | +24.3% | +2.7% | +21.6 pts |
| Cherokee | +14.6% | 0.0% | +14.6 pts |
| DeKalb | +11.0% | -2.8% | +13.8 pts |
| Henry | +1.6% | -10.0% | +11.6 pts |
| Cobb | +17.7% | +7.9% | +9.8 pts |
| Gwinnett | +6.8% | -2.8% | +9.5 pts |
| Clayton | -2.6% | -7.6% | +5.0 pts |

- **Against Cobb.** The two had nearly the same mix effect. Gwinnett's lag
  behind Cobb is almost all in income for the same kind of household (-2.8%
  against +7.9%).
- **Against Fulton, DeKalb and Cherokee.** The lag is mostly in the mix.
  Gwinnett's renter householders with a bachelor's degree or more went from
  23% to 30%. That is a smaller rise than in Fulton (34% to 49%), DeKalb (28%
  to 42%), Cherokee (17% to 30%) or Cobb (32% to 41%).

## R2. Workers per household: not a factor

Gwinnett's renter households averaged 1.29 workers in 2005-09 and 1.36 in
2020-24. Cobb's went from 1.27 to 1.34. Every peer rose.

## R3. Pay of renter workers: supported

**Rule.** The change in median earnings of full-time, year-round renter
workers living in Gwinnett is at least 5 points below Cobb's and below the
peer median.

| County | 2005-09 | 2020-24 | Change |
|---|---|---|---|
| Fulton | $49,215 | $59,662 | +21.2% |
| DeKalb | $44,863 | $49,325 | +9.9% |
| Cobb | $49,215 | $52,503 | +6.7% |
| Gwinnett | $46,139 | $44,627 | -3.3% (+/-3.1) |
| Henry | $49,397 | $47,730 | -3.4% |
| Cherokee | $49,688 | $46,702 | -6.0% |
| Clayton | $44,502 | $40,405 | -9.2% |

Gwinnett is 10 points below Cobb, about two standard errors, and below the
peer median of +1.7%. Gwinnett's pay change is not the lowest. Henry, Cherokee
and Clayton also fell, but rents rose less there (Henry, Clayton) or renter
incomes rose more for other reasons (Cherokee).

**Where Gwinnett's renters work.** Fewer worked in construction (19% to 14%),
retail (15% to 12%) and wholesale (5% to 2%). More worked in transportation and
warehousing (4% to 8%) and education and health care (11% to 16%).
Professional and technical work grew less than in Cobb (5% to 8% against 7% to
11%).

## R4. Pay of jobs located in the county: supported

Average annual pay of jobs in Gwinnett (QCEW) rose 1.0% after inflation
between the two periods. That is the smallest rise of the eight counties.
Clayton rose 16.4%, Fulton 15.8%, Cobb 10.3% and the peer median 9.2%. Many
Gwinnett renters work outside the county, and many Gwinnett jobs are held by
people who live elsewhere, so this is context.

## What this cannot show

- **Why pay lagged.** The data show where the lag is, not its cause.
- **The same people.** The microdata are two snapshots of different people,
  not the same renters followed over time.
- **Mix cells.** The reweighting uses three traits. Other traits (field of
  work, English ability, how long people have lived in the U.S.) are not held
  fixed.
- **QCEW** covers jobs in the county, not the jobs residents hold, and
  changes in job mix (such as more warehousing jobs) move the average.
