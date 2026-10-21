# Gwinnett County, Georgia: rentals out of reach

Work in progress for a Data 4 The People county spotlight on Gwinnett County,
Georgia. In the Rentals Within Reach tool, Gwinnett is among the least
affordable rental counties in the country in 2020-2024, and its share of
rentals priced within reach of the median renter household fell from 25.5% in
2005-2009 to 10.5% in 2020-2024. No post or Pages link yet.

## What is here

- `research/candidate-selection.md`: how Gwinnett was chosen, the other
  candidates, and the questions this project starts from.
- `research/candidate-selection-output.txt`: the full output of the
  selection script.
- `scripts/01_candidate_selection.py`: recomputes every number in the
  selection notes.
- `research/suburb-vs-city.md`: whether this is a Gwinnett story or a
  suburb-versus-city story, tested two ways across the 54 metros of 1 million
  or more.
- `scripts/02_core_vs_suburb_counties.py` and
  `scripts/03_city_vs_suburb.py`: the two tests, with their output in
  `research/`.
- `research/why-rents.md`: five explanations for Gwinnett's rent rise, each
  tested against seven neighboring counties, with
  `scripts/04_fetch_county_tables.py`, `scripts/05_why_rents.py` and
  `scripts/06_pums_turnover.py`.
- `research/new-rentals.md`: whether new apartments or older rentals account
  for the loss of rentals within reach, by year built and building type, with
  `scripts/07_new_rentals.py`.
- `research/owner-renter-gap.md`: how far renters' income sits below
  homeowners' in Gwinnett, its neighbors and large counties nationwide, with
  `scripts/08_owner_renter_gap.py`.
- `research/values-vs-rents.md`: whether home price growth explains rent
  growth across counties, with `scripts/10_values_vs_rents.py`.
- `research/renter-income.md`: why Gwinnett's renter income lagged its
  neighbors, with `scripts/11_fetch_renter_people.py` and
  `scripts/12_renter_income.py`.
- `research/investor-sources.md`: published research on investor ownership
  of single-family homes in Gwinnett and metro Atlanta.
- `charts/`: draft charts, drawn by `scripts/09_charts.py` with the house
  style in `scripts/plot_style.py`. Every number is recomputed when the charts
  are drawn.
- `research/thread.md`: the proposed thread and chart list.
- `scripts/13_tieout.py`: recomputes every number in the thread, with output
  in `research/tieout-output.txt`.
- `research/independent-tieout.md`: an independent recomputation from the raw
  data, with its code in `tieout/independent/`.
- `DATASETS.md`: every dataset used, with its limits and quirks.

## Data sources

The shares come from the Rentals Within Reach tool
([repo](https://github.com/Data4ThePeople/AffordableHousing)), built from the
American Community Survey 5-year files (Census Bureau tables B25063, B25119
and others), NBER TAXSIM35 for taxes, and the BLS Consumer Price Index.
Its `DATASETS.md` lists every limit of those data. The suburb and city
tests also use the NCHS 2023 Urban-Rural Classification Scheme for Counties,
the OMB July 2023 metro delineation, ACS 5-year place-level tables B25063,
B25118 and B25119, ACS 5-year county tables on housing stock and renters, ACS
5-year microdata (PUMS), the Census Building Permits Survey, the FHFA
house price index for counties, and the BLS Quarterly Census of Employment
and Wages.

## How to rebuild

The selection script reads the processed files of the AffordableHousing
project, expected at `~/PycharmProjects/AffordableHousing`:

```
python scripts/01_candidate_selection.py
python scripts/02_core_vs_suburb_counties.py
python scripts/03_city_vs_suburb.py
python scripts/04_fetch_county_tables.py
python scripts/05_why_rents.py
python scripts/06_pums_turnover.py
python scripts/07_new_rentals.py
python scripts/08_owner_renter_gap.py
python scripts/09_charts.py
python scripts/10_values_vs_rents.py
python scripts/11_fetch_renter_people.py
python scripts/12_renter_income.py
python scripts/13_tieout.py
```

The NCHS and OMB files go in `data/raw/nchs/` and `data/raw/omb/` (links in
`DATASETS.md`). The third script pulls the place tables from the Census API
and needs a Census API key.

## Method notes

The share is the share of cash-rent units with a gross rent at or under 30%
of the median renter household's income after taxes (married, no children),
at the tool's defaults. A county is ranked when it has at least 1,000
cash-rent units in 2020-2024 and the tool does not mark it low reliability.
Each period is in its own final-year dollars.
