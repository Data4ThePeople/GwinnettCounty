"""Did Gwinnett just have a stronger housing market? Home price growth against rent growth, by county.

Home prices two ways:
  - ACS 5-year B25077, median value of owner-occupied homes (owners' own estimate), 2005-09 and 2020-24, brought
    to 2024 dollars with CPI-U as for rents.
  - FHFA all-transactions house price index for counties (repeat sales and appraisals on Fannie Mae and Freddie
    Mac mortgages; developmental). Change between the averages of 2005-2009 and 2020-2024, nominal. A common
    inflation factor would not change correlations or ranks, so none is applied.
Rent: median gross rent from the tool's harmonized file, after inflation, as in 08_owner_renter_gap.py.

Rules, written before the run. "Gwinnett's rents rose because its home prices rose more" is consistent with the
data if all three hold:
  (a) across counties with 10,000+ renter households nationwide, home price change and rent change are at least
      moderately correlated (r of 0.5 or more);
  (b) Gwinnett's home price change ranks in the top third (5th or better) of the 15 large Atlanta-metro counties;
  (c) given its home price change, Gwinnett's rent change is not unusually high: its residual from the national
      fit is within one standard deviation of the residuals.

Output: research/values-vs-rents-output.txt"""
import io
import json
import math
import sys
from contextlib import redirect_stdout
from importlib import import_module
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
AH = Path.home() / "PycharmProjects" / "AffordableHousing"
sys.path.insert(0, str(AH / "scripts"))
from common import PROC, census  # noqa: E402

G8 = import_module("08_owner_renter_gap")
RAW = ROOT / "data" / "raw"
FK = ["2009", "2024"]


def pct(a, b):
    return 100 * (b / a - 1)


def values(v):
    rows = census(f"{v}/acs/acs5", {"get": "B25077_001E,B25077_001M", "for": "county:*"}, RAW / "acs" / f"B25077_{v}_county.json")
    h = {c: i for i, c in enumerate(rows[0])}
    out = {}
    for r in rows[1:]:
        try:
            val = float(r[h["B25077_001E"]])
        except (TypeError, ValueError):
            continue
        if val > 0:
            out[r[h["state"]] + r[h["county"]]] = val
    return out


def fhfa():
    d = pd.read_excel(RAW / "fhfa" / "hpi_at_county.xlsx", header=5, dtype={"FIPS code": str})
    d["HPI"] = pd.to_numeric(d["HPI"], errors="coerce")
    out = {}
    for f, g in d.groupby("FIPS code"):
        s = g.set_index("Year")["HPI"]
        a, b = s.reindex(range(2005, 2010)), s.reindex(range(2020, 2025))
        if a.notna().all() and b.notna().all():
            out[f] = pct(a.mean(), b.mean())
    return out


def corr(x, y):
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    sxy = sum((a - mx) * (b - my) for a, b in zip(x, y))
    return sxy / math.sqrt(sum((a - mx) ** 2 for a in x) * sum((b - my) ** 2 for b in y))


def ranks(x):
    order = sorted(range(len(x)), key=lambda i: x[i])
    r = [0] * len(x)
    for k, i in enumerate(order):
        r[i] = k
    return r


def fit(x, y):
    n = len(x)
    mx, my = sum(x) / n, sum(y) / n
    b = sum((a - mx) * (c - my) for a, c in zip(x, y)) / sum((a - mx) ** 2 for a in x)
    return my - b * mx, b


def main():
    cpi = json.loads((PROC / "cpi.json").read_text())
    k = {v: cpi["2024"] / cpi[v] for v in FK}
    H = json.loads((PROC / "harmonized.json").read_text())
    D = {v: G8.pull(v, "county:*") for v in FK}
    V = {v: values(v) for v in FK}
    F = fhfa()

    rows = {}
    for f, x in D["2024"].items():
        if x["renters"] < 10000 or f not in D["2009"] or f not in V["2009"] or f not in V["2024"] or f not in H["units"]:
            continue
        g = H["units"][f]["f"]
        if "na" in g["2009"] or "na" in g["2024"] or not g["2009"]["mr"]:
            continue
        rows[f] = {"name": x["name"], "rent": pct(g["2009"]["mr"] * k["2009"], g["2024"]["mr"] * k["2024"]),
                   "inc": pct(D["2009"][f]["rent"] * k["2009"], x["rent"] * k["2024"]),
                   "val": pct(V["2009"][f] * k["2009"], V["2024"][f] * k["2024"]), "hpi": F.get(f)}

    print("Home price change vs rent change, 2005-09 to 2020-24. ACS values and rents after inflation; FHFA nominal.")
    for key, label in (("val", "ACS median home value"), ("hpi", "FHFA house price index")):
        fs = [f for f in rows if rows[f][key] is not None]
        x, y = [rows[f][key] for f in fs], [rows[f]["rent"] for f in fs]
        a, b = fit(x, y)
        res = [yy - (a + b * xx) for xx, yy in zip(x, y)]
        sd = math.sqrt(sum(r * r for r in res) / (len(res) - 2))
        gi = fs.index("13135")
        above = sum(r > res[gi] for r in res)
        print(f"\n{label}: {len(fs)} counties with 10,000+ renter households")
        print(f"   correlation with rent change r = {corr(x, y):.2f} (rank correlation {corr(ranks(x), ranks(y)):.2f});"
              f" fit: rent change = {a:.1f} + {b:.2f} x price change")
        print(f"   Gwinnett: price {x[gi]:+.1f}%, rent {y[gi]:+.1f}%, predicted rent {a + b * x[gi]:+.1f}%,"
              f" residual {res[gi]:+.1f} pts = {res[gi] / sd:+.2f} SD; {above} of {len(fs)} counties sit further above the fit")
        print(f"   renter income change vs price change r = {corr(x, [rows[f]['inc'] for f in fs]):.2f}")

    print("\n15 Atlanta-metro counties with 10,000+ renter households, sorted by ACS home value change")
    metro = {o[6] for o in G8.metro_changes() if o[4] >= 10000}
    m = sorted((f for f in rows if f in metro), key=lambda f: -rows[f]["val"])
    assert len(m) == 15
    hr = sorted(m, key=lambda f: -rows[f]["hpi"])
    for i, f in enumerate(m, 1):
        r = rows[f]
        print(f"   {i:2d} {r['name'].split(' County')[0]:10s} home value {r['val']:+5.1f}%  FHFA {r['hpi']:+6.1f}% (rank {hr.index(f) + 1:2d})"
              f"  rent {r['rent']:+5.1f}%  renter income {r['inc']:+5.1f}%{'  <--' if f == '13135' else ''}")
    for key, label in (("val", "ACS home value"), ("hpi", "FHFA")):
        x, y = [rows[f][key] for f in m], [rows[f]["rent"] for f in m]
        print(f"   metro {label} vs rent: r = {corr(x, y):.2f}")


if __name__ == "__main__":
    buf = io.StringIO()
    with redirect_stdout(buf):
        main()
    (ROOT / "research" / "values-vs-rents-output.txt").write_text(buf.getvalue())
    print(buf.getvalue())
