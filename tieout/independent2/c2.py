"""Helpers for independent tie-out 2 (own code). Cached downloads in ./raw."""
import hashlib, json, os, sys, time
import numpy as np, requests
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw"); os.makedirs(RAW, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (Data 4 The People research; eric@asaltollc.com)"}
sys.path.insert(0, os.path.expanduser("~/.claude/d4tp-process"))
from d4tp_env import load_env, get_key
load_env()
AH = os.path.expanduser("~/PycharmProjects/AffordableHousing/data/processed")
CPI = {int(k): v for k, v in json.load(open(os.path.join(AH, "cpi.json"))).items()}
F09 = CPI[2024] / CPI[2009]

def api(path, params, sub="acs"):
    key = path + "?" + "&".join(f"{k}={v}" for k, v in sorted(params.items()))
    d = os.path.join(RAW, sub); os.makedirs(d, exist_ok=True)
    fp = os.path.join(d, hashlib.sha1(key.encode()).hexdigest()[:20] + ".json")
    if os.path.exists(fp):
        rows = json.load(open(fp))
    else:
        p = dict(params); p["key"] = get_key("CENSUS_API_KEY")
        for a in range(8):
            try:
                r = requests.get("https://api.census.gov/data/" + path, params=p, headers=UA, timeout=600)
                if r.status_code == 204: rows = []; break
                r.raise_for_status(); rows = r.json(); break
            except Exception as e:
                if a == 7: raise RuntimeError(f"fail {path} {params}: {str(e)[:200]}")
                time.sleep(5 * (a + 1))
        json.dump(rows, open(fp, "w")); open(fp + ".key", "w").write(key)
    if not rows: return []
    h = rows[0]; return [dict(zip(h, r)) for r in rows[1:]]

def fetch(url, name):
    fp = os.path.join(RAW, name)
    if not os.path.exists(fp):
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        r = requests.get(url, headers=UA, timeout=300); r.raise_for_status()
        open(fp, "wb").write(r.content)
    return fp

def wmed(x, w):
    x = np.asarray(x, float); w = np.asarray(w, float)
    o = np.argsort(x, kind="mergesort"); x, w = x[o], w[o]
    c = np.cumsum(w); return float(x[np.searchsorted(c, c[-1] / 2.0)])
