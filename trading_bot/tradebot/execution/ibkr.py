"""Interactive Brokers via ib_async. TWS or IB Gateway must be running and logged in.

Safety: the default ports are the paper ones (TWS 7497, Gateway 4002). The live
ports (7496, 4001) are refused unless config `execution.allow_live: true` AND the
environment variable TRADEBOT_LIVE=YES are both set.

Status: written against the ib_async API but not yet exercised on a real
account. Run it on an IBKR paper account first and compare `tradebot portfolio`
with what TWS shows.
"""

from __future__ import annotations

import math
import os

from tradebot.config import ExecutionConfig
from tradebot.models import AccountSnapshot, OrderResult, Position, Side

LIVE_PORTS = {7496, 4001}


class IBKRBroker:
    name = "ibkr"

    def __init__(self, cfg: ExecutionConfig, ib=None):
        self.is_live = cfg.ibkr_port in LIVE_PORTS
        if self.is_live and not (cfg.allow_live and os.environ.get("TRADEBOT_LIVE") == "YES"):
            raise RuntimeError(
                "拒绝连接 IBKR 实盘端口：需要同时设置 execution.allow_live: true 和环境变量 TRADEBOT_LIVE=YES"
            )
        if ib is None:
            try:
                from ib_async import IB
            except ImportError as exc:
                raise RuntimeError("IBKR 需要 ib_async：pip install 'tradebot[ibkr]'") from exc
            ib = IB()
            ib.connect(cfg.ibkr_host, cfg.ibkr_port, clientId=cfg.ibkr_client_id, timeout=20)
        self.ib = ib
        self._contracts: dict = {}
        self._pnl = None

    def _contract(self, ticker: str):
        if ticker not in self._contracts:
            from ib_async import Stock

            # IBKR writes share classes with a space: BRK.B -> "BRK B".
            qualified = self.ib.qualifyContracts(Stock(ticker.replace(".", " "), "SMART", "USD"))
            if not qualified:
                raise RuntimeError(f"IBKR 找不到合约 {ticker}")
            self._contracts[ticker] = qualified[0]
        return self._contracts[ticker]

    def _usd_rate(self, base_currency: str) -> float:
        """Base-currency units per 1 USD (an IBKR Hong Kong account may be based in HKD)."""
        if base_currency == "USD":
            return 1.0
        for value in self.ib.accountValues():
            if value.tag == "ExchangeRate" and value.currency == "USD":
                return float(value.value)
        raise RuntimeError(f"找不到 USD 对 {base_currency} 的汇率，无法把净值换算成美元")

    def account(self) -> AccountSnapshot:
        summary = {v.tag: v for v in self.ib.accountSummary()}
        nav_base = float(summary["NetLiquidation"].value)
        rate = self._usd_rate(summary["NetLiquidation"].currency)
        positions = {}
        for item in self.ib.portfolio():
            contract = item.contract
            if contract.secType != "STK" or contract.currency != "USD":
                continue  # the bot only manages US stocks; everything else still counts in NAV
            ticker = contract.symbol.replace(" ", ".")
            positions[ticker] = Position(
                ticker=ticker, qty=float(item.position), avg_cost=float(item.averageCost),
                market_price=float(item.marketPrice),
            )
        return AccountSnapshot(
            nav=nav_base / rate,
            cash=float(summary["TotalCashValue"].value) / rate,
            positions=positions,
            day_pnl_pct=self._day_pnl_pct(nav_base),
        )

    def _day_pnl_pct(self, nav_base: float) -> float | None:
        try:
            if self._pnl is None:
                self._pnl = self.ib.reqPnL(self.ib.managedAccounts()[0])
                self.ib.sleep(1)
            daily = self._pnl.dailyPnL
        except Exception:
            return None
        if daily is None or math.isnan(daily) or nav_base - daily <= 0:
            return None
        return 100 * daily / (nav_base - daily)

    def round_quantity(self, ticker: str, quantity: int) -> int:
        return max(int(quantity), 0)

    def place_limit_order(self, ticker: str, side: Side, quantity: int, limit_price: float) -> OrderResult:
        from ib_async import LimitOrder

        trade = self.ib.placeOrder(self._contract(ticker), LimitOrder(side, quantity, limit_price, tif="DAY"))
        self.ib.sleep(2)
        return self._result(trade)

    def order_status(self, broker_order_id: str) -> OrderResult | None:
        for trade in self.ib.trades():
            if str(trade.order.orderId) == broker_order_id:
                return self._result(trade)
        return None

    @staticmethod
    def _result(trade) -> OrderResult:
        status = trade.orderStatus
        return OrderResult(
            broker_order_id=str(trade.order.orderId),
            status=status.status or "Submitted",
            filled_qty=float(status.filled or 0),
            avg_price=float(status.avgFillPrice) if status.avgFillPrice else None,
        )
