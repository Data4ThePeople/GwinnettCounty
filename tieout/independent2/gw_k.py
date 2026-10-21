"""K1-K4 from Gwinnett household PUMS."""
from c2 import *
import pandas as pd
R = json.load(open(os.path.join(HERE, "out_reach.json"))); AMT = {2009: R["gw"]["2009"], 2024: R["gw"]["2024"]}
D = {}
for y in (2009, 2024):
    d = pd.read_pickle(os.path.join(RAW, f"gw_hh_{y}.pkl"))
    d["rent"] = d.GRNTP * d.ADJHSG / 1e6
    d["house"] = d.BLD.between(2, 3); d["apt"] = d.BLD.between(6, 9)
    if y == 2009:
        d["pre2000"] = d.YBL >= 3; d["b2000"] = d.YBL <= 2; d["b2010"] = False
    else:
        d["pre2000"] = d.YRBLT < 2000; d["b2000"] = d.YRBLT.between(2000, 2009); d["b2010"] = d.YRBLT >= 2010
    D[y] = d
def wmed_interp(x, w):  # alternative: midpoint-of-50%-weight
    o = np.argsort(x.values); x = x.values[o]; w = w.values[o]; c = np.cumsum(w); h = c[-1] / 2
    i = np.searchsorted(c, h); return float(x[i]) if c[i] > h or i + 1 >= len(x) else (x[i] + x[i + 1]) / 2
def grp(d, m): s = d[m]; return s
out = {}
t9, t4 = D[2009].WGTP.sum(), D[2024].WGTP.sum()
print(f"K1 total cash-rent renter hh {t9:.0f} -> {t4:.0f}, change {t4-t9:+.0f} ({100*(t4/t9-1):.1f}%)")
groups = {"house_pre2000": lambda d: d.house & d.pre2000, "apt_pre2000": lambda d: d.apt & d.pre2000,
          "house_2000s": lambda d: d.house & d.b2000, "apt_2000s": lambda d: d.apt & d.b2000,
          "house_2010": lambda d: d.house & d.b2010, "apt_2010": lambda d: d.apt & d.b2010,
          "house_all": lambda d: d.house, "apt_all": lambda d: d.apt}
ch = {}
for k, f in groups.items():
    a = D[2009][f(D[2009])]; b = D[2024][f(D[2024])]
    ch[k] = b.WGTP.sum() - a.WGTP.sum()
    print(f"  {k:14s} 2009 {a.WGTP.sum():7.0f} (n={len(a):4d}) 2024 {b.WGTP.sum():7.0f} (n={len(b):4d}) change {ch[k]:+7.0f}")
both = ch["house_pre2000"] + ch["apt_2010"]
print(f"K1 houses pre-2000 {ch['house_pre2000']:+.0f}, apts 2010+ {ch['apt_2010']:+.0f}, combined {both:+.0f} = {100*both/(t4-t9):.1f}% of total change")
print(f"K2 affordable amount 2024: {AMT[2024]:.2f}; 2009: {AMT[2009]:.2f} (2009$) = {AMT[2009]*F09:.2f} (2024$)")
d = D[2024]
print(f"   all cash-rent 2024 median {wmed(d.rent,d.WGTP):.0f}, within reach {100*d[d.rent<=AMT[2024]].WGTP.sum()/d.WGTP.sum():.1f}%; 2009 median {wmed(D[2009].rent,D[2009].WGTP):.0f} within {100*D[2009][D[2009].rent<=AMT[2009]].WGTP.sum()/t9:.1f}%")
for k in ("house_pre2000", "apt_2010", "house_2010", "apt_pre2000", "house_2000s", "apt_2000s"):
    s = d[groups[k](d)]
    print(f"K3 2024 {k:14s} median {wmed(s.rent,s.WGTP):.0f} (alt {wmed_interp(s.rent,s.WGTP):.0f}) within reach {100*s[s.rent<=AMT[2024]].WGTP.sum()/s.WGTP.sum():.1f}%  n={len(s)}")
a = D[2009][groups["apt_pre2000"](D[2009])]; b = d[groups["apt_pre2000"](d)]
m9, m4 = wmed(a.rent, a.WGTP), wmed(b.rent, b.WGTP)
print(f"K4 older apts count {a.WGTP.sum():.0f} -> {b.WGTP.sum():.0f} ({100*(b.WGTP.sum()/a.WGTP.sum()-1):.1f}%)")
print(f"   median rent 2009 {m9:.0f} (alt {wmed_interp(a.rent,a.WGTP):.0f}) [{m9*F09:.0f} in 2024$], 2024 {m4:.0f} (alt {wmed_interp(b.rent,b.WGTP):.0f})")
print(f"   change before inflation {100*(m4/m9-1):.1f}%, after {100*(m4/(m9*F09)-1):.1f}%")
A9 = AMT[2009] * F09
print(f"   amount 2024$: {A9:.0f} -> {AMT[2024]:.0f} ({100*(AMT[2024]/A9-1):.1f}%)")
print(f"   gap rent - amount: 2005-09 {m9*F09 - A9:+.0f}, 2020-24 {m4 - AMT[2024]:+.0f}")
print(f"   older apts within reach: 2009 {100*a[a.rent<=AMT[2009]].WGTP.sum()/a.WGTP.sum():.1f}%  2024 {100*b[b.rent<=AMT[2024]].WGTP.sum()/b.WGTP.sum():.1f}%")
