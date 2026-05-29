"""Gate 6 — signal combination. Four methods benchmarked OOS, net of cost.

  1. equal_weight       (rank-averaged baseline)
  2. ic_weighted        (IC/sigma(IC), shrunk toward equal weight)
  3. mean_variance      (max-IR of signal-portfolios, Ledoit-Wolf shrinkage)
  4. ml_stack           (regularized linear / GBM, purged-embargoed walk-forward)

House rule #5: a complex combiner must beat equal-weight OOS net-of-cost or we
ship equal-weight. The benchmark() function makes that comparison explicit.
"""
from __future__ import annotations
from typing import Dict, List
import numpy as np
import pandas as pd

from config import CONFIG
from testing.strength import information_coefficient
from testing.turnover import signal_to_weights, gross_net_sharpe


def _align(signals: Dict[str, pd.DataFrame]) -> Dict[str, pd.DataFrame]:
    idx = None
    cols = None
    for s in signals.values():
        idx = s.index if idx is None else idx.intersection(s.index)
        cols = s.columns if cols is None else cols.intersection(s.columns)
    return {k: v.reindex(index=idx, columns=cols) for k, v in signals.items()}


def equal_weight(signals: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    s = _align(signals)
    return sum(s.values()) / len(s)


def ic_weighted(signals: Dict[str, pd.DataFrame], md, specs,
                shrink: float = 0.5) -> pd.DataFrame:
    """Weight by annualized IC-IR, shrunk toward equal weight."""
    s = _align(signals)
    irs = {}
    ann = np.sqrt(CONFIG.trading_days_per_year)
    for name, sig in s.items():
        ic = information_coefficient(sig, md.forward_return(specs[name].horizon))
        irs[name] = max((ic.mean() / (ic.std() + 1e-12)) * ann, 0.0)
    tot = sum(irs.values()) or 1.0
    eq = 1.0 / len(s)
    weights = {k: shrink * eq + (1 - shrink) * (v / tot) for k, v in irs.items()}
    return sum(weights[k] * s[k] for k in s)


def mean_variance(signals: Dict[str, pd.DataFrame], md, shrink: float = 0.3
                  ) -> pd.DataFrame:
    """Max-IR combo of standalone signal-portfolio return streams, LW-shrunk cov."""
    s = _align(signals)
    fwd = md.returns.shift(-1)
    streams = {}
    for name, sig in s.items():
        w = signal_to_weights(sig)
        streams[name] = (w * fwd).sum(axis=1)
    R = pd.DataFrame(streams).dropna()
    mu = R.mean().values
    cov = R.cov().values
    # Ledoit-Wolf style shrink toward diagonal
    diag = np.diag(np.diag(cov))
    cov_s = (1 - shrink) * cov + shrink * diag
    try:
        w = np.linalg.solve(cov_s, mu)
    except np.linalg.LinAlgError:
        w = mu
    w = np.clip(w, 0, None)
    w = w / (w.sum() + 1e-12)
    names = list(R.columns)
    return sum(w[i] * s[n] for i, n in enumerate(names))


def ml_stack(signals: Dict[str, pd.DataFrame], md, horizon: int = 1,
             embargo: int = 5) -> pd.DataFrame:
    """Purged/embargoed walk-forward Ridge stack over the signal features.

    Avoids look-ahead by training only on data ending `embargo+horizon` before
    the prediction day. Falls back to equal-weight if sklearn missing.
    """
    s = _align(signals)
    fwd = md.forward_return(horizon)
    names = list(s)
    try:
        from sklearn.linear_model import Ridge
    except Exception:  # noqa: BLE001
        return equal_weight(signals)

    # build long panel
    frames = {n: s[n].stack() for n in names}
    y = fwd.stack()
    X = pd.DataFrame(frames)
    common = X.dropna().index.intersection(y.dropna().index)
    X, y = X.loc[common], y.loc[common]
    dates = X.index.get_level_values(0)
    uniq = np.array(sorted(dates.unique()))
    pred = pd.Series(index=X.index, dtype=float)
    # expanding walk-forward, refit every ~63 days
    fold_starts = uniq[252::63]
    model = Ridge(alpha=1.0)
    for cut in fold_starts:
        train_end = cut - pd.tseries.offsets.BDay(embargo + horizon)
        tr = dates <= train_end
        te = (dates > cut) & (dates <= cut + pd.tseries.offsets.BDay(63))
        if tr.sum() < 500 or te.sum() == 0:
            continue
        model.fit(X[tr].values, y[tr].values)
        pred[te] = model.predict(X[te].values)
    out = pred.dropna().unstack()
    return out.reindex(index=s[names[0]].index, columns=s[names[0]].columns)


def benchmark(signals: Dict[str, pd.DataFrame], md, specs,
              oos_frac: float = 0.4) -> pd.DataFrame:
    """Compare combiners OOS, net of cost. Equal-weight is the bar to beat."""
    s = _align(signals)
    idx = list(s.values())[0].index
    split = idx[int(len(idx) * (1 - oos_frac))]
    combos = {
        "equal_weight": equal_weight(s),
        "ic_weighted": ic_weighted(s, md, specs),
        "mean_variance": mean_variance(s, md),
        "ml_stack": ml_stack(s, md),
    }
    rows = []
    for name, combo in combos.items():
        oos = combo.loc[combo.index > split]
        w = signal_to_weights(oos)
        sr = gross_net_sharpe(w, md.returns.loc[md.returns.index > split],
                              md.dollar_volume.loc[md.dollar_volume.index > split])
        ic = information_coefficient(oos, md.forward_return(1)).mean()
        rows.append({"combiner": name, "oos_ic": ic,
                     "oos_gross_sharpe": sr["gross_sharpe"],
                     "oos_net_sharpe": sr["net_sharpe"]})
    df = pd.DataFrame(rows)
    eq = df.loc[df.combiner == "equal_weight", "oos_net_sharpe"].iloc[0]
    df["beats_equal_weight"] = df["oos_net_sharpe"] > eq + 1e-9
    return df.sort_values("oos_net_sharpe", ascending=False).reset_index(drop=True), combos
