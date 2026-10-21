"""C1-C4, D3, D4, E7 from ACS county tables, OMB list, FHFA, BPS and QCEW."""
import sys, os, json, csv
import numpy as np, pandas as pd, requests
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
C = cpi(); f09 = C[2024] / C[2009]
a09 = json.load(open(os.path.join(HERE, "acs_2009.json"))); a24 = json.load(open(os.path.join(HERE, "acs_2024.json")))
out = {}
# C1
g9, g4 = a09["13135"], a24["13135"]
rent = g4["B25064_001E"] / (g9["B25064_001E"] * f09) - 1
inc = g4["B25119_003E"] / (g9["B25119_003E"] * f09) - 1
print(f"C1 Gwinnett rent {g9['B25064_001E']}->{g4['B25064_001E']} real {100*rent:.2f}% ; renter inc {g9['B25119_003E']}->{g4['B25119_003E']} real {100*inc:.2f}%")
# margin on income change (approx: ratio MOE formula)
r = g4["B25119_003E"] / g9["B25119_003E"]
moe_ratio = np.sqrt(g4["B25119_003M"]**2 + r**2 * g9["B25119_003M"]**2) / g9["B25119_003E"]
print(f"   90% MOE on renter income change approx +/- {100*moe_ratio*f09**-1*1:.1f} pts nominal-ratio basis; real pts {100*moe_ratio/f09:.1f}")
# C2
L = pd.read_excel(os.path.join(RAW, "omb/list1_2023.xlsx"), header=2, dtype=str)
atl = L[L["CBSA Code"] == "12060"]
fips = sorted(atl["FIPS State Code"] + atl["FIPS County Code"])
print("Atlanta metro counties:", len(fips))
rows = []
for f in fips:
    x9, x4 = a09[f], a24[f]
    rc = x4["B25064_001E"] / (x9["B25064_001E"] * f09) - 1
    ic = x4["B25119_003E"] / (x9["B25119_003E"] * f09) - 1
    rows.append((x4["NAME"].replace(" County, Georgia", ""), x4["B25003_003E"], 100 * rc, 100 * ic, 100 * (rc - ic)))
big = sorted([r for r in rows if r[1] >= 10000], key=lambda r: -r[4])
print("large metro counties:", len(big))
for i, r in enumerate(big): print(f"  {i+1:2d} {r[0]:10s} renters {r[1]:>8.0f} rent {r[2]:6.1f} inc {r[3]:6.1f} gap {r[4]:6.1f}")
out["C2"] = big
# C3
for k, x in (("Gwinnett", g4), ("US", a24["us"])):
    print(f"C3 {k} renter/owner median 2020-24: {100*x['B25119_003E']/x['B25119_002E']:.1f}%  ({x['B25119_003E']}/{x['B25119_002E']})")
# C4 FHFA
H = pd.read_excel(os.path.join(RAW, "fhfa/hpi_at_county.xlsx"), header=5, dtype=str)
print(H.columns.tolist()[:8])
H["FIPS code"] = H["FIPS code"].str.zfill(5)
for f, n in (("13135", "Gwinnett"), ("13067", "Cobb"), ("13121", "Fulton"), ("13089", "DeKalb")):
    s = H[H["FIPS code"] == f].copy(); s["Year"] = s["Year"].astype(int); s["HPI"] = pd.to_numeric(s["HPI"], errors="coerce")
    a = s[s.Year.between(2005, 2009)].HPI.mean(); b = s[s.Year.between(2020, 2024)].HPI.mean()
    print(f"C4 FHFA {n}: avg05-09 {a:.2f} avg20-24 {b:.2f} change {100*(b/a-1):.1f}%")
# D3 permits
peers = {"13121": "Fulton", "13089": "DeKalb", "13067": "Cobb", "13063": "Clayton", "13151": "Henry", "13057": "Cherokee", "13117": "Forsyth", "13135": "Gwinnett"}
perm = {f: 0 for f in peers}; rep = {f: 0 for f in peers}
for y in range(2007, 2022):
    with open(os.path.join(RAW, f"bps/co{y}a.txt")) as fh:
        for row in csv.reader(fh):
            if len(row) < 30 or not row[1].strip().isdigit(): continue
            f = row[1].strip().zfill(2) + row[2].strip().zfill(3)
            if f in perm:
                perm[f] += sum(int(row[i]) for i in (7, 10, 13, 16))
                rep[f] += sum(int(row[i]) for i in (19, 22, 25, 28))
d3 = []
for f, n in peers.items():
    add = a24[f]["B11001_001E"] - a09[f]["B11001_001E"]
    d3.append((n, perm[f], add, perm[f] / add, perm[f] - rep[f]))
d3.sort(key=lambda r: -r[3])
for r in d3: print(f"D3 {r[0]:9s} permits {r[1]:>7d} added hh {r[2]:>8.0f} ratio {r[3]:.3f}  (imputed {r[4]})")
# D4
for k, x in (("2005-09", g9), ("2020-24", g4)):
    print(f"D4 Gwinnett single-family share of renter units {k}: {100*(x['B25032_014E']+x['B25032_015E'])/x['B25032_013E']:.1f}%")
# E7 QCEW
fp = os.path.join(RAW, "bls", "qcew.json")
ser = {f"ENU{f}50010": n for f, n in peers.items()}
if not os.path.exists(fp):
    body = {"seriesid": list(ser), "startyear": "2005", "endyear": "2024", "registrationkey": get_key("BLS_API_KEY")}
    rr = requests.post("https://api.bls.gov/publicAPI/v2/timeseries/data/", json=body, headers=UA, timeout=120)
    rr.raise_for_status(); open(fp, "w").write(rr.text)
Q = json.load(open(fp))
print("BLS status", Q["status"], Q.get("message"))
e7 = []
for s in Q["Results"]["series"]:
    v = {int(d["year"]): float(d["value"].replace(",", "")) for d in s["data"]}
    assert all(y in v for y in range(2005, 2025)), (s["seriesID"], sorted(v))
    a = np.mean([v[y] * C[2024] / C[y] for y in range(2005, 2010)]); b = np.mean([v[y] * C[2024] / C[y] for y in range(2020, 2025)])
    e7.append((ser[s["seriesID"]], a, b, 100 * (b / a - 1), s["data"][0]["period"]))
e7.sort(key=lambda r: -r[3])
for i, r in enumerate(e7): print(f"E7 {i+1} {r[0]:9s} {r[1]:9.0f} -> {r[2]:9.0f}  {r[3]:5.1f}%  period {r[4]}")
