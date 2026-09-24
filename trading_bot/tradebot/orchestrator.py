"""The bot: wires sources, research, risk and execution into one loop.

One cycle:
  1. poll news (inbox, FMP, Grok) -> triage -> route to open theses or the idea queue
  2. open theses touched by news are re-assessed; conviction changes resize or exit
  3. once a day: industry scan -> company screen -> idea queue; re-check prices
  4. work the idea queue (deep dives, capped per day); good theses become orders
Every order goes through OrderDesk: risk engine -> approval -> broker.
"""

from __future__ import annotations

import logging
import os
import time
from collections import defaultdict
from datetime import timedelta
from typing import Callable

from tradebot.config import Settings
from tradebot.execution import Broker
from tradebot.llm import LLMRouter, Provider
from tradebot.models import NewsItem, OrderProposal, Quote, Thesis, iso, parse_iso, utcnow
from tradebot.notify import Notifier
from tradebot.research.deep_dive import DeepDive
from tradebot.research.industry import scan_industries
from tradebot.research.screener import in_universe, screen_industry
from tradebot.research.thesis_update import apply_assessment, assess_thesis
from tradebot.research.triage import triage_items
from tradebot.risk.engine import RiskDecision, RiskEngine
from tradebot.risk.sizing import plan_order
from tradebot.sources import NewsSource
from tradebot.sources.inbox import InboxSource
from tradebot.store import Store

log = logging.getLogger(__name__)

NEWS_OVERLAP = timedelta(hours=2)
DEAD_ORDER_STATUSES = ("cancelled", "apicancelled", "inactive", "rejected")


def safe_quote(fmp) -> Callable[[str], Quote | None]:
    """A quote lookup that returns None instead of raising, so one bad ticker never stops a cycle."""
    def quote(ticker: str) -> Quote | None:
        try:
            return fmp.quote(ticker)
        except Exception as exc:
            log.warning("quote %s failed: %s", ticker, exc)
            return None
    return quote


class OrderDesk:
    """Every order passes here: risk check -> approval -> broker."""

    def __init__(self, settings: Settings, store: Store, broker: Broker, risk: RiskEngine,
                 quote: Callable[[str], Quote | None], notifier: Notifier, clock=utcnow):
        self.settings = settings
        self.store = store
        self.broker = broker
        self.risk = risk
        self.quote = quote
        self.notifier = notifier
        self.clock = clock

    def _check(self, order: OrderProposal, thesis: Thesis | None) -> RiskDecision:
        account = self.broker.account()
        docs_cleared = {}
        for doc_id in thesis.evidence_doc_ids if thesis else []:
            doc = self.store.get_document(doc_id)
            docs_cleared[doc_id] = bool(doc and doc.compliance_cleared)
        return self.risk.check(
            order, thesis, account, self.quote(order.ticker),
            buys_today=self.store.count("buys", self.clock().date().isoformat()),
            docs_cleared=docs_cleared,
            industries={t.ticker: t.industry for t in self.store.theses()},
        )

    def _save(self, order: OrderProposal) -> OrderProposal:
        order.updated_at = iso(self.clock())
        self.store.save_order(order)
        return order

    def _auto_approved(self, order: OrderProposal) -> bool:
        cfg = self.settings.execution
        if cfg.auto_approve_exits and order.side == "SELL":
            return True
        if cfg.approval != "auto":
            return False
        return not self.broker.is_live or os.environ.get("TRADEBOT_AUTO_LIVE") == "YES"

    def submit(self, order: OrderProposal, thesis: Thesis | None) -> OrderProposal:
        decision = self._check(order, thesis)
        if not decision.approved:
            order.status = "rejected"
            order.risk_notes = decision.violations
            self.notifier.send(f"风控拒绝 {order.side} {order.quantity} {order.ticker}", "\n".join(decision.violations))
            return self._save(order)
        if self._auto_approved(order):
            return self._execute(order)
        order.status = "pending_approval"
        self._save(order)
        self.notifier.send(
            f"待审批：{order.side} {order.quantity} {order.ticker} @ {order.limit_price}",
            f"{order.reason}\n批准：tradebot approve {order.id}\n拒绝：tradebot reject {order.id}",
        )
        return order

    def approve(self, order_id: str) -> OrderProposal:
        order = self.store.get_order(order_id)
        if order is None:
            raise ValueError(f"找不到订单 {order_id}")
        if order.status != "pending_approval":
            raise ValueError(f"订单 {order.id} 的状态是 {order.status}，不能批准")
        # Prices and limits may have moved since the proposal: check again with fresh data.
        decision = self._check(order, self.store.get_thesis(order.ticker))
        if not decision.approved:
            order.status = "rejected"
            order.risk_notes = decision.violations
            self.notifier.send(f"批准时风控复核未通过：{order.ticker}", "\n".join(decision.violations))
            return self._save(order)
        return self._execute(order)

    def reject(self, order_id: str, reason: str = "人工拒绝") -> OrderProposal:
        order = self.store.get_order(order_id)
        if order is None or order.status != "pending_approval":
            raise ValueError(f"找不到待审批订单 {order_id}")
        order.status = "cancelled"
        order.risk_notes.append(reason)
        return self._save(order)

    def expire_stale(self) -> int:
        cutoff = self.clock() - timedelta(hours=self.settings.schedule.approval_ttl_hours)
        expired = 0
        for order in self.store.orders("pending_approval"):
            created = parse_iso(order.created_at)
            if created and created < cutoff:
                order.status = "expired"
                self._save(order)
                expired += 1
        return expired

    def sync_submitted(self) -> None:
        for order in self.store.orders("submitted"):
            result = self.broker.order_status(order.broker_order_id or "")
            if result is None:
                continue
            order.filled_qty = result.filled_qty
            order.avg_fill_price = result.avg_price
            if result.filled_qty >= order.quantity:
                order.status = "filled"
            elif result.status.lower().startswith(DEAD_ORDER_STATUSES):
                order.status = "cancelled"
            self._save(order)

    def _execute(self, order: OrderProposal) -> OrderProposal:
        try:
            result = self.broker.place_limit_order(order.ticker, order.side, order.quantity, order.limit_price)
        except Exception as exc:
            order.status = "failed"
            order.risk_notes.append(f"下单失败：{exc}")
            self.notifier.send(f"下单失败：{order.ticker}", str(exc))
            return self._save(order)
        order.broker_order_id = result.broker_order_id
        order.filled_qty = result.filled_qty
        order.avg_fill_price = result.avg_price
        if result.filled_qty >= order.quantity:
            order.status = "filled"
        elif result.status.lower().startswith(DEAD_ORDER_STATUSES):
            order.status = "cancelled"
            order.risk_notes.append(f"券商返回：{result.status}")
        else:
            order.status = "submitted"
        if order.side == "BUY" and order.status in ("filled", "submitted"):
            self.store.bump("buys", self.clock().date().isoformat())
        self.notifier.send(
            f"{'已成交' if order.status == 'filled' else order.status}：{order.side} {order.quantity} {order.ticker}",
            f"券商 {self.broker.name}，订单号 {order.broker_order_id}，均价 {order.avg_fill_price}",
        )
        return self._save(order)


class TradingBot:
    def __init__(self, settings: Settings, store: Store, router: LLMRouter, fmp, broker: Broker,
                 news_sources: list[NewsSource], inbox: InboxSource, notifier: Notifier, clock=utcnow):
        self.settings = settings
        self.store = store
        self.router = router
        self.fmp = fmp
        self.broker = broker
        self.news_sources = news_sources
        self.inbox = inbox
        self.notifier = notifier
        self.clock = clock
        self.quote = safe_quote(fmp)
        self.risk = RiskEngine(settings, settings.stop_file)
        self.desk = OrderDesk(settings, store, broker, self.risk, self.quote, notifier, clock)
        self.deep_dive = DeepDive(router, fmp, store, inbox, settings)

    # ------------------------------------------------------------------ helpers
    def halted(self) -> bool:
        return self.settings.stop_file.exists()

    def _today(self) -> str:
        return self.clock().date().isoformat()

    # ------------------------------------------------------------------ 1-2: news
    def poll_news(self) -> int:
        now = self.clock()
        last = parse_iso(self.store.get_meta("news_since")) or now - timedelta(hours=24)
        # Overlap the window: feeds publish some items late. Dedupe drops the repeats.
        since = last - NEWS_OVERLAP
        items: dict[str, NewsItem] = {}
        for source in [self.inbox, *self.news_sources]:
            try:
                for item in source.fetch(since):
                    items.setdefault(item.id, item)
            except Exception as exc:  # one broken feed must not stop the others
                log.warning("news source %s failed: %s", source.name, exc)
                self.store.log("source_error", f"{source.name}: {exc}")
        fresh = [item for item in items.values() if not self.store.is_seen(item.id)]
        if not fresh:
            self.store.set_meta("news_since", iso(now))
            return 0

        open_theses = self.store.theses("active", "watch")
        open_tickers = {t.ticker for t in open_theses}
        results = triage_items(self.router, fresh, open_theses, self.settings.universe.themes)
        touched: dict[str, list[NewsItem]] = defaultdict(list)
        threshold = self.settings.research.materiality_threshold
        for item, result in results:
            self.store.save_news(item, result)
            self.store.mark_seen(item.id)
            if item.doc_id and result.tickers:
                self.store.add_document_tickers(item.doc_id, result.tickers)
            if result.route == "ignore" or result.materiality < threshold:
                continue
            for ticker in result.tickers:
                if ticker in open_tickers and result.route in ("thesis_check", "both"):
                    touched[ticker].append(item)
                elif ticker not in open_tickers and result.route in ("new_idea", "both") \
                        and in_universe(ticker, self.settings.universe):
                    self.store.enqueue_idea(ticker, result.summary, f"news:{item.source}", result.materiality * 10)
        self.store.set_meta("news_since", iso(now))
        for ticker, news in touched.items():
            try:
                self.review_thesis(ticker, news)
            except Exception as exc:  # the news is already marked seen, so tell a human
                log.exception("thesis review %s failed", ticker)
                self.notifier.send(f"{ticker} thesis 复核失败，请人工查看", "\n".join(n.title for n in news) + f"\n{exc}")
        return len(fresh)

    def review_thesis(self, ticker: str, news: list[NewsItem]) -> Thesis | None:
        thesis = self.store.get_thesis(ticker)
        if thesis is None or thesis.status == "closed":
            return None
        assessment = assess_thesis(self.router, thesis, news)
        updated = apply_assessment(
            thesis, assessment, trigger=",".join(n.id for n in news),
            research=self.settings.research, now=self.clock(), long_only=self.settings.risk.long_only,
        )
        self.store.upsert_thesis(updated)
        if (updated.conviction, updated.status) != (thesis.conviction, thesis.status):
            self.notifier.send(
                f"{ticker} thesis 更新：conviction {thesis.conviction} -> {updated.conviction}，状态 {updated.status}",
                updated.history[-1].note,
            )
        if assessment.needs_full_refresh and updated.status != "closed":
            self.store.enqueue_idea(ticker, f"重大变化，重做深度研究：{assessment.note}", "refresh", 95, force=True)
        self.rebalance(updated)
        return updated

    # ------------------------------------------------------------------ 3: daily funnel
    def daily_due(self) -> bool:
        now = self.clock()
        return now.hour >= self.settings.schedule.daily_scan_hour_utc and \
            self.store.get_meta("daily_scan_day") != self._today()

    def daily_scan(self) -> int:
        sched = self.settings.schedule
        scan = scan_industries(
            self.router, self.fmp, self.store, self.settings.universe.themes,
            self.store.theses("active", "watch"), self.clock().date(),
        )
        self.store.save_industry_scan(self._today(), scan)
        skip = {t.ticker for t in self.store.theses()}
        queued = 0
        for view in scan.industries[:sched.top_industries]:
            if view.stance == "underweight":
                continue
            try:
                ranking = screen_industry(self.router, self.fmp, view, self.settings.universe, skip)
            except Exception as exc:
                log.warning("screen %s failed: %s", view.industry, exc)
                continue
            for candidate in ranking.candidates[:sched.candidates_per_industry]:
                if self.store.enqueue_idea(candidate.ticker, f"[{view.industry}] {candidate.why}", "screen", candidate.score):
                    queued += 1
        # Prices move: an active thesis may now be below its max entry price, a closed one may still be held.
        for thesis in self.store.theses("active", "closed"):
            try:
                self.rebalance(thesis)
            except Exception as exc:
                log.warning("rebalance %s failed: %s", thesis.ticker, exc)
        self.store.set_meta("daily_scan_day", self._today())
        return queued

    # ------------------------------------------------------------------ 4: deep dives
    def research(self, ticker: str, reason: str) -> Thesis:
        self.store.enqueue_idea(ticker, reason, "manual", 100, force=True)
        self.store.set_idea_status(ticker, "researching")
        try:
            thesis = self.deep_dive.run(ticker, reason)
        except Exception:
            self.store.set_idea_status(ticker, "failed")
            raise
        self.store.set_idea_status(ticker, "researched")
        self.store.bump("deep_dives", self._today())
        self.notifier.send(
            f"深度研究完成：{ticker}，conviction {thesis.conviction}，审核 {thesis.reviewer_verdict}，状态 {thesis.status}",
            thesis.summary,
        )
        self.rebalance(thesis)
        return thesis

    def work_research_queue(self) -> int:
        done = 0
        universe = self.settings.universe
        while self.store.count("deep_dives", self._today()) < self.settings.schedule.max_deep_dives_per_day:
            idea = self.store.next_idea()
            if idea is None:
                break
            ticker = idea["ticker"]
            quote = self.quote(ticker)
            if not in_universe(ticker, universe) or quote is None or quote.price < universe.min_price \
                    or (quote.market_cap or 0) < universe.min_market_cap_usd:
                self.store.set_idea_status(ticker, "skipped")
                continue
            try:
                self.research(ticker, idea["reason"])
                done += 1
            except Exception as exc:
                # Stop for this cycle: if the cause is systemic (API key, outage) we should not
                # burn through the whole queue marking every idea as failed.
                log.exception("deep dive %s failed", ticker)
                self.store.log("research_error", f"{ticker}: {exc}")
                break
        return done

    # ------------------------------------------------------------------ orders
    def rebalance(self, thesis: Thesis) -> OrderProposal | None:
        if self.store.has_open_order(thesis.ticker):
            return None
        quote = self.quote(thesis.ticker)
        if quote is None:
            return None
        order = plan_order(thesis, self.broker.account(), quote, self.settings, self.clock(),
                           round_qty=self.broker.round_quantity)
        return self.desk.submit(order, thesis) if order else None

    # ------------------------------------------------------------------ loop
    def cycle(self) -> dict[str, int]:
        if self.halted():
            log.warning("STOP file present: skipping this cycle")
            return {"halted": 1}
        stats: dict[str, int] = {}
        steps = [
            ("synced", lambda: self.desk.sync_submitted() or 0),
            ("news", self.poll_news),
            ("screened", lambda: self.daily_scan() if self.daily_due() else 0),
            ("researched", self.work_research_queue),
            ("expired", self.desk.expire_stale),
        ]
        for name, step in steps:
            try:
                stats[name] = step()
            except Exception as exc:
                log.exception("step %s failed", name)
                self.store.log("cycle_error", f"{name}: {exc}")
                stats[name] = -1
        return stats

    def run_forever(self) -> None:
        interval = self.settings.schedule.news_poll_minutes * 60
        log.info("tradebot running: broker=%s approval=%s every %d min",
                 self.broker.name, self.settings.execution.approval, interval // 60)
        while True:
            started = time.monotonic()
            stats = self.cycle()
            log.info("cycle done: %s", stats)
            time.sleep(max(5.0, interval - (time.monotonic() - started)))


def make_providers(settings: Settings) -> dict[str, Provider]:
    tasks = ["triage", "industry", "screen", "research", "thesis"]
    if settings.sources.grok_scout:
        tasks.append("scout")
    wanted = {getattr(settings.llm, t).provider for t in tasks}
    providers: dict[str, Provider] = {}
    if "claude" in wanted:
        from tradebot.llm.claude import ClaudeProvider
        providers["claude"] = ClaudeProvider()
    if "grok" in wanted:
        from tradebot.llm.grok import GrokProvider
        providers["grok"] = GrokProvider(x_handles=settings.sources.grok_x_handles)
    return providers


def make_broker(settings: Settings, store: Store, quote: Callable[[str], Quote | None]) -> Broker:
    if settings.execution.broker == "ibkr":
        from tradebot.execution.ibkr import IBKRBroker
        return IBKRBroker(settings.execution)
    from tradebot.execution.paper import PaperBroker
    return PaperBroker(store, quote, settings.execution.paper_starting_cash)


def build_bot(settings: Settings, *, providers: dict[str, Provider] | None = None, fmp=None,
              broker: Broker | None = None, news_sources: list[NewsSource] | None = None,
              clock=utcnow) -> TradingBot:
    settings.data_path.mkdir(parents=True, exist_ok=True)
    store = Store(settings.db_path)
    notifier = Notifier(os.environ.get("TRADEBOT_WEBHOOK_URL"))
    if fmp is None:
        from tradebot.sources.fmp import FMPClient
        fmp = FMPClient()
    router = LLMRouter(settings.llm, providers if providers is not None else make_providers(settings))
    inbox = InboxSource(settings.path(settings.sources.inbox_dir), store)
    inbox.ensure_dirs()
    if news_sources is None:
        news_sources = []
        if settings.sources.fmp_news:
            from tradebot.sources.fmp import FMPNewsSource
            news_sources.append(FMPNewsSource(fmp, settings.universe.watchlist, settings.universe.min_market_cap_usd))
        if settings.sources.grok_scout:
            from tradebot.sources.grok_scout import GrokScoutSource
            news_sources.append(GrokScoutSource(
                router, settings.universe.watchlist, settings.universe.themes,
                lambda: [t.ticker for t in store.theses("active", "watch")],
            ))

    broker = broker or make_broker(settings, store, safe_quote(fmp))
    return TradingBot(settings, store, router, fmp, broker, news_sources, inbox, notifier, clock)
