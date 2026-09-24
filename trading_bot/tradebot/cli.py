"""Command line: `tradebot <command>`. Run `tradebot -h` for the list."""

from __future__ import annotations

import argparse
import logging
import shutil
import sys
from pathlib import Path

from pydantic import ValidationError

from tradebot.config import Settings, load_settings

EXAMPLES = Path(__file__).resolve().parent.parent  # config.example.yaml / .env.example live here


def _bot(settings: Settings, one_off: bool = True):
    """One-off commands (approve, portfolio...) use the next IBKR client id, so they can run
    while `tradebot run` holds its own connection."""
    from tradebot.orchestrator import build_bot
    if one_off:
        settings.execution.ibkr_client_id += 1
    return build_bot(settings)


def cmd_init(settings: Settings, args) -> int:
    base = settings.base_dir
    for name, example in (("config.yaml", "config.example.yaml"), (".env", ".env.example")):
        target, source = base / name, EXAMPLES / example
        if not target.exists() and source.exists():
            shutil.copy(source, target)
            print(f"已创建 {target}")
    from tradebot.sources.inbox import InboxSource
    from tradebot.store import Store
    settings.data_path.mkdir(parents=True, exist_ok=True)
    InboxSource(settings.path(settings.sources.inbox_dir), Store(settings.db_path)).ensure_dirs()
    print(f"数据目录：{settings.data_path}\n收件箱：{settings.path(settings.sources.inbox_dir)}")
    print("下一步：在 .env 填 API key，然后运行 tradebot cycle（模拟盘 + 人工审批是默认设置）")
    return 0


def cmd_demo(settings: Settings, args) -> int:
    from tradebot.demo import run_demo
    run_demo()
    return 0


def cmd_run(settings: Settings, args) -> int:
    try:
        _bot(settings, one_off=False).run_forever()
    except KeyboardInterrupt:
        print("已停止")
    return 0


def cmd_cycle(settings: Settings, args) -> int:
    print(_bot(settings).cycle())
    return 0


def cmd_research(settings: Settings, args) -> int:
    thesis = _bot(settings).research(args.ticker.upper(), args.reason or "手动发起的深度研究")
    print(f"{thesis.ticker}: conviction {thesis.conviction}，审核 {thesis.reviewer_verdict}，状态 {thesis.status}")
    print("memo 文件：\n" + "\n".join(thesis.memo_paths))
    return 0


def cmd_theses(settings: Settings, args) -> int:
    from tradebot.store import Store
    theses = Store(settings.db_path).theses()
    if not theses:
        print("还没有 thesis")
    for t in theses:
        print(f"{t.ticker:<6} {t.status:<7} conviction {t.conviction:>3}  {t.reviewer_verdict:<26} {t.summary[:60]}")
    return 0


def cmd_show(settings: Settings, args) -> int:
    from tradebot.research.thesis_update import render_checklist
    from tradebot.store import Store
    thesis = Store(settings.db_path).get_thesis(args.ticker.upper())
    if thesis is None:
        print("没有这只股票的 thesis")
        return 1
    print(render_checklist(thesis))
    print(f"\n公允价值 {thesis.fair_value}，最高买入价 {thesis.max_entry_price}，状态 {thesis.status}")
    print("\n## 历史")
    for event in thesis.history:
        print(f"{event.at}  {event.conviction_before} -> {event.conviction_after}  {event.note}")
    return 0


def cmd_orders(settings: Settings, args) -> int:
    from tradebot.store import Store
    orders = Store(settings.db_path).orders(limit=args.limit)
    if not orders:
        print("没有订单")
    for o in orders:
        print(f"{o.id}  {o.created_at[:16]}  {o.status:<16} {o.side:<4} {o.quantity:>6} {o.ticker:<6} @ {o.limit_price}")
        for note in o.risk_notes:
            print(f"      - {note}")
    return 0


def cmd_approve(settings: Settings, args) -> int:
    order = _bot(settings).desk.approve(args.order_id)
    print(f"{order.ticker}: {order.status}")
    for note in order.risk_notes:
        print(f"  - {note}")
    return 0 if order.status in ("filled", "submitted") else 1


def cmd_reject(settings: Settings, args) -> int:
    order = _bot(settings).desk.reject(args.order_id)
    print(f"{order.ticker}: 已拒绝")
    return 0


def cmd_portfolio(settings: Settings, args) -> int:
    bot = _bot(settings)
    account = bot.broker.account()
    leverage = account.gross_exposure / account.nav if account.nav > 0 else 0.0
    print(f"券商 {bot.broker.name}  净值 ${account.nav:,.0f}  现金 ${account.cash:,.0f}  总仓位 {leverage:.2f} 倍")
    for ticker, pos in sorted(account.positions.items()):
        print(f"{ticker:<6} {pos.qty:>8g} 股  成本 {pos.avg_cost:>9.2f}  现价 {pos.market_price:>9.2f}  "
              f"占比 {account.weight_pct(ticker):5.1f}%")
    return 0


def cmd_doctor(settings: Settings, args) -> int:
    from tradebot.doctor import FAIL, live_checks, run_checks
    checks = run_checks(settings)
    if args.live:
        from tradebot.llm import LLMRouter
        from tradebot.orchestrator import make_provider
        router = LLMRouter(settings.llm, factory=lambda name: make_provider(settings, name))
        checks += live_checks(settings, router)
    for check in checks:
        print(check.line())
    failed = sum(c.status == FAIL for c in checks)
    print("\n全部通过，可以运行 tradebot cycle" if not failed else f"\n有 {failed} 项需要处理")
    return 1 if failed else 0


def cmd_usage(settings: Settings, args) -> int:
    from tradebot.store import Store
    rows = Store(settings.db_path).usage_summary(args.days)
    if not rows:
        print("还没有 AI 调用记录")
        return 0
    print(f"最近 {args.days} 天的 AI 用量（金额按 API 标价折算，估算）\n")
    print(f"{'计费':<12} {'通道':<11} {'模型':<18} {'次数':>6} {'输入 token':>12} {'输出 token':>12} {'API 价折算':>10}")
    totals = {"api": 0.0, "subscription": 0.0}
    for r in rows:
        label = {"api": "API 按量", "subscription": "订阅包月"}.get(r["billing"], r["billing"])
        cost = r["api_cost_usd"] or 0.0
        totals[r["billing"]] = totals.get(r["billing"], 0.0) + cost
        print(f"{label:<12} {r['provider']:<11} {r['model']:<18} {r['calls']:>6} "
              f"{r['input_tokens'] or 0:>12,} {r['output_tokens'] or 0:>12,} {'$' + format(cost, ',.2f'):>10}")
    print(f"\nAPI 实际花费（估算）：${totals['api']:,.2f}")
    print(f"订阅通道的用量如果走 API，要花（估算）：${totals['subscription']:,.2f}，这部分实际由月费支付")
    return 0


def cmd_compare(settings: Settings, args) -> int:
    from tradebot.orchestrator import compare_routes
    bot = _bot(settings)
    routes = compare_routes(settings, args.via)
    print(f"用 {', '.join(routes)} 分别研究 {args.ticker.upper()}（结果不会覆盖正式 thesis，也不会下单）...\n")
    failed = 0
    for label, result in bot.compare(args.ticker.upper(), routes).items():
        thesis = result.thesis
        if thesis is None:
            failed += 1
            print(f"== {label}：失败，{result.error}\n")
            continue
        print(f"== {label}：conviction {thesis.conviction}，审核 {thesis.reviewer_verdict}，方向 {thesis.direction}，"
              f"公允价值 {thesis.fair_value}，最高买入价 {thesis.max_entry_price}，按 API 价折算 ${result.api_cost_usd:,.2f}")
        print(f"   {thesis.summary[:200]}")
        print(f"   退出条件：{'；'.join(thesis.kill_criteria)}")
        if thesis.memo_paths:
            print(f"   memo：{Path(thesis.memo_paths[0]).parent}（文件名带 {label}）\n")
    return 1 if failed == len(routes) else 0


def cmd_stop(settings: Settings, args) -> int:
    settings.data_path.mkdir(parents=True, exist_ok=True)
    settings.stop_file.write_text("stop\n", encoding="utf-8")
    print(f"紧急停止已打开（{settings.stop_file}）。机器人不会再下任何单，运行 tradebot resume 恢复。")
    return 0


def cmd_resume(settings: Settings, args) -> int:
    settings.stop_file.unlink(missing_ok=True)
    print("紧急停止已解除")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="tradebot", description="新闻驱动、thesis 管理的研究与交易机器人")
    parser.add_argument("-c", "--config", default="config.yaml", help="配置文件路径（默认 ./config.yaml）")
    parser.add_argument("-v", "--verbose", action="store_true", help="输出调试日志")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("init", help="创建 config.yaml、.env、数据目录和收件箱文件夹").set_defaults(func=cmd_init)
    sub.add_parser("demo", help="不需要 API key，用模拟数据走一遍完整流程").set_defaults(func=cmd_demo)
    sub.add_parser("run", help="持续运行，每隔 news_poll_minutes 跑一轮").set_defaults(func=cmd_run)
    sub.add_parser("cycle", help="只跑一轮（适合 cron 定时调用）").set_defaults(func=cmd_cycle)
    p = sub.add_parser("research", help="立刻对一只股票做深度研究")
    p.add_argument("ticker")
    p.add_argument("--reason", default="")
    p.set_defaults(func=cmd_research)
    sub.add_parser("theses", help="列出所有 thesis").set_defaults(func=cmd_theses)
    p = sub.add_parser("show", help="查看一只股票的 thesis 和更新历史")
    p.add_argument("ticker")
    p.set_defaults(func=cmd_show)
    p = sub.add_parser("orders", help="列出订单（含待审批）")
    p.add_argument("--limit", type=int, default=30)
    p.set_defaults(func=cmd_orders)
    p = sub.add_parser("approve", help="批准一张待审批订单（会先重新过一遍风控）")
    p.add_argument("order_id")
    p.set_defaults(func=cmd_approve)
    p = sub.add_parser("reject", help="拒绝一张待审批订单")
    p.add_argument("order_id")
    p.set_defaults(func=cmd_reject)
    sub.add_parser("portfolio", help="查看账户和持仓").set_defaults(func=cmd_portfolio)
    p = sub.add_parser("doctor", help="检查 API key、命令行工具、订阅登录和券商设置")
    p.add_argument("--live", action="store_true", help="再给每个模型发一个极小的测试请求")
    p.set_defaults(func=cmd_doctor)
    p = sub.add_parser("usage", help="AI 用量和花费（API 实付 vs 订阅覆盖）")
    p.add_argument("--days", type=int, default=7)
    p.set_defaults(func=cmd_usage)
    p = sub.add_parser("compare", help="用不同模型对同一只股票各做一次深度研究，对比结论")
    p.add_argument("ticker")
    p.add_argument("--via", nargs="+", default=["claude", "codex"],
                   help="对比路线：claude（Claude Code 订阅）、codex（Codex 订阅）、claude_api、openai_api")
    p.set_defaults(func=cmd_compare)
    sub.add_parser("stop", help="紧急停止：机器人不再下任何单").set_defaults(func=cmd_stop)
    sub.add_parser("resume", help="解除紧急停止").set_defaults(func=cmd_resume)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )
    if args.command == "demo":
        logging.getLogger("tradebot").setLevel(logging.WARNING)  # keep the narrated demo readable
    try:
        settings = load_settings(args.config)
    except ValidationError as exc:
        print(f"配置文件 {args.config} 有误：\n{exc}", file=sys.stderr)
        return 2
    try:
        return args.func(settings, args)
    except Exception as exc:  # missing API keys, refused live ports, network errors...
        if args.verbose:
            raise
        print(f"错误：{type(exc).__name__}: {exc}\n（加 -v 查看完整报错）", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
