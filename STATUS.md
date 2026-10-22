# Status

Project: GwinnettCounty
Process: ~/.claude/d4tp-process/PROCESS.md

## Current

Post: gwinnett-county-rents
Step: 2e
Since: 2026-10-22

## Steps

| Step | What | Confirmed | Notes |
|---|---|---|---|
| 1  | Exploration and analysis | 2026-10-21 | thread and charts in research/thread.md; both tie-outs pass |
| 2a | Draft with brackets resolved | 2026-10-21 | 7 charts; tie-outs: Claude 86/86, independent 1 and 2 match |
| 2b | Eric's edit, Claude's look-over | 2026-10-22 | pay section now full-time pay only; tie-out 93/93 |
| 2c | Slice markup | 2026-10-22 | defaults only; 33 slices, 7 images |
| 2d | Hero 1680x1080 + alt text | 2026-10-22 | Norcross College Street photo, Wikimedia Commons, CC0; alt 410 chars |
| 2e | SEO | | |
| 2f | Pushed to Prismic (draft) | | |
| 2g | Mailchimp teaser | | |

## Stale

None.

## Log

- 2026-10-21 Step 1 opened. Topic: a county spotlight in the style of the
  Dawson County post, on the least affordable rental county with the largest
  decline. Eric's rule: among the top 10 least affordable counties in
  2020-2024 with at least 1,000 rentals, the one with the largest change since
  2005-2009, using the Rentals Within Reach tool (AffordableHousing project).
- 2026-10-21 Selection carried over from a session run in the AffordableHousing
  project: research/candidate-selection.md (the rules, the candidates, why
  Lincoln County NM was set aside, why Gwinnett, the Atlanta pattern, open
  questions) and scripts/01_candidate_selection.py, which reproduces every
  number from the tool's processed data. By the rule as written Lincoln
  County NM has the largest decline (-72%), but its 2005-2009 starting point
  is marked low reliability and its decline comes from renter incomes, not
  rents. Eric chose Gwinnett County GA: rank 3 of 1,987 (rank 1 with college
  counties left out), 25.5% to 10.5% (-59%), renter median margin 3% in every
  period, rent up 32% after inflation against renter income up 8%. Nothing in
  AffordableHousing was changed.
- 2026-10-21 Eric is moving this work to a new PyCharm window. Next: plan mode
  for the exploration, then DATASETS.md before any new data or chart.
- 2026-10-21 Plan approved: settle "Gwinnett story or suburb vs. inner city"
  first, with decision rules set before the tests. DATASETS.md written (tool
  shares, NCHS 2023 urban-rural codes, OMB 2023 delineation, ACS place
  tables). Test 1 (counties, tool measure): suburbs fell more in 34 of 49
  large metros. Test 2 (largest city vs. rest of metro, one metro income
  line): suburbs fell more in only 15 of 54, and Atlanta city fell more than
  its suburbs. By the rules: not a national or Atlanta suburb story; a
  Gwinnett story (-38% at the metro line vs. DeKalb -26%, Clayton +16%, city
  -24%). Memo: research/suburb-vs-city.md. Waiting on Eric's call on framing.
- 2026-10-21 Eric chose the Gwinnett frame. Gwinnett's median rent ($1,810)
  is third in the metro after Forsyth and Fayette; what stands out is rent
  against renter income. Tested five explanations against seven peers with
  rules set first (research/why-rents.md). Supported: supply (0.65 permitted
  units per added household, 12% in 5+ unit buildings) and single-family
  rentals (share of rentals 31.0% to 39.5%, the largest rise; ARC says the
  region's most corporate-owned homes). Not supported: bedroom mix, richer
  renter pool, turnover pricing. Investor sources gathered by an agent in
  research/investor-sources.md; GAO and ARC/AJC figures checked by hand.
  DATASETS.md sections 5-8 added. Waiting on Eric.
- 2026-10-21 Eric asked whether new high-priced apartments explain the loss.
  PUMS by year built (research/new-rentals.md, scripts/07_new_rentals.py):
  mostly no. Apartments built 2010+ are 10% of rentals, median $1,870 vs
  county $1,812. Pre-2000 rentals went from 27.5% to 13.5% within reach;
  pre-2000 apartments lost about 5,500 within reach, more than the county's
  net loss. Microdata number within reach -26% vs the tool's -33% (exact
  rents vs rent ranges). Waiting on Eric.
- 2026-10-21 Eric asked about the owner-renter income gap. Not wide
  (research/owner-renter-gap.md): renter median 54.8% of owner median vs
  53.0% nationally; 220th of 282 large counties from the widest; narrowed 5.3
  pts. Gwinnett owners' median fell 2% after inflation while most neighbors'
  rose. Waiting on Eric.
- 2026-10-21 Eric asked for draft charts. Eight drawn in charts/ by
  scripts/09_charts.py (house dark style, numbers recomputed at render):
  share within reach vs US, rentals vs within-reach counts, rent vs renter
  income after inflation, older apartments, rent by year built, permits by
  year, permits per added household, single-family share change. Waiting on
  Eric's pick of charts.
- 2026-10-21 Eric asked whether Gwinnett's renter income lagged. Yes:
  +8.3% after inflation vs metro +15.8%, 12th of 15 metro counties with
  10,000+ renters; rent +31.8%, and rent minus income is the largest of the
  15. Added to research/owner-renter-gap.md. Waiting on Eric.
- 2026-10-21 Eric asked for a scatter of renter income change vs rent change
  to show Gwinnett as an outlier. Drawn as charts/09-income-vs-rent.png (15
  metro counties with 10,000+ renters). Gwinnett is farthest above the
  equal-growth line (+23.6 pts vs Clayton +18.3, DeKalb +17.6, Cherokee
  +17.3), but within margins; against a fitted trend it is level with
  Forsyth and Cherokee. Told Eric "outlier" overstates it.
- 2026-10-21 Eric asked whether a stronger housing market explains it.
  Partly (research/values-vs-rents.md): price vs rent change r = 0.60 ACS,
  0.66 FHFA across 655 large counties; Gwinnett's prices 6th (ACS) / 3rd
  (FHFA) of 15 metro counties; its rent is 1.0-1.4 SD above the fit. Cobb and
  Cherokee had the same FHFA rise and similar rent rises, but renter income
  +17-18% vs Gwinnett +8%. Waiting on Eric.
- 2026-10-21 Eric asked why renter income lagged (research/renter-income.md).
  R1 mix of households: not a factor by the rule (mix shift raised income
  +9.5 pts, about the same as Cobb, less than Fulton/DeKalb/Cherokee/Henry).
  R2 workers per household: not a factor (rose like peers). R3 full-time
  year-round renter pay: -3.3% vs Cobb +6.7% (supported). R4 QCEW pay of jobs
  in county: +1.0%, lowest of eight (supported). Waiting on Eric.
- 2026-10-21 Eric proposed five beats. Edited against the findings in
  research/thread.md (rank caveats, the 59% decline, rent vs income, older
  rentals not new apartments, renter pay). Two new charts: 10 least
  affordable, 11 renter pay. Proposed set: 10, 01, 02, 09, 05, 04, 07, 11.
  Waiting on Eric to confirm the thread, then the tie-outs.
- 2026-10-21 Beat 5 framing added (household income +8% vs full-time pay
  -3%). Claude's tie-out (scripts/13_tieout.py, research/tieout-output.txt):
  55 of 55 number checks pass after three text fixes in thread.md (national
  share was 27.6% in 2010-14, not "near 31-32%"; 2+ worker households 37%,
  not 38%; Clayton "half a point behind"; beat 5 mix wording). Independent
  tie-out running.
- 2026-10-21 Independent tie-out done (research/independent-tieout.md, code in
  tieout/independent/). Every recomputed value and every chart number matches
  within rounding; 2009 YBL coding in DATASETS.md confirmed against B25036.
  Labels fixed per its findings: chart 09 title (certainty), chart 10 title
  and footer (college-county rule), chart 11 title and beat 5 ("fell 3%" is
  inside the margin, now "did not rise"); beat 5 notes the PUMS 7% vs table
  8%. Ready to ask Eric to close Step 1.
- 2026-10-21 Step 1 confirmed by Eric. Slug: gwinnett-county-rents. Step 2a opened:
  posts/gwinnett-county-rents/ created; waiting on Eric's draft.
- 2026-10-21 Eric asked Claude to write the beats with placeholders for his
  intro, closing and title, charts carrying the story with light text.
  POST.md drafted (8 charts, limits, method); charts copied to
  posts/gwinnett-county-rents/images/ by 09_charts.py. Fixed "Clayton, next
  door" in thread.md (Clayton does not border Gwinnett). Waiting on Eric.
- 2026-10-21 Eric swapped the share line and counts bar (post charts 02, 03)
  for one stacked bar of rentals within reach by period (draft chart 12).
  Post now has 7 charts, renumbered 01-07.
- 2026-10-21 Eric approved the growth-by-age chart (draft 13); it replaces
  rent by year built and older apartments. Post now has 6 charts. Tie-out
  extended (F1-F5): group changes add to the microdata total; 60 of 60 pass.
  Chart notes the tool's counts (+41,400 rentals, -5,500 within reach) vs
  microdata (+40,800, -4,200).
- 2026-10-21 Eric reworked beat 4 around older apartments (median rent +92%
  nominal, +31% after inflation vs +8% for what renters could afford). New
  charts 14 (new-to-market rents vs the $1,250 line) and 15 (older apartment
  rent vs affordable amount, two periods); permits chart dropped from the
  post. Beat 5 now opens with like-for-like income -3%. Post has 7 charts.
  Tie-out extended (G1-G12): 75 of 75 pass.
- 2026-10-21 Eric dropped the growth-by-age chart (draft 13) from the post as
  confusing; its numbers stay in the text. Post has 6 charts.
- 2026-10-21 Eric asked to compare Gwinnett's renter pay with large-metro
  counties where rent rose 25%+ after inflation (research/national-pay.md,
  DATASETS 13). 37 measurable counties; Gwinnett -3.3% is 2nd lowest, after
  Cherokee GA; only those two show a drop; middle county +14.5%. Chart 16
  replaces the Atlanta renter-pay chart as post image 06. Tie-out 81 of 81.
  New numbers since Step 1 have Claude's tie-out only.
- 2026-10-21 Eric asked whether to keep Cherokee (margin +/-10.8). Kept;
  90% margin lines added to every bar of chart 16, and the post text notes
  Cherokee's estimate is much less certain.
- 2026-10-21 Eric's intro placed verbatim; its map bracket resolved with chart
  17 (Atlanta metro map, Gwinnett outlined). Beat 1 trimmed to avoid overlap.
  Proposed edits to Eric's intro sent as a numbered list (not applied).
  Post has 7 charts. Tie-out 84 of 84. DATASETS 14 (county boundaries).
- 2026-10-21 Eric accepted intro edits 1-5 (northeast, top ten outside college
  towns, household definition, tool link, Tyson); applied.
- 2026-10-21 Independent tie-out 2 done (research/independent-tieout-2.md,
  code in tieout/independent2/): every number in the new sections and on post
  images 01, 02, 05-07 matches. Wording fixes applied to Claude's text and
  chart titles (cause words, "after-tax", "median renter", pay-drop margins,
  ranked-county limits). Three edits to Eric-derived wording sent as a list.
- 2026-10-21 Eric accepted edits 1-3 (college counties, rentals-added sentence,
  net rentals in older houses); applied. Asked for the median rent as a share
  of after-tax renter income: 43.3% in 2020-24, 35.6% in 2005-09 (not yet in post).
- 2026-10-21 Eric's closing placed verbatim under its own heading. 43% figure tied
  out (K1). Proposed edits to the closing sent as a numbered list (not applied).
- 2026-10-21 Eric accepted closing edits 1-10; applied.
- 2026-10-21 Title set: Good Luck Renting It in Gwinnett.
- 2026-10-21 Title changed: Renters Can't Win It in Gwinnett.
- 2026-10-21 Subtitle set (Claude's suggestion); both closing sections kept. No
  brackets left in POST.md. Waiting on Eric to confirm 2a.
- 2026-10-21 Step 2a confirmed by Eric. Next: 2b, Eric edits POST.md, then
  Claude's look-over.
- 2026-10-22 Step 2b: chart 15 (post image 06) redrawn as a slope chart with
  the gap shaded; alt text updated. Eric's edits reviewed as a numbered list;
  accepted edits applied (college names, Newton comparison, three kinds of
  added rentals as bullets, rentals within reach lost, closing tightened).
  Like-for-like income dropped from the post; the pay section now goes
  straight to full-time renter pay, with household changes (2+ workers 34% to
  37%, full-time share 66% to 76%, bachelor's 23% to 30%). New numbers tied
  out (C11-C14, F7, E15-E16): 93 of 93 pass.
- 2026-10-22 Step 2b confirmed by Eric. Next: 2c, slice markup.
- 2026-10-22 Step 2c confirmed by Eric. Importer convert-only: 33 slices, 7
  images, defaults only, no fences added. Next: 2d, hero.
- 2026-10-22 Step 2d confirmed by Eric. Hero: "College Street, Norcross March
  2017" by Thomson200, Wikimedia Commons, CC0 (no credit required), center
  crop to 1680x1080; source kept as images/gwinnett-county-rents-hero-source.jpg.
  No usable Lawrenceville GA sign or downtown photo found (Commons sign is
  Lawrenceville, Quebec; Flickr ones are small and no-derivatives). Next: 2e, SEO.
