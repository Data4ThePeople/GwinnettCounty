# Gwinnett story, or suburb vs. inner city?

October 21, 2026. The decision rules below were written into the plan before
either test ran. Numbers come from `scripts/02_core_vs_suburb_counties.py`
(output in `research/test1-counties-output.txt`) and
`scripts/03_city_vs_suburb.py` (output in `research/test2-cities-output.txt`).
Nothing here has had an independent tie-out yet.

## The two tests

**Test 1, counties.** This test uses the tool's own measure, where each county
is judged by its own renter median income. It compares the counties NCHS codes
"large central" with those it codes "large fringe" in the 54 metros of 1
million or more people. In Atlanta, Fulton is the only central county. DeKalb,
Gwinnett, Cobb and Clayton are all coded fringe.

**Test 2, cities.** This test compares the largest city in each of those metros
with the rest of the metro. Everyone is held to one income line: the metro's
renter median income, after taxes, with rent at 30% of income. It asks where
the rentals that the typical renter in the metro can afford are located, and
how that changed.

## What they found

| | Test 1: counties, own income | Test 2: city vs. rest, metro income |
|---|---|---|
| Large metros where the suburbs fell more | 34 of 49 (69%) | 15 of 54 (28%) |
| All large metros, central side | 29.3% to 28.3% (-4%) | 35.8% to 32.8% (-8%) |
| All large metros, suburban side | 31.5% to 29.3% (-7%) | 26.8% to 26.9% (+0%) |
| Atlanta, central side | Fulton 26.4% to 24.6% (-7%) | City 33.7% to 25.7% (-24%) |
| Atlanta, suburban side | Fringe 25.5% to 19.7% (-23%) | Rest 24.0% to 21.5% (-10%) |

The two tests point in opposite directions, both nationally and in Atlanta.
The difference is renter income.
- In Test 1, a city county's share can hold up because its renters' median
  income rose quickly.
- In Test 2, everyone in the metro is held to the same income, so the result
  shows where the rents themselves moved.
- In Atlanta, the city's renter median went from $30,307 to $57,026 (+88%).
  The metro's renter median went from $34,686 to $59,206 (+71%).

Inside the Atlanta suburbs, the decline is concentrated in three counties.
These are Test 1 figures, on the tool's own measure:

| Atlanta group | 2005-09 | 2020-24 | Change |
|---|---|---|---|
| Fulton (central) | 26.4% | 24.6% | -7% |
| Gwinnett, Clayton and DeKalb | 22.0% | 12.1% | -45% |
| The other 25 fringe counties | 28.9% | 27.0% | -7% |

At the shared metro income line from Test 2, the three counties do not move
together:

| County | 2005-09 | 2020-24 | Change | Own renter median, change |
|---|---|---|---|---|
| Gwinnett | 16.0% | 9.8% | -38% | +58% |
| DeKalb | 23.8% | 17.6% | -26% | +62% |
| Clayton | 27.0% | 31.5% | +16% | +41% |
| Atlanta city | 33.7% | 25.7% | -24% | +88% |

Clayton's low score in the tool comes from its renters' incomes, which rose
less than the metro's, not from its rents. Gwinnett has the smallest share
within reach of the metro renter median of any core county and city in this
table, and the largest decline.

## Against the rules set in advance

- **National suburb story: not met.** Test 2 has 28% of metros, not
  two-thirds, and the city side fell more than the suburban side in Test 2's
  national totals.
- **Atlanta suburb story: not met cleanly.** Atlanta's suburbs fell more in
  Test 1, but the city fell more in Test 2.
- **Gwinnett story: met.** Gwinnett's decline is well beyond Clayton's and
  DeKalb's on both measures:
  - tool: -59% vs. -44% and -32%
  - metro line: -38% vs. +16% and -26%

  Fringe and central counties as groups are close nationally (-7% vs. -4% in
  Test 1).

## Recommendation

Tell it as a Gwinnett story, with Atlanta as the setting. The data do not show
a general pattern of suburbs losing affordable rentals faster than cities. They
show one large suburban county where rents moved further from what renters
earn than anywhere else in the core metro, including the city of Atlanta. A
suburb that now has fewer rentals within reach of the typical metro renter than
the city does is still a suburb-and-city comparison, but as a fact about
Gwinnett, not as a national trend.

## What this cannot tell us

- **Why Gwinnett's rents rose so much.** The leads are investor purchases of
  single-family homes, what kind of rental housing was built, and who moved in.
  None of these is tested yet.
- **What happened inside counties.** Fulton mixes the city with northern
  suburbs. Splitting it would take tract or city-by-county data.
- **How much of the city's change comes from annexation.** The city's renter
  households went from 97,452 to 126,676, and part of that growth may come
  from land added to the city.
- **Margins.** The test does not compute margins for the rest-of-metro
  figures, which are found by subtraction.
- **The renter pool.** It changes over time (limitation 19 of the tool), so a
  rising renter median can reflect who rents, not raises.
