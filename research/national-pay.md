# Gwinnett's renter pay against large-metro counties where rent rose fast

October 21, 2026. Numbers come from `scripts/15_national_pay.py` (output in
`research/national-pay-output.txt`), using ACS microdata for full-time
year-round workers in renter households in every state (`DATASETS.md`
section 13). Nothing here has had an independent tie-out yet.

## The question

Eric asked how Gwinnett's -3.3% change in full-time renter pay ranks among
counties in large metro areas where median rent rose 25% or more after
inflation from 2005-09 to 2020-24.

## Who is in the comparison

- 435 counties are in metros of 1 million or more (NCHS 2023 large central
  and large fringe counties). 81 of them saw median rent rise 25% or more after
  inflation.
- 37 of those 81 can be measured on their own: in both periods, the county is
  made up of whole microdata areas (PUMAs). The other 44 share a microdata
  area with a neighbor. In metro Atlanta, that leaves out Forsyth, Fayette,
  Paulding and Dawson.
- The 37 lean toward large counties, since small counties usually share a
  microdata area.

## Result

- Gwinnett's change (-3.3%, plus or minus 5.2 at 90%) is second lowest of the
  37. Only Cherokee County, also in metro Atlanta, is lower (-6.0%, plus or
  minus 10.8).
- Only those two show a drop. The middle county rose 14.5%.
- No county is lower than Gwinnett by more than the combined margin, and the
  next counties up (Lake County, Florida, +2.6%; Hillsborough County, Florida,
  +4.9%) are within margins of Gwinnett. The order near the bottom is not
  certain.
- Among all 155 measurable large-metro counties, whatever their rent growth,
  Gwinnett ranks 16th from the lowest; 19% of them show a drop.
- **Check.** Gwinnett's -3.3% from the state-wide pull matches the county pull
  in `scripts/12_renter_income.py` exactly.

## What this cannot show

- **Why** pay lagged.
- **Margins from replicate weights may be too small where earnings bunch at
  round numbers.** Maricopa County's margin (plus or minus 0.3) is an
  example. Gwinnett's and Cherokee's margins are wide enough that this does not
  change the reading.
- **The 44 counties left out.** Their pay could not be measured on their own.
