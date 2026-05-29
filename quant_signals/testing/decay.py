"""Gate 2b — decay analysis. IC(horizon) curve, fitted tau / half-life,
optimal holding period, and rolling live-IC for crowding detection.
"""
from __future__ import annotations
from typing import Dict
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit

from config import CONFIG
from testing.strength import information_coefficient


def ic_decay_curve(signal: pd.DataFrame, md,
                   horizons=CONFIG.decay_horizons) -> pd.Series:
    """Mean rank-IC at each forward horizon."""
    out = {}
    for h in horizons:
        ic = information_coefficient(signal, md.forward_return(h))
        out[h] = ic.mean() if not ic.empty else np.nan
    return pd.Series(out, name="ic_by_horizon")


def fit_decay(curve: pd.Series) -> Dict[str, float]:
    """Fit IC(h) = IC0 * exp(-h/tau). Return IC0, tau, half_life."""
    h = np.array(curve.index, dtype=float)
    y = curve.values.astype(float)
    mask = np.isfinite(y)
    if mask.sum() < 3 or np.all(y[mask] <= 0):
        return {"ic0": np.nan, "tau": np.nan, "half_life": np.nan}
    sign = np.sign(np.nanmean(y))
    yy = sign * y
    try:
        (ic0, tau), _ = curve_fit(lambda x, a, t: a * np.exp(-x / t),
                                  h[mask], yy[mask],
                                  p0=[max(yy[mask][0], 1e-3), 10.0],
                                  maxfev=10000, bounds=([0, 0.1], [1.0, 500]))
        return {"ic0": float(sign * ic0), "tau": float(tau),
                "half_life": float(tau * np.log(2))}
    except Exception:  # noqa: BLE001
        return {"ic0": np.nan, "tau": np.nan, "half_life": np.nan}


def optimal_holding_period(curve: pd.Series, cost_per_period_ic: float = 0.0
                           ) -> int:
    """Horizon maximizing cumulative cost-adjusted IC (cumIC - h*cost)."""
    cum = curve.cumsum() - cost_per_period_ic * np.array(curve.index)
    return int(cum.idxmax())


def rolling_live_ic(signal: pd.DataFrame, md, horizon: int = 1,
                    window: int = CONFIG.gates.monitor_window_days) -> pd.Series:
    """Rolling mean IC — the crowding / live-decay monitor (Gate 7)."""
    ic = information_coefficient(signal, md.forward_return(horizon))
    return ic.rolling(window).mean()


def run_decay_analysis(signals: Dict[str, pd.DataFrame], specs, md) -> pd.DataFrame:
    rows = []
    for name, sig in signals.items():
        curve = ic_decay_curve(sig, md)
        fit = fit_decay(curve)
        ohp = optimal_holding_period(curve)
        rows.append({"name": name, "family": specs[name].family,
                     "ic_h1": curve.get(1, np.nan),
                     "ic_h21": curve.get(21, np.nan),
                     "tau_days": fit["tau"], "half_life_days": fit["half_life"],
                     "optimal_holding_days": ohp})
    return pd.DataFrame(rows).sort_values("half_life_days").reset_index(drop=True)
