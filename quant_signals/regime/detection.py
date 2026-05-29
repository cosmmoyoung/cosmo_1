"""Gate 5 — regime detection & conditional stability.

Two labelers:
  - GaussianMixture (2-3 state) on [market return, realized vol] as an HMM proxy
  - interpretable vol-tercile + trend-sign cuts
Then conditional IC/Sharpe within each regime, and a flag if the signal loses in
a regime occupying > max_losing_regime_time_share of the sample.
"""
from __future__ import annotations
from typing import Dict
import numpy as np
import pandas as pd

from config import CONFIG
from testing.strength import information_coefficient


def label_regimes(md, n_states: int = 3) -> pd.Series:
    """GMM regime labels ordered by volatility (0=calm ... n-1=crisis)."""
    mkt = md.returns.mean(axis=1)
    rv = mkt.rolling(21).std()
    X = pd.concat([mkt, rv], axis=1).dropna()
    X.columns = ["mkt", "rv"]
    try:
        from sklearn.mixture import GaussianMixture
        gm = GaussianMixture(n_components=n_states, covariance_type="full",
                             random_state=CONFIG.random_seed, n_init=3)
        lab = pd.Series(gm.fit_predict(X.values), index=X.index)
        # order states by mean rv so 0=calm, high=crisis
        order = X.groupby(lab)["rv"].mean().sort_values().index
        remap = {old: new for new, old in enumerate(order)}
        return lab.map(remap).reindex(md.returns.index).ffill()
    except Exception:  # noqa: BLE001  (sklearn missing -> vol-tercile fallback)
        ter = pd.qcut(rv.rank(method="first"), n_states, labels=False)
        return ter.reindex(md.returns.index).ffill()


def conditional_performance(signal: pd.DataFrame, md, regimes: pd.Series,
                            horizon: int = 1) -> pd.DataFrame:
    """Mean IC and time-share within each regime."""
    ic = information_coefficient(signal, md.forward_return(horizon))
    reg = regimes.reindex(ic.index)
    df = pd.DataFrame({"ic": ic, "regime": reg}).dropna()
    g = df.groupby("regime")["ic"]
    out = pd.DataFrame({"mean_ic": g.mean(), "n_days": g.size()})
    out["time_share"] = out["n_days"] / out["n_days"].sum()
    return out


def run_regime_analysis(signals: Dict[str, pd.DataFrame], specs, md) -> pd.DataFrame:
    regimes = label_regimes(md)
    g = CONFIG.gates
    rows = []
    for name, sig in signals.items():
        cond = conditional_performance(sig, md, regimes, specs[name].horizon)
        # flag if it loses (ic<0 vs overall sign) in a regime with big time-share
        overall = cond["mean_ic"].mean()
        losing = cond[(np.sign(cond["mean_ic"]) != np.sign(overall)) &
                      (cond["time_share"] > g.max_losing_regime_time_share)]
        rows.append({"name": name,
                     "ic_calm": cond["mean_ic"].get(0, np.nan),
                     "ic_crisis": cond["mean_ic"].get(cond.index.max(), np.nan),
                     "ic_dispersion": cond["mean_ic"].std(),
                     "regime_robust": len(losing) == 0,
                     "flag": "regime-gate" if len(losing) else "ok"})
    return pd.DataFrame(rows).reset_index(drop=True), regimes
