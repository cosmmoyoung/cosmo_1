#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Convert the India RE markdown encyclopedia to a styled PDF (CJK-aware)."""
import re
import markdown
from weasyprint import HTML

SRC = "/home/user/cosmo_1/印度新能源行业全景研究报告.md"
OUT = "/home/user/cosmo_1/印度新能源行业全景研究报告.pdf"

with open(SRC, encoding="utf-8") as f:
    text = f.read()

# Pull the H1 title for a simple cover, keep it in body too.
md = markdown.Markdown(extensions=["tables", "fenced_code", "sane_lists", "toc", "attr_list"])
body_html = md.convert(text)

CSS = """
@page {
  size: A4;
  margin: 1.8cm 1.6cm 2.0cm 1.6cm;
  @bottom-center { content: counter(page) " / " counter(pages);
    font-family: "WenQuanYi Zen Hei"; font-size: 8pt; color: #888; }
  @top-right { content: "印度新能源行业全景研究报告"; font-family: "WenQuanYi Zen Hei";
    font-size: 7.5pt; color: #aaa; }
}
* { box-sizing: border-box; }
body {
  font-family: "WenQuanYi Zen Hei", sans-serif;
  font-size: 10pt; line-height: 1.62; color: #1a1a1a;
}
h1 { font-size: 21pt; color: #0b5d3b; line-height: 1.3;
  border-bottom: 3px solid #0b5d3b; padding-bottom: 10px; margin-top: 6px; }
h2 { font-size: 15pt; color: #0b5d3b; margin-top: 24px;
  border-left: 6px solid #0b5d3b; padding-left: 10px; page-break-after: avoid; }
h3 { font-size: 12.5pt; color: #14794e; margin-top: 16px; page-break-after: avoid; }
h4 { font-size: 11pt; color: #333; margin-top: 12px; page-break-after: avoid; }
p { margin: 6px 0; text-align: justify; }
a { color: #1558b0; text-decoration: none; word-break: break-all; }
strong { color: #b3261e; }
ul, ol { margin: 6px 0 6px 0; padding-left: 22px; }
li { margin: 3px 0; }
hr { border: none; border-top: 1px solid #ccc; margin: 18px 0; }
blockquote {
  background: #f3f8f5; border-left: 4px solid #2e9e6b;
  margin: 10px 0; padding: 8px 14px; color: #234; font-size: 9.5pt;
}
blockquote p { margin: 4px 0; }
table {
  border-collapse: collapse; width: 100%; margin: 10px 0;
  font-size: 8.4pt; page-break-inside: avoid;
}
th, td { border: 1px solid #b8c8c0; padding: 4px 6px; vertical-align: top; text-align: left; }
th { background: #0b5d3b; color: #fff; font-weight: bold; }
tr:nth-child(even) td { background: #f4f8f6; }
pre {
  background: #1f2630; color: #e6edf3; font-family: "WenQuanYi Zen Hei Mono", monospace;
  font-size: 7.2pt; line-height: 1.32; white-space: pre; overflow: hidden;
  padding: 10px 12px; border-radius: 4px; margin: 10px 0; page-break-inside: avoid;
}
code { font-family: "WenQuanYi Zen Hei Mono", monospace; background: #eef1f0;
  padding: 0 3px; border-radius: 3px; font-size: 8.6pt; color: #b3261e; }
pre code { background: none; color: inherit; padding: 0; font-size: 7.2pt; }
h1 + blockquote, body > blockquote:first-of-type { font-size: 9pt; }
"""

html_doc = f"""<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8">
<style>{CSS}</style></head><body>{body_html}</body></html>"""

with open("/tmp/report.html", "w", encoding="utf-8") as f:
    f.write(html_doc)

HTML(string=html_doc, base_url="/home/user/cosmo_1").write_pdf(OUT)
print("PDF written:", OUT)
