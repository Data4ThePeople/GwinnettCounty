# Independent tie-out 2 (fresh agent, October 21, 2026)

Scope: the intro and map, "The lowest share in the country, outside college
counties", "New rentals came in out of reach", "Renters' pay did not keep up",
and images 01, 02, 05, 06, 07 of `posts/gwinnett-county-rents/`.

Independence: in phase 1 this agent read only `DATASETS.md`, the AffordableHousing
`DATASETS.md`, `tax_grid.json` and `cpi.json`. It did not read `research/`,
`scripts/`, `data/processed/`, `STATUS.md`, `README.md` or `posts/`, and it did
not reuse code from `tieout/independent/` (it looked at it for API patterns).
Every table was pulled again from the Census API, the NCHS file and the OMB list
were downloaded again, and the PUMA equivalency files for 14 states were
downloaded. Phase 1 values were written to
`tieout/independent2/phase1_values.txt` before the post was opened.

Code: `tieout/independent2/` (`c2.py` helpers, `acs.py`, `reach.py`,
`pums_gw.py`, `gw_k.py`, `puma.py`, `l1.py`, `l2_pull.py`, `l2_calc.py`,
`l2_sens.py`, `phase2_extra.py`). Raw downloads: `tieout/independent2/raw/`.

CPI-U factor 2024/2009 = 313.689 / 214.537 = 1.46217.

## 1. Recomputed values

| ID | Value | Method | Caveats |
|---|---|---|---|
| J1 | Gwinnett 10.51% (lowest of 29). Clayton 10.95, DeKalb 14.00, Henry 18.24, Newton 19.09, Spalding 19.29, Cherokee 22.57, Fayette 22.98, Cobb 23.90, Fulton 24.61, Carroll 27.27, Douglas 28.68, Heard 29.03 (low rel.), Paulding 29.68, Walton 29.92, Meriwether 30.70, Forsyth 31.36, Rockdale 31.84, Dawson 33.60, Coweta 33.71, Lumpkin 36.03 (college county), Barrow 36.30, Morgan 36.35 (low rel.), Pickens 37.83, Bartow 39.11, Butts 46.79, Pike 48.87, Jasper 57.03 (low rel.), Haralson 70.05 (highest). | B25063 cash-rent buckets 2020-24, even spread; ceiling = 0.30 x (B25119_003 - grid tax, married no children) / 12, linear interpolation in the tax grid; CBSA 12060 from OMB list1_2023 (29 counties). | Low reliability = under 200 cash-rent units, CV of B25063_001 over 30%, or renter-median MOE over 25% of estimate (my reading of the tool rule). |
| J2 | 3 (Gwinnett 1st, Clayton 2nd, DeKalb 4th). Ten lowest: Gwinnett 10.51, Clayton 10.95, Lincoln NM 11.79, DeKalb 14.00, Broward 14.20, Dallas AL 14.39, Tunica 15.22, Boulder 15.24, Osceola 15.35, Kendall TX 15.38. 1,922 ranked without college counties; 1,987 with them; Gwinnett 3rd with them (Whitman WA 9.82, Benton OR 10.47). | Ranked = 1,000+ cash-rent units, not low reliability; college = (B14001_008 + _009) / B14001_001 >= 15%, 2020-24 (71 units). | Joined Alaska/Virginia units use a bucket median; none near the bottom ten. |
| K1 | Cash-rent renter households 65,811 -> 106,566, +40,755. Houses built before 2000: 14,918 -> 26,182, +11,264. Apartments built 2010+: 0 -> 10,959, +10,959. Combined +22,223 = 54.5% of the total change. (Also: houses 2010+ +6,733; houses 2000-09 +3,835; apartments 2000-09 +2,270; apartments before 2000 +1,213.) | PUMS household records, TEN=3, PUMAs 01501-01505 (2000) and 01601-01607 (2020), all inside Gwinnett; WGTP. Houses BLD 2-3, apartments BLD 6-9. YBL 3-9 = before 2000; YRBLT < 2000. | YBL coding verified against B25036 2005-09 renters: YBL 1 = 2,665 vs "2005 or later" 2,695; YBL 2 = 13,402 vs "2000-2004" 13,582; YBL 3 = 19,479 vs "1990s" 19,531. So 1 = newest, as DATASETS section 7 says. Sample sizes: 198 records for houses 2010+, 346 for apartments 2010+. No margins computed. |
| K2 | $1,253.28 a month (2020-24). 2005-09: $791.53 in 2009 dollars = $1,157.35 in 2024 dollars. | Published B25119_003 $60,473 (2024) and $38,202 (2009); tool tax grid, GA, married no children. | - |
| K3 | Houses before 2000: median $1,994.94, 10.2% within reach (n=918). Apartments 2010+: $1,870, 7.9% (n=346). Houses 2010+: $2,496, 2.4% (n=198). (All cash-rent: $1,812, 11.0%.) | GRNTP x ADJHSG/1e6, lower weighted median by WGTP; within reach = rent <= $1,253.28. | A second median definition gave the same values. |
| K4 | Apartments before 2000: 28,759 -> 29,972 (+4.2%). Median gross rent $864.71 (2009 $) = $1,264 (2024 $); 2020-24 $1,660. Change +92.0% before inflation, +31.3% after. Affordable amount $1,157 -> $1,253 (2024 $), +8.3%. Gap rent minus amount: +$107 (2005-09), +$407 (2020-24). Within reach 33.3% -> 13.6%. | As K1-K3. | Within-reach households by group: older apartments 9,589 -> 4,073 (-5,516), against -4,159 for all cash-rent households; apartments 2000-09 -771; every house group and apartments 2010+ rose. |
| L1 | 438 NCHS code 1-2 rows (68 + 370); 435 current counties; 433 with B25064 in both periods (Connecticut drops out). 81 with median gross rent up 25%+ after inflation. 37 measurable on their own, 44 not (18 fail only in 2000 PUMAs, 4 only in 2020 PUMAs, 22 in both; Broomfield CO has no 2000 PUMA as it did not exist). Not measurable in metro Atlanta: Paulding, Forsyth, Dawson, Fayette. | NCHSUR2023_3156.csv (Latin-1); B25064 2024 / (2009 x CPI) - 1 >= 0.25; PUMEQ5 summary level 781 lines for 2000; 2020 tract-to-PUMA file for 2020. | "Number of large-metro counties" depends on whether deleted rows count (438 / 435 / 433). |
| L2 | See table below. Gwinnett -3.3% +/- 5.2 (2nd from the bottom). Drops: Cherokee GA -6.0% +/- 10.8 and Gwinnett. Middle (19th of 37): Ellis TX +14.5% (+/- 12.9). Gwinnett median $46,139 -> $44,627 (2024 $). Cobb +6.7% +/- 4.8. | API-filtered person records (TEN 3:4, WKHP 35:99, ESR 1:5 then 3 dropped, WKW=1 / WKWN 50:52), PERNP > 0, PERNP x ADJINC (x CPI for 2009), lower weighted median by PWGTP; replicate medians with PWGTP1-80, SE = sqrt(4/80 x sum of squared differences), x 1.645. Three pulls per state and period, row counts checked equal and joined 1:1. | Neither drop has a 90% margin that excludes zero (Gwinnett -8.5 to +1.9; Cherokee -16.8 to +4.8). Maricopa's margin (0.3) is tiny because replicate medians land on the same heaped value. An interpolated median moves Gwinnett to -3.4 and Cherokee to -5.7. |

L2 full list (change after inflation, 90% margin): Cherokee GA -6.0 (10.8),
Gwinnett -3.3 (5.2), Lake FL +2.6 (5.8), Hillsborough +4.9 (2.4), Sacramento
+6.2 (2.6), Bexar +6.7 (3.0), Cobb +6.7 (4.8), Rutherford +7.0 (8.0), Contra
Costa +8.9 (4.7), DeKalb +9.9 (5.1), Pinellas +10.1 (3.2), Snohomish +11.5
(5.2), Maricopa +13.0 (0.3), Denton +13.1 (4.4), Pierce +13.3 (3.8), Collin
+13.4 (4.2), Brazoria +14.1 (6.6), San Diego +14.1 (2.0), Ellis +14.5 (12.9),
Davidson +15.6 (3.8), Alameda +16.7 (3.6), Clark WA +17.4 (6.5), Mecklenburg
+17.9 (4.7), Williamson TN +18.9 (16.1), Salt Lake +19.0 (4.5), Fulton +21.2
(6.4), Dallas +22.4 (2.7), Suffolk MA +22.5 (3.7), San Mateo +24.0 (5.2),
Hudson +26.4 (4.8), Williamson TX +27.1 (7.3), Santa Clara +29.1 (3.5), Kings
+31.1 (2.0), Delaware OH +31.5 (11.1), DC +36.9 (3.1), King +37.4 (3.2), San
Francisco +44.5 (5.3).

## 2. Phase 2: numbers in the post and charts against mine

No number in scope differs from mine beyond rounding.

| Where | Post / chart | Mine | Result |
|---|---|---|---|
| Intro | three of ten least affordable outside college towns in metro Atlanta | 3 | Match |
| Intro | Gwinnett 10.5% | 10.51% | Match |
| Map 01 alt + labels | Gwinnett 10.5, Clayton 11.0, DeKalb 14.0, Henry 18.2, Cobb 23.9, Fulton 24.6, Haralson 70.0; all 29 labels | J1 list | All 29 match after rounding (Morgan 36.348 -> 36.3, Barrow 36.305 -> 36.3) |
| Map 01 | Hatched low reliability: Heard, Morgan, Jasper | same three | Match |
| Map 01 | 29 counties; range 10.5% to 70.0% | 29; 10.51 to 70.05 | Match |
| Section 2 | lowest of 1,922 counties | 1st of 1,922 | Match |
| Chart 02 | ten bars 10.5, 11.0, 11.8, 14.0, 14.2, 14.4, 15.2, 15.2, 15.3, 15.4, same names and order | J2 | Match |
| Chart 02 / text | ranks 3 of 1,987 with college counties, behind Whitman and Benton | same | Match |
| Text | Clayton "only half a point behind" | 0.44 points (11.0 - 10.5 rounded) | Match within rounding |
| Section 4 text | added about 41,000 rentals | +40,755 (PUMS); B25063 cash rent +41,400 | Match |
| Text | two kinds more than half | 54.5% | Match |
| Text | about 11,300 older houses; about 11,000 new apartments; about 6,700 houses since 2010 | 11,264; 10,959; 6,733 | Match |
| Text / chart 05 | about $1,250 a month | $1,253.28 | Match |
| Text / chart 05 | older houses $1,990, 10%; new apartments $1,870, 8%; houses since 2010 $2,500, 2% | $1,994.94, 10.2%; $1,870, 7.9%; $2,496, 2.4% | Match ($1,994.94 rounds to $1,990) |
| Text | older apartments about the same number in both periods | 28,759 -> 29,972 (+4.2%) | Match |
| Text / chart 06 | $860 -> $1,660, up 92% | $864.71 -> $1,660, +92.0% | Match |
| Text / chart 06 | 31% after inflation; amount up 8% | 31.3%; 8.3% | Match |
| Chart 06 | $1,260 / $1,160 (2005-09); $1,660 / $1,250 (2020-24) | $1,264 / $1,157; $1,660 / $1,253 | Match |
| Text | about $100 more, then about $400 more | $107; $407 | Match |
| Section 5 text | $46,100 -> $44,600 | $46,139 -> $44,627 | Match |
| Text | Cobb rose 7% | +6.7% | Match |
| Text / chart 07 | 37 counties; only two drops (Gwinnett, Cherokee); middle county 15% | 37; 2; Ellis +14.5% | Match |
| Chart 07 | all 37 bar values and their order | L2 list | All 37 match to 0.1 point; order identical |
| Chart 07 / caption | margins about 5 for Gwinnett, 11 for Cherokee; error bars | 5.2; 10.8; bar widths look consistent with mine | Match |
| Chart 07 / caption | 44 other counties not measurable, including Forsyth, Fayette, Paulding, Dawson | 44; those four | Match |
| Chart 07 subtitle | metros of 1 million or more, rent up 25%+ after inflation | NCHS 1-2, same rule | Match |

## 3. Word check

| Claim | Mark | Why |
|---|---|---|
| Intro: "three of the ten least affordable counties outside college towns were in the Atlanta metro area" | PARTLY SUPPORTED | Numbers match, but "least affordable" is one measure (share within reach for the median renter household), and the ten are among counties with 1,000+ rentals and not low reliability. "College towns" should read "college counties". |
| Intro: Gwinnett "had just 10.5% of rental units within reach" | SUPPORTED | 10.51%. |
| Intro: definition of within reach | SUPPORTED | Matches the tool rule (gross rent, after-tax, 30%). |
| Intro: Dawson County, Nebraska and the Tyson closure | COULD NOT CHECK | Outside this tie-out. |
| Map 01 title "smallest share ... in metro Atlanta: 10.5%" | SUPPORTED | Lowest of 29. |
| Map 01 subtitle (29 counties, 10.5% to 70.0%, hatching) | SUPPORTED | |
| Section heading "The lowest share in the country, outside college counties" | PARTLY SUPPORTED | True among the 1,922 ranked counties; about 1,150 smaller or low-reliability counties are not ranked, so "in the country" goes slightly past what was measured. The sentence below states the limits, except low reliability. |
| "lowest of the 1,922 counties we ranked with at least 1,000 rentals, leaving out college counties" | SUPPORTED | It also leaves out low-reliability counties (said on chart 02, not in the text). |
| Chart 02 title and subtitle | SUPPORTED | |
| "Clayton County is only half a point behind" | SUPPORTED | 0.44 points. |
| "with college counties included, Gwinnett ranks third, behind Whitman ... and Benton" | SUPPORTED | |
| "Gwinnett added about 41,000 rentals" | SUPPORTED | Net change in cash-rent renter households. |
| "about 11,300 older houses, built before 2000, that became rentals" | PARTLY SUPPORTED | The data show a net rise of 11,264 renter households in such houses. They do not show individual houses switching from owned to rented; "became rentals" implies that. Year built is self-reported. |
| "Two kinds account for more than half of them" | SUPPORTED | 54.5%. |
| "None of the three was priced for the median renter household" | PARTLY SUPPORTED | Each group's median rent is above the amount, but 10%, 8% and 2% of units were within reach. Stated as a group fact, it is a little over-certain. |
| "could afford about $1,250 a month at 30% of its income" | PARTLY SUPPORTED | The number is right, but it is 30% of after-tax income; the sentence says "its income". |
| Rents and shares for the three groups | SUPPORTED | |
| Chart 05 title "The kinds of rentals Gwinnett added rent well above what renters could afford" | PARTLY SUPPORTED | Medians are well above the median renter household's amount; "renters" broadens this to all renters. |
| Chart 05 subtitle "the three groups that added the most rentals since 2005-09" | SUPPORTED | Among house and apartment groups by build era: +11,264, +10,959, +6,733, then +3,835. |
| "That does not explain why the number of rentals within reach fell. The answer is in older apartments" | PARTLY SUPPORTED; implied cause, over-certain | As accounting it holds: older apartments within reach fell by about 5,500, more than the net fall of about 4,200. But "why" and "the answer" frame an accounting split as a cause. |
| "Gwinnett had about the same number of them in both periods" | SUPPORTED | +4%. |
| "$860 to $1,660, up 92% ... 31% rise ... rose 8%" | SUPPORTED | |
| "$100 more ... about $400 more" | SUPPORTED | |
| Chart 06 title "Older apartment rents rose 31%; what renters could afford rose 8%" | PARTLY SUPPORTED | Numbers are right; "what renters could afford" is the median renter household's amount. |
| Chart 06 subtitle | SUPPORTED | |
| "the rentals new to the market came in out of reach, and the older apartments that used to be close to reach rose far faster than renters' income" | PARTLY SUPPORTED | Older houses are not new to the market, and "came in out of reach" holds for medians only. "Renters' income" is the after-tax amount for the median renter household. |
| Heading "Renters' pay did not keep up" | SUPPORTED | Gwinnett full-time renter pay -3.3% against rent +31.8%. |
| "For the same kind of renter household ... income fell about 3%" | COULD NOT CHECK | Not in my list of figures, and the cell definitions are not in DATASETS.md. |
| "Renter households as a whole earned more only because the households changed ... Pay itself did not rise." | NOT SUPPORTED as worded; implied cause, over-certain | "Only because" claims a full cause; a reweighting shows association. "Pay itself did not rise" rests on -3.3% +/- 5.2, a range that includes a small rise (up to +1.9%). The composition figures (more workers, more full time, older, more degrees) were not checked here. |
| "$46,100 ... $44,600" and "In Cobb, that pay rose 7%" | SUPPORTED | |
| "Few counties with rents rising this fast saw that" | SUPPORTED | 2 of 37 measurable counties. |
| "We looked at 37 counties ... measure the county on its own" | SUPPORTED | |
| "Only two showed a drop ... Cherokee ... whose estimate is much less certain" | PARTLY SUPPORTED; over-certainty | The point estimates are the only two below zero, but neither margin rules out zero, and Lake FL (+2.6 +/- 5.8) and Rutherford TN (+7.0 +/- 8.0) margins reach below zero. The text calls out Cherokee's uncertainty but not Gwinnett's; the caption does say the order near the bottom is not certain. |
| "In the middle county of the group, it rose 15%" | SUPPORTED | Ellis TX +14.5%. |
| Chart 07 title "Where rent rose 25%+, renter pay did worst in Cherokee and Gwinnett" | PARTLY SUPPORTED | True for point estimates; the margins overlap with the next counties, which the subtitle says. "Rent rose 25%+" leaves out the large-metro and measurable limits that the subtitle gives. |
| Chart 07 subtitle | SUPPORTED | Wording is careful ("show a fall", "not certain"). |
| Chart 07 footnote (44 counties, four Atlanta-area names) | SUPPORTED | Broomfield CO is left out because it did not exist in 2000, not because it shares a PUMA; a small wording point. |

## 4. Could not check

- The "same kind of renter household" income change (about -3%) and the
  composition claims in "Renters' pay did not keep up" (more members worked,
  more full time, older, more degrees). Not in my figures, and the cell
  definitions are not in `DATASETS.md`.
- Intro facts about Dawson County, Nebraska and the Tyson plant.
- Margins on K1-K4 (counts, medians, shares by building type): no replicate
  weights were pulled for the household file, so I cannot say how certain the
  group medians and counts are. Houses built 2010+ rest on 198 records.
- How accurate year built is: self-reported, and YBL/YRBLT were checked only
  against B25036 totals.
- The even spread inside rent buckets and the tool's tax grid (taken as given).
- The exact low-reliability rule: I used the B25063_001 margin. If the tool uses
  another margin, the 1,922 and 1,987 counts could move, though they matched.
- Map shapes and the position of the downtown marker on image 01.
