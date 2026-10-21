"""Why did Gwinnett's rents rise so far above what its renters earn? Explanations 1 to 4, against peers.

Peers: Fulton, DeKalb, Cobb, Clayton, Henry, Cherokee, Forsyth. Rules set in the plan before the data came in:
  1 mix shift      holding the 2005-09 bedroom mix fixed moves the 2020-24 share within reach by 3+ points
                   (main driver) or under 1 point (driver is rent within each unit size)
  2 single-family  (ACS part) single-family share of renter-occupied units rose faster than in the peers;
                   the published-source part is in research/investor-sources.md
  3 supply         fewer permitted units per added household than the peers, or a larger fall in rental vacancy
  4 renter pool    growth at $75,000+ (2024 dollars) while the under-$35,000 count held steady

Output: research/why-rents-output.txt"""
import importlib.util
import io
import json
import sys
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AH = Path.home() / "PycharmProjects" / "AffordableHousing"
sys.path.insert(0, str(AH / "scripts"))
from common import PROC, RENT_EDGES, RENTER_EDGES  # noqa: E402

spec = importlib.util.spec_from_file_location("tieout", AH / "scripts" / "10_tieout.py")
T0 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(T0)

RAW = ROOT / "data" / "raw"
FK = ["2009", "2014", "2019", "2024"]
LABEL = {"2009": "2005-09", "2014": "2010-14", "2019": "2015-19", "2024": "2020-24"}
PEERS = {"135": "Gwinnett", "121": "Fulton", "089": "DeKalb", "067": "Cobb", "063": "Clayton", "151": "Henry", "057": "Cherokee", "117": "Forsyth"}
# B25068 rent bands per bedroom group: 2009 and 2014 releases vs 2019 and 2024
BAND_EDGES = {"2009": [0, 200, 300, 500, 750, 1000], "2014": [0, 200, 300, 500, 750, 1000],
              "2019": [0, 300, 500, 750, 1000, 1500], "2024": [0, 300, 500, 750, 1000, 1500]}
BEDS = ["studio", "1 bedroom", "2 bedrooms", "3+ bedrooms"]


def load(g, v):
    j = json.loads((RAW / "acs" / f"{g}_{v}_ga_county.json").read_text())
    h = {c: i for i, c in enumerate(j[0])}
    return {row[h["county"]]: {c: row[i] for c, i in h.items() if c.startswith(g) and c.endswith("E")} for row in j[1:]}


def num(t, g, i):
    return int(float(t[f"{g}_{i:03d}E"]))


def tool_ceiling(H, tax, c, fk):
    x = H["units"]["13" + c]["f"][fk]
    inc = T0.income(x, fk, 5)
    return 0.30 * (inc - T0.tax(tax, fk, 1, "13", inc)) / 12


def pct(a, b):
    return 100 * (b / a - 1)


def count_below(ti, edges, x):
    """Renter households with income under x, spreading each bucket evenly. x must sit below the open top bucket ($150,000+)."""
    assert x < edges[-1]
    out = 0.0
    for k, n in enumerate(ti[:-1]):
        lo, hi = edges[k], edges[k + 1]
        if x >= hi:
            out += n
        elif x > lo:
            out += n * (x - lo) / (hi - lo)
    return out


def permits():
    """Permitted units (estimates, with imputation) and reported-only units, by Georgia county and year."""
    out = {}
    for y in range(2000, 2026):
        lines = (RAW / "bps" / f"co{y}a.txt").read_text(encoding="latin-1").splitlines()
        assert lines[1].startswith("Date,State,County"), y
        for ln in lines[3:]:
            f = ln.split(",")
            if len(f) < 30 or f[1] != "13" or f[2] not in PEERS:
                continue
            est = [int(f[i]) for i in (7, 10, 13, 16)]
            rep = [int(f[i]) for i in (19, 22, 25, 28)]
            out[(f[2], y)] = {"est": est, "rep": rep}
    return out


def main():
    H = json.loads((PROC / "harmonized.json").read_text())
    tax = json.loads((PROC / "tax_grid.json").read_text())
    cpi = json.loads((PROC / "cpi.json").read_text())
    T = {g: {v: load(g, v) for v in FK} for g in ["B25068", "B25042", "B25032", "B25036", "B25038", "B25003", "B25004", "B25001", "B11001"]}

    g = H["units"]["13135"]["f"]
    print(f"Check: Gwinnett median gross rent {LABEL['2009']} ${g['2009']['mr']:,.0f}, {LABEL['2024']} ${g['2024']['mr']:,.0f}")

    # ---------- 1. bedroom mix ----------
    print("\n1. Bedroom mix. Share of cash-rent units within reach (tool ceiling), read from B25068's coarse rent bands.")
    print("   'actual' uses each period's own bedroom mix; 'fixed' holds the 2005-09 mix. The rule looks at the gap between them.")
    for c, name in PEERS.items():
        res = {}
        for v in ("2009", "2024"):
            t = T["B25068"][v][c]
            ceil = tool_ceiling(H, tax, c, v)
            grp = []
            for b in range(4):
                base = 2 + 9 * b                      # group total, then with-cash-rent, then six bands, then no cash rent
                bands = [num(t, "B25068", base + 2 + k) for k in range(6)]
                assert sum(bands) == num(t, "B25068", base + 1), (c, v, b)
                grp.append((sum(bands), T0.share(bands, BAND_EDGES[v], ceil) if sum(bands) else 0.0))
            res[v] = grp
        tot = {v: sum(n for n, _ in res[v]) for v in res}
        mix = {v: [n / tot[v] for n, _ in res[v]] for v in res}
        actual = 100 * sum(w * s for w, (_, s) in zip(mix["2024"], res["2024"]))
        fixed = 100 * sum(w * s for w, (_, s) in zip(mix["2009"], res["2024"]))
        a09 = 100 * sum(w * s for w, (_, s) in zip(mix["2009"], res["2009"]))
        print(f"   {name:9s} mix 2005-09 " + " ".join(f"{100 * w:4.1f}" for w in mix["2009"]) + "  2020-24 " + " ".join(f"{100 * w:4.1f}" for w in mix["2024"])
              + f" | within reach 2005-09 {a09:4.1f}, 2020-24 actual {actual:4.1f}, fixed mix {fixed:4.1f}, gap {fixed - actual:+4.1f} pts")
        if c == "135":
            print("             within reach by bedroom group 2005-09 -> 2020-24: " + ", ".join(f"{BEDS[b]} {100 * res['2009'][b][1]:.0f}% -> {100 * res['2024'][b][1]:.0f}%" for b in range(4)))

    # ---------- 2. single-family rentals (ACS part) ----------
    print("\n2. Single-family homes as a share of renter-occupied units (B25032, 1-unit detached + attached), and owner households (B25003)")
    for c, name in PEERS.items():
        s, n, own = {}, {}, {}
        for v in FK:
            t = T["B25032"][v][c]
            sf = num(t, "B25032", 14) + num(t, "B25032", 15)
            n[v], s[v] = sf, 100 * sf / num(t, "B25032", 13)
            own[v] = num(T["B25003"][v][c], "B25003", 2)
        r09, r24 = num(T["B25032"]["2009"][c], "B25032", 13), num(T["B25032"]["2024"][c], "B25032", 13)
        print(f"   {name:9s} SF share " + " ".join(f"{s[v]:4.1f}" for v in FK) + f"  SF renter units {n['2009']:>7,} -> {n['2024']:>7,} ({n['2024'] - n['2009']:+,})"
              f"  of all renter growth {100 * (n['2024'] - n['2009']) / (r24 - r09):4.0f}%  owners {own['2009']:,} -> {own['2024']:,} ({pct(own['2009'], own['2024']):+.0f}%)")

    # ---------- 3. supply ----------
    print("\n3. Supply. Permitted units 2007-2021 (the years between the two periods' midpoints) per added household, and rental vacancy (B25004)")
    P = permits()
    for c, name in PEERS.items():
        units = sum(sum(P[(c, y)]["est"]) for y in range(2007, 2022))
        rep = sum(sum(P[(c, y)]["rep"]) for y in range(2007, 2022))
        mf = sum(P[(c, y)]["est"][3] for y in range(2007, 2022))
        hh = {v: num(T["B11001"][v][c], "B11001", 1) for v in FK}
        vac = {}
        for v in FK:
            b4 = T["B25004"][v][c]
            fr, rn = num(b4, "B25004", 2), num(b4, "B25004", 3)
            vac[v] = 100 * fr / (fr + rn + num(T["B25003"][v][c], "B25003", 3))
        add = hh["2024"] - hh["2009"]
        print(f"   {name:9s} households {hh['2009']:>7,} -> {hh['2024']:>7,} ({add:+,}); permits {units:>6,} ({100 * mf / units:3.0f}% in 5+ unit buildings,"
              f" {100 * (units - rep) / units:3.1f}% imputed) = {units / add:4.2f} per added household; rental vacancy " + " ".join(f"{vac[v]:4.1f}%" for v in FK))
    peak = {c: [sum(P[(c, y)]["est"]) for y in range(2000, 2026)] for c in PEERS}
    print("   Gwinnett permits by year 2000-2025: " + ", ".join(f"{y}:{n:,}" for y, n in zip(range(2000, 2026), peak["135"])))

    # ---------- 4. renter pool ----------
    print("\n4. Renter households by income in constant 2024 dollars (B25118 buckets, CPI-U), and renters who moved in during the 5-year window (B25038)")
    for c, name in PEERS.items():
        x = H["units"]["13" + c]["f"]
        out = {}
        for v in ("2009", "2024"):
            k = cpi[v] / cpi["2024"]
            ti, tot = x[v]["ti"], sum(x[v]["ti"])
            out[v] = (count_below(ti, RENTER_EDGES, 35000 * k), tot - count_below(ti, RENTER_EDGES, 75000 * k), tot)
        lo, hi, tot = (out["2024"][i] - out["2009"][i] for i in range(3))
        m09 = num(T["B25038"]["2009"][c], "B25038", 10) / num(T["B25038"]["2009"][c], "B25038", 9)
        m24 = (num(T["B25038"]["2024"][c], "B25038", 10) + num(T["B25038"]["2024"][c], "B25038", 11)) / num(T["B25038"]["2024"][c], "B25038", 9)
        print(f"   {name:9s} under $35k {out['2009'][0]:>8,.0f} -> {out['2024'][0]:>8,.0f} ({lo:+8,.0f}) | $75k+ {out['2009'][1]:>8,.0f} -> {out['2024'][1]:>8,.0f} ({hi:+8,.0f})"
              f" | all {tot:+8,.0f}; $75k+ share of growth {100 * hi / tot:4.0f}% | moved in within window {100 * m09:.0f}% -> {100 * m24:.0f}%")

    # newer rentals (2020-24 release only; year-built bands do not line up across releases)
    print("\n   Renter-occupied units built 2010 or later, 2020-24 (B25036)")
    for c, name in PEERS.items():
        t = T["B25036"]["2024"][c]
        print(f"   {name:9s} {100 * (num(t, 'B25036', 14) + num(t, 'B25036', 15)) / num(t, 'B25036', 13):4.1f}%")


if __name__ == "__main__":
    buf = io.StringIO()
    with redirect_stdout(buf):
        main()
    (ROOT / "research").mkdir(exist_ok=True)
    (ROOT / "research" / "why-rents-output.txt").write_text(buf.getvalue())
    print(buf.getvalue())
