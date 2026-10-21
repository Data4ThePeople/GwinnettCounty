"""Download the data for "why did renter income lag": PUMS person records for renter households (DATASETS.md
section 11) and QCEW average annual pay by county with annual CPI-U (section 12). Cached; re-runs make no calls.

Output: data/raw/pums_people/*.json, data/raw/qcew/*.json"""
import json
import os
import sys
from importlib import import_module
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
AH = Path.home() / "PycharmProjects" / "AffordableHousing"
sys.path.insert(0, str(AH / "scripts"))
from common import census  # noqa: E402

sys.path.insert(0, os.path.expanduser("~/.claude/d4tp-process"))
from d4tp_env import get_key, load_env  # noqa: E402

PUMAS = import_module("04_fetch_county_tables").PUMAS
RAW = ROOT / "data" / "raw"
BASE = "SERIALNO,SPORDER,TEN,NP,HINCP,ADJINC,WGTP,AGEP,ESR,PERNP,WAGP,WKHP,NATIVITY,HISP,RAC1P,SCHL,COW,INDP,PWGTP"
GETS = {"2009": [BASE + ",WKW"], "2024": [BASE + ",WKWN"]}
for _v in GETS:
    GETS[_v] += ["SERIALNO,SPORDER," + ",".join(f"{w}{i}" for i in range(a, a + 40)) for w in ("WGTP", "PWGTP") for a in (1, 41)]
QCEW = ["13135", "13121", "13089", "13067", "13063", "13151", "13057", "13117"]
UA = {"User-Agent": "Mozilla/5.0 (Data 4 The People research; eric@asaltollc.com)"}


def bls(ids, dest):
    if not dest.exists():
        load_env()
        r = requests.post("https://api.bls.gov/publicAPI/v2/timeseries/data/", headers=UA, timeout=120,
                          json={"seriesid": ids, "startyear": "2005", "endyear": "2024", "annualaverage": True,
                                "registrationkey": get_key("BLS_API_KEY")}).json()
        assert r["status"] == "REQUEST_SUCCEEDED", r.get("message")
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(json.dumps(r))
    return json.loads(dest.read_text())


def main():
    for v, counties in PUMAS.items():
        for c, ps in counties.items():
            for p in ps:
                for k, get in enumerate(GETS[v]):
                    rows = census(f"{v}/acs/acs5/pums", {"get": get, "for": f"public use microdata area:{p}", "in": "state:13", "TEN": "3,4"},
                                  RAW / "pums_people" / f"{v}_{p}_{k}.json")
                print(v, c, p, len(rows) - 1, "people in renter households")
    r = bls([f"ENU{f}50010" for f in QCEW] + ["CUUR0000SA0"], RAW / "qcew" / "qcew_pay_cpi_2005_2024.json")
    for s in r["Results"]["series"]:
        print(s["seriesID"], len(s["data"]), "values")


if __name__ == "__main__":
    main()
