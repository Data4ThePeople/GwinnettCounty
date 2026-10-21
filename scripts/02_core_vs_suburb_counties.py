"""Test 1: do suburban counties in large metros lose more affordability than central counties?

Uses the Rentals Within Reach measure exactly as the tool computes it (each county's own renter
median, after taxes, married no children, rent at 30% of income) and the NCHS 2023 urban-rural codes:
1 = large central metro, 2 = large fringe metro, both in metros of 1 million or more. The 2023 codes are
held fixed for all four periods.

For each large metro, the share within reach in its central counties and in its fringe counties is the
rental-weighted average of the county shares, built like nation() in the tool's tie-out script.

Birmingham, AL has no county coded central; it is left out, and a check codes Jefferson County as central.

Output: research/test1-counties-output.txt, data/processed/test1_metros.csv"""
import csv
import importlib.util
import io
import json
import sys
from contextlib import redirect_stdout
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
AH = Path.home() / "PycharmProjects" / "AffordableHousing"
sys.path.insert(0, str(AH / "scripts"))
from common import COLLEGE_SHARE, PROC, RENT_EDGES  # noqa: E402

spec = importlib.util.spec_from_file_location("tieout", AH / "scripts" / "10_tieout.py")
T0 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(T0)

FK = ["2009", "2014", "2019", "2024"]
LABEL = {"2009": "2005-09", "2014": "2010-14", "2019": "2015-19", "2024": "2020-24"}
NCHS = ROOT / "data" / "raw" / "nchs" / "NCHSUR2023_3156.csv"
OUT = ROOT / "data" / "processed"
ATLANTA = "Atlanta-Sandy Springs-Roswell, GA"
CORE11 = ["13121", "13089", "13067", "13135", "13063", "13151", "13247", "13097", "13113", "13117", "13057"]


def load():
    H = json.loads((PROC / "harmonized.json").read_text())
    tax = json.loads((PROC / "tax_grid.json").read_text())
    n = pd.read_csv(NCHS, encoding="latin-1", dtype={"STFIPS": int, "CTYFIPS": int})
    n["fips"] = n.STFIPS.map("{:02d}".format) + n.CTYFIPS.map("{:03d}".format)
    big = n[n.CODE2023.isin([1, 2])]
    missing = sorted(set(big.fips) - set(H["units"]))
    # deleted Connecticut counties carry 2013 codes; the tool uses the planning regions, which are also in the file
    missing = [f for f in missing if not (f.startswith("09") and int(f[2:]) < 100)]
    big = big[big.fips.isin(H["units"])]
    return H, tax, big, missing


def county_share(H, tax, uid, fk):
    info = H["units"][uid]
    x = info["f"][fk]
    inc = T0.income(x, fk, 5)
    net = inc - T0.tax(tax, fk, 1, info["st"], inc)
    return T0.share(x["r"], RENT_EDGES[fk], 0.30 * net / 12), sum(x["r"])


def group_share(H, tax, uids, fk, nocollege=False):
    a = t = 0
    for u in uids:
        if nocollege and H["units"][u]["college"] >= COLLEGE_SHARE:
            continue
        s, n = county_share(H, tax, u, fk)
        a += s * n
        t += n
    return 100 * a / t if t else None


def pct(a, b):
    return 100 * (b / a - 1)


def run(H, tax, big, nocollege, rows=None):
    tag = "college counties left out" if nocollege else "college counties included (page default)"
    print(f"\n=== {tag}")
    nat = {c: {fk: group_share(H, tax, big[big.CODE2023 == c].fips, fk, nocollege) for fk in FK} for c in (1, 2)}
    for c, name in ((1, "Large central counties"), (2, "Large fringe counties ")):
        s = nat[c]
        print(f"  {name} " + "  ".join(f"{LABEL[k]} {s[k]:5.1f}" for k in FK) + f"   change {s['2024'] - s['2009']:+5.1f} pts {pct(s['2009'], s['2024']):+4.0f}%")

    print("\n  Per metro: share within reach in central and fringe counties, 2005-09 -> 2020-24")
    print(f"  {'metro':44s} {'central':>17s} {'chg':>5s}   {'fringe':>17s} {'chg':>5s}   fringe fell more?")
    tally = {"fringe": 0, "central": 0}
    for m, g in sorted(big.groupby("CBSATITLE"), key=lambda kv: -kv[1].CBSAPOP.iloc[0]):
        cen, fri = list(g[g.CODE2023 == 1].fips), list(g[g.CODE2023 == 2].fips)
        if not cen or not fri:
            print(f"  {m[:44]:44s} skipped: {len(cen)} central, {len(fri)} fringe counties")
            continue
        c = {fk: group_share(H, tax, cen, fk, nocollege) for fk in FK}
        f = {fk: group_share(H, tax, fri, fk, nocollege) for fk in FK}
        if None in c.values() or None in f.values():
            print(f"  {m[:44]:44s} skipped: no counties left")
            continue
        cc, fc = pct(c["2009"], c["2024"]), pct(f["2009"], f["2024"])
        more = "fringe" if fc < cc else "central"
        tally[more] += 1
        print(f"  {m[:44]:44s} {c['2009']:5.1f} -> {c['2024']:5.1f} {cc:+5.0f}%   {f['2009']:5.1f} -> {f['2024']:5.1f} {fc:+5.0f}%   {'yes' if more == 'fringe' else 'no'}")
        if rows is not None:
            rows.append({"metro": m, "pop2022": int(g.CBSAPOP.iloc[0]), "n_central": len(cen), "n_fringe": len(fri),
                         **{f"central_{k}": round(c[k], 2) for k in FK}, **{f"fringe_{k}": round(f[k], 2) for k in FK},
                         "central_chg_pct": round(cc, 1), "fringe_chg_pct": round(fc, 1), "fringe_fell_more": more == "fringe"})
    n = tally["fringe"] + tally["central"]
    print(f"\n  Fringe fell more than central in {tally['fringe']} of {n} metros ({100 * tally['fringe'] / n:.0f}%)")
    return tally


def main():
    H, tax, big, missing = load()
    print(f"NCHS large-metro counties matched to the tool: {len(big)}; unmatched: {len(missing)} {missing}")
    print(f"Large metros: {big.CBSATITLE.nunique()}; central counties {int((big.CODE2023 == 1).sum())}, fringe {int((big.CODE2023 == 2).sum())}")
    s = {fk: county_share(H, tax, "13135", fk)[0] * 100 for fk in FK}
    print("Check, Gwinnett share: " + "  ".join(f"{LABEL[k]} {s[k]:.1f}" for k in FK))

    rows = []
    run(H, tax, big, False, rows)
    run(H, tax, big, True)

    print("\n=== Check: Birmingham with Jefferson County coded central")
    alt = big.copy()
    alt.loc[alt.fips == "01073", "CODE2023"] = 1
    b = alt[alt.CBSATITLE == "Birmingham, AL"]
    c = {fk: group_share(H, tax, b[b.CODE2023 == 1].fips, fk) for fk in FK}
    f = {fk: group_share(H, tax, b[b.CODE2023 == 2].fips, fk) for fk in FK}
    print(f"  Jefferson {c['2009']:.1f} -> {c['2024']:.1f} ({pct(c['2009'], c['2024']):+.0f}%); rest {f['2009']:.1f} -> {f['2024']:.1f} ({pct(f['2009'], f['2024']):+.0f}%)")

    print(f"\n=== Atlanta metro, county by county (NCHS code: 1 central, 2 fringe)")
    a = big[big.CBSATITLE == ATLANTA].set_index("fips")
    order = CORE11 + sorted(set(a.index) - set(CORE11), key=lambda u: -sum(H["units"][u]["f"]["2024"]["r"]))
    for u in order:
        s = {fk: 100 * county_share(H, tax, u, fk)[0] for fk in FK}
        n = sum(H["units"][u]["f"]["2024"]["r"])
        print(f"  {H['units'][u]['name']:24s} code {int(a.loc[u, 'CODE2023'])}  " + " ".join(f"{s[k]:5.1f}" for k in FK)
              + f"  {pct(s['2009'], s['2024']):+5.0f}%  cash-rent units 2020-24 {n:>7,}")
    cen, fri = list(a[a.CODE2023 == 1].index), list(a[a.CODE2023 == 2].index)
    for name, g in (("central (Fulton)", cen), ("fringe, all 28", fri), ("Gwinnett+Clayton+DeKalb", ["13135", "13063", "13089"]),
                    ("fringe without those three", [u for u in fri if u not in ("13135", "13063", "13089")])):
        s = {fk: group_share(H, tax, g, fk) for fk in FK}
        print(f"  group: {name:28s} " + " ".join(f"{s[k]:5.1f}" for k in FK) + f"  {pct(s['2009'], s['2024']):+5.0f}%")

    OUT.mkdir(parents=True, exist_ok=True)
    with open(OUT / "test1_metros.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    buf = io.StringIO()
    with redirect_stdout(buf):
        main()
    (ROOT / "research").mkdir(exist_ok=True)
    (ROOT / "research" / "test1-counties-output.txt").write_text(buf.getvalue())
    print(buf.getvalue())
