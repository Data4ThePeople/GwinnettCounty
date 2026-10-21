"""Why did Gwinnett's renter income lag its neighbors? ACS PUMS person records (DATASETS.md section 11) and QCEW
pay (section 12), 2005-09 and 2020-24, Gwinnett against Fulton, DeKalb, Cobb, Clayton, Henry and Cherokee.

Household income is HINCP x ADJINC (file's final-year dollars), then CPI-U to 2024 dollars. Earnings are PERNP x
ADJINC. A worker is a person with ESR 1, 2, 4 or 5 (employed, civilian or armed forces). Full-time year-round:
35+ usual hours (WKHP) and 50+ weeks (WKW 1 in 2005-09, WKWN 50+ in 2020-24). Standard errors from the 80
replicate weights (successive difference formula), as in 06_pums_turnover.py.

Gwinnett's renter median rose 8.3% after inflation (B25119) against 15.8% for the Atlanta metro: a gap of about
7.5 points. Rules, written before the run:
  R1 composition  Reweight Gwinnett's 2020-24 renter households to the 2005-09 mix of cells (workers in household
                  0/1/2+ x householder age under 35/35-64/65+ x householder education, 4 levels). If that raises
                  Gwinnett's growth by 3.75 points or more (half the gap), the mix of households is a main factor;
                  1 to 3.75 a partial factor; under 1 not a factor.
  R2 workers      Workers per renter household fell in Gwinnett by at least 0.1 more than in Cobb, or fell while
                  rising in most peers.
  R3 pay          The real change in median earnings of full-time year-round renter workers living in Gwinnett is
                  at least 5 points below Cobb's and below the peer median.
  R4 local jobs   QCEW average annual pay of jobs located in Gwinnett rose at least 5 points less than the peer
                  median (context: jobs in a county are not all held by its residents).

Output: research/renter-income-output.txt"""
import io
import json
import math
import sys
from collections import defaultdict
from contextlib import redirect_stdout
from importlib import import_module
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
AH = Path.home() / "PycharmProjects" / "AffordableHousing"
sys.path.insert(0, str(AH / "scripts"))
from common import PROC  # noqa: E402

PUMAS = import_module("04_fetch_county_tables").PUMAS
RAW = ROOT / "data" / "raw"
NAMES = {"135": "Gwinnett", "121": "Fulton", "089": "DeKalb", "067": "Cobb", "063": "Clayton", "151": "Henry", "057": "Cherokee"}
LABEL = {"2009": "2005-09", "2024": "2020-24"}
R = range(80)
AGE = ("under 35", "35-64", "65+")
EDU = ("less than high school", "high school", "some college", "bachelor's+")
SECTORS = [(170, 490, "farming and mining"), (570, 690, "utilities"), (770, 770, "construction"), (1070, 3990, "manufacturing"),
           (4070, 4590, "wholesale"), (4670, 5790, "retail"), (6070, 6390, "transportation and warehousing"),
           (6470, 6780, "information"), (6870, 7190, "finance and real estate"), (7270, 7570, "professional and technical"),
           (7580, 7790, "administrative and support"), (7860, 8470, "education and health care"),
           (8560, 8690, "leisure and hospitality"), (8770, 9290, "other services"), (9370, 9870, "government and military")]


def adj(s):
    return float(s) if "." in s else int(s) / 1e6


def edu(v, s):
    s = int(s or 0)
    if v == "2009":
        return 0 if s < 9 else 1 if s == 9 else 2 if s < 13 else 3
    return 0 if s < 16 else 1 if s < 18 else 2 if s < 21 else 3


def sector(code):
    c = int(code) if code and code.isdigit() else 0
    return next((name for lo, hi, name in SECTORS if lo <= c <= hi), None)


def load(v, c, cpi):
    k = cpi["2024"] / cpi[v]
    people = defaultdict(dict)
    for p in PUMAS[v][c]:
        parts = [json.loads((RAW / "pums_people" / f"{v}_{p}_{i}.json").read_text()) for i in range(5)]
        for j in parts:
            h = j[0]
            for row in j[1:]:
                people[(row[h.index("SERIALNO")], row[h.index("SPORDER")])].update(zip(h, row))
    hh = {}
    workers = []
    for (s, o), x in people.items():
        rw = [int(x[f"PWGTP{i}"]) for i in range(1, 81)]
        a = adj(x["ADJINC"]) * k
        emp = x["ESR"] in ("1", "2", "4", "5")
        if emp and int(x["PERNP"] or 0) > 0:
            weeks = (x["WKW"] == "1") if v == "2009" else int(x["WKWN"] or 0) >= 50
            workers.append({"earn": int(x["PERNP"]) * a, "ftyr": int(x["WKHP"] or 0) >= 35 and weeks, "sector": sector(x["INDP"]),
                            "w": int(x["PWGTP"]), "rw": rw})
        d = hh.setdefault(s, {"n_work": 0})
        d["n_work"] += emp
        if o == "1":
            d.update({"inc": int(x["HINCP"] or 0) * a, "age": 0 if int(x["AGEP"]) < 35 else 1 if int(x["AGEP"]) < 65 else 2,
                      "edu": edu(v, x["SCHL"]), "fb": x["NATIVITY"] == "2", "np": int(x["NP"]),
                      "w": int(x["WGTP"]), "rw": [int(x[f"WGTP{i}"]) for i in range(1, 81)]})
    hh = [d for d in hh.values() if "inc" in d]
    for d in hh:
        d["cell"] = (min(d["n_work"], 2), d["age"], d["edu"])
    return hh, workers


def wmed(rows, key, wts):
    pairs = sorted((x[key], w) for x, w in zip(rows, wts))
    half, run = sum(w for _, w in pairs) / 2, 0
    for val, w in pairs:
        run += w
        if run >= half:
            return val


def weights(rows, r=None):
    return [x["w"] if r is None else x["rw"][r] for x in rows]


def se_of(f):
    m = f(None)
    return m, math.sqrt(4 / 80 * sum((f(r) - m) ** 2 for r in R))


def shares(rows, key, levels, r=None):
    w = weights(rows, r)
    tot = sum(w)
    return [100 * sum(ww for x, ww in zip(rows, w) if x[key] == lv) / tot for lv in levels]


def reweighted(rows, base, r=None):
    """2020-24 households reweighted so each cell's share matches the 2005-09 share; empty cells are dropped."""
    w = weights(rows, r)
    bw = weights(base, r)
    btot, tot = sum(bw), sum(w)
    bs, cs = defaultdict(float), defaultdict(float)
    for x, ww in zip(base, bw):
        bs[x["cell"]] += ww / btot
    for x, ww in zip(rows, w):
        cs[x["cell"]] += ww / tot
    nw = [ww * bs[x["cell"]] / cs[x["cell"]] if cs[x["cell"]] else 0 for x, ww in zip(rows, w)]
    return wmed(rows, "inc", nw)


def pct(a, b):
    return 100 * (b / a - 1)


def qcew():
    j = json.loads((RAW / "qcew" / "qcew_pay_cpi_2005_2024.json").read_text())
    s = {x["seriesID"]: {d["year"]: float(d["value"]) for d in x["data"] if d["period"] in ("A01", "M13")} for x in j["Results"]["series"]}
    cpi = s.pop("CUUR0000SA0")
    out = {}
    for sid, d in s.items():
        real = {y: d[str(y)] * cpi["2024"] / cpi[str(y)] for y in range(2005, 2025)}
        out[sid[3:8]] = pct(sum(real[y] for y in range(2005, 2010)) / 5, sum(real[y] for y in range(2020, 2025)) / 5)
    return out


def ftyr_change(c, cpi):
    """Median earnings of full-time year-round renter workers, 2005-09 and 2020-24 (2024 dollars), and the change
    in percent with its standard error. Also used by 09_charts.py."""
    a = [x for x in load("2009", c, cpi)[1] if x["ftyr"]]
    b = [x for x in load("2024", c, cpi)[1] if x["ftyr"]]
    ch, s = se_of(lambda r: pct(wmed(a, "earn", weights(a, r)), wmed(b, "earn", weights(b, r))))
    return wmed(a, "earn", weights(a)), wmed(b, "earn", weights(b)), ch, s


def main():
    cpi = json.loads((PROC / "cpi.json").read_text())
    D = {c: {v: load(v, c, cpi) for v in LABEL} for c in NAMES}

    print("Renter households, 2024 dollars. Median income change after inflation (+/- 1 SE).")
    print("R1 'reweighted' holds the 2005-09 mix of households by workers x householder age x householder education.")
    res = {}
    for c, name in NAMES.items():
        (h0, w0), (h1, w1) = D[c]["2009"], D[c]["2024"]
        m0, s0 = se_of(lambda r: wmed(h0, "inc", weights(h0, r)))
        m1, s1 = se_of(lambda r: wmed(h1, "inc", weights(h1, r)))
        ch, chs = se_of(lambda r: pct(wmed(h0, "inc", weights(h0, r)), wmed(h1, "inc", weights(h1, r))))
        rwch, rws = se_of(lambda r: pct(wmed(h0, "inc", weights(h0, r)), reweighted(h1, h0, r)))
        res[c] = {"ch": ch, "rw": rwch}
        print(f"   {name:9s} median ${m0:>7,.0f} (+/-{s0:,.0f}) -> ${m1:>7,.0f} (+/-{s1:,.0f}): {ch:+5.1f}% (+/-{chs:.1f});"
              f" reweighted {rwch:+5.1f}% (+/-{rws:.1f}); mix effect {rwch - ch:+5.1f} pts")

    print("\nR2 workers per renter household (mean) and share with 0 / 1 / 2+ workers")
    for c, name in NAMES.items():
        line = f"   {name:9s}"
        for v in LABEL:
            h = D[c][v][0]
            mean, se = se_of(lambda r: sum(x["n_work"] * w for x, w in zip(h, weights(h, r))) / sum(weights(h, r)))
            for x in h:
                x["wk"] = min(x["n_work"], 2)
            s = shares(h, "wk", (0, 1, 2))
            line += f" | {LABEL[v]} {mean:.2f} (+/-{se:.2f})  " + " / ".join(f"{q:4.1f}%" for q in s)
        print(line)

    print("\nHouseholder age, education, birthplace and household size (share of renter households)")
    for c, name in NAMES.items():
        for v in LABEL:
            h = D[c][v][0]
            a, e = shares(h, "age", (0, 1, 2)), shares(h, "edu", (0, 1, 2, 3))
            fb = shares(h, "fb", (True,))[0]
            npm = sum(x["np"] * x["w"] for x in h) / sum(x["w"] for x in h)
            print(f"   {name:9s} {LABEL[v]} age " + " / ".join(f"{q:4.1f}" for q in a) + " | education " + " / ".join(f"{q:4.1f}" for q in e)
                  + f" | foreign-born householder {fb:4.1f}% | persons per household {npm:.2f}")
    print("   (age: " + ", ".join(AGE) + "; education: " + ", ".join(EDU) + ")")

    print("\nR3 median earnings of renter workers, 2024 dollars, change after inflation (+/- 1 SE)")
    for c, name in NAMES.items():
        w0, w1 = D[c]["2009"][1], D[c]["2024"][1]
        line = f"   {name:9s}"
        for tag, keep in (("all workers", lambda x: True), ("full-time year-round", lambda x: x["ftyr"])):
            a, b = [x for x in w0 if keep(x)], [x for x in w1 if keep(x)]
            m0, m1 = wmed(a, "earn", weights(a)), wmed(b, "earn", weights(b))
            ch, s = se_of(lambda r: pct(wmed(a, "earn", weights(a, r)), wmed(b, "earn", weights(b, r))))
            line += f" | {tag} ${m0:>7,.0f} -> ${m1:>7,.0f} {ch:+5.1f}% (+/-{s:.1f})"
            if tag.startswith("full"):
                res[c]["ftyr"] = ch
                ft1 = 100 * sum(x["w"] for x in w1 if x["ftyr"]) / sum(x["w"] for x in w1)
                ft0 = 100 * sum(x["w"] for x in w0 if x["ftyr"]) / sum(x["w"] for x in w0)
                line += f" | full-time year-round share of workers {ft0:.0f}% -> {ft1:.0f}%"
        print(line)

    print("\nRenter workers by sector, Gwinnett and Cobb (share of workers with earnings; median earnings 2020-24)")
    for c in ("135", "067"):
        w0, w1 = D[c]["2009"][1], D[c]["2024"][1]
        t0, t1 = sum(x["w"] for x in w0), sum(x["w"] for x in w1)
        print(f"   {NAMES[c]}")
        for _, _, s in SECTORS:
            a = [x for x in w0 if x["sector"] == s]
            b = [x for x in w1 if x["sector"] == s]
            if not b:
                continue
            print(f"      {s:32s} {100 * sum(x['w'] for x in a) / t0:5.1f}% -> {100 * sum(x['w'] for x in b) / t1:5.1f}%"
                  f"  median earnings 2020-24 ${wmed(b, 'earn', weights(b)):>7,.0f}")

    print("\nR4 QCEW average annual pay of jobs located in the county, 2005-09 average to 2020-24 average, after inflation")
    q = qcew()
    for f, ch in sorted(q.items(), key=lambda t: -t[1]):
        print(f"   {f} {NAMES.get(f[2:], 'Forsyth'):9s} {ch:+5.1f}%")

    peers = [c for c in NAMES if c != "135"]
    med = lambda xs: (sorted(xs)[(len(xs) - 1) // 2] + sorted(xs)[len(xs) // 2]) / 2  # noqa: E731
    print("\nRules")
    eff = res["135"]["rw"] - res["135"]["ch"]
    print(f"   R1 mix effect for Gwinnett {eff:+.1f} pts -> {'main factor' if eff >= 3.75 else 'partial factor' if eff >= 1 else 'not a factor'}")
    print(f"   R3 Gwinnett full-time year-round earnings {res['135']['ftyr']:+.1f}% vs Cobb {res['067']['ftyr']:+.1f}%, peer median "
          f"{med([res[c]['ftyr'] for c in peers]):+.1f}%")
    pq = [q["13" + c] for c in peers]
    print(f"   R4 Gwinnett QCEW {q['13135']:+.1f}% vs peer median {med(pq):+.1f}%")


if __name__ == "__main__":
    buf = io.StringIO()
    with redirect_stdout(buf):
        main()
    (ROOT / "research" / "renter-income-output.txt").write_text(buf.getvalue())
    print(buf.getvalue())
