"""End-to-end signal-discovery pipeline (the runnable artifact, §13).

  build universe -> engineer features -> define signals -> Gate 2 strength
  -> Gate 2b decay -> Gate 3 orthogonality -> Gate 4 turnover/cost
  -> Gate 5 regime -> Gate 6 combine -> Gate 7 dashboard.

Usage:
  python run_pipeline.py --mode synthetic --universe 300 --days 1500
  python run_pipeline.py --mode live --start 2018-01-01
"""
from __future__ import annotations
import argparse
import os
import sys
import numpy as np
import pandas as pd

# allow `python run_pipeline.py` from the package dir
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import CONFIG
from data.loader import load_data
from features.engineering import build_signal
from signals.definitions import REGISTRY
from testing.strength import run_strength_battery
from testing.decay import run_decay_analysis
from testing.correlation import run_orthogonality, signal_correlation_matrix
from testing.turnover import run_turnover_analysis
from regime.detection import run_regime_analysis
from combination.ensemble import benchmark
from monitoring.dashboard import render_dashboard


def banner(t):
    print("\n" + "=" * 72 + f"\n  {t}\n" + "=" * 72)


def build_signals(md):
    """Run each registered raw feature through the neutralization pipeline."""
    log_mcap = np.log(md.market_cap.replace(0, np.nan))
    signals = {}
    for name, spec in REGISTRY.items():
        raw = spec.fn(md)
        exposures = log_mcap if spec.neutralize else None
        sector = md.sector if spec.neutralize else None
        signals[name] = build_signal(raw, exposures=exposures, sector=sector,
                                     sign=spec.sign)
    return signals


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["synthetic", "live"], default="synthetic")
    ap.add_argument("--universe", type=int, default=300)
    ap.add_argument("--days", type=int, default=1500)
    ap.add_argument("--start", default="2018-01-01")
    ap.add_argument("--tickers", default=None,
                    help="comma list, or SP100 (live mode)")
    ap.add_argument("--aum", type=float, default=1e8)
    ap.add_argument("--outdir", default="outputs")
    args = ap.parse_args()

    np.random.seed(CONFIG.random_seed)
    tickers = None
    if args.tickers and args.tickers != "SP100":
        tickers = args.tickers.split(",")

    banner(f"LOAD DATA  (mode={args.mode})")
    md = load_data(mode=args.mode, universe=args.universe, days=args.days,
                   tickers=tickers, start=args.start, seed=CONFIG.random_seed)
    print(f"  prices: {md.prices.shape[0]} days x {md.prices.shape[1]} names")

    banner("FEATURE ENGINEERING  (neutralize + rank-normalize)")
    signals = build_signals(md)
    print(f"  built {len(signals)} signals: {', '.join(signals)}")

    banner("GATE 2 — STANDALONE STRENGTH")
    strength = run_strength_battery(signals, REGISTRY, md)
    print(strength.to_string(index=False))

    banner("GATE 2b — DECAY / HOLDING PERIOD")
    decay = run_decay_analysis(signals, REGISTRY, md)
    print(decay.to_string(index=False))

    banner("GATE 3 — ORTHOGONALITY / INCREMENTAL IC")
    orth = run_orthogonality(signals, REGISTRY, md)
    print(orth.to_string(index=False))
    corr = signal_correlation_matrix(signals)
    print("\n  signal-vector correlation matrix:")
    print(corr.round(2).to_string())

    banner("GATE 4 — TURNOVER / COST-ADJUSTED SHARPE")
    turn = run_turnover_analysis(signals, REGISTRY, md, aum_usd=args.aum)
    print(turn.to_string(index=False))

    banner("GATE 5 — REGIME CONDITIONAL STABILITY")
    regime, regimes = run_regime_analysis(signals, REGISTRY, md)
    print(regime.to_string(index=False))

    # keep only signals that cleared the core gates for the combiner
    survivors = set(strength.loc[strength.verdict == "PASS", "name"])
    if len(survivors) < 2:  # ensure the combiner has something to work with
        survivors = set(strength.sort_values("ic_ir_annual", ascending=False)
                        .head(4)["name"])
    print(f"\n  survivors advanced to combiner: {sorted(survivors)}")
    surv_signals = {k: v for k, v in signals.items() if k in survivors}

    banner("GATE 6 — SIGNAL COMBINATION (OOS, net of cost)")
    combo_table, combos = benchmark(surv_signals, md, REGISTRY)
    print(combo_table.to_string(index=False))
    best = combo_table.iloc[0]["combiner"]
    # House rule #5: ship equal-weight unless a complex combiner truly beats it
    eq_sr = combo_table.loc[combo_table.combiner == "equal_weight",
                            "oos_net_sharpe"].iloc[0]
    best_sr = combo_table.iloc[0]["oos_net_sharpe"]
    ship = best if best_sr > eq_sr + 0.1 else "equal_weight"
    print(f"\n  best OOS: {best}; SHIPPING: {ship} "
          f"(house rule #5: complexity must beat equal-weight by >0.1 SR)")
    composite = combos[ship]

    banner("GATE 7 — MONITORING DASHBOARD")
    tables = {"strength": strength, "decay": decay, "orthogonality": orth,
              "turnover": turn, "regime": regime, "combination": combo_table}
    report = render_dashboard(surv_signals, composite, md, REGISTRY, tables,
                              regimes, outdir=args.outdir)
    print(f"  report written -> {report}")
    print(f"  panels in -> {args.outdir}/")

    banner("SUMMARY")
    n_pass = (strength.verdict == "PASS").sum()
    print(f"  signals tested : {len(signals)}")
    print(f"  passed Gate 2  : {n_pass}")
    print(f"  shipped combiner: {ship}")
    print("  artifact       : outputs/signal_research_report.html")


if __name__ == "__main__":
    main()
