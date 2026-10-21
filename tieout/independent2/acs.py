"""Pull county ACS 5-yr tables, 2009 and 2024."""
from c2 import *
def pull(y):
    nb = 21 if y == 2009 else 24
    groups = [[f"B25063_{i:03d}E" for i in range(1, nb + 4)] + ["B25063_001M", "B25063_002M"],
              ["B25119_003E", "B25119_003M", "B25064_001E", "B25064_001M", "B25003_001E", "B25003_003E"]
              + [f"B25118_{i:03d}E" for i in range(14, 26)],
              ["B14001_001E", "B14001_008E", "B14001_009E"]]
    out = {}
    for g in groups:
        for r in api(f"{y}/acs/acs5", {"get": "NAME," + ",".join(g), "for": "county:*", "in": "state:*"}):
            d = out.setdefault(r["state"] + r["county"], {"NAME": r["NAME"]})
            for v in g: d[v] = float(r[v]) if r[v] not in (None, "") else None
    json.dump(out, open(os.path.join(RAW, f"acs_{y}.json"), "w"))
    return out
for y in (2009, 2024):
    o = pull(y); print(y, len(o), o["13135"]["NAME"], o["13135"]["B25119_003E"], o["13135"]["B25064_001E"])
# labels check
for y in (2009, 2024):
    for t in ("B25063", "B14001", "B25036"):
        fetch(f"https://api.census.gov/data/{y}/acs/acs5/groups/{t}.json", f"meta/{y}_{t}.json")
    j = json.load(open(os.path.join(RAW, f"meta/{y}_B25063.json")))["variables"]
    print(y, [(k, j[k]["label"]) for k in sorted(j) if k.endswith("E") and k[-4:-1] in ("002","003","023","024","025","026","027")])
    j = json.load(open(os.path.join(RAW, f"meta/{y}_B14001.json")))["variables"]
    print(y, [(k, j[k]["label"]) for k in sorted(j) if k.endswith("E")][:10])
