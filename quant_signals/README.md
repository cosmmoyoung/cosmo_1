# quant_signals — Systematic Alpha Signal Discovery Pipeline

A runnable, end-to-end implementation of the signal-discovery funnel described in
[`../research/quant_signal_discovery_framework.md`](../research/quant_signal_discovery_framework.md).
US equities, multi-frequency, four signal families (alt-data · microstructure ·
price/volume + cross-asset · fundamental/earnings). Built on **free data**
(yfinance) with a **synthetic backend** that plants known ground-truth alphas so
every statistical test can be verified to recover them.

## Quick start

```bash
pip install -r requirements.txt

# 1) Offline, no network — synthetic data with embedded alphas (runs every gate):
python run_pipeline.py --mode synthetic --universe 300 --days 1500

# 2) Real free data via yfinance (auto-falls-back to synthetic if offline):
python run_pipeline.py --mode live --start 2018-01-01
```

Output: a PASS/FAIL table per gate in the console, plus
`outputs/signal_research_report.html` and PNG monitoring panels.

## The funnel (kill-gate at every step)

| Gate | Module | What it tests | House threshold |
|---|---|---|---|
| 0 Idea | `signals/hypotheses.yaml` | economic story + named counterparty | must exist before backtest |
| 1 Feature | `features/engineering.py` | point-in-time, winsorize, neutralize, rank-norm | no look-ahead |
| 2 Strength | `testing/strength.py` | rank-IC, IC-IR, Newey-West t, deciles, Deflated Sharpe, BH-FDR | IC>0.02, IR>0.5, t>3, DSR>0.95 |
| 2b Decay | `testing/decay.py` | IC(horizon) curve, τ / half-life, holding period | live-IC ≥ 0.5× backtest |
| 3 Orthogonality | `testing/correlation.py` | incremental IC vs book, pairwise corr | retention>60%, |ρ|<0.7 |
| 4 Cost | `testing/turnover.py` | turnover, √-impact cost, net Sharpe, breakeven, capacity | net SR>0.7, breakeven>2× cost |
| 5 Regime | `regime/detection.py` | GMM/HMM regimes, conditional IC | no loss in >20%-time regime |
| 6 Combine | `combination/ensemble.py` | equal-wt / IC-wt / mean-var / ML-stack, OOS net | beat equal-wt OOS net-of-cost |
| 7 Monitor | `monitoring/dashboard.py` | rolling live-IC, P&L, decay, alerts | retire when edge crowds out |

## Wiring in real institutional data

Every loader sits behind the `MarketData` interface in `data/loader.py`. To swap
free data for CRSP/Compustat-PIT/TAQ/RavenPack, implement a backend returning the
same bundle (`prices, volume, market_cap, sector, raw{}`) with **point-in-time**
timestamps. The gates, tests, and thresholds are unchanged.

## What's real vs illustrative

The **methods, tests, thresholds, and code** are production-grade and run on real
free data. The **specific IC/Sharpe numbers** in the framework doc come from the
synthetic harness (which injects known alphas so you can confirm each test
recovers them) — they show the gate logic and realistic magnitudes, not a live
track record.
