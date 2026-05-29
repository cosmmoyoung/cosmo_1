"""Feature engineering: clean -> transform -> neutralize -> standardize.

Implements the §3 pipeline: point-in-time alignment is the caller's job (the
loaders already lag observable panels); here we winsorize, neutralize against
systematic exposures, and rank-normalize cross-sectionally so every signal is
sign-conventioned (higher = predicted higher forward return) and comparable.
"""
from __future__ import annotations
from typing import Optional
import numpy as np
import pandas as pd


def winsorize_xs(df: pd.DataFrame, lower: float = 0.01, upper: float = 0.99) -> pd.DataFrame:
    """Cross-sectional winsorize each row at [lower, upper] quantiles."""
    lo = df.quantile(lower, axis=1)
    hi = df.quantile(upper, axis=1)
    return df.clip(lower=lo, upper=hi, axis=0)


def zscore_xs(df: pd.DataFrame) -> pd.DataFrame:
    """Cross-sectional z-score (demean / std per row)."""
    return df.sub(df.mean(axis=1), axis=0).div(df.std(axis=1) + 1e-12, axis=0)


def rank_normal_xs(df: pd.DataFrame) -> pd.DataFrame:
    """Cross-sectional rank -> uniform(0,1) -> centered to [-0.5, 0.5].

    House default: robust to fat tails that blow up raw z-scores in crises.
    """
    r = df.rank(axis=1, pct=True)
    return r - 0.5


def neutralize_xs(signal: pd.DataFrame, exposures: pd.DataFrame,
                  sector: Optional[pd.Series] = None) -> pd.DataFrame:
    """Per-day cross-sectional OLS residual of signal on exposures (+ sector dummies).

    exposures: dict-like DataFrame stacked? Here we accept a single panel of
    one exposure (e.g. log-mktcap). For multiple, call repeatedly or pass a
    pre-built design via `neutralize_multi`. Keeps the residual.
    """
    out = pd.DataFrame(index=signal.index, columns=signal.columns, dtype=float)
    sec_dummies = None
    if sector is not None:
        sec_dummies = pd.get_dummies(sector).astype(float)  # ticker x sector
    for t in signal.index:
        y = signal.loc[t]
        valid = y.notna()
        if valid.sum() < 10:
            continue
        cols = [np.ones(valid.sum())]
        if t in exposures.index:
            x = exposures.loc[t][valid]
            cols.append(((x - x.mean()) / (x.std() + 1e-12)).values)
        if sec_dummies is not None:
            cols.append(sec_dummies.loc[y.index[valid]].values.T)
        X = np.vstack([c if np.ndim(c) > 1 else c[None, :] for c in cols]).T
        yv = y[valid].values
        try:
            beta, *_ = np.linalg.lstsq(X, yv, rcond=None)
            resid = yv - X @ beta
        except np.linalg.LinAlgError:
            resid = yv - yv.mean()
        out.loc[t, y.index[valid]] = resid
    return out


def build_signal(raw: pd.DataFrame, exposures: Optional[pd.DataFrame] = None,
                 sector: Optional[pd.Series] = None, sign: float = 1.0,
                 method: str = "rank", winsor=(0.01, 0.99)) -> pd.DataFrame:
    """Full pipeline for one raw feature -> tradable signal vector.

    sign: +1 if higher raw -> higher forward return, else -1 (flips convention).
    """
    s = winsorize_xs(raw, *winsor)
    if exposures is not None or sector is not None:
        s = neutralize_xs(s, exposures if exposures is not None
                          else pd.DataFrame(0, index=s.index, columns=s.columns),
                          sector=sector)
    s = rank_normal_xs(s) if method == "rank" else zscore_xs(s)
    return sign * s
