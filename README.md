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

## Data sources

The shares come from the Rentals Within Reach tool
([repo](https://github.com/Data4ThePeople/AffordableHousing)), built from the
American Community Survey 5-year files (Census Bureau tables B25063, B25119
and others), NBER TAXSIM35 for taxes, and the BLS Consumer Price Index.
Its `DATASETS.md` lists every limit of those data.

## How to rebuild

The selection script reads the processed files of the AffordableHousing
project, expected at `~/PycharmProjects/AffordableHousing`:

```
python scripts/01_candidate_selection.py
```

## Method notes

The share is the share of cash-rent units with a gross rent at or under 30%
of the median renter household's income after taxes (married, no children),
at the tool's defaults. A county is ranked when it has at least 1,000
cash-rent units in 2020-2024 and the tool does not mark it low reliability.
Each period is in its own final-year dollars.
