# Why did Gwinnett's rents rise so far above what its renters earn?

October 21, 2026. Five explanations, each tested against seven peer counties
(Fulton, DeKalb, Cobb, Clayton, Henry, Cherokee, Forsyth) with a rule written
before the data came in. Numbers come from `scripts/05_why_rents.py` (output in
`research/why-rents-output.txt`) and `scripts/06_pums_turnover.py` (output in
`research/pums-turnover-output.txt`). Published investor sources are in
`research/investor-sources.md`. Nothing here has had an independent tie-out
yet.

## The short version

Two explanations hold up, and three do not.

- **Hold up:**
  - Gwinnett built fewer homes per new household than most of its peers,
    and few of them were apartments.
  - Its rental growth came largely from single-family houses becoming
    rentals.
- **Do not hold up:**
  - Bigger rentals.
  - Richer renters arriving.
  - New leases priced far above old ones.

These are patterns that came alongside the rent rise. The data cannot show
that any one of them caused it.

## 1. Bigger rentals (bedroom mix): not supported

**Rule.** Holding the 2005-09 bedroom mix fixed moves the 2020-24 share
within reach by 3 points or more.

**Result.** It moves it by 0.8 points. Rentals in Gwinnett did shift toward
three or more bedrooms, from 34% to 42% of cash-rent units, but the share
within reach fell inside every size:

| Size | 2005-09 | 2020-24 |
|---|---|---|
| 1 bedroom | 56% | 27% |
| 2 bedrooms | 21% | 14% |
| 3 or more | 10% | 8% |

These shares come from coarse rent bands (see `DATASETS.md` section 5). The
gap between the two mixes is the reliable part, not the levels. Every peer
county also shows a gap under 1 point. Rents rose for the same kind of unit;
the units did not just get bigger.

## 2. Single-family homes became rentals: partly supported

**Rule.** The single-family share of renter-occupied units rose faster than in
the peers, and a published source reports Gwinnett-specific investor figures.

**Result.**
- **Single-family share of rentals.** In Gwinnett it went from 31.0% to
  39.5%, a rise of 8.5 points. That is the largest rise of the eight counties.
  Clayton is close at 8.1 points; Cobb rose 4.3 and DeKalb 4.0. Fulton fell
  1.1 points.
- **Single-family rentals.** They more than doubled, from 20,868 to 43,526,
  which is 53% of all renter growth. Owner households grew 16%.
- **Published investor figures.**
  - The Atlanta Regional Commission (November 2024, Parcl Labs data, seven
    named firms) says Gwinnett has the most corporate-owned single-family
    homes in the 21-county region. The AJC reports the count as 9,680. As a
    share of all single-family homes, Gwinnett (3.8%) is below Henry (7.4%)
    and Clayton (4.6%).
  - GAO puts owners of 1,000+ homes at about 25% of the Atlanta metro's
    single-family rental market in 2022, and says that may be overstated.

**What it cannot show.** No source gives Gwinnett investor figures for
2005-09, so we cannot say how much of the growth in single-family rentals went
to companies rather than to individual landlords. GAO calls the research on
investors and rents mixed.

## 3. Too few homes for the people arriving (supply): supported

**Rule.** Fewer permitted units per added household than the peers, or a
larger fall in rental vacancy.

**Result.**
- **Households and permits.** Gwinnett added 72,528 households between the
  two periods. Permits from 2007 through 2021 came to 47,411 units, or 0.65
  per added household. That is lower than every peer except Clayton (0.42):
  Henry 0.76, Cobb 0.80, Cherokee 0.91, Fulton 0.92, Forsyth 1.03,
  DeKalb 1.86.
- **Apartments.** Only 12% of Gwinnett's permitted units were in buildings of
  5 or more units. The figure is 59% in Fulton, 49% in DeKalb and 39% in Cobb.
- **Permits by year.** Gwinnett permitted about 9,000 to 12,000 units a year
  from 2000 to 2006, then 719 in 2009. It has not passed 5,603 in any year
  since.
- **Rental vacancy.** It fell from 11.4% to 5.1%. That is a large fall, but
  not larger than the falls in Clayton, Cobb or Fulton, so this part of the
  rule is not met.

**What it cannot show.**
- **Spare housing at the start.** In 2005-09, after the building boom, many
  homes stood empty. Some of the new households moved into those homes rather
  than into new ones.
- **Permits are not finished homes.** And permits do not say whether a home
  will be owned or rented.

## 4. Higher-income renters arrived (the renter pool): not supported

**Rule.** Growth at $75,000 and up (2024 dollars) while the under-$35,000
count held steady.

**Result.** Gwinnett's renter households grew at every income level.
- **Under $35,000:** from 17,598 to 29,076, up 11,478. That is the largest
  increase among the eight counties, larger than Fulton's 10,255.
- **$75,000 and up:** up 17,512. That is 41% of Gwinnett's renter growth,
  against 68% in Fulton and 72% in Cobb.

This backs the reading that Gwinnett's renters stayed middle-income. The
renter median did not rise mainly because better-off renters moved in.

## 5. New leases priced far above old ones (turnover): not supported

**Rule.** The rent gap between recent movers and longer-term renters is much
larger in Gwinnett than in the peers.

**Result.** In 2020-24, Gwinnett renters who moved in within the last two years
paid a median of $1,880. Those who had stayed longer paid $1,761. The gap is
+6.8%, plus or minus 2.2 points. The gap is larger in Fulton (+20.0%),
Henry (+13.7%), Cherokee (+10.0%), Cobb (+9.5%) and DeKalb (+9.3%). Only
Clayton's is smaller (+4.4%). Gwinnett's longer-term renters were paying close
to new-lease prices too.

**Single-family rentals.** The gap is wider for single-family rentals in
Gwinnett (+13.9%) than for apartments (+4.4%). The single-family gap is still
smaller than in Fulton, Cobb, Clayton and Henry.

## Ranked

1. **Supply.** Fewer homes per new household than most peers, and few
   apartments among them.
2. **Single-family rentals.** The fastest shift of rentals into houses among
   the peers, in the county with the region's largest count of corporate-owned
   homes. We cannot measure what share of that shift went to companies.

Ruled out by the tests: bedroom mix, a richer renter pool, and turnover
pricing.

## Open for Step 1

- **Fulton's split.** City and suburb are not separated inside Fulton
  (tracts or city-by-county data).
- **Tract-level investor data.** A Gwinnett-only figure for single-family
  homes that became rentals before and after 2012, if one of the unread
  sources (Georgia Tech Research Brief 2022-1, the AJC county tables) has it.
- **Tie-outs.** Both tie-outs on any number that goes into the draft.
