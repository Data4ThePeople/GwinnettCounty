# Status

Project: GwinnettCounty
Process: ~/.claude/d4tp-process/PROCESS.md

## Current

Post: none yet
Step: 1
Since: 2026-10-21

## Steps

| Step | What | Confirmed | Notes |
|---|---|---|---|
| 1  | Exploration and analysis | | |
| 2a | Draft with brackets resolved | | |
| 2b | Eric's edit, Claude's look-over | | |
| 2c | Slice markup | | |
| 2d | Hero 1680x1080 + alt text | | |
| 2e | SEO | | |
| 2f | Pushed to Prismic (draft) | | |
| 2g | Mailchimp teaser | | |

## Stale

None.

## Log

- 2026-10-21 Step 1 opened. Topic: a county spotlight in the style of the
  Dawson County post, on the least affordable rental county with the largest
  decline. Eric's rule: among the top 10 least affordable counties in
  2020-2024 with at least 1,000 rentals, the one with the largest change since
  2005-2009, using the Rentals Within Reach tool (AffordableHousing project).
- 2026-10-21 Selection carried over from a session run in the AffordableHousing
  project: research/candidate-selection.md (the rules, the candidates, why
  Lincoln County NM was set aside, why Gwinnett, the Atlanta pattern, open
  questions) and scripts/01_candidate_selection.py, which reproduces every
  number from the tool's processed data. By the rule as written Lincoln
  County NM has the largest decline (-72%), but its 2005-2009 starting point
  is marked low reliability and its decline comes from renter incomes, not
  rents. Eric chose Gwinnett County GA: rank 3 of 1,987 (rank 1 with college
  counties left out), 25.5% to 10.5% (-59%), renter median margin 3% in every
  period, rent up 32% after inflation against renter income up 8%. Nothing in
  AffordableHousing was changed.
- 2026-10-21 Eric is moving this work to a new PyCharm window. Next: plan mode
  for the exploration, then DATASETS.md before any new data or chart.
- 2026-10-21 Plan approved: settle "Gwinnett story or suburb vs. inner city"
  first, with decision rules set before the tests. DATASETS.md written (tool
  shares, NCHS 2023 urban-rural codes, OMB 2023 delineation, ACS place
  tables). Test 1 (counties, tool measure): suburbs fell more in 34 of 49
  large metros. Test 2 (largest city vs. rest of metro, one metro income
  line): suburbs fell more in only 15 of 54, and Atlanta city fell more than
  its suburbs. By the rules: not a national or Atlanta suburb story; a
  Gwinnett story (-38% at the metro line vs. DeKalb -26%, Clayton +16%, city
  -24%). Memo: research/suburb-vs-city.md. Waiting on Eric's call on framing.
- 2026-10-21 Eric chose the Gwinnett frame. Gwinnett's median rent ($1,810)
  is third in the metro after Forsyth and Fayette; what stands out is rent
  against renter income. Tested five explanations against seven peers with
  rules set first (research/why-rents.md). Supported: supply (0.65 permitted
  units per added household, 12% in 5+ unit buildings) and single-family
  rentals (share of rentals 31.0% to 39.5%, the largest rise; ARC says the
  region's most corporate-owned homes). Not supported: bedroom mix, richer
  renter pool, turnover pricing. Investor sources gathered by an agent in
  research/investor-sources.md; GAO and ARC/AJC figures checked by hand.
  DATASETS.md sections 5-8 added. Waiting on Eric.
- 2026-10-21 Eric asked whether new high-priced apartments explain the loss.
  PUMS by year built (research/new-rentals.md, scripts/07_new_rentals.py):
  mostly no. Apartments built 2010+ are 10% of rentals, median $1,870 vs
  county $1,812. Pre-2000 rentals went from 27.5% to 13.5% within reach;
  pre-2000 apartments lost about 5,500 within reach, more than the county's
  net loss. Microdata number within reach -26% vs the tool's -33% (exact
  rents vs rent ranges). Waiting on Eric.
- 2026-10-21 Eric asked about the owner-renter income gap. Not wide
  (research/owner-renter-gap.md): renter median 54.8% of owner median vs
  53.0% nationally; 220th of 282 large counties from the widest; narrowed 5.3
  pts. Gwinnett owners' median fell 2% after inflation while most neighbors'
  rose. Waiting on Eric.
- 2026-10-21 Eric asked for draft charts. Eight drawn in charts/ by
  scripts/09_charts.py (house dark style, numbers recomputed at render):
  share within reach vs US, rentals vs within-reach counts, rent vs renter
  income after inflation, older apartments, rent by year built, permits by
  year, permits per added household, single-family share change. Waiting on
  Eric's pick of charts.
- 2026-10-21 Eric asked whether Gwinnett's renter income lagged. Yes:
  +8.3% after inflation vs metro +15.8%, 12th of 15 metro counties with
  10,000+ renters; rent +31.8%, and rent minus income is the largest of the
  15. Added to research/owner-renter-gap.md. Waiting on Eric.
- 2026-10-21 Eric asked for a scatter of renter income change vs rent change
  to show Gwinnett as an outlier. Drawn as charts/09-income-vs-rent.png (15
  metro counties with 10,000+ renters). Gwinnett is farthest above the
  equal-growth line (+23.6 pts vs Clayton +18.3, DeKalb +17.6, Cherokee
  +17.3), but within margins; against a fitted trend it is level with
  Forsyth and Cherokee. Told Eric "outlier" overstates it.
