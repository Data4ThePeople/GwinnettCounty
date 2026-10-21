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
