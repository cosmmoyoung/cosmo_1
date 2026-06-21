#!/usr/bin/env python3
"""把《AI未来世界沙盘推演报告.md》渲染成排版精良的中文 PDF。"""
import re
import markdown
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

SRC = "AI未来世界沙盘推演报告.md"
OUT = "AI未来世界沙盘推演报告.pdf"

with open(SRC, encoding="utf-8") as f:
    md_text = f.read()

# 提取标题(首个一级标题)与副标题
lines = md_text.splitlines()
title = "AI 未来世界沙盘推演报告"
subtitle = ""
for ln in lines:
    if ln.startswith("# "):
        title = ln[2:].strip()
        break
for ln in lines:
    if ln.startswith("### "):
        subtitle = ln[4:].strip()
        break

# 去掉正文里的第一段元信息块引用之前不动;Markdown 转 HTML
html_body = markdown.markdown(
    md_text,
    extensions=["tables", "fenced_code", "toc", "sane_lists", "nl2br"],
    output_format="html5",
)

# 给每个 <h2> 之前插入分页(章与章之间)——通过 CSS 实现,见下方 page-break

cover = f"""
<div class="cover">
  <div class="cover-kicker">理性推演 · 沙盘报告</div>
  <h1 class="cover-title">{title}</h1>
  <div class="cover-sub">{subtitle}</div>
  <div class="cover-meta">
    <div>撰写日期:2026 年 6 月 21 日</div>
    <div>方法:多路并行网络研究综合 · 区分【事实/数据/预测】并标注置信度</div>
    <div>覆盖:白领自动化 · 后劳动经济 · 虚拟内容 · 面向 AI 的互联网 · 具身智能 · AI 安全 · 巨头格局 · 中美欧地缘</div>
  </div>
  <div class="cover-note">本报告为公开信息的整理、综合与理性推演,不构成任何投资、政治或职业建议。<br/>所有面向未来的判断均含高度不确定性——它推演的是概率,不是命运。</div>
</div>
"""

html_doc = f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8"><title>{title}</title></head>
<body>{cover}<div class="content">{html_body}</div></body></html>"""

css = CSS(string="""
@page {
  size: A4;
  margin: 22mm 18mm 20mm 18mm;
  @bottom-center {
    content: counter(page) " / " counter(pages);
    font-family: "WenQuanYi Zen Hei"; font-size: 9pt; color: #888;
  }
  @top-right {
    content: "AI 未来世界沙盘推演报告";
    font-family: "WenQuanYi Zen Hei"; font-size: 8pt; color: #bbb;
  }
}
@page :first { margin: 0; @bottom-center { content: none; } @top-right { content: none; } }

* { box-sizing: border-box; }
body {
  font-family: "WenQuanYi Zen Hei", sans-serif;
  font-size: 10.5pt; line-height: 1.75; color: #1a1a1a;
}

/* 封面 */
.cover {
  page-break-after: always;
  height: 297mm; padding: 55mm 24mm 24mm 24mm;
  background: linear-gradient(160deg, #0f172a 0%, #1e293b 55%, #334155 100%);
  color: #f1f5f9;
}
.cover-kicker { font-size: 12pt; letter-spacing: 6px; color: #93c5fd; margin-bottom: 18mm; }
.cover-title { font-size: 30pt; line-height: 1.35; font-weight: 700; margin: 0 0 8mm 0; color: #fff; }
.cover-sub { font-size: 13pt; line-height: 1.7; color: #cbd5e1; margin-bottom: 30mm; }
.cover-meta { font-size: 10pt; line-height: 2.0; color: #e2e8f0; border-top: 1px solid #475569; padding-top: 8mm; }
.cover-note { margin-top: 22mm; font-size: 9pt; line-height: 1.9; color: #94a3b8; border-left: 3px solid #3b82f6; padding-left: 5mm; }

/* 正文 */
.content { counter-reset: none; }
h1 { font-size: 19pt; color: #0f172a; border-bottom: 3px solid #3b82f6; padding-bottom: 3mm; margin: 0 0 6mm 0; }
h2 {
  font-size: 15pt; color: #1e3a8a; margin: 9mm 0 4mm 0;
  padding: 2mm 0 2mm 4mm; border-left: 5px solid #3b82f6; background: #f8fafc;
  page-break-before: always; page-break-after: avoid;
}
.content > h1 + h2:first-of-type, h2:first-of-type { page-break-before: avoid; }
h3 { font-size: 12.5pt; color: #1e40af; margin: 6mm 0 2mm 0; page-break-after: avoid; }
h4 { font-size: 11pt; color: #334155; margin: 4mm 0 1.5mm 0; page-break-after: avoid; }
p { margin: 0 0 2.6mm 0; text-align: justify; }
strong { color: #b91c1c; font-weight: 700; }

a { color: #2563eb; text-decoration: none; word-break: break-all; }

ul, ol { margin: 1.5mm 0 3mm 0; padding-left: 7mm; }
li { margin: 0 0 1.4mm 0; }

blockquote {
  margin: 3mm 0; padding: 3mm 5mm; background: #eff6ff;
  border-left: 4px solid #60a5fa; color: #1e293b; border-radius: 2px;
}
blockquote p { margin: 0 0 1.5mm 0; }
blockquote strong { color: #1d4ed8; }

table {
  border-collapse: collapse; width: 100%; margin: 3mm 0; font-size: 9.5pt;
  page-break-inside: avoid;
}
th { background: #1e3a8a; color: #fff; font-weight: 600; padding: 2mm 2.5mm; text-align: left; border: 1px solid #1e3a8a; }
td { padding: 2mm 2.5mm; border: 1px solid #cbd5e1; vertical-align: top; }
tr:nth-child(even) td { background: #f1f5f9; }

code {
  font-family: "WenQuanYi Zen Hei Mono", monospace; font-size: 9pt;
  background: #f1f5f9; padding: 0.5mm 1.5mm; border-radius: 2px; color: #be123c;
}
hr { border: none; border-top: 1px solid #e2e8f0; margin: 6mm 0; }

/* 让目录段更紧凑 */
.content > ol:first-of-type li, .content > ul:first-of-type li { margin-bottom: 0.8mm; }
""")

font_config = FontConfiguration()
HTML(string=html_doc, base_url=".").write_pdf(OUT, stylesheets=[css], font_config=font_config)
print(f"OK -> {OUT}")
