# Is the income gap between Gwinnett's homeowners and renters unusually wide?

October 21, 2026. Numbers come from `scripts/08_owner_renter_gap.py` (output
in `research/owner-renter-gap-output.txt`), using ACS 5-year table B25119,
median household income by tenure, for every county and the nation. Dollars
are 2024 dollars. Nothing here has had an independent tie-out yet.

## The short version

No. Gwinnett's renters earn a little over half what its homeowners earn,
close to the national figure, and the gap narrowed. What sets Gwinnett apart
is that both groups earn less than in its richer neighbors while its rents
reached similar levels.

## The gap

The gap is the renter median as a percent of the owner median. A lower number
means a wider gap. Margins are at 90%.

| | Owners 2020-24 | Renters 2020-24 | Gap 2005-09 | Gap 2020-24 |
|---|---|---|---|---|
| United States | $100,009 | $52,966 | 48.6% | 53.0% |
| Gwinnett | $110,370 | $60,473 | 49.5% (+/-1.7) | 54.8% (+/-2.2) |
| Fulton | $138,102 | $62,287 | 38.7% | 45.1% |
| DeKalb | $110,882 | $54,357 | 47.8% | 49.0% |
| Cobb | $129,248 | $67,585 | 47.2% | 52.3% |
| Clayton | $75,697 | $45,679 | 59.1% | 60.3% |
| Henry | $92,634 | $59,703 | 54.7% | 64.5% |
| Cherokee | $122,110 | $66,514 | 51.2% | 54.5% |
| Forsyth | $157,188 | $84,052 | 48.4% | 53.5% |

- **Against large counties.** Among the 282 counties with at least 100,000
  households, Gwinnett ranks 220th from the widest gap. Most large counties
  have a wider gap.
- **Change.** Gwinnett's gap narrowed by 5.3 points, about as much as the
  nation's (4.4 points).
- **Owners.** Gwinnett's owner median fell 2% after inflation, while owner
  medians rose 7% to 13% in Fulton, DeKalb, Cobb, Cherokee and Forsyth.
  Renters' median rose 8%.

## What this cannot show

- **Medians only.** Two medians can sit close together while the spread
  within each group differs.
- **Geography changes.** Connecticut reports planning regions in 2020-24 and
  counties in 2005-09; those places drop out of the change ranking. Puerto
  Rico is included in the rankings.

## Did Gwinnett's renter income lag its neighbors?

Yes. After inflation, the renter median rose 8.3% (plus or minus 4.5) from
2005-09 to 2020-24. That is about half the rise for the Atlanta metro (15.8%)
and the nation (15.9%). Rent rose 31.8%.

Among the 15 metro counties with at least 10,000 renter households:

| County | Renter income | Median gross rent |
|---|---|---|
| Fulton | +25.5% (+/-4.5) | +29.7% |
| Cobb | +18.3% (+/-4.5) | +27.6% |
| Cherokee | +16.7% (+/-10.9) | +34.0% |
| DeKalb | +11.0% (+/-4.0) | +28.6% |
| **Gwinnett** | **+8.3% (+/-4.5)** | **+31.8%** |
| Henry | +4.0% (+/-6.3) | +17.2% |
| Clayton | -3.7% (+/-5.8) | +14.6% |

- **Income.** Gwinnett ranks 12th of 15. Its gain is clearly below Fulton's
  and Cobb's, and too close to DeKalb's to call different. Henry and Clayton
  did worse.
- **Income and rent together.** Gwinnett's rent rose about as much as in the
  higher-income counties, while its renter income rose about as little as in
  the lower-income ones. The gap between the two, 23.6 percentage points, is
  the largest of the 15.

All 29 counties are in `research/owner-renter-gap-output.txt`. The smaller
counties have margins too wide to rank.
