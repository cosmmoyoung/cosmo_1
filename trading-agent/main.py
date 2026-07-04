"""市场监测 Agent 入口。

用法:
    python main.py             # 真实模式:抓行情 + RSS(+ X,如有 token)
    python main.py --demo      # 演示模式:用 data/fixtures 里的快照数据
"""
import argparse
import sys

from agent.config import load_config
from agent.sources.market import fetch_market
from agent.sources.news import fetch_news
from agent.sources.x_source import fetch_x_posts
from agent.analysis.signals import screen_market
from agent.analysis.llm import analyze
from agent import report as rpt
from agent.notify import notify


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--demo", action="store_true", help="用本地快照数据演示")
    parser.add_argument("--date", default=None, help="覆盖报告日期(演示用)")
    args = parser.parse_args()

    cfg = load_config()
    run_date = args.date or rpt.today()

    print(f"=== 市场监测 Agent · {run_date} {'(demo)' if args.demo else ''} ===")

    print("[1/5] 抓取行情 ...")
    market = fetch_market(cfg, demo=args.demo)
    print(f"      {len(market)} 只标的")

    print("[2/5] 抓取叙事材料(新闻 + X)...")
    news = fetch_news(cfg, demo=args.demo)
    x_posts = fetch_x_posts(cfg, demo=args.demo)
    print(f"      新闻 {len(news)} 条,大佬发言 {len(x_posts)} 条")

    print("[3/5] 规则引擎筛选异动 ...")
    rule_signals = screen_market(market, cfg["rules"])
    print(f"      触发 {len(rule_signals)} 条信号")

    print("[4/5] 分析(LLM 或规则汇总)...")
    analysis = analyze(cfg, market, rule_signals, news, x_posts)

    print("[5/5] 生成日报 + 留痕 + 推送 ...")
    content = rpt.render_report(run_date, market, rule_signals, analysis,
                                x_count=len(x_posts), news_count=len(news))
    path = rpt.save_report(run_date, content)
    rpt.log_signals(run_date, rule_signals)
    notify(cfg, run_date, content)

    print(f"完成:{path}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
