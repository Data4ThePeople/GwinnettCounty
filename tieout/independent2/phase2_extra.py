"""Exact values at rounding boundaries; within-reach change by group (phase 2 support)."""
from c2 import *
import pandas as pd
from reach import units
U = units(2024)
for f in ("13211", "12097", "13013", "13057", "13187", "28143", "08013", "48259", "13063", "13135"):
    print(f, U[f]["name"], repr(100 * U[f]["share"]))
exec(open(os.path.join(HERE, "gw_k.py")).read().split("ch = {}")[0])
d = D[2024]; s = d[d.house & d.pre2000]; print("house pre2000 2024 median exact", wmed(s.rent, s.WGTP))
a = D[2009][D[2009].apt & D[2009].pre2000]; print("older apt 2009 median exact", wmed(a.rent, a.WGTP), "x F09", wmed(a.rent, a.WGTP) * F09)
print("within-reach households by group (PUMS), 2005-09 -> 2020-24:")
tot = {}
for k, f in groups.items():
    if k.endswith("_all"): continue
    w = [D[y][f(D[y]) & (D[y].rent <= AMT[y])].WGTP.sum() for y in (2009, 2024)]
    print(f"  {k:14s} {w[0]:7.0f} -> {w[1]:7.0f} ({w[1]-w[0]:+.0f})")
w = [D[y][D[y].rent <= AMT[y]].WGTP.sum() for y in (2009, 2024)]
print(f"  ALL            {w[0]:7.0f} -> {w[1]:7.0f} ({w[1]-w[0]:+.0f})")
