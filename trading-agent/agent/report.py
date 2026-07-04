"""日报生成 + 信号留痕。

信号留痕(signals.jsonl)是这个系统里最重要的纪律:每天的信号都
追加记录,几个月后你就能回答"我的信号到底准不准"——这是从
"感觉不错"进化到"有统计依据"的唯一路径。
"""
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORTS = ROOT / "reports"


def render_report(run_date: str, market: list[dict], rule_signals: list[dict],
                  analysis: dict, x_count: int, news_count: int) -> str:
    lines = [f"# 市场监测晨报 · {run_date}", ""]
    mode = "🧠 LLM 分析" if analysis["mode"] == "llm" else "⚙️ 规则汇总(未启用 LLM)"
    lines.append(f"*模式:{mode} · 叙事材料:大佬发言 {x_count} 条 / 新闻 {news_count} 条*")
    lines.append("")

    lines.append("## 行情快照")
    lines.append("| 标的 | 主题 | 收盘 | 涨跌 | 距52周高点 |")
    lines.append("|---|---|---:|---:|---:|")
    for r in sorted(market, key=lambda x: x.get("change_pct") or 0):
        pct = r.get("change_pct") or 0
        arrow = "🔴" if pct < 0 else "🟢"
        off_hi = ""
        if r.get("price") and r.get("year_high"):
            off_hi = f"-{(r['year_high'] - r['price']) / r['year_high'] * 100:.0f}%"
        lines.append(f"| {r['symbol']} | {r.get('theme','')} | {r['price']:.2f} "
                     f"| {arrow} {pct:+.1f}% | {off_hi} |")
    lines.append("")

    lines.append(analysis["text"])
    lines.append("")
    lines.append("---")
    lines.append("*本报告由自动化系统生成,仅为研究线索,不构成投资建议。*")
    return "\n".join(lines)


def save_report(run_date: str, content: str) -> Path:
    REPORTS.mkdir(exist_ok=True)
    path = REPORTS / f"brief-{run_date}.md"
    path.write_text(content, encoding="utf-8")
    return path


def log_signals(run_date: str, rule_signals: list[dict]) -> None:
    """把当日信号追加到 signals.jsonl,供日后统计信号胜率。"""
    REPORTS.mkdir(exist_ok=True)
    with open(REPORTS / "signals.jsonl", "a", encoding="utf-8") as f:
        for s in rule_signals:
            f.write(json.dumps({"date": run_date, **s}, ensure_ascii=False) + "\n")


def today() -> str:
    return date.today().isoformat()
