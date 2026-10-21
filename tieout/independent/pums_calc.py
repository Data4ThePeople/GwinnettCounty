"""D1, D2, E1-E6 from PUMS. Own code."""
import sys, os, json
import numpy as np, pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
C = cpi(); f09 = C[2024] / C[2009]
R = json.load(open(os.path.join(HERE, "out_reach.json")))
CEIL = {"2009": R["2009"]["gw_ceil"], "2024": R["2024"]["gw_ceil"]}
YBL_MODE = os.environ.get("YBL_MODE", "asc")  # how 2009 YBL is coded: "asc" (1=1939 or earlier ... 8=2000-04, 9+=2005+) or "desc" (1=2005+, 9=1939-)

def load(y):
    d = pd.read_pickle(os.path.join(RAW, f"pums_{y}.pkl"))
    num = [c for c in d.columns if c not in ("SERIALNO", "county", "puma", "state", "public use microdata area")]
    for c in num: d[c] = pd.to_numeric(d[c], errors="coerce")
    for c in ("ADJINC", "ADJHSG"):
        d[c] = np.where(d[c] > 100, d[c] / 1e6, d[c])
    d["inc"] = d["HINCP"] * d["ADJINC"] * (f09 if y == "2009" else 1)
    d["earn"] = d["PERNP"] * d["ADJINC"] * (f09 if y == "2009" else 1)
    d["rent"] = d["GRNTP"] * d["ADJHSG"]   # in the file's final-year dollars
    if y == "2009":
        if YBL_MODE == "asc":
            d["pre2000"] = d["YBL"] <= 7; d["b2000s"] = d["YBL"] >= 8
        else:
            d["pre2000"] = d["YBL"] >= 3; d["b2000s"] = d["YBL"] <= 2
        d["ftyr_w"] = d["WKW"] == 1
        s = d["SCHL"]; d["edu"] = np.select([s <= 8, s == 9, s <= 12], [0, 1, 2], 3)
    else:
        d["pre2000"] = d["YRBLT"] < 2000; d["b2000s"] = d["YRBLT"].between(2000, 2009); d["b2010"] = d["YRBLT"] >= 2010
        d["ftyr_w"] = d["WKWN"] >= 50
        s = d["SCHL"]; d["edu"] = np.select([s <= 15, s <= 17, s <= 20], [0, 1, 2], 3)
    d["worker"] = d["ESR"].isin([1, 2, 4, 5])
    d["ftyr"] = d["worker"] & (d["WKHP"] >= 35) & d["ftyr_w"]
    d["apt"] = d["BLD"].between(6, 9); d["house"] = d["BLD"].between(2, 3)
    d["renter"] = d["TEN"].isin([3, 4])
    return d

D = {y: load(y) for y in ("2009", "2024")}
out = {}
def pct(a, b): return 100 * (a / b - 1)

# ---- YBL check: PUMS renter households by YBL code vs B25036 (Gwinnett 2005-09)
g9 = D["2009"]; h = g9[(g9.county == "Gwinnett") & (g9.SPORDER == 1) & g9.renter]
print("2009 Gwinnett renter hh by YBL code (weighted):", h.groupby("YBL").WGTP.sum().to_dict())

# ---- D1 / chart 05 (2024 Gwinnett)
g = D["2024"]; hh = g[(g.county == "Gwinnett") & (g.SPORDER == 1) & (g.TEN == 3)]
tot = hh.WGTP.sum()
new_apt = hh[hh.apt & hh.b2010]
print(f"D1 apts built 2010+: {new_apt.WGTP.sum():.0f} of {tot:.0f} = {100*new_apt.WGTP.sum()/tot:.1f}%; median rent {wmedian(new_apt.rent,new_apt.WGTP):.0f}; all cash-rent median {wmedian(hh.rent,hh.WGTP):.0f}")
print(f"   newer apts vs all: {pct(wmedian(new_apt.rent,new_apt.WGTP), wmedian(hh.rent,hh.WGTP)):.1f}%")
for lab, m in (("pre2000 apt", hh.pre2000 & hh.apt), ("pre2000 house", hh.pre2000 & hh.house), ("2000-09 apt", hh.b2000s & hh.apt),
               ("2000-09 house", hh.b2000s & hh.house), ("2010+ apt", hh.b2010 & hh.apt), ("2010+ house", hh.b2010 & hh.house)):
    s = hh[m]; print(f"   chart05 {lab:14s} n={len(s):4d} wt={s.WGTP.sum():7.0f} median {wmedian(s.rent, s.WGTP):.0f}")
# ---- D2
for y in ("2009", "2024"):
    d = D[y]; hh = d[(d.county == "Gwinnett") & (d.SPORDER == 1) & (d.TEN == 3)]
    s = hh[hh.apt & hh.pre2000]
    w = s[s.rent <= CEIL[y]].WGTP.sum()
    print(f"D2 {y} older apts (cash rent): {s.WGTP.sum():.0f} (n={len(s)}), within reach (rent <= {CEIL[y]:.1f}): {w:.0f} ({100*w/s.WGTP.sum():.1f}% of them)")
    out[f"D2_{y}"] = (s.WGTP.sum(), w)
print(f"   change in older apts {pct(out['D2_2024'][0], out['D2_2009'][0]):.1f}%, within reach {pct(out['D2_2024'][1], out['D2_2009'][1]):.1f}%")

# ---- E: renter households
def hhframe(d, county):
    p = d[(d.county == county) & d.renter]
    hh = p[p.SPORDER == 1].set_index("SERIALNO")
    hh = hh.assign(nw=p.groupby("SERIALNO").worker.sum())
    return p, hh
for county in ("Gwinnett", "Cobb", "DeKalb", "Fulton", "Henry", "Cherokee", "Clayton"):
    res = {}
    for y in ("2009", "2024"):
        p, hh = hhframe(D[y], county)
        f = p[p.ftyr & (p.earn > 0)]
        f0 = p[p.ftyr]
        res[y] = dict(inc=wmedian(hh.inc, hh.WGTP), ft=wmedian(f.earn, f.PWGTP), ft_any=wmedian(f0.earn, f0.PWGTP),
                      mw=np.average(hh.nw, weights=hh.WGTP), two=100 * hh[hh.nw >= 2].WGTP.sum() / hh.WGTP.sum(), n_ft=len(f))
    print(f"E {county:9s} renter hh inc {res['2009']['inc']:.0f}->{res['2024']['inc']:.0f} ({pct(res['2024']['inc'],res['2009']['inc']):.1f}%) | "
          f"FTYR earn {res['2009']['ft']:.0f}->{res['2024']['ft']:.0f} ({pct(res['2024']['ft'],res['2009']['ft']):.1f}%; n {res['2009']['n_ft']}/{res['2024']['n_ft']}; incl <=0 earnings {pct(res['2024']['ft_any'],res['2009']['ft_any']):.1f}%) | "
          f"workers/hh {res['2009']['mw']:.3f}->{res['2024']['mw']:.3f} | 2+ workers {res['2009']['two']:.1f}%->{res['2024']['two']:.1f}%")
    out[county] = res

# Gwinnett replicate margin for E2 and E1
reps = {}
for y in ("2009", "2024"):
    p, hh = hhframe(D[y], "Gwinnett")
    f = p[p.ftyr & (p.earn > 0)]
    reps[y] = dict(ft=[wmedian(f.earn, f[f"PWGTP{i}"].clip(lower=0)) for i in range(1, 81)],
                   inc=[wmedian(hh.inc, hh[f"WGTP{i}"].clip(lower=0)) for i in range(1, 81)])
for k in ("ft", "inc"):
    full = pct(out["Gwinnett"]["2024"][k], out["Gwinnett"]["2009"][k])
    rc = [pct(a, b) for a, b in zip(reps["2024"][k], reps["2009"][k])]
    se = np.sqrt(4 / 80 * sum((r - full) ** 2 for r in rc))
    print(f"Gwinnett {k} change {full:.1f}%  SE {se:.2f} pts  90% MOE +/- {1.645*se:.1f} pts")

# E4, E5
for y in ("2009", "2024"):
    p, hh = hhframe(D[y], "Gwinnett")
    w = p[p.worker & (p.earn > 0)]
    w2 = p[p.earn > 0]
    print(f"E4 {y}: FTYR share of renter workers (employed, earnings>0) {100*w[w.ftyr].PWGTP.sum()/w.PWGTP.sum():.1f}%; "
          f"of all with earnings>0 {100*w2[w2.ftyr].PWGTP.sum()/w2.PWGTP.sum():.1f}%")
    print(f"E5 {y}: householder 65+ {100*hh[hh.AGEP>=65].WGTP.sum()/hh.WGTP.sum():.1f}%; bachelor's+ {100*hh[hh.edu==3].WGTP.sum()/hh.WGTP.sum():.1f}%")

# E6 reweight 2024 to 2009 cell mix
def cells(hh):
    wk = np.minimum(hh.nw, 2); ag = np.select([hh.AGEP < 35, hh.AGEP < 65], [0, 1], 2)
    return wk.astype(int) * 100 + ag * 10 + hh.edu.astype(int)
_, h9 = hhframe(D["2009"], "Gwinnett"); _, h4 = hhframe(D["2024"], "Gwinnett")
h9 = h9.assign(cell=cells(h9)); h4 = h4.assign(cell=cells(h4))
s9 = h9.groupby("cell").WGTP.sum() / h9.WGTP.sum(); s4 = h4.groupby("cell").WGTP.sum() / h4.WGTP.sum()
missing = set(s9.index) - set(s4.index)
fac = (s9 / s4).reindex(h4.cell).fillna(0).values
w_rw = h4.WGTP.values * fac
m_rw = wmedian(h4.inc, w_rw)
print(f"E6 reweighted 2024 median {m_rw:.0f} vs 2009 {out['Gwinnett']['2009']['inc']:.0f}: change {pct(m_rw, out['Gwinnett']['2009']['inc']):.1f}% "
      f"(actual {pct(out['Gwinnett']['2024']['inc'], out['Gwinnett']['2009']['inc']):.1f}%); 2009 cells missing in 2024: {len(missing)} "
      f"(share {100*s9.reindex(list(missing)).sum() if missing else 0:.2f}%); cells 36 possible, 2009 {len(s9)}, 2024 {len(s4)}")
