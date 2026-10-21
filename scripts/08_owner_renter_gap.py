"""How wide is the income gap between Gwinnett's homeowners and renters, and is it unusual?

ACS 5-year B25119 (median household income by tenure) for every county and the nation, 2005-09 and 2020-24.
Gap = renter median as a percent of the owner median. Dollar changes use CPI-U to 2024 dollars, as in
05_why_rents.py. Margins: the ratio's margin uses the Census approximation for a ratio (not a proportion) of two estimates
(ACS General Handbook, chapter 8), with MOEs at 90%.

Comparison sets: counties with at least 1,000 renter households (B25003) in 2020-24, and large counties with at
least 100,000 households.

Output: research/owner-renter-gap-output.txt"""
import io
import json
import math
import sys
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AH = Path.home() / "PycharmProjects" / "AffordableHousing"
sys.path.insert(0, str(AH / "scripts"))
from common import PROC, census  # noqa: E402

RAW = ROOT / "data" / "raw" / "acs"
FK = ["2009", "2024"]
LABEL = {"2009": "2005-09", "2024": "2020-24"}
GET = "NAME,B25119_002E,B25119_002M,B25119_003E,B25119_003M,B25003_001E,B25003_003E"
PEERS = {"13135": "Gwinnett", "13121": "Fulton", "13089": "DeKalb", "13067": "Cobb", "13063": "Clayton",
         "13151": "Henry", "13057": "Cherokee", "13117": "Forsyth"}


def pull(v, geo):
    rows = census(f"{v}/acs/acs5", {"get": GET, "for": geo}, RAW / f"tenure_income_{v}_{geo.split(':')[0]}.json")
    h = {c: i for i, c in enumerate(rows[0])}
    out = {}
    for r in rows[1:]:
        key = r[h["state"]] + r[h["county"]] if "county" in h else "us"
        try:
            o, om, ren, rm = (float(r[h[k]]) for k in ("B25119_002E", "B25119_002M", "B25119_003E", "B25119_003M"))
        except (TypeError, ValueError):
            continue
        if o <= 0 or ren <= 0:
            continue
        out[key] = {"name": r[h["NAME"]], "own": o, "own_m": om, "rent": ren, "rent_m": rm,
                    "hh": int(r[h["B25003_001E"]]), "renters": int(r[h["B25003_003E"]])}
    return out


def ratio(x):
    r = x["rent"] / x["own"]
    return 100 * r, 100 * math.sqrt(x["rent_m"] ** 2 + r ** 2 * x["own_m"] ** 2) / x["own"]


def main():
    cpi = json.loads((PROC / "cpi.json").read_text())
    D = {v: pull(v, "county:*") for v in FK}
    US = {v: pull(v, "us:1")["us"] for v in FK}
    k = {v: cpi["2024"] / cpi[v] for v in FK}

    print("Median household income by tenure (B25119), 2024 dollars. Gap = renter median as % of owner median (90% MOE).")
    for label, x in [("United States", US)] + [(n, {v: D[v][f] for v in FK}) for f, n in PEERS.items()]:
        line = f"   {label:14s}"
        for v in FK:
            r, m = ratio(x[v])
            line += f" | {LABEL[v]} owners ${x[v]['own'] * k[v]:>8,.0f} renters ${x[v]['rent'] * k[v]:>7,.0f} gap {r:4.1f}% (+/-{m:.1f})"
        do = 100 * (x["2024"]["own"] * k["2024"] / (x["2009"]["own"] * k["2009"]) - 1)
        dr = 100 * (x["2024"]["rent"] * k["2024"] / (x["2009"]["rent"] * k["2009"]) - 1)
        print(line + f" | real change owners {do:+.0f}%, renters {dr:+.0f}%")

    for title, keep in (("at least 1,000 renter households", lambda x: x["renters"] >= 1000),
                        ("at least 100,000 households", lambda x: x["hh"] >= 100000)):
        print(f"\nCounties with {title} in 2020-24: rank of Gwinnett (1 = renters furthest below owners)")
        for v in FK:
            pool = {f: x for f, x in D[v].items() if f in D["2024"] and keep(D["2024"][f])}
            ranked = sorted(pool, key=lambda f: pool[f]["rent"] / pool[f]["own"])
            g = ranked.index("13135") + 1
            med = sorted(100 * pool[f]["rent"] / pool[f]["own"] for f in pool)[len(pool) // 2]
            print(f"   {LABEL[v]}: Gwinnett rank {g} of {len(pool)}, gap {100 * pool['13135']['rent'] / pool['13135']['own']:.1f}%;"
                  f" middle county {med:.1f}%")
            if v == "2024" and title.startswith("at least 100"):
                print("   Widest 15 gaps, 2020-24:")
                for f in ranked[:15]:
                    r, m = ratio(pool[f])
                    print(f"      {pool[f]['name']:42s} {r:4.1f}% (+/-{m:.1f})  owners ${pool[f]['own']:,.0f} renters ${pool[f]['rent']:,.0f}")
                g24 = 100 * pool["13135"]["rent"] / pool["13135"]["own"]
                g09 = 100 * D["2009"]["13135"]["rent"] / D["2009"]["13135"]["own"]
                both = [f for f in pool if f in D["2009"]]
                fell = sorted(both, key=lambda f: 100 * pool[f]["rent"] / pool[f]["own"] - 100 * D["2009"][f]["rent"] / D["2009"][f]["own"])
                print(f"   Change in gap, Gwinnett {g24 - g09:+.1f} pts; rank {fell.index('13135') + 1} of {len(both)} (1 = gap widened most)")


if __name__ == "__main__":
    buf = io.StringIO()
    with redirect_stdout(buf):
        main()
    (ROOT / "research" / "owner-renter-gap-output.txt").write_text(buf.getvalue())
    print(buf.getvalue())
