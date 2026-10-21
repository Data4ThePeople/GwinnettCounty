"""Tool share within reach per county (median renter hh, married no children, after taxes, 30%)."""
from c2 import *
import pandas as pd
GRID = json.load(open(os.path.join(AH, "tax_grid.json"))); GI = np.array(GRID["inc"], float)
INC_E = [0, 5000, 10000, 15000, 20000, 25000, 35000, 50000, 75000, 100000, 150000]
def redges(y):
    e = [0, 100] + list(range(150, 800, 50)) + [800, 900, 1000, 1250, 1500, 2000]
    return e + ([2500, 3000, 3500] if y >= 2019 else [])
def tax(y, st, inc):
    t = np.array(GRID["tax"][str(y)]["1"][st], float)
    if inc >= GI[-1]: return t[-1] * inc / GI[-1]
    return float(np.interp(inc, GI, t))
def amount(y, st, med):
    return 0.30 * (med - tax(y, st, med)) / 12
def share_at(counts, edges, c):
    tot = sum(counts); cum = 0.0
    for i, n in enumerate(counts):
        lo = edges[i]; hi = edges[i + 1] if i + 1 < len(edges) else None
        if hi is None: return cum / tot   # open top bucket: 'at least'
        if c >= hi: cum += n; continue
        if c > lo: cum += n * (c - lo) / (hi - lo)
        return cum / tot
    return cum / tot
def bmed(counts, edges):
    tot = sum(counts); h = tot / 2; cum = 0
    for i, n in enumerate(counts):
        if n > 0 and cum + n >= h:
            return edges[i] + (h - cum) / n * (edges[i + 1] - edges[i]) if i + 1 < len(edges) else None
        cum += n
JOIN = {"02063": "AKcc", "02066": "AKcc", "02261": "AKcc", "02195": "AKph", "02105": "AKph", "02198": "AKph",
        "51515": "51019", "46113": "46102", "02270": "02158"}
def units(y):
    A = json.load(open(os.path.join(RAW, f"acs_{y}.json")))
    nb = 21 if y == 2009 else 24
    U = {}
    for g, v in A.items():
        if g.startswith("72"): continue
        u = JOIN.get(g, g)
        r = U.setdefault(u, dict(mem=[], r=np.zeros(nb), ti=np.zeros(11), tot=0., m2=0., cn=0., cd=0., st=g[:2]))
        r["mem"].append(g); r["name"] = v["NAME"]
        r["r"] += np.array([v[f"B25063_{i:03d}E"] for i in range(3, 3 + nb)])
        r["ti"] += np.array([v[f"B25118_{i:03d}E"] for i in range(15, 26)])
        r["tot"] += v["B25063_001E"]; r["m2"] += (v["B25063_001M"] or 0) ** 2
        r["med"] = v["B25119_003E"]; r["mm"] = v["B25119_003M"]; r["rent"] = v["B25064_001E"]
        if v.get("B14001_001E"): r["cn"] += v["B14001_008E"] + v["B14001_009E"]; r["cd"] += v["B14001_001E"]
    for u, r in U.items():
        if len(r["mem"]) > 1 or not r["med"] or r["med"] <= 0:
            r["med"] = bmed(list(r["ti"]), INC_E); r["mm"] = None; r["est"] = True
        else: r["est"] = False
        r["cash"] = float(r["r"].sum())
        cv = (np.sqrt(r["m2"]) / 1.645) / r["tot"] if r["tot"] else 9
        r["lo"] = r["cash"] < 200 or cv > 0.30 or (r["mm"] is not None and r["mm"] > 0.25 * r["med"])
        r["college"] = r["cd"] > 0 and r["cn"] / r["cd"] >= 0.15
        if r["med"] and r["cash"]:
            r["amt"] = amount(y, r["st"], r["med"]); r["share"] = share_at(list(r["r"]), redges(y), r["amt"])
        else: r["share"] = None
    return U
if __name__ == "__main__":
    U24, U09 = units(2024), units(2009)
    col24 = {u for u, r in U24.items() if r["college"]}
    fp = fetch("https://www2.census.gov/programs-surveys/metro-micro/geographies/reference-files/2023/delineation-files/list1_2023.xlsx", "omb/list1_2023.xlsx")
    L = pd.read_excel(fp, header=2, dtype=str)
    atl = sorted((L[L["CBSA Code"] == "12060"]["FIPS State Code"] + L[L["CBSA Code"] == "12060"]["FIPS County Code"]).tolist())
    print("college units 2024:", len(col24), "| Atlanta counties:", len(atl))
    out = {"atl": []}
    for f in sorted(atl, key=lambda f: U24[f]["share"]):
        r = U24[f]; out["atl"].append((f, r["name"], 100 * r["share"], r["amt"], r["cash"], r["lo"], r["college"]))
        print(f"  {f} {r['name'][:-17]:12s} share {100*r['share']:5.2f}  amt {r['amt']:7.1f}  cash {r['cash']:7.0f} lo {r['lo']} col {r['college']}")
    ranked = sorted([(r["share"], u, r["name"]) for u, r in U24.items() if r["share"] is not None and r["cash"] >= 1000 and not r["lo"]])
    nc = [x for x in ranked if x[1] not in col24]
    print("ranked units:", len(ranked), "excluding college:", len(nc))
    print("lowest 15 (no college):")
    for i, (s, u, n) in enumerate(nc[:15]): print(f"  {i+1:2d} {u} {n:40s} {100*s:5.2f} {'ATL' if u in atl else ''}")
    print("ATL in lowest 10:", sum(1 for x in nc[:10] if x[1] in atl))
    print("lowest 8 incl college:", [(n, round(100*s,2), u in col24) for s, u, n in ranked[:8]])
    g4, g9 = U24["13135"], U09["13135"]
    print(f"Gwinnett 2024 med {g4['med']} amt {g4['amt']:.2f} share {100*g4['share']:.2f} | 2009 med {g9['med']} amt {g9['amt']:.2f} (x CPI {g9['amt']*F09:.2f}) share {100*g9['share']:.2f}")
    print("CPI factor", F09)
    out.update(nc10=[(u, n, 100 * s) for s, u, n in nc[:10]], gw={"2024": g4["amt"], "2009": g9["amt"]}, F09=F09)
    json.dump(out, open(os.path.join(HERE, "out_reach.json"), "w"), indent=1)
