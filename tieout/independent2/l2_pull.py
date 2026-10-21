"""Pull FTYR renter workers for PUMAs of the measurable counties, both periods, with 80 replicate weights."""
from c2 import *
import pandas as pd, collections
R = pd.read_json(os.path.join(HERE, "out_l1.json"), dtype={"fips": str})
R = R[R.ok]
need = {2009: collections.defaultdict(list), 2024: collections.defaultdict(list)}
for _, r in R.iterrows():
    need[2009][r.fips[:2]] += r.p0; need[2024][r.fips[:2]] += r.p2
WK = {2009: {"WKW": "1"}, 2024: {"WKWN": "50:52"}}
frames = {2009: [], 2024: []}
for y in (2009, 2024):
    for st, ps in sorted(need[y].items()):
        ps = sorted(set(ps)); geo = ",".join(p if y == 2024 else p for p in ps)
        parts = []
        for g in ("PERNP,ADJINC,PWGTP,ESR,TEN,WKHP", ",".join(f"PWGTP{i}" for i in range(1, 41)), ",".join(f"PWGTP{i}" for i in range(41, 81))):
            rows = api(f"{y}/acs/acs5/pums", {"get": "SERIALNO,SPORDER," + g, "for": "public use microdata area:" + geo, "in": f"state:{st}",
                                              "TEN": "3:4", "WKHP": "35:99", "ESR": "1:5", **WK[y]}, sub="ftyr")
            d = pd.DataFrame(rows).drop(columns=[c for c in ("WKW", "WKWN", "TEN_", "WKHP_") if False], errors="ignore")
            parts.append(d)
        base = parts[0]
        for p in parts[1:]:
            p = p[["SERIALNO", "SPORDER"] + [c for c in p.columns if c.startswith("PWGTP")]]
            assert len(p) == len(base), (y, st, len(p), len(base))
            base = base.merge(p, on=["SERIALNO", "SPORDER"], how="inner", validate="1:1")
        assert len(base) == len(parts[0])
        base["puma"] = base["public use microdata area"].str.zfill(5)
        print(y, st, len(ps), "PUMAs", len(base), "rows", flush=True)
        frames[y].append(base)
    pd.concat(frames[y]).to_pickle(os.path.join(RAW, f"ftyr_{y}.pkl"))
