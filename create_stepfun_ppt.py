#!/usr/bin/env python3
"""Generate StepFun (阶跃星辰) Fundraising & Competitive Benchmarking slide."""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION
from pptx.chart.data import CategoryChartData

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# ── Color scheme (dark navy tech theme) ──
DARK_NAVY = RGBColor(0x0D, 0x1B, 0x3E)
MED_BLUE = RGBColor(0x15, 0x65, 0xC0)
LIGHT_BLUE = RGBColor(0xE3, 0xF2, 0xFD)
ACCENT_RED = RGBColor(0xC6, 0x28, 0x28)
ACCENT_GREEN = RGBColor(0x2E, 0x7D, 0x32)
ACCENT_ORANGE = RGBColor(0xE6, 0x51, 0x00)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
BLACK = RGBColor(0x33, 0x33, 0x33)
GRAY = RGBColor(0x66, 0x66, 0x66)
LIGHT_GRAY = RGBColor(0xF5, 0xF5, 0xF5)
VERY_LIGHT_GRAY = RGBColor(0xFA, 0xFA, 0xFA)

# Chart colors
CHART_TOTAL_RAISED = RGBColor(0x1A, 0x23, 0x7E)   # indigo - Total Raised
CHART_CASH_ON_HAND = RGBColor(0x2E, 0x7D, 0x32)   # green  - Cash on Hand
CHART_ANNUAL_BURN = RGBColor(0xE6, 0x51, 0x00)     # orange - Annual Burn


# ── Helper functions ──
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


def add_rounded_rect(slide, left, top, width, height, fill_color, line_color=None):
    shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if line_color:
        shape.line.color.rgb = line_color
    else:
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


def add_table(slide, left, top, width, height, rows, cols):
    table_shape = slide.shapes.add_table(rows, cols, left, top, width, height)
    return table_shape.table


def style_cell(cell, text, font_size=8, bold=False, color=BLACK, fill=None,
               alignment=PP_ALIGN.CENTER, font_name="Calibri"):
    cell.text = ""
    p = cell.text_frame.paragraphs[0]
    p.text = text
    p.font.size = Pt(font_size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.font.name = font_name
    p.alignment = alignment
    cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    if fill:
        cell.fill.solid()
        cell.fill.fore_color.rgb = fill


def style_chart_series(chart, series_idx, color_rgb):
    """Set fill color for a chart series."""
    series = chart.series[series_idx]
    series.format.fill.solid()
    series.format.fill.fore_color.rgb = color_rgb


# ============================================================
# SLIDE 1: StepFun Fundraising Track Record & Benchmarking
# ============================================================
slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank layout

# Background
add_shape(slide, Inches(0), Inches(0), Inches(13.333), Inches(7.5), WHITE)

# ── Top header bar ──
add_shape(slide, Inches(0), Inches(0), Inches(13.333), Inches(0.85), DARK_NAVY)
add_text_box(slide, Inches(0.5), Inches(0.12), Inches(10), Inches(0.6),
             "StepFun (阶跃星辰) | Fundraising Track Record & Competitive Benchmarking",
             font_size=21, bold=True, color=WHITE)
add_text_box(slide, Inches(10.5), Inches(0.22), Inches(2.5), Inches(0.4),
             "Confidential | April 2026", font_size=10,
             color=RGBColor(0x90, 0xCA, 0xF9), alignment=PP_ALIGN.RIGHT)


# ============================================================
# TOP LEFT: StepFun Fundraising History Table
# ============================================================
section_top = Inches(1.0)

# Section header
add_text_box(slide, Inches(0.4), section_top, Inches(5), Inches(0.3),
             "融资历史 Fundraising History", font_size=12, bold=True, color=DARK_NAVY)

# Fundraising table
table_top = section_top + Inches(0.35)
tbl = add_table(slide, Inches(0.4), table_top, Inches(7.2), Inches(2.1), 8, 6)

# Column widths
col_widths = [Inches(0.45), Inches(0.9), Inches(0.7), Inches(1.05), Inches(0.9), Inches(3.2)]
for i, w in enumerate(col_widths):
    tbl.columns[i].width = w

# Header row
headers = ["#", "日期", "轮次", "投前估值($)", "融资额($)", "主要投资人"]
for j, h in enumerate(headers):
    style_cell(tbl.cell(0, j), h, font_size=7.5, bold=True, color=WHITE,
               fill=DARK_NAVY, alignment=PP_ALIGN.CENTER)

# Data rows
data = [
    ["1", "2023.06", "A轮",  "$7亿",   "$1.7亿", "红杉、启明、滨柏"],
    ["2", "2024.04", "A+轮", "$11.4亿", "$1.1亿", "五源、联想、众源、顺为等"],
    ["3", "2024.12", "B轮",  "$20亿",   "$2.3亿", "HKIC、腾讯、无锡、上海国投+华腾等"],
    ["4", "2025.12", "B+轮", "$26亿",   "$7.7亿", "浦东创投、徐汇资本、国投先导、华勤、上海仪电集团等"],
    ["5", "2026.03", "B3轮", "$40亿",   "$5.0亿", "3W Fund、华勤、亦庄国投、长三角数文、龙旗、豪威、上汽等"],
    ["6", "2026.04", "B4轮", "$60亿",   "交割中",  "—"],
]

for i, row in enumerate(data):
    row_fill = VERY_LIGHT_GRAY if i % 2 == 0 else WHITE
    # Highlight B3/B4 rows
    if i >= 4:
        row_fill = LIGHT_BLUE
    for j, val in enumerate(row):
        align = PP_ALIGN.CENTER if j < 5 else PP_ALIGN.LEFT
        style_cell(tbl.cell(i + 1, j), val, font_size=7, bold=(j == 0),
                   color=BLACK, fill=row_fill, alignment=align)

# Total row indicator
add_text_box(slide, Inches(0.4), table_top + Inches(2.15), Inches(7.2), Inches(0.2),
             "累计融资 ~$17.8亿 (不含B4) | 估值增长: $7亿 → $60亿 (8.6x, <3年)",
             font_size=8, bold=True, color=MED_BLUE)


# ============================================================
# TOP RIGHT: Key Highlights & Ownership
# ============================================================
right_x = Inches(7.85)

add_text_box(slide, right_x, section_top, Inches(5), Inches(0.3),
             "核心指标 Key Highlights", font_size=12, bold=True, color=DARK_NAVY)

# Highlights box
box_top = section_top + Inches(0.35)
highlight_box = add_rounded_rect(slide, right_x, box_top, Inches(5.1), Inches(1.15),
                                 VERY_LIGHT_GRAY, line_color=RGBColor(0xCC, 0xCC, 0xCC))

txBox = slide.shapes.add_textbox(right_x + Inches(0.15), box_top + Inches(0.05),
                                 Inches(4.8), Inches(1.05))
tf = txBox.text_frame
tf.word_wrap = True

highlights = [
    ("累计融资:", " ~$17.8亿 (不含B4交割)"),
    ("最新估值:", " $60亿 (B4轮投前)  |  3年增长 8.6x"),
    ("创始人:", " 姜大昕 (前微软全球副总裁)"),
    ("成立时间:", " 2023年4月，上海"),
    ("IPO计划:", " 筹划港股上市，或融~$5亿 (Bloomberg 2月报道)"),
]
for i, (label, desc) in enumerate(highlights):
    p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
    r1 = p.add_run()
    r1.text = label
    r1.font.size = Pt(8.5)
    r1.font.bold = True
    r1.font.color.rgb = DARK_NAVY
    r1.font.name = "Calibri"
    r2 = p.add_run()
    r2.text = desc
    r2.font.size = Pt(8.5)
    r2.font.color.rgb = GRAY
    r2.font.name = "Calibri"
    p.space_before = Pt(1)
    p.space_after = Pt(0.5)

# Ownership structure mini-table
own_top = box_top + Inches(1.25)
add_text_box(slide, right_x, own_top, Inches(5), Inches(0.25),
             "股权结构 (B3轮后)", font_size=9, bold=True, color=DARK_NAVY)

own_tbl = add_table(slide, right_x, own_top + Inches(0.25), Inches(5.1), Inches(1.0), 4, 6)

own_col_widths = [Inches(0.85), Inches(0.85), Inches(0.85), Inches(0.85), Inches(0.85), Inches(0.85)]
for i, w in enumerate(own_col_widths):
    own_tbl.columns[i].width = w

# Header
own_headers = ["公司团队", "ESOP", "上海仪电", "红杉", "启明", "其他"]
own_values = ["24.8%", "16.2%", "7.6%", "7.2%", "3.6%", "40.6%"]
own_notes = ["", "", "", "(不含HKIC)", "", "(含HKIC 3.1%)"]
for j, h in enumerate(own_headers):
    style_cell(own_tbl.cell(0, j), h, font_size=7, bold=True, color=WHITE, fill=DARK_NAVY)
for j, v in enumerate(own_values):
    style_cell(own_tbl.cell(1, j), v, font_size=8.5, bold=True,
               color=MED_BLUE if j == 0 else BLACK, fill=WHITE)
for j, n in enumerate(own_notes):
    style_cell(own_tbl.cell(2, j), n, font_size=6, color=GRAY, fill=WHITE)

# Summary row
style_cell(own_tbl.cell(3, 0), "团队合计持股 41%", font_size=7, bold=True,
           color=ACCENT_GREEN, fill=LIGHT_BLUE, alignment=PP_ALIGN.CENTER)
# Merge-like: put text spanning conceptually
style_cell(own_tbl.cell(3, 1), "", font_size=7, fill=LIGHT_BLUE)
style_cell(own_tbl.cell(3, 2), "外部股东 59%", font_size=7, bold=True,
           color=GRAY, fill=LIGHT_BLUE)
style_cell(own_tbl.cell(3, 3), "", font_size=7, fill=LIGHT_BLUE)
style_cell(own_tbl.cell(3, 4), "董事长表决权 35%", font_size=7, bold=True,
           color=ACCENT_RED, fill=LIGHT_BLUE)
style_cell(own_tbl.cell(3, 5), "", font_size=7, fill=LIGHT_BLUE)


# ============================================================
# BOTTOM SECTION: Competitive Benchmarking Charts
# ============================================================
chart_section_top = Inches(3.75)

add_text_box(slide, Inches(0.4), chart_section_top, Inches(8), Inches(0.3),
             "同业对标 Competitive Benchmarking — 融资总额 / 账上现金 / 年化消耗",
             font_size=12, bold=True, color=DARK_NAVY)

# Thin separator line
add_shape(slide, Inches(0.4), chart_section_top + Inches(0.28), Inches(12.5), Inches(0.02), MED_BLUE)

# ── LEFT CHART: Chinese AI Startups ──
chart_top = chart_section_top + Inches(0.4)

add_text_box(slide, Inches(0.4), chart_top, Inches(4), Inches(0.25),
             "中国 AI 创业公司 (单位: $B)", font_size=9, bold=True, color=MED_BLUE)

chart_data_cn = CategoryChartData()
chart_data_cn.categories = ["StepFun\n阶跃星辰", "MiniMax", "Zhipu AI\n智谱", "DeepSeek\n深度求索", "Moonshot\nKimi"]

# Values in $B
chart_data_cn.add_series("Total Raised 累计融资",  [1.78, 1.70, 2.00, 1.60, 2.97])
chart_data_cn.add_series("Cash on Hand 账上现金",   [0.90, 0.70, 0.65, 99,   1.75])  # DeepSeek=99 as marker
chart_data_cn.add_series("Annual Burn 年化消耗",    [0.35, 0.65, 0.66, 0.75, 0.50])

cn_chart_shape = slide.shapes.add_chart(
    XL_CHART_TYPE.COLUMN_CLUSTERED,
    Inches(0.3), chart_top + Inches(0.25),
    Inches(7.0), Inches(3.0),
    chart_data_cn
)
cn_chart = cn_chart_shape.chart

# Style Chinese chart
cn_chart.has_legend = True
cn_chart.legend.position = XL_LEGEND_POSITION.BOTTOM
cn_chart.legend.include_in_layout = False
cn_chart.legend.font.size = Pt(7)

# Color the series
style_chart_series(cn_chart, 0, CHART_TOTAL_RAISED)
style_chart_series(cn_chart, 1, CHART_CASH_ON_HAND)
style_chart_series(cn_chart, 2, CHART_ANNUAL_BURN)

# Y-axis formatting
value_axis = cn_chart.value_axis
value_axis.maximum_scale = 4.0
value_axis.minimum_scale = 0
value_axis.major_unit = 1.0
value_axis.has_title = False
value_axis.tick_labels.font.size = Pt(7)
value_axis.tick_labels.number_format = '$#,##0.0"B"'

# Category axis
cat_axis = cn_chart.category_axis
cat_axis.tick_labels.font.size = Pt(7)
cat_axis.has_major_gridlines = False

# Add data labels for the series
for i in range(3):
    plot = cn_chart.plots[0]
    series = plot.series[i]
    series.has_data_labels = True
    data_labels = series.data_labels
    data_labels.font.size = Pt(6)
    data_labels.number_format = '$#,##0.0"B"'
    data_labels.show_value = True

# DeepSeek annotation
add_text_box(slide, Inches(4.15), chart_top + Inches(0.55), Inches(1.4), Inches(0.5),
             "* DeepSeek 账上现金\n实质无限 (母公司\n幻方量化 AUM $13B,\n2025收益率57%)",
             font_size=5.5, color=GRAY)


# ── RIGHT CHART: US Frontier Labs ──
add_text_box(slide, Inches(7.6), chart_top, Inches(4), Inches(0.25),
             "美国前沿实验室 (单位: $B)", font_size=9, bold=True, color=MED_BLUE)

chart_data_us = CategoryChartData()
chart_data_us.categories = ["OpenAI", "Anthropic"]

chart_data_us.add_series("Total Raised 累计融资",  [168.0, 67.3])
chart_data_us.add_series("Cash on Hand 账上现金",   [70.0,  35.0])
chart_data_us.add_series("Annual Burn 年化消耗",    [25.0,   5.0])

us_chart_shape = slide.shapes.add_chart(
    XL_CHART_TYPE.COLUMN_CLUSTERED,
    Inches(7.5), chart_top + Inches(0.25),
    Inches(5.5), Inches(3.0),
    chart_data_us
)
us_chart = us_chart_shape.chart

# Style US chart
us_chart.has_legend = True
us_chart.legend.position = XL_LEGEND_POSITION.BOTTOM
us_chart.legend.include_in_layout = False
us_chart.legend.font.size = Pt(7)

style_chart_series(us_chart, 0, CHART_TOTAL_RAISED)
style_chart_series(us_chart, 1, CHART_CASH_ON_HAND)
style_chart_series(us_chart, 2, CHART_ANNUAL_BURN)

# Y-axis
us_value_axis = us_chart.value_axis
us_value_axis.maximum_scale = 180.0
us_value_axis.minimum_scale = 0
us_value_axis.major_unit = 30.0
us_value_axis.has_title = False
us_value_axis.tick_labels.font.size = Pt(7)
us_value_axis.tick_labels.number_format = '$#,##0"B"'

# Category axis
us_cat_axis = us_chart.category_axis
us_cat_axis.tick_labels.font.size = Pt(8)
us_cat_axis.has_major_gridlines = False

# Data labels
for i in range(3):
    series = us_chart.plots[0].series[i]
    series.has_data_labels = True
    data_labels = series.data_labels
    data_labels.font.size = Pt(7)
    data_labels.number_format = '$#,##0"B"'
    data_labels.show_value = True


# ── KEY TAKEAWAYS callout box ──
callout_top = Inches(7.05)
callout_box = add_rounded_rect(slide, Inches(0.4), callout_top, Inches(12.5), Inches(0.35),
                                RGBColor(0xFD, 0xF0, 0xE0),
                                line_color=ACCENT_ORANGE)
txBox_callout = slide.shapes.add_textbox(Inches(0.55), callout_top + Inches(0.02),
                                         Inches(12.2), Inches(0.3))
tf_c = txBox_callout.text_frame
tf_c.word_wrap = True
p = tf_c.paragraphs[0]
r1 = p.add_run()
r1.text = "Key Takeaway: "
r1.font.size = Pt(7.5)
r1.font.bold = True
r1.font.color.rgb = ACCENT_ORANGE
r1.font.name = "Calibri"
r2 = p.add_run()
r2.text = ("StepFun累计融资$17.8亿，位列中国四小龙前列 | "
           "中国AI创业公司融资$1-3B vs 美国前沿实验室$67-168B，差距50-100x | "
           "MiniMax/智谱IPO后仅12-18个月runway; Moonshot/StepFun约3年 | "
           "现金消耗是核心生存指标")
r2.font.size = Pt(7.5)
r2.font.color.rgb = BLACK
r2.font.name = "Calibri"
p.alignment = PP_ALIGN.LEFT


# ── Footer / Source ──
add_text_box(slide, Inches(0.4), Inches(7.25), Inches(12), Inches(0.2),
             "Sources: Caixin, CNBC, TechCrunch, Bloomberg, SCMP, Tracxn, PitchBook, company filings | "
             "注: 现金及消耗率为估算值; DeepSeek为母公司幻方量化自主注资; OpenAI Series G含大量非现金承诺(GPU credits等)",
             font_size=5.5, color=GRAY)


# Save
output_path = "/home/user/cosmo_1/StepFun_Fundraising_Benchmarking.pptx"
prs.save(output_path)
print(f"PPT saved to: {output_path}")
