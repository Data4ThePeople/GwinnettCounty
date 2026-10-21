"""Pull county + nation ACS 5-year tables for 2009, 2014, 2019, 2024. Saves acs_<year>.json (dict geoid -> vars)."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

def vlist(y):
    nb = 23 if y in (2009, 2014) else 26
    rent = [f"B25063_{i:03d}E" for i in range(1, nb + 2)] + ["B25063_001M", "B25063_002M"]
    inc = ["B25119_001E", "B25119_002E", "B25119_003E", "B25119_001M", "B25119_002M", "B25119_003M"]
    ti = [f"B25118_{i:03d}E" for i in range(14, 26)]
    other = ["B25064_001E", "B25064_001M", "B25003_001E", "B25003_002E", "B25003_003E", "B11001_001E",
             "B25032_013E", "B25032_014E", "B25032_015E"]
    col = ["B14001_001E", "B14001_008E", "B14001_009E"]
    return [rent, inc + ti, other + col]

out = {}
for y in (2009, 2014, 2019, 2024):
    data = {}
    for chunk in vlist(y):
        for geo in ({"for": "county:*", "in": "state:*"}, {"for": "us:1"}):
            rows = census(f"{y}/acs/acs5", dict(get="NAME," + ",".join(chunk), **geo))
            for r in rows:
                gid = "us" if "us" in r else r["state"] + r["county"]
                d = data.setdefault(gid, {"NAME": r["NAME"]})
                for v in chunk:
                    x = r.get(v)
                    d[v] = None if x in (None, "") else float(x)
    json.dump(data, open(os.path.join(HERE, f"acs_{y}.json"), "w"))
    print(y, len(data), data["13135"]["NAME"], data["13135"]["B25119_003E"], data["13135"]["B25063_002E"])
