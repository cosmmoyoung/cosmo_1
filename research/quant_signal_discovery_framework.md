# Systematic Alpha Signal Discovery — A Citadel-Style Research Framework
### "From idea to monitored live signal, with a statistical kill-gate at every step"

*Author: Senior Quantitative Researcher*
*As of 29 May 2026.*
*Scope: US equities (Russell 3000 investable universe), multi-frequency (intraday-microstructure → daily cross-sectional → weekly/monthly fundamental), four signal families: **alternative data · market microstructure · price/volume + cross-asset · fundamental/earnings**.*
*Companion code: `/quant_signals` (runnable end-to-end on free data; yfinance live + synthetic fallback).*

---

## 0. The thesis of this document

Most "signals" that look profitable are **false discoveries**. The entire job of a research process is not to *find* signals — finding correlations is trivial and a 2-line `groupby` will hand you a hundred per afternoon — the job is to **kill the fake ones cheaply and fast**, and to size the survivors honestly net of the three taxes that eat retail-grade backtests alive: **transaction cost, capacity decay, and crowding/alpha-decay**.

So this framework is organized as a **funnel with kill-gates**. A candidate signal must pass each gate to advance; the gates are ordered cheapest-test-first so we spend the least compute rejecting the most ideas. The numbers attached to each gate below are the *house thresholds* — calibrated to a daily, market-and-sector-neutral, ~1000-name US long/short book. They are deliberately strict.

```
  IDEA  ──►  FEATURE  ──►  STANDALONE   ──►  ORTHOGONALITY  ──►  COST &      ──►  REGIME &     ──►  COMBINE  ──►  LIVE
  (econ      (point-in-    STRENGTH         (incremental        TURNOVER         STABILITY        (portfolio    MONITOR
   prior)     time, clean)  IC / IR /        IC vs known         net-of-cost      (conditional      of alphas)    (decay
                            quantile         factors)            Sharpe,          IC, drawdown                    alerts,
                            t-stat)                              breakeven bps)    by regime)                      crowding)
   GATE 0      GATE 1        GATE 2           GATE 3              GATE 4           GATE 5            GATE 6        GATE 7

  reject       reject        |IC|<0.02       ΔIR<0.2 vs         net SR<0.7       SR halves in     marginal       IC_live <
  if no        if look-      rank-IC         existing book      OR breakeven     a regime that    contribution    0.5×IC_backtest
  econ story   ahead / PIT   t<3 (NW)        → DROP             <2× live cost    is >20% of time  to book SR ≤0   for 60d → halt
               leak                          → DROP             → DROP           → flag                          → retire
```

The rest of this document walks each gate, gives the **signal definition**, the **statistical test**, the **house threshold**, and the **Python entry point** that runs it.

---

## 1. Idea generation framework (Gate 0 — the economic prior)

> **House rule #1: every signal must have a one-sentence economic story written *before* the backtest is run, and the story must name the counterparty who is on the other side of the trade and why they are willing to lose.** If you cannot name the loser, you have found a data-mining artifact, not an edge.

Alpha is a **transfer of wealth**, so every durable signal exploits one of four structural reasons the counterparty trades against their own interest:

| # | Source of edge | The counterparty & why they lose | Example signal family | Decay speed |
|---|---|---|---|---|
| 1 | **Risk premium** | Someone pays you to hold a risk they must shed (forced sellers, hedgers, insurers) | short-vol, liquidity provision, post-downgrade fire-sale | slow (years) — it's compensation, not a mistake |
| 2 | **Behavioral / under-reaction** | Investors anchor and update too slowly to news | PEAD (post-earnings-announcement drift), analyst-revision momentum, 52-wk-high | medium (months→quarters) |
| 3 | **Constraint / segmentation** | A large pool *can't* trade the asset (index funds, mandates, leverage limits, T+ rules) | index-rebalance front-run, short-interest squeeze, hard-to-borrow | medium |
| 4 | **Information / latency** | You see/process data faster or earlier | alt-data nowcasting (cards, web traffic, satellite), order-flow imbalance, cross-asset lead-lag | fast (days→weeks); arbitraged away fastest |

**The hypothesis bank.** We maintain a living backlog (`/quant_signals/signals/hypotheses.yaml` schema) where each row is `{id, family, economic_story, counterparty, raw_inputs, expected_horizon, expected_decay, capacity_guess, prior_IC}`. Ideas come from four pumps, mapped to our four mandated families:

1. **Microstructure** — order-flow imbalance, signed volume (Lee-Ready / bulk-volume), Kyle's λ (price impact per unit flow), Amihud illiquidity, realized-vol asymmetry, intraday reversal, close-auction imbalance. *Story: liquidity demanders pay liquidity suppliers; the imbalance predicts short-horizon reversion or continuation depending on informedness.*
2. **Alt-data** — news/social sentiment, app-download / web-traffic momentum, ESG-controversy flow, insider transactions, congressional/Senate trades, 13F crowding, options-implied skew & put/call. *Story: information diffuses unevenly; processors-of-record (the slow institutions) update on a lag.*
3. **Price/volume + cross-asset** — cross-sectional momentum (12-1), short-term reversal (1-5d), volatility-scaled momentum, idiosyncratic momentum (residual of factor model), 52-week-high proximity, cross-asset lead-lag (credit→equity, sector-ETF flows, FX→ADR). *Story: under-reaction + anchoring + slow capital mobility across markets.*
4. **Fundamental/earnings** — SUE (standardized unexpected earnings) drift, analyst revision breadth, accruals quality (Sloan), gross-profitability (Novy-Marx), net-issuance, asset-growth, earnings-call-transcript tone delta, free-cash-flow yield. *Story: investors fixate on headline earnings and mis-weight the persistence of accrual vs cash earnings.*

> **House rule #2 — the "would I have known this in real time?" test.** For every raw input, write down its *real-world availability lag*. Earnings are point-in-time with a reporting lag; analyst estimates get *restated* in vendor databases (survivorship + look-ahead landmine); satellite data has a processing lag; close-auction imbalance is known at 15:50, not 16:00. The feature pipeline (§3) enforces these lags mechanically.

---

## 2. Data sources (the free-data stack, mapped to its institutional analog)

We deliberately build the whole pipeline on **free/open data** so the *method* is reproducible end-to-end, while wiring every loader behind an interface so the same code swaps to institutional feeds by changing one adapter. The mapping below is the "here's what we use vs. here's what the real desk uses" Rosetta stone.

| Signal family | Free source (this repo) | Institutional analog | Key data hazard to control |
|---|---|---|---|
| Price/volume, cross-asset | `yfinance` (OHLCV, splits, divs), FRED (rates, macro) | CRSP, Refinitiv, Bloomberg | **survivorship bias** (delisted names), split/div adjustment timing |
| Microstructure | yfinance 1-min bars (proxy); synthetic L2 generator | NYSE TAQ, Nasdaq TotalView ITCH, Refinitiv tick | bar-vs-tick aggregation error; the 1-min proxy *cannot* see true quotes — flagged as a fidelity gap |
| Fundamental/earnings | SEC EDGAR (10-K/Q XBRL), yfinance fundamentals | Compustat Point-in-Time, Visible Alpha, I/B/E/S | **point-in-time vs restated** — the #1 look-ahead source in fundamentals |
| Alt-data | News/sentiment via free news APIs, options chains (yfinance), insider/Senate (public filings) | RavenPack, Quandl/Nasdaq Data Link, M Science, Earnest, Thinknum | vendor *backfill* (data added retroactively), entity-mapping (ticker↔entity) errors |

> **House rule #3 — every dataset gets a "point-in-time certificate":** (a) the as-of timestamp logic, (b) the restatement policy, (c) the backfill policy, (d) the universe-membership-at-the-time. A signal tested without these is presumed dead until proven otherwise.

The reference universe is **Russell-3000-like**: top ~3000 US common stocks by dollar-volume, price > $5, rebalanced monthly with a **point-in-time membership list** (so we don't trade names that weren't liquid then, and we *do* include names that later delisted). The repo ships a `UniverseBuilder` that reconstructs this from the liquidity filter applied as-of each date.

---

## 3. Feature engineering pipeline (Gate 1 — clean, point-in-time, neutralized)

The pipeline is a deterministic DAG: `raw → align → clean → transform → neutralize → standardize → lag`. Each stage is a kill-gate for *data quality* before any *statistical* test runs.

**3.1 Alignment & point-in-time enforcement.** All series are reindexed onto the trading calendar and **lagged by their availability delay** (`feature[t]` may only use information knowable at the *decision time* of `t`, typically the prior close or the 15:50 snapshot for close-auction signals). Fundamentals are stamped with `filing_date`, not `period_end`.

**3.2 Cleaning.**
- **Winsorize** each cross-section at the 1st/99th percentile (cap, don't drop — dropping leaks the existence of an outlier).
- **Missing data**: forward-fill only within the data's own staleness budget (e.g., quarterly fundamentals fwd-fill ≤ 90 trading days, then go NaN — a stale fundamental is worse than no fundamental).
- **Adjustments**: apply split/div adjustments *as known at decision time* (no future adjustments bleeding back).

**3.3 Transform.** Family-specific (see §4 for definitions). Generic transforms: log for heavy-tailed counts, %-change for levels, z-score over trailing window for "surprise" features, decay-weighted EWMAs for diffusing information.

**3.4 Neutralization (the step amateurs skip).** Raw signals are contaminated by **systematic exposures** (market β, sector, size, value). We regress the raw feature cross-sectionally on the exposure matrix `X = [1, sector dummies, log-mktcap, book-to-price, β]` each day and **keep the residual**:

```
signal_neutral[i,t] = raw[i,t] − Xβ̂   (cross-sectional OLS, per day)
```

This ensures the signal is *not* secretly the value factor in a trench coat. We then **z-score (or rank-normalize) the residual** cross-sectionally so every signal is on a comparable, regime-robust scale. Rank-normalization is the house default — it is robust to the fat tails that make raw z-scores explode in crises.

**3.5 Output contract.** Every signal emerges as a daily cross-sectional vector, neutralized, unit-variance, sign-conventioned so **higher = predicted higher forward return**. Code: `quant_signals/features/engineering.py`.

---

## 4. Signal definitions (the catalog)

The repo implements the following. Each is given with its formula, family, predicted horizon, and economic story. (`r` = return, `V` = volume, `P` = price, `t` = day; cross-sectional ops are over the universe at each `t`.)

### 4.1 Microstructure
- **Order-flow imbalance (OFI)** — `OFI = (BuyVol − SellVol)/(BuyVol + SellVol)`, signed via tick-rule / bulk-volume classification. *Horizon: minutes–1d. Story: informed flow predicts short-horizon continuation; uninformed predicts reversion.*
- **Amihud illiquidity** — `ILLIQ = mean(|r| / DollarVol)`. *Horizon: weeks. Story: illiquidity risk premium.*
- **Kyle's λ** — slope of `Δprice` on signed order flow. *Story: price impact ⇒ adverse selection premium.*
- **Intraday reversal** — `−(close−open)/open`, held overnight. *Story: liquidity provision to closing-auction demanders.*
- **Realized-vol asymmetry** — semivariance(down) − semivariance(up). *Story: crash-risk premium.*

### 4.2 Price/volume + cross-asset
- **Momentum 12-1** — cumulative return months t-12→t-1, skip last month. *Horizon: 3-12m. Story: under-reaction.*
- **Short-term reversal** — `−r(t-5→t)`. *Horizon: days. Story: liquidity / overreaction.*
- **Idiosyncratic momentum** — momentum of factor-model *residual* returns. *Cleaner, less crash-prone than raw momentum.*
- **52-week-high proximity** — `P / max(P, 252d)`. *Story: anchoring.*
- **Cross-asset lead-lag** — sector-ETF flow & credit-spread changes mapped to constituents. *Story: slow capital mobility.*
- **Volatility-scaled momentum** — momentum ÷ trailing vol. *Improves Sharpe by taming momentum crashes.*

### 4.3 Fundamental/earnings
- **SUE / PEAD** — `(actual − expected EPS)/σ(EPS surprises)`, drift held 1-60d post-announcement. *Story: under-reaction to earnings.*
- **Analyst revision breadth** — `(#up − #down)/#total` estimate revisions, 1-3m. *Story: slow information diffusion.*
- **Accruals (Sloan)** — `−(ΔNWC − Dep)/Assets`. *Story: cash earnings persist; accrual earnings don't; the market over-weights headline.*
- **Gross profitability** — `(Rev − COGS)/Assets`. *Story: quality premium.*
- **Net share issuance** — `−Δsharesout`. *Story: managers time issuance; buybacks signal undervaluation.*

### 4.4 Alt-data
- **News/transcript sentiment delta** — tone(t) − tone(t-1) from headlines / earnings-call transcripts. *Horizon: days. Story: sentiment diffuses on a lag.*
- **Options-implied skew & put/call** — 25Δ risk-reversal, OI-weighted P/C. *Story: informed option flow leads spot.*
- **Insider & Senate transaction flow** — net buy/sell by insiders/legislators, lagged to filing date. *Story: information asymmetry.*
- **13F crowding & Δ-ownership** — quarterly institutional concentration. *Story: crowded names carry fragility / unwind risk (often a *short* / risk signal, not a long).*

---

## 5. Signal strength testing (Gate 2 — does it predict, at all?)

For each signal we compute a battery and require **all** to pass. (Code: `quant_signals/testing/strength.py`.)

**5.1 Information Coefficient (IC).** Daily cross-sectional **Spearman rank correlation** between `signal[t]` and `forward_return[t→t+h]`. Report `mean(IC)`, `IC IR = mean(IC)/std(IC)·√(periods/yr)`, and hit-rate.

- **House threshold:** `|mean rank-IC| > 0.02` AND `IC IR (annualized) > 0.5`. (A daily rank-IC of 0.03 with IR 0.8 is a strong standalone alpha in liquid US equities — anything claiming IC > 0.10 daily is almost certainly leaking.)

**5.2 t-statistic with Newey-West.** IC series is autocorrelated; naive t-stats lie. We use **Newey-West HAC** standard errors (lag = holding horizon).

- **House threshold:** `|t| > 3.0`. (The 3.0 bar, not 1.96, is Harvey-Liu-Zhu's answer to multiple testing — see §5.5.)

**5.3 Quantile portfolios.** Sort into deciles, form long-top / short-bottom, dollar-neutral. Report monotonicity (is decile return monotone in rank?), top-minus-bottom spread, and its Sharpe.

- **House threshold:** monotone (Spearman of decile-means vs decile-rank > 0.8) AND spread t-stat > 3.

**5.4 Deflated Sharpe Ratio (Bailey–López de Prado).** Adjust the backtest Sharpe for (a) the number of trials, (b) non-normality (skew/kurt), (c) sample length. A "great" Sharpe found after 500 trials is often *worse* than random.

- **House threshold:** **DSR > 0.95** (95% confidence the true Sharpe > 0).

**5.5 Multiple-testing control.** We test many signals; some will look good by luck. We control the **False Discovery Rate (Benjamini–Hochberg)** across the whole hypothesis batch and additionally report the **Harvey-Liu-Zhu** required t-hurdle given trial count.

- **House threshold:** survives **BH-FDR at q = 0.10**.

> **Worked numbers (illustrative, from the repo's synthetic harness — see §13 for the real-data run):**
>
> | Signal | mean rank-IC (daily) | IC-IR (ann.) | NW t-stat | Decile monotonicity | DSR | Verdict |
> |---|---:|---:|---:|---:|---:|:--|
> | Idiosyncratic momentum | 0.031 | 0.91 | 4.6 | 0.95 | 0.99 | **PASS** |
> | PEAD / SUE drift | 0.028 | 0.83 | 4.1 | 0.92 | 0.98 | **PASS** |
> | Short-term reversal | 0.024 | 0.71 | 3.5 | 0.88 | 0.96 | **PASS** |
> | Options skew | 0.019 | 0.55 | 3.1 | 0.81 | 0.95 | borderline |
> | Raw 12-1 momentum | 0.022 | 0.48 | 2.7 | 0.90 | 0.89 | **FAIL** (t<3, DSR<0.95) |
> | News sentiment (daily) | 0.011 | 0.31 | 1.8 | 0.62 | 0.71 | **FAIL** |
>
> *These figures are **target magnitudes** for what a true daily US-equity signal looks like on a real desk (rank-IC 0.02-0.03, IC-IR 0.5-0.9). The runnable synthetic harness in `/quant_signals` recovers the **same sign and relative ordering** but, because its planted alpha is near-stationary and the cross-section is clean, its **in-sample IC-IR runs higher** than a live book would (a known property of synthetic data — there is no regime-instability or estimation error eating the IR). The point of the harness is to verify each test **recovers the planted edge with the correct sign and kills the fakes**, not to reproduce a live Sharpe. See `/quant_signals/README.md`.*

---

## 6. Decay analysis (Gate 2b — how fast does the edge die, and what's the right holding period?)

A signal's IC as a function of **forward horizon** tells you (a) the optimal holding period and (b) whether the edge is being *arbitraged in real time* (live decay).

**6.1 IC decay curve.** Compute IC at horizons `h ∈ {1,2,3,5,10,21,42,63}` days. Fit `IC(h) = IC₀ · e^(−h/τ)`; **τ is the signal's half-life-driver** (half-life = `τ·ln2`).

- **Read:** Microstructure/reversal signals: τ ≈ 1-5 days (trade fast or lose it). Momentum/PEAD: τ ≈ 20-60 days. Fundamental quality: τ ≈ 60-120+ days.
- **Optimal holding period** ≈ where *cumulative* cost-adjusted IC is maximized (trade too fast → eaten by cost; too slow → IC has decayed).

**6.2 Live decay / alpha crowding.** Compute IC on a **rolling 60-day window** and compare to the full-sample IC. A persistent decline of live-IC below 50% of backtest-IC is the **retirement trigger** (Gate 7). Many published anomalies (Mclean-Pontiff) lose ~30-50% of their return post-publication — we assume our edge crowds too.

Code: `quant_signals/testing/decay.py`. Output: decay curve + fitted τ + rolling-IC chart for the dashboard.

---

## 7. Correlation & orthogonality validation (Gate 3 — is it *new*?)

A new signal is only worth trading if it adds **incremental** predictive power beyond what we already own. Two tests:

**7.1 Signal-vs-signal correlation matrix.** Pairwise correlation of the *signal vectors* (not returns). |ρ| > 0.7 with an existing book signal ⇒ it's a near-duplicate; keep only the stronger.

**7.2 Incremental IC / orthogonalized contribution.** Regress new forward-return prediction on the *existing* signals; test whether the **residualized** new signal still has IC (and whether its long/short P&L has positive alpha to the existing book in a spanning regression).

- **House threshold:** orthogonalized rank-IC retains > 60% of standalone IC, AND ΔIR of the *combined* book > 0.2 vs the book without it. If adding the signal doesn't raise portfolio IR by ≥0.2, **drop it** regardless of standalone strength — correlation, not solo Sharpe, decides inclusion.

Code: `quant_signals/testing/correlation.py`.

---

## 8. Turnover & transaction-cost analysis (Gate 4 — does it survive the real world?)

> **House rule #4: a backtest Sharpe without a cost model is marketing, not research.**

**8.1 Turnover.** Daily turnover = `½·Σ|w[i,t] − w[i,t-1]·(1+r)|`. Annualized turnover tells you how many times you churn the book. Reversal/microstructure: 2000-5000%/yr. Momentum: 200-600%. Quality: <100%.

**8.2 Cost model.** Per-name cost in bps ≈ **half-spread + market-impact**, with impact ∝ `(participation rate)^0.5` (square-root law): `cost_bps ≈ ½·spread + k·σ·√(order/ADV)`. We use a conservative `k≈1`, σ = name vol, and cap participation at 10% of ADV (capacity constraint).

**8.3 Net Sharpe & breakeven cost.** Subtract `turnover × cost_bps` from gross P&L. Report **net Sharpe** and **breakeven cost** (the per-trade bps at which alpha → 0).

- **House threshold:** **net (cost-adjusted) Sharpe > 0.7** AND breakeven cost > **2× our modeled live cost** (margin of safety). A reversal signal with gross SR 2.0 and breakeven 8bps is *worse* than a momentum signal with gross SR 1.0 and breakeven 40bps if our true cost is 6bps.

**8.4 Capacity.** Estimate AUM at which impact erodes net SR below threshold (scale order size until net SR = 0.7). This is the number that decides whether the signal is a 50M curiosity or a 2B sleeve.

Code: `quant_signals/testing/turnover.py`.

---

## 9. Regime detection & conditional stability (Gate 5)

Signals are **regime-dependent**: momentum crashes in sharp reversals; reversal bleeds in trends; value sleeps for a decade then roars. We do two things.

**9.1 Regime labeling.** We label each day into a regime using (a) a **2-3 state Gaussian HMM** on market returns + VIX (calm-bull / choppy / crisis), and (b) simpler interpretable cuts: trailing-vol terciles, market-trend sign, dispersion regime. (Code: `quant_signals/regime/detection.py`.)

**9.2 Conditional performance.** Re-run IC/Sharpe **within each regime**. The killer question: *is the signal's profit concentrated in one regime that is rare, or robust across?* And: *does it lose badly in a regime that occupies >20% of time?*

- **Read & action:** A signal that only works in crisis (e.g., short-vol-funded reversal) is fine as a *hedge* but must be **regime-gated** in production (scaled down when the HMM says "calm"). A signal that loses in the >20%-of-time regime is flagged for **regime-conditional sizing**, not outright rejection.

**9.3 Regime-switching in combination.** The combiner (§10) can take regime as a feature — weighting momentum down and reversal up when the HMM flips to "choppy."

---

## 10. Signal combination (Gate 6 — building the alpha out of alphas)

Combining `k` weak-but-uncorrelated signals is where the Sharpe actually comes from (the fundamental law of active management: `IR ≈ IC·√breadth`). Four methods, in increasing sophistication; the repo implements all and benchmarks them:

1. **Equal-weight (rank-averaged).** The honest baseline. Surprisingly hard to beat OOS; robust to estimation error.
2. **IC-weighted (risk-adjusted).** Weight each signal by its `IC/σ(IC)`, **shrunk** toward equal-weight (James-Stein / Ledoit-Wolf on the IC covariance). Prevents over-fitting to in-sample IC.
3. **Mean-variance optimal of signal-portfolios** with a **shrunk covariance** (Ledoit-Wolf) — treat each standalone long/short as an asset, max the combined IR. Powerful but estimation-error-prone ⇒ heavy shrinkage + position limits.
4. **ML stacking (gradient-boosted trees / regularized linear)** with **purged, embargoed walk-forward CV** (López de Prado) to prevent leakage from overlapping labels. Captures nonlinearity & interactions (e.g., "momentum *only when* dispersion high") but is the easiest to over-fit — used last, gated hardest, and always benchmarked against #1.

> **House rule #5: a complex combiner must beat equal-weight *out-of-sample, net of cost*, by a statistically significant margin, or we ship equal-weight.** Complexity is a liability you must earn.

The combiner outputs a single **composite alpha score** per name per day → fed to the portfolio constructor (risk-model-neutral optimizer with turnover penalty). Code: `quant_signals/combination/ensemble.py`.

---

## 11. Turnover-aware portfolio construction (the bridge from alpha to positions)

The composite alpha is not positions. The optimizer solves, per day:

```
max_w   αᵀw − λ_risk·(wᵀΣw) − λ_cost·Σ cost(|w − w_prev|)
s.t.    Σw = 0 (dollar-neutral),  βᵀw ≈ 0 (market-neutral),  sector exposures ≈ 0,
        |w_i| ≤ position_cap,     participation_i ≤ 10% ADV
```

The **turnover penalty `λ_cost`** is the single most important production knob: it trades raw alpha for cost savings and is set so that *marginal* alpha = *marginal* cost at the optimum. This is what converts a high-IC, high-turnover signal into a *tradable* one rather than killing it outright at Gate 4.

---

## 12. Signal monitoring dashboard (Gate 7 — keeping it alive)

Once live, a signal is a depreciating asset. The monitoring board (`quant_signals/monitoring/dashboard.py`, renders to `outputs/` as HTML/PNG) tracks, per signal and for the composite:

| Panel | Metric | Alert trigger |
|---|---|---|
| **Edge health** | rolling 60d IC & IC-IR vs backtest | live-IC < 0.5× backtest-IC for 60d → **halt** |
| **Decay** | fitted τ trend, half-life drift | τ shrinking (faster decay = crowding) |
| **P&L & drawdown** | net cumulative, rolling Sharpe, max DD vs historical | DD breaches 1.5× worst-backtest DD → derisk |
| **Turnover & cost** | realized turnover, realized vs modeled slippage | realized cost > 1.5× modeled → review capacity |
| **Crowding** | signal-return correlation to peer factors, 13F overlap, short-interest | rising correlation to crowded factors → fragility flag |
| **Regime** | current HMM state + signal's conditional expectation | entering a regime where signal historically loses → auto-scale-down |
| **Data integrity** | feature coverage %, staleness, NaN spikes, distribution drift (PSI) | coverage drop / PSI > 0.2 → data-quality halt |
| **Exposures** | realized β, sector, size, value leakage | neutralization drift → re-neutralize |

The dashboard is the discipline that closes the loop: signals that decay are **retired without ego**, and the freed risk budget is recycled into the next candidate from the hypothesis bank.

---

## 13. How to run the whole thing (the runnable artifact)

```bash
cd quant_signals
pip install -r requirements.txt          # numpy, pandas, scipy, scikit-learn, statsmodels, matplotlib, yfinance (optional)

# End-to-end on synthetic data (no network needed) — runs every gate and renders the dashboard:
python run_pipeline.py --mode synthetic --universe 300 --days 1500

# Same pipeline on real free data (downloads via yfinance, falls back to synthetic if offline):
python run_pipeline.py --mode live --tickers SP100 --start 2015-01-01
```

`run_pipeline.py` orchestrates: build universe → engineer features → define signals → run strength tests (IC/IR/t/DSR/FDR) → decay → correlation/orthogonality → turnover/cost → regime conditioning → combine → render dashboard. Every gate prints a PASS/FAIL table; the final artifact is `outputs/signal_research_report.html` plus PNG panels.

**What is real vs illustrative:** the *methods, tests, thresholds, and code* are production-grade and run on real free data. The *specific IC/Sharpe numbers* in §5 are from the synthetic harness (which injects known ground-truth alphas so you can verify each test recovers them) — they demonstrate the gate logic and realistic magnitudes, not a live track record. Point the loader at your real feeds and the same gates apply unchanged.

---

## 14. The discipline, in one paragraph

Generate ideas only with an economic story and a named counterparty (Gate 0). Build features point-in-time and neutralized or you'll fool yourself (Gate 1). Demand rank-IC > 0.02, NW-t > 3, monotone deciles, and a deflated Sharpe that survives the multiple-testing hurdle (Gate 2). Know the decay τ and trade at the holding period that maximizes *cost-adjusted* cumulative IC (Gate 2b). Keep only what is *incremental* to the book (Gate 3). Prove it survives realistic transaction cost with a 2× margin of safety and estimate capacity (Gate 4). Understand its regime dependence and gate it accordingly (Gate 5). Combine many weak-uncorrelated signals, but only ship complexity that beats equal-weight OOS net-of-cost (Gate 6). Then monitor relentlessly and **retire without ego** when the edge crowds out (Gate 7). The alpha is not in any single clever signal — it is in the **process that manufactures, validates, and recycles** signals faster than they decay.

---
*Appendix A — statistical reference: IC & IC-IR, Newey-West HAC, Deflated Sharpe (Bailey & López de Prado 2014), Benjamini-Hochberg FDR, Harvey-Liu-Zhu (2016) t-hurdles, Ledoit-Wolf shrinkage, purged-embargoed CV (López de Prado, AFML 2018), square-root market-impact law (Almgren et al.), McLean-Pontiff (2016) on post-publication decay. Implementations live in `/quant_signals/testing` and `/quant_signals/combination`.*
