# Were Gwinnett's new rentals mostly high-priced apartments?

October 21, 2026. Numbers come from `scripts/07_new_rentals.py` (output in
`research/new-rentals-output.txt`), using ACS 5-year microdata (PUMS) for
2005-09 and 2020-24. Rentals are split by when the building was built and by
building type. "Within reach" uses the tool's ceiling for each period: $792 a
month in 2005-09 and $1,253 in 2020-24. Nothing here has had an independent
tie-out yet.

## The question

In the tool, Gwinnett's rentals grew 63% while the number within reach fell
33%. Did new high-priced apartments drive that?

## The short version

Mostly no. New apartments were a small part of the rental stock and were
priced near the county median. Most of the loss came from older rentals,
built before 2000, whose rents rose past what the county's renters could
afford.

## Check against the tool

Microdata use exact rents, and the tool reads shares from rent ranges, so
the levels differ a little.

| | 2005-09 | 2020-24 |
|---|---|---|
| Rentals with a cash rent (microdata) | 65,811 | 106,566 (+62%) |
| Share within reach, microdata | 24.1% | 11.0% |
| Share within reach, tool | 25.5% | 10.5% |
| Number within reach, microdata | 15,875 | 11,716 (-26%) |

The microdata drop in the number within reach (-26%) is smaller than the
tool's (-33%). The direction is the same, and the comparisons below are
within the microdata only.

## New apartments were a small slice, priced near the median

In 2020-24, apartments in buildings of 5 or more units built in 2010 or later
held about 10,960 renter households (plus or minus about 670). That is 10% of
Gwinnett's rentals.

- **Rent.** Their median gross rent was $1,870, 3% above the county median of
  $1,812.
- **Within reach.** 7.9% of them were within reach, against 11.0% of all
  rentals.
- **Against neighbors.** New apartments cost more in Fulton ($2,039),
  Cobb ($1,938) and DeKalb ($1,897).

The highest-priced newer rentals were houses. Single-family rentals built in
2010 or later had a median of $2,496, and 2.4% were within reach. There were
about 6,730 of them.

## The loss was in older rentals

Rentals in buildings built before 2000 made up 61% of the stock in 2020-24.

| Built before 2000 | 2005-09 | 2020-24 |
|---|---|---|
| Rentals | 49,744 | 64,756 |
| Median gross rent | $919 | $1,741 |
| Share within reach | 27.5% | 13.5% |
| Number within reach | 13,659 | 8,773 |

**Older apartments.** Apartments in buildings of 5 or more units built before
2000 held about the same number of renters in both periods: 28,759 and
29,972. The share within reach fell from 33.3% to 13.6%, and the number fell
from about 9,590 to about 4,070. That loss of about 5,500 is larger than the
county's whole net loss of about 4,160 in the microdata.

**Against neighbors.** The share of pre-2000 rentals within reach also fell in
DeKalb (20.8% to 13.8%), Clayton (19.7% to 13.8%), Cobb (29.0% to 25.0%) and
Cherokee (37.8% to 30.7%). It rose in Fulton (27.5% to 32.8%) and Henry
(28.0% to 29.9%). Gwinnett's fall, about half, was the largest of the seven.

## Where the 63% growth came from

Rentals with a cash rent grew by about 40,760.

- **Built 2010 or later:** about 19,370, close to half the growth. Of these,
  about 10,960 were apartments and 6,730 houses.
- **Built before 2000:** up about 15,010, mostly houses (14,918 to 26,182).
  These are older homes that became rentals.
- **Built 2000-09:** the rest.

## What this cannot show

- **Same buildings.** The microdata do not follow buildings. "Built before
  2000" in 2020-24 is close to the same stock as in 2005-09, but some
  buildings were torn down or changed from owned to rented, or back.
- **Year built is reported by the household.** Renters may not know it
  exactly, especially for older buildings.
- **Why older rents rose.** This shows where the loss happened, not why.
  Explanations tested earlier (`research/why-rents.md`) point to few new homes
  per new household, which would raise rents across the stock, but the data
  cannot prove that link.
- **"Luxury."** The data have rent, size, age and building type, not finishes
  or amenities. We describe new apartments by their rent, not as "luxury."
