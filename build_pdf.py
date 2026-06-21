#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Render the Chinese research report markdown into a polished PDF via WeasyPrint."""
import re, datetime, markdown
from weasyprint import HTML

SRC = "/home/user/cosmo_1/AI原生软件基础设施_卡位研究报告.md"
OUT = "/home/user/cosmo_1/AI原生软件基础设施_卡位研究报告.pdf"

raw = open(SRC, encoding="utf-8").read()

# --- clean emoji that color-font rendering may break, swap for tidy text badges ---
raw = raw.replace("⚠️", "▲ ").replace("⚠", "▲ ")
raw = raw.replace("📅", "▣ ")
raw = raw.replace("🤖", "")

# Drop the very first H1 (we build a dedicated cover instead)
lines = raw.split("\n")
for i, ln in enumerate(lines):
    if ln.startswith("# "):
        del lines[i]
        break
body_md = "\n".join(lines).strip()

md = markdown.Markdown(extensions=["tables", "fenced_code", "toc", "attr_list", "sane_lists"])
body_html = md.convert(body_md)

today = "2026-06-21"

cover = """
<section class="cover">
  <div class="cover-band"></div>
  <div class="cover-inner">
    <div class="eyebrow">深度行业研究 · DEEP-DIVE RESEARCH</div>
    <h1 class="cover-title">AI 时代被错杀的<br>软件基础设施</h1>
    <h2 class="cover-sub">卡位深度研究报告</h2>
    <p class="cover-tag">当互联网流量从「人」转向「AI Agent」,谁是真正不可替代的卖铲人?</p>
    <div class="chips">
      <span>Cloudflare</span><span>Datadog</span><span>MongoDB</span>
      <span>ServiceNow</span><span>Okta</span><span>Snowflake</span>
      <span>Palo Alto</span><span>Stripe</span><span>Databricks</span><span>Twilio</span>
    </div>
    <div class="cover-meta">
      <div><span class="k">基准日</span><span class="v">%s</span></div>
      <div><span class="k">方法</span><span class="v">多智能体并行调研 + 实时财务交叉验证 + 红队压力测试</span></div>
      <div><span class="k">性质</span><span class="v">投资研究与教育材料 · 非投资建议</span></div>
    </div>
  </div>
  <div class="cover-foot">生成于 Claude Code · 仅供研究与学习用途</div>
</section>
""" % today

CSS = r"""
@page {
  size: A4;
  margin: 18mm 16mm 20mm 16mm;
  @bottom-center {
    content: "AI 时代被错杀的软件基础设施 · 卡位深度研究报告";
    font-family: "DejaVu Sans","WenQuanYi Zen Hei",sans-serif;
    font-size: 7.5pt; color: #9aa6b2;
  }
  @bottom-right {
    content: counter(page) " / " counter(pages);
    font-family: "DejaVu Sans",sans-serif; font-size: 7.5pt; color: #9aa6b2;
  }
}
@page cover { margin: 0; @bottom-center { content: none; } @bottom-right { content: none; } }

:root{}
* { box-sizing: border-box; }
body {
  font-family: "DejaVu Sans","WenQuanYi Zen Hei",sans-serif;
  font-size: 10pt; line-height: 1.72; color: #1f2933;
  -weasy-hyphens: none;
}

/* ---------- Cover ---------- */
.cover { page: cover; position: relative; height: 297mm; width: 210mm;
  background: linear-gradient(160deg,#0f2740 0%,#16334f 45%,#1d4763 100%);
  color: #eef3f7; overflow: hidden; }
.cover-band { position:absolute; top:0; left:0; right:0; height:8mm;
  background: linear-gradient(90deg,#c8a046,#e0bf6e,#c8a046); }
.cover-inner { padding: 46mm 22mm 0 22mm; }
.eyebrow { letter-spacing: .32em; font-size: 9pt; color:#c8a046; font-weight:700; margin-bottom: 14mm; }
.cover-title { font-size: 40pt; line-height: 1.18; font-weight: 800; margin: 0 0 6mm 0; color:#ffffff; }
.cover-sub { font-size: 19pt; font-weight: 600; color:#bcd2e2; margin: 0 0 10mm 0; }
.cover-tag { font-size: 11.5pt; color:#d8e4ee; line-height:1.7; max-width: 150mm; margin: 0 0 16mm 0; }
.chips { margin: 0 0 18mm 0; }
.chips span { display:inline-block; border:1px solid rgba(200,160,70,.55); color:#e7d6a8;
  border-radius: 20px; padding: 2.5pt 10pt; font-size: 8.6pt; margin: 0 6pt 7pt 0; }
.cover-meta { border-top:1px solid rgba(255,255,255,.18); padding-top: 8mm; max-width: 160mm; }
.cover-meta > div { display:flex; margin-bottom: 4mm; font-size: 9.5pt; }
.cover-meta .k { width: 26mm; color:#8fb0c7; font-weight:700; letter-spacing:.05em; }
.cover-meta .v { flex:1; color:#e9f1f7; }
.cover-foot { position:absolute; bottom: 14mm; left:0; right:0; text-align:center;
  font-size: 8pt; color:#7f9bb0; letter-spacing:.06em; }

/* ---------- Headings ---------- */
h1,h2,h3,h4 { font-weight:700; color:#0f2740; line-height:1.35; }
h1 { font-size: 19pt; }
h2 { font-size: 15.5pt; margin: 16pt 0 9pt 0; padding-bottom: 5pt;
  border-bottom: 2.4pt solid #1d4763; color:#13344f;
  break-before: page; }
h2:first-of-type { break-before: avoid; }
h3 { font-size: 12.6pt; margin: 14pt 0 6pt 0; color:#1d4763;
  border-left: 4pt solid #c8a046; padding-left: 8pt; }
h4 { font-size: 11pt; margin: 11pt 0 4pt 0; color:#2f6f8f; }
h2,h3,h4 { break-after: avoid; }

p { margin: 4pt 0 7pt 0; text-align: justify; }
strong { color:#10314c; }
a { color:#1d4763; text-decoration: none; }
hr { border:none; border-top:1px solid #d9e1e8; margin: 12pt 0; }

/* ---------- Lists ---------- */
ul,ol { margin: 4pt 0 8pt 0; padding-left: 18pt; }
li { margin: 2.5pt 0; }

/* ---------- Tables ---------- */
table { width:100%; border-collapse: collapse; margin: 9pt 0 12pt 0;
  font-size: 7.9pt; line-height:1.45; break-inside: avoid; }
thead { background: #13344f; }
th { color:#fff; font-weight:700; padding: 5pt 5pt; text-align:left;
  border:.6pt solid #13344f; }
td { padding: 4.5pt 5pt; border:.6pt solid #d3dde5; vertical-align: top;
  word-break: break-word; }
tbody tr:nth-child(even){ background:#f3f7fa; }
tbody tr:nth-child(odd){ background:#ffffff; }

/* ---------- Blockquote ---------- */
blockquote { margin: 8pt 0; padding: 8pt 12pt; background:#f5f0e1;
  border-left: 4pt solid #c8a046; border-radius: 2pt; color:#3a3526;
  break-inside: avoid; font-size: 9.4pt; }
blockquote p { margin: 3pt 0; }
blockquote strong { color:#7a5a12; }

/* ---------- Code ---------- */
code { background:#eef2f5; padding: 1pt 3pt; border-radius:3pt;
  font-family:"DejaVu Sans Mono",monospace; font-size: 8.6pt; color:#9a3b3b; }

/* table of contents block (the manual 目录 list) */
h2#目录 + ol, h2:contains('目录') + ol { font-size: 9.5pt; }
"""

html = """<!DOCTYPE html><html lang="zh"><head><meta charset="utf-8">
<style>%s</style></head><body>%s<main>%s</main></body></html>""" % (CSS, cover, body_html)

open("/tmp/report.html","w",encoding="utf-8").write(html)
HTML(string=html, base_url="/home/user/cosmo_1/").write_pdf(OUT)
print("PDF written ->", OUT)
