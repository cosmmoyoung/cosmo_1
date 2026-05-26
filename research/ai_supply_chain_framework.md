# AI Supply Chain — Master Valuation Framework
### "How much is priced in, and where is consensus wrong?"
*Author: senior buy-side analyst*
*As of 26 May 2026. This is the FRAMEWORK document (methodology + chokepoint map + hypothesis bank). Per-sector deep-dive memos follow separately under `/research`.*

---

## 0. The question, restated precisely

The investor's problem is **not** "is AI a real long-term trend" (it is, and that is consensus). The problem is a **pricing** problem with three nested sub-questions:

1. **From what size to what size?** Each AI-supply-chain segment has been re-rated from an "old TAM" (telecom-era, PC/server-era, commodity-cycle) to a "new AI TAM." We need to measure *both endpoints* and the *bridge* between them — because the bridge (volume × content × ASP × attach) is where the assumptions live.
2. **What is priced in?** Given today's price, what TAM / market-share / margin / duration is the market *requiring* the company to deliver? This is a reverse-engineering exercise, not a forward-DCF exercise. If the implied TAM the price requires is already beyond the credible terminal TAM, the name is expensive even if the trend is real.
3. **Where is consensus wrong?** The edge is almost never "AI is big." The edge is in one of: (a) **content/intensity per unit** rising faster than the Street models (the optics-attach and HBM-per-GPU story), (b) **bottleneck duration** lasting longer than the Street's mean-reversion assumption (the sold-out chokepoints), (c) a **small base** that the Street can't size because there's no clean comp, or (d) a **mis-attributed risk** (e.g., CPO "kills" transceivers — true or false?).

> **Core thesis filter (the investor's own words):** we want segments that are **high-elasticity × mission-critical / 卡脖子 (indispensable, chokepoint) × long-dated visible demand × small-enough base to grow an order of magnitude.** The segment does NOT need to be a large industry or the company a large company. Elasticity + indispensability + a small base is the ideal — that is the Nittobo T-glass template (sold-out, oligopoly, ASP 5–10x commodity, demand inelastic to its own price because it's a tiny BOM line that gates a $40k server).

---

## 1. The demand spine — first-principles derivation chain

Everything downstream is a **derived demand**. There is exactly **one exogenous driver** at the top of the funnel, and everything else is a transfer function applied to it.

```
                         (EXOGENOUS)
            ┌─────────────────────────────────────┐
            │   AI COMPUTE DEMAND                  │
            │   = Training FLOPs + Inference FLOPs │
            └─────────────────┬───────────────────┘
                              │  monetized as ↓
            ┌─────────────────────────────────────┐
   LAYER 1  │   AI CAPEX ($)                       │  ← hyperscaler + neocloud + sovereign
            │   the dollars actually spent          │
            └─────────────────┬───────────────────┘
                              │  ÷ system ASP →
            ┌─────────────────────────────────────┐
   LAYER 2  │   ACCELERATOR UNITS (GPU / ASIC)     │  ← the physical "cell" that replicates
            │   + the RACK/CLUSTER it sits in       │
            └─────────────────┬───────────────────┘
                              │  × content intensity per unit →
            ┌─────────────────────────────────────┐
   LAYER 3  │   COMPONENT DEMAND (units × content) │  ← HBM stacks/GPU, optics/GPU, PCB
            │   THE ELASTICITY LAYER                │     area/GPU, laser chips/module …
            └─────────────────┬───────────────────┘
                              │  × ASP × mix →
            ┌─────────────────────────────────────┐
   LAYER 4  │   SEGMENT TAM ($)                    │
            └─────────────────┬───────────────────┘
                              │  × company share × margin →
            ┌─────────────────────────────────────┐
   LAYER 5  │   COMPANY EARNINGS CEILING → FAIR MC │
            └─────────────────────────────────────┘
```

### 1.1 Two demand regimes (do not conflate them)

| | **Training** | **Inference** |
|---|---|---|
| Driver | Model scaling (params × tokens × frontier-lab competition) | End-user/agent token consumption |
| Shape | Lumpy, capex-cycle, winner-take-most, **policy/funding-sensitive** | Compounding, utility-like, **revenue-linked** |
| Bull case | Frontier scaling continues; Rubin/next-gen | Agents + reasoning models → token explosion (10–100x) |
| Bear case | Scaling plateaus, ROI scrutiny, capex air-pocket | Inference deflation (price/token falls faster than volume) |
| Investment read | This is the **lumpiness/air-pocket** risk in all names | This is the **durability** that underwrites the terminal TAM |

> **Why this matters for "priced in":** a segment whose demand is mostly *training-capex-linked* deserves a lower terminal multiple (cyclical, lumpy) than one whose demand rides *inference token growth* (utility, compounding). The market frequently applies one multiple to both. **Mispricing hides in the regime mix.**

### 1.2 The master variable: **content intensity per accelerator** (Layer 3)

Unit growth (Layer 2) is roughly *common* to every AI name and is the most consensus part of the model. **The differentiated edge lives in content intensity per accelerator and its rate of change.** This is the elasticity multiplier:

- **HBM:** GB of HBM per GPU is rising every generation (H100 → Blackwell → Rubin). Demand grows even if GPU *units* are flat.
- **Optics:** transceivers per GPU rises as networks go to higher radix / scale-out and rail-optimized topologies; **and** ASP per transceiver rises 800G→1.6T→3.2T. **Double-counted elasticity** (more modules × higher $/module per GPU).
- **Laser chips (EML/InP):** lasers per transceiver rises (more lanes), so this compounds *on top of* the optics-per-GPU growth → **triple-derivative** elasticity.
- **PCB/CCL/glass-cloth:** layer count and area per board rise; material spec jumps (low-Dk/low-CTE), ASP/m² jumps 5–10x → content × ASP elasticity.

> **Rule:** the further down the BOM you go toward a *gating chemistry/physics input* (glass cloth, InP wafer, EML chip), the more the elasticity is "units × content × ASP × attach" stacked — and the smaller the base, hence the bigger the multiple-of-current-size headroom. This is precisely the investor's target zone.

---

## 2. The TAM-bridge methodology — "from how big to how big"

For each segment we build an explicit **bridge from Old TAM to New (terminal) TAM**, decomposed so the assumptions are visible and auditable:

```
Old TAM (pre-AI, e.g. CY2022)
  + Δ from UNIT growth          (accelerator units)
  + Δ from CONTENT growth        (intensity per unit)
  + Δ from ASP/MIX               (spec upgrade, premiumization)
  + Δ from ATTACH/PENETRATION    (new use that didn't exist)
  − Δ from DEFLATION/SUBSTITUTION (price erosion, tech displacement e.g. CPO)
= New (terminal) TAM (e.g. CY2030)
```

We do this at **two horizons** (per the investor's instruction):
- **NTM / CY2027 anchor** → tests "is the *near-term* multiple supported by *near-term* earnings power" (downside / margin-of-safety lens).
- **CY2030 terminal anchor** → tests the *ceiling*; upside lens; the number the bulls are really paying for.

### 2.1 "What's priced in" = the reverse exercise

Instead of (or alongside) a forward DCF, we **back out** from the current EV the operating outcome the price *requires*:

1. Take current EV.
2. Apply a *defensible terminal multiple* (what should this business trade at in steady state — gross margin, cyclicality, moat).
3. Solve for the **implied terminal earnings** → implied terminal revenue (at terminal margin) → **implied segment TAM × required share**.
4. Compare that **implied TAM** to the **credible terminal TAM** from §2.

> **Verdict logic:**
> - Implied TAM **<** credible terminal TAM, with a real moat → *room; possibly under-priced.*
> - Implied TAM **≈** credible terminal TAM → *fully valued; you're paying for the base case, no margin of safety.*
> - Implied TAM **>** credible terminal TAM, or requires share the company can't physically supply → *over-priced; the trend can be 100% right and you still lose.*

This single test directly answers the investor's "how much is priced in." We will compute it for every name.

---

## 3. Per-company sizing — ceiling vs. current

The investor's specific ask: *"if a company has X% of this market, how big a company can it become, vs. how big is it now?"* The bridge:

```
Terminal company revenue  =  Terminal segment TAM  ×  defensible market share
Terminal EBIT             =  × terminal operating margin
Terminal fair market cap  =  Terminal EBIT × (1−tax) × terminal P/E   (or EV/EBIT)
"Headroom multiple"       =  Terminal fair MC ÷ current MC   (then discount to PV at ~12–15%/yr)
```

We report, for every name, a single comparison the investor asked for:

| Metric | Today | Terminal (CY2030 base) | Headroom |
|---|---|---|---|
| Segment TAM | $X bn | $Y bn | Y/X |
| Company share | a% | b% | — |
| Company revenue | $ | $ | — |
| Net income | $ | $ | — |
| Implied fair MC | (= current) | $ | **× multiple** |
| PV of terminal MC @14% | — | $ | **× vs today** |

A name only clears the bar if the **PV-discounted** terminal MC is still meaningfully above today's MC AND the §2.1 reverse test doesn't already require a heroic TAM.

---

## 4. The chokepoint screen — what qualifies as "high-elasticity 卡脖子"

Every candidate segment is scored 1–5 on six axes. We are explicitly **willing to accept a small absolute TAM** if elasticity + bottleneck + base are right (the investor's instruction).

| Axis | Question | 5 = best |
|---|---|---|
| **E — Elasticity** | How many derivatives of AI-compute does demand stack (units × content × ASP × attach)? | Triple/quadruple-derivative (e.g., InP lasers) |
| **C — Criticality** | Does the AI server *not work* without it? Is it on the critical path / gating BOM? | Mission-critical, no substitute |
| **B — Bottleneck** | Oligopoly? Sold-out? Multi-year lead time? Hard-to-replicate (physics/chemistry/yield/capex)? | 1–3 suppliers, sold-out into 2027 |
| **V — Visibility** | Is demand long-dated and *inference-underwritten* (durable) vs. training-lumpy? | Locked multi-year, inference-linked |
| **S — Small base** | Is current revenue small enough that an order-of-magnitude move is physically possible? | Sub-scale today, 10x headroom |
| **H — Headroom** | After the re-rating, does valuation still leave the §2.1 test passable? | Implied TAM << terminal TAM |

**The ideal name scores high on E·C·B·S and is *not yet* maxed on H.** A name that scores 5/5/5 on E/C/B but 1 on H (already pricing the terminal) is a *great business, bad entry* — exactly the trap the investor is trying to avoid.

---

## 5. Candidate landscape map *(scores + numbers populated from live research — see §5 table; deep dives refine)*

> *The two research agents are pulling the latest (post Q1-CY2026) TAM, supplier-share, and valuation data. The scored table and the per-segment bridges below are populated as that data lands. Placeholders marked ⟨DATA⟩ until then.*

### 5.1 Segment scorecard (to be filled)

| Segment | E | C | B | V | S | H | Old TAM → Terminal TAM | Key names | Priced-in verdict |
|---|---|---|---|---|---|---|---|---|---|
| HBM / advanced DRAM | | | | | | | ⟨DATA⟩ | SK Hynix, Micron, Samsung | ⟨DATA⟩ |
| Optical transceivers (800G/1.6T) | | | | | | | ⟨DATA⟩ | Innolight, Eoptolink, Coherent, Lumentum, 天孚 | ⟨DATA⟩ |
| InP / EML laser chips | | | | | | | ⟨DATA⟩ | Coherent, Lumentum, 源杰, POET | ⟨DATA⟩ |
| CPO (co-packaged optics) | | | | | | | ⟨DATA⟩ | Broadcom, Nvidia, optics ODMs | ⟨DATA⟩ |
| Custom ASIC / connectivity | | | | | | | ⟨DATA⟩ | Broadcom, Marvell, Astera | ⟨DATA⟩ |
| High-speed PCB / CCL / glass cloth | | | | | | | ⟨DATA⟩ | 沪电, 生益, Nittobo | ⟨DATA⟩ |
| ABF / IC substrate | | | | | | | ⟨DATA⟩ | Ibiden, Shinko, AT&S | ⟨DATA⟩ |
| Power (rack power / power semis) | | | | | | | ⟨DATA⟩ | Vertiv, MPS, Navitas, Eaton | ⟨DATA⟩ |
| Thermal / liquid cooling | | | | | | | ⟨DATA⟩ | Vertiv, 英维克, AVC, BOYD | ⟨DATA⟩ |
| Copper connectivity (NVLink) | | | | | | | ⟨DATA⟩ | Amphenol, 沃尔核材 | ⟨DATA⟩ |
| HBM/SoC test | | | | | | | ⟨DATA⟩ | Advantest, Teradyne | ⟨DATA⟩ |

---

## 6. Hypothesis bank — where consensus may be wrong *(to be tested in deep dives)*

These are the *a priori* "variant perception" candidates we will try to confirm or kill with data. Each is framed as a falsifiable claim:

1. **Optics elasticity is under-modeled.** The Street models transceiver *units* off port counts but under-weights the *triple-derivative* (modules/GPU × $/module × lasers/module). If 1.6T attach + scale-out radix rise together, transceiver TAM compounds faster than port-count models imply. *Test: build the per-GPU optics-$ ladder across GB200→GB300→Rubin.*
2. **CPO is a tail-risk, not a near-term displacement** — and even if it ramps, it *shifts* value toward InP/laser-engines, not away from the supply chain. Consensus may be over-discounting transceiver names on CPO fear while under-pricing the laser/InP chokepoint that CPO *needs more of*. *Test: CPO volume timeline vs. pluggable installed base; InP content in CPO vs pluggable.*
3. **InP / EML is the real chokepoint** — smallest base, hardest physics, longest lead time, fewest suppliers; demand stacks the most derivatives; yet it's buried inside larger optics names so the market can't size it. *Test: 200G/lane EML supply vs. 1.6T ramp; pure-play sizing.*
4. **HBM is being modeled as a memory cycle, not a logic-like content story.** If HBM4 customization (base-die on logic process) makes it more foundry-like / less commoditized, terminal margins and multiple are too low in consensus. *Test: HBM4 architecture, custom base-die, ASP premium durability.*
5. **Glass cloth / low-Dk specialty (Nittobo template) repeats in adjacent materials** — there may be other "tiny BOM line that gates a $40k server" inputs that haven't been found yet (specialty resins, copper foil, mask/quartz, specific test sockets). *Test: walk the AI-server BOM for sub-$X-bn TAM lines with oligopoly supply.*
6. **Power & cooling are re-rating off a "facilities" multiple toward a "semiconductor-content" multiple** as 1MW racks / 800V DC / liquid cooling become gating. The base is large (less S-score), but the *content-per-rack* step-change may be under-modeled. *Test: $/rack power+cooling content GB200 vs Rubin.*

---

## 7. Deep-dive sequencing & deliverables

Per investor priority (optical first, then memory, then CPO/InP, then adjacent chokepoints), the deep-dive memos will be produced in this order, each following the house template (business description → demand bridge → TAM endpoints → reverse "priced-in" test → per-company ceiling table → bear case → variant perception → data-quality caveats), mirroring the existing Nittobo memos:

1. `optical_transceivers_deepdive.md` — incl. Innolight, Eoptolink, Coherent, Lumentum, 天孚
2. `inp_cpo_deepdive.md` — the laser/InP chokepoint + CPO threat/tailwind analysis
3. `memory_hbm_deepdive.md` — SK Hynix, Micron, Samsung; cycle-vs-content debate
4. `chokepoints_screen.md` — ASIC/connectivity, PCB/CCL, substrate, power, cooling, copper, test — screened, top 2–3 promoted to full memos
5. `synthesis_priced_in_scorecard.md` — the cross-segment "what's priced in / ranked by upside-after-risk" master scorecard; critical-thinker bear review + reviewer citation audit applied.

---

*Status: methodology complete. Numbers populating from live research; §5 and §6 will be filled and this file re-committed once the data packs land.*
