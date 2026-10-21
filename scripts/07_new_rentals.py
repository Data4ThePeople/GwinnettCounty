"""Were Gwinnett's newer rentals mostly high-priced apartments? And did the older rentals get pricier too? ACS PUMS.

Cash-rent renter households in 2005-09 and 2020-24, split by when the building was built and by building type.
"Within reach" uses the tool's ceiling for that county and period (30% of the renter median after tax, a month),
compared with each household's gross rent (GRNTP x ADJHSG, the file's final-year dollars). The tool reads shares
from rent buckets, so its levels differ a little from these exact-rent shares; the whole-county line is printed as a
check. Standard errors come from the 80 replicate weights, as in 06_pums_turnover.py. Forsyth is left out (its 2000
PUMA also covers Dawson and Pickens; DATASETS.md section 7).

Year built (DATASETS.md section 7): the 2005-09 file's YBL codes are 1 = 2005 or later, 2 = 2000-04, 3 = 1990s,
down to 9 = 1939 or earlier. The 2020-24 file's YRBLT gives the first year of a decade (2000 = 2000-09,
2010 = 2010-19) and single years from 2020.

Output: research/new-rentals-output.txt"""
import importlib.util
import io
import json
import math
import sys
from contextlib import redirect_stdout
from importlib import import_module
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
AH = Path.home() / "PycharmProjects" / "AffordableHousing"
sys.path.insert(0, str(AH / "scripts"))
from common import PROC  # noqa: E402

spec = importlib.util.spec_from_file_location("tieout", AH / "scripts" / "10_tieout.py")
T0 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(T0)

PUMAS = import_module("04_fetch_county_tables").PUMAS
RAW = ROOT / "data" / "raw" / "pums"
NAMES = {"135": "Gwinnett", "121": "Fulton", "089": "DeKalb", "067": "Cobb", "063": "Clayton", "151": "Henry", "057": "Cherokee"}
LABEL = {"2009": "2005-09", "2024": "2020-24"}
TYPES = {"single-family": {2, 3}, "2-4 units": {4, 5}, "5+ unit apartments": {6, 7, 8, 9}, "mobile home/other": {1, 10}}


def era(v, row, h):
    """'newer' = built in the ten or so years before the period; 'older' = built before 2000."""
    if v == "2009":
        y = int(row[h["YBL"]])
        return "newer (2000+)" if y <= 2 else "older (pre-2000)"
    y = int(row[h["YRBLT"]])
    return "newer (2010+)" if y >= 2010 else ("2000s" if y == 2000 else "older (pre-2000)")


def records(v, c):
    out = []
    for p in PUMAS[v][c]:
        parts = [json.loads((RAW / f"{v}_{p}_{k}.json").read_text()) for k in range(3)]
        heads = [{n: i for i, n in enumerate(j[0])} for j in parts]
        reps = [{row[h["SERIALNO"]]: row for row in j[1:]} for j, h in zip(parts[1:], heads[1:])]
        h = heads[0]
        for row in parts[0][1:]:
            rent = int(row[h["GRNTP"]] or 0)
            if rent <= 0:                                   # no cash rent
                continue
            adj = row[h["ADJHSG"]]
            adj = float(adj) if "." in adj else int(adj) / 1e6
            s = row[h["SERIALNO"]]
            w = [int(reps[0][s][heads[1][f"WGTP{i}"]]) for i in range(1, 41)] + [int(reps[1][s][heads[2][f"WGTP{i}"]]) for i in range(41, 81)]
            bld = int(row[h["BLD"]])
            out.append({"rent": rent * adj, "era": era(v, row, h), "type": next(t for t, k in TYPES.items() if bld in k),
                        "w": int(row[h["WGTP"]]), "rw": w})
    return out


def wt(x, r):
    return x["w"] if r is None else x["rw"][r]


def wmedian(rows, r=None):
    pairs = sorted((x["rent"], wt(x, r)) for x in rows)
    half, run = sum(w for _, w in pairs) / 2, 0
    for rent, w in pairs:
        run += w
        if run >= half:
            return rent


def within(rows, ceil, r=None):
    return 100 * sum(wt(x, r) for x in rows if x["rent"] <= ceil) / sum(wt(x, r) for x in rows)


def se(f, rows, *a):
    m = f(rows, *a)
    return m, math.sqrt(4 / 80 * sum((f(rows, *a, r) - m) ** 2 for r in range(80)))


def count(rows, r=None):
    return sum(wt(x, r) for x in rows)


def main():
    H = json.loads((PROC / "harmonized.json").read_text())
    tax = json.loads((PROC / "tax_grid.json").read_text())
    print("Cash-rent renter households by year built and building type. Rents in each file's final-year dollars.")
    print("households (+/- 1 SE) | share of the period's rentals | median gross rent | share within reach of the tool's ceiling")
    for c, name in NAMES.items():
        for v in ("2009", "2024"):
            x = H["units"]["13" + c]["f"][v]
            inc = T0.income(x, v, 5)
            ceil = 0.30 * (inc - T0.tax(tax, v, 1, "13", inc)) / 12
            rows = records(v, c)
            tot = count(rows)
            (wa, wse) = se(within, rows, ceil)
            print(f"\n{name} {LABEL[v]}: ceiling ${ceil:,.0f}/month; all cash-rent rentals {tot:,}, median ${wmedian(rows):,.0f}, within reach {wa:.1f}% (+/-{wse:.1f}) = {tot * wa / 100:,.0f} households")
            eras = sorted({x["era"] for x in rows}, key=lambda e: ("newer" not in e, e != "2000s"))
            for e in eras:
                for t in [None] + list(TYPES):
                    sub = [x for x in rows if x["era"] == e and (t is None or x["type"] == t)]
                    if not sub:
                        continue
                    n, nse = se(count, sub)
                    m, mse = se(wmedian, sub)
                    s, sse = se(within, sub, ceil)
                    lab = f"{e}, {t}" if t else f"{e}, all types"
                    print(f"   {lab:40s} {n:>7,.0f} (+/-{nse:>5,.0f}) {100 * n / tot:5.1f}%  median ${m:>5,.0f} (+/-{mse:>4,.0f})  within reach {s:5.1f}% (+/-{sse:4.1f}) = {n * s / 100:>6,.0f} households")


if __name__ == "__main__":
    buf = io.StringIO()
    with redirect_stdout(buf):
        main()
    (ROOT / "research" / "new-rentals-output.txt").write_text(buf.getvalue())
    print(buf.getvalue())
