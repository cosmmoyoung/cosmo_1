"""`tradebot demo`: the whole pipeline on made-up data.

No API keys, no network, no real money. A fictional company (Demo Photonics,
ticker DPHO) wins a contract, gets researched and bought on the paper account,
then loses its anchor customer, which hits a kill criterion and triggers an exit.
"""

from __future__ import annotations

import re
import tempfile
from datetime import datetime
from pathlib import Path
from typing import Callable

from tradebot.config import Settings
from tradebot.llm.fake import FakeProvider
from tradebot.models import (
    CandidateRanking,
    IndustryScan,
    NewsItem,
    Pillar,
    PillarUpdate,
    Quote,
    ThesisAssessment,
    ThesisDraft,
    TriageBatch,
    TriageResult,
    iso,
    utcnow,
)
from tradebot.orchestrator import TradingBot, build_bot

TICKER = "DPHO"
GOOD_NEWS = "demo-contract-win"
BAD_NEWS = "demo-customer-loss"


class DemoFMP:
    """Stands in for FMPClient with fixed data for one fictional company."""

    def __init__(self, price: float = 50.0):
        self.price = price

    def quote(self, symbol: str) -> Quote | None:
        return Quote(ticker=symbol, price=self.price, market_cap=8e9) if symbol == TICKER else None

    def company_snapshot(self, symbol: str) -> dict:
        return {"symbol": symbol, "as_of": iso(utcnow()), "note": "fictional demo data",
                "profile": {"companyName": "Demo Photonics Inc.", "industry": "Semiconductors"},
                "quote": {"price": self.price}}

    def industry_performance(self, day, exchange=None) -> list[dict]:
        return [{"industry": "Semiconductors", "averageChange": 0.8}]

    def industry_pe(self, day, exchange=None) -> list[dict]:
        return [{"industry": "Semiconductors", "pe": 31.0}]

    def screener(self, **filters) -> list[dict]:
        return []

    def key_metrics_ttm(self, symbol: str) -> dict:
        return {}


class ScriptedNews:
    """Emits one scripted batch of headlines per poll."""

    name = "demo-news"

    def __init__(self, batches: list[list[NewsItem]]):
        self.batches = batches

    def fetch(self, since: datetime) -> list[NewsItem]:
        return self.batches.pop(0) if self.batches else []


def demo_news() -> list[list[NewsItem]]:
    now = iso(utcnow())
    return [
        [NewsItem(id=GOOD_NEWS, source="demo", tickers=[TICKER], published_at=now,
                  title="Demo Photonics wins multi-year 1.6T laser supply deal with a hyperscaler",
                  summary="The contract covers 2027-2029 and makes DPHO the second source for EML lasers.")],
        [NewsItem(id=BAD_NEWS, source="demo", tickers=[TICKER], published_at=now,
                  title="Demo Photonics' largest customer moves laser design in-house from 2027",
                  summary="The customer was 41% of revenue last year; the company cut 2027 guidance.")],
    ]


def _triage(system: str, prompt: str) -> TriageBatch:
    results = []
    for item_id in re.findall(r"^\[([^\]]+)\]", prompt, flags=re.M):
        if item_id == GOOD_NEWS:
            results.append(TriageResult(
                item_id=item_id, materiality=8, tickers=[TICKER], industries=["Semiconductors"],
                event_type="customer win", route="new_idea",
                summary="DPHO 拿到云厂商 2027-2029 年 1.6T 激光器二供合同，值得深度研究"))
        elif item_id == BAD_NEWS:
            results.append(TriageResult(
                item_id=item_id, materiality=9, tickers=[TICKER], industries=["Semiconductors"],
                event_type="customer loss", route="thesis_check",
                summary="DPHO 最大客户（占收入 41%）2027 年起自研激光器，公司下调指引"))
    return TriageBatch(results=results)


def _memo(system: str, prompt: str) -> str:
    if "quality control" in system:
        return "审核：数据均有出处，两处口径需要注明。\n\nVERDICT: PASS WITH MINOR REVISIONS"
    if "contrarian" in system:
        return ("反方观点：客户集中度高是最大风险。\n证伪条件：最大客户转向自研或引入第三家供应商；"
                "毛利率连续两个季度低于 40%。")
    return "研究员 memo：DPHO 是 1.6T EML 激光器的第二供应商，产能已预订到 2028 年。"


def _thesis(system: str, prompt: str) -> ThesisDraft:
    return ThesisDraft(
        ticker=TICKER, company="Demo Photonics Inc.", industry="Semiconductors", direction="long",
        summary="1.6T 光模块放量，DPHO 作为 EML 激光器二供，未来三年收入有望翻倍。",
        pillars=[
            Pillar(claim="大客户合同在 2027-2029 年如期执行", evidence="合同公告", status="intact"),
            Pillar(claim="EML 激光器毛利率维持 45% 以上", evidence="近四个季度财报", status="intact"),
            Pillar(claim="1.6T 光模块 2027 年出货量翻倍", evidence="行业预测", status="intact"),
        ],
        kill_criteria=["最大客户转向自研或引入第三家供应商", "毛利率连续两个季度低于 40%"],
        catalysts=["下季度财报", "客户 1.6T 放量"], key_risks=["客户集中度", "技术路线切换"],
        fair_value=68.0, max_entry_price=58.0, conviction=78,
        reviewer_verdict="PASS_WITH_MINOR_REVISIONS", evidence_doc_ids=[],
    )


def _assessment(system: str, prompt: str) -> ThesisAssessment:
    return ThesisAssessment(
        pillar_updates=[PillarUpdate(index=0, status="broken", reason="最大客户 2027 年起自研")],
        kill_criteria_hit=[0], conviction_delta=-45,
        note="最大客户转向自研，第一条证伪条件被触发，收入支柱不成立。", needs_full_refresh=False,
    )


def demo_provider() -> FakeProvider:
    return FakeProvider(
        structured={
            "TriageBatch": _triage,
            "ThesisDraft": _thesis,
            "ThesisAssessment": _assessment,
            "IndustryScan": lambda s, p: IndustryScan(industries=[]),
            "CandidateRanking": lambda s, p: CandidateRanking(candidates=[]),
        },
        text=_memo,
    )


def demo_settings(workdir: Path) -> Settings:
    settings = Settings()
    settings.base_dir = workdir
    settings.sources.fmp_news = False
    settings.universe.themes = ["AI 光通信"]
    for stage in settings.llm.STAGES:
        getattr(settings.llm, stage).provider = "fake"
    return settings


def run_demo(workdir: Path | None = None, say: Callable[[str], None] = print) -> TradingBot:
    workdir = workdir or Path(tempfile.mkdtemp(prefix="tradebot-demo-"))
    bot = build_bot(demo_settings(workdir), providers={"fake": demo_provider()}, fmp=DemoFMP(),
                    news_sources=[ScriptedNews(demo_news())])

    say(f"演示目录：{workdir}（模拟盘，初始资金 $1,000,000）\n")
    say("① 新闻进来：DPHO 拿下云厂商大合同")
    bot.poll_news()
    idea = bot.store.next_idea()
    say(f"   分诊结果：重要性高，放入研究队列（优先级 {idea['priority']}）\n")

    say("② 深度研究：研究员 -> 反方 -> 审核 -> PM 定论")
    bot.work_research_queue()
    thesis = bot.store.get_thesis(TICKER)
    say(f"   thesis：conviction {thesis.conviction}，审核 {thesis.reviewer_verdict}，状态 {thesis.status}")
    say(f"   退出条件：{'；'.join(thesis.kill_criteria)}\n")

    order = bot.store.orders("pending_approval")[0]
    say("③ 风控通过，生成订单，等你审批")
    say(f"   {order.side} {order.quantity} 股 @ {order.limit_price}（{order.reason[:40]}...）")
    bot.desk.approve(order.id)
    account = bot.broker.account()
    say(f"   你批准后成交。持仓 {account.qty(TICKER):g} 股，占净值 {account.weight_pct(TICKER):.1f}%\n")

    say("④ 新闻打脸：最大客户转向自研")
    bot.poll_news()
    thesis = bot.store.get_thesis(TICKER)
    say(f"   thesis 更新：conviction {thesis.history[-1].conviction_before} -> {thesis.conviction}，状态 {thesis.status}")
    say(f"   原因：{thesis.history[-1].note}\n")

    exit_order = bot.store.orders("pending_approval")[0]
    say(f"⑤ 自动生成清仓单：{exit_order.side} {exit_order.quantity} 股，审批后成交")
    bot.desk.approve(exit_order.id)
    account = bot.broker.account()
    say(f"   持仓 {account.qty(TICKER):g} 股，账户净值 ${account.nav:,.0f}（手续费已扣）\n")
    say("演示结束。真实运行时，数据来自 FMP / Grok / 你的研报文件夹；深度研究走你的订阅"
        "（Claude Code 或 Codex），新闻分诊这类全天候的小任务走便宜的 API 模型。")
    return bot
