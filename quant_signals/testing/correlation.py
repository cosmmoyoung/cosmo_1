"""Gate 3 — correlation & orthogonality. Is the new signal incremental to the book?

(1) pairwise signal-vector correlation matrix
(2) orthogonalized IC retention: residualize a signal vs the rest, re-test IC
"""
from __future__ import annotations
from typing import Dict
import numpy as np
import pandas as pd

from config import CONFIG
from testing.strength import information_coefficient


def signal_correlation_matrix(signals: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Average cross-sectional correlation between each pair of signal vectors."""
    names = list(signals)
    M = pd.DataFrame(np.nan, index=names, columns=names)
    # stack each signal to a long vector aligned on (date,ticker)
    stacks = {n: s.stack().dropna() for n, s in signals.items()}
    for i, a in enumerate(names):
        for b in names[i:]:
            common = stacks[a].index.intersection(stacks[b].index)
            if len(common) < 100:
                continue
            c = np.corrcoef(stacks[a].loc[common], stacks[b].loc[common])[0, 1]
            M.loc[a, b] = M.loc[b, a] = c
    return M


def orthogonalize(target: pd.DataFrame, others: Dict[str, pd.DataFrame]
                  ) -> pd.DataFrame:
    """Per-day residual of `target` regressed on the other signal vectors."""
    out = pd.DataFrame(index=target.index, columns=target.columns, dtype=float)
    other_list = list(others.values())
    for t in target.index:
        y = target.loc[t]
        valid = y.notna()
        Xcols = []
        for o in other_list:
            if t in o.index:
                Xcols.append(o.loc[t].reindex(y.index))
        if not Xcols:
            out.loc[t] = y
            continue
        X = pd.concat(Xcols, axis=1)
        m = valid & X.notna().all(axis=1)
        if m.sum() < 10:
            continue
        Xm = np.column_stack([np.ones(m.sum()), X[m].values])
        try:
            beta, *_ = np.linalg.lstsq(Xm, y[m].values, rcond=None)
            out.loc[t, y.index[m]] = y[m].values - Xm @ beta
        except np.linalg.LinAlgError:
            out.loc[t, y.index[m]] = y[m].values
    return out


def run_orthogonality(signals: Dict[str, pd.DataFrame], specs, md) -> pd.DataFrame:
    g = CONFIG.gates
    rows = []
    for name, sig in signals.items():
        others = {k: v for k, v in signals.items() if k != name}
        fwd = md.forward_return(specs[name].horizon)
        standalone = information_coefficient(sig, fwd).mean()
        orth = orthogonalize(sig, others)
        orth_ic = information_coefficient(orth, fwd).mean()
        retention = orth_ic / standalone if abs(standalone) > 1e-9 else np.nan
        rows.append({"name": name, "standalone_ic": standalone,
                     "orthogonal_ic": orth_ic,
                     "ic_retention": retention,
                     "incremental_pass": bool(np.isfinite(retention)
                                              and retention > g.min_orthogonal_ic_retention)})
    return pd.DataFrame(rows).sort_values("orthogonal_ic", ascending=False).reset_index(drop=True)
