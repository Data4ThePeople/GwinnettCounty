"""How Gwinnett County was chosen: re-run of the October 21, 2026 selection done in the
AffordableHousing session.

Reads the processed files of the Rentals Within Reach tool (AffordableHousing project) and its
tie-out functions, so the shares match the published tool exactly. Settings are the tool's
defaults: median renter household, after taxes (married, no children), rent at 30% of income.

Rules:
- at least 1,000 cash-rent units in 2020-2024
- not low reliability in 2020-2024 under the tool's rules (under 200 cash-rent units, rent count
  coefficient of variation over 30%, or a renter median income margin over 25% of the estimate)
- top 10 least affordable in 2020-2024, with and without the tool's 71 college counties
- among those, the largest change from 2005-2009 to 2020-2024

Output: research/candidate-selection-output.txt"""
import importlib.util
import io
import json
import sys
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AH = Path.home() / "PycharmProjects" / "AffordableHousing"
sys.path.insert(0, str(AH / "scripts"))
from common import COLLEGE_SHARE, PROC, RENT_EDGES  # noqa: E402

spec = importlib.util.spec_from_file_location("tieout", AH / "scripts" / "10_tieout.py")
T0 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(T0)

FK = ["2009", "2014", "2019", "2024"]
LABEL = {"2009": "2005-09", "2014": "2010-14", "2019": "2015-19", "2024": "2020-24"}
ATLANTA = {"13121": "Fulton", "13089": "DeKalb", "13067": "Cobb", "13135": "Gwinnett", "13063": "Clayton", "13151": "Henry",
           "13247": "Rockdale", "13097": "Douglas", "13113": "Fayette", "13117": "Forsyth", "13057": "Cherokee"}
DETAIL = ["13135", "35027", "48259", "13063", "13089", "12011", "01047", "28143"]


def build():
    """The tool's shares for every county and period, the low-reliability flags, and the 2020-2024 ranking
    (least affordable first). Also used by 09_charts.py."""
    H = json.loads((PROC / "harmonized.json").read_text())
    tax = json.loads((PROC / "tax_grid.json").read_text())
    M = json.loads((PROC / "map_data.json").read_text())
    weak = {u["id"]: [bool(f.get("lo")) or bool(f.get("pm", 0) & 32) or "x" in f for f in u["f"]] for u in M["units"]}

    def share(uid, fk, inc=None):
        info = H["units"][uid]
        x = info["f"][fk]
        if "na" in x or sum(x["r"]) == 0:
            return None
        inc = T0.income(x, fk, 5) if inc is None else inc
        net = inc - T0.tax(tax, fk, 1, info["st"], inc)
        return 100 * T0.share(x["r"], RENT_EDGES[fk], 0.30 * net / 12)

    S = {uid: {fk: share(uid, fk) for fk in FK} for uid in H["units"]}
    ranked = sorted((S[u]["2024"], u) for u, info in H["units"].items()
                    if S[u]["2024"] is not None and sum(info["f"]["2024"]["r"]) >= 1000 and not weak[u][3])
    return H, S, weak, ranked, share


def main():
    H, S, weak, ranked, share = build()
    cpi = json.loads((PROC / "cpi.json").read_text())
    infl = cpi["2024"] / cpi["2009"]
    rank = {u: i + 1 for i, (_, u) in enumerate(ranked)}
    print(f"CPI-U, 2009 to 2024: +{100 * (infl - 1):.0f}%")
    print(f"Ranked counties (1,000+ cash-rent units, reliable in 2020-2024): {len(ranked)}")

    for excl in (False, True):
        print(f"\nTop 10 least affordable, 2020-2024, college counties {'left out' if excl else 'included (page default)'}")
        print("  * = the tool marks that period low reliability")
        top = [u for _, u in ranked if not (excl and H["units"][u]["college"] >= COLLEGE_SHARE)][:10]
        for u in top:
            s, col = S[u], H["units"][u]["college"] >= COLLEGE_SHARE
            cells = " ".join(f"{s[k]:5.1f}{'*' if weak[u][i] else ' '}" for i, k in enumerate(FK))
            print(f"  {H['units'][u]['name']:26s} {'college' if col else '       '} {cells} {s['2024'] - s['2009']:+6.1f} pts {100 * (s['2024'] / s['2009'] - 1):+5.0f}%")
        best = min(top, key=lambda u: S[u]["2024"] / S[u]["2009"])
        print(f"  Largest decline: {H['units'][best]['name']}")

    print("\nCandidate detail (renter median income and median gross rent, each period in its own final-year dollars)")
    for u in DETAIL:
        f, s = H["units"][u]["f"], S[u]
        moe = " ".join(f"{100 * f[k]['pm'][1] / f[k]['ri']:3.0f}%" if f[k]["ri"] and f[k]["pm"][1] else "  na" for k in FK)
        ri0, ri1 = T0.income(f["2009"], "2009", 5), T0.income(f["2024"], "2024", 5)
        hh = [sum(f[k]["r"]) + f[k]["nc"] for k in FK]
        held = share(u, "2009", ri1 * cpi["2009"] / cpi["2024"])
        print(f"\n  {H['units'][u]['name']} (rank {rank.get(u, '-')} of {len(ranked)})")
        print("    share:   " + "  ".join(f"{LABEL[k]} {s[k]:.1f}" for k in FK))
        print(f"    renter median margin as % of estimate: {moe}")
        print(f"    renter households: {', '.join(f'{n:,}' for n in hh)}")
        print(f"    renter median ${ri0:,.0f} to ${ri1:,.0f} ({100 * (ri1 / (ri0 * infl) - 1):+.0f}% after inflation)")
        print(f"    median gross rent ${f['2009']['mr']:,.0f} to ${f['2024']['mr']:,.0f} "
              f"({100 * (f['2024']['mr'] / f['2009']['mr'] - 1):+.0f}%; {100 * (f['2024']['mr'] / f['2009']['mr'] / infl - 1):+.0f}% after inflation)")
        print(f"    2020-24 renter income held fixed after inflation: {held:.1f}% in 2005-09, {s['2024']:.1f}% in 2020-24")

    print("\nCore Atlanta metro counties")
    for u, n in ATLANTA.items():
        s = S[u]
        f = H["units"][u]["f"]["2024"]
        print(f"  {n:9s} " + " ".join(f"{s[k]:5.1f}" for k in FK)
              + f"  {100 * (s['2024'] / s['2009'] - 1):+5.0f}%  rank {rank.get(u, '-'):>4}  renter households {sum(f['r']) + f['nc']:,}")


if __name__ == "__main__":
    buf = io.StringIO()
    with redirect_stdout(buf):
        main()
    (ROOT / "research").mkdir(exist_ok=True)
    (ROOT / "research" / "candidate-selection-output.txt").write_text(buf.getvalue())
    print(buf.getvalue())
