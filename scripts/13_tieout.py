"""Claude's tie-out of every number in research/thread.md and on the charts in the proposed set.

Each check recomputes the figure through the analysis functions and compares it with the text as written, within
rounding. Cross-checks take a second path where one exists: the tool's own published tie-out
(AffordableHousing/data/processed/tieout.csv) for the national shares; fresh Census API pulls of B25063 and B25064
for Gwinnett's rental count and median rent; the national B25119 pull (tenure_income_*) for renter income instead of
the tool's harmonized file; PUMS counts against the published tables. Words are checked in a list at the end.

Output: research/tieout-output.txt"""
import csv
import io
import json
import sys
from contextlib import redirect_stdout
from importlib import import_module
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
AH = Path.home() / "PycharmProjects" / "AffordableHousing"
sys.path.insert(0, str(AH / "scripts"))
from common import PROC, census  # noqa: E402

C1 = import_module("01_candidate_selection")
W5 = import_module("05_why_rents")
N7 = import_module("07_new_rentals")
G8 = import_module("08_owner_renter_gap")
V10 = import_module("10_values_vs_rents")
P12 = import_module("12_renter_income")
RAW = ROOT / "data" / "raw" / "acs"
G = "13135"
FK = ["2009", "2014", "2019", "2024"]
results = []


def check(cid, text, claimed, value, tol):
    ok = abs(claimed - value) <= tol
    results.append(ok)
    print(f"   {'PASS' if ok else 'FAIL'}  {cid:4s} {text:62s} claimed {claimed:>10,.2f}  computed {value:>10,.2f}")


def pct(a, b):
    return 100 * (b / a - 1)


def main():
    cpi = json.loads((PROC / "cpi.json").read_text())
    k = {v: cpi["2024"] / cpi[v] for v in cpi}
    H, S, weak, ranked, _ = C1.build()
    nc = [u for _, u in ranked if H["units"][u]["college"] < C1.COLLEGE_SHARE]
    s = S[G]

    print("Beat 1")
    check("A1", "Gwinnett share within reach 2020-24 (%)", 10.5, s["2024"], 0.05)
    check("A2", "rank outside college towns", 1, nc.index(G) + 1, 0)
    check("A2b", "counties outside college towns", 1922, len(nc), 0)
    check("A3", "rank with college towns", 3, [u for _, u in ranked].index(G) + 1, 0)
    check("A3b", "counties with college towns", 1987, len(ranked), 0)
    check("A4", "Clayton share 2020-24 (%)", 11.0, S["13063"]["2024"], 0.05)
    atl = sum(u in ("13135", "13063", "13089") for u in nc[:4])
    check("A5", "Atlanta-area counties among the lowest four", 3, atl, 0)

    print("Beat 2")
    check("B1", "share 2005-09 (%)", 25.5, s["2009"], 0.05)
    check("B2", "decline in share (%)", -59, pct(s["2009"], s["2024"]), 0.5)
    check("B3", "share 2015-19 (%)", 21.5, s["2019"], 0.05)
    f = H["units"][G]["f"]
    n = {v: sum(f[v]["r"]) for v in ("2009", "2024")}
    check("B4", "rentals growth (%)", 63, pct(n["2009"], n["2024"]), 0.5)
    w = {v: n[v] * S[G][v] / 100 for v in n}
    check("B5", "within-reach count change (%)", -33, pct(w["2009"], w["2024"]), 0.5)
    raw = {}
    for v in ("2009", "2024"):
        rows = census(f"{v}/acs/acs5", {"get": "B25063_002E,B25064_001E", "for": "county:135", "in": "state:13"}, RAW / f"tieout_B25063_{v}_gwinnett.json")
        raw[v] = (int(rows[1][0]), int(rows[1][1]))
    check("B4x", "  cross-check: cash-rent units 2020-24, fresh B25063_002", raw["2024"][0], n["2024"], 0)
    check("B4y", "  cross-check: cash-rent units 2005-09, fresh B25063_002", raw["2009"][0], n["2009"], 0)
    us = {r["period"]: float(r["share_recomputed"]) for r in csv.DictReader((PROC / "tieout.csv").open()) if r["setting"] == "default"}
    check("B6", "US share 2005-09, text says about 32% (%)", 32, us["2005-2009"], 0.5)
    check("B7", "US share 2020-24, text says about 31% (%)", 31, us["2020-2024"], 0.5)
    print(f"   NOTE  US share 2010-14 is {us['2010-2014']:.1f}% and 2015-19 {us['2015-2019']:.1f}%: the text's 'stayed near 31% to 32%'"
          " does not hold for 2010-14.")

    print("Beat 3")
    rent = pct(f["2009"]["mr"] * k["2009"], f["2024"]["mr"] * k["2024"])
    check("C1", "real rent change (%)", 32, rent, 0.5)
    check("C1x", "  cross-check: fresh B25064, real change (%)", pct(raw["2009"][1] * k["2009"], raw["2024"][1] * k["2024"]), rent, 0.05)
    D = {v: G8.pull(v, "county:*") for v in ("2009", "2024")}
    inc = pct(D["2009"][G]["rent"] * k["2009"], D["2024"][G]["rent"] * k["2024"])
    check("C2", "real renter income change (%)", 8, inc, 0.5)
    import importlib.util
    spec = importlib.util.spec_from_file_location("tieout", AH / "scripts" / "10_tieout.py")
    T0 = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(T0)
    tool_inc = pct(T0.income(f["2009"], "2009", 5) * k["2009"], T0.income(f["2024"], "2024", 5) * k["2024"])
    check("C2x", "  cross-check: tool's renter median, real change (%)", inc, tool_inc, 0.05)
    big = [o for o in G8.metro_changes() if o[4] >= 10000]
    check("C3", "large metro counties", 15, len(big), 0)
    gap = sorted(big, key=lambda o: o[3] - o[0], reverse=True)
    check("C4", "Gwinnett rank, rent minus income", 1, [o[6] for o in gap].index(G) + 1, 0)
    print("   INFO  next three: " + ", ".join(f"{o[5]} {o[3] - o[0]:+.1f}" for o in gap[1:4]) + f"; Gwinnett {gap[0][3] - gap[0][0]:+.1f}")
    check("C5", "next three are Clayton, DeKalb, Cherokee", 1, float({o[5] for o in gap[1:4]} == {"Clayton", "DeKalb", "Cherokee"}), 0)
    us_ratio = 100 * G8.pull("2024", "us:1")["us"]["rent"] / G8.pull("2024", "us:1")["us"]["own"]
    check("C6", "renter median as % of owner median (%)", 55, 100 * D["2024"][G]["rent"] / D["2024"][G]["own"], 0.5)
    print(f"   INFO  US figure {us_ratio:.1f}% ('about the national figure')")
    F = V10.fhfa()
    check("C7", "FHFA change Gwinnett (%)", 82, F[G], 0.5)
    check("C8", "FHFA change Cobb (%)", 83, F["13067"], 0.5)

    print("Beat 4")
    r24 = N7.records("2024", "135")
    tot = N7.count(r24)
    newapt = [x for x in r24 if x["era"] == "newer (2010+)" and x["type"] == "5+ unit apartments"]
    check("D1", "new apartments share of rentals (%), 'about 10%'", 10, 100 * N7.count(newapt) / tot, 0.5)
    check("D2", "new apartments median rent ($)", 1870, N7.wmedian(newapt), 5)
    check("D3", "county median rent ($), tool", 1810, f["2024"]["mr"], 5)
    check("D3x", "  cross-check: PUMS median rent ($)", 1810, N7.wmedian(r24), 5)
    check("D4", "new apartments above county median (%)", 3, pct(f["2024"]["mr"], N7.wmedian(newapt)), 0.5)
    ceil = {}
    for v in ("2009", "2024"):
        x = f[v]
        i = T0.income(x, v, 5)
        ceil[v] = 0.30 * (i - T0.tax(json.loads((PROC / "tax_grid.json").read_text()), v, 1, "13", i)) / 12
    old = {v: [x for x in N7.records(v, "135") if x["era"] == "older (pre-2000)" and x["type"] == "5+ unit apartments"] for v in ("2009", "2024")}
    print(f"   INFO  older apartments {N7.count(old['2009']):,} and {N7.count(old['2024']):,} ('about the same number')")
    check("D5", "older apartments within reach 2005-09, 'about 9,600'", 9600, N7.count(old["2009"]) * N7.within(old["2009"], ceil["2009"]) / 100, 50)
    check("D6", "older apartments within reach 2020-24, 'about 4,100'", 4100, N7.count(old["2024"]) * N7.within(old["2024"], ceil["2024"]) / 100, 50)
    P = W5.permits()
    hh = W5.load("B11001", "2009"), W5.load("B11001", "2024")
    per = {c: sum(sum(P[(c, y)]["est"]) for y in range(2007, 2022)) / (W5.num(hh[1][c], "B11001", 1) - W5.num(hh[0][c], "B11001", 1)) for c in W5.PEERS}
    check("D7", "permits per added household", 0.65, per["135"], 0.005)
    check("D8", "peers below Gwinnett (only Clayton)", 1, sum(v < per["135"] for v in per.values()), 0)
    sf = {}
    for v in ("2009", "2024"):
        t = W5.load("B25032", v)["135"]
        sf[v] = 100 * (W5.num(t, "B25032", 14) + W5.num(t, "B25032", 15)) / W5.num(t, "B25032", 13)
    check("D9", "houses share of rentals 2005-09 (%)", 31, sf["2009"], 0.5)
    check("D10", "houses share of rentals 2020-24 (%)", 39.5, sf["2024"], 0.05)
    hs = [x for x in r24 if x["type"] == "single-family"]
    print(f"   INFO  median rent of house rentals 2020-24 ${N7.wmedian(hs):,.0f} ('above the county median')")

    print("Beat 5")
    h0, w0 = P12.load("2009", "135", cpi)
    h1, w1 = P12.load("2024", "135", cpi)
    print(f"   INFO  PUMS renter median change {pct(P12.wmed(h0, 'inc', P12.weights(h0)), P12.wmed(h1, 'inc', P12.weights(h1))):+.1f}%"
          " (the text's 8% is the published table, C2)")
    m0, m1, ch, se = P12.ftyr_change("135", cpi)
    check("E1", "full-time year-round pay change (%)", -3, ch, 0.5)
    check("E2", "its 90% margin (points), 'about 5'", 5, 1.645 * se, 0.5)
    for c, name, claim in (("067", "Cobb", 7), ("089", "DeKalb", 10), ("121", "Fulton", 21)):
        check("E3", f"full-time pay change {name} (%)", claim, P12.ftyr_change(c, cpi)[2], 0.5)
    for c, name in (("151", "Henry"), ("057", "Cherokee"), ("063", "Clayton")):
        v = P12.ftyr_change(c, cpi)[2]
        check("E4", f"{name} full-time pay fell (1 = yes)", 1, float(v < 0), 0)
    wk = lambda h: sum(x["n_work"] * x["w"] for x in h) / sum(x["w"] for x in h)  # noqa: E731
    check("E5", "workers per household 2005-09", 1.29, wk(h0), 0.005)
    check("E6", "workers per household 2020-24", 1.36, wk(h1), 0.005)
    c0, c1 = P12.load("2009", "067", cpi)[0], P12.load("2024", "067", cpi)[0]
    check("E7", "Cobb rise vs Gwinnett rise, workers ('about the same')", wk(h1) - wk(h0), wk(c1) - wk(c0), 0.02)
    two = lambda h: 100 * sum(x["w"] for x in h if x["n_work"] >= 2) / sum(x["w"] for x in h)  # noqa: E731
    check("E8", "2+ workers 2005-09 (%)", 34, two(h0), 0.5)
    check("E9", "2+ workers 2020-24 (%)", 37, two(h1), 0.5)
    ft = lambda ws: 100 * sum(x["w"] for x in ws if x["ftyr"]) / sum(x["w"] for x in ws)  # noqa: E731
    check("E10", "full-time year-round share of workers 2005-09 (%)", 66, ft(w0), 0.5)
    check("E11", "full-time year-round share of workers 2020-24 (%)", 76, ft(w1), 0.5)
    check("E12", "same-kind-of-household income change (%)", -3, pct(P12.wmed(h0, "inc", P12.weights(h0)), P12.reweighted(h1, h0)), 0.5)
    q = P12.qcew()
    check("E13", "QCEW pay change Gwinnett (%)", 1, q[G], 0.5)
    check("E14", "QCEW rank of Gwinnett, 8 = smallest", 8, sorted(q, key=q.get, reverse=True).index(G) + 1, 0)

    print("\nWords (checked by hand against the results above and the memos)")
    for line in (
        "SUPPORTED  beat 1 'smallest share ... outside college towns' (A1-A3); 'could swap places' with Clayton: no margin on the share"
        " exists, so this was a judgment, PARTLY SUPPORTED; now reads 'half a point behind' (fixed).",
        "NOT SUPPORTED  beat 2 'The nation stayed near 31% to 32%': 27.6% in 2010-14 (B6 note). Fix: 'The national share was 32% in"
        " 2005-09 and 31% in 2020-24.' (fixed)",
        "SUPPORTED  beat 2 'Most of the drop came after 2015-19': 21.5 to 10.5 is 11 of the 15 points.",
        "SUPPORTED  beat 3 'widest' with the stated margin caveat (C4, C5).",
        "SUPPORTED  beat 3 'about the national figure' (C6 and US figure).",
        "SUPPORTED  beat 4 'not a story of high-priced new apartments' as a description of rent levels (D1-D4); it does not rule out"
        " new apartments raising nearby rents, which the data cannot test.",
        "SUPPORTED  beat 4 'lower than every large neighbor but Clayton' (D8; 'large neighbor' = the seven peers).",
        "PARTLY SUPPORTED  beat 5 'mostly because more of their members worked': the mix effect also includes householder age and"
        " education, not only work. Suggest 'mostly because households changed: more members worked, more worked full time, and more"
        " householders were older or had degrees.' (fixed)",
        "SUPPORTED  beat 5 'its pay moved like Henry's' (-3.3% vs -3.4%).",
        "FIXED  beat 5 and chart 11 'fell 3%': -3.3% is inside its 90% margin of about 5 points, so the text now says pay 'did not"
        " rise' (flagged by the independent tie-out).",
        "FIXED  beat 5 '34% to 38%' for households with 2+ workers: 37.46% rounds to 37 (E9); 'the same rise' as Cobb is now 'about the"
        " same rise' (E7, within the margin of about 0.02).",
    ):
        print("   " + line)

    print(f"\n{sum(results)} of {len(results)} number checks pass.")


if __name__ == "__main__":
    buf = io.StringIO()
    with redirect_stdout(buf):
        main()
    (ROOT / "research" / "tieout-output.txt").write_text(buf.getvalue())
    print(buf.getvalue())
