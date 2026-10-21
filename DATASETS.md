# Datasets

One section per dataset, written before any analysis, updated whenever we learn
something new. The point is to know the traps before they show up in a chart.

## 1. Rentals Within Reach county shares (Data 4 The People)

**What it is.** For each county and ACS 5-year period, the share of cash-rent
units with a gross rent at or under 30% of the median renter household's income
after taxes (married, no children). Built in the AffordableHousing project.

**Where it comes from.** `~/PycharmProjects/AffordableHousing/data/processed/`:
`harmonized.json` (bucket counts and medians), `tax_grid.json`, `cpi.json`.
We read them in place and recompute shares with that project's own functions
(`scripts/10_tieout.py`: `income`, `tax`, `share`, `percentile`), so shares
match the published tool. Nothing in AffordableHousing is changed.

**Version and vintage.** As built for the published tool, October 2026. Four
periods: 2005-2009, 2010-2014, 2015-2019, 2020-2024.

**Coverage, changes, suppression, missing data, revisions, uncertainty.** See
the AffordableHousing `DATASETS.md`, sections 1 to 8. The ones that matter most
here:
- 3,141 county units on 2024 boundaries. Connecticut's nine planning regions
  are rebuilt from towns before 2020-2024. A few Alaska and Virginia areas are
  joined in every period.
- Limitation 3: unit size is ignored. A studio and a three-bedroom count the
  same.
- Limitation 14: college counties read low because students report little
  income.
- Limitation 19: the renter pool changes over time. A county's renter median
  can rise because higher-income households start renting there, not because
  existing renters earn more.
- Each period is in its own final-year dollars.

**Known quirks for this project.**
- `harmonized.json` has B25118 renter income buckets (`ti`, 11 buckets, top
  bucket $150,000 and up). A median read from these buckets with
  `percentile()` is within about 2% of the published B25119 renter median for
  Gwinnett, Fulton and DeKalb in 2005-09 and 2020-24. Test 2 relies on this,
  because a renter median for a group of counties cannot be read from the
  published county medians.
- Bucket counts can be added and subtracted. Medians cannot.

**License and attribution.** Census Bureau data are public domain. Credit the
American Community Survey 5-year estimates.

## 2. NCHS Urban-Rural Classification Scheme for Counties, 2023 (National Center for Health Statistics)

**What it is.** One code per county, 1 to 6. Code 1 is "large central metro"
and code 2 is "large fringe metro." Both are counties in metropolitan areas of
1 million or more people. A county is large central if it:
- contains the entire population of the metro's largest principal city, or
- is entirely contained in that city, or
- contains at least 250,000 residents of any principal city in the metro.

Every other county in a metro of 1 million or more is large fringe. Codes 3 to
6 are medium metro, small metro, micropolitan and noncore.

**Where it comes from.**
- Page: https://www.cdc.gov/nchs/data-analysis-tools/urban-rural.html
- Data: `NCHSUR2023_3156.csv` (160 KB, no login)
- Method: `2023-File-Documentation_updated-2026.pdf` and
  `County-Geography_updated-2026.pdf`
- All are saved in `data/raw/nchs/`.

**Version and vintage.** The 2023 scheme, first published September 2024 and
re-released September 2026. The re-release added rows for counties deleted
since 2013, with their 2013 codes. The scheme is based on the July 2023 OMB
metro delineation and Vintage 2022 population estimates. The 2023 rules are the
same as in 2006 and 2013. The 2006 and 2013 schemes also ran a discriminant
analysis that moved a handful of counties between central and fringe; the 2023
scheme does not.

**Coverage.** 3,156 rows: 68 large central, 370 large fringe, 400 medium metro,
356 small metro, 659 micropolitan, 1,303 noncore. 54 metros of 1 million or
more. These are counts of rows in the CSV.

**Changes over time.** We use the 2023 codes for every period, so the groups are
fixed, and a county that became suburban after 2009 counts as suburban in all
four periods. This is a choice, not a fact about 2005-2009. The 2023 file has
both Connecticut's old counties (with 2013 codes) and its nine planning regions
(with 2023 codes). We use the planning regions, which match the tool's units.

**Suppressed or missing values.** No codes are missing for current counties.
Population is blank for deleted counties.

**Known quirks.**
- **One central county per metro, sometimes none.** The rule is about city
  population inside a county line, so it can label inner suburbs, and parts of
  the city, as fringe.
- **Atlanta: Fulton is the only large central county.** DeKalb is large fringe,
  even though part of the city of Atlanta lies in DeKalb. Gwinnett, Cobb and
  Clayton are large fringe.
- **Fulton itself is mixed.** It holds the city of Atlanta and suburbs to the
  north such as Sandy Springs, Roswell and Alpharetta. So county codes alone
  blur the city-suburb line, and that is why Test 2 uses city boundaries.
- **Birmingham, AL has no large central county.** All seven of its counties are
  coded 2. It is left out of the central-vs-fringe comparison in Test 1, with a
  check that codes Jefferson County as central.
- **Encoding.** The file is Latin-1, not UTF-8 (county names such as Doña Ana).
  Read it with `encoding="latin-1"`.

**Uncertainty.** None stated. It is a rule-based classification.

**License and attribution.** Public domain (US government). Credit: National
Center for Health Statistics, 2023 NCHS Urban-Rural Classification Scheme for
Counties.

## 3. OMB metropolitan delineation, July 2023 (Census Bureau, for OMB)

**What it is.**
- List 1: each county's metro or micro area (CBSA), with a central or
  outlying flag.
- List 2: the principal cities of each CBSA, with state and place FIPS codes.

**Where it comes from.**
- `https://www2.census.gov/programs-surveys/metro-micro/geographies/reference-files/2023/delineation-files/`
- Files: `list1_2023.xlsx` and `list2_2023.xlsx`, saved in `data/raw/omb/`.

**Version and vintage.** OMB Bulletin 23-01, July 2023, based on the 2020
standards and 2020 census commuting data.

**Coverage.** 1,915 county rows in List 1 and 1,294 principal city rows in List
2. These are data rows, not counting headers and notes.

**Changes over time.** Metro definitions change with each delineation (2003,
2013, 2018, 2020, 2023). The 2005-2009 ACS used the 2008 definitions. We hold
the 2023 county list fixed for every period and build each metro by adding the
tool's county units. We do not use CBSA-level ACS estimates, which follow the
definitions in force for each release.

**Known quirks.**
- Each metro's largest principal city is the first name in its title (for
  example "Atlanta" in "Atlanta-Sandy Springs-Roswell, GA"). We match it to
  List 2 by name within the CBSA and check every match by hand in the output.
  Two cities can share the first name: "Kansas City, MO-KS" lists both Kansas
  City, Missouri and Kansas City, Kansas. The script takes the one with more
  cash-rent units (Missouri).
- Consolidated city-counties are listed under their "balance" place code (for
  example Nashville-Davidson, Louisville/Jefferson County, Indianapolis). Those
  codes are what the place-level ACS uses.
- The OMB "central" flag is a commuting-based label. It is not the same as the
  NCHS "large central" code, and many suburban counties are OMB "central."

**License and attribution.** Public domain.

## 4. ACS 5-year place-level tables (Census Bureau)

**What it is.** For each city (Census "place"):
- B25063 gross rent: bucket counts of cash-rent units and units with no cash rent
- B25118 renter households by income: 11 buckets
- B25119 median household income by tenure: the renter median and its margin

Four periods: 2005-2009, 2010-2014, 2015-2019, 2020-2024.

**Where it comes from.**
- Census API, `{year}/acs/acs5`, `group(B25063)` etc., `for=place:*`,
  `in=state:*`.
- Cached as JSON in `data/raw/acs/` through the AffordableHousing `census()`
  helper. The key comes from the central `.env` through `d4tp_env`.

**Version and vintage.** The 2009, 2014, 2019 and 2024 ACS 5-year releases.
Released estimates are not revised.

**Coverage.** Every incorporated place and census-designated place in the 50
states and DC.

**Changes over time.**
- **City boundaries are those in force at the start of each release's final
  year.** Annexations change the area being measured. For Atlanta, this
  includes annexations into DeKalb and Fulton after 2009, such as the 2017
  annexation of the Emory University area. We record how large each change is
  once we have the data (the change in the city's renter households is the
  check). Atlanta's renter households went from 97,452 (2005-09) to 126,676
  (2020-24). How much of that is annexation is not yet measured.
- **Rent buckets.** B25063 has 21 rent buckets in 2009 and 2014 and 24 in 2019
  and 2024 (the top bucket was split into $2,500, $3,000 and $3,500). This is
  the same as at county level, and `RENT_EDGES` handles it.

**Suppressed, censored or missing values.**
- Medians outside the published range come back as annotation codes such as
  -666666666, so medians are read only when positive.
- Places with very small samples have wide margins. That should not affect the
  large cities used here.

**Units and rounding.** Counts are whole numbers, dollars are nominal, and each
period is in its own final-year dollars.

**Known quirks.**
- **A city can cross county lines** (Atlanta lies in Fulton and DeKalb). The
  rest of the metro is the metro total minus the city, so that is fine as long
  as the city lies entirely inside its metro's 2023 counties. The script checks
  that no remainder count goes negative; none did, in any metro or period.
- **The rest of the metro is not "the suburbs" in a planning sense.** It also
  includes other principal cities (Sandy Springs and Roswell in Atlanta's
  case), exurbs and rural edges.

**Uncertainty.** Each estimate has a published 90% margin of error. The margin
on the city renter median is reported for each city and period. We do not
compute margins for the subtracted rest-of-metro counts.

**License and attribution.** Public domain. Credit: U.S. Census Bureau,
American Community Survey 5-year estimates.

## 5. ACS 5-year county tables on housing stock and renters (Census Bureau)

**What it is.** Tables for Gwinnett and seven peer counties (Fulton, DeKalb,
Cobb, Clayton, Henry, Cherokee, Forsyth), all four periods:
- B25068 bedrooms by gross rent
- B25042 tenure by bedrooms
- B25032 tenure by units in structure
- B25036 tenure by year built
- B25038 tenure by year the householder moved in
- B25003 tenure
- B25004 vacancy status
- B25001 housing units
- B11001 households

**Where it comes from.** Census API, `{year}/acs/acs5`, `group(...)`,
`for=county:...&in=state:13`, cached in `data/raw/acs/`. Table layouts are
saved in `data/raw/meta/`.

**Version and vintage.** 2009, 2014, 2019 and 2024 releases. They are not
revised.

**Changes over time.**
- **B25068 rent bands.** There are only six rent bands per bedroom group, and
  they changed. In 2009 the bands are under $200, $200-299, $300-499, $500-749,
  $750-999 and $1,000 or more. In 2024 they are under $300, $300-499, $500-749,
  $750-999, $1,000-1,499 and $1,500 or more. A share within reach read from
  these bands is rough. So the bedroom-mix test compares two figures built from
  the same bands (actual mix against fixed mix) and reports the difference, not
  the level.
- **B25036 year built and B25038 year moved in.** The bands move with each
  release. For example, the newest band is "2005 or later" in 2009 and "2020
  or later" in 2024. We compare "built in the last 15 to 20 years" and "moved
  in within the five-year window" only where the bands line up, and say so.
- **B25031 median gross rent by bedrooms.** Not published in the 2009 release
  (the API returns 404), so it is not used for the comparison over time.

**Suppressed or missing values.** None expected for counties of this size.

**Uncertainty.** Each cell has a 90% margin of error. Counts of renter units by
structure type and bedrooms in the smaller peers (Cherokee, Forsyth, Henry)
have wide margins, which we report where a finding rests on them.

**License.** Public domain.

## 6. Building Permits Survey, county annual (Census Bureau)

**What it is.** New privately owned housing units authorized by building
permits, by county and year. Reported as 1-unit, 2-unit, 3-4 unit and 5+ unit
buildings, with buildings, units and value for each.

**Where it comes from.**
`https://www2.census.gov/econ/bps/County/co{YYYY}a.txt`, 2000-2025. Saved in
`data/raw/bps/`.

**Coverage and filling.** Each file has two sets of columns:
- **Estimates:** reported counts plus Census imputation for permit offices
  that did not report every month.
- **"rep":** reported only.

We use the estimates and report how much of each county's total was imputed
(estimate minus reported).

**Known quirks.** Permits are authorizations, not homes built. Some are never
built, and timing lags vary. A unit permitted as 1-unit can be owned or
rented; permits do not record tenure. Permit offices are cities and counties,
summed to counties by Census.

**Revisions.** Annual files replace the monthly figures. We use the annual
files as published.

**License.** Public domain.

## 7. ACS 5-year PUMS (Census Bureau)

**What it is.** Household microdata with weights. We use gross rent (GRNTP),
when the household moved in (MV), units in structure (BLD), bedrooms
(BDS/BDSP), year built (YBL/YRBLT), tenure (TEN) and household income (HINCP).

**Where it comes from.** Census microdata API, `2009/acs/acs5/pums` and
`2024/acs/acs5/pums`, by PUMA. Cached in `data/raw/pums/`.

**Geography.**
- **2005-09 file:** uses 2000 PUMAs. In the Census 2000 5% equivalency file
  (`data/raw/puma/PUMEQ5-GA.TXT`), Gwinnett is PUMAs 01501-01505, all inside
  the county. Fulton, DeKalb, Cobb, Clayton, Henry and Cherokee also nest.
  **Forsyth does not:** its PUMA 00800 also covers Dawson and Pickens, so
  Forsyth is left out of the PUMS test.
- **2020-24 file:** uses 2020 PUMAs for every record ("based on 2020 Census
  definition"). The 2020 tract-to-PUMA file
  (`data/raw/puma/tract2020_puma2020.txt`) shows Gwinnett as PUMAs
  01601-01607, all inside the county. All eight counties nest.

**Changes over time.**
- Variable names changed: BDS became BDSP, YBL became YRBLT.
- Year built uses different codes. In the 2005-09 file, YBL 1 = 2005 or
  later, 2 = 2000-04, 3 = 1990s, down to 9 = 1939 or earlier. In the 2020-24
  file, YRBLT gives the first year of a decade (2000 = 2000-09, 2010 =
  2010-19) and single years from 2020. Both files can be split at 2000, so
  "built before 2000" lines up across them. Year built is reported by the
  household, and renters may not know it exactly.
- The MV categories differ between files, and we map them to "moved in within
  the last 2 years" or "longer."
- Dollar amounts are in the survey year's dollars. ADJHSG brings housing costs
  to the final year of the file.

**Uncertainty.** We use the 80 replicate weights (WGTP1-80) for standard
errors on any difference we report.

**License.** Public domain.

## 8. Published sources on investor ownership of single-family homes

**What it is.** Reports, articles and vendor pages, not a dataset we
compute from. The full list, with quotes, pages, definitions and status, is in
`research/investor-sources.md`.

**What we checked ourselves (October 21, 2026).**
- **GAO-24-106643, May 2024, p. 15** (PDF page 19): "institutional
  investor-owned homes constituted about 25 percent ... of the single-family
  rental market" in Atlanta, as of June 2022. Owners of 1,000+ homes. GAO
  footnote 40 says the shares "may be overstated." Gwinnett does not appear in
  the report. GAO calls the evidence on rents mixed (p. 20).
- **Atlanta Regional Commission, November 13, 2024.** The text says "Gwinnett
  County is tops in the region in total single-family units owned by a
  corporate landlord," with seven named firms and Parcl Labs data. County
  counts appear only in chart images. The AJC (December 5, 2024) repeats
  Gwinnett 9,680, Cobb 5,284, Fulton 4,150, DeKalb 3,859, Clayton 3,444. The
  shares of all single-family units (Gwinnett 3.8%, Henry 7.4%) were read from
  the chart by the research agent and not checked again here.

**Known traps.**
- Every source uses a different definition: one home, LLC name keywords, 15+,
  50+, 100+ or 1,000+ homes, or a named list of firms. They also use
  different denominators: all single-family homes, single-family rentals, all
  rentals, or sales. Figures from different sources cannot be compared.
- No source gives a Gwinnett figure for 2005-2009 or a Gwinnett series across
  our periods. So these sources can describe ownership around 2022-2024. They
  cannot show how it changed over our periods or measure an effect on rent.
- The Georgia Tech figures (53% of single-family rental purchases, 17% of
  single-family sales, summer 2021) are often quoted as "Atlanta." They cover
  Gwinnett and DeKalb combined.

## 9. ACS 5-year table B25119 for every county (Census Bureau)

**What it is.** Median household income in the past 12 months, by tenure
(owner and renter), with B25003 for household and renter counts.

**Where it comes from.** Census API, `2009/acs/acs5` and `2024/acs/acs5`, all
counties and the nation. Cached in `data/raw/acs/tenure_income_*.json`.

**Quirks.**
- Dollars are in each file's final-year dollars; we bring them to 2024 with
  CPI-U, as for the tool.
- Connecticut reports nine planning regions in 2020-24 and eight counties in
  2005-09, so Connecticut drops out of any change between the two periods.
- Puerto Rico's municipios are included.
- The margin for the renter-to-owner ratio uses the Census formula for a ratio
  of two estimates (renters are not a subset of owners), with 90% MOEs.

**License.** Public domain.

## 10. Home prices: ACS B25077 and the FHFA county house price index

**ACS B25077.** Median value of owner-occupied homes, as estimated by the
owner. Census API, `2009/acs/acs5` and `2024/acs/acs5`, every county. Cached in
`data/raw/acs/B25077_*_county.json`. Brought to 2024 dollars with CPI-U.

**FHFA house price index for counties.** All-transactions index (sales and
appraisals on mortgages bought or guaranteed by Fannie Mae and Freddie Mac),
annual, nominal, not seasonally adjusted. From
`https://www.fhfa.gov/hpi/download/annual/hpi_at_county.csv`, which is in fact
an Excel file despite the `.csv` name; saved as
`data/raw/fhfa/hpi_at_county.xlsx` (last updated March 31, 2026). The header
row is the sixth row.

**Quirks.**
- FHFA calls these county indexes developmental and leaves a period (".") where
  the sample is too small. Counties missing any year in 2005-2009 or 2020-2024
  are left out.
- We compare the average of 2005-2009 with the average of 2020-2024 to match
  the ACS periods. The FHFA change is not adjusted for inflation; a common
  factor would not change correlations or ranks.
- The index measures price change for the same homes; ACS values also change
  as the mix of owned homes changes.

**License.** FHFA data are public.

## 11. ACS 5-year PUMS person records for renter households

**What it is.** Every person in a renter household (TEN 3, rented for cash or
not, and TEN 4, occupied without rent), so that B25119's renter universe is
covered. Variables:
- **Household:** SERIALNO, SPORDER, NP, HINCP, ADJINC, WGTP, TEN.
- **Person:** AGEP, ESR (employment status), PERNP (earnings), WAGP, WKHP
  (usual hours), WKW (2005-09) or WKWN (2020-24) for weeks worked, NATIVITY,
  HISP, RAC1P, SCHL, COW, INDP, PWGTP.
- **Replicate weights:** WGTP1-80 and PWGTP1-80.

**Where it comes from.** Census microdata API, `2009/acs/acs5/pums` and
`2024/acs/acs5/pums`, same PUMAs as section 7 (Forsyth left out). Five calls
per PUMA and period because of the 50-variable limit, joined on SERIALNO and
SPORDER. Cached in `data/raw/pums_people/`.

**Changes over time.**
- **SCHL.** The 2005-09 file uses the old 16 codes (9 = high school
  graduate, 12 = associate, 13 = bachelor's, 14-16 = graduate). The 2020-24
  file uses 24 codes (16-17 = high school or GED, 18-20 = some college or
  associate, 21-24 = bachelor's or more). Both map to four levels: less than
  high school, high school, some college or associate, bachelor's or more.
- **Weeks worked.** WKW in 2005-09 is a range code (1 = 50-52 weeks); WKWN in
  2020-24 is the number of weeks. Full-time year-round means 35+ usual hours and
  50+ weeks in both.
- **Industry codes (INDP).** The Census industry codes were revised between
  the files. We use only broad sectors, from code ranges that hold across
  revisions.
- **ADJINC** brings income and earnings to the file's final year. CPI-U then
  takes 2009 dollars to 2024 dollars.

**Uncertainty.** Successive difference replicate weights, as in section 7.

**License.** Public domain.

## 12. QCEW average annual pay by county (BLS)

**What it is.** The Quarterly Census of Employment and Wages: average annual
pay of jobs covered by unemployment insurance, all ownerships, all industries,
by county where the job is located (not where the worker lives).

**Where it comes from.** BLS public API v2, series `ENU{county FIPS}50010`
(data type 5 = average annual pay, size 0, ownership 0, industry 10 = total),
2005-2024. CPI-U annual averages (series CUUR0000SA0, period M13) come from the
same API to put each year in 2024 dollars. Cached in `data/raw/qcew/`.

**Quirks.** Pay is for jobs in the county, including jobs held by people who
commute in. Federal, state and local government jobs are included; the
self-employed are not. We compare the average of 2005-2009 with the average of
2020-2024 to match the ACS periods.

**License.** Public domain.
