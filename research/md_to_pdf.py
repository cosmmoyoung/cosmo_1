#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convert the embodied-AI report Markdown to a styled PDF with CJK support."""
import re
import markdown
from weasyprint import HTML, CSS

SRC = "/home/user/cosmo_1/具身智能行业全景研究报告.md"
OUT = "/home/user/cosmo_1/具身智能行业全景研究报告.pdf"

with open(SRC, encoding="utf-8") as f:
    md_text = f.read()

# Drop the markdown TOC anchor spans (<a name=...>) — WeasyPrint handles them fine,
# but we convert in-page links to plain text by leaving them; markdown handles anchors.
html_body = markdown.markdown(
    md_text,
    extensions=["tables", "fenced_code", "toc", "sane_lists", "attr_list"],
)

html_doc = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"></head>
<body>{html_body}</body></html>"""

css = CSS(string="""
@page {
    size: A4;
    margin: 18mm 16mm 20mm 16mm;
    @bottom-center {
        content: "具身智能行业全景研究报告  ·  第 " counter(page) " 页 / 共 " counter(pages) " 页";
        font-family: "WenQuanYi Zen Hei"; font-size: 8pt; color: #888;
    }
}
* { font-family: "WenQuanYi Zen Hei", "WenQuanYi Zen Hei Sharp", sans-serif; }
body { font-size: 10.5pt; line-height: 1.65; color: #1a1a1a; }
h1 { font-size: 20pt; color: #0b3d66; border-bottom: 3px solid #0b3d66;
     padding-bottom: 8px; margin-top: 6px; line-height: 1.35; }
h2 { font-size: 15pt; color: #0b4f8a; border-bottom: 1px solid #c9ddef;
     padding-bottom: 5px; margin-top: 22px; page-break-after: avoid; }
h3 { font-size: 12.5pt; color: #14618f; margin-top: 16px; page-break-after: avoid; }
h4 { font-size: 11pt; color: #2c3e50; margin-top: 12px; page-break-after: avoid; }
p { margin: 6px 0; text-align: justify; }
a { color: #1a6fb5; text-decoration: none; word-break: break-all; }
strong { color: #b3261e; }
ul, ol { margin: 6px 0 6px 0; padding-left: 22px; }
li { margin: 3px 0; }
blockquote { background: #f3f7fb; border-left: 4px solid #5b9bd5;
    margin: 10px 0; padding: 8px 14px; color: #333; border-radius: 3px; }
blockquote p { margin: 4px 0; }
table { border-collapse: collapse; width: 100%; margin: 10px 0;
        font-size: 9pt; page-break-inside: avoid; }
th { background: #0b4f8a; color: #fff; padding: 6px 8px; text-align: left;
     border: 1px solid #0b4f8a; }
td { padding: 5px 8px; border: 1px solid #cdd9e5; vertical-align: top; }
tr:nth-child(even) td { background: #f5f9fc; }
code { background: #eef2f5; padding: 1px 4px; border-radius: 3px;
       font-family: "WenQuanYi Zen Hei", monospace; font-size: 9pt; }
pre { background: #f6f8fa; border: 1px solid #dfe5ea; border-radius: 5px;
      padding: 10px; overflow-x: auto; page-break-inside: avoid; }
pre code { background: none; font-size: 8pt; line-height: 1.3; white-space: pre; }
h1 + p, h1 + blockquote { page-break-before: avoid; }
""")

HTML(string=html_doc).write_pdf(OUT, stylesheets=[css])
print("PDF written:", OUT)
