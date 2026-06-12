#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convert Chinese research-report Markdown -> styled HTML -> PDF (WeasyPrint, CJK font).

Usage:
    python3 build_report_pdf.py [file1.md file2.md ...]
If no args are given, it builds the two logistics reports in this repo.
"""
import markdown, pathlib, sys

DEFAULTS = [
    "全球物流行业商业模式与估值研究报告.md",
    "轻资产vs重资产3PL_与Logisteed重估分析.md",
]

CSS = """
@page { size: A4; margin: 1.5cm 1.5cm 1.8cm 1.5cm;
        @bottom-center { content: "第 " counter(page) " 页 / 共 " counter(pages) " 页";
                          font-size: 8pt; color: #999; } }
body { font-family: 'WenQuanYi Zen Hei', 'IPAGothic', sans-serif;
       font-size: 10.5pt; line-height: 1.55; color: #1a1a1a; margin: 0; }
h1, h2, h3, h4 { page-break-after: avoid; }
tr, blockquote, pre { page-break-inside: avoid; }
table { page-break-inside: auto; }
h1 { font-size: 20pt; color: #0b3d66; border-bottom: 3px solid #0b3d66;
     padding-bottom: 6px; margin-top: 18px; }
h2 { font-size: 15.5pt; color: #0b3d66; border-bottom: 1.5px solid #9bbcd6;
     padding-bottom: 4px; margin-top: 22px; }
h3 { font-size: 13pt; color: #114a7a; margin-top: 16px; }
h4 { font-size: 11.5pt; color: #1c5a8f; margin-top: 12px; }
p  { margin: 6px 0; }
strong { color: #b3261e; }
a { color: #0b5cab; text-decoration: none; }
code { font-family: 'WenQuanYi Zen Hei Mono', monospace; background: #f2f4f7;
       padding: 1px 4px; border-radius: 3px; font-size: 9.5pt; }
pre { background: #f2f4f7; border: 1px solid #d6dbe1; border-radius: 5px;
      padding: 10px; font-size: 9pt; line-height: 1.4; white-space: pre-wrap; }
pre code { background: none; padding: 0; }
blockquote { border-left: 4px solid #f0a202; background: #fff8e8;
             margin: 10px 0; padding: 8px 14px; color: #5a4a1a; }
table { border-collapse: collapse; width: 100%; margin: 12px 0; font-size: 9pt; }
th, td { border: 1px solid #b9c2cc; padding: 5px 7px; text-align: left; vertical-align: top; }
th { background: #0b3d66; color: #ffffff; font-weight: bold; }
tr:nth-child(even) td { background: #f5f8fb; }
hr { border: none; border-top: 1px solid #cdd5dd; margin: 18px 0; }
ul, ol { margin: 6px 0 6px 22px; }
li { margin: 3px 0; }
"""

def build(md_path: str):
    src = pathlib.Path(md_path)
    body = markdown.markdown(
        src.read_text(encoding="utf-8"),
        extensions=["tables", "fenced_code", "sane_lists", "toc", "attr_list"],
        output_format="html5",
    )
    doc = (f'<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">'
           f"<title>{src.stem}</title><style>{CSS}</style></head><body>{body}</body></html>")
    from weasyprint import HTML
    pdf = str(src.with_suffix(".pdf"))
    HTML(string=doc).write_pdf(pdf)
    print("PDF written:", pdf)

if __name__ == "__main__":
    targets = sys.argv[1:] or DEFAULTS
    for t in targets:
        build(t)
