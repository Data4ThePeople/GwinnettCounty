"""L2: change in median earnings of FTYR renter workers after inflation, with 90% margins (SDR)."""
from c2 import *
import pandas as pd
R = pd.read_json(os.path.join(HERE, "out_l1.json"), dtype={"fips": str}); R = R[R.ok]
D = {}
for y in (2009, 2024):
    d = pd.read_pickle(os.path.join(RAW, f"ftyr_{y}.pkl"))
    for c in d.columns:
        if c.startswith("PWGTP") or c in ("PERNP", "ADJINC", "ESR", "TEN", "WKHP"): d[c] = pd.to_numeric(d[c])
    d["state"] = d.state.str.zfill(2)
    d["ADJINC"] = np.where(d.ADJINC > 100, d.ADJINC / 1e6, d.ADJINC)
    d = d[d.ESR.isin([1, 2, 4, 5]) & (d.PERNP > 0) & (d.WKHP >= 35) & d.TEN.isin([3, 4])].copy()
    d["earn"] = d.PERNP * d.ADJINC * (F09 if y == 2009 else 1)
    D[y] = d
def meds(d):
    full = wmed(d.earn, d.PWGTP)
    reps = [wmed(d.earn, d[f"PWGTP{i}"].clip(lower=0)) for i in range(1, 81)]
    return full, reps
out = []
for _, r in R.iterrows():
    st = r.fips[:2]
    a = D[2009][(D[2009].state == st) & D[2009].puma.isin(r.p0)]
    b = D[2024][(D[2024].state == st) & D[2024].puma.isin(r.p2)]
    (m9, r9), (m4, r4) = meds(a), meds(b)
    full = 100 * (m4 / m9 - 1)
    rc = [100 * (x / y_ - 1) for x, y_ in zip(r4, r9)]
    se = np.sqrt(4 / 80 * sum((x - full) ** 2 for x in rc))
    out.append(dict(fips=r.fips, name=r["name"], rent=r.chg, m9=m9, m4=m4, chg=full, moe=1.645 * se, n9=len(a), n4=len(b)))
O = pd.DataFrame(out).sort_values("chg").reset_index(drop=True)
O["rank_from_bottom"] = O.index + 1
for _, r in O.iterrows():
    print(f"{r.rank_from_bottom:2d} {r['name']:30s} rent {r.rent:5.1f}%  earn {r.m9:8.0f} -> {r.m4:8.0f}  {r.chg:+6.1f}% +/- {r.moe:4.1f}  n {r.n9}/{r.n4}"
          + ("  [drop, margin excl 0]" if r.chg + r.moe < 0 else ("  [drop]" if r.chg < 0 else "")))
print("median of county changes:", O.chg.median(), "| middle county:", O.iloc[len(O)//2]["name"], O.iloc[len(O)//2].chg)
O.to_json(os.path.join(HERE, "out_l2.json"), orient="records", indent=1)
