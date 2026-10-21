# How we chose Gwinnett County

Notes from a session in the AffordableHousing project on October 21, 2026,
carried over to start this project. Every number here comes from
`scripts/01_candidate_selection.py`, which reads the processed data of the
Rentals Within Reach tool in `~/PycharmProjects/AffordableHousing`. Its full
output is in `research/candidate-selection-output.txt`. Nothing here has had
an independent tie-out yet.

## What Eric asked for

A county spotlight in the style of the Dawson County post. Start from the
least affordable rental counties with at least 1,000 rentals, and tell the
story of one of them. The wrinkle: of the counties in the top 10 least
affordable in the latest data, pick the one with the largest change from the
start of the measurement period to the latest data.

## The rules we used

- **Measure:** the share of rentals priced within reach in the Rentals Within
  Reach tool, at its defaults: the median renter household, income after
  taxes (married, no children), rent at 30% of income.
- **Periods:** ACS 5-year files. Start is 2005-2009, latest is 2020-2024.
- **At least 1,000 rentals:** 1,000 or more cash-rent units in 2020-2024.
- **Reliable data:** the county is not marked low reliability by the tool in
  2020-2024. The tool marks a county low reliability when it has under 200
  cash-rent units, when the margin on its rent count is too wide, or when the
  margin on its renter median income is over 25% of the estimate. That leaves
  1,987 ranked counties.
- **Change:** percent change in the share, 2005-2009 to 2020-2024.

A first pass left out the renter income margin rule. That let in seven
counties the tool does not rank (Putnam GA, Park CO, Quay NM, St. Charles LA,
Claiborne LA, Fairfax city VA, Nantucket MA). They are out.

## The top 10 in 2020-2024

With college counties included (the page default), six of the top 10 are
college counties, and most of those got more affordable over the period.
Limitation 14 of the tool explains why they read low: students report little
income. The three that are not college counties are Gwinnett GA, Clayton GA
and Lincoln County NM. With college counties left out, DeKalb GA, Broward FL,
Dallas AL, Tunica MS, Boulder CO, Osceola FL and Kendall TX join them. The
table shows the candidates that declined, in order of the decline.

| County | 2005-09 | 2020-24 | Change | Note |
|---|---|---|---|---|
| Lincoln County, NM | 42.1% | 11.8% | -72% | 2005-09 and 2015-19 marked low reliability |
| Gwinnett County, GA | 25.5% | 10.5% | -59% | margin 3% in every period |
| Kendall County, TX | 34.6% | 15.4% | -56% | top 10 only with college counties left out |
| Clayton County, GA | 19.5% | 11.0% | -44% | swings between periods |
| DeKalb County, GA | 20.7% | 14.0% | -32% | top 10 only with college counties left out |
| Dallas County, AL | 20.7% | 14.4% | -31% | top 10 only with college counties left out |
| Tunica County, MS | 21.5% | 15.2% | -29% | two periods marked low reliability |
| Broward County, FL | 19.1% | 14.2% | -25% | top 10 only with college counties left out |

## Why not Lincoln County, New Mexico

By the rule as written, Lincoln County has the largest decline. We set it
aside because:

- Its starting point (2005-2009) and its 2015-2019 figure are both marked low
  reliability: the renter median income margin is 28% and 33% of the estimate.
- The decline comes from renter incomes, not rents. Median gross rent went
  from $645 to $956, up 48%, while prices overall rose 46%. The median renter
  income went from $26,979 to $26,113, down 34% after inflation.
- With about 2,300 renter households, a change in who rents there can move
  the renter median a lot. That is the renter-pool question in limitation 19
  of the tool, which the data cannot answer.

## Why Gwinnett County, Georgia

- Rank 3 of 1,987 in 2020-2024 with college counties included, and rank 1
  with them left out. In the top 10 either way.
- Among the top 10 counties whose data is reliable in every period, the
  largest decline: 25.5% to 10.5%, down 59%.
- The most solid data in the group: the renter median margin is 3% of the
  estimate in every period, and the county has 110,314 renter households in
  2020-2024.
- The decline comes from rent. Median gross rent went from $939 to $1,810, up
  93%, or 32% after inflation. The median renter income went from $38,202 to
  $60,473, up 8% after inflation.
- Holding the 2020-2024 renter income fixed after inflation, the share would
  have been 34.8% in 2005-2009 against 10.5% in 2020-2024. Rents moved even
  at a constant income.
- Renter households grew from 67,396 to 110,314 over the four periods.
- It is already on the follow-up list in AffordableHousing `DATASETS.md`
  section 10 (large Sun Belt suburban counties), with the 2024 GAO report on
  company ownership of single-family rentals in Atlanta as a lead.

Kendall County, Texas (Boerne) was the runner-up: clean data and a decline
driven by rent, but it is in the top 10 only with college counties left out.

## The Atlanta pattern

Three of the top counties are in metro Atlanta: Gwinnett, Clayton and DeKalb.
DeKalb is just east of the city and holds part of Atlanta. Gwinnett is to its
northeast and the two share a border. Clayton is directly south of the city.
The rest of the core metro reads very differently:

| County | 2005-09 | 2020-24 | Change | Rank of 1,987 |
|---|---|---|---|---|
| Gwinnett | 25.5% | 10.5% | -59% | 3 |
| Clayton | 19.5% | 11.0% | -44% | 4 |
| DeKalb | 20.7% | 14.0% | -32% | 11 |
| Henry | 23.8% | 18.2% | -23% | 48 |
| Cherokee | 34.4% | 22.6% | -34% | 143 |
| Fayette | 23.5% | 23.0% | -2% | 157 |
| Cobb | 29.8% | 23.9% | -20% | 183 |
| Fulton | 26.4% | 24.6% | -7% | 210 |
| Douglas | 33.6% | 28.7% | -15% | 354 |
| Forsyth | 36.7% | 31.4% | -14% | 490 |
| Rockdale | 15.4% | 31.8% | +107% | 514 |

Fulton, which holds most of the city, and Cobb are in the middle of the
national ranking. So this does not read as "Atlanta is unaffordable." The
three near the top are inner suburbs to the east and south. Whether the post
treats the neighbors as context or tells the three-county story is Eric's call.

## Open questions for Step 1

- Why do Gwinnett, Clayton and DeKalb sit so far from Fulton and Cobb? Who
  rents there, what kind of rental housing it is, and how it changed.
- Investor and company purchases of single-family homes in Gwinnett (the 2024
  GAO report on Atlanta is the starting point).
- The renter pool: 43,000 more renter households since 2005-2009. How much is
  new arrivals, how much is owners turning renter, and how the income mix
  changed (B25118 with constant-dollar bands, as done for Cook County).
- Rent by unit size and building type, to check limitation 3 of the tool
  (a studio and a three-bedroom count the same).
- Background in the style of Dawson County: the county's history, population
  and growth, jobs, and what changed in housing.
- The tool's tie-out and its independent tie-out covered these shares. Any new
  dataset needs its own `DATASETS.md` section before analysis, a coverage
  check, and both tie-outs before Step 1 closes.
