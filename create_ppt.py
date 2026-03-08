#!/usr/bin/env python3
"""Generate Greenstone Financial Services research PPT."""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# Color scheme
DARK_GREEN = RGBColor(0x1B, 0x5E, 0x20)
MED_GREEN = RGBColor(0x2E, 0x7D, 0x32)
LIGHT_GREEN = RGBColor(0xE8, 0xF5, 0xE9)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BLACK = RGBColor(0x33, 0x33, 0x33)
GRAY = RGBColor(0x66, 0x66, 0x66)
LIGHT_GRAY = RGBColor(0xF5, 0xF5, 0xF5)
ACCENT_BLUE = RGBColor(0x15, 0x65, 0xC0)
ACCENT_ORANGE = RGBColor(0xE6, 0x51, 0x00)


def add_shape(slide, left, top, width, height, fill_color, line_color=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if line_color:
        shape.line.color.rgb = line_color
        shape.line.width = Pt(1)
    else:
        shape.line.fill.background()
    return shape


def add_rounded_rect(slide, left, top, width, height, fill_color):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.color.rgb = RGBColor(0xDD, 0xDD, 0xDD)
    shape.line.width = Pt(0.5)
    return shape


def add_text_box(slide, left, top, width, height, text, font_size=12,
                 bold=False, color=BLACK, alignment=PP_ALIGN.LEFT, font_name="Calibri"):
    txBox = slide.shapes.add_textbox(left, top, width, height)
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.font.name = font_name
    p.alignment = alignment
    return txBox


def add_bullet_text(text_frame, text, font_size=10, color=BLACK, bold=False, level=0,
                    space_before=Pt(2), space_after=Pt(2), font_name="Calibri"):
    p = text_frame.add_paragraph()
    p.text = text
    p.font.size = Pt(font_size)
    p.font.color.rgb = color
    p.font.bold = bold
    p.font.name = font_name
    p.level = level
    p.space_before = space_before
    p.space_after = space_after
    return p


# ============================================================
# SLIDE 1: Business Model & P&L Structure
# ============================================================
slide1 = prs.slides.add_slide(prs.slide_layouts[6])  # blank layout

# Background
add_shape(slide1, Inches(0), Inches(0), Inches(13.333), Inches(7.5), WHITE)

# Top header bar
add_shape(slide1, Inches(0), Inches(0), Inches(13.333), Inches(0.9), DARK_GREEN)
add_text_box(slide1, Inches(0.5), Inches(0.15), Inches(10), Inches(0.6),
             "Greenstone Financial Services | Business Model Deep Dive",
             font_size=22, bold=True, color=WHITE)
add_text_box(slide1, Inches(10.5), Inches(0.25), Inches(2.5), Inches(0.4),
             "Confidential | March 2026", font_size=10, color=RGBColor(0xA5, 0xD6, 0xA7),
             alignment=PP_ALIGN.RIGHT)

# --- Section 1: Company Overview (Left top) ---
box1 = add_rounded_rect(slide1, Inches(0.4), Inches(1.1), Inches(6.3), Inches(2.8), LIGHT_GRAY)
add_text_box(slide1, Inches(0.6), Inches(1.15), Inches(5), Inches(0.35),
             "Company Overview", font_size=13, bold=True, color=DARK_GREEN)

txBox = slide1.shapes.add_textbox(Inches(0.6), Inches(1.5), Inches(5.9), Inches(2.3))
tf = txBox.text_frame
tf.word_wrap = True
items = [
    ("Founded:", " 2007, Sydney, Australia (part of Hollard Insurance Group expansion)"),
    ("What it does:", " Australia & NZ's largest direct insurance distributor"),
    ("Business:", " Design, market, distribute & administer personal insurance products"),
    ("Products:", " Life, Funeral, Income Protection, Pet, Home, Car, Health, Travel, Landlords"),
    ("Geographies:", " Australia (core), New Zealand (2019), Canada (2023)"),
    ("Employees:", " ~800+"),
    ("Ownership:", " CDPQ (44%), OTPP (33.4%), HIBV/Hollard (remainder)"),
    ("Valuation:", " ~A$984M (2015 IPO attempt, aborted due to market conditions)"),
]
for i, (label, desc) in enumerate(items):
    p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
    run1 = p.add_run()
    run1.text = label
    run1.font.size = Pt(9)
    run1.font.bold = True
    run1.font.color.rgb = BLACK
    run1.font.name = "Calibri"
    run2 = p.add_run()
    run2.text = desc
    run2.font.size = Pt(9)
    run2.font.color.rgb = GRAY
    run2.font.name = "Calibri"
    p.space_before = Pt(2)
    p.space_after = Pt(1)

# --- Section 2: Business Model (Right top) ---
box2 = add_rounded_rect(slide1, Inches(6.85), Inches(1.1), Inches(6.1), Inches(2.8), LIGHT_GRAY)
add_text_box(slide1, Inches(7.05), Inches(1.15), Inches(5), Inches(0.35),
             "Business Model: Insurance Distribution Platform", font_size=13, bold=True, color=DARK_GREEN)

# Model flow diagram - simplified boxes
flow_items = [
    ("Underwriters\n(Hollard, Hannover\netc.)", RGBColor(0xBB, 0xDE, 0xFB)),
    ("Greenstone\nPlatform\n(Design/Distribute)", RGBColor(0xC8, 0xE6, 0xC9)),
    ("End Consumers\n(Direct-to-\nConsumer)", RGBColor(0xFF, 0xE0, 0xB2)),
]
x_start = Inches(7.1)
for i, (text, color) in enumerate(flow_items):
    bx = Inches(1.5)
    shape = add_rounded_rect(slide1, x_start + i * Inches(1.85), Inches(1.55),
                             Inches(1.6), Inches(0.85), color)
    shape.text_frame.word_wrap = True
    p = shape.text_frame.paragraphs[0]
    p.text = text
    p.font.size = Pt(7.5)
    p.font.bold = True
    p.font.color.rgb = BLACK
    p.font.name = "Calibri"
    p.alignment = PP_ALIGN.CENTER
    shape.text_frame.paragraphs[0].space_before = Pt(4)

# Arrow indicators
add_text_box(slide1, x_start + Inches(1.55), Inches(1.75), Inches(0.3), Inches(0.3),
             "→", font_size=18, bold=True, color=DARK_GREEN, alignment=PP_ALIGN.CENTER)
add_text_box(slide1, x_start + Inches(3.4), Inches(1.75), Inches(0.3), Inches(0.3),
             "→", font_size=18, bold=True, color=DARK_GREEN, alignment=PP_ALIGN.CENTER)

# Distribution channels
txBox2 = slide1.shapes.add_textbox(Inches(7.05), Inches(2.5), Inches(5.7), Inches(1.3))
tf2 = txBox2.text_frame
tf2.word_wrap = True
channels = [
    "Distribution Channels:",
    "• Proprietary Brands: Real Insurance, Australian Seniors, Guardian, Prime Pet",
    "• Affinity Partners: Medibank, Woolworths, RSPCA, Kogan, Guide Dogs",
    "• Comparison Platform: Choosi (online aggregator)",
    "",
    "Key: Greenstone does NOT bear underwriting risk — it earns commissions/fees",
    "from product design, marketing, distribution & policy administration"
]
for i, line in enumerate(channels):
    p = tf2.paragraphs[0] if i == 0 else tf2.add_paragraph()
    p.text = line
    p.font.size = Pt(8.5)
    p.font.name = "Calibri"
    p.font.color.rgb = BLACK if i > 0 else DARK_GREEN
    p.font.bold = (i == 0 or i == 5)
    p.space_before = Pt(1)
    p.space_after = Pt(1)

# --- Section 3: P&L Waterfall / Cost Structure (Bottom left) ---
box3 = add_rounded_rect(slide1, Inches(0.4), Inches(4.05), Inches(6.3), Inches(3.2), LIGHT_GRAY)
add_text_box(slide1, Inches(0.6), Inches(4.1), Inches(5), Inches(0.35),
             "P&L Structure & Cost Breakdown (Insurance Distributor Model)", font_size=13, bold=True, color=DARK_GREEN)

txBox3 = slide1.shapes.add_textbox(Inches(0.6), Inches(4.45), Inches(5.9), Inches(2.7))
tf3 = txBox3.text_frame
tf3.word_wrap = True

pnl_items = [
    ("Revenue (Commission & Fee Income)", "~A$500M estimated (D&B)", ACCENT_BLUE, True),
    ("  ├ Commission income: 20-52% of premiums over policy life", "", GRAY, False),
    ("  ├ Upfront commission: 40-100% of first-year premium (Life/Funeral)", "", GRAY, False),
    ("  ├ Renewal/trail commission: 3-5% annually on renewals", "", GRAY, False),
    ("  └ Administration & platform fees from affinity partners", "", GRAY, False),
    ("", "", BLACK, False),
    ("(-) Cost of Revenue / COGS", "", ACCENT_ORANGE, True),
    ("  ├ Customer acquisition cost (CAC): digital marketing, TV, direct mail", "", GRAY, False),
    ("  ├ Lead generation & performance marketing spend", "", GRAY, False),
    ("  └ Commissions paid to sub-agents / comparison platforms", "", GRAY, False),
    ("= Gross Profit  |  Typical margin: 50-70% for asset-light distributors", "", MED_GREEN, True),
    ("", "", BLACK, False),
    ("(-) SG&A (Operating Expenses)", "", ACCENT_ORANGE, True),
    ("  ├ People cost (~800 FTE): product design, tech, ops, compliance, mgmt", "", GRAY, False),
    ("  ├ Technology & platform: policy admin systems, CRM, data analytics", "", GRAY, False),
    ("  ├ Brand building & above-the-line marketing", "", GRAY, False),
    ("  ├ Rent, office, corporate overhead", "", GRAY, False),
    ("  └ Regulatory, compliance & licensing costs (ASIC, APRA)", "", GRAY, False),
    ("", "", BLACK, False),
    ("= EBITDA  |  Typical range: 20-30% for top insurance MGAs/distributors", "", DARK_GREEN, True),
    ("  (Industry avg: 15-20%;  Top performers: 25-30%+)", "", MED_GREEN, False),
]

for i, (text, note, color, bold) in enumerate(pnl_items):
    p = tf3.paragraphs[0] if i == 0 else tf3.add_paragraph()
    run = p.add_run()
    run.text = text
    run.font.size = Pt(8.5)
    run.font.color.rgb = color
    run.font.bold = bold
    run.font.name = "Calibri"
    if note:
        run2 = p.add_run()
        run2.text = f"  {note}"
        run2.font.size = Pt(8)
        run2.font.color.rgb = GRAY
        run2.font.italic = True
        run2.font.name = "Calibri"
    p.space_before = Pt(0.5)
    p.space_after = Pt(0.5)

# --- Section 4: Key Financials (Bottom right) ---
box4 = add_rounded_rect(slide1, Inches(6.85), Inches(4.05), Inches(6.1), Inches(3.2), LIGHT_GRAY)
add_text_box(slide1, Inches(7.05), Inches(4.1), Inches(5), Inches(0.35),
             "Key Financial Profile & Revenue Drivers", font_size=13, bold=True, color=DARK_GREEN)

txBox4 = slide1.shapes.add_textbox(Inches(7.05), Inches(4.45), Inches(5.7), Inches(1.2))
tf4 = txBox4.text_frame
tf4.word_wrap = True

metrics = [
    ("Estimated Revenue:", "~A$500M (Dun & Bradstreet); ~A$139M (RocketReach est. 2026)"),
    ("IPO Valuation (2015):", "A$810M - A$984M (aborted)"),
    ("Revenue Model:", "Commission-based, asset-light (no underwriting risk)"),
    ("Revenue Quality:", "High recurring revenue from renewal/trail commissions"),
    ("Key Metric:", "Policies in-force × Average commission per policy"),
]
for i, (label, value) in enumerate(metrics):
    p = tf4.paragraphs[0] if i == 0 else tf4.add_paragraph()
    r1 = p.add_run()
    r1.text = label + " "
    r1.font.size = Pt(9)
    r1.font.bold = True
    r1.font.color.rgb = BLACK
    r1.font.name = "Calibri"
    r2 = p.add_run()
    r2.text = value
    r2.font.size = Pt(9)
    r2.font.color.rgb = GRAY
    r2.font.name = "Calibri"
    p.space_before = Pt(2)
    p.space_after = Pt(1)

# Revenue drivers section
add_text_box(slide1, Inches(7.05), Inches(5.7), Inches(5), Inches(0.3),
             "What Drives Profitability:", font_size=10, bold=True, color=DARK_GREEN)

txBox5 = slide1.shapes.add_textbox(Inches(7.05), Inches(5.95), Inches(5.7), Inches(1.2))
tf5 = txBox5.text_frame
tf5.word_wrap = True
drivers = [
    "1. Policy volume growth (new customer acquisition efficiency)",
    "2. Retention rate (renewals = high-margin recurring revenue with minimal CAC)",
    "3. Cross-sell / upsell across product lines (Life → Home → Car → Pet)",
    "4. Affinity partner pipeline expansion (branded insurance for retailers/brands)",
    "5. Geographic expansion leverage (NZ/Canada replicating AU playbook)",
    "6. Operating leverage: platform costs largely fixed → scale drives margin expansion",
]
for i, text in enumerate(drivers):
    p = tf5.paragraphs[0] if i == 0 else tf5.add_paragraph()
    p.text = text
    p.font.size = Pt(8.5)
    p.font.color.rgb = BLACK
    p.font.name = "Calibri"
    p.space_before = Pt(1)
    p.space_after = Pt(1)

# ============================================================
# SLIDE 2: Industry, Competitors & Competitive Advantages
# ============================================================
slide2 = prs.slides.add_slide(prs.slide_layouts[6])

# Background
add_shape(slide2, Inches(0), Inches(0), Inches(13.333), Inches(7.5), WHITE)

# Top header bar
add_shape(slide2, Inches(0), Inches(0), Inches(13.333), Inches(0.9), DARK_GREEN)
add_text_box(slide2, Inches(0.5), Inches(0.15), Inches(10), Inches(0.6),
             "Greenstone Financial Services | Industry, Competition & Moat",
             font_size=22, bold=True, color=WHITE)
add_text_box(slide2, Inches(10.5), Inches(0.25), Inches(2.5), Inches(0.4),
             "Confidential | March 2026", font_size=10, color=RGBColor(0xA5, 0xD6, 0xA7),
             alignment=PP_ALIGN.RIGHT)

# --- Section 1: Industry Overview (Left top) ---
box5 = add_rounded_rect(slide2, Inches(0.4), Inches(1.1), Inches(6.3), Inches(2.6), LIGHT_GRAY)
add_text_box(slide2, Inches(0.6), Inches(1.15), Inches(5), Inches(0.35),
             "Industry Overview & Market Trends", font_size=13, bold=True, color=DARK_GREEN)

txBox6 = slide2.shapes.add_textbox(Inches(0.6), Inches(1.5), Inches(5.9), Inches(2.1))
tf6 = txBox6.text_frame
tf6.word_wrap = True

industry_items = [
    ("Market Size:", " Australia total insurance market: US$50.9B (2024) → US$84.7B (2033E), CAGR 5.4%"),
    ("General Insurance:", " US$18.1B (2024) → US$33.0B (2033E), CAGR 6.9%"),
    ("Aggregator Market:", " Global insurance aggregators: US$35.7B (2024) → US$103B (2029E), CAGR 23.4%"),
    ("", ""),
    ("Key Trends:", ""),
    ("  1.", " Digital shift: Online/digital is the fastest growing channel (4.67% CAGR in AU)"),
    ("  2.", " Embedded insurance: Cover bundled into retail/e-commerce transactions"),
    ("  3.", " Data & AI: Personalized pricing, automated underwriting, chatbot servicing"),
    ("  4.", " Regulatory tightening: ASIC scrutiny on comparison sites (Choosi case)"),
    ("  5.", " Climate risk: Increasing natural catastrophe losses driving premium inflation"),
    ("  6.", " Consolidation: Compare the Market acquired iSelect (A$72M); PE/pension fund activity"),
]
for i, (label, desc) in enumerate(industry_items):
    p = tf6.paragraphs[0] if i == 0 else tf6.add_paragraph()
    r1 = p.add_run()
    r1.text = label
    r1.font.size = Pt(9)
    r1.font.bold = True
    r1.font.color.rgb = DARK_GREEN if "Trends" in label else BLACK
    r1.font.name = "Calibri"
    r2 = p.add_run()
    r2.text = desc
    r2.font.size = Pt(9)
    r2.font.color.rgb = GRAY
    r2.font.name = "Calibri"
    p.space_before = Pt(1)
    p.space_after = Pt(0.5)

# --- Section 2: Competitive Landscape (Right top) ---
box6 = add_rounded_rect(slide2, Inches(6.85), Inches(1.1), Inches(6.1), Inches(2.6), LIGHT_GRAY)
add_text_box(slide2, Inches(7.05), Inches(1.15), Inches(5), Inches(0.35),
             "Competitive Landscape", font_size=13, bold=True, color=DARK_GREEN)

# Table-like competitor comparison
headers = ["Player", "Type", "Key Brands", "Notes"]
col_widths = [Inches(1.3), Inches(1.2), Inches(1.8), Inches(1.5)]
x_start = Inches(7.1)
y_start = Inches(1.55)

# Header row
for j, (hdr, w) in enumerate(zip(headers, col_widths)):
    x = x_start + sum(cw for cw in [Inches(0)] + [col_widths[k] for k in range(j)])
    add_text_box(slide2, x, y_start, w, Inches(0.25),
                 hdr, font_size=8, bold=True, color=WHITE)
    add_shape(slide2, x, y_start, w, Inches(0.25), MED_GREEN)
    add_text_box(slide2, x, y_start, w, Inches(0.25),
                 hdr, font_size=8, bold=True, color=WHITE, alignment=PP_ALIGN.CENTER)

competitors = [
    ("Greenstone", "Direct Distributor", "Real, Seniors, Choosi", "Largest DTC in AU/NZ"),
    ("Compare the\nMarket / iSelect", "Aggregator", "CTM, iSelect", "Owned by IHA (SA);\nacquired iSelect A$72M"),
    ("Auto & General\n(Budget Direct)", "Underwriter +\nDistributor", "Budget Direct, Virgin", "Vertically integrated;\nalso IHA group"),
    ("IAG", "Major Insurer", "NRMA, CGU, SGIO", "Largest AU general\ninsurer; direct + broker"),
    ("Suncorp", "Major Insurer", "AAMI, GIO, Apia", "2nd largest; strong\nbrand portfolio"),
    ("NobleOak /\nIntegrity Life", "Direct Life\nInsurer", "NobleOak, Integrity", "Direct life insurance\nspecialists"),
]

for i, (name, typ, brands, notes) in enumerate(competitors):
    y = y_start + Inches(0.28) + i * Inches(0.32)
    row_color = WHITE if i % 2 == 0 else LIGHT_GREEN
    vals = [name, typ, brands, notes]
    for j, (val, w) in enumerate(zip(vals, col_widths)):
        x = x_start + sum(cw for cw in [Inches(0)] + [col_widths[k] for k in range(j)])
        add_shape(slide2, x, y, w, Inches(0.32), row_color)
        tb = add_text_box(slide2, x, y, w, Inches(0.32),
                          val, font_size=7, color=BLACK, alignment=PP_ALIGN.CENTER)
        tb.text_frame.paragraphs[0].font.bold = (j == 0)

# --- Section 3: Core Competitive Advantages / Moat (Bottom left) ---
box7 = add_rounded_rect(slide2, Inches(0.4), Inches(3.85), Inches(6.3), Inches(3.4), LIGHT_GRAY)
add_text_box(slide2, Inches(0.6), Inches(3.9), Inches(5), Inches(0.35),
             "Core Competitive Advantages (Moat)", font_size=13, bold=True, color=DARK_GREEN)

txBox7 = slide2.shapes.add_textbox(Inches(0.6), Inches(4.25), Inches(5.9), Inches(2.9))
tf7 = txBox7.text_frame
tf7.word_wrap = True

moat_items = [
    ("1. Multi-Brand Distribution Platform",
     "Operates 6+ proprietary brands + multiple affinity partnerships, creating diversified "
     "customer acquisition channels. Unlike single-brand insurers, Greenstone can target "
     "different demographics (seniors, young families, pet owners) through purpose-built brands."),
    ("2. Asset-Light Model (No Underwriting Risk)",
     "Pure distributor model — earns commissions without bearing claims risk. This results in "
     "more predictable earnings, lower capital requirements, and higher ROE vs. traditional insurers."),
    ("3. Data & Analytics Capability",
     "15+ years of direct insurance data across millions of policies. Proprietary data on customer "
     "acquisition costs, lifetime value, and retention by product/channel enables precision marketing "
     "and product design — a significant barrier to entry."),
    ("4. Recurring Revenue Base",
     "Renewal/trail commissions create a 'book' of recurring revenue. As policies renew, "
     "commission income flows with near-zero incremental cost — driving operating leverage."),
    ("5. Proven International Expansion Playbook",
     "Successfully replicated AU model in NZ (2019) and Canada (2023), demonstrating that the "
     "platform, technology, and expertise are transferable to new geographies."),
    ("6. Strong Institutional Backing",
     "CDPQ + OTPP ownership provides patient capital, governance standards, and credibility "
     "for partnerships. These are among the world's most sophisticated infrastructure/PE investors."),
]

for i, (title, desc) in enumerate(moat_items):
    p = tf7.paragraphs[0] if i == 0 else tf7.add_paragraph()
    r1 = p.add_run()
    r1.text = title + ": "
    r1.font.size = Pt(9)
    r1.font.bold = True
    r1.font.color.rgb = ACCENT_BLUE
    r1.font.name = "Calibri"
    r2 = p.add_run()
    r2.text = desc
    r2.font.size = Pt(8)
    r2.font.color.rgb = GRAY
    r2.font.name = "Calibri"
    p.space_before = Pt(3)
    p.space_after = Pt(2)

# --- Section 4: Key Risks & Considerations (Bottom right) ---
box8 = add_rounded_rect(slide2, Inches(6.85), Inches(3.85), Inches(6.1), Inches(3.4), LIGHT_GRAY)
add_text_box(slide2, Inches(7.05), Inches(3.9), Inches(5), Inches(0.35),
             "Key Risks & Investment Considerations", font_size=13, bold=True, color=DARK_GREEN)

txBox8 = slide2.shapes.add_textbox(Inches(7.05), Inches(4.25), Inches(5.7), Inches(1.5))
tf8 = txBox8.text_frame
tf8.word_wrap = True

risks = [
    ("Regulatory Risk:", " ASIC alleged Choosi received A$61M while steering customers to single "
     "underwriter (Hannover). Comparison site business model under scrutiny — potential "
     "requirement for greater transparency and reduced commissions."),
    ("Underwriter Concentration:", " Heavy reliance on Hollard as primary underwriting partner. "
     "Loss of key underwriter relationship would significantly impact operations."),
    ("Competition:", " Consolidation (CTM + iSelect) and vertical integration by large insurers "
     "(IAG, Suncorp going direct) threaten market share. Low switching costs for consumers."),
    ("Customer Acquisition Cost:", " Digital marketing costs rising (Google, Meta). "
     "TV/above-the-line advertising required for brand building is expensive and hard to measure."),
    ("Growth Risks:", " NZ and Canada expansion requires upfront investment with uncertain payback. "
     "New market dynamics, regulation, and competitive landscapes differ from AU."),
]

for i, (label, desc) in enumerate(risks):
    p = tf8.paragraphs[0] if i == 0 else tf8.add_paragraph()
    r1 = p.add_run()
    r1.text = label
    r1.font.size = Pt(9)
    r1.font.bold = True
    r1.font.color.rgb = ACCENT_ORANGE
    r1.font.name = "Calibri"
    r2 = p.add_run()
    r2.text = desc
    r2.font.size = Pt(8)
    r2.font.color.rgb = GRAY
    r2.font.name = "Calibri"
    p.space_before = Pt(3)
    p.space_after = Pt(2)

# Valuation context box
add_text_box(slide2, Inches(7.05), Inches(5.95), Inches(5), Inches(0.3),
             "Valuation Context:", font_size=10, bold=True, color=DARK_GREEN)

txBox9 = slide2.shapes.add_textbox(Inches(7.05), Inches(6.2), Inches(5.7), Inches(0.9))
tf9 = txBox9.text_frame
tf9.word_wrap = True

val_items = [
    "• Insurance distributor/MGA comps trade at 5-7x EBITDA (wholesale); 8-12x (retail/direct)",
    "• 2015 IPO attempt implied ~A$984M valuation; current value likely higher given expansion",
    "• Key value driver: Quality of recurring commission book + growth optionality (NZ/Canada)",
    "• Comparable transactions: Compare the Market/iSelect (A$72M for iSelect alone)",
]
for i, text in enumerate(val_items):
    p = tf9.paragraphs[0] if i == 0 else tf9.add_paragraph()
    p.text = text
    p.font.size = Pt(8.5)
    p.font.color.rgb = BLACK
    p.font.name = "Calibri"
    p.space_before = Pt(1)
    p.space_after = Pt(1)

# Save
output_path = "/home/user/cosmo_1/Greenstone_Financial_Services_Overview.pptx"
prs.save(output_path)
print(f"PPT saved to: {output_path}")
