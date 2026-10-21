# Did Gwinnett just have a stronger housing market?

October 21, 2026. Numbers come from `scripts/10_values_vs_rents.py` (output
in `research/values-vs-rents-output.txt`). Home prices are measured two ways:
- **ACS median home value.** Owners' own estimate, after inflation.
- **FHFA house price index.** Repeat sales and appraisals; the change
  between the averages of 2005-2009 and 2020-2024, before inflation.

Rent is median gross rent after inflation, the same as in the earlier memos.
The rules below were written before the run. Nothing here has had an
independent tie-out yet.

## The short version

Partly. Gwinnett's home prices rose a lot, and across the country rents rose
more where home prices rose more. But the link is moderate, not tight, and
Gwinnett's rent rose more than its price growth alone would predict. The
clearest difference from its neighbors is renter income, not home prices.

## The rules and the results

| Rule | Result | Met? |
|---|---|---|
| (a) Home price and rent change correlate at 0.5 or more across the 655 counties with 10,000+ renter households | r = 0.60 (ACS), 0.66 (FHFA) | Yes |
| (b) Gwinnett's home price change ranks 5th or better of the 15 large metro counties | 6th (ACS), 3rd (FHFA) | Mixed |
| (c) Gwinnett's rent change is within one standard deviation of what its price change predicts | +1.44 SD above (ACS), +1.02 SD (FHFA) | No, narrowly |

- **How tight.** A correlation of 0.6 to 0.66 means home price change accounts
  for roughly 35% to 45% of the differences in rent change between counties.
  The rest comes from other things.
- **Gwinnett against the national fit.** Given its price growth, Gwinnett's
  rent rose about 9 to 13 points more than the fit predicts. Of 655 large
  counties, 55 (ACS) to 105 (FHFA) sit further above the fit.

## Cobb is the closest comparison

By the FHFA index, Gwinnett (+82.4%), Cobb (+83.3%) and Cherokee (+83.9%) had
nearly the same rise in home prices, the top three in the metro.

| County | FHFA price index | Rent | Renter income |
|---|---|---|---|
| Cherokee | +83.9% | +34.0% | +16.7% |
| Cobb | +83.3% | +27.6% | +18.3% |
| Gwinnett | +82.4% | +31.8% | +8.3% |

Rent rose by similar amounts in all three. Renter income in Gwinnett rose about
half as much as in the other two. Across large counties nationwide, renter
income also tended to rise where home prices rose (r = 0.48 ACS, 0.52 FHFA).
Gwinnett did not follow that pattern.

## What this cannot show

- **Cause.** Home prices and rents can both rise because of the same demand.
  These data show that they move together, not that one pulls the other.
- **Measures.** ACS home values are owners' estimates. The FHFA index covers
  only homes with Fannie Mae or Freddie Mac mortgages, and FHFA calls its
  county index developmental.
