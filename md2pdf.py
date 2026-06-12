#!/usr/bin/env python3
import sys, re, markdown
from weasyprint import HTML, CSS
from weasyprint.text.fonts import FontConfiguration

def convert(md_path, pdf_path, title):
    with open(md_path, encoding="utf-8") as f:
        text = f.read()
    # Strip leading H1 duplication is fine; keep as-is.
    html_body = markdown.markdown(
        text,
        extensions=["tables", "fenced_code", "sane_lists", "nl2br", "attr_list"],
    )
    css = """
    @page {
        size: A4;
        margin: 18mm 16mm 20mm 16mm;
        @bottom-center { content: counter(page) " / " counter(pages);
            font-family: 'WenQuanYi Zen Hei'; font-size: 8pt; color: #888; }
    }
    * { font-family: 'WenQuanYi Zen Hei', sans-serif; }
    body { font-size: 10.5pt; line-height: 1.62; color: #1a1a1a; }
    h1 { font-size: 19pt; color: #0b3d5c; border-bottom: 3px solid #0b3d5c;
         padding-bottom: 6px; margin: 0 0 10px 0; line-height: 1.3; }
    h2 { font-size: 14.5pt; color: #0b3d5c; margin: 20px 0 8px;
         border-left: 5px solid #1f7a99; padding-left: 9px; }
    h3 { font-size: 12pt; color: #134; margin: 15px 0 6px; }
    h4 { font-size: 10.8pt; color: #225; margin: 11px 0 5px; }
    p { margin: 6px 0; }
    em { color: #444; }
    strong { color: #0b2a3a; }
    blockquote { background: #eef4f8; border-left: 4px solid #1f7a99;
        margin: 10px 0; padding: 8px 14px; color: #163; }
    blockquote strong { color: #0b3d5c; }
    code { background: #f0f0f0; padding: 1px 4px; border-radius: 3px;
        font-size: 9.5pt; }
    table { border-collapse: collapse; width: 100%; margin: 10px 0;
        font-size: 9pt; }
    th { background: #0b3d5c; color: #fff; padding: 6px 8px; text-align: left;
        border: 1px solid #0b3d5c; }
    td { padding: 5px 8px; border: 1px solid #c5d2da; vertical-align: top; }
    tr:nth-child(even) td { background: #f3f7fa; }
    hr { border: none; border-top: 1px solid #cdd; margin: 14px 0; }
    ul, ol { margin: 6px 0 6px 4px; padding-left: 20px; }
    li { margin: 3px 0; }
    h1, h2, h3, h4 { page-break-after: avoid; }
    table, blockquote { page-break-inside: avoid; }
    """
    full = f"<html><head><meta charset='utf-8'><title>{title}</title></head><body>{html_body}</body></html>"
    fc = FontConfiguration()
    HTML(string=full).write_pdf(pdf_path, stylesheets=[CSS(string=css, font_config=fc)], font_config=fc)
    print("wrote", pdf_path)

if __name__ == "__main__":
    for md, pdf, title in [
        ("research/the_80_percent_bet.md", "research/80%身家之战_最终结论.pdf", "80%身家之战"),
        ("research/storage_master_synthesis.md", "research/存储为王_总结论.pdf", "存储为王"),
    ]:
        convert(md, pdf, title)
