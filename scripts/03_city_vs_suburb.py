"""Test 2: inside each large metro, did rentals within reach disappear faster in the central city or in
the rest of the metro?

County lines blur the city line (Fulton holds Atlanta and suburbs; part of Atlanta is in DeKalb), so this
test uses the city itself: the largest principal city of each metro of 1 million or more (OMB July 2023,
first name in the metro title), at Census place level.

One income line for everyone in the metro: the metro's renter median household income (read from the
summed B25118 renter income buckets of its counties), after taxes in the city's state (married, no
children), with rent at 30% of income. The share is the share of cash-rent units at or under that rent.
The rest of the metro is the metro's county totals minus the city. Metro county lists are the 2023 lists,
held fixed for every period and built from the tool's harmonized county units.

Output: research/test2-cities-output.txt, data/processed/test2_metros.csv"""
import csv
import importlib.util
import io
import json
import re
import sys
from contextlib import redirect_stdout
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
AH = Path.home() / "PycharmProjects" / "AffordableHousing"
sys.path.insert(0, str(AH / "scripts"))
from common import PROC, RENT_EDGES, RENTER_EDGES, census  # noqa: E402

spec = importlib.util.spec_from_file_location("tieout", AH / "scripts" / "10_tieout.py")
T0 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(T0)

FK = ["2009", "2014", "2019", "2024"]
LABEL = {"2009": "2005-09", "2014": "2010-14", "2019": "2015-19", "2024": "2020-24"}
RAW = ROOT / "data" / "raw"
OUT = ROOT / "data" / "processed"
GROUPS = ["B25063", "B25118", "B25119"]
ATLANTA = "Atlanta-Sandy Springs-Roswell, GA"


def fetch():
    for v in FK:
        for g in GROUPS:
            census(f"{v}/acs/acs5", {"get": f"group({g})", "for": "place:*", "in": "state:*"}, RAW / "acs" / f"{g}_{v}_place.json")


def read_places(v, wanted):
    """Bucket records for the wanted (state, place) codes in one ACS release."""
    nr = len(RENT_EDGES[v])
    tabs = {}
    for g in GROUPS:
        j = json.loads((RAW / "acs" / f"{g}_{v}_place.json").read_text())
        h = {c: i for i, c in enumerate(j[0])}
        for row in j[1:]:
            code = row[h["state"]] + row[h["place"]]
            if code in wanted:
                tabs.setdefault(code, {"name": row[h["NAME"]]}).update({c: row[i] for c, i in h.items() if c.startswith(g)})
    out = {}
    for code, t in tabs.items():
        r = [int(t[f"B25063_{i:03d}E"]) for i in range(3, 3 + nr)]
        nc = int(t[f"B25063_{3 + nr:03d}E"])
        assert int(t["B25063_001E"]) == sum(r) + nc, (v, code)
        ti = [int(t[f"B25118_{i:03d}E"]) for i in range(15, 26)]
        assert sum(ti) == int(t["B25118_014E"]), (v, code)
        ri, rm = float(t["B25119_003E"]), float(t["B25119_003M"])
        out[code] = {"name": t["name"], "r": r, "nc": nc, "ti": ti, "ri": ri if ri > 0 else None, "rm": rm if rm > 0 else None}
    return out


def principal_cities():
    """Largest principal city of each 1M+ metro: the List 2 city named first in the metro title."""
    nchs = pd.read_csv(RAW / "nchs" / "NCHSUR2023_3156.csv", encoding="latin-1")
    nchs["fips"] = nchs.STFIPS.map("{:02d}".format) + nchs.CTYFIPS.map("{:03d}".format)
    big = nchs[nchs.CODE2023.isin([1, 2]) & nchs.CTYPOP.notna()]  # deleted counties (old Connecticut) have no population
    l2 = pd.read_excel(RAW / "omb" / "list2_2023.xlsx", header=2, dtype=str).dropna(subset=["FIPS Place Code"])
    out = {}
    for title, g in big.groupby("CBSATITLE"):
        first = re.split(r"[-,]", title)[0].strip()
        cand = l2[l2["CBSA Title"] == title]
        hit = cand[cand["Principal City Name"].str.startswith(first)]
        assert len(hit) >= 1, title
        out[title] = {"hits": {r["FIPS State Code"] + r["FIPS Place Code"]: r["Principal City Name"] for _, r in hit.iterrows()},
                      "counties": list(g.fips), "pop": int(g.CBSAPOP.iloc[0])}
    return out


def ceiling(tax, fk, st, ti):
    inc = T0.percentile(ti, RENTER_EDGES, 0.5)
    net = inc - T0.tax(tax, fk, 1, st, inc)
    return inc, 0.30 * net / 12


def pct(a, b):
    return 100 * (b / a - 1)


def main():
    fetch()
    H = json.loads((PROC / "harmonized.json").read_text())
    tax = json.loads((PROC / "tax_grid.json").read_text())
    pc = principal_cities()
    wanted = {c for m in pc.values() for c in m["hits"]}
    P = {fk: read_places(fk, wanted) for fk in FK}
    for d in pc.values():  # two cities can share the first name (Kansas City MO and KS): take the one with more rentals
        d["place"] = max(d["hits"], key=lambda c: sum(P["2024"][c]["r"]))
        d["city"] = d["hits"][d["place"]]

    print("Largest principal city of each metro of 1 million or more (check by hand):")
    for m, d in sorted(pc.items(), key=lambda kv: -kv[1]["pop"]):
        names = {P[fk][d["place"]]["name"] if d["place"] in P[fk] else "MISSING" for fk in FK}
        print(f"  {m[:44]:44s} {d['place']}  {d['city']}  | ACS names: {'; '.join(sorted(names))}")

    rows, tally, problems = [], {"suburb": 0, "city": 0}, []
    sums = {k: {fk: [0.0, 0] for fk in FK} for k in ("city", "rest")}
    detail = []
    for m, d in sorted(pc.items(), key=lambda kv: -kv[1]["pop"]):
        st = d["place"][:2]
        rec = {}
        for fk in FK:
            if d["place"] not in P[fk]:
                problems.append(f"{m}: city missing in {LABEL[fk]}")
                break
            c = P[fk][d["place"]]
            mr = [sum(H["units"][u]["f"][fk]["r"][i] for u in d["counties"]) for i in range(len(RENT_EDGES[fk]))]
            mti = [sum(H["units"][u]["f"][fk]["ti"][i] for u in d["counties"]) for i in range(11)]
            rest = [a - b for a, b in zip(mr, c["r"])]
            if min(rest) < 0:
                problems.append(f"{m} {LABEL[fk]}: rest-of-metro bucket below zero {rest}")
            inc, ceil = ceiling(tax, fk, st, mti)
            rec[fk] = {"inc": inc, "ceil": ceil, "city": 100 * T0.share(c["r"], RENT_EDGES[fk], ceil),
                       "rest": 100 * T0.share(rest, RENT_EDGES[fk], ceil), "city_n": sum(c["r"]), "rest_n": sum(rest),
                       "city_ri": c["ri"], "city_rm": c["rm"], "city_hh": sum(c["ti"]),
                       "city_ti_med": T0.percentile(c["ti"], RENTER_EDGES, 0.5), "rest_ti_med": T0.percentile([a - b for a, b in zip(mti, c["ti"])], RENTER_EDGES, 0.5)}
        if len(rec) < 4:
            continue
        for fk in FK:
            for k in ("city", "rest"):
                sums[k][fk][0] += rec[fk][k] * rec[fk][f"{k}_n"]
                sums[k][fk][1] += rec[fk][f"{k}_n"]
        cc, rc = pct(rec["2009"]["city"], rec["2024"]["city"]), pct(rec["2009"]["rest"], rec["2024"]["rest"])
        more = "suburb" if rc < cc else "city"
        tally[more] += 1
        detail.append((m, d, rec, cc, rc, more))
        rows.append({"metro": m, "city": d["city"], "place": d["place"], **{f"city_{k}": round(rec[k]["city"], 2) for k in FK},
                     **{f"rest_{k}": round(rec[k]["rest"], 2) for k in FK}, "city_chg_pct": round(cc, 1), "rest_chg_pct": round(rc, 1),
                     "rest_fell_more": more == "suburb", "city_share_of_metro_rentals_2024": round(100 * rec["2024"]["city_n"] / (rec["2024"]["city_n"] + rec["2024"]["rest_n"]), 1)})

    print("\nProblems: " + ("none" if not problems else ""))
    for p in problems:
        print("  " + p)

    print("\nAll large metros together (rental-weighted), share within reach of each metro's renter median")
    for k, name in (("city", "Largest principal cities"), ("rest", "Rest of their metros   ")):
        s = {fk: 100 * 0 + sums[k][fk][0] / sums[k][fk][1] for fk in FK}
        print(f"  {name} " + "  ".join(f"{LABEL[f]} {s[f]:5.1f}" for f in FK) + f"   change {s['2024'] - s['2009']:+5.1f} pts {pct(s['2009'], s['2024']):+4.0f}%")

    print("\nPer metro, 2005-09 -> 2020-24 (shares within reach of the metro renter median)")
    print(f"  {'metro':44s} {'city':>16s} {'chg':>5s}   {'rest of metro':>16s} {'chg':>5s}  rest fell more?  city % of metro rentals")
    for m, d, rec, cc, rc, more in detail:
        print(f"  {m[:44]:44s} {rec['2009']['city']:5.1f} -> {rec['2024']['city']:5.1f} {cc:+5.0f}%   {rec['2009']['rest']:5.1f} -> {rec['2024']['rest']:5.1f} {rc:+5.0f}%  "
              f"{'yes' if more == 'suburb' else 'no ':3s}              {100 * rec['2024']['city_n'] / (rec['2024']['city_n'] + rec['2024']['rest_n']):4.0f}%")
    n = tally["suburb"] + tally["city"]
    print(f"\n  Rest of metro fell more than the city in {tally['suburb']} of {n} metros ({100 * tally['suburb'] / n:.0f}%)")

    print("\nAtlanta detail")
    for m, d, rec, cc, rc, more in detail:
        if m != ATLANTA:
            continue
        for fk in FK:
            r = rec[fk]
            print(f"  {LABEL[fk]}: metro renter median ${r['inc']:,.0f}, rent ceiling ${r['ceil']:,.0f}/mo | city {r['city']:.1f}% of {r['city_n']:,} cash-rent units, "
                  f"rest {r['rest']:.1f}% of {r['rest_n']:,} | city renter households {r['city_hh']:,}, city renter median ${r['city_ri']:,.0f} (+/- ${r['city_rm']:,.0f}), "
                  f"from buckets: city ${r['city_ti_med']:,.0f}, rest ${r['rest_ti_med']:,.0f}")
        print("\n  Core counties at the same metro line (share within reach of the metro renter median), and each county's own renter median")
        print("  Fulton and DeKalb both hold part of the city of Atlanta, so their figures mix city and suburb")
        for u in ["13121", "13089", "13067", "13135", "13063", "13151", "13057"]:
            f = H["units"][u]["f"]
            s = {fk: 100 * T0.share(f[fk]["r"], RENT_EDGES[fk], rec[fk]["ceil"]) for fk in FK}
            print(f"    {H['units'][u]['name']:22s} " + " ".join(f"{s[k]:5.1f}" for k in FK) + f"  {pct(s['2009'], s['2024']):+5.0f}%"
                  f"   own renter median ${f['2009']['ri']:,.0f} -> ${f['2024']['ri']:,.0f} ({pct(f['2009']['ri'], f['2024']['ri']):+.0f}%)")
        r0, r1 = rec["2009"], rec["2024"]
        print(f"    {'Atlanta city':22s} {r0['city']:5.1f} ... {r1['city']:5.1f}  {pct(r0['city'], r1['city']):+5.0f}%   own renter median ${r0['city_ri']:,.0f} -> ${r1['city_ri']:,.0f} ({pct(r0['city_ri'], r1['city_ri']):+.0f}%)")
        print(f"    {'Metro renter median':22s} ${r0['inc']:,.0f} -> ${r1['inc']:,.0f} ({pct(r0['inc'], r1['inc']):+.0f}%)")

    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / "test2_metros.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    buf = io.StringIO()
    with redirect_stdout(buf):
        main()
    (ROOT / "research").mkdir(exist_ok=True)
    (ROOT / "research" / "test2-cities-output.txt").write_text(buf.getvalue())
    print(buf.getvalue())
