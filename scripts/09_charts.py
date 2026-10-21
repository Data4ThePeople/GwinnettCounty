"""Draft charts, dark house palette. Every number is recomputed at render time from the tool's processed files, the
cached ACS tables, permits and PUMS, through the same functions as scripts 05 and 07; nothing is typed in.
Output: charts/01-*.png onward."""
import importlib.util
import json
import sys
from importlib import import_module
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))
AH = Path.home() / "PycharmProjects" / "AffordableHousing"
sys.path.insert(0, str(AH / "scripts"))
from common import PROC, RENT_EDGES  # noqa: E402
from plot_style import BLUE, GRID, INK, INK_DIM, MUTED, YELLOW, credit, titleblock, use_house_style  # noqa: E402

spec = importlib.util.spec_from_file_location("tieout", AH / "scripts" / "10_tieout.py")
T0 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(T0)
W5 = import_module("05_why_rents")
N7 = import_module("07_new_rentals")

CHARTS = ROOT / "charts"
FK = ["2009", "2014", "2019", "2024"]
LABEL = {"2009": "2005-09", "2014": "2010-14", "2019": "2015-19", "2024": "2020-24"}
G = "13135"
W, H = 10, 6.2
ACS = "Source: U.S. Census Bureau, American Community Survey 5-year estimates"
TOOL = "Source: Data 4 The People, Rentals Within Reach, from Census Bureau American Community Survey 5-year estimates."
REACH = ("Within reach: gross rent at or below 30% of the county's median renter income after taxes,\n"
         "the Rentals Within Reach tool's default.")

H_ = json.loads((PROC / "harmonized.json").read_text())
TAX = json.loads((PROC / "tax_grid.json").read_text())
CPI = json.loads((PROC / "cpi.json").read_text())


def frame(top=0.78, bottom=0.14, left=0.08, right=0.95, h=H):
    fig = plt.figure(figsize=(W, h))
    ax = fig.add_axes([left, bottom, right - left, top - bottom])
    ax.set_axisbelow(True)
    ax.tick_params(length=0)
    return fig, ax


def save(fig, name):
    CHARTS.mkdir(exist_ok=True)
    fig.savefig(CHARTS / name)
    plt.close(fig)
    print("wrote charts/" + name)


def pct(a, b):
    return 100 * (b / a - 1)


def tool_share(x, fk, st="13"):
    inc = T0.income(x, fk, 5)
    return 100 * T0.share(x["r"], RENT_EDGES[fk], 0.30 * (inc - T0.tax(TAX, fk, 1, st, inc)) / 12)


def hbars(ax, labels, vals, colors, fmt, pad):
    y = list(range(len(labels)))[::-1]
    ax.barh(y, vals, color=colors, height=0.62)
    ax.set_yticks(y, labels, color=INK, fontsize=11)
    for yy, v in zip(y, vals):
        ax.text(v + (pad if v >= 0 else -pad), yy, fmt(v), va="center", ha="left" if v >= 0 else "right", color=INK, fontsize=10)
    ax.set_xticks([])
    for s in ("left", "bottom"):
        ax.spines[s].set_visible(False)
    ax.axvline(0, color=GRID, lw=1)


# ---------------------------------------------------------------- 01 share within reach, Gwinnett and the nation
def share_line():
    g = {fk: tool_share(H_["units"][G]["f"][fk], fk) for fk in FK}
    us = {fk: T0.nation(H_, TAX, CPI, fk, int(fk))[0] for fk in FK}
    fig, ax = frame()
    xs = range(len(FK))
    for s, c, name, dy in ((g, BLUE, "Gwinnett County", -16), (us, MUTED, "United States", 10)):
        ax.plot(xs, list(s.values()), color=c, lw=2.4, marker="o", ms=6)
        for x, v in zip(xs, s.values()):
            ax.annotate(f"{v:.1f}%", (x, v), xytext=(0, dy), textcoords="offset points", ha="center", color=INK, fontsize=10)
        ax.text(3.12, s["2024"], name, color=c if c != MUTED else INK_DIM, fontsize=11.5, fontweight="bold", va="center")
    ax.set_xticks(list(xs), [LABEL[k] for k in FK])
    ax.set_xlim(-0.3, 3.9)
    ax.set_ylim(0, 40)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:.0f}%"))
    ax.grid(axis="y")
    titleblock(fig, f"The share of Gwinnett's rentals within reach fell from {g['2009']:.1f}% to {g['2024']:.1f}%",
               "Share of rentals with a cash rent that the median renter household could afford, by survey period.\n" + REACH)
    credit(fig, TOOL)
    save(fig, "01-share-within-reach.png")


# ---------------------------------------------------------------- 02 rentals and rentals within reach, counts
def counts():
    f = H_["units"][G]["f"]
    n = {fk: sum(f[fk]["r"]) for fk in ("2009", "2024")}
    w = {fk: n[fk] * tool_share(f[fk], fk) / 100 for fk in n}
    fig, ax = frame(left=0.2, top=0.74)
    labels = ["All rentals, 2005-09", "All rentals, 2020-24", "Within reach, 2005-09", "Within reach, 2020-24"]
    vals = [n["2009"], n["2024"], w["2009"], w["2024"]]
    hbars(ax, labels, vals, [MUTED, BLUE, MUTED, BLUE], lambda v: f"{v:,.0f}", 1200)
    ax.set_xlim(0, max(vals) * 1.15)
    titleblock(fig, f"Gwinnett's rentals grew {pct(n['2009'], n['2024']):.0f}%, but the number within reach fell {-pct(w['2009'], w['2024']):.0f}%",
               "Rentals with a cash rent, and the number of them within reach of the median renter household.\n" + REACH)
    credit(fig, TOOL + "\nWithin-reach counts are the tool's share times its count of rentals, rounded.")
    save(fig, "02-rentals-and-within-reach.png")


# ---------------------------------------------------------------- 03 rent and renter income after inflation
def rent_vs_income():
    f = H_["units"][G]["f"]
    rent = {fk: f[fk]["mr"] * CPI["2024"] / CPI[fk] for fk in FK}
    inc = {fk: T0.income(f[fk], fk, 5) * CPI["2024"] / CPI[fk] for fk in FK}
    fig, ax = frame()
    xs = range(len(FK))
    for s, c, name in ((rent, YELLOW, "Median gross rent"), (inc, BLUE, "Median renter income")):
        ch = [pct(s["2009"], s[fk]) for fk in FK]
        ax.plot(xs, ch, color=c, lw=2.4, marker="o", ms=6)
        for x, v in zip(xs, ch):
            if x:
                ax.annotate(f"{v:+.0f}%", (x, v), xytext=(0, 9 if v >= 0 else -17), textcoords="offset points", ha="center", color=INK, fontsize=10)
        ax.text(3.12, ch[-1], name, color=c, fontsize=11.5, fontweight="bold", va="center")
    ax.axhline(0, color=INK_DIM, lw=1)
    ax.set_xticks(list(xs), [LABEL[k] for k in FK])
    ax.set_xlim(-0.3, 4.1)
    ax.set_ylim(-20, 40)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:+.0f}%"))
    ax.grid(axis="y")
    titleblock(fig, f"Gwinnett's rents rose {pct(rent['2009'], rent['2024']):.0f}% after inflation; renter income rose {pct(inc['2009'], inc['2024']):.0f}%",
               "Change since 2005-09, in 2024 dollars (CPI-U). Median gross rent includes utilities.\n"
               f"2020-24: rent ${f['2024']['mr']:,.0f} a month, renter household income ${T0.income(f['2024'], '2024', 5):,.0f} a year.")
    credit(fig, ACS + ", via the Rentals Within Reach tool's files; BLS CPI-U.")
    save(fig, "03-rent-and-income.png")


# ---------------------------------------------------------------- 04 and 05 rentals by year built (PUMS)
GROUPS = [("Built before 2000, apartments", "older (pre-2000)", "5+ unit apartments"),
          ("Built before 2000, houses", "older (pre-2000)", "single-family"),
          ("Built 2000-09, apartments", "2000s", "5+ unit apartments"),
          ("Built 2000-09, houses", "2000s", "single-family"),
          ("Built 2010 or later, apartments", "newer (2010+)", "5+ unit apartments"),
          ("Built 2010 or later, houses", "newer (2010+)", "single-family")]
PUMS = ("Source: U.S. Census Bureau, American Community Survey 5-year microdata (PUMS). Year built is reported by the household.\n"
        "Apartments are buildings with 5 or more units; houses are single-family, detached or attached.")


def ceiling(fk):
    x = H_["units"][G]["f"][fk]
    inc = T0.income(x, fk, 5)
    return 0.30 * (inc - T0.tax(TAX, fk, 1, "13", inc)) / 12


def older_apartments():
    out = {}
    for fk in ("2009", "2024"):
        rows = [x for x in N7.records(fk, "135") if x["era"] == "older (pre-2000)" and x["type"] == "5+ unit apartments"]
        n = N7.count(rows)
        out[fk] = (n, n * N7.within(rows, ceiling(fk)) / 100)
    fig, ax = frame(left=0.25, top=0.74)
    labels = ["All, 2005-09", "All, 2020-24", "Within reach, 2005-09", "Within reach, 2020-24"]
    vals = [out["2009"][0], out["2024"][0], out["2009"][1], out["2024"][1]]
    hbars(ax, labels, vals, [MUTED, BLUE, MUTED, BLUE], lambda v: f"{round(v, -2):,.0f}", 500)
    ax.set_xlim(0, max(vals) * 1.15)
    titleblock(fig, f"Gwinnett's older apartments: about the same number, {-pct(out['2009'][1], out['2024'][1]):.0f}% fewer within reach",
               "Renter households with a cash rent in apartment buildings built before 2000, rounded to the nearest 100.\n" + REACH)
    credit(fig, PUMS)
    save(fig, "04-older-apartments.png")


def rent_by_group():
    rows = N7.records("2024", "135")
    med = N7.wmedian(rows)
    vals, labels = [med], ["All rentals"]
    for lab, era, typ in GROUPS:
        vals.append(N7.wmedian([x for x in rows if x["era"] == era and x["type"] == typ]))
        labels.append(lab)
    fig, ax = frame(left=0.29, top=0.74)
    cols = [YELLOW] + [BLUE if "2010" in lab and "apartments" in lab else MUTED for lab in labels[1:]]
    hbars(ax, labels, vals, cols, lambda v: f"${round(v, -1):,.0f}", 40)
    ax.set_xlim(0, max(vals) * 1.18)
    new = vals[5]
    titleblock(fig, f"Newer apartments in Gwinnett rent for {pct(med, new):.0f}% more than the county median",
               "Median gross rent a month, renter households with a cash rent, 2020-24, by when the building was built.\n"
               "Rounded to the nearest $10.")
    credit(fig, PUMS)
    save(fig, "05-rent-by-year-built.png")


# ---------------------------------------------------------------- 06 permits by year
def permits_by_year():
    P = W5.permits()
    ys = list(range(2000, 2026))
    v = [sum(P[("135", y)]["est"]) for y in ys]
    fig, ax = frame()
    ax.bar(ys, v, color=BLUE, width=0.72)
    for y, n in zip(ys, v):
        if y in (2000, 2005, 2009, 2025) or n == max(v[10:]):
            ax.text(y, n + 150, f"{n:,}", ha="center", va="bottom", color=INK, fontsize=9)
    ax.set_xticks([2000, 2005, 2010, 2015, 2020, 2025])
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
    ax.grid(axis="y")
    late = max(v[ys.index(2010):])
    titleblock(fig, f"Gwinnett has not permitted more than {late:,} homes in a year since 2009",
               "New housing units authorized by building permits in Gwinnett County, all building types, by year.")
    credit(fig, "Source: U.S. Census Bureau, Building Permits Survey, county annual estimates (including imputed counts).")
    save(fig, "06-permits-by-year.png")


# ---------------------------------------------------------------- 07 permits per added household, peers
def permits_per_household():
    P = W5.permits()
    hh = W5.load("B11001", "2009"), W5.load("B11001", "2024")
    res = {}
    for c, name in W5.PEERS.items():
        units = sum(sum(P[(c, y)]["est"]) for y in range(2007, 2022))
        add = W5.num(hh[1][c], "B11001", 1) - W5.num(hh[0][c], "B11001", 1)
        res[name] = units / add
    order = sorted(res, key=res.get, reverse=True)
    fig, ax = frame(left=0.15, top=0.74)
    hbars(ax, order, [res[n] for n in order], [BLUE if n == "Gwinnett" else MUTED for n in order], lambda v: f"{v:.2f}", 0.02)
    ax.set_xlim(0, max(res.values()) * 1.12)
    titleblock(fig, f"Gwinnett permitted {res['Gwinnett']:.2f} homes for each household it added",
               "Housing units permitted 2007-2021, divided by the change in households from 2005-09 to 2020-24.\n"
               "Eight Atlanta-area counties.")
    credit(fig, "Source: U.S. Census Bureau, Building Permits Survey and American Community Survey 5-year estimates (table B11001).")
    save(fig, "07-permits-per-household.png")


# ---------------------------------------------------------------- 08 single-family share of rentals, change
def single_family_shift():
    res = {}
    for c, name in W5.PEERS.items():
        s = []
        for fk in ("2009", "2024"):
            t = W5.load("B25032", fk)[c]
            s.append(100 * (W5.num(t, "B25032", 14) + W5.num(t, "B25032", 15)) / W5.num(t, "B25032", 13))
        res[name] = s
    order = sorted(res, key=lambda n: res[n][1] - res[n][0], reverse=True)
    fig, ax = frame(left=0.13, top=0.74)
    hbars(ax, order, [res[n][1] - res[n][0] for n in order], [BLUE if n == "Gwinnett" else MUTED for n in order],
          lambda v: f"{v:+.1f} pts", 0.2)
    ch = [res[n][1] - res[n][0] for n in order]
    ax.set_xlim(min(ch) - 3.5, max(ch) + 2.5)
    g = res["Gwinnett"]
    titleblock(fig, f"Houses went from {g[0]:.1f}% to {g[1]:.1f}% of Gwinnett's rentals",
               "Change in single-family homes (detached or attached) as a share of renter-occupied homes,\n"
               "2005-09 to 2020-24, in percentage points. Eight Atlanta-area counties.")
    credit(fig, ACS + " (table B25032).")
    save(fig, "08-single-family-rentals.png")


if __name__ == "__main__":
    use_house_style()
    share_line()
    counts()
    rent_vs_income()
    older_apartments()
    rent_by_group()
    permits_by_year()
    permits_per_household()
    single_family_shift()
