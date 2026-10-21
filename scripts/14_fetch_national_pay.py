"""Download the data for the national renter-pay comparison (DATASETS.md section 13): Census 2000 PUMA equivalency
files for every state, and PUMS records of full-time year-round workers in renter households, every state, 2005-09
and 2020-24, filtered by the API. Cached; re-runs make no calls.

Output: data/raw/puma/PUMEQ5-XX.TXT, data/raw/pums_ftyr/*.json"""
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AH = Path.home() / "PycharmProjects" / "AffordableHousing"
sys.path.insert(0, str(AH / "scripts"))
from common import census, fetch  # noqa: E402

RAW = ROOT / "data" / "raw"
STATES = {"01": ("Alabama", "AL"), "02": ("Alaska", "AK"), "04": ("Arizona", "AZ"), "05": ("Arkansas", "AR"), "06": ("California", "CA"),
          "08": ("Colorado", "CO"), "09": ("Connecticut", "CT"), "10": ("Delaware", "DE"), "11": ("District_of_Columbia", "DC"),
          "12": ("Florida", "FL"), "13": ("Georgia", "GA"), "15": ("Hawaii", "HI"), "16": ("Idaho", "ID"), "17": ("Illinois", "IL"),
          "18": ("Indiana", "IN"), "19": ("Iowa", "IA"), "20": ("Kansas", "KS"), "21": ("Kentucky", "KY"), "22": ("Louisiana", "LA"),
          "23": ("Maine", "ME"), "24": ("Maryland", "MD"), "25": ("Massachusetts", "MA"), "26": ("Michigan", "MI"), "27": ("Minnesota", "MN"),
          "28": ("Mississippi", "MS"), "29": ("Missouri", "MO"), "30": ("Montana", "MT"), "31": ("Nebraska", "NE"), "32": ("Nevada", "NV"),
          "33": ("New_Hampshire", "NH"), "34": ("New_Jersey", "NJ"), "35": ("New_Mexico", "NM"), "36": ("New_York", "NY"),
          "37": ("North_Carolina", "NC"), "38": ("North_Dakota", "ND"), "39": ("Ohio", "OH"), "40": ("Oklahoma", "OK"), "41": ("Oregon", "OR"),
          "42": ("Pennsylvania", "PA"), "44": ("Rhode_Island", "RI"), "45": ("South_Carolina", "SC"), "46": ("South_Dakota", "SD"),
          "47": ("Tennessee", "TN"), "48": ("Texas", "TX"), "49": ("Utah", "UT"), "50": ("Vermont", "VT"), "51": ("Virginia", "VA"),
          "53": ("Washington", "WA"), "54": ("West_Virginia", "WV"), "55": ("Wisconsin", "WI"), "56": ("Wyoming", "WY")}
FILTERS = {"2009": {"TEN": "3,4", "ESR": "1,2,4,5", "WKHP": "35:99", "WKW": "1"},
           "2024": {"TEN": "3,4", "ESR": "1,2,4,5", "WKHP": "35:99", "WKWN": "50:52"}}
GETS = ["SERIALNO,SPORDER,PERNP,ADJINC,PWGTP"] + ["SERIALNO,SPORDER," + ",".join(f"PWGTP{i}" for i in range(a, a + 40)) for a in (1, 41)]


def one(job):
    v, st, k = job
    rows = census(f"{v}/acs/acs5/pums", {"get": GETS[k], "for": "public use microdata area:*", "in": f"state:{st}", **FILTERS[v]},
                  RAW / "pums_ftyr" / f"{v}_{st}_{k}.json")
    return v, st, k, len(rows) - 1


def main():
    for st, (name, ab) in STATES.items():
        base = f"https://www2.census.gov/census_2000/datasets/PUMS/FivePercent/{name}/PUMEQ5-"
        if not fetch(base + f"{ab}.TXT", RAW / "puma" / f"PUMEQ5-{ab}.TXT"):
            assert fetch(base + f"{st}.TXT", RAW / "puma" / f"PUMEQ5-{ab}.TXT"), st   # Wisconsin's file is named by FIPS code
    print("PUMEQ5 files:", len(STATES))
    jobs = [(v, st, k) for v in FILTERS for st in STATES for k in range(3)]
    with ThreadPoolExecutor(6) as ex:
        for v, st, k, n in ex.map(one, jobs):
            if k == 0:
                print(v, st, n, "full-time year-round renter workers")


if __name__ == "__main__":
    main()
