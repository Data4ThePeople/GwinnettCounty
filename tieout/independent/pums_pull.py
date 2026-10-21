"""Pull PUMS person records (all tenures) for the seven nesting counties, 2009 and 2024; replicate weights for Gwinnett."""
import sys, os, json
import pandas as pd
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
P = json.load(open(os.path.join(HERE, "pumas.json")))
base = {"2009": "SERIALNO,SPORDER,TEN,GRNTP,ADJHSG,ADJINC,HINCP,BLD,YBL,WGTP,NP,AGEP,ESR,PERNP,WKHP,WKW,SCHL,PWGTP",
        "2024": "SERIALNO,SPORDER,TEN,GRNTP,ADJHSG,ADJINC,HINCP,BLD,YRBLT,WGTP,NP,AGEP,ESR,PERNP,WKHP,WKWN,SCHL,PWGTP"}
for y in ("2009", "2024"):
    frames = []
    for county, pumas in P[y].items():
        if county == "Forsyth": continue
        for pu in pumas:
            rows = census(f"{y}/acs/acs5/pums", {"get": base[y], "for": f"public use microdata area:{pu}", "in": "state:13"}, sub="pums")
            df = pd.DataFrame(rows); df["county"] = county; df["puma"] = pu
            if county == "Gwinnett":
                for blk in (range(1, 41), range(41, 81)):
                    for wt in ("PWGTP", "WGTP"):
                        g = "SERIALNO,SPORDER," + ",".join(f"{wt}{i}" for i in blk)
                        rr = pd.DataFrame(census(f"{y}/acs/acs5/pums", {"get": g, "for": f"public use microdata area:{pu}", "in": "state:13"}, sub="pums"))
                        rr = rr.drop(columns=[c for c in rr.columns if c in ("state", "public use microdata area")])
                        df = df.merge(rr, on=["SERIALNO", "SPORDER"], how="left", validate="1:1")
            frames.append(df)
            print(y, county, pu, len(df), flush=True)
    out = pd.concat(frames, ignore_index=True)
    out.to_parquet(os.path.join(RAW, f"pums_{y}.parquet")) if False else out.to_pickle(os.path.join(RAW, f"pums_{y}.pkl"))
    print(y, "total rows", len(out))
