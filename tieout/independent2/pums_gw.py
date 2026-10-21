"""Gwinnett household PUMS, renter households (TEN=3 cash rent), 2009 and 2024, own pull."""
from c2 import *
from puma import *
import pandas as pd
m0 = map2000("13"); m2 = map2020()
p09, ok09 = nests("13135", m0); p24, ok24 = nests("13135", {p: c for (s, p), c in m2.items() if s == "13"})
print("2000 PUMAs", p09, ok09, "| 2020 PUMAs", p24, ok24)
V = {2009: "SERIALNO,SPORDER,TEN,GRNTP,ADJHSG,BLD,YBL,WGTP", 2024: "SERIALNO,SPORDER,TEN,GRNTP,ADJHSG,BLD,YRBLT,WGTP"}
for y, pumas in ((2009, p09), (2024, p24)):
    rows = api(f"{y}/acs/acs5/pums", {"get": V[y], "for": "public use microdata area:*", "in": "state:13", "TEN": "3", "SPORDER": "1"}, sub="pums")
    d = pd.DataFrame(rows)
    d["puma"] = d["public use microdata area"].str.zfill(5)
    d = d[d.puma.isin(pumas)].copy()
    for c in d.columns:
        if c not in ("SERIALNO", "puma", "public use microdata area", "state"): d[c] = pd.to_numeric(d[c])
    print(y, len(d), "rows; PUMAs", sorted(d.puma.unique()), "weighted", d.WGTP.sum(), "TEN", d.TEN.unique(), "SPORDER", d.SPORDER.unique())
    d.to_pickle(os.path.join(RAW, f"gw_hh_{y}.pkl"))
