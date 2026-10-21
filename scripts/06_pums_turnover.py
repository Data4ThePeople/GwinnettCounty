"""Explanation 5: were new leases priced well above old ones? ACS PUMS, renter households, 2005-09 and 2020-24.

Recent movers moved in within the last two years (MV 1-2); longer-term renters moved in 2 or more years ago
(MV 3-7). Rents are in each file's final-year dollars (GRNTP x ADJHSG). Medians are weighted by WGTP; standard
errors come from the 80 replicate weights (successive difference formula: SE = sqrt(4/80 * sum of squared
differences)). Forsyth is left out: its 2000 PUMA also covers Dawson and Pickens (DATASETS.md section 7).

Rule set in the plan: the gap between recent movers and longer-term renters is much larger in Gwinnett than in
the peers.

Output: research/pums-turnover-output.txt"""
import io
import json
import math
import sys
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
from importlib import import_module  # noqa: E402

PUMAS = import_module("04_fetch_county_tables").PUMAS
RAW = ROOT / "data" / "raw" / "pums"
NAMES = {"135": "Gwinnett", "121": "Fulton", "089": "DeKalb", "067": "Cobb", "063": "Clayton", "151": "Henry", "057": "Cherokee"}
LABEL = {"2009": "2005-09", "2024": "2020-24"}
SF, APT = {2, 3}, {6, 7, 8, 9}


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
            out.append({"rent": rent * adj, "mv": int(row[h["MV"]]), "bld": int(row[h["BLD"]]), "w": int(row[h["WGTP"]]), "rw": w})
    return out


def wmedian(rows, wkey=None, r=None):
    pairs = sorted((x["rent"], x["w"] if r is None else x["rw"][r]) for x in rows)
    half, run = sum(w for _, w in pairs) / 2, 0
    for rent, w in pairs:
        run += w
        if run >= half:
            return rent
    return None


def est(rows):
    m = wmedian(rows)
    se = math.sqrt(4 / 80 * sum((wmedian(rows, r=r) - m) ** 2 for r in range(80)))
    return m, se, sum(x["w"] for x in rows)


def ratio(a, b):
    m = wmedian(a) / wmedian(b)
    se = math.sqrt(4 / 80 * sum((wmedian(a, r=r) / wmedian(b, r=r) - m) ** 2 for r in range(80)))
    return m, se


def main():
    print("Median gross rent, cash-rent renter households, each file's final-year dollars")
    print("recent = moved in within the last 2 years; longer = 2 or more years ago; premium = recent / longer - 1 (+/- 1 standard error)")
    for c, name in NAMES.items():
        for v in ("2009", "2024"):
            rows = records(v, c)
            rec = [x for x in rows if x["mv"] in (1, 2)]
            old = [x for x in rows if x["mv"] >= 3]
            (mr, sr, nr), (mo, so, no) = est(rec), est(old)
            pr, ps = ratio(rec, old)
            line = (f"  {name:9s} {LABEL[v]}  recent ${mr:,.0f} (+/-{sr:,.0f}, {nr:,} households)  longer ${mo:,.0f} (+/-{so:,.0f}, {no:,})"
                    f"  premium {100 * (pr - 1):+5.1f}% (+/-{100 * ps:.1f})")
            for tag, keep in (("single-family", SF), ("5+ unit apartments", APT)):
                a, b = [x for x in rec if x["bld"] in keep], [x for x in old if x["bld"] in keep]
                if a and b:
                    q, qs = ratio(a, b)
                    line += f" | {tag} {100 * (q - 1):+5.1f}% (+/-{100 * qs:.1f})"
            print(line)


if __name__ == "__main__":
    buf = io.StringIO()
    with redirect_stdout(buf):
        main()
    (ROOT / "research").mkdir(exist_ok=True)
    (ROOT / "research" / "pums-turnover-output.txt").write_text(buf.getvalue())
    print(buf.getvalue())
