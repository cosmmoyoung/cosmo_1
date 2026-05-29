"""Data loading with two backends behind one interface.

  - SyntheticBackend: generates a panel of prices/volumes/fundamentals with
    *known ground-truth alphas embedded*, so each statistical test can be
    verified to recover the planted signal. No network required.
  - LiveBackend: pulls free data via yfinance (OHLCV) and derives what it can;
    falls back to synthetic automatically if yfinance is missing or offline.

Output contract (a `MarketData` bundle), all indexed [date x ticker]:
    prices, returns, volume, dollar_volume, market_cap, plus a dict of
    raw fundamental/alt panels, plus a `forward_return(h)` helper.
"""
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Optional
import numpy as np
import pandas as pd


@dataclass
class MarketData:
    prices: pd.DataFrame
    volume: pd.DataFrame
    market_cap: pd.DataFrame
    sector: pd.Series                       # ticker -> sector id
    raw: Dict[str, pd.DataFrame] = field(default_factory=dict)  # extra panels
    truth: Dict[str, pd.DataFrame] = field(default_factory=dict)  # planted alphas (synthetic only)

    @property
    def returns(self) -> pd.DataFrame:
        return self.prices.pct_change()

    @property
    def dollar_volume(self) -> pd.DataFrame:
        return self.prices * self.volume

    def forward_return(self, h: int = 1) -> pd.DataFrame:
        """Forward simple return over the next h days, decision-time aligned.

        forward_return[t] = P[t+h]/P[t] - 1  (what a position opened on t earns).
        """
        return self.prices.shift(-h) / self.prices - 1.0


class SyntheticBackend:
    """Factor model + planted cross-sectional alphas.

    Return model per name i, day t:
        r = beta_i * market_t + sector_loading + idio_t
            + sum_k  payoff_k * alpha_feature_k[i, t-lag_k]   (the planted edge)
    The alpha features are stored in `truth` so tests can be validated, and the
    *observable* versions (with noise + realistic lags) are exposed in `raw`.
    """

    def __init__(self, n_assets: int = 300, n_days: int = 1500, n_sectors: int = 11,
                 seed: int = 42):
        self.n, self.T, self.S, self.seed = n_assets, n_days, n_sectors, seed

    def load(self) -> MarketData:
        rng = np.random.default_rng(self.seed)
        n, T, S = self.n, self.T, self.S
        dates = pd.bdate_range("2017-01-02", periods=T)
        tickers = [f"SY{idx:04d}" for idx in range(n)]
        sector = pd.Series(rng.integers(0, S, n), index=tickers, name="sector")

        # --- systematic structure ---
        beta = pd.Series(rng.normal(1.0, 0.3, n), index=tickers).clip(0.2, 2.0)
        market = rng.normal(0.0003, 0.011, T)                      # mkt daily return
        sector_ret = rng.normal(0, 0.006, (T, S))                   # sector factors
        idio = rng.normal(0, 0.014, (T, n))                         # idiosyncratic

        # --- plant ground-truth alpha features (each a [T x n] standardized panel) ---
        truth: Dict[str, pd.DataFrame] = {}

        def ar1_panel(rho: float, scale: float) -> np.ndarray:
            """Persistent latent feature (AR1) cross-sectionally standardized."""
            x = np.zeros((T, n))
            x[0] = rng.normal(0, scale, n)
            for t in range(1, T):
                x[t] = rho * x[t - 1] + rng.normal(0, scale * np.sqrt(1 - rho ** 2), n)
            # standardize cross-sectionally each day
            x = (x - x.mean(1, keepdims=True)) / (x.std(1, keepdims=True) + 1e-9)
            return x

        # momentum-like (slow, persistent), reversal-like (fast, mean-reverting),
        # earnings-surprise-like (sparse jumps), sentiment-like (noisy fast)
        mom = ar1_panel(0.98, 1.0)
        rev = ar1_panel(0.50, 1.0)
        sue = ar1_panel(0.90, 1.0)
        senti = ar1_panel(0.30, 1.0)

        # payoff per unit of standardized feature, scaled to realistic daily IC.
        # forward 1d return contribution ~ payoff * feature ; daily idio ~0.014.
        # Payoffs are made TIME-VARYING (AR(1) wobble that can flip sign in
        # adverse regimes) so the recovered IC is noisy day-to-day -> realistic
        # IC-IR (single digits, not 18) and a meaningful regime dependence.
        payoff_mean = {"mom": 0.0013, "rev": -0.0011, "sue": 0.0012, "senti": 0.0004}
        lags = {"mom": 1, "rev": 1, "sue": 1, "senti": 1}
        feats = {"mom": mom, "rev": rev, "sue": sue, "senti": senti}

        alpha_component = np.zeros((T, n))
        for k, f in feats.items():
            lag = lags[k]
            shifted = np.vstack([np.zeros((lag, n)), f[:-lag]]) if lag else f
            # gentle mean-reverting wobble: adds day-to-day IC noise + regime
            # structure (so IC-IR is not absurdly high) WITHOUT flipping the
            # planted sign — sd < mean and AR=0.90 keeps the time-average ~mean.
            sd = abs(payoff_mean[k]) * 0.5
            wobble = np.zeros(T)
            wobble[0] = rng.normal(0, sd)
            for t in range(1, T):
                wobble[t] = 0.90 * wobble[t - 1] + rng.normal(0, sd * np.sqrt(1 - 0.90 ** 2))
            daily_payoff = payoff_mean[k] + wobble
            alpha_component += daily_payoff[:, None] * shifted
            truth[k] = pd.DataFrame(f, index=dates, columns=tickers)

        # --- assemble returns ---
        ret = np.zeros((T, n))
        for t in range(T):
            ret[t] = (beta.values * market[t]
                      + sector_ret[t, sector.values]
                      + idio[t]
                      + alpha_component[t])
        ret_df = pd.DataFrame(ret, index=dates, columns=tickers)

        # prices, volume, mktcap
        prices = 50.0 * (1 + ret_df).cumprod()
        base_vol = rng.lognormal(13, 1.0, n)                       # share volume scale
        vol = pd.DataFrame(base_vol * np.exp(rng.normal(0, 0.4, (T, n))),
                           index=dates, columns=tickers).round()
        shares = pd.Series(rng.lognormal(18, 0.8, n), index=tickers)
        mcap = prices.mul(shares, axis=1)

        # --- observable (noisy, realistically-lagged) feature panels in `raw` ---
        raw: Dict[str, pd.DataFrame] = {}
        # observable SUE: planted feature + noise, only "released" sparsely (quarterly)
        sue_obs = truth["sue"] + rng.normal(0, 0.8, (T, n))
        rel_mask = pd.DataFrame(rng.random((T, n)) < (1 / 63), index=dates, columns=tickers)
        sue_panel = sue_obs.where(rel_mask).ffill(limit=63)
        raw["sue_surprise"] = sue_panel
        # observable sentiment: planted + heavy noise (alt-data is dirty)
        raw["news_sentiment"] = truth["senti"] + rng.normal(0, 1.5, (T, n))
        # an observable options-skew proxy correlated weakly with reversal+senti
        raw["options_skew"] = (0.4 * truth["rev"] + 0.3 * truth["senti"]
                               + rng.normal(0, 1.0, (T, n)))

        return MarketData(prices=prices, volume=vol, market_cap=mcap,
                          sector=sector, raw=raw, truth=truth)


class LiveBackend:
    """Free real data via yfinance; auto-falls-back to synthetic if unavailable."""

    SP100 = ("AAPL MSFT AMZN NVDA GOOGL GOOG META BRK-B TSLA UNH JNJ JPM V PG XOM "
             "HD CVX MA ABBV PFE COST AVGO KO PEP TMO MRK WMT BAC ADBE CRM ACN "
             "MCD CSCO ABT LIN DHR TXN NEE WFC PM AMD INTC VZ COP NKE BMY UPS RTX "
             "HON QCOM LOW UNP T IBM GS CAT SPGI INTU AMGN ISRG PLD AMAT BKNG "
             "DE NOW MS BLK GE ELV MDT GILD ADP TJX MMC VRTX REGN LRCX C SCHW "
             "CB ZTS MO SO BSX PGR DUK CME EOG SLB BDX ITW AON CL PYPL APD "
             "MU FCX EMR NSC WM").split()

    def __init__(self, tickers: Optional[List[str]] = None,
                 start: str = "2017-01-01", end: Optional[str] = None,
                 fallback_seed: int = 42):
        self.tickers = tickers or list(self.SP100)
        self.start, self.end, self.seed = start, end, fallback_seed

    def load(self) -> MarketData:
        try:
            import yfinance as yf
            df = yf.download(self.tickers, start=self.start, end=self.end,
                             auto_adjust=True, progress=False, threads=True)
            if df is None or df.empty:
                raise RuntimeError("empty yfinance response")
            close = df["Close"].dropna(axis=1, how="all").dropna(how="all")
            volume = df["Volume"].reindex_like(close)
            close = close.ffill().dropna(axis=1)
            volume = volume.reindex_like(close).fillna(0)
            if close.shape[1] < 10:
                raise RuntimeError("too few usable tickers from yfinance")
            # crude sector proxy by hashing ticker (real desk: GICS map)
            sector = pd.Series([hash(t) % 11 for t in close.columns],
                               index=close.columns, name="sector")
            mcap = close * volume.rolling(20).mean()  # proxy only (no shares-out free)
            print(f"[LiveBackend] loaded {close.shape[1]} tickers x "
                  f"{close.shape[0]} days from yfinance")
            return MarketData(prices=close, volume=volume, market_cap=mcap,
                              sector=sector, raw={}, truth={})
        except Exception as exc:  # noqa: BLE001
            print(f"[LiveBackend] live load failed ({exc}); "
                  f"falling back to synthetic data.")
            return SyntheticBackend(n_assets=max(100, len(self.tickers)),
                                    seed=self.seed).load()


def load_data(mode: str = "synthetic", **kw) -> MarketData:
    if mode == "live":
        return LiveBackend(tickers=kw.get("tickers"),
                           start=kw.get("start", "2017-01-01"),
                           end=kw.get("end")).load()
    return SyntheticBackend(n_assets=kw.get("universe", 300),
                            n_days=kw.get("days", 1500),
                            seed=kw.get("seed", 42)).load()
