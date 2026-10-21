"""L1: large-metro counties, rent up 25%+ after inflation, measurable on their own."""
from c2 import *
from puma import *
import pandas as pd
N = pd.read_csv(os.path.join(RAW, "nchs/NCHSUR2023_3156.csv"), encoding="latin-1", dtype=str)
N["fips"] = N.STFIPS.str.zfill(2) + N.CTYFIPS.str.zfill(3)
big = N[N.CODE2023.isin(["1", "2"])]
print("NCHS code 1/2 rows:", len(big), "| with current pop:", big.CTYPOP.notna().sum(), "| code1", (big.CODE2023=="1").sum(), "code2", (big.CODE2023=="2").sum())
A9 = json.load(open(os.path.join(RAW, "acs_2009.json"))); A4 = json.load(open(os.path.join(RAW, "acs_2024.json")))
rows = []
for _, r in big.iterrows():
    f = r.fips
    a, b = A9.get(f), A4.get(f)
    rows.append(dict(fips=f, name=f"{r.CTYNAME}, {r.ST_ABBREV}", code=r.CODE2023, cur=pd.notna(r.CTYPOP),
                     r9=a["B25064_001E"] if a else None, r4=b["B25064_001E"] if b else None))
df = pd.DataFrame(rows)
print("in 2024 ACS:", df.r4.notna().sum(), "| in both:", (df.r4.notna() & df.r9.notna()).sum(),
      "| current-pop rows missing 2009:", df[df.cur & df.r9.isna()].name.tolist(), "| missing 2024:", df[df.r4.isna()].name.tolist()[:12])
both = df[df.r4.notna() & df.r9.notna() & (df.r4 > 0) & (df.r9 > 0)].copy()
both["chg"] = 100 * (both.r4 / (both.r9 * F09) - 1)
up = both[both.chg >= 25].sort_values("chg", ascending=False).copy()
print("large-metro counties with rent in both periods:", len(both), "| rent up 25%+ after inflation:", len(up))
m20 = map2020(); cache = {}
res = []
for _, r in up.iterrows():
    st = r.fips[:2]
    if st not in cache: cache[st] = map2000(st)
    p0, ok0 = nests(r.fips, cache[st])
    p2, ok2 = nests(r.fips, {p: c for (s, p), c in m20.items() if s == st})
    res.append(dict(fips=r.fips, name=r["name"], chg=r.chg, ok=ok0 and ok2, ok0=ok0, ok2=ok2, p0=p0, p2=p2))
R = pd.DataFrame(res)
print("measurable on own:", R.ok.sum(), "| not:", (~R.ok).sum(), "| fail 2000 only", (~R.ok0 & R.ok2).sum(), "fail 2020 only", (R.ok0 & ~R.ok2).sum(), "both fail", (~R.ok0 & ~R.ok2).sum())
for _, r in R.iterrows(): print(f"  {r.fips} {r['name']:32s} {r.chg:6.1f}%  {'MEASURABLE' if r.ok else '-'}  2000:{len(r.p0)} {r.ok0}  2020:{len(r.p2)} {r.ok2}")
R.to_json(os.path.join(HERE, "out_l1.json"), orient="records", indent=1)
