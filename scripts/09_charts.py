"""Draft charts, dark house palette. Every number is recomputed at render time from the tool's processed files, the
cached ACS tables, permits and PUMS, through the same functions as scripts 05 and 07; nothing is typed in.
Output: charts/01-*.png onward."""
import importlib.util
import json
import shutil
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
G8 = import_module("08_owner_renter_gap")
C1 = import_module("01_candidate_selection")
P12 = import_module("12_renter_income")

CHARTS = ROOT / "charts"
SLUG = "gwinnett-county-rents"
# draft chart -> its name in the post, in order of appearance
POST_ORDER = {"10-least-affordable.png": "01-least-affordable.png", "12-rentals-stacked.png": "02-rentals-within-reach.png",
              "09-income-vs-rent.png": "03-income-vs-rent.png", "13-growth-by-age.png": "04-growth-by-age.png",
              "07-permits-per-household.png": "05-permits-per-household.png", "11-renter-pay.png": "06-renter-pay.png"}
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


# ---------------------------------------------------------------- 09 rent change against renter income change, metro
# label offsets in points, placement only
NUDGE = {"Newton": (-7, -9), "Coweta": (6, 4), "Fulton": (7, -5), "Forsyth": (-8, 4), "Cobb": (7, -9), "DeKalb": (7, -9)}


def income_vs_rent():
    big = [o for o in G8.metro_changes() if o[4] >= 10000]
    fig, ax = frame(top=0.76, bottom=0.12, left=0.09, right=0.95, h=7)
    lo, hi = -10, 45
    ax.plot([lo, hi], [lo, hi], color=MUTED, lw=1, ls=(0, (4, 4)))
    ax.text(38.5, 33, "Rent and income\nrose at the same rate", color=INK_DIM, fontsize=9.5, ha="left", va="top", rotation=0)
    for ch, m, r1, mr, n, name, f in big:
        me = f == "13135"
        ax.scatter(ch, mr, s=90 if me else 55, color=BLUE if me else MUTED, zorder=3, edgecolors="#181A1B", linewidths=1.5)
        dx, dy = NUDGE.get(name, (7, 3))
        ax.annotate(f"{name}\nincome {ch:+.0f}%, rent {mr:+.0f}%" if me else name, (ch, mr), xytext=(dx, dy), textcoords="offset points",
                    ha="right" if dx < 0 else "left", va="center" if not me else "bottom", color=BLUE if me else INK,
                    fontsize=11 if me else 9.5, fontweight="bold" if me else "normal")
    ax.axhline(0, color=GRID, lw=1)
    ax.axvline(0, color=GRID, lw=1)
    ax.set_xlim(lo, hi)
    ax.set_ylim(0, hi)
    ax.set_yticks(range(10, hi + 1, 10))
    fmt = matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:+.0f}%")
    ax.xaxis.set_major_formatter(fmt)
    ax.yaxis.set_major_formatter(fmt)
    ax.set_xlabel("Change in median renter household income", color=INK_DIM, fontsize=10)
    ax.set_ylabel("Change in median gross rent", color=INK_DIM, fontsize=10)
    ax.grid(True)
    g = next(o for o in big if o[6] == "13135")
    rank = sorted(big, key=lambda o: o[3] - o[0], reverse=True).index(g) + 1
    assert rank == 1
    titleblock(fig, "Rent outran renter income in Gwinnett by one of the metro's widest gaps",
               f"Change from 2005-09 to 2020-24 after inflation, the {len(big)} Atlanta-metro counties with at least 10,000 renter households.\n"
               f"Points above the dashed line saw rent rise faster than renter income. Gwinnett sits farthest above it,\n"
               f"but its income change has a margin of about {g[1]:.0f} points either way, so its lead over the next counties is uncertain.")
    credit(fig, ACS + " (B25119), median gross rent via the Rentals Within Reach tool's files; BLS CPI-U.\n"
           "Counties in the Atlanta metro as defined by OMB in July 2023.")
    save(fig, "09-income-vs-rent.png")


# ---------------------------------------------------------------- 10 least affordable counties, 2020-24
def ranking():
    H, S, weak, ranked, _ = C1.build()
    top = [(v, u) for v, u in ranked if H["units"][u]["college"] < C1.COLLEGE_SHARE][:10]
    assert top[0][1] == G
    n_all = len(ranked)
    n_nc = sum(1 for _, u in ranked if H["units"][u]["college"] < C1.COLLEGE_SHARE)
    rank_all = [u for _, u in ranked].index(G) + 1
    names = [H["units"][u]["name"].replace(" County", "") for _, u in top]
    fig, ax = frame(left=0.2, top=0.74)
    hbars(ax, names, [v for v, _ in top], [BLUE if u == G else MUTED for _, u in top], lambda v: f"{v:.1f}%", 0.25)
    ax.set_xlim(0, max(v for v, _ in top) * 1.15)
    titleblock(fig, f"Gwinnett had the lowest share within reach of {n_nc:,} non-college counties",
               f"Share of rentals within reach, 2020-24: the 10 lowest of {n_nc:,} counties with 1,000+ rentals, leaving out college counties.\n"
               f"With college counties included, Gwinnett ranks {rank_all} of {n_all:,}.\n" + REACH.replace(",\nthe", ", the"))
    n_col = sum(1 for info in H["units"].values() if info["college"] >= C1.COLLEGE_SHARE)
    credit(fig, TOOL + f"\nCounties the tool marks low reliability in 2020-24 are left out. \nCollege counties: the tool's {n_col} counties"
           " where 15% or more of residents age 3 and over are enrolled in college.")
    save(fig, "10-least-affordable.png")


# ---------------------------------------------------------------- 11 renter workers' pay, peers
def renter_pay():
    cpi = json.loads((PROC / "cpi.json").read_text())
    res = {name: P12.ftyr_change(c, cpi) for c, name in P12.NAMES.items()}
    order = sorted(res, key=lambda n: res[n][2], reverse=True)
    fig, ax = frame(left=0.13, top=0.74)
    vals = [res[n][2] for n in order]
    hbars(ax, order, vals, [BLUE if n == "Gwinnett" else MUTED for n in order], lambda v: f"{v:+.1f}%", 0.4)
    ax.set_xlim(min(vals) - 5, max(vals) + 5)
    g = res["Gwinnett"]
    titleblock(fig, f"Full-time renter pay in Gwinnett did not rise after inflation; in Cobb it rose {res['Cobb'][2]:.0f}%",
               "Change in median earnings of renters who worked full time all year, 2005-09 to 2020-24, in 2024 dollars.\n"
               f"Gwinnett: ${round(g[0], -2):,.0f} to ${round(g[1], -2):,.0f}, within about {g[3] * 1.645:.0f} points either way.")
    credit(fig, "Source: U.S. Census Bureau, American Community Survey 5-year microdata (PUMS); BLS CPI-U. Full time: 35+ hours a week, 50+ weeks"
           " a year.\nForsyth is left out because its 2005-09 microdata area also covers Dawson and Pickens counties.")
    save(fig, "11-renter-pay.png")


# ---------------------------------------------------------------- 12 stacked bars: rentals within reach and the rest, by period
def stacked():
    f = H_["units"][G]["f"]
    n = {fk: sum(f[fk]["r"]) for fk in FK}
    sh = {fk: tool_share(f[fk], fk) for fk in FK}
    w = {fk: n[fk] * sh[fk] / 100 for fk in FK}
    fig, ax = frame(top=0.76)
    xs = list(range(len(FK)))
    ax.bar(xs, [w[k] for k in FK], color=BLUE, width=0.62, edgecolor="#181A1B", linewidth=2)
    ax.bar(xs, [n[k] - w[k] for k in FK], bottom=[w[k] for k in FK], color=MUTED, width=0.62, edgecolor="#181A1B", linewidth=2)
    for x, k in zip(xs, FK):
        ax.text(x, w[k] / 2, f"{round(w[k], -2):,.0f}\n{sh[k]:.1f}%", ha="center", va="center", color=INK, fontsize=10)
        ax.text(x, n[k] + 1500, f"{round(n[k], -2):,.0f}", ha="center", va="bottom", color=INK, fontsize=10.5, fontweight="bold")
    ax.set_xticks(xs, [LABEL[k] for k in FK])
    ax.set_ylim(0, max(n.values()) * 1.12)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    ax.grid(axis="y")
    titleblock(fig, f"Gwinnett's rentals grew {pct(n['2009'], n['2024']):.0f}%, but the number within reach fell {-pct(w['2009'], w['2024']):.0f}%",
               "Rentals with a cash rent in Gwinnett County: within reach of the median renter household (blue, with the share)\n"
               "and out of reach (gray). Bar totals on top. Rounded to the nearest 100.\n" + REACH.replace(",\nthe", ", the"))
    credit(fig, TOOL + "\nWithin-reach counts are the tool's share times its count of rentals.")
    save(fig, "12-rentals-stacked.png")


# ---------------------------------------------------------------- 13 where the rentals came from, and where the ones within reach went
GROUP_ROWS = [("houses", "before 2000"), ("houses", "2000-09"), ("houses", "2010 or later"),
              ("apartments", "before 2000"), ("apartments", "2000-09"), ("apartments", "2010 or later"), ("other", "all")]


def by_age_type():
    """Cash-rent renter households and those within reach, 2005-09 and 2020-24, by building type and year built (PUMS).
    Buildings built 2000-09 are the 'newer (2000+)' group in 2005-09 and the '2000s' group in 2020-24."""
    era = {"older (pre-2000)": "before 2000", "newer (2000+)": "2000-09", "2000s": "2000-09", "newer (2010+)": "2010 or later"}
    out = {g: {v: [0, 0] for v in ("2009", "2024")} for g in GROUP_ROWS}
    for v in ("2009", "2024"):
        c = ceiling(v)
        for x in N7.records(v, "135"):
            t = {"single-family": "houses", "5+ unit apartments": "apartments"}.get(x["type"], "other")
            g = (t, "all") if t == "other" else (t, era[x["era"]])
            out[g][v][0] += x["w"]
            out[g][v][1] += x["w"] * (x["rent"] <= c)
    return out


def growth_by_age():
    d = by_age_type()
    labels = {"houses": "Houses", "apartments": "Apartments"}
    names = [f"{labels[t]}, built {e}" if t != "other" else "Other (2-4 unit buildings, mobile homes)" for t, e in GROUP_ROWS]
    all_ch = [d[g]["2024"][0] - d[g]["2009"][0] for g in GROUP_ROWS]
    in_ch = [d[g]["2024"][1] - d[g]["2009"][1] for g in GROUP_ROWS]
    tot = sum(all_ch)
    f = H_["units"][G]["f"]
    tool_add = sum(f["2024"]["r"]) - sum(f["2009"]["r"])
    tool_drop = sum(f["2024"]["r"]) * tool_share(f["2024"], "2024") / 100 - sum(f["2009"]["r"]) * tool_share(f["2009"], "2009") / 100
    houses = sum(c for g, c in zip(GROUP_ROWS, all_ch) if g[0] == "houses")
    fig = plt.figure(figsize=(W, H))
    cols = [BLUE if g[1] == "before 2000" else MUTED for g in GROUP_ROWS]
    hi = max(all_ch + in_ch) * 1.3
    lims = [(min(all_ch + [0]) * 1.5 - 0.02 * hi, hi), (min(in_ch + [0]) * 1.5 - 0.02 * hi, max(in_ch) + 0.25 * hi)]
    per = 0.6 / sum(b - a for a, b in lims)                 # same width per household in both panels
    x0 = 0.34
    for i, (vals, head) in enumerate(((all_ch, "Change in all rentals"), (in_ch, "Change in rentals within reach"))):
        lo, top = lims[i]
        ax = fig.add_axes([x0, 0.14, per * (top - lo), 0.56])
        x0 += per * (top - lo) + 0.03
        ax.tick_params(length=0)
        hbars(ax, names if i == 0 else [""] * len(names), vals, cols, lambda v: f"{round(v, -2):+,.0f}", 400 if i == 0 else 250)
        if i:
            ax.set_yticks([])
        ax.set_xlim(lo, top)
        ax.set_title(head, color=INK, fontsize=11.5, loc="left", pad=10)
    titleblock(fig, "Houses added most new rentals; older apartments lost the most within reach",
               f"Change in renter households with a cash rent, 2005-09 to 2020-24, by building type and year built, rounded to the nearest 100.\n"
               f"All rentals grew by about {round(tot, -2):,.0f}; houses account for {100 * houses / tot:.0f}% of that. "
               f"Rentals within reach fell by about {round(-sum(in_ch), -2):,.0f}.\n" + REACH.replace(",\nthe", ", the"))
    credit(fig, PUMS + f"\nThe tool's counts: about {round(tool_add, -2):,.0f} more rentals and {round(-tool_drop, -2):,.0f} fewer within reach"
           " (from rent ranges, not exact rents).")
    save(fig, "13-growth-by-age.png")


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
    income_vs_rent()
    ranking()
    renter_pay()
    stacked()
    growth_by_age()
    out = ROOT / "posts" / SLUG / "images"
    out.mkdir(parents=True, exist_ok=True)
    for src, dst in POST_ORDER.items():
        shutil.copyfile(CHARTS / src, out / dst)
    print(f"copied {len(POST_ORDER)} charts to posts/{SLUG}/images/")
