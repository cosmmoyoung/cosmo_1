"""Signal catalog (§4). Each function maps MarketData -> a raw feature panel.

The orchestrator runs these through features.build_signal() for neutralization
and rank-normalization. Sign convention (higher = predicted higher fwd return)
is set in the registry so build_signal flips where needed.
"""
from __future__ import annotations
from typing import Callable, Dict, NamedTuple
import numpy as np
import pandas as pd

from data.loader import MarketData


# ---------------------------------------------------------------- price/volume
def momentum_12_1(md: MarketData) -> pd.DataFrame:
    """Cumulative return from t-252 to t-21 (skip last month)."""
    p = md.prices
    return p.shift(21) / p.shift(252) - 1.0


def idiosyncratic_momentum(md: MarketData) -> pd.DataFrame:
    """Momentum of returns residualized against market + sector (crash-robust)."""
    r = md.returns
    mkt = r.mean(axis=1)
    resid = r.sub(mkt, axis=0)  # cheap market neutralization
    cum = (1 + resid).rolling(231).apply(np.prod, raw=True) - 1
    return cum.shift(21)


def short_term_reversal(md: MarketData) -> pd.DataFrame:
    """-(5-day return). Higher (more negative past) -> higher fwd return => sign -1."""
    return md.prices.pct_change(5)


def high_52w_proximity(md: MarketData) -> pd.DataFrame:
    p = md.prices
    return p / p.rolling(252, min_periods=60).max()


def vol_scaled_momentum(md: MarketData) -> pd.DataFrame:
    mom = momentum_12_1(md)
    vol = md.returns.rolling(63).std() * np.sqrt(252)
    return mom / (vol + 1e-9)


# --------------------------------------------------------------- microstructure
def amihud_illiquidity(md: MarketData) -> pd.DataFrame:
    """Mean |return| / dollar volume over 21d. Illiquidity premium => sign +1."""
    illiq = (md.returns.abs() / (md.dollar_volume + 1e-9))
    return illiq.rolling(21).mean()


def intraday_reversal_proxy(md: MarketData) -> pd.DataFrame:
    """Proxy without OHLC: -(1-day return) as overnight-reversal stand-in => sign -1."""
    return md.returns


def realized_vol_asym(md: MarketData) -> pd.DataFrame:
    """Downside minus upside semivariance over 21d (crash-risk premium)."""
    r = md.returns
    down = r.clip(upper=0) ** 2
    up = r.clip(lower=0) ** 2
    return down.rolling(21).mean() - up.rolling(21).mean()


# ----------------------------------------------------------- fundamental/earnings
def sue_drift(md: MarketData) -> pd.DataFrame:
    """Standardized unexpected earnings panel from raw (PEAD). Higher -> higher."""
    if "sue_surprise" in md.raw:
        return md.raw["sue_surprise"]
    # fallback proxy: earnings-less environments -> use mom as weak stand-in
    return momentum_12_1(md)


# ------------------------------------------------------------------- alt-data
def news_sentiment(md: MarketData) -> pd.DataFrame:
    if "news_sentiment" in md.raw:
        return md.raw["news_sentiment"]
    return md.returns.rolling(5).mean()


def options_skew(md: MarketData) -> pd.DataFrame:
    if "options_skew" in md.raw:
        return md.raw["options_skew"]
    return -md.returns.rolling(10).std()


class SignalSpec(NamedTuple):
    fn: Callable[[MarketData], pd.DataFrame]
    family: str
    sign: float          # +1 or -1 to enforce "higher = higher fwd return"
    horizon: int         # nominal holding horizon (days) for the test
    neutralize: bool


REGISTRY: Dict[str, SignalSpec] = {
    # name:           function,            family,           sign, horizon, neutralize
    "idio_momentum":  SignalSpec(idiosyncratic_momentum, "price_volume", +1, 21, True),
    "momentum_12_1":  SignalSpec(momentum_12_1,          "price_volume", +1, 21, True),
    "st_reversal":    SignalSpec(short_term_reversal,    "price_volume", -1, 5,  True),
    "high_52w":       SignalSpec(high_52w_proximity,     "price_volume", +1, 21, True),
    "vol_scaled_mom": SignalSpec(vol_scaled_momentum,    "price_volume", +1, 21, True),
    "amihud_illiq":   SignalSpec(amihud_illiquidity,     "microstructure", +1, 10, True),
    "intraday_rev":   SignalSpec(intraday_reversal_proxy,"microstructure", -1, 1,  True),
    "rv_asymmetry":   SignalSpec(realized_vol_asym,      "microstructure", +1, 10, True),
    "pead_sue":       SignalSpec(sue_drift,              "fundamental",  +1, 21, True),
    "news_sentiment": SignalSpec(news_sentiment,         "alt_data",     +1, 5,  True),
    "options_skew":   SignalSpec(options_skew,           "alt_data",     +1, 10, True),
}
