"""How does Gwinnett's -3.3% change in full-time renter pay rank among large-metro counties whose rents rose 25% or
more after inflation? (DATASETS.md section 13.)

Universe: counties in metros of 1 million or more (NCHS 2023 codes 1 and 2, as in 02 and 03), whose median gross rent
(the tool's harmonized file) rose 25% or more after inflation from 2005-09 to 2020-24, and that are exactly a set of
whole PUMAs in both periods. Measure: median earnings (PERNP x ADJINC, CPI-U to 2024 dollars) of full-time
year-round workers in renter households, as in 12_renter_income.py; standard errors from the 80 replicate weights.

Output: research/national-pay-output.txt"""
import io
import json
import math
import re
import sys
from collections import defaultdict
from contextlib import redirect_stdout
from importlib import import_module
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
AH = Path.home() / "PycharmProjects" / "AffordableHousing"
sys.path.insert(0, str(AH / "scripts"))
from common import PROC  # noqa: E402

F14 = import_module("14_fetch_national_pay")
RAW = ROOT / "data" / "raw"
G = "13135"
THRESHOLD = 25


def pumas_2000():
    """county FIPS -> set of 2000 PUMAs, and (state, PUMA) -> set of counties, from summary level 781 lines."""
    c2p, p2c = defaultdict(set), defaultdict(set)
    for st, (_, ab) in F14.STATES.items():
        for line in (RAW / "puma" / f"PUMEQ5-{ab}.TXT").read_text(encoding="latin-1").splitlines():
            m = re.match(r"\s*781 (\d\d) \d{5} (\d{5}) (\d{3})\s", line)
            if m:
                c2p[m[1] + m[3]].add((m[1], m[2]))
                p2c[(m[1], m[2])].add(m[1] + m[3])
    return c2p, p2c


def pumas_2020():
    d = pd.read_csv(RAW / "puma" / "tract2020_puma2020.txt", dtype=str, encoding="utf-8-sig")
    c2p, p2c = defaultdict(set), defaultdict(set)
    for st, co, pu in zip(d.STATEFP, d.COUNTYFP, d.PUMA5CE):
        c2p[st + co].add((st, pu))
        p2c[(st, pu)].add(st + co)
    return c2p, p2c


def nests(fips, c2p, p2c):
    return bool(c2p.get(fips)) and all(p2c[p] == {fips} for p in c2p[fips])


def adj(s):
    return float(s) if "." in s else int(s) / 1e6


def load_state(v, st, k):
    parts = [json.loads((RAW / "pums_ftyr" / f"{v}_{st}_{i}.json").read_text()) for i in range(3)]
    if len(parts[0]) < 2:
        return defaultdict(list)
    h = [{c: i for i, c in enumerate(p[0])} for p in parts]
    reps = [{(r[x["SERIALNO"]], r[x["SPORDER"]]): r for r in p[1:]} for p, x in zip(parts[1:], h[1:])]
    keys = {(r[h[0]["SERIALNO"]], r[h[0]["SPORDER"]]) for r in parts[0][1:]}
    assert all(set(rp) == keys for rp in reps), (v, st)    # an API pull once came back with mismatched rows (DATASETS.md section 13)
    out = defaultdict(list)
    h0 = h[0]
    for r in parts[0][1:]:
        earn = int(r[h0["PERNP"]] or 0)
        if earn <= 0:
            continue
        key = (r[h0["SERIALNO"]], r[h0["SPORDER"]])
        rw = [int(reps[0][key][h[1][f"PWGTP{i}"]]) for i in range(1, 41)] + [int(reps[1][key][h[2][f"PWGTP{i}"]]) for i in range(41, 81)]
        out[r[h0["public use microdata area"]].zfill(5)].append((earn * adj(r[h0["ADJINC"]]) * k, int(r[h0["PWGTP"]]), rw))
    return out


def wmed(rows, r=None):
    pairs = sorted((e, w if r is None else rw[r]) for e, w, rw in rows)
    half, run = sum(w for _, w in pairs) / 2, 0
    for e, w in pairs:
        run += w
        if run >= half:
            return e


def compute():
    """Returns (res, rent, hot, metro, names): res[fips] = (change %, SE, 2005-09 median, 2020-24 median, n0, n1)
    for every measurable large-metro county. Also used by 09_charts.py and 13_tieout.py."""
    cpi = json.loads((PROC / "cpi.json").read_text())
    k = {v: cpi["2024"] / cpi[v] for v in ("2009", "2024")}
    H = json.loads((PROC / "harmonized.json").read_text())
    nchs = pd.read_csv(RAW / "nchs" / "NCHSUR2023_3156.csv", encoding="latin-1")
    nchs["fips"] = nchs.STFIPS.map("{:02d}".format) + nchs.CTYFIPS.map("{:03d}".format)
    big = nchs[nchs.CODE2023.isin([1, 2]) & nchs.CTYPOP.notna()]
    metro = dict(zip(big.fips, big.CBSATITLE))

    rent = {}
    for f in metro:
        u = H["units"].get(f)
        if not u or "na" in u["f"]["2009"] or "na" in u["f"]["2024"] or not u["f"]["2009"]["mr"]:
            continue
        rent[f] = 100 * (u["f"]["2024"]["mr"] / (u["f"]["2009"]["mr"] * k["2009"]) - 1)
    hot = {f for f, ch in rent.items() if ch >= THRESHOLD}
    P0, P1 = pumas_2000(), pumas_2020()
    ok = {f for f in metro if f in rent and nests(f, *P0) and nests(f, *P1)}

    data = {}
    for v in ("2009", "2024"):
        c2p = (P0 if v == "2009" else P1)[0]
        for st in sorted({f[:2] for f in ok}):
            recs = load_state(v, st, k[v])
            for f in ok:
                if f[:2] == st:
                    data.setdefault(f, {})[v] = [x for _, pu in c2p[f] for x in recs.get(pu, [])]
    res = {}
    for f, d in data.items():
        a, b = d["2009"], d["2024"]
        if len(a) < 30 or len(b) < 30:
            continue
        ch = lambda r: 100 * (wmed(b, r) / wmed(a, r) - 1)  # noqa: E731
        m = ch(None)
        se = math.sqrt(4 / 80 * sum((ch(r) - m) ** 2 for r in range(80)))
        res[f] = (m, se, wmed(a), wmed(b), len(a), len(b))

    return res, rent, hot, metro, {f: H["units"][f]["name"] for f in res}, (len(metro), len(rent), len(hot), len(hot & ok), len(ok))


def main():
    res, rent, hot, metro, names, counts = compute()
    print(f"Counties in 1M+ metros: {counts[0]}; with rent data: {counts[1]}; rent up {THRESHOLD}%+ after inflation: {counts[2]};"
          f" of those, measurable from whole PUMAs in both periods: {counts[3]}")
    print(f"All large-metro counties measurable from whole PUMAs: {counts[4]}")
    name = names.get
    for label, pool in ((f"rent up {THRESHOLD}%+ after inflation", [f for f in res if f in hot]), ("all large-metro counties", list(res))):
        pool = sorted(pool, key=lambda f: res[f][0])
        g = pool.index(G) + 1 if G in pool else None
        below = [f for f in pool if res[f][0] < res[G][0]]
        sig_lower = [f for f in pool if f != G and res[f][0] + 1.645 * math.hypot(res[f][1], res[G][1]) < res[G][0]]
        print(f"\n{label}: {len(pool)} counties. Gwinnett {res[G][0]:+.1f}% (+/-{1.645 * res[G][1]:.1f}) ranks {g} from the lowest;"
              f" {len(below)} counties lower, {len(sig_lower)} of them lower by more than the combined margin."
              f" Median county {sorted(res[f][0] for f in pool)[len(pool) // 2]:+.1f}%; share with a fall {100 * sum(res[f][0] < 0 for f in pool) / len(pool):.0f}%")
        if label.startswith("rent"):
            print("   Lowest 15:")
            for f in pool[:15]:
                m, se, a, b, na, nb = res[f]
                print(f"      {name(f):34s} {metro[f][:38]:38s} pay {m:+5.1f}% (+/-{1.645 * se:4.1f})  ${a:>7,.0f} -> ${b:>7,.0f}  rent {rent[f]:+5.1f}%"
                      f"  n {na}/{nb}")
            print("   Atlanta metro counties in this group:")
            for f in pool:
                if metro[f].startswith("Atlanta"):
                    m, se = res[f][:2]
                    print(f"      {name(f):34s} pay {m:+5.1f}% (+/-{1.645 * se:4.1f})  rent {rent[f]:+5.1f}%  rank {pool.index(f) + 1}")
    H = json.loads((PROC / "harmonized.json").read_text())
    left = sorted(f for f in hot if f not in res)
    print(f"\nRent up {THRESHOLD}%+ but not measurable (shared PUMA or small sample): {len(left)}; Atlanta ones: "
          + ", ".join(H["units"][f]["name"] for f in left if metro[f].startswith("Atlanta")))


if __name__ == "__main__":
    buf = io.StringIO()
    with redirect_stdout(buf):
        main()
    (ROOT / "research" / "national-pay-output.txt").write_text(buf.getvalue())
    print(buf.getvalue())
