"""Hard risk rules checked on every order, at proposal time and again at approval time.

Selling what you own always reduces risk, so SELL orders only face the global
switches and price sanity checks. BUY orders face everything.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from tradebot.config import Settings
from tradebot.models import AccountSnapshot, OrderProposal, Quote, Thesis

EPS = 1e-6


@dataclass
class RiskDecision:
    violations: list[str] = field(default_factory=list)

    @property
    def approved(self) -> bool:
        return not self.violations


class RiskEngine:
    def __init__(self, settings: Settings, stop_file: Path):
        self.settings = settings
        self.stop_file = stop_file

    def check(self, order: OrderProposal, thesis: Thesis | None, account: AccountSnapshot,
              quote: Quote | None, *, buys_today: int, docs_cleared: dict[str, bool],
              industries: dict[str, str]) -> RiskDecision:
        risk, research = self.settings.risk, self.settings.research
        d = RiskDecision()
        v = d.violations

        # Global switches.
        if self.stop_file.exists():
            v.append(f"紧急停止开关已打开（{self.stop_file.name} 文件存在）")
        if not risk.trading_enabled:
            v.append("config 里 risk.trading_enabled 是 false")

        # Order sanity.
        if order.quantity <= 0:
            v.append("下单数量必须大于 0")
        if quote is None:
            v.append("拿不到最新报价，无法核对价格")
        else:
            deviation = abs(order.limit_price / quote.price - 1) * 100
            if deviation > risk.max_price_deviation_pct:
                v.append(f"限价 {order.limit_price} 偏离现价 {quote.price} 达 {deviation:.1f}%，"
                         f"超过 {risk.max_price_deviation_pct}%（防乌龙指）")

        held = account.qty(order.ticker)
        if order.side == "SELL":
            if risk.long_only and order.quantity > held + EPS:
                v.append(f"只做多：卖出 {order.quantity} 股超过持仓 {held:g} 股")
            return d

        # BUY: research gate.
        if buys_today >= risk.max_orders_per_day:
            v.append(f"今天已买入 {buys_today} 次，达到上限 {risk.max_orders_per_day}")
        if thesis is None:
            v.append("没有对应的 thesis，不允许买入")
        else:
            if thesis.status != "active":
                v.append(f"thesis 状态是 {thesis.status}，不是 active")
            if thesis.direction != "long":
                v.append(f"thesis 方向是 {thesis.direction}，不是做多")
            if thesis.reviewer_verdict not in research.allowed_verdicts:
                v.append(f"研究审核结论 {thesis.reviewer_verdict} 不在允许范围 {research.allowed_verdicts}")
            if held <= 0 and thesis.conviction < research.open_conviction:
                v.append(f"conviction {thesis.conviction} 低于开仓门槛 {research.open_conviction}")
            if risk.require_compliance_cleared:
                uncleared = [doc for doc in thesis.evidence_doc_ids if not docs_cleared.get(doc, False)]
                if uncleared:
                    v.append(f"thesis 引用了未经合规确认的材料 {uncleared}（可能含内幕信息）")
            if quote and thesis.max_entry_price is not None and quote.price > thesis.max_entry_price:
                v.append(f"现价 {quote.price} 高于 thesis 的最高买入价 {thesis.max_entry_price}")

        # BUY: market and account limits.
        universe = self.settings.universe
        if quote and quote.market_cap is not None and quote.market_cap < universe.min_market_cap_usd:
            v.append(f"市值 {quote.market_cap / 1e9:.1f}bn 低于下限 {universe.min_market_cap_usd / 1e9:.1f}bn")
        if order.notional < risk.min_order_value:
            v.append(f"订单金额 {order.notional:,.0f} 低于最小金额 {risk.min_order_value:,.0f}")
        if account.day_pnl_pct is not None and account.day_pnl_pct <= -risk.max_daily_loss_pct:
            v.append(f"今日亏损 {account.day_pnl_pct:.1f}% 已达上限 {risk.max_daily_loss_pct}%，暂停买入")
        if account.nav <= 0:
            v.append("账户净值不为正")
            return d

        new_value = account.value(order.ticker) + order.notional
        weight = 100 * new_value / account.nav
        if weight > risk.max_position_pct + EPS:
            v.append(f"买入后单票仓位 {weight:.1f}% 超过上限 {risk.max_position_pct}%")

        industry = industries.get(order.ticker) or (thesis.industry if thesis else "")
        if industry:
            same_industry = sum(
                p.value for t, p in account.positions.items()
                if t != order.ticker and industries.get(t) == industry
            )
            industry_weight = 100 * (same_industry + new_value) / account.nav
            if industry_weight > risk.max_industry_pct + EPS:
                v.append(f"买入后 {industry} 行业仓位 {industry_weight:.1f}% 超过上限 {risk.max_industry_pct}%")

        leverage = (account.gross_exposure + order.notional) / account.nav
        if leverage > risk.max_gross_leverage + EPS:
            v.append(f"买入后总仓位 {leverage:.2f} 倍净值，超过上限 {risk.max_gross_leverage} 倍")
        if risk.max_gross_leverage <= 1.0 and order.notional > account.cash + EPS:
            v.append(f"现金 {account.cash:,.0f} 不够买 {order.notional:,.0f}（不加杠杆）")

        positions_after = len(account.positions) + (0 if held > 0 else 1)
        if positions_after > risk.max_positions:
            v.append(f"持仓数量将达 {positions_after}，超过上限 {risk.max_positions}")
        return d
