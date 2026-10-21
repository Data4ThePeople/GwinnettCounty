"""Rentals Within Reach default (median renter household, after taxes, married no children, 30%), own code."""
import sys, os, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *

YEARS = (2009, 2014, 2019, 2024)
GRID = json.load(open(os.path.expanduser("~/PycharmProjects/AffordableHousing/data/processed/tax_grid.json")))
TINC = np.array(GRID["inc"], float)
INC_EDGES = [0, 5000, 10000, 15000, 20000, 25000, 35000, 50000, 75000, 100000, 150000]

def rent_edges(y):
    e = [0, 100] + list(range(150, 800, 50)) + [800, 900, 1000, 1250, 1500, 2000]
    if y >= 2019:
        e += [2500, 3000, 3500]
    return e

def tax(y, st, inc):
    t = np.array(GRID["tax"][str(y)]["1"][st], float)
    if inc <= 0: return 0.0
    if inc >= TINC[-1]: return t[-1] / TINC[-1] * inc
    return float(np.interp(inc, TINC, t))

def share(r, edges, c):
    tot = sum(r); cum = 0.0
    for i, n in enumerate(r):
        a = edges[i]; b = edges[i + 1] if i + 1 < len(edges) else None
        if b is None:
            return cum / tot, (c >= a)
        if c >= b: cum += n; continue
        if c <= a: return cum / tot, False
        return (cum + n * (c - a) / (b - a)) / tot, False
    return cum / tot, False

def bucket_median(counts, edges):
    tot = sum(counts); half = tot / 2; cum = 0
    for i, n in enumerate(counts):
        if cum + n >= half and n > 0:
            if i + 1 >= len(edges): return None
            return edges[i] + (half - cum) / n * (edges[i + 1] - edges[i])
        cum += n
    return None

# unit definitions on 2024 boundaries (only joins that touch 2020-24 matter for ranking)
JOIN = {"02063": "AK-CHUGACH-COPPER", "02066": "AK-CHUGACH-COPPER", "02261": "AK-CHUGACH-COPPER",
        "02195": "AK-PET-HA-POW", "02105": "AK-PET-HA-POW", "02198": "AK-PET-HA-POW",
        "51515": "51019", "46113": "46102", "02270": "02158"}

def units(y):
    d = json.load(open(os.path.join(HERE, f"acs_{y}.json")))
    nb = 21 if y in (2009, 2014) else 24
    U = {}
    for g, v in d.items():
        if g == "us" or g.startswith("72"):
            continue
        u = JOIN.get(g, g)
        rec = U.setdefault(u, {"members": [], "r": np.zeros(nb), "ti": np.zeros(11), "tot": 0.0, "totM2": 0.0,
                               "col_num": 0.0, "col_den": 0.0, "st": g[:2]})
        rec["members"].append(g)
        rec["r"] += np.array([v[f"B25063_{i:03d}E"] for i in range(3, 3 + nb)])
        rec["ti"] += np.array([v[f"B25118_{i:03d}E"] for i in range(15, 26)])
        rec["tot"] += v["B25063_001E"]; rec["totM2"] += (v["B25063_001M"] or 0) ** 2
        rec["name"] = v["NAME"]
        rec["med_pub"] = v["B25119_003E"]; rec["med_moe"] = v["B25119_003M"]
        if v.get("B14001_001E"):
            rec["col_num"] += v["B14001_008E"] + v["B14001_009E"]; rec["col_den"] += v["B14001_001E"]
    for u, rec in U.items():
        joined = len(rec["members"]) > 1
        med = rec["med_pub"] if (not joined and rec["med_pub"] and rec["med_pub"] > 0) else None
        rec["est"] = med is None
        if med is None:
            med = bucket_median(list(rec["ti"]), INC_EDGES)
            rec["med_moe"] = None
        rec["med"] = med
        rec["cash"] = float(rec["r"].sum())
        se = np.sqrt(rec["totM2"]) / 1.645
        cv = se / rec["tot"] if rec["tot"] else 9
        thin_inc = (not rec["est"]) and rec["med_moe"] is not None and rec["med_moe"] > 0 and rec["med_moe"] / rec["med"] > 0.25
        rec["lo"] = rec["cash"] < 200 or cv > 0.30 or thin_inc
        rec["cv"] = cv; rec["thin_inc"] = thin_inc
        if rec["med"] is None or rec["cash"] == 0:
            rec["share"] = None; continue
        net = rec["med"] - tax(y, rec["st"], rec["med"])
        rec["ceil"] = 0.30 * net / 12
        rec["share"], rec["top"] = share(list(rec["r"]), rent_edges(y), rec["ceil"])
    return U

if __name__ == "__main__":
    res = {}
    U24 = units(2024)
    college = {u for u, r in U24.items() if r["col_den"] and r["col_num"] / r["col_den"] >= 0.15}
    print("college counties (2024, >=15%):", len(college))
    for y in YEARS:
        U = units(y)
        num = sum(r["share"] * r["cash"] for r in U.values() if r["share"] is not None)
        den = sum(r["cash"] for r in U.values() if r["share"] is not None)
        g = U["13135"]
        print(y, "national", round(100 * num / den, 3), "units", len(U), "| Gwinnett share", round(100 * g["share"], 3),
              "med", g["med"], "ceil", round(g["ceil"], 1), "cash", g["cash"], "within", round(g["share"] * g["cash"]))
        res[y] = {"nat": 100 * num / den, "gw": 100 * g["share"], "gw_cash": g["cash"], "gw_ceil": g["ceil"], "gw_med": g["med"],
                  "clay": 100 * U["13063"]["share"]}
    # ranking 2020-24
    rows = [(r["share"], u, r["name"]) for u, r in U24.items()
            if r["share"] is not None and r["cash"] >= 1000 and not r["lo"]]
    rows.sort()
    nocol = [x for x in rows if x[1] not in college]
    def rank(lst):
        return [i for i, x in enumerate(lst) if x[1] == "13135"][0] + 1, len(lst)
    print("rank no college:", rank(nocol), "with college:", rank(rows))
    print("lowest 12 no college:")
    for s, u, n in nocol[:12]: print("  ", u, n, round(100 * s, 2), "college" if u in college else "")
    print("lowest 5 with college:")
    for s, u, n in rows[:5]: print("  ", u, n, round(100 * s, 2), "college" if u in college else "")
    lo_big = [(u, r["name"], r["cv"], r["thin_inc"]) for u, r in U24.items() if r["cash"] >= 1000 and r["lo"]]
    print("1000+ but lo in 2024:", len(lo_big))
    est_big = [(u, r["name"]) for u, r in U24.items() if r["cash"] >= 1000 and r["est"]]
    print("1000+ with estimated median:", est_big)
    print("top-bucket ceilings 2024:", [u for u, r in U24.items() if r.get("top")])
    res["rank"] = {"nocol": rank(nocol), "col": rank(rows), "low_nocol": [(n, 100 * s) for s, u, n in nocol[:10]]}
    json.dump(res, open(os.path.join(HERE, "out_reach.json"), "w"), indent=1, default=str)
