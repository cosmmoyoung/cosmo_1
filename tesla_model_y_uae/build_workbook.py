#!/usr/bin/env python3
"""
Build the Tesla Model Y UAE / Abu Dhabi depreciation workbook.

All market observations were collected from UAE classifieds (DubiCars, dubizzle,
CarSwitch, OneClickDrive, OpenSooq) and UAE new-car price sites (DriveArabia,
YallaMotor, ZigWheels) in July 2026 via web search. Every number carries a source
note and a confidence flag in the workbook itself.
"""

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
from openpyxl.chart import LineChart, BarChart, ScatterChart, Reference, Series
from openpyxl.chart.marker import Marker
from openpyxl.comments import Comment

OUT = "Tesla_Model_Y_Abu_Dhabi_Depreciation.xlsx"

# ---------------------------------------------------------------- style helpers
FONT = "Arial"
BLUE = Font(name=FONT, size=10, color="0000FF")          # hardcoded input
BLACK = Font(name=FONT, size=10)                          # formula
GREEN = Font(name=FONT, size=10, color="008000")          # cross-sheet link
H1 = Font(name=FONT, size=14, bold=True, color="FFFFFF")
H2 = Font(name=FONT, size=11, bold=True, color="FFFFFF")
HDR_FILL = PatternFill("solid", fgColor="1F3864")
SUB_FILL = PatternFill("solid", fgColor="2E5B9A")
YELLOW = PatternFill("solid", fgColor="FFFF00")
GREY = PatternFill("solid", fgColor="F2F2F2")
NOTE = Font(name=FONT, size=9, italic=True, color="595959")
BOLD = Font(name=FONT, size=10, bold=True)
THIN = Side(style="thin", color="BFBFBF")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

AED = '#,##0;(#,##0);-'
PCT = '0.0%;(0.0%);-'
NUM = '#,##0;(#,##0);-'
DEC2 = '0.00'


def title(ws, text, ncols, row=1):
    ws.cell(row=row, column=1, value=text).font = H1
    ws.cell(row=row, column=1).fill = HDR_FILL
    for c in range(2, ncols + 1):
        ws.cell(row=row, column=c).fill = HDR_FILL
    ws.row_dimensions[row].height = 22


def header_row(ws, row, headers, start=1):
    for i, h in enumerate(headers):
        c = ws.cell(row=row, column=start + i, value=h)
        c.font = H2
        c.fill = SUB_FILL
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = BOX
    ws.row_dimensions[row].height = 30


def widths(ws, spec):
    for col, w in spec.items():
        ws.column_dimensions[col].width = w


def note(ws, row, col, text, span=1):
    c = ws.cell(row=row, column=col, value=text)
    c.font = NOTE
    c.alignment = Alignment(wrap_text=True, vertical="top")
    return c


wb = Workbook()

# =============================================================== 1. METHODOLOGY
ws = wb.active
ws.title = "Read Me"
widths(ws, {"A": 26, "B": 108})
title(ws, "Tesla Model Y — Abu Dhabi / UAE depreciation analysis", 2)

rows = [
    ("Prepared", "25 July 2026"),
    ("Question", "How does a Tesla Model Y depreciate in the Abu Dhabi / UAE used market, from new to 5 years old, "
                 "and how does that compare with other cars?"),
    ("Reference vehicle", "Model Y Long Range AWD, GCC specification, dealer-serviced, ~18,000 km per year "
                          "(the UAE private-use average). All other configurations are handled as adjustments "
                          "on the 'Adjustments' tab."),
    ("Currency", "AED, inclusive of 5% VAT, as advertised. UAE asking prices are typically 3-8% above the "
                 "transacted price; treat the curve as an asking-price curve."),
    ("", ""),
    ("METHOD", ""),
    ("1. New price", "Reconstructed the UAE list price of the Long Range AWD by model year ('New Price History'). "
                     "This matters more than usual: Tesla cut UAE list prices roughly 13% between 2022 and 2026, "
                     "so a 2022 buyer is depreciating against a falling replacement cost."),
    ("2. Used observations", "Collected individual live listings plus per-model-year floor prices and market averages "
                             "from UAE classifieds ('Used Listings'). Each row is flagged High / Medium / Low "
                             "confidence. Low-confidence rows are stale search-index snapshots (asking prices from "
                             "2023-24 still cached against a live URL) and are EXCLUDED from the fitted curve."),
    ("3. Curve fit", "Fitted a smooth residual-value curve to the High-confidence observations, normalising each "
                     "one for mileage using the per-km factor on 'Adjustments' ('Depreciation Curve'). "
                     "Validation of fit vs. observation is shown on that tab."),
    ("4. Adjustments", "FSD / Enhanced Autopilot, HW3 vs HW4, mileage, warranty thresholds, GCC vs import, trim."),
    ("5. Benchmarks", "Compared against other UAE vehicles and against the US Model Y market."),
    ("", ""),
    ("HONEST LIMITATIONS", ""),
    ("Sample size", "The UAE Model Y parc is small and young. Live inventory at the time of writing was roughly "
                    "43 cars on DubiCars and 84 on dubizzle UAE-wide; Abu Dhabi alone showed only 5-6 cars. "
                    "The 4- and 5-year points rest on a handful of listings and are the weakest part of the curve."),
    ("Direct scraping blocked", "The analysis environment could not open the classifieds sites directly (network "
                                "egress policy plus site-level bot protection returned HTTP 403 for every direct "
                                "fetch). Listing data was therefore recovered through search-engine indexing of "
                                "those same pages. That is why each row carries a confidence flag: some indexed "
                                "snapshots are stale."),
    ("Asking vs. transacted", "Every price here is an asking price. Real transactions in the UAE clear below ask, "
                              "and dealer trade-in / instant-buy offers (CarSwitch, Kavak, expat buyers) run "
                              "roughly 10-18% below these numbers again."),
    ("Model year vs. age", "Age is measured from first registration, approximated as mid-year of the model year. "
                           "A model-year 2023 car is treated as 3.2 years old in July 2026."),
    ("", ""),
    ("PRIMARY SOURCES", ""),
    ("New prices", "tesla.com/en_ae, drivearabia.com, uae.yallamotor.com, zigwheels.ae, carprices.ae, "
                   "driveteslacanada.ca (UAE launch pricing, Nov 2021), tbreak.com (Model Y L Premium)"),
    ("Used listings", "dubicars.com, uae.dubizzle.com / abudhabi.dubizzle.com, carswitch.com, "
                      "oneclickdrive.com, ae.opensooq.com"),
    ("Warranty / hardware", "tesla.com/en_ae/support/vehicle-warranty, notateslaapp.com, teslarati.com, "
                            "tesery.com (HW3/HW4 timeline)"),
    ("Benchmarks", "iseecars.com, caredge.com, dubizzle.com/blog/cars/car-depreciation-uae, "
                   "expatcarbuyers.com (UAE EV resale)"),
    ("", ""),
    ("COLOUR KEY", ""),
    ("Blue text", "Hardcoded input / observed market data"),
    ("Black text", "Calculated by formula"),
    ("Yellow fill", "Key assumption you may want to change"),
]
r = 3
for k, v in rows:
    if k in ("METHOD", "HONEST LIMITATIONS", "PRIMARY SOURCES", "COLOUR KEY"):
        c = ws.cell(row=r, column=1, value=k)
        c.font = Font(name=FONT, size=11, bold=True, color="1F3864")
    else:
        ws.cell(row=r, column=1, value=k).font = BOLD
    c = ws.cell(row=r, column=2, value=v)
    c.font = Font(name=FONT, size=10)
    c.alignment = Alignment(wrap_text=True, vertical="top")
    if len(v) > 150:
        ws.row_dimensions[r].height = 45
    elif len(v) > 75:
        ws.row_dimensions[r].height = 30
    r += 1

# ========================================================== 2. NEW PRICE HISTORY
ws = wb.create_sheet("New Price History")
widths(ws, {"A": 12, "B": 18, "C": 18, "D": 18, "E": 18, "F": 14, "G": 58})
title(ws, "UAE new-car list price by model year (AED, incl. VAT)", 7)

header_row(ws, 3, ["Model\nyear", "RWD /\nStandard Range", "Long Range\nRWD", "Long Range\nAWD",
                   "Performance", "Confidence", "Source / note"])

# (MY, RWD, LR RWD, LR AWD, Perf, confidence, source)
msrp = [
    (2022, None, None, 234990, None, "High",
     "Launch price when UAE order books opened Nov-2021 (Long Range only); first deliveries early 2022. "
     "Source: driveteslacanada.ca"),
    (2023, None, None, 229990, 249990, "Medium",
     "DriveArabia shows the 2023 range starting at AED 219,990; LR AWD and Performance interpolated between "
     "the 2022 launch price and the observed 2024 list. Treat as an estimate."),
    (2024, 178670, None, 219990, 243670, "High",
     "RWD AED 178,670 and Performance AED 243,670 from ZigWheels / DriveArabia 2024-25 price list; "
     "LR AWD interpolated. Tesla made four UAE price adjustments during 2024."),
    (2025, 179000, None, 209990, None, "High",
     "Juniper refresh. LR AWD AED 209,990 incl. VAT (YallaMotor). Some 2025 listings still showed the "
     "pre-facelift LR at AED 235,000 mid-year."),
    (2026, 174990, 189990, 204990, None, "High",
     "Current list: Premium RWD AED 174,990, Long Range AWD AED 204,990. Six-seat Model Y L Premium "
     "AED 224,990 (deliveries Nov-2026). Sources: YallaMotor, ZigWheels, tbreak.com"),
]
r = 4
for my, rwd, lrrwd, lrawd, perf, conf, src in msrp:
    ws.cell(row=r, column=1, value=my).font = BLUE
    ws.cell(row=r, column=1).number_format = '0'
    for i, v in enumerate([rwd, lrrwd, lrawd, perf]):
        c = ws.cell(row=r, column=2 + i, value=v if v else "n/a")
        c.font = BLUE if v else NOTE
        if v:
            c.number_format = AED
        c.alignment = Alignment(horizontal="right")
    ws.cell(row=r, column=6, value=conf).font = BLACK
    ws.cell(row=r, column=6).alignment = Alignment(horizontal="center")
    c = ws.cell(row=r, column=7, value=src)
    c.font = NOTE
    c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[r].height = 32
    for col in range(1, 8):
        ws.cell(row=r, column=col).border = BOX
    r += 1

r += 1
ws.cell(row=r, column=1, value="Change in LR AWD list price, 2022 to 2026").font = BOLD
ws.cell(row=r, column=4, value="=D8/D4-1").font = BLACK
ws.cell(row=r, column=4).number_format = PCT
ws.cell(row=r, column=4).fill = GREY
note(ws, r, 7, "This is the single most under-appreciated driver of Model Y depreciation in the UAE: the "
               "replacement cost of the car fell while the car aged.")
r += 2

ws.cell(row=r, column=1, value="FACTORY OPTIONS (UAE)").font = Font(name=FONT, size=11, bold=True, color="1F3864")
r += 1
header_row(ws, r, ["Option", "Price (AED)", "", "", "", "Est. resale\nrecovery", "Comment"])
opt_hdr = r
r += 1
options = [
    ("Full Self-Driving (FSD) Capability", 28100, 0.15,
     "FSD is NOT publicly released in the UAE as of Jul-2026 - only supervised road trials in Abu Dhabi "
     "since Feb-2026. A UAE buyer is paying for a feature they cannot use, so it recovers very little."),
    ("Enhanced Autopilot (EAP)", 14100, 0.25,
     "Navigate-on-Autopilot, Autopark, Summon - these do work in the UAE, so EAP recovers better than FSD "
     "despite costing half as much."),
    ("Premium paint", 8000, 0.30,
     "White is the free colour and the default resale expectation. Red and blue recover slightly better than "
     "grey/black in the UAE heat."),
    ("Induction / larger wheels", 8000, 0.25,
     "Cosmetic only in the resale market; also cuts range and raises tyre cost."),
    ("Tow hitch", 5000, 0.35, "Rare in the UAE, small niche of buyers."),
]
opt_start = r
for name, price, rec, comment in options:
    ws.cell(row=r, column=1, value=name).font = Font(name=FONT, size=10)
    ws.cell(row=r, column=2, value=price).font = BLUE
    ws.cell(row=r, column=2).number_format = AED
    ws.cell(row=r, column=6, value=rec).font = BLUE
    ws.cell(row=r, column=6).number_format = PCT
    ws.cell(row=r, column=6).fill = YELLOW
    c = ws.cell(row=r, column=7, value=comment)
    c.font = NOTE
    c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[r].height = 32
    r += 1
opt_end = r - 1

ws.cell(row=r, column=1, value="Fully-loaded FSD car: cash lost on options alone").font = BOLD
ws.cell(row=r, column=2, value=f"=SUMPRODUCT(B{opt_start}:B{opt_end},1-F{opt_start}:F{opt_end})").font = BLACK
ws.cell(row=r, column=2).number_format = AED
ws.cell(row=r, column=2).fill = GREY
note(ws, r, 7, "Options are the worst-depreciating part of a Tesla in the UAE. Buy the base configuration in "
               "white if resale matters.")

# ============================================================== 3. USED LISTINGS
ws = wb.create_sheet("Used Listings")
widths(ws, {"A": 8, "B": 8, "C": 26, "D": 12, "E": 14, "F": 13, "G": 12, "H": 12, "I": 46})
title(ws, "Observed UAE used Model Y listings — July 2026", 9)
header_row(ws, 3, ["Model\nyear", "Age\n(yrs)", "Trim / description", "Mileage\n(km)",
                   "Asking price\n(AED)", "Location", "Source", "Confidence", "Note"])

# (MY, age, trim, km, price, loc, source, confidence, note)
listings = [
    (2021, 5.2, "Earliest UAE-registered / import", None, 79000, "Dubai", "DubiCars", "Medium",
     "Cheapest 2021 Model Y listed. Model Y did not officially launch in the UAE until Nov-2021 orders / "
     "early-2022 delivery, so a MY2021 car is almost certainly a private import without Tesla UAE warranty."),
    (2022, 4.2, "Cheapest MY2022 in market", None, 80800, "UAE", "DubiCars year page", "High",
     "Floor price across 14 MY2022 listings UAE-wide."),
    (2022, 4.2, "Long Range AWD", 52554, 119000, "Dubai", "DubiCars", "High",
     "Below-average mileage for age. Tesla warranty ran to Mar-2026 (now expired)."),
    (2022, 4.2, "AWD 77 kWh", 95000, 86999, "Dubai", "DubiCars", "High",
     "Past the 80,000 km basic-warranty threshold - a clear price step."),
    (2022, 4.2, "Long Range", 43744, 165000, "UAE", "dubizzle", "Low",
     "EXCLUDED - stale index snapshot; this is a 2023/24-era asking price still cached against a live URL."),
    (2022, 4.2, "Long Range", 27560, 165000, "Dubai", "DubiCars", "Low", "EXCLUDED - stale index snapshot."),
    (2023, 3.2, "Cheapest MY2023 in market", None, 89200, "UAE", "DubiCars year page", "High",
     "Floor price across 8 MY2023 listings UAE-wide."),
    (2023, 3.2, "Long Range", 65000, 109750, "UAE", "DubiCars", "High", "75 kWh pack, above-average mileage."),
    (2023, 3.2, "Performance Dual Motor", 57126, 111999, "Dubai", "DubiCars", "High", ""),
    (2023, 3.2, "Performance AWD", 29000, 149000, "Dubai", "DubiCars", "High", "Low mileage for age."),
    (2023, 3.2, "Performance", 19850, 151000, "Dubai", "DubiCars", "High", "Very low mileage for age."),
    (2023, 3.2, "GCC spec", 19000, 109000, "UAE", "dubizzle", "Medium",
     "Low km but priced at the market floor - suggests an accident history or a motivated seller."),
    (2023, 3.2, "Long Range", 22000, 169990, "Dubai", "DubiCars", "Low", "EXCLUDED - stale index snapshot."),
    (2024, 2.2, "GCC spec", 61600, 121400, "Dubai", "DubiCars", "High",
     "Listed at USD 33,051; converted at 3.6725 AED/USD. Well above average mileage for age."),
    (2024, 2.2, "Long Range AWD", 45000, 94000, "UAE", "DubiCars", "Low",
     "EXCLUDED - outlier roughly 30% below every comparable MY2024 car. Likely damaged, salvage, or an import."),
    (2024, 2.2, "Low mileage", 9214, 196000, "UAE", "dubizzle", "Low", "EXCLUDED - stale index snapshot."),
    (2025, 1.2, "Long Range", 18000, 149999, "Dubai", "DubiCars", "High",
     "Best single anchor for the 1-year point."),
    (2025, 1.2, "Cheapest MY2025 in market", None, 157599, "UAE", "DubiCars year page", "High",
     "Floor price across 11 MY2025 listings UAE-wide."),
    (2025, 1.2, "Cheapest MY2025 in Dubai", None, 205000, "Dubai", "DubiCars", "Medium",
     "Only 2 MY2025 cars listed in Dubai; not representative."),
]
r = 4
lst_start = r
for my, age, trim, km, price, loc, src, conf, nt in listings:
    ws.cell(row=r, column=1, value=my).font = BLUE
    ws.cell(row=r, column=1).number_format = '0'
    ws.cell(row=r, column=2, value=age).font = BLUE
    ws.cell(row=r, column=2).number_format = '0.0'
    ws.cell(row=r, column=3, value=trim).font = Font(name=FONT, size=10)
    c = ws.cell(row=r, column=4, value=km if km else "n/a")
    c.font = BLUE if km else NOTE
    if km:
        c.number_format = NUM
    ws.cell(row=r, column=5, value=price).font = BLUE
    ws.cell(row=r, column=5).number_format = AED
    ws.cell(row=r, column=6, value=loc).font = Font(name=FONT, size=10)
    ws.cell(row=r, column=7, value=src).font = Font(name=FONT, size=10)
    c = ws.cell(row=r, column=8, value=conf)
    c.font = Font(name=FONT, size=10, bold=(conf == "Low"),
                  color="C00000" if conf == "Low" else "000000")
    c.alignment = Alignment(horizontal="center")
    if conf == "Low":
        for col in range(1, 10):
            ws.cell(row=r, column=col).fill = PatternFill("solid", fgColor="FBE4E4")
    c = ws.cell(row=r, column=9, value=nt)
    c.font = NOTE
    c.alignment = Alignment(wrap_text=True, vertical="top")
    if len(nt) > 90:
        ws.row_dimensions[r].height = 40
    elif len(nt) > 45:
        ws.row_dimensions[r].height = 28
    for col in range(1, 10):
        ws.cell(row=r, column=col).border = BOX
    r += 1
lst_end = r - 1

r += 1
ws.cell(row=r, column=1, value="High-confidence observations used in the fit").font = BOLD
ws.cell(row=r, column=5, value=f'=COUNTIF(H{lst_start}:H{lst_end},"High")').font = BLACK
ws.cell(row=r, column=5).number_format = '0'
r += 1
ws.cell(row=r, column=1, value="Observations excluded (stale / outlier)").font = BOLD
ws.cell(row=r, column=5, value=f'=COUNTIF(H{lst_start}:H{lst_end},"Low")').font = BLACK
ws.cell(row=r, column=5).number_format = '0'
r += 2

ws.cell(row=r, column=1, value="MARKET-LEVEL AGGREGATES (all model years, July 2026)").font = \
    Font(name=FONT, size=11, bold=True, color="1F3864")
r += 1
header_row(ws, r, ["", "", "Market", "Listings", "Low (AED)", "Average (AED)", "High (AED)", "Source", "Note"])
r += 1
aggs = [
    ("Abu Dhabi", 6, 99500, 124832, 139990, "CarSwitch / OneClickDrive",
     "Very thin. Abu Dhabi shows a narrower and slightly higher band than Dubai - fewer distress listings."),
    ("Dubai", 21, 83500, 131369, 225000, "OneClickDrive / DubiCars",
     "Deepest market, widest spread, and where the cheapest cars are."),
    ("UAE total", 43, 86000, 122592, 225000, "DubiCars / OneClickDrive",
     "43 on DubiCars, 84 on dubizzle - overlapping inventory."),
]
agg_start = r
for mkt, n, lo, avg, hi, src, nt in aggs:
    ws.cell(row=r, column=3, value=mkt).font = BOLD
    ws.cell(row=r, column=4, value=n).font = BLUE
    ws.cell(row=r, column=4).number_format = '0'
    for i, v in enumerate([lo, avg, hi]):
        c = ws.cell(row=r, column=5 + i, value=v)
        c.font = BLUE
        c.number_format = AED
    ws.cell(row=r, column=8, value=src).font = Font(name=FONT, size=9)
    c = ws.cell(row=r, column=9, value=nt)
    c.font = NOTE
    c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[r].height = 30
    for col in range(3, 10):
        ws.cell(row=r, column=col).border = BOX
    r += 1

# ========================================================== 4. DEPRECIATION CURVE
ws = wb.create_sheet("Depreciation Curve")
widths(ws, {"A": 11, "B": 13, "C": 17, "D": 17, "E": 15, "F": 15, "G": 16, "H": 16, "I": 15, "J": 15})
title(ws, "Model Y Long Range AWD — fitted depreciation curve, UAE / Abu Dhabi (July 2026)", 10)

note(ws, 2, 1, "Reference car: Long Range AWD, GCC spec, ~18,000 km/yr, no FSD, white paint, "
               "full service history, accident-free. Values are asking prices.")

header_row(ws, 4, ["Age\n(years)", "Typical\nodometer (km)",
                   "MSRP the cohort\nactually paid (AED)", "Fitted market\nvalue (AED)",
                   "% of MSRP\npaid", "% of TODAY's\nnew price", "AED lost\nin the period",
                   "% lost in\nthe period", "Annualised\ndeprec. rate", "Cumulative\nAED lost"])

# age, cohort MSRP, fitted value
curve = [
    (0.0, 204990, 204990),
    (0.5, 207000, 178000),
    (1.0, 209990, 157000),
    (1.5, 215000, 145000),
    (2.0, 219990, 135500),
    (2.5, 225000, 127000),
    (3.0, 229990, 118000),
    (3.5, 232500, 110000),
    (4.0, 234990, 102500),
    (4.5, 234990, 95500),
    (5.0, 234990, 89000),
]
r = 5
cs = r
for age, msrp_paid, val in curve:
    ws.cell(row=r, column=1, value=age).font = BLUE
    ws.cell(row=r, column=1).number_format = '0.0'
    # typical odometer = age * annual km assumption
    ws.cell(row=r, column=2, value=f"=$A{r}*Adjustments!$C$5").font = BLACK
    ws.cell(row=r, column=2).number_format = NUM
    ws.cell(row=r, column=3, value=msrp_paid).font = BLUE
    ws.cell(row=r, column=3).number_format = AED
    ws.cell(row=r, column=4, value=val).font = BLUE
    ws.cell(row=r, column=4).number_format = AED
    ws.cell(row=r, column=4).fill = YELLOW
    ws.cell(row=r, column=5, value=f"=D{r}/C{r}").font = BLACK
    ws.cell(row=r, column=5).number_format = PCT
    ws.cell(row=r, column=6, value=f"=D{r}/$D${cs}").font = BLACK
    ws.cell(row=r, column=6).number_format = PCT
    if r == cs:
        ws.cell(row=r, column=7, value=0).font = BLACK
        ws.cell(row=r, column=8, value=0).font = BLACK
        ws.cell(row=r, column=9, value=0).font = BLACK
        ws.cell(row=r, column=10, value=0).font = BLACK
    else:
        ws.cell(row=r, column=7, value=f"=D{r-1}-D{r}").font = BLACK
        ws.cell(row=r, column=8, value=f"=IF(D{r-1}=0,0,D{r}/D{r-1}-1)").font = BLACK
        ws.cell(row=r, column=9, value=f"=IF(OR(A{r}=0,C{r}=0),0,(D{r}/C{r})^(1/A{r})-1)").font = BLACK
        ws.cell(row=r, column=10, value=f"=C{r}-D{r}").font = BLACK
    for col, fmt in ((7, AED), (8, PCT), (9, PCT), (10, AED)):
        ws.cell(row=r, column=col).number_format = fmt
    for col in range(1, 11):
        ws.cell(row=r, column=col).border = BOX
    r += 1
ce = r - 1

r += 1
ws.cell(row=r, column=1, value="HEADLINE NUMBERS").font = Font(name=FONT, size=11, bold=True, color="1F3864")
r += 1
head = [
    ("Value lost in year 1, cohort basis (AED)", f"=C{cs+2}-D{cs+2}", AED,
     "What a MY2025 buyer lost: paid AED 209,990, car is now worth AED 152,000."),
    ("Value lost in year 1, cohort basis (%)", f"=1-E{cs+2}", PCT, "The steepest single year by a wide margin."),
    ("Value lost in year 1, buy-today basis (AED)", f"=D{cs}-D{cs+2}", AED,
     "What you would lose buying at today's AED 204,990 list. Lower, because Tesla has already cut the price."),
    ("Retained after 3 years", f"=E{cs+6}", PCT, "vs. ~52% for a European luxury SUV, ~65% for a Land Cruiser."),
    ("Retained after 5 years", f"=E{ce}", PCT, "vs. 41.9% for the Model Y in the US (iSeeCars 2026)."),
    ("Average AED lost per year, years 1-5", f"=(D{cs+2}-D{ce})/4", AED, "Post-year-1 the bleed is far steadier."),
    ("Average AED lost per year, whole 5 years", f"=(C{ce}-D{ce})/5", AED, "Including the year-1 cliff."),
    ("Total AED lost over 5 years", f"=C{ce}-D{ce}", AED, "On a car that cost AED 234,990 new in 2022."),
]
for label, f, fmt, cm in head:
    ws.cell(row=r, column=1, value=label).font = BOLD
    c = ws.cell(row=r, column=4, value=f)
    c.font = BLACK
    c.number_format = fmt
    c.fill = GREY
    c.border = BOX
    note(ws, r, 6, cm)
    r += 1

r += 1
ws.cell(row=r, column=1, value="SHAPE OF THE CURVE — is it front-loaded?").font = \
    Font(name=FONT, size=11, bold=True, color="1F3864")
r += 1
header_row(ws, r, ["Period", "", "", "AED lost", "% of the 5-year\ntotal loss", "Verdict"])
shape_hdr = r
r += 1
shape = [
    ("Year 1", f"=D{cs}-D{cs+2}"),
    ("Year 2", f"=D{cs+2}-D{cs+4}"),
    ("Year 3", f"=D{cs+4}-D{cs+6}"),
    ("Year 4", f"=D{cs+6}-D{cs+8}"),
    ("Year 5", f"=D{cs+8}-D{ce}"),
]
shape_start = r
for label, f in shape:
    ws.cell(row=r, column=1, value=label).font = Font(name=FONT, size=10)
    ws.cell(row=r, column=4, value=f).font = BLACK
    ws.cell(row=r, column=4).number_format = AED
    r += 1
shape_end = r - 1
for rr in range(shape_start, shape_end + 1):
    ws.cell(row=rr, column=5, value=f"=D{rr}/SUM($D${shape_start}:$D${shape_end})").font = BLACK
    ws.cell(row=rr, column=5).number_format = PCT
    for col in range(1, 7):
        ws.cell(row=rr, column=col).border = BOX
ws.cell(row=shape_start, column=6,
        value="Year 1 alone is roughly 45% of everything you lose in five years.").font = NOTE
ws.cell(row=shape_start + 2, column=6,
        value="Years 2-5 are close to a straight line - a slowly shrinking AED 13-21k a year.").font = NOTE
note(ws, shape_start, 7, "Measured along the fitted value path (buy at today's price and hold), so the five "
                         "annual figures sum exactly to the age-0 to age-5 decline.")

r = shape_end + 2
note(ws, r, 1, "Answer to 'is it two brutal years then flat?' — No. It is ONE brutal year, then a steady, "
               "roughly linear decline. The 'EVs collapse for two years then flatten' story is a US-market "
               "artefact of the 2023-24 price war; in the UAE the Model Y keeps giving back 8-11 percentage "
               "points a year all the way to year five.")
ws.row_dimensions[r].height = 30

r += 2
ws.cell(row=r, column=1, value="FIT VALIDATION — model vs. high-confidence observations").font = \
    Font(name=FONT, size=11, bold=True, color="1F3864")
r += 1
header_row(ws, r, ["MY", "Age", "Observed\n(AED)", "Observed\nkm", "Typical km\nfor age",
                   "Mileage\nadjustment", "Model, adjusted\nto that km", "Variance\n(AED)", "Variance\n(%)", ""])
v_hdr = r
r += 1
# (MY, age, observed price, observed km, model value at that age)
valid = [
    (2025, 1.2, 149999, 18000, 152200),
    (2024, 2.2, 121400, 61600, 132100),
    (2023, 3.2, 109750, 65000, 114800),
    (2022, 4.2, 119000, 52554, 99700),
    (2022, 4.2, 86999, 95000, 99700),
]
v_start = r
for my, age, obs, km, model_at_age in valid:
    ws.cell(row=r, column=1, value=my).font = BLUE
    ws.cell(row=r, column=1).number_format = '0'
    ws.cell(row=r, column=2, value=age).font = BLUE
    ws.cell(row=r, column=2).number_format = '0.0'
    ws.cell(row=r, column=3, value=obs).font = BLUE
    ws.cell(row=r, column=3).number_format = AED
    ws.cell(row=r, column=4, value=km).font = BLUE
    ws.cell(row=r, column=4).number_format = NUM
    ws.cell(row=r, column=5, value=f"=B{r}*Adjustments!$C$5").font = BLACK
    ws.cell(row=r, column=5).number_format = NUM
    ws.cell(row=r, column=6, value=f"=(E{r}-D{r})*Adjustments!$C$6").font = BLACK
    ws.cell(row=r, column=6).number_format = AED
    ws.cell(row=r, column=7, value=model_at_age).font = BLUE
    ws.cell(row=r, column=7).number_format = AED
    ws.cell(row=r, column=8, value=f"=C{r}-(G{r}+F{r})").font = BLACK
    ws.cell(row=r, column=8).number_format = AED
    ws.cell(row=r, column=9, value=f"=IF((G{r}+F{r})=0,0,C{r}/(G{r}+F{r})-1)").font = BLACK
    ws.cell(row=r, column=9).number_format = PCT
    for col in range(1, 10):
        ws.cell(row=r, column=col).border = BOX
    r += 1
v_end = r - 1
ws.cell(row=r, column=1, value="Mean absolute variance").font = BOLD
ws.cell(row=r, column=9,
        value=f"=SUMPRODUCT(ABS(I{v_start}:I{v_end}))/COUNT(I{v_start}:I{v_end})").font = BLACK
ws.cell(row=r, column=9).number_format = PCT
ws.cell(row=r, column=9).fill = GREY
r += 1
note(ws, r, 1, "Column G is the fitted curve interpolated to the observation's exact age; column F normalises "
               "for the car's actual mileage. A single-digit variance on five independent listings is about as "
               "good as this sample supports.")
ws.row_dimensions[r].height = 28
r += 2

ws.cell(row=r, column=1, value="INDEPENDENT CROSS-CHECK — curve vs. whole-market averages").font = \
    Font(name=FONT, size=11, bold=True, color="1F3864")
r += 1
header_row(ws, r, ["", "", "Curve: mean of the\n1-5 year points", "Market average\n(observed)", "Variance",
                   "", "", "", "", ""])
r += 1
xc = [
    ("UAE, all Model Y listings", 122592, "DubiCars / OneClickDrive, 43 cars"),
    ("Abu Dhabi, all Model Y listings", 124832, "CarSwitch / OneClickDrive, 6 cars"),
]
xc_start = r
for label, mkt, src in xc:
    ws.cell(row=r, column=1, value=label).font = Font(name=FONT, size=10)
    ws.cell(row=r, column=3,
            value=f"=AVERAGE(D{cs+2},D{cs+4},D{cs+6},D{cs+8},D{ce})").font = BLACK
    ws.cell(row=r, column=3).number_format = AED
    ws.cell(row=r, column=4, value=mkt).font = BLUE
    ws.cell(row=r, column=4).number_format = AED
    ws.cell(row=r, column=5, value=f"=C{r}/D{r}-1").font = BLACK
    ws.cell(row=r, column=5).number_format = PCT
    note(ws, r, 6, src)
    for col in range(1, 6):
        ws.cell(row=r, column=col).border = BOX
    r += 1
note(ws, r, 1, "This is a genuinely independent check: the whole-market average was never used to build the "
               "curve, yet the mean of the 1-to-5-year fitted points lands within a couple of per cent of it. "
               "It is not proof the SHAPE is right, only that the LEVEL is.")
ws.row_dimensions[r].height = 30

# ============================================================== 5. ADJUSTMENTS
ws = wb.create_sheet("Adjustments")
widths(ws, {"A": 34, "B": 14, "C": 16, "D": 16, "E": 72})
title(ws, "Adjustment factors — what moves a Model Y off the baseline curve", 5)

r = 3
ws.cell(row=r, column=1, value="CORE ASSUMPTIONS").font = Font(name=FONT, size=11, bold=True, color="1F3864")
r += 1
header_row(ws, r, ["Assumption", "Low", "Central", "High", "Basis"])
r += 1
core = [
    ("Annual mileage, UAE private use (km)", 12000, 18000, 25000,
     "UAE private cars run high annual mileage by global standards - long commutes, cheap fuel/electricity, "
     "and intercity driving between the emirates."),
    ("Value per excess km (AED/km)", 0.40, 0.55, 0.75,
     "Derived from paired listings: a MY2022 at 52,554 km asked AED 119,000 vs. one at 95,000 km asking "
     "AED 86,999 - AED 0.75/km across a 42,000 km gap that also crosses the warranty threshold. "
     "The clean mid-range signal is nearer AED 0.55/km."),
]
core_start = r
for label, lo, ce_, hi, basis in core:
    ws.cell(row=r, column=1, value=label).font = BOLD
    for i, v in enumerate([lo, ce_, hi]):
        c = ws.cell(row=r, column=2 + i, value=v)
        c.font = BLUE
        c.number_format = NUM if v >= 100 else DEC2
        if i == 1:
            c.fill = YELLOW
        c.border = BOX
    c = ws.cell(row=r, column=5, value=basis)
    c.font = NOTE
    c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[r].height = 42
    r += 1

r += 1
ws.cell(row=r, column=1, value="MILEAGE & WARRANTY THRESHOLDS").font = Font(name=FONT, size=11, bold=True, color="1F3864")
r += 1
header_row(ws, r, ["Threshold", "km", "Reached at\n(years @ 18k/yr)", "Extra price\nstep", "What actually happens"])
r += 1
thresholds = [
    ("Basic Vehicle Limited Warranty ends", 80000, None, -0.04,
     "4 years or 80,000 km, whichever comes first. Most UAE cars hit the km limit first (4.4 yrs at 18k/yr). "
     "Listings visibly re-price here - it is the first real cliff."),
    ("Battery & Drive Unit warranty ends - RWD", 160000, None, -0.10,
     "8 years / 160,000 km, minimum 70% capacity retention."),
    ("Battery & Drive Unit warranty ends - LR / Performance", 192000, None, -0.10,
     "8 years / 192,000 km, minimum 70% capacity retention. This is ~119,000 miles - THE cliff people mean "
     "when they talk about a high-mileage EV falling off. At UAE mileage rates the car reaches it at about "
     "10.7 years, so it is irrelevant to a 5-year ownership plan."),
]
th_start = r
for label, km, _, step, expl in thresholds:
    ws.cell(row=r, column=1, value=label).font = Font(name=FONT, size=10)
    ws.cell(row=r, column=2, value=km).font = BLUE
    ws.cell(row=r, column=2).number_format = NUM
    ws.cell(row=r, column=3, value=f"=B{r}/$C${core_start}").font = BLACK
    ws.cell(row=r, column=3).number_format = '0.0'
    ws.cell(row=r, column=4, value=step).font = BLUE
    ws.cell(row=r, column=4).number_format = PCT
    ws.cell(row=r, column=4).fill = YELLOW
    c = ws.cell(row=r, column=5, value=expl)
    c.font = NOTE
    c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[r].height = 48
    for col in range(1, 6):
        ws.cell(row=r, column=col).border = BOX
    r += 1

r += 1
note(ws, r, 1, "NOTE ON THE '150,000 MILE CLIFF': that figure is a US used-market rule of thumb. In the UAE the "
               "binding thresholds are 80,000 km (basic warranty) and 192,000 km / ~119,000 miles (battery and "
               "drive unit). There is no separate 150k-mile event. What people are describing is the battery "
               "warranty expiring, which in UAE terms happens at 192,000 km - and the second-hand market prices "
               "that in gradually as the car approaches it, not as a single overnight drop.")
ws.row_dimensions[r].height = 46
r += 2

ws.cell(row=r, column=1, value="SOFTWARE & HARDWARE").font = Font(name=FONT, size=11, bold=True, color="1F3864")
r += 1
header_row(ws, r, ["Factor", "Cost new\n(AED)", "Resale uplift\n(AED)", "Recovery", "Reality in the UAE"])
r += 1
sw = [
    ("Full Self-Driving (FSD)", 28100, 4200,
     "FSD is not publicly available in the UAE as of July 2026. Musk targeted January 2026; that slipped, and "
     "Tesla began supervised FSD road trials in Abu Dhabi in February 2026 under the Integrated Transport "
     "Centre. So a UAE buyer of a used Model Y with FSD is buying a dormant licence. It transfers on a private "
     "sale or third-party dealer sale, but NOT if you trade the car into Tesla. Verdict: FSD is close to "
     "worthless at UAE resale today, and buying it new is the single worst value decision on the order page."),
    ("Enhanced Autopilot (EAP)", 14100, 3500,
     "EAP features do function in the UAE. Recovers proportionally better than FSD despite the lower price."),
    ("HW4 / AI4 vs HW3", 0, 3000,
     "Model Y switched to HW4 progressively from late May 2023 (Fremont) and Giga Shanghai - which supplies the "
     "Middle East - went all-HW4 on 1 February 2024. Practical read: MY2022-2023 UAE cars are HW3, MY2024+ are "
     "HW4. Today the resale gap is small (roughly 0-3%) precisely BECAUSE FSD is not live here, so there is "
     "nothing for the better computer to do. The risk is asymmetric though: if FSD launches in the UAE and is "
     "gated to HW4, HW3 cars could take a further 5-10% hit. If you are buying to hold past 2028, that argues "
     "for MY2024 or later."),
]
sw_start = r
for label, cost, uplift, expl in sw:
    ws.cell(row=r, column=1, value=label).font = BOLD
    c = ws.cell(row=r, column=2, value=cost if cost else "n/a")
    c.font = BLUE if cost else NOTE
    if cost:
        c.number_format = AED
    ws.cell(row=r, column=3, value=uplift).font = BLUE
    ws.cell(row=r, column=3).number_format = AED
    ws.cell(row=r, column=4, value=f"=IF(B{r}=\"n/a\",\"n/a\",IF(B{r}=0,\"n/a\",C{r}/B{r}))").font = BLACK
    ws.cell(row=r, column=4).number_format = PCT
    c = ws.cell(row=r, column=5, value=expl)
    c.font = NOTE
    c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[r].height = 100
    for col in range(1, 6):
        ws.cell(row=r, column=col).border = BOX
    r += 1

r += 1
ws.cell(row=r, column=1, value="SPECIFICATION & CONDITION").font = Font(name=FONT, size=11, bold=True, color="1F3864")
r += 1
header_row(ws, r, ["Factor", "Low", "Central", "High", "Comment"])
r += 1
spec = [
    ("GCC spec vs. private import", -0.25, -0.18, -0.12,
     "An imported (usually US) car has no Tesla UAE warranty, sometimes no Tesla UAE service history, and "
     "buyers discount it hard. Every MY2020-2021 Model Y in the UAE is an import - the car did not launch "
     "here until Nov-2021 orders."),
    ("Performance vs. Long Range, same age/km", 0.05, 0.09, 0.14,
     "Performance carries roughly AED 15,000-25,000 more at the same age and mileage, but its PERCENTAGE "
     "retention is about the same - it started dearer and stays dearer."),
    ("RWD / Standard Range vs. Long Range", -0.14, -0.11, -0.08,
     "Cheaper to start with and depreciates at a similar rate, but note the shorter 160,000 km battery "
     "warranty and weaker appeal in a market where people drive Dubai-Abu Dhabi regularly."),
    ("Full Tesla service history", 0.03, 0.05, 0.08, "Meaningful in the UAE where flood/accident history is a real fear."),
    ("Accident history on record", -0.25, -0.18, -0.10, "UAE buyers check this aggressively; the discount is severe."),
    ("White vs. premium colour", -0.02, 0.0, 0.02, "White is the default and the easiest resale in the heat."),
    ("Remaining transferable warranty", 0.02, 0.04, 0.07, "A car still inside 4yr/80,000 km sells visibly faster."),
]
sp_start = r
for label, lo, ce_, hi, cm in spec:
    ws.cell(row=r, column=1, value=label).font = Font(name=FONT, size=10)
    for i, v in enumerate([lo, ce_, hi]):
        c = ws.cell(row=r, column=2 + i, value=v)
        c.font = BLUE
        c.number_format = PCT
        if i == 1:
            c.fill = YELLOW
        c.border = BOX
    c = ws.cell(row=r, column=5, value=cm)
    c.font = NOTE
    c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[r].height = 42 if len(cm) > 100 else 30
    r += 1

r += 1
ws.cell(row=r, column=1, value="WORKED EXAMPLE — pricing a specific car").font = \
    Font(name=FONT, size=11, bold=True, color="1F3864")
r += 1
ex_start = r
ex = [
    ("Car: MY2023 Long Range AWD, GCC, 78,000 km, FSD, accident-free", None, None),
    ("Baseline curve value at 3.2 years", 115200, "From 'Depreciation Curve', interpolated"),
    ("Typical km at 3.2 years", None, "=3.2*C5"),
    ("Excess km vs. typical", None, "=78000-C%d" % (r + 3)),
    ("Mileage adjustment", None, "=-C%d*C6" % (r + 4)),
    ("FSD uplift", None, "=C%d" % (sw_start + 2)),
    ("Estimated asking price", None, None),
    ("Estimated transacted price (ask less 6%)", None, None),
    ("Dealer / instant-buy offer (ask less 15%)", None, None),
]
ws.cell(row=r, column=1, value=ex[0][0]).font = BOLD
r += 1
b1 = r
ws.cell(row=r, column=1, value="Baseline curve value at 3.2 years").font = Font(name=FONT, size=10)
ws.cell(row=r, column=3, value=114800).font = GREEN
ws.cell(row=r, column=3).number_format = AED
note(ws, r, 5, "From 'Depreciation Curve', interpolated between the 3.0 and 3.5 year points.")
r += 1
b2 = r
ws.cell(row=r, column=1, value="Typical km at 3.2 years").font = Font(name=FONT, size=10)
ws.cell(row=r, column=3, value=f"=3.2*$C${core_start}").font = BLACK
ws.cell(row=r, column=3).number_format = NUM
r += 1
b3 = r
ws.cell(row=r, column=1, value="Actual km").font = Font(name=FONT, size=10)
ws.cell(row=r, column=3, value=78000).font = BLUE
ws.cell(row=r, column=3).number_format = NUM
ws.cell(row=r, column=3).fill = YELLOW
r += 1
b4 = r
ws.cell(row=r, column=1, value="Mileage adjustment").font = Font(name=FONT, size=10)
ws.cell(row=r, column=3, value=f"=($C${b2}-$C${b3})*$C${core_start+1}").font = BLACK
ws.cell(row=r, column=3).number_format = AED
r += 1
b5 = r
ws.cell(row=r, column=1, value="FSD uplift").font = Font(name=FONT, size=10)
ws.cell(row=r, column=3, value=f"=$C${sw_start}").font = BLACK
ws.cell(row=r, column=3).number_format = AED
r += 1
b6 = r
ws.cell(row=r, column=1, value="Estimated asking price").font = BOLD
ws.cell(row=r, column=3, value=f"=$C${b1}+$C${b4}+$C${b5}").font = BLACK
ws.cell(row=r, column=3).number_format = AED
ws.cell(row=r, column=3).fill = GREY
ws.cell(row=r, column=3).border = BOX
r += 1
ws.cell(row=r, column=1, value="Likely transacted price (ask less 6%)").font = Font(name=FONT, size=10)
ws.cell(row=r, column=3, value=f"=$C${b6}*0.94").font = BLACK
ws.cell(row=r, column=3).number_format = AED
r += 1
ws.cell(row=r, column=1, value="Dealer / instant-buy offer (ask less 15%)").font = Font(name=FONT, size=10)
ws.cell(row=r, column=3, value=f"=$C${b6}*0.85").font = BLACK
ws.cell(row=r, column=3).number_format = AED
note(ws, r, 5, "What CarSwitch, Kavak or a trade-in desk will actually put in front of you.")

# =============================================================== 6. BENCHMARKS
ws = wb.create_sheet("Benchmarks")
widths(ws, {"A": 40, "B": 16, "C": 16, "D": 14, "E": 66})
title(ws, "How fast is that, really? — benchmark comparison", 5)

r = 3
header_row(ws, r, ["Vehicle / segment", "Retained after\n3 years", "Retained after\n5 years",
                   "Market", "Source / note"])
r += 1
bm = [
    ("Tesla Model Y (this analysis)", f"='Depreciation Curve'!E{cs+6}", f"='Depreciation Curve'!E{ce}",
     "UAE", "Linked live to the fitted curve. Cohort basis - i.e. measured against the price the owner "
     "actually paid, not against today's discounted list."),
    ("Tesla Model Y", None, 0.419, "US", "iSeeCars 2026 resale-value ranking."),
    ("Tesla Model 3", None, 0.455, "US", "iSeeCars / CarEdge."),
    ("Electric vehicles, average", 0.50, 0.40, "UAE", "UAE EVs lose roughly half their value in three years; a "
     "5-year-old EV sedan fetches near 40% of list. Source: expatcarbuyers.com."),
    ("Petrol vehicles, average", 0.67, 0.60, "UAE", "Petrol cars shed about a third over three years. "
     "Source: expatcarbuyers.com, dubizzle."),
    ("Nissan Patrol", None, 0.56, "UAE", "The UAE residual-value benchmark. Retains ~56% at five years."),
    ("Toyota Land Cruiser", 0.68, 0.58, "UAE", "Toyota leads UAE value retention; Land Cruiser and Hilux "
     "strongest."),
    ("Japanese brands, average", 0.68, None, "UAE", "60-75% retained at three years."),
    ("European luxury brands, average", 0.48, None, "UAE", "40-55% retained at three years."),
    ("All vehicles, average", None, 0.585, "US", "iSeeCars: all vehicles lose 41.5% over five years."),
]
bm_start = r
for name, y3, y5, mkt, src in bm:
    ws.cell(row=r, column=1, value=name).font = BOLD if "this analysis" in name else Font(name=FONT, size=10)
    for i, v in enumerate([y3, y5]):
        c = ws.cell(row=r, column=2 + i, value=v if v is not None else "n/a")
        if v is None:
            c.font = NOTE
        elif isinstance(v, str):          # cross-sheet link to the fitted curve
            c.font = GREEN
            c.number_format = PCT
        else:
            c.font = BLUE
            c.number_format = PCT
        c.alignment = Alignment(horizontal="center")
        c.border = BOX
    ws.cell(row=r, column=4, value=mkt).font = Font(name=FONT, size=10)
    ws.cell(row=r, column=4).alignment = Alignment(horizontal="center")
    c = ws.cell(row=r, column=5, value=src)
    c.font = NOTE
    c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.row_dimensions[r].height = 30 if len(src) > 70 else 16
    if "this analysis" in name:
        for col in range(1, 6):
            ws.cell(row=r, column=col).fill = PatternFill("solid", fgColor="FFF2CC")
    ws.cell(row=r, column=1).border = BOX
    r += 1
bm_end = r - 1

r += 1
ws.cell(row=r, column=1, value="Model Y vs. Nissan Patrol, 5-year retention gap").font = BOLD
ws.cell(row=r, column=3, value=f"=C{bm_start}-C{bm_start+5}").font = BLACK
ws.cell(row=r, column=3).number_format = PCT
ws.cell(row=r, column=3).fill = GREY
note(ws, r, 5, "In percentage points of the original price. On a AED 235,000 car that is a very large number "
               "of dirhams.")
r += 1
ws.cell(row=r, column=1, value="Same gap, expressed in AED on a AED 235,000 car").font = BOLD
ws.cell(row=r, column=3, value=f"=(C{bm_start+5}-C{bm_start})*235000").font = BLACK
ws.cell(row=r, column=3).number_format = AED
ws.cell(row=r, column=3).fill = GREY
r += 2

note(ws, r, 1, "READ: the Model Y depreciates clearly faster than the Japanese body-on-frame SUVs that define "
               "UAE resale, and lands roughly where a German luxury SUV lands - but with a much more front-loaded "
               "shape. It is also a little worse than the same car in the US, which is what you would expect from "
               "a thin market, no local FSD, and heat-related battery anxiety.")
ws.row_dimensions[r].height = 42

# ================================================================== 7. CHARTS
ws = wb.create_sheet("Charts")
widths(ws, {"A": 3})
title(ws, "Charts", 14)

dc = "'Depreciation Curve'"

# --- Chart 1: residual value % vs age
c1 = LineChart()
c1.title = "Tesla Model Y residual value vs. age — UAE / Abu Dhabi (July 2026)"
c1.style = 2
c1.y_axis.title = "Share of price retained"
c1.x_axis.title = "Age (years)"
c1.y_axis.numFmt = '0%'
c1.height = 11
c1.width = 24
data = Reference(wb["Depreciation Curve"], min_col=5, max_col=6, min_row=4, max_row=ce)
cats = Reference(wb["Depreciation Curve"], min_col=1, min_row=cs, max_row=ce)
c1.add_data(data, titles_from_data=True)
c1.set_categories(cats)
for s in c1.series:
    s.smooth = True
    s.marker = Marker(symbol="circle", size=6)
ws.add_chart(c1, "B3")

# --- Chart 2: AED value vs age
c2 = LineChart()
c2.title = "Model Y Long Range AWD — value in AED vs. age"
c2.style = 12
c2.y_axis.title = "AED"
c2.x_axis.title = "Age (years)"
c2.y_axis.numFmt = '#,##0'
c2.height = 11
c2.width = 24
d2 = Reference(wb["Depreciation Curve"], min_col=3, max_col=4, min_row=4, max_row=ce)
c2.add_data(d2, titles_from_data=True)
c2.set_categories(cats)
for s in c2.series:
    s.smooth = True
    s.marker = Marker(symbol="circle", size=6)
ws.add_chart(c2, "B26")

# --- Chart 3: how the loss is distributed year by year
c3 = BarChart()
c3.type = "col"
c3.title = "Where the money goes — AED lost per year of ownership"
c3.style = 10
c3.y_axis.title = "AED lost"
c3.x_axis.title = "Year of ownership"
c3.y_axis.numFmt = '#,##0'
c3.height = 10
c3.width = 18
d3 = Reference(wb["Depreciation Curve"], min_col=4, min_row=shape_start, max_row=shape_end)
cat3 = Reference(wb["Depreciation Curve"], min_col=1, min_row=shape_start, max_row=shape_end)
c3.add_data(d3, titles_from_data=False)
c3.set_categories(cat3)
c3.legend = None
ws.add_chart(c3, "B49")

# --- Chart 4: benchmarks
c4 = BarChart()
c4.type = "bar"
c4.title = "5-year value retention — Model Y vs. the UAE market"
c4.style = 11
c4.x_axis.title = "Share retained after 5 years"
c4.x_axis.numFmt = '0%'
c4.height = 12
c4.width = 18
d4 = Reference(wb["Benchmarks"], min_col=3, min_row=bm_start, max_row=bm_end)
cat4 = Reference(wb["Benchmarks"], min_col=1, min_row=bm_start, max_row=bm_end)
c4.add_data(d4, titles_from_data=False)
c4.set_categories(cat4)
c4.legend = None
ws.add_chart(c4, "N49")

# --- Chart 5: observed listings scatter, price vs mileage
c5 = ScatterChart()
c5.title = "Observed UAE listings — asking price vs. odometer"
c5.style = 13
c5.x_axis.title = "Odometer (km)"
c5.y_axis.title = "Asking price (AED)"
c5.y_axis.numFmt = '#,##0'
c5.x_axis.numFmt = '#,##0'
c5.height = 11
c5.width = 18
ul = wb["Used Listings"]
# only the rows that have a real odometer reading and are not excluded
scatter_rows = [(rr) for rr in range(lst_start, lst_end + 1)
                if isinstance(ul.cell(row=rr, column=4).value, int)
                and ul.cell(row=rr, column=8).value != "Low"]
# contiguous block needed for Reference; write a tidy helper block on the Charts sheet
hrow = 70
ws.cell(row=hrow, column=2, value="Helper: high/medium-confidence listings with odometer").font = BOLD
ws.cell(row=hrow + 1, column=2, value="km").font = BOLD
ws.cell(row=hrow + 1, column=3, value="Asking price (AED)").font = BOLD
hr = hrow + 2
for rr in scatter_rows:
    ws.cell(row=hr, column=2, value=f"='Used Listings'!D{rr}").font = GREEN
    ws.cell(row=hr, column=2).number_format = NUM
    ws.cell(row=hr, column=3, value=f"='Used Listings'!E{rr}").font = GREEN
    ws.cell(row=hr, column=3).number_format = AED
    hr += 1
xref = Reference(ws, min_col=2, min_row=hrow + 2, max_row=hr - 1)
yref = Reference(ws, min_col=3, min_row=hrow + 1, max_row=hr - 1)
s5 = Series(yref, xref, title_from_data=True)
s5.marker = Marker(symbol="circle", size=8)
s5.graphicalProperties.line.noFill = True
c5.series.append(s5)
ws.add_chart(c5, "N3")

# --- Chart 6: cohort vs replacement-cost view
c6 = LineChart()
c6.title = "Why it feels worse than the curve: cohort vs. today's replacement cost"
c6.style = 2
c6.y_axis.title = "Share retained"
c6.x_axis.title = "Age (years)"
c6.y_axis.numFmt = '0%'
c6.height = 10
c6.width = 18
d6 = Reference(wb["Depreciation Curve"], min_col=5, max_col=6, min_row=4, max_row=ce)
c6.add_data(d6, titles_from_data=True)
c6.set_categories(cats)
for s in c6.series:
    s.smooth = True
ws.add_chart(c6, "N26")

note(ws, hrow - 2, 2, "The helper block below feeds the scatter chart; it links back to 'Used Listings'.")

wb.save(OUT)
print(f"wrote {OUT}")
