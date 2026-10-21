"""County<->PUMA maps: 2000 PUMAs (PUMEQ5 files) and 2020 PUMAs (tract file)."""
from c2 import *
import collections
STNAME = {"01":"Alabama","02":"Alaska","04":"Arizona","05":"Arkansas","06":"California","08":"Colorado","09":"Connecticut","10":"Delaware","11":"District_of_Columbia","12":"Florida","13":"Georgia","15":"Hawaii","16":"Idaho","17":"Illinois","18":"Indiana","19":"Iowa","20":"Kansas","21":"Kentucky","22":"Louisiana","23":"Maine","24":"Maryland","25":"Massachusetts","26":"Michigan","27":"Minnesota","28":"Mississippi","29":"Missouri","30":"Montana","31":"Nebraska","32":"Nevada","33":"New_Hampshire","34":"New_Jersey","35":"New_Mexico","36":"New_York","37":"North_Carolina","38":"North_Dakota","39":"Ohio","40":"Oklahoma","41":"Oregon","42":"Pennsylvania","44":"Rhode_Island","45":"South_Carolina","46":"South_Dakota","47":"Tennessee","48":"Texas","49":"Utah","50":"Vermont","51":"Virginia","53":"Washington","54":"West_Virginia","55":"Wisconsin","56":"Wyoming"}
ABBR = {"01":"AL","02":"AK","04":"AZ","05":"AR","06":"CA","08":"CO","09":"CT","10":"DE","11":"DC","12":"FL","13":"GA","15":"HI","16":"ID","17":"IL","18":"IN","19":"IA","20":"KS","21":"KY","22":"LA","23":"ME","24":"MD","25":"MA","26":"MI","27":"MN","28":"MS","29":"MO","30":"MT","31":"NE","32":"NV","33":"NH","34":"NJ","35":"NM","36":"NY","37":"NC","38":"ND","39":"OH","40":"OK","41":"OR","42":"PA","44":"RI","45":"SC","46":"SD","47":"TN","48":"TX","49":"UT","50":"VT","51":"VA","53":"WA","54":"WV","55":"WI","56":"WY"}
def map2000(st):
    a = ABBR[st]; nm = STNAME[st]
    urls = [f"https://www2.census.gov/census_2000/datasets/PUMS/FivePercent/{nm}/PUMEQ5-{a}.TXT",
            f"https://www2.census.gov/census_2000/datasets/PUMS/FivePercent/{nm}/PUMEQ5-{st}.TXT"]
    fp = None
    for u in urls:
        try: fp = fetch(u, f"puma/PUMEQ5-{a}.TXT"); break
        except Exception: pass
    if fp is None: raise RuntimeError("no PUMEQ5 for " + st)
    p2c = collections.defaultdict(set)
    for ln in open(fp, encoding="latin-1"):
        t = ln.split()
        if len(t) > 4 and t[0] == "781" and t[1] == st: p2c[t[3]].add(st + t[4])
    return p2c
def map2020():
    fp = fetch("https://www2.census.gov/geo/docs/maps-data/data/rel2020/2020_Census_Tract_to_2020_PUMA.txt", "puma/tract2020_puma2020.txt")
    p2c = collections.defaultdict(set)
    for ln in open(fp, encoding="utf-8-sig").read().splitlines()[1:]:
        t = ln.split(",")
        p2c[(t[0], t[3])].add(t[0] + t[1])
    return p2c
def nests(county, p2c):
    """PUMAs touching county; True if every one lies wholly inside it."""
    ps = sorted(p for p, cs in p2c.items() if county in cs)
    return ps, bool(ps) and all(p2c[p] == {county} for p in ps)
