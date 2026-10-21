import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
fp = download("https://api.census.gov/data/2009/acs/acs5/groups/B25036.json", "meta/2009_B25036.json")
v = json.load(open(fp))["variables"]
ks = sorted(k for k in v if k.endswith("E") and k.startswith("B25036"))
r = census("2009/acs/acs5", {"get": ",".join(ks), "for": "county:135", "in": "state:13"})[0]
for k in ks: print(k, v[k]["label"].split("!!")[-2:], r[k])
