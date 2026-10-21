"""Shared helpers for the independent tie-out. Cached downloads only."""
import hashlib
import json
import os
import sys
import time

import numpy as np
import requests

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
os.makedirs(RAW, exist_ok=True)
UA = {"User-Agent": "Mozilla/5.0 (Data 4 The People research; eric@asaltollc.com)"}

sys.path.insert(0, os.path.expanduser("~/.claude/d4tp-process"))
from d4tp_env import load_env, get_key  # noqa: E402

load_env()


def _cache_path(sub, key, ext):
    d = os.path.join(RAW, sub)
    os.makedirs(d, exist_ok=True)
    h = hashlib.md5(key.encode()).hexdigest()[:16]
    return os.path.join(d, h + ext)


def census(path, params, sub="acs"):
    """GET api.census.gov/data/{path} with params; returns list of dicts. Cached."""
    key = path + "?" + "&".join(f"{k}={v}" for k, v in sorted(params.items()))
    fp = _cache_path(sub, key, ".json")
    if os.path.exists(fp):
        with open(fp) as f:
            rows = json.load(f)
    else:
        p = dict(params)
        p["key"] = get_key("CENSUS_API_KEY")
        for attempt in range(6):
            try:
                r = requests.get("https://api.census.gov/data/" + path, params=p, headers=UA, timeout=300)
                if r.status_code == 204:
                    rows = []
                    break
                r.raise_for_status()
                rows = r.json()
                break
            except Exception as e:  # retry
                if attempt == 5:
                    raise RuntimeError(f"census call failed: {path} {params}: {e}")
                time.sleep(3 * (attempt + 1))
        with open(fp, "w") as f:
            json.dump(rows, f)
        with open(fp + ".key", "w") as f:
            f.write(key)
    if not rows:
        return []
    hdr = rows[0]
    return [dict(zip(hdr, r)) for r in rows[1:]]


def download(url, name):
    fp = os.path.join(RAW, name)
    if not os.path.exists(fp):
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        r = requests.get(url, headers=UA, timeout=300)
        r.raise_for_status()
        with open(fp, "wb") as f:
            f.write(r.content)
    return fp


def wmedian(x, w):
    x = np.asarray(x, float)
    w = np.asarray(w, float)
    o = np.argsort(x, kind="mergesort")
    x, w = x[o], w[o]
    c = np.cumsum(w)
    return float(x[np.searchsorted(c, c[-1] / 2.0)])


CPI = None


def cpi():
    """Annual CPI-U (CUUR0000SA0, M13) 2005-2024 from the BLS API, cached."""
    global CPI
    if CPI is not None:
        return CPI
    fp = os.path.join(RAW, "bls", "cpi.json")
    if not os.path.exists(fp):
        os.makedirs(os.path.dirname(fp), exist_ok=True)
        body = {"seriesid": ["CUUR0000SA0"], "startyear": "2005", "endyear": "2024",
                "annualaverage": True, "registrationkey": get_key("BLS_API_KEY")}
        r = requests.post("https://api.bls.gov/publicAPI/v2/timeseries/data/", json=body, headers=UA, timeout=120)
        r.raise_for_status()
        with open(fp, "w") as f:
            f.write(r.text)
    d = json.load(open(fp))
    out = {}
    for it in d["Results"]["series"][0]["data"]:
        if it["period"] == "M13":
            out[int(it["year"])] = float(it["value"])
    CPI = out
    return out
