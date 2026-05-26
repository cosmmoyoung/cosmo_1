# Probe Cards — Deep-Dive Investment Memo
### FormFactor (FORM, Nasdaq) & Technoprobe (TPRO.MI, Milan)
*Author: senior buy-side analyst*
*As of 26 May 2026. Companion to `ai_supply_chain_framework.md` (§5.4) and `bom_walk_chokepoints.md` (top BOM-walk find). Follows the house template: business → demand bridge → TAM endpoints → reverse "priced-in" test → per-company ceiling → bear case → variant perception.*

---

## A note on data quality before we start

I built this from Q1-CY2026 prints (FORM reported 29 Apr 2026; Technoprobe 14 May 2026), the companies' IR, and reputable aggregators. The sandbox blocked direct retrieval of **Technoprobe's IR PDFs (403)** and some FORM GlobeNewswire/StockTitan pages, so a few figures are multiply-sourced via press rather than primary filings.

**Numbers I am confident on** (multiply-sourced, consistent): FORM Q1-CY26 revenue $226.1m (+32%) and the segment split (DRAM probe cards +70% YoY is the key live datapoint), FORM Q2 guide ($240m), Technoprobe FY25 (€628.4m rev, 32.1% EBITDA margin) and the **raised guidance** (FY26 €950m–1,050m rev, 44–46% EBITDA margin — a major positive event, stock +36% on the print), the ~$3.3bn (2025) probe-card TAM and ~9–10% base-case CAGR, and the consolidated top-5 ~73% share.

**Numbers I explicitly distrust / flag** (the memo does NOT lean on these as point estimates):
1. **FORM's aggregator multiples are internally inconsistent** — a "forward P/E ~26×" cannot be reconciled with "FY26 EPS ~$1.93" at a ~$128 share price (that implies ~66×), and a quoted "EV/EBITDA ~27×" implies a ~45% EBITDA margin that is *above* FORM's gross margin — impossible. I therefore run the priced-in test on **EV/Sales and a scenario-based EV/EBITDA range with stated margin assumptions**, not on a single quoted multiple. *Verify all FORM/TPRO multiples on a terminal before acting.*
2. **The "Technoprobe ≈30% of TSMC 2nm qualifications" claim is UNVERIFIED** and partly *contradicted* by TSMC qualifying **MJC (Micronics Japan) as a primary 2nm supplier (Aug 2025)**. I do not print the 30% figure as fact; I treat it as an un-underwritten bull claim.
3. **There is no clean published "test-seconds-per-die" index.** The entire "test intensity rises super-linearly" thesis (the variant perception, §8) rests on qualitative + proxy evidence, not a hard number. This is the #1 thing to harden.
4. Technoprobe market-cap sources conflict (€11.8bn vs €16.7bn — I use ~€11.8bn, which ties to ~€26 × ~454m shares); **Teradyne's reported 10% stake needs primary confirmation**; customer-concentration % for TPRO is undisclosed.

A complete picture needs FORM's FY2025 10-K customer-concentration note, Technoprobe's FY25 PR + Q1-26 deck pulled directly, and a TechInsights/Yole primary test-intensity index. Flagging so the reader can close these.

---

## 1. Business description — what a probe card is, and why it's a chokepoint

A **probe card** is the electro-mechanical interface between the test machine (ATE — Teradyne/Advantest) and the **bare wafer**. Hundreds-to-thousands of micro-probes land on each die's pads/bumps at **wafer sort** to test electrical function *before* the wafer is diced and packaged. Three features make it a chokepoint, not a commodity:

1. **Bespoke per device.** A probe card is custom-designed to one chip's pad map, pin count and frequency. A new device design = a new probe card. It is not reusable across designs. This makes the business a **recurring redesign annuity**: every new GPU/ASIC/HBM die, every shrink, every chiplet variant pulls a fresh card.
2. **Consumable, not just capex.** The probe tips/heads **wear with touchdowns** and need replacement. So demand tracks **wafer volume**, not only equipment capex — a more resilient, razor-blade-like demand stream than WFE tools (this matters enormously for the multiple — see §8).
3. **MEMS/vertical-probe IP moat + qualification lock-in.** The advanced standard is MEMS / vertical probe (vs. legacy cantilever). Cards are co-designed and **qualified per device with the foundry/IDM over months** — once designed-in, switching is costly and slow. FORM paid ~$120m (Oct 2025) to acquire a California MEMS firm — a tell that the IP is scarce.

### Why AI raises "test intensity" (the demand thesis)
The AI build raises probe-card content per unit of compute through several stacked effects:

- **HBM Known-Good-Die (KGD):** every DRAM die in a stack must be probed/tested **before** stacking (you cannot afford a bad die inside a 16-high stack), then the assembled stack is re-tested at multiple points → **multiplicative touchdowns** vs. a monolithic die. *(Source: FormFactor, "KGD test enables advanced packaging for HBM," 2024 [SRC].)*
- **HBM stack height 8-high (HBM3) → 16-high (HBM4):** FORM states directly that "the increase in layer count to 16-high increases the number of probe-cards required for good chip out." [SRC]
- **Advanced logic (2nm GAA, chiplets/2.5D):** higher frequency + lower-insertion-loss cards (FORM's K40: −3 dB at 7 GHz, supports HBM4/LPDDR6/GDDR7), and **chiplet disaggregation multiplies the number of *unique die types*** → more bespoke cards per "system."
- **ATE parallelism proxy:** Teradyne's Magnum 7H HBM tester carries up to 9,216 digital + 2,560 power pins and 1.6× throughput vs. prior gen — a proxy for the rising pin-count/parallelism the card must mate to. [SRC]

> **The live proof:** FORM's **DRAM probe-card revenue grew +70% YoY in Q1-CY2026** — that is the HBM/KGD content step-up showing up in the P&L *right now*, not a 2030 promise. [SRC]

---

## 2. The demand bridge — first principles (per framework §1)

```
AI compute demand
  → advanced-die wafer starts (2nm logic + HBM DRAM)        [units]
  → × KGD test requirement (test before stack)              [content ×]
  → × stack height 8→16-high (more cards/good-die-out)      [content ×]
  → × chiplet design proliferation (more unique die types)  [content ×]
  → × higher-spec MEMS card ASP (frequency/pin count)       [ASP ×]
  → × consumable replacement (tips wear w/ touchdowns)      [recurring]
  = probe-card demand
```

This stacks **three content multipliers + an ASP multiplier on top of unit growth** — i.e., it is *multiplicative*, exactly the "elasticity layer" the framework targets (§1.2). The catch (vs. InP or glass cloth): the absolute TAM is small **and** the unit base (wafer starts) is itself only mid-single-digit growth, so the elasticity comes from *content per wafer*, not from runaway unit growth. That makes the **content-step-up magnitude (1.3× vs 2× per HBM generation) the single most thesis-load-bearing number** — and it is the one nobody has cleanly published (§A, gap #3).

---

## 3. TAM endpoints & bridge

| | Old TAM (pre-AI ~2022) | 2025 | 2030E base | 2030E bull |
|---|---:|---:|---:|---:|
| Total probe-card TAM | ~$2.4bn [EST] | **~$3.3bn** [SRC] | **~$5.0bn** (@~9–10% CAGR) | **~$7–8bn** (content super-linearity) |
| of which MEMS/advanced (AI-levered) | ~$1.0bn [EST] | ~$1.74bn [SRC] | ~$3.0bn | ~$4.5–5bn |
| of which DRAM/HBM | ~$0.7bn [EST] | ~$1.3bn [EST] | ~$2.2bn | ~$3.5bn |

**Bridge decomposition (2025 → 2030 base, ~+$1.7bn):** ~⅓ unit/wafer-start growth, ~½ content (KGD + 16-high + chiplet design count), ~⅙ ASP/mix (higher-spec MEMS). The **bull case ($7–8bn) requires the content multiplier to run ~2× per HBM generation rather than ~1.3×** and is where the variant perception lives.

> **Key framing for "how big to how big":** this is the most modest TAM in the whole AI-supply-chain screen — ~$3.3bn going to ~$5bn base. It clears the investor's filter on *elasticity-per-content × chokepoint × small-base × ownable*, **not** on absolute market size. The thesis is "a small market with pricing power and two clean listed leaders," not "a huge market."

---

## 4. Market structure & moat

| Player | Share (2025, total probe card) | Position | Trend |
|---|---|---|---|
| **FormFactor (US)** | **~30%** (No. 1) | Leads **DRAM/HBM** + strong foundry-logic | Stable leader; HBM-levered |
| **Technoprobe (IT)** | top-2; leads/co-leads **MEMS advanced-logic** | Logic/TSMC-levered, highest margin | Gaining in AI/logic |
| Micronics Japan (MJC) | ~14% (No. 3) | **Qualified as TSMC *primary* 2nm supplier (Aug 2025)** | **Gaining at the leading node** |
| JEM / MPI / others | balance | — | — |
| **Top-5 combined** | **~73%** | Consolidated oligopoly | Consolidating |

*Share denominators differ by source (total vs. MEMS-only vs. by end-segment) — treat as directional; FORM clearly leads DRAM/HBM while Technoprobe leads/co-leads advanced-logic MEMS.* The **moat = MEMS IP + multi-month per-device qualification lock-in**, evidenced by structurally high and *rising* margins (FORM probe-card GM 50.5% in Q1-CY26; Technoprobe EBITDA margin 32%→44–46% guided). **The MJC 2nm qualification is the live "monopoly-decay" risk** (framework §5.4 lesson) — share at the leading node is contestable.

---

## 5. The reverse "priced-in" test (framework §2.1)

Because the aggregator P/E and EV/EBITDA point-estimates are inconsistent (§A), I anchor on **EV/Sales** (least ambiguous) and a **scenario EV/EBITDA with explicit margin assumptions**, then back out the implied terminal TAM/share and compare to §3.

### 5.1 FormFactor
- **Current EV ≈ $9.5–10.0bn** (mkt cap ~$10.05bn, ~debt-light); **fwd revenue ~$0.96–1.0bn** → **EV/Sales ≈ 10×.**
- 10× sales for a ~30%-share test company whose *underlying TAM* compounds ~10% is a **full multiple** — a steady-state quality semicap consumable would fairly sit ~4–6× through-cycle. **10× embeds either sustained ~20%+ revenue growth or a consumable re-rating.**
- **Reverse-engineering the implied terminal** (range, EBITDA margin assumed 22–26% normalized):

| Fair terminal EV/EBITDA | Implied terminal EBITDA | → Implied revenue @24% margin | → Implied TAM @30% share | vs $5bn base 2030 |
|---:|---:|---:|---:|---|
| 15× | $650m | $2.7bn | **$9.0bn** | 1.8× over base |
| 18× | $542m | $2.3bn | **$7.5bn** | 1.5× over base |
| 22× | $443m | $1.85bn | **$6.2bn** | 1.2× over base |

> **Verdict (FORM):** under *every* reasonable terminal multiple, today's EV implies a probe-card TAM **above the ~$5bn base case** (or share gains beyond 30%, or margins above 24%). The base-case TAM does **not** support forward upside at 10× sales — **FORM is priced for the variant perception (content super-linearity / re-rating) to be RIGHT.** This is "right chokepoint, full price," not a fat pitch.

### 5.2 Technoprobe
- **Current EV ≈ €11.1bn**; **fwd revenue ~€1.0bn** (guided) → **EV/Sales ≈ 11×**, but at a **44–46% EBITDA margin** vs FORM's mid-20s%. Margin-adjusted, TPRO's 11× sales is *"cheaper"* than FORM's 10× — each euro of revenue drops ~2× more to EBITDA. On **fwd EV/EBITDA both sit ~24×.**
- **Reverse:** at €11.1bn EV / 22× fair EBITDA → implied terminal EBITDA ~€505m → at 45% margin → revenue ~€1.12bn → at ~25% advanced-logic share → implied advanced-logic probe TAM ~€4.5bn. **More achievable relative to its served market than FORM's**, *because the just-raised guidance already pulls FY27 targets into FY26* (positive estimate-revision momentum).

> **Verdict (TPRO):** higher-quality margin profile + positive guidance revisions make the "priced-in" hurdle *less* stretched than FORM's — but you pay with **governance/liquidity risk (Crippa family 63%, free float ~16.5%)** and **customer/2nm-share concentration** (the unverified TSMC claim + MJC threat). Quality at a full-but-not-absurd price.

### 5.3 Relative read
Same chokepoint, two expressions: **FORM = the more liquid, HBM-content-step-up beta** (SK Hynix 29.5% of revenue; DRAM +70% YoY) priced for the bull case; **TPRO = the higher-margin, logic-levered quality compounder** with a governance/float discount and a contestable 2nm narrative. Neither is cheap; TPRO is the better margin-adjusted value, FORM the better pure-play on the HBM4 content step-up.

---

## 6. Per-company ceiling — "how big can it get vs. how big it is now" (framework §3)

### 6.1 FormFactor

| | Today (FY26E) | 2030 base | 2030 bull (content 2× + share 33%) |
|---|---:|---:|---:|
| Probe-card TAM | $3.3bn (25) | $5.0bn | $7.5bn |
| FORM share | ~30% | 30% | 33% |
| FORM probe-card rev | ~$0.83bn | $1.5bn | $2.5bn |
| + Systems | ~$0.13bn | $0.16bn | $0.20bn |
| **Total revenue** | **~$0.96bn** | **~$1.66bn** | **~$2.7bn** |
| Net margin (normalized) | ~18–20% | 21% | 24% |
| Net income | ~$185m | ~$350m | ~$650m |
| Fair P/E | — | 24× | 28× |
| Implied market cap | $10.05bn (now) | **~$8.4bn** | **~$18.2bn** |
| PV @14% (4 yr) | — | **~$5.0bn (−50%)** | **~$10.8bn (≈ today)** |

> **The uncomfortable read:** discounted back, FORM's **base case is ~50% below today's price**, and even the **bull case only ≈ matches today's price.** You are paying for the bull case as your *base*. For this to work you need a *super-bull* (TAM > $8bn / share > 33% / re-rating to a consumable multiple).

### 6.2 Technoprobe

| | Today (FY26E guided) | 2030 base | 2030 bull |
|---|---:|---:|---:|
| Revenue | ~€1.0bn | €1.6bn | €2.4bn |
| EBITDA margin | 44–46% | 45% | 47% |
| EBITDA | ~€460m | €720m | €1,130m |
| Fair EV/EBITDA | — | 18× | 22× |
| Implied EV | ~€11.1bn (now) | **~€13.0bn** | **~€24.9bn** |
| PV @14% (4 yr) | — | **~€7.7bn (−30%)** | **~€14.7bn (+33%)** |

> **Read:** TPRO's higher margin means the **base case is "only" ~30% below today** (vs FORM −50%) and the **bull case offers ~+33% PV upside** — a *better-shaped* risk/reward than FORM, consistent with §5.2. But the upside still requires revenue to ~2.4× by 2030 *and* the governance/concentration risks not to bite.

*(Ceiling tables use my normalized-margin and fair-multiple assumptions; the FORM EPS-consensus inputs are unreliable per §A, so treat these as scenario scaffolding, not precision forecasts.)*

---

## 7. Bear case

1. **Memory cyclicality.** DRAM/HBM is the most volatile demand vector; FORM's DRAM +70% can reverse hard in an HBM digestion air-pocket (e.g., if HBM4 qual slips or hyperscaler capex pauses). FORM's 2022→2023 revenue fell −11% in the last downcycle. SK Hynix at 29.5% of revenue concentrates this.
2. **Monopoly decay at the leading node.** MJC qualified as a TSMC *primary* 2nm supplier (Aug 2025) — directly threatens the advanced-logic share both leaders rely on for the re-rating. The "chokepoint" is more contestable than the multiple assumes (the framework §5.4 standing risk, live here).
3. **The TAM is just small.** Even the bull case is a ~$7–8bn market. There is a ceiling on how big a 30%-share player can get — FORM's *bull-case* market cap (~$18bn) is only ~1.8× today, and only ≈ today on a PV basis.
4. **Content step-up may be ~1.3×, not ~2×.** The whole elasticity case rests on an unpublished number (§A). If KGD/16-high adds ~30% content rather than ~100% per generation, the bull TAM collapses toward the base.
5. **Valuation already embeds the bull** (§5–6). The base case is downside in both names.
6. **TPRO-specific:** 16.5% float + 63% family control = liquidity/governance discount and event risk; the load-bearing 2nm-share claim is unverified.

---

## 8. Variant perception — where consensus may be wrong (the edge)

The bull edge is a **multiple-regime** argument, not a "bigger market" argument:

> **The Street models probe cards as cyclical WFE/test *capex*. They are increasingly a rising-content *consumable* — a per-die, per-design, per-touchdown razor-blade annuity whose content compounds with HBM stack height, KGD and chiplet proliferation every node.** If demand is (a) more recurring/volume-linked than capex-cyclical *and* (b) growing content super-linearly (~2× per HBM gen, not ~1.3×), then both the **growth rate** *and* the **fair multiple** are too low in consensus — and the two compound.

What would confirm it (the things to underwrite — these are the deep-dive's open questions):
- A **hard test-intensity index** (test-seconds or touchdowns per die, or probe-cards per wafer-out) across HBM3→HBM4→HBM4E. This single number (§A gap #3) decides base-vs-bull. **Get TechInsights/Yole primary.**
- **Aftermarket/consumable revenue mix** — how much of FORM/TPRO revenue is recurring tip/head replacement vs. new-card capex? A high recurring mix justifies the consumable re-rating.
- **Whether DRAM probe-card growth (+70%) is HBM4 content or a one-off restock** — a second quarter of it would be strong confirmation.

**Honest synthesis:** probe cards is a *genuine* chokepoint and the cleanest *investable* find of the BOM walk — but the re-rating has already happened. At today's prices you are **not** buying a mispriced chokepoint cheaply; you are **buying the variant perception (consumable-content super-linearity) at roughly fair-to-full value**, with FORM pricing it more aggressively than Technoprobe. The alpha is in *confirming the test-intensity number before the Street puts it in models* — if it's ~2×, both re-rate; if it's ~1.3×, both are expensive.

---

## 9. Verdict & what to watch

- **Rank vs. the investor's filter:** clears elasticity/criticality/bottleneck/small-base/ownability — **fails (for now) on valuation headroom.** "Right chokepoint, full price."
- **Preferred expression if forced:** **Technoprobe** on margin-adjusted value + estimate-revision momentum, sized small for governance/liquidity risk; **FormFactor** as the higher-beta pure-play on the HBM4 content step-up — but only with conviction on the ~2× content thesis, and ideally bought into a memory-cycle air-pocket (the bear case #1 is also the entry opportunity).
- **The three things to watch:** (1) a primary **test-intensity index** HBM3→HBM4; (2) **FORM DRAM probe-card growth durability** (a second +YoY quarter); (3) **MJC/Chinese share at TSMC 2nm** (monopoly-decay check).
- **Next in queue:** InP/EML lasers (highest framework conviction), then optical transceivers (Eoptolink), then HBM (with BESI/TCB→hybrid-bonding folded in).

---

## Sources
- FormFactor Q1-CY2026 results/slides/transcript (Investing.com; Motley Fool transcript, 29 Apr 2026); FY2025 Q4 (GlobeNewswire, 4 Feb 2026); revenue history (Macrotrends); statistics (StockAnalysis).
- FormFactor "Known-Good-Die test enables advanced packaging for HBM" (2024); K40 card specs; ~$120m MEMS acquisition (Oct 2025).
- Teradyne Magnum 7H HBM tester press release.
- Technoprobe Q1-2026 call highlights & "shares +36% on raised targets" (Investing.com, 14 May 2026); FY2025 PR (18 Mar 2026); Q1 EBITDA €69.2m (MarketScreener); valuation (StockAnalysis BIT:TPRO). *Primary IR PDFs blocked in sandbox — verify directly.*
- Probe-card market: Mordor Intelligence (~$2.71bn narrow def., 47.59% Foundry&Logic, +11.02% NAND CAGR, $4.23bn 2031); Business Research Insights ($3.31bn 2025, 9.85% CAGR to $7.02bn 2033); MEMS Probe Card market (~$1.74bn 2025).
- Share/structure: aggregated 2025 (FORM ~30%, MJC ~14%, top-5 ~73%); MJC qualified TSMC primary 2nm supplier (Aug 2025).
- **Flagged unverified:** Technoprobe "~30% of TSMC 2nm quals"; Teradyne 10% TPRO stake; no clean published test-seconds/die index.
