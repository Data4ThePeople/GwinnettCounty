"""Download the data for the "why did rents rise" tests.

ACS 5-year county tables (all Georgia counties, four releases) on bedrooms, structure type, year built,
year moved in, tenure, vacancy, housing units and households; the Census Building Permits Survey county
annual files, 2000-2025; and ACS PUMS household records for the PUMAs of the peer counties, 2005-2009 and
2020-2024. Everything is cached, so re-runs do not call the API again.

Output: data/raw/acs/*_ga_county.json, data/raw/bps/co*.txt, data/raw/pums/*.json"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AH = Path.home() / "PycharmProjects" / "AffordableHousing"
sys.path.insert(0, str(AH / "scripts"))
from common import census, fetch  # noqa: E402

RAW = ROOT / "data" / "raw"
FK = ["2009", "2014", "2019", "2024"]
TABLES = ["B25068", "B25042", "B25032", "B25036", "B25038", "B25003", "B25004", "B25001", "B11001"]
# PUMAs inside each peer county (see DATASETS.md section 7); Forsyth's 2000 PUMA also covers Dawson and Pickens
PUMAS = {
    "2009": {"135": ["01501", "01502", "01503", "01504", "01505"], "121": [f"0110{i}" for i in range(1, 8)],
             "089": [f"0120{i}" for i in range(1, 7)], "067": [f"0130{i}" for i in range(1, 6)], "063": ["01401", "01402"],
             "151": ["01700"], "057": ["01900"]},
    "2024": {"135": [f"0160{i}" for i in range(1, 8)], "121": [f"0140{i}" for i in range(1, 9)],
             "089": [f"0150{i}" for i in range(1, 7)], "067": [f"0130{i}" for i in range(1, 6)], "063": ["02301", "02302"],
             "151": ["02201", "02202"], "057": ["00801", "00802"]},
}
# the API allows 50 variables per call, so the 80 replicate weights come in two more calls, joined on SERIALNO
PUMS_VARS = {"2009": ["SERIALNO,TEN,GRNTP,MV,BLD,BDS,YBL,HINCP,ADJHSG,ADJINC,WGTP"],
             "2024": ["SERIALNO,TEN,GRNTP,MV,BLD,BDSP,YRBLT,HINCP,ADJHSG,ADJINC,WGTP"]}
for _v in PUMS_VARS:
    PUMS_VARS[_v] += ["SERIALNO," + ",".join(f"WGTP{i}" for i in range(a, a + 40)) for a in (1, 41)]


def main():
    for v in FK:
        for g in TABLES:
            rows = census(f"{v}/acs/acs5", {"get": f"group({g})", "for": "county:*", "in": "state:13"}, RAW / "acs" / f"{g}_{v}_ga_county.json")
            print(v, g, len(rows) - 1, "Georgia counties")
    for y in range(2000, 2026):
        fetch(f"https://www2.census.gov/econ/bps/County/co{y}a.txt", RAW / "bps" / f"co{y}a.txt")
    print("permits 2000-2025")
    for v, counties in PUMAS.items():
        for c, ps in counties.items():
            for p in ps:
                # the microdata API returns person rows; SPORDER=1 keeps the householder, one row per renter household
                for k, get in enumerate(PUMS_VARS[v]):
                    rows = census(f"{v}/acs/acs5/pums", {"get": get, "for": f"public use microdata area:{p}", "in": "state:13", "TEN": "3", "SPORDER": "1"},
                                  RAW / "pums" / f"{v}_{p}_{k}.json")
                print(v, c, p, len(rows) - 1, "renter households")


if __name__ == "__main__":
    main()
