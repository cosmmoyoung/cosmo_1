#!/usr/bin/env python3
"""Convert the Neocloud markdown report into a styled PDF (CJK-aware)."""
import re
import sys
import markdown
from weasyprint import HTML

SRC = "Neocloud新云算力行业全景研究报告.md"
OUT = "Neocloud新云算力行业全景研究报告.pdf"

with open(SRC, encoding="utf-8") as f:
    text = f.read()

# Emoji -> clean text glyphs (no color-emoji font is installed; avoid tofu boxes)
emoji_map = {
    "⚠️": "▲", "⚠": "▲",
    "✅": "✓",
    "⭐": "★",
    "↓": "↓",
}
for k, v in emoji_map.items():
    text = text.replace(k, v)

html_body = markdown.markdown(
    text,
    extensions=["tables", "fenced_code", "toc", "attr_list", "md_in_html", "sane_lists"],
)

CSS = """
@page {
  size: A4;
  margin: 18mm 16mm 20mm 16mm;
  @bottom-center {
    content: "Neocloud 新云算力行业全景研究报告  ·  第 " counter(page) " / " counter(pages) " 页";
    font-family: "WenQuanYi Zen Hei";
    font-size: 8.5pt;
    color: #888;
  }
}
@page :first { @bottom-center { content: ""; } }

* { box-sizing: border-box; }
body {
  font-family: "WenQuanYi Zen Hei", "Noto Sans CJK SC", sans-serif;
  font-size: 10.5pt;
  line-height: 1.65;
  color: #1a1a1a;
}

h1 {
  font-size: 22pt; color: #0b3d5c; line-height: 1.3;
  border-bottom: 3px solid #0b3d5c; padding-bottom: 8px; margin: 0 0 6px;
}
h1 + h3 { color: #2c7fb8; font-size: 12.5pt; margin-top: 0; font-weight: normal; }
h2 {
  font-size: 16pt; color: #0b3d5c; margin-top: 26px; margin-bottom: 10px;
  border-left: 6px solid #2c7fb8; padding-left: 10px;
  page-break-after: avoid;
}
h3 { font-size: 12.5pt; color: #15576e; margin-top: 18px; page-break-after: avoid; }
h4 { font-size: 11pt; color: #15576e; margin-top: 14px; page-break-after: avoid; }
p { margin: 6px 0; text-align: justify; }

a { color: #1763a6; text-decoration: none; }

strong { color: #b3261e; }

blockquote {
  background: #f3f8fb; border-left: 4px solid #2c7fb8;
  margin: 10px 0; padding: 8px 14px; border-radius: 3px;
  page-break-inside: avoid;
}
blockquote strong { color: #0b3d5c; }

table {
  border-collapse: collapse; width: 100%; margin: 12px 0;
  font-size: 9pt; page-break-inside: avoid;
}
th, td { border: 1px solid #cfd9e0; padding: 5px 7px; text-align: left; vertical-align: top; }
th { background: #0b3d5c; color: #fff; font-weight: bold; }
tr:nth-child(even) td { background: #f5f8fa; }

code {
  font-family: "WenQuanYi Zen Hei Mono", monospace;
  background: #eef2f4; padding: 1px 4px; border-radius: 3px; font-size: 9pt;
}
pre {
  background: #1e2a32; color: #e6edf2; padding: 12px 14px; border-radius: 5px;
  font-family: "WenQuanYi Zen Hei Mono", monospace; font-size: 8.5pt;
  line-height: 1.4; overflow-x: auto; white-space: pre-wrap; page-break-inside: avoid;
}
pre code { background: none; color: inherit; padding: 0; }

hr { border: none; border-top: 1px solid #d6dee3; margin: 18px 0; }

ul, ol { margin: 6px 0 6px 4px; padding-left: 22px; }
li { margin: 3px 0; }

/* Title block sits on its own first page region */
h1 { page-break-before: avoid; }
"""

full = f"""<!DOCTYPE html><html lang="zh-CN"><head><meta charset="utf-8">
<style>{CSS}</style></head><body>{html_body}</body></html>"""

HTML(string=full, base_url=".").write_pdf(OUT)
print(f"PDF written: {OUT}")
