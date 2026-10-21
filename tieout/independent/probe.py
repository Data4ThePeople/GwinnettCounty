import sys, os, json, requests
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
c = cpi(); print({k: c[k] for k in (2009, 2014, 2019, 2024)}, len(c))
for y in (2009, 2024):
    for g in ("B25063", "B25032", "B14001", "B25118"):
        fp = download(f"https://api.census.gov/data/{y}/acs/acs5/groups/{g}.json", f"meta/{y}_{g}.json")
        v = json.load(open(fp))["variables"]
        ks = sorted(k for k in v if k.endswith("E"))
        print(y, g, len(ks))
        for k in ks:
            print("   ", k, v[k]["label"])
