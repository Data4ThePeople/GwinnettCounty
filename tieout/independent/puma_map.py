"""County -> PUMA lists for the 2000 PUMAs (2005-09 PUMS) and 2020 PUMAs (2020-24 PUMS), with a nesting check."""
import sys, os, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
peers = {"135": "Gwinnett", "067": "Cobb", "089": "DeKalb", "121": "Fulton", "151": "Henry", "057": "Cherokee", "063": "Clayton", "117": "Forsyth"}
fp = download("https://www2.census.gov/census_2000/datasets/PUMS/FivePercent/Georgia/PUMEQ5-GA.TXT", "puma/PUMEQ5-GA.TXT")
p2c = collections.defaultdict(set)
for ln in open(fp, encoding="latin-1"):
    t = ln.split()
    if t and t[0] == "781" and len(t) > 4 and t[1] == "13":
        p2c[t[3]].add(t[4])
fp2 = download("https://www2.census.gov/geo/docs/maps-data/data/rel2020/2020_Census_Tract_to_2020_PUMA.txt", "puma/tract2020_puma2020.txt")
p2c20 = collections.defaultdict(set)
for ln in open(fp2, encoding="utf-8-sig"):
    t = ln.strip().split(",")
    if t[0] == "13":
        p2c20[t[3]].add(t[1])
out = {}
for per, m in (("2009", p2c), ("2024", p2c20)):
    out[per] = {}
    for c, n in peers.items():
        pumas = sorted(p for p, cs in m.items() if c in cs)
        nest = all(m[p] == {c} for p in pumas)
        print(per, n, pumas, "nests" if nest else "DOES NOT NEST: " + str({p: sorted(m[p]) for p in pumas}))
        if nest: out[per][n] = pumas
json.dump(out, open(os.path.join(HERE, "pumas.json"), "w"), indent=1)
