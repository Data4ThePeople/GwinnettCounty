import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from common import *
for y in (2009, 2024):
    fp = download(f"https://api.census.gov/data/{y}/acs/acs5/pums/variables.json", f"meta/pums_{y}_vars.json")
    v = json.load(open(fp))["variables"]
    for k in ("SERIALNO","SPORDER","RELP","RELSHIPP","TEN","GRNTP","ADJHSG","ADJINC","HINCP","BLD","YBL","YRBLT","WGTP","PWGTP","AGEP","ESR","PERNP","WKHP","WKW","WKWN","SCHL","NP","WGTP1","PWGTP80"):
        if k in v:
            it = v[k]; vals = it.get("values", {}).get("item") or it.get("values", {}).get("range")
            print(y, k, it.get("label"), "|", str(vals)[:250])
        else:
            print(y, k, "MISSING")
r = census("2009/acs/acs5/pums", {"get": "SERIALNO,SPORDER,TEN,GRNTP,ADJHSG,ADJINC,BLD,YBL,WGTP,HINCP", "for": "public use microdata area:01501", "in": "state:13"}, sub="pums_probe")
print(len(r), r[:3])
r = census("2024/acs/acs5/pums", {"get": "SERIALNO,SPORDER,TEN,GRNTP,ADJHSG,ADJINC,BLD,YRBLT,WGTP,HINCP", "for": "public use microdata area:01601", "in": "state:13"}, sub="pums_probe")
print(len(r), r[:3])
