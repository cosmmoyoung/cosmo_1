"""House configuration: thresholds and constants for the signal-discovery funnel.

Every kill-gate threshold from the research framework lives here so the
production gates and the documentation never drift apart.
"""
from __future__ import annotations
from dataclasses import dataclass, field


@dataclass(frozen=True)
class GateThresholds:
    # Gate 2 — standalone strength (daily, market/sector-neutral US L/S book)
    min_abs_rank_ic: float = 0.02
    min_ic_ir_annual: float = 0.5
    min_newey_west_t: float = 3.0          # Harvey-Liu-Zhu multiple-testing bar, not 1.96
    min_decile_monotonicity: float = 0.80   # Spearman(decile means, decile rank)
    min_deflated_sharpe: float = 0.95
    fdr_q: float = 0.10                      # Benjamini-Hochberg

    # Gate 3 — orthogonality / incremental value
    max_pairwise_signal_corr: float = 0.70
    min_orthogonal_ic_retention: float = 0.60
    min_combined_ir_uplift: float = 0.20

    # Gate 4 — turnover / cost
    min_net_sharpe: float = 0.70
    min_breakeven_cost_multiple: float = 2.0  # breakeven must be >= 2x modeled live cost

    # Gate 5 — regime stability
    max_losing_regime_time_share: float = 0.20

    # Gate 7 — live monitoring / retirement
    live_ic_retire_fraction: float = 0.50    # retire if live IC < 0.5x backtest for 60d
    monitor_window_days: int = 60


@dataclass(frozen=True)
class CostModel:
    """Square-root market-impact cost model (Almgren-style)."""
    half_spread_bps: float = 2.0     # one-way half spread for liquid US large caps
    impact_coef_k: float = 1.0        # impact = k * vol * sqrt(participation)
    max_participation: float = 0.10   # cap order at 10% of ADV (capacity constraint)


@dataclass(frozen=True)
class Config:
    trading_days_per_year: int = 252
    universe_size: int = 300
    winsor_limits: tuple = (0.01, 0.99)
    fundamental_staleness_days: int = 90
    decay_horizons: tuple = (1, 2, 3, 5, 10, 21, 42, 63)
    rebalance_freq_days: int = 1
    gates: GateThresholds = field(default_factory=GateThresholds)
    cost: CostModel = field(default_factory=CostModel)
    random_seed: int = 42


CONFIG = Config()
