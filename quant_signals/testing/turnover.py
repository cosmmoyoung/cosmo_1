"""Gate 4 — turnover & transaction-cost analysis.

Builds dollar-neutral weights from a signal, computes annualized turnover, a
square-root market-impact cost, gross vs net Sharpe, and the breakeven cost
(bps at which alpha -> 0). Also a crude capacity estimate.
"""
from __future__ import annotations
from typing import Dict
import numpy as np
import pandas as pd

from config import CONFIG


def signal_to_weights(signal: pd.DataFrame, gross: float = 1.0) -> pd.DataFrame:
    """Cross-sectional demean -> L1-normalize to dollar-neutral, gross exposure=gross."""
    w = signal.sub(signal.mean(axis=1), axis=0)
    l1 = w.abs().sum(axis=1)
    return w.div(l1.replace(0, np.nan), axis=0).fillna(0) * gross


def annualized_turnover(weights: pd.DataFrame, returns: pd.DataFrame) -> float:
    """0.5 * sum|w_t - w_{t-1} drifted| averaged, annualized."""
    drifted = (weights.shift(1) * (1 + returns)).div(
        (weights.shift(1) * (1 + returns)).abs().sum(axis=1).replace(0, np.nan),
        axis=0).fillna(0)
    trades = (weights - drifted).abs().sum(axis=1) * 0.5
    return float(trades.mean() * CONFIG.trading_days_per_year)


def impact_cost_bps(weights: pd.DataFrame, returns: pd.DataFrame,
                    aum_usd: float, dollar_volume: pd.DataFrame) -> pd.Series:
    """Per-day weighted cost in bps using half-spread + sqrt impact."""
    c = CONFIG.cost
    vol = returns.rolling(21).std().fillna(returns.std())
    trade = (weights - weights.shift(1)).abs()
    notional = trade * aum_usd
    adv = dollar_volume.rolling(21).mean()
    participation = (notional / adv.replace(0, np.nan)).clip(upper=c.max_participation)
    impact = c.impact_coef_k * vol * np.sqrt(participation.fillna(0)) * 1e4  # bps
    per_name_bps = c.half_spread_bps + impact
    # weight by traded fraction
    day_cost = (trade * per_name_bps).sum(axis=1) / trade.sum(axis=1).replace(0, np.nan)
    return day_cost.fillna(0)


def gross_net_sharpe(weights: pd.DataFrame, returns: pd.DataFrame,
                     dollar_volume: pd.DataFrame, aum_usd: float = 1e8
                     ) -> Dict[str, float]:
    ann = np.sqrt(CONFIG.trading_days_per_year)
    fwd = returns.shift(-1)
    pnl_gross = (weights * fwd).sum(axis=1)
    # cost charged on traded notional fraction each day (bps -> return)
    trade_frac = (weights - weights.shift(1)).abs().sum(axis=1) * 0.5
    cost_bps = impact_cost_bps(weights, returns, aum_usd, dollar_volume)
    cost_ret = trade_frac * cost_bps / 1e4
    pnl_net = pnl_gross - cost_ret
    gsr = pnl_gross.mean() / (pnl_gross.std() + 1e-12) * ann
    nsr = pnl_net.mean() / (pnl_net.std() + 1e-12) * ann
    # breakeven cost: bps that drives mean net pnl to zero
    mean_trade = trade_frac.mean()
    breakeven_bps = (pnl_gross.mean() / (mean_trade + 1e-12)) * 1e4
    modeled_cost_bps = cost_bps.replace(0, np.nan).mean()
    return {"gross_sharpe": float(gsr), "net_sharpe": float(nsr),
            "breakeven_bps": float(breakeven_bps),
            "modeled_cost_bps": float(modeled_cost_bps),
            "breakeven_multiple": float(breakeven_bps / (modeled_cost_bps + 1e-9))}


def estimate_capacity(weights: pd.DataFrame, returns: pd.DataFrame,
                      dollar_volume: pd.DataFrame,
                      target_net_sr: float = None) -> float:
    """Largest AUM keeping net SR >= target (house min). Coarse line search."""
    target = target_net_sr or CONFIG.gates.min_net_sharpe
    last = 0.0
    for aum in [5e7, 1e8, 2.5e8, 5e8, 1e9, 2.5e9, 5e9, 1e10]:
        nsr = gross_net_sharpe(weights, returns, dollar_volume, aum)["net_sharpe"]
        if nsr >= target:
            last = aum
        else:
            break
    return last


def run_turnover_analysis(signals: Dict[str, pd.DataFrame], specs, md,
                          aum_usd: float = 1e8) -> pd.DataFrame:
    g = CONFIG.gates
    rows = []
    for name, sig in signals.items():
        w = signal_to_weights(sig)
        to = annualized_turnover(w, md.returns)
        sr = gross_net_sharpe(w, md.returns, md.dollar_volume, aum_usd)
        cap = estimate_capacity(w, md.returns, md.dollar_volume)
        passes = (sr["net_sharpe"] > g.min_net_sharpe and
                  sr["breakeven_multiple"] > g.min_breakeven_cost_multiple)
        rows.append({"name": name, "family": specs[name].family,
                     "ann_turnover": to,
                     "gross_sharpe": sr["gross_sharpe"],
                     "net_sharpe": sr["net_sharpe"],
                     "breakeven_bps": sr["breakeven_bps"],
                     "modeled_cost_bps": sr["modeled_cost_bps"],
                     "capacity_usd": cap,
                     "cost_pass": passes})
    return pd.DataFrame(rows).sort_values("net_sharpe", ascending=False).reset_index(drop=True)
