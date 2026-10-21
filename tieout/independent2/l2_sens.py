"""Sensitivity: median definition (lower weighted median vs linear interpolation of weighted CDF)."""
from c2 import *
import pandas as pd
exec(open(os.path.join(HERE, "l2_calc.py")).read().split("def meds")[0])
def interp_med(x, w):
    o = np.argsort(x.values); x = x.values[o]; w = w.values[o]; c = np.cumsum(w) - w / 2
    return float(np.interp(c[-1] / 2 + w[-1] / 2 - 0, c, x)) if False else float(np.interp((c[-1] + w[-1] / 2) / 2, c, x))
for _, r in R.iterrows():
    if r["name"] not in ("Gwinnett County, GA", "Cherokee County, GA", "Ellis County, TX", "Lake County, FL", "Maricopa County, AZ"): continue
    st = r.fips[:2]
    a = D[2009][(D[2009].state == st) & D[2009].puma.isin(r.p0)]; b = D[2024][(D[2024].state == st) & D[2024].puma.isin(r.p2)]
    print(r["name"], "interp-median change", round(100 * (interp_med(b.earn, b.PWGTP) / interp_med(a.earn, a.PWGTP) - 1), 1),
          "| unweighted share at exact median value 2024:", round((b.earn == wmed(b.earn, b.PWGTP)).mean() * 100, 1), "%")
