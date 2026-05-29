"""Gate 2 — standalone signal strength.

IC / IC-IR / Newey-West t-stat / quantile (decile) portfolios / Deflated Sharpe
/ Benjamini-Hochberg FDR across the batch. Returns a tidy results table and a
PASS/FAIL verdict against the house thresholds in config.
"""
from __future__ import annotations
from dataclasses import dataclass, asdict
from typing import Dict, List
import numpy as np
import pandas as pd
from scipy import stats

from config import CONFIG


# --------------------------------------------------------------------- IC stats
def information_coefficient(signal: pd.DataFrame, fwd_ret: pd.DataFrame,
                            method: str = "spearman") -> pd.Series:
    """Daily cross-sectional rank-IC time series."""
    common = signal.index.intersection(fwd_ret.index)
    ics = {}
    s, f = signal.loc[common], fwd_ret.loc[common]
    for t in common:
        a, b = s.loc[t], f.loc[t]
        m = a.notna() & b.notna()
        if m.sum() < 10:
            continue
        if method == "spearman":
            ic, _ = stats.spearmanr(a[m], b[m])
        else:
            ic = np.corrcoef(a[m], b[m])[0, 1]
        if np.isfinite(ic):
            ics[t] = ic
    return pd.Series(ics, name="ic").sort_index()


def newey_west_tstat(x: pd.Series, lags: int) -> float:
    """t-stat of mean(x) with Newey-West HAC variance (autocorrelation-robust)."""
    x = x.dropna().values
    n = len(x)
    if n < 5:
        return np.nan
    mu = x.mean()
    e = x - mu
    gamma0 = (e @ e) / n
    var = gamma0
    for k in range(1, min(lags, n - 1) + 1):
        w = 1 - k / (lags + 1)
        cov = (e[k:] @ e[:-k]) / n
        var += 2 * w * cov
    se = np.sqrt(max(var, 1e-18) / n)
    return mu / se


def decile_portfolios(signal: pd.DataFrame, fwd_ret: pd.DataFrame,
                      n_bins: int = 10) -> Dict[str, float]:
    """Long-top/short-bottom decile spread, monotonicity, spread t-stat."""
    common = signal.index.intersection(fwd_ret.index)
    bin_rets = {b: [] for b in range(n_bins)}
    spread = []
    for t in common:
        s, f = signal.loc[t], fwd_ret.loc[t]
        m = s.notna() & f.notna()
        if m.sum() < n_bins * 3:
            continue
        ranks = s[m].rank(method="first")
        bins = pd.qcut(ranks, n_bins, labels=False, duplicates="drop")
        if bins.nunique() < n_bins:
            continue
        means = f[m].groupby(bins).mean()
        for b in range(n_bins):
            if b in means.index:
                bin_rets[b].append(means[b])
        spread.append(means.get(n_bins - 1, np.nan) - means.get(0, np.nan))
    bin_mean = np.array([np.nanmean(bin_rets[b]) if bin_rets[b] else np.nan
                         for b in range(n_bins)])
    spread = pd.Series(spread).dropna()
    mono, _ = stats.spearmanr(np.arange(n_bins), bin_mean) if np.isfinite(bin_mean).all() else (np.nan, None)
    sp_t = newey_west_tstat(spread, lags=CONFIG.decay_horizons[0]) if len(spread) else np.nan
    ann = np.sqrt(CONFIG.trading_days_per_year)
    sp_sharpe = (spread.mean() / (spread.std() + 1e-12)) * ann if len(spread) else np.nan
    return {"decile_monotonicity": float(mono) if mono is not None else np.nan,
            "spread_mean": float(spread.mean()) if len(spread) else np.nan,
            "spread_tstat": float(sp_t), "spread_sharpe": float(sp_sharpe),
            "bin_means": bin_mean.tolist()}


def deflated_sharpe_ratio(returns: pd.Series, n_trials: int,
                          freq: int = CONFIG.trading_days_per_year) -> float:
    """Bailey & López de Prado (2014) Deflated Sharpe Ratio.

    Adjusts observed SR for: number of trials, skew, kurtosis, sample length.
    Returns P(true SR > 0) given the selection from n_trials.
    """
    r = returns.dropna().values
    n = len(r)
    if n < 20:
        return np.nan
    sr = r.mean() / (r.std(ddof=1) + 1e-12)            # per-period SR
    skew = stats.skew(r)
    kurt = stats.kurtosis(r, fisher=False)
    # expected max SR from n_trials independent strategies (variance of trial SRs ~1/n)
    emc = 0.5772156649
    sr_trials_std = 1.0 / np.sqrt(n)                     # approx std of per-period SR
    z = stats.norm.ppf(1 - 1.0 / max(n_trials, 1)) if n_trials > 1 else 0.0
    z2 = stats.norm.ppf(1 - 1.0 / max(n_trials, 1) * np.e) if n_trials > 1 else 0.0
    sr0 = sr_trials_std * ((1 - emc) * z + emc * z2)    # expected max under null
    num = (sr - sr0) * np.sqrt(n - 1)
    den = np.sqrt(1 - skew * sr + (kurt - 1) / 4.0 * sr ** 2)
    if not np.isfinite(den) or den <= 0:
        return np.nan
    return float(stats.norm.cdf(num / den))


def benjamini_hochberg(pvals: Dict[str, float], q: float) -> Dict[str, bool]:
    """Return {name: passes_FDR} at level q."""
    items = [(k, v) for k, v in pvals.items() if np.isfinite(v)]
    items.sort(key=lambda kv: kv[1])
    m = len(items)
    passed = {k: False for k in pvals}
    thresh_rank = 0
    for i, (_, p) in enumerate(items, start=1):
        if p <= (i / m) * q:
            thresh_rank = i
    for i, (k, _) in enumerate(items, start=1):
        passed[k] = i <= thresh_rank
    return passed


@dataclass
class StrengthResult:
    name: str
    family: str
    mean_ic: float
    ic_ir_annual: float
    nw_tstat: float
    decile_monotonicity: float
    spread_sharpe: float
    deflated_sharpe: float
    fdr_pass: bool
    verdict: str


def run_strength_battery(signals: Dict[str, pd.DataFrame],
                         specs: Dict, md, n_trials: int | None = None
                         ) -> pd.DataFrame:
    """Run the full Gate-2 battery over a dict of {name: signal_panel}."""
    g = CONFIG.gates
    ann = np.sqrt(CONFIG.trading_days_per_year)
    n_trials = n_trials or len(signals)
    rows: List[StrengthResult] = []
    pvals: Dict[str, float] = {}
    cache = {}
    for name, sig in signals.items():
        h = specs[name].horizon
        fwd = md.forward_return(h)
        ic = information_coefficient(sig, fwd)
        if ic.empty:
            continue
        mean_ic = ic.mean()
        ic_ir = (mean_ic / (ic.std() + 1e-12)) * ann
        nwt = newey_west_tstat(ic, lags=h)
        dec = decile_portfolios(sig, fwd)
        # spread P&L series for DSR (use top-bottom daily spread proxy = ic*scale)
        spread_series = ic  # IC series stands in as the standardized daily edge
        dsr = deflated_sharpe_ratio(spread_series, n_trials=n_trials)
        # two-sided p from NW t
        pvals[name] = 2 * (1 - stats.norm.cdf(abs(nwt))) if np.isfinite(nwt) else 1.0
        cache[name] = (mean_ic, ic_ir, nwt, dec, dsr)

    fdr = benjamini_hochberg(pvals, g.fdr_q)
    for name, (mean_ic, ic_ir, nwt, dec, dsr) in cache.items():
        checks = {
            "ic": abs(mean_ic) > g.min_abs_rank_ic,
            "ir": abs(ic_ir) > g.min_ic_ir_annual,
            "t": abs(nwt) > g.min_newey_west_t,
            "mono": (dec["decile_monotonicity"] or 0) > g.min_decile_monotonicity,
            "dsr": (dsr or 0) > g.min_deflated_sharpe,
            "fdr": fdr.get(name, False),
        }
        verdict = "PASS" if all(checks.values()) else (
            "FAIL[" + ",".join(k for k, v in checks.items() if not v) + "]")
        rows.append(StrengthResult(
            name=name, family=specs[name].family, mean_ic=mean_ic,
            ic_ir_annual=ic_ir, nw_tstat=nwt,
            decile_monotonicity=dec["decile_monotonicity"],
            spread_sharpe=dec["spread_sharpe"], deflated_sharpe=dsr,
            fdr_pass=fdr.get(name, False), verdict=verdict))
    df = pd.DataFrame([asdict(r) for r in rows])
    return df.sort_values("ic_ir_annual", ascending=False).reset_index(drop=True)
