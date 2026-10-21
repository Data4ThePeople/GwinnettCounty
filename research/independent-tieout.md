# Independent tie-out

Run October 21, 2026 by a fresh agent that had not seen the analysis. It read
only `DATASETS.md`, the chart images in `charts/`, and from AffordableHousing its
`DATASETS.md`, `tax_grid.json`, `cpi.json` and the published page (used only to
confirm the rent bucket edges). Every input was pulled again from the source:
the Census API (ACS 5-year tables and PUMS), the Census Building Permits Survey
files, the OMB July 2023 delineation, the FHFA county index, and the BLS API
(QCEW and CPI-U). Code: `tieout/independent/` (`acs_pull.py`, `reach.py`,
`misc_calc.py`, `puma_map.py`, `pums_prefetch.py`, `pums_pull.py`,
`pums_calc.py`). Raw downloads are cached in `tieout/independent/raw/`
(gitignored).

CPI-U annual averages from BLS match `cpi.json` (2009 214.537, 2024 313.689).
The factor from 2009 to 2024 dollars is 1.4622.

## Values

| ID | My value | How I got it | Caveat |
|---|---|---|---|
| A1 | Gwinnett 10.51% (2020-24) | Renter median B25119_003 $60,473; tax from the tool's grid (married, no children, GA, 2024), linear between grid points; line = 30% of after-tax income / 12 = $1,253.28; share of 107,229 cash-rent units in B25063 buckets, spread evenly inside the bucket | |
| A2 | 1 of 1,922 | Ranked: 1,000+ cash-rent units in 2020-24 and not low reliability (under 200 cash-rent units, CV over 30% on B25063_001, or B25119_003 margin over 25% of the estimate). College counties: (B14001_008 + _009) / B14001_001 of 15% or more, 2020-24; I get 71 | Low reliability read from the B25063_001 margin; the count matches the chart |
| A3 | 3 of 1,987 | Same, college counties included. Lower: Whitman WA 9.82%, Benton OR 10.47% | |
| A4 | Clayton 10.95%. Four lowest outside college counties: Gwinnett 10.51%, Clayton 10.95%, Lincoln NM 11.79%, DeKalb 14.00% | As A2. Next six: Broward 14.20, Dallas AL 14.39, Tunica 15.22, Boulder 15.24, Osceola 15.35, Kendall TX 15.38 | |
| B1 | 25.52%, 18.11%, 21.46% (2005-09, 2010-14, 2015-19) | As A1 with each period's tax grid and buckets. Lines: $791.53, $781.54, $1,017.58 | |
| B2 | -58.8% | 10.509 / 25.520 - 1 | |
| B3 | Units +63.0% (65,785 to 107,229); within reach -32.9% (16,789 to 11,269) | B25063_002; share x units | |
| B4 | 31.95%, 27.64%, 31.95%, 31.32% | All county units, share weighted by cash-rent units, Puerto Rico left out; renter median from B25118 buckets where none is published or units are joined | Connecticut's earlier periods use its old counties, not rebuilt planning regions; Alaska joins approximate. Effect under 0.01 points against the chart |
| C1 | Rent +31.8% ($939 to $1,810); renter income +8.3% ($38,202 to $60,473), after inflation | B25064, B25119_003, CPI-U | 90% margin on the income change about ±4.7 points (Census ratio formula) |
| C2 | Gwinnett 1st of 15, gap +23.6 points. Next: Clayton +18.4, DeKalb +17.6, Cherokee +17.3 | 29 CBSA 12060 counties from OMB list 1; 15 with B25003_003 of 10,000+ in 2020-24. Full list: Henry 13.2, Forsyth 12.3, Douglas 9.9, Cobb 9.3, Paulding 7.6, Coweta 6.0, Newton 4.9, Fulton 4.3, Carroll 3.2, Rockdale -9.2, Bartow -21.7 | Gwinnett's lead over Clayton (5.2 points) is about the size of Gwinnett's income margin alone |
| C3 | Gwinnett 54.8% ($60,473 / $110,370); United States 53.0% ($52,966 / $100,009) | B25119_003 / B25119_002, 2020-24 | |
| C4 | Gwinnett +82.4%, Cobb +83.3% (also Fulton +72.6%, DeKalb +63.8%) | FHFA all-transactions annual county index, average 2020-24 over average 2005-09, nominal | |
| D1 | 10.3% (10,959 of 106,566 households); median rent $1,870; all cash-rent households $1,812 | 2024 PUMS, Gwinnett PUMAs 01601-01607, householder records, TEN 3, BLD 6-9, YRBLT 2010+; GRNTP x ADJHSG; WGTP weighted median | 346 sample households in the newer-apartment group |
| D2 | Older apartments 28,759 (2005-09) and 29,972 (2020-24); within reach 9,589 and 4,073 | TEN 3, BLD 6-9, built before 2000 (2009: YBL 3-9; 2024: YRBLT under 2000); within reach = GRNTP x ADJHSG at or below that period's line (B1, A1) | Older apartments +4.2%; within reach -57.5%. Samples 1,086 and 838. Depends on the 2009 YBL coding, settled below |
| D3 | Gwinnett 0.654 (47,411 units / 72,528 households). Ranking: DeKalb 1.860, Forsyth 1.034, Fulton 0.915, Cherokee 0.914, Cobb 0.800, Henry 0.758, Gwinnett 0.654, Clayton 0.418 | BPS county annual files 2007-2021, estimate columns, units in all four structure types; B11001_001 2020-24 minus 2005-09 | Imputed units (estimate minus reported) are small: Gwinnett 633, DeKalb 1,323, Henry 952 |
| D4 | 31.0% (2005-09), 39.5% (2020-24) | B25032 (_014 + _015) / _013 | |
| E1 | +6.8% ($56,375 to $60,204 in 2024 dollars) | PUMS householder records, TEN 3 or 4, HINCP x ADJINC, WGTP weighted median | 90% margin ±4.7 points. Lower than the B25119 change (+8.3%) because PUMS and the published table differ in sample and rounding |
| E2 | Gwinnett -3.3% ($46,139 to $44,627), Cobb +6.7%, DeKalb +9.9%, Fulton +21.2%, Henry -3.4%, Cherokee -6.0%, Clayton -9.2% | Persons in renter households, ESR 1, 2, 4 or 5, WKHP 35+, WKW 1 (2009) or WKWN 50+ (2024), PERNP x ADJINC above 0, PWGTP weighted median | Gwinnett 90% margin ±5.2 points (SE 3.14, 80 replicate weights, SE = sqrt(4/80 x sum of squared differences)). Same results without the earnings-above-0 rule. Henry and Cherokee rest on 419 to 688 sample workers |
| E3 | Workers per renter household: Gwinnett 1.295 to 1.356, Cobb 1.269 to 1.343. Gwinnett share with 2+ workers 33.8% to 37.5% | Count of ESR 1, 2, 4, 5 per household, WGTP weighted | |
| E4 | 65.8% (2005-09), 75.6% (2020-24) | Persons in renter households with ESR employed and earnings above 0, PWGTP | Counting everyone with earnings above 0 whatever their current status: 58.3% and 70.2% |
| E5 | Householder 65+: 5.5%, 9.7%. Bachelor's or more: 23.4%, 30.3% | Householder record (SPORDER 1); SCHL 13+ (2009) and 21+ (2024) | |
| E6 | -2.8% ($54,824 reweighted against $56,375) | 2020-24 households reweighted by 2005-09 cell share / 2020-24 cell share; 36 cells (workers 0/1/2+ x age under 35/35-64/65+ x 4 education levels), all filled in both periods | Unweighted change is +6.8% |
| E7 | Clayton +16.4%, Fulton +15.8%, Cobb +10.3%, Cherokee +8.1%, DeKalb +7.9%, Henry +5.6%, Forsyth +3.2%, Gwinnett +1.0%. Gwinnett ranks 8 of 8 | BLS API, ENU{fips}50010, annual (A01); each year to 2024 dollars; average of 2020-24 over average of 2005-09. Gwinnett $67,350 to $68,030 | |

### 2009 year-built coding (settled)

The 2009 PUMS API metadata lists YBL codes from oldest to newest (01 = 1939 or
earlier, 08 = 2000-04, 09 and up = 2005 and later). The values in the file run
only from 1 to 9, and they match the descending order in `DATASETS.md`
section 7 (1 = 2005 or later, 9 = 1939 or earlier). Gwinnett renter households
(TEN 3 or 4), weighted PUMS against published B25036, 2005-09:

| Built | PUMS (descending coding) | B25036 renters |
|---|---|---|
| 2005 or later | 2,824 (4.2%) | 2,695 (4.0%) |
| 2000-04 | 13,725 (20.4%) | 13,582 (20.2%) |
| 1990s | 19,722 (29.2%) | 19,531 (29.0%) |
| 1980s | 19,628 (29.1%) | 19,478 (28.9%) |
| 1970s | 7,942 (11.8%) | 7,941 (11.8%) |
| 1960s | 1,711 (2.5%) | 2,016 (3.0%) |
| 1950s | 888 (1.3%) | 1,009 (1.5%) |
| 1940s | 468 (0.7%) | 475 (0.7%) |
| 1939 or earlier | 519 (0.8%) | 669 (1.0%) |
| Total | 67,427 | 67,396 |

With descending coding, every band is within 0.5 points of B25036, and the
share built before 2000 is 75.5% against 75.8% published. Under the API
metadata's coding, 98.5% would be built before 2000, which is far off. So the
descending coding is the right one, and D2 uses it. With the wrong coding, the
2005-09 older-apartment count would be 38,504 and the within-reach count would
be 11,143.

## Charts: numbers and words

### 01 Share within reach
- Numbers: Gwinnett 25.5, 18.1, 21.5, 10.5; United States 32.0, 27.6, 32.0, 31.3. All match.
- Title "fell from 25.5% to 10.5%": SUPPORTED.
- Subtitle (definition, "the median renter household could afford"): SUPPORTED. It matches the tool's default.

### 02 Rentals and within reach
- Numbers: 65,785; 107,229; 16,789; 11,269. All match.
- Title "rentals grew 63%, but the number within reach fell 33%": SUPPORTED (+63.0%, -32.9%).
- Footer (counts are share x rentals): SUPPORTED.

### 04 Older apartments
- Numbers: 28,800; 30,000; 9,600; 4,100. Mine are 28,759; 29,972; 9,589; 4,073. All match when rounded to 100.
- Title "about the same number": SUPPORTED (+4.2%).
- Title "58% fewer within reach": SUPPORTED (-57.5%). These are survey estimates from about 840 to 1,090 sample households, so the 58% has a margin I did not compute.
- Footer "Year built is reported by the household": SUPPORTED.

### 05 Rent by year built
- Numbers (2020-24 medians), mine against the chart: all $1,812 ($1,810); before 2000: apartments $1,660, houses $1,994.94 ($1,990); 2000-09: apartments $1,673 ($1,670), houses $2,221 ($2,220); 2010 or later: apartments $1,870, houses $2,496 ($2,500). All match when rounded to $10.
- Title "Newer apartments in Gwinnett rent for 3% more than the county median": SUPPORTED (+3.2%). The newer-apartment group is 346 sample households, so the margin is not small next to 3%.

### 07 Permits per household
- Numbers: 1.86, 1.03, 0.92, 0.91, 0.80, 0.76, 0.65, 0.42. All match.
- Title "permitted 0.65 homes for each household it added": SUPPORTED. Permits are authorizations, not homes built. The two periods are not the same years (permits 2007-2021, households between the midpoints of the two ACS periods). The subtitle says this.

### 09 Income vs rent
- Numbers: Gwinnett income +8%, rent +32%. Every dot I compared sits where my values put it. There are 15 counties. The "about 5 points" margin matches (±4.7).
- Title "Among large Atlanta-area counties, Gwinnett's rent outran renter income the most": PARTLY SUPPORTED. The point estimate is the largest gap (23.6 against Clayton 18.4 and DeKalb 17.6). But the title states it flatly, while the subtitle says the lead is uncertain. The title is more certain than the data.
- Subtitle: SUPPORTED.

### 10 Least affordable
- Numbers: all ten shares, 1,922, "3 of 1,987" and 71 match.
- Title "Gwinnett had the smallest share of rentals within reach outside college towns": PARTLY SUPPORTED. It is true only among counties with 1,000+ rentals that are not marked low reliability. The subtitle and footer give these limits; the title does not. The excluded units are counties, not towns.
- Footer "71 counties where students are a large share of renters": NOT SUPPORTED. The tool's rule is 15% or more of residents age 3 and over enrolled in college or graduate school. That is a share of residents, not of renters.

### 11 Renter pay
- Numbers: Fulton +21.2, DeKalb +9.9, Cobb +6.7, Gwinnett -3.3, Henry -3.4, Cherokee -6.0, Clayton -9.2; Gwinnett $46,100 to $44,600. All match ($46,139 to $44,627).
- Subtitle "within about 5 points either way": SUPPORTED (±5.2).
- Title "Pay for Gwinnett's full-time renter workers fell 3% after inflation; in Cobb it rose 7%": PARTLY SUPPORTED. Both numbers match. But Gwinnett's -3.3% has a 90% margin of ±5.2 points, so the data cannot rule out no change or a small rise. Saying "fell" is more certain than the data. I did not compute Cobb's margin.

### Cause and universal claims
No title or subtitle on the eight charts states a cause or makes a universal claim. Chart 04 pairs the older-apartment counts with a within-reach line. It reads as description, not a statement of why.

## Could not check

- **Rents inside a bucket.** The even spread of rents inside a B25063 bucket is an assumption I reused, not something I could test.
- **Tax grid.** I used the tool's tax grid as given. I did not re-run TAXSIM.
- **National figures.** My national figures treat Connecticut's first three periods as its old counties rather than planning regions rebuilt from towns, and handle the Alaska boundary changes only roughly. They still match the chart to 0.01 points.
- **Low reliability.** I read low reliability from the margin on B25063_001. The tool's documentation does not say which margin it uses. My choice gives the same 1,922.
- **Margins.** I did not compute margins for D1, D2, D4 or E3-E6, Cobb's earnings change (E2), or the C2 gaps other than Gwinnett's income change.
- **E1 against C1.** The PUMS renter income change (+6.8%) and the published B25119 change (+8.3%) differ by 1.5 points. That is inside the ±4.7 margin, but posts should not mix the two.
