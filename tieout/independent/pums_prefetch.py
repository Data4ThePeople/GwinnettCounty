"""Warm the PUMS cache in parallel (same calls as pums_pull.py)."""
import sys, os, json
from concurrent.futures import ThreadPoolExecutor, as_completed
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
P = json.load(open(os.path.join(HERE, "pumas.json")))
base = {"2009": "SERIALNO,SPORDER,TEN,GRNTP,ADJHSG,ADJINC,HINCP,BLD,YBL,WGTP,NP,AGEP,ESR,PERNP,WKHP,WKW,SCHL,PWGTP",
        "2024": "SERIALNO,SPORDER,TEN,GRNTP,ADJHSG,ADJINC,HINCP,BLD,YRBLT,WGTP,NP,AGEP,ESR,PERNP,WKHP,WKWN,SCHL,PWGTP"}
jobs = []
for y in ("2009", "2024"):
    for county, pumas in P[y].items():
        if county == "Forsyth": continue
        for pu in pumas:
            jobs.append((y, base[y], pu))
            if county == "Gwinnett":
                for blk in (range(1, 41), range(41, 81)):
                    for wt in ("PWGTP", "WGTP"):
                        jobs.append((y, "SERIALNO,SPORDER," + ",".join(f"{wt}{i}" for i in blk), pu))
def run(j):
    y, g, pu = j
    census(f"{y}/acs/acs5/pums", {"get": g, "for": f"public use microdata area:{pu}", "in": "state:13"}, sub="pums")
    return j
with ThreadPoolExecutor(8) as ex:
    n = 0
    for f in as_completed([ex.submit(run, j) for j in jobs]):
        f.result(); n += 1
        if n % 10 == 0: print(n, "of", len(jobs), flush=True)
print("prefetch done", len(jobs))
