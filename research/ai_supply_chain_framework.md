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

## 5. Candidate landscape map *(populated from live research, 26-May-2026 data packs; deep dives will refine each)*

### 5.1 Segment scorecard

Scores 1–5 per §4 rubric (E=elasticity, C=criticality, B=bottleneck, V=visibility, S=small-base/headroom-to-grow, H=valuation-headroom-after-rerating). **Total /30.** The investor's target zone is the top-left of "high E·B·S still with workable H" — *not* simply the highest total (a 27-total name with H=2 is a great business at a bad price).

| Segment | E | C | B | V | S | H | **Tot** | Terminal-TAM trajectory | Key names | One-line priced-in verdict |
|---|:-:|:-:|:-:|:-:|:-:|:-:|:-:|---|---|---|
| **InP / EML laser chips** | 5 | 5 | 5 | 5 | 4 | 3 | **27** | ~$1–2bn → multi-$bn; gates the entire 1.6T ramp | COHR, LITE (owned InP); 源杰, POET (pure-play) | *Truest chokepoint; market can't size it cleanly because it's buried in larger optics names. Best risk/reward in the chain.* |
| **Low-Dk glass cloth** (Nittobo template) | 5 | 5 | 5 | 4 | 4 | 3 | **26** | tiny → ¥30bn+ specialty sub-line; cap tripling but lags demand | Nittobo (3110.T) | *Already re-rated hard; the question is whether sold-out duration + ASP holds into 2027. See existing Nittobo memos.* |
| **HBM / advanced DRAM** | 4 | 5 | 5 | 4 | 2 | 4 | **24** | $38bn(25)→$58bn(26E)→~$80bn+ | SK Hynix, Micron, Samsung | *Priced as a CYCLE (NTM P/E ~6–12x), not as content/logic-like. If HBM4 custom base-die de-commoditizes margin, multiple too low. Big base caps the x, but cheap entry.* |
| **ABF / IC substrate** | 3 | 5 | 5 | 4 | 3 | 3 | **23** | $4.9bn(24)→$9.6bn(32) — only ~2x | Ibiden, Shinko, AT&S, Unimicron | *True oligopoly (5 players=74%), long capex lead — but modest TAM elasticity (~2x/8yr). Chokepoint without the explosive growth.* |
| **Optical transceivers (800G/1.6T)** | 5 | 5 | 3 | 3 | 3 | 3 | **22** | $16.5bn(25)→$26bn(26E,+60%) | Innolight, Eoptolink, COHR, LITE, 天孚 | *Elasticity real (units×speed×$); but competitive + CPO-2028 overhang + crowded (Eoptolink lost $10bn cap in a day on CPO fear). Eoptolink cheapest (~22x).* |
| **High-end ATE / test** | 4 | 4 | 5 | 4 | 2 | 3 | **22** | rising test-time/die | Advantest (6857.T), Teradyne | *Advantest/Teradyne duopoly, structural pricing power — but already re-rated, large base. Solid not explosive.* |
| **Custom ASIC / connectivity** | 4 | 5 | 5 | 4 | 1 | 2 | **21** | hyperscaler XPU TAM rising fast | AVGO, MRVL, ALAB | *True duopoly (AVGO/MRVL) + IP/packaging lock-in — but $2T/$172bn/$53bn base + 37x/51x/105x multiples = great business, expensive entry. Fails the small-base/headroom filter.* |
| **CPO (co-packaged optics)** | 4 | 3 | 4 | 2 | 5 | 2 | **20** | $46mn(24)→>$5bn(27E)→$8.1bn(30E, Yole) | NVDA, AVGO (embedded); optics ODMs | *Optionality/RISK lens, not a clean long — can't isolate it as a pure play, and timing is 2027 (LC) vs 2028–30 (Yole). Matters most as a threat to read for transceivers.* |
| **Power (800VDC / 1MW rack)** | 4 | 4 | 3 | 4 | 2 | 3 | **20** | rack power 100kW→1MW+; new vector | Vertiv, MPWR, ETN, Navitas | *Genuine new secular vector (800VDC H2-2026). VRT system-advantaged; power semis more competitive. Large base limits x.* |
| **High-speed PCB / CCL** | 4 | 4 | 3 | 3 | 3 | 3 | **20** | rising layer-count/area + spec | 沪电(002463), 生益(600183) | *Competitive at board level; the real chokepoint sits UPSTREAM in glass cloth. 沪电 advantaged in AI high-layer-count but contestable.* |
| **Thermal / liquid cooling** | 4 | 4 | 2 | 3 | 3 | 3 | **19** | ~¥800bn server liquid-cooling by 26 | VRT, 英维克, AVC, BOYD | *COMMODITIZING at module level — 英维克 NI −82% YoY despite +26% rev is the tell. Only CDU/system-integration (VRT) defensible. Avoid cold-plate module makers.* |
| **Copper connectivity (NVLink)** | 3 | 4 | 3 | 2 | 2 | 3 | **17** | NVL72 all-copper intra-rack | APH, 沃尔核材 | *Real but a BRIDGE chokepoint — physics reach-limit pushes to optics at scale-up over time. APH advantaged but large base.* |

### 5.2 Valuation anchors (indicative, May-2026; refresh on a terminal before modeling)

| Name | Ticker | Mkt cap | Latest growth print | NTM/fwd P/E | Note |
|---|---|---:|---|---:|---|
| SK Hynix | 000660.KS | ~$940bn [EST FX] | record Q1'26 profit; sold out to 2027 | **~6×** | Overtook Samsung mkt cap ~14 May |
| Micron | MU | ~$850bn | Q2 FY26 rev $23.9bn (+196% YoY) | **~11–12×** | HBM sold out thru 2026 |
| Innolight 中际旭创 | 300308.SZ | ~CNY 860bn | Q1'26 rev ¥19.5bn (+192%), NI +262% | ~43x (26E) | Scale leader, premium |
| Eoptolink 新易盛 | 300502.SZ | ~CNY 388bn | Q1'26 rev ¥8.34bn (+106%), GM ~49% | **~22–23x (26E)** | Cheapest high-grower; crowded |
| 天孚通信 | 300394.SZ | large-cap | Q1'26 NI +45.8% | ~56x (26E) | Picks-and-shovels, CPO-agnostic |
| Coherent | COHR | ~$56bn | FQ3'26 rev $1.81bn (+21%); booked to 2028 | ~mid-20s | **Owns 6" InP** — the moat |
| Lumentum | LITE | ~$70bn+ | FQ3'26 +85% guide | ~high-30s | **Only volume 200G EML shipper today** |
| 源杰科技 Yuanjie | 688498.SH | ~CNY 300–350bn | CW 70mW in volume; 200G EML in qual | rich | China laser-chip substitution play; A+H pursuit |
| Broadcom | AVGO | ~$1.96T | Q1 FY26 AI rev $8.4bn (+106%) | ~37x | Custom XPU duopoly |
| Marvell | MRVL | ~$172bn | AI XPU/custom ASIC | ~51x | — |
| Astera Labs | ALAB | ~$53bn | PCIe/CXL connectivity | ~105x | Richest = most thesis risk |
| Advantest | 6857.T | mega-cap | FY26 guide +26% rev | — | HBM/SoC test duopoly |
| Vertiv | VRT | ~$113bn | 800VDC portfolio H2-2026 | — | NVIDIA reference-design partner |
| Amphenol | APH | large-cap | Q1'26 rev $7.6bn | ~34x | NVLink copper |

*China NTM P/E figures are sell-side targets from Feb–Mar 2026 and predate Q1 prints; COHR/LITE/VRT/MPWR caps were not tick-accurate in-sandbox. Verify on a terminal.*

### 5.3 Where the deep dives should focus (ranked by fit to the investor's filter)

The investor wants **high-elasticity × chokepoint × small-base × workable valuation** — explicitly tolerant of a small absolute TAM. Ranking the screen on that *specific* fit (not raw total):

1. **InP / EML laser chips — HIGHEST CONVICTION.** Stacks the most demand derivatives (GPU units × optics/GPU × lasers/module × $/laser), truest sold-out chokepoint (lead times past 2027), and — critically — *the market cannot price it cleanly* because it's embedded inside COHR/LITE or sits in early pure-plays (源杰, POET). This is the closest thing to "a chokepoint the consensus literally cannot size." **Deep dive first.**
2. **Optical transceivers (esp. Eoptolink) — HIGH-BETA EXPRESSION.** The cleanest, most liquid way to play optics elasticity; the debate is entirely *CPO-displacement timing* and *crowding*, both of which we can frame. Eoptolink at ~22x is the asymmetry candidate.
3. **HBM, contrarian-multiple angle.** Not small-base, but the *variant perception* is sharp: the Street prices it as a memory cycle (~6–12x) while the demand is increasingly inference-underwritten and HBM4 is going custom/logic-like. If the multiple re-rates from "cycle" to "content," that's the upside — different shape from the others (re-rating, not 10x-base-growth).
4. **Low-Dk glass cloth (Nittobo)** — already have base/bear memos; refresh the sold-out-duration and Nan-Ya-dilution questions.
5. **Watch-but-not-yet:** ABF substrate & Advantest (true chokepoints, modest elasticity/base); AVGO/MRVL (great businesses, bad entry); CPO (read as a *risk input* to #2, not a standalone long).
6. **Avoid as primaries:** liquid-cooling modules (commoditizing), copper (bridge), generic PCB/CCL (chokepoint is upstream).

### 5.4 BOM-walk discoveries (tests Hypothesis #5 — see `bom_walk_chokepoints.md`)

We walked the GB200/GB300/Rubin rack BOM line-by-line for *under-the-radar* Nittobo-template chokepoints, adding a decisive 5th screen the headline sectors pass too easily: **investability as a clean pure-play.** The key finding is an **"investability gap"**: the *truest* monopolies (Ajinomoto ABF film ~95%, AGC/Hoya EUV mask blanks ~93%, Resonac MR-MUF) are **buried <5% inside giant diversified parents — their scarcity rent doesn't move the stock.** Only a handful are *both* structurally tight *and* cleanly listed:

| New name surfaced | Chokepoint | Why it clears the filter | Status |
|---|---|---|---|
| **FormFactor (FORM) / Technoprobe (TPRO.MI)** | Probe cards (HBM/2nm wafer test) | Only candidate clearing all 5 screens incl. investability; ~$4–5bn TAM, top-3 ~60%, consumable + rising test-intensity; **market mis-models it as cyclical capex vs. consumable content** | ★ promote to deep-dive |
| **BESI (BESI.AS)** | D2W hybrid bonding | Forward gate (TCB→hybrid bonding for HBM4E/logic); <10nm placement lead, ~⅓ of co by '26; own the *next-node share-gainer* not the eroding incumbent | ★ fold into HBM/packaging dive |
| **Resonac (4004.T)** | Back-end materials basket (MR-MUF + EMC + films) | Only name where AI back-end materials are the *actual earnings engine* (>30% sales, +74% seg. profit Q1'26); solves the investability gap | watch / optional note |

**Two transferable lessons for every name:** (1) the *buried-monopoly* trap — right insight, wrong instrument (ABF film, mask blanks, pellicle); (2) **"monopoly decay"** — Hanmi's HBM TC-bonder share is collapsing 71%→20–30% (2026) as ASMPT/BESI take share, so *every* chokepoint long must be underwritten against "who takes share by 2027." This becomes a standing question for the critical-thinker pass.

---

## 6. Hypothesis bank — where consensus may be wrong *(to be tested in deep dives)*

Falsifiable "variant perception" claims, now sharpened with the data packs. Ranked by conviction:

1. **InP / EML is THE chokepoint the market can't size — and that's the edge.** Smallest base, hardest physics (low-yield InP wafers, long cycle), longest lead time (NVDA pre-buying EML, lead times past 2027), fewest suppliers (LITE = *only* volume 200G EML shipper today; COHR ramping 6" InP). Demand stacks the most derivatives (units × optics/GPU × lasers/module × $/laser). Yet it's buried inside COHR/LITE or in qual-stage pure-plays (源杰), so there's no clean comp and the Street under-prices the scarcity rent. *Test: 200G/lane EML supply curve vs. 1.6T ramp; isolate InP-attributable earnings inside COHR/LITE; size 源杰/POET ceiling.*
2. **"CPO kills transceivers" is the wrong frame for 2026–27 — and it actually *increases* demand for the InP chokepoint.** CPO first attacks switch-to-switch scale-up (where pluggables are weakest), not the ~1-port/GPU scale-out NIC links; pluggables stay the majority "throughout the decade" and 800G+ still triples 2025→2030 *even with* CPO. And CPO still needs external CW/EML lasers + SiPh engines → it *shifts* value toward InP/laser-engines, not away from the chain. Consensus over-discounts transceiver names on CPO fear (Eoptolink −$10bn cap in a day) while under-pricing the laser input CPO needs *more* of. *Test: Spectrum-X Photonics 2026 ship rate (the leading indicator); InP content per CPO port vs per pluggable.*
3. **HBM is priced as a memory CYCLE (~6–12x P/E), not as a logic-like CONTENT story.** Demand is increasingly inference-underwritten (durable) not just training-lumpy; HBM4 base-die moves to a logic process / customization → more foundry-like, stickier margins; 1 HBM4 wafer eats ~3 DRAM wafers and AI takes ~20% of DRAM capacity in 2026, structurally tightening *commodity* DRAM too. If the multiple re-rates from "cycle" to "content," that's the upside — and the second-order DDR5/NAND squeeze (+58–75% QoQ 2Q26) is a cleaner, less-crowded way to play it. *Test: HBM4 custom base-die economics; ASP-premium durability; DRAM-as-AI-derivative price elasticity.*
4. **Optics elasticity is under-modeled because it's multiplicative, not additive.** The Street models transceiver *units* off port counts (~1/GPU, stable) but under-weights the *speed×price* ladder (400G→800G→1.6T raises $/port even at flat attach) AND the latent **scale-up optics** unlock (today copper/NVLink; optics may migrate in at Rubin-era). The bigger TAM lever is scale-up migration, not scale-out attach creep. *Test: build the per-GPU optics-$ ladder GB200→GB300→Rubin incl. a scale-up-optics scenario.*
5. **The Nittobo glass-cloth template likely repeats in other "tiny BOM line that gates a $40k server" inputs.** Candidates to walk the BOM for: specialty low-loss resins, ultra-low-profile copper foil, photomask/quartz, specific high-speed test sockets/probe cards. *Test: AI-server BOM walk for sub-$2bn-TAM lines with 1–3 suppliers and sold-out status.*
6. **Power/cooling are NOT uniform.** Power (800VDC/1MW rack) is a genuine new content vector with a system-integration chokepoint (VRT), but liquid-cooling *modules* are already commoditizing (英维克 NI −82% YoY on +26% rev). The market may be lumping them together; the spread (long VRT/power-content vs. fade cold-plate module makers) is the trade. *Test: $/rack power+cooling content GB200→Rubin, split by defensible vs. commoditizing layers.*

---

## 6b. 写作标准 — 所有 memo 必须遵守(WRITING STANDARD — applies to every memo)

**这是一条强制标准,所有深挖 memo 都要 fully reflect。** 读者是**没有任何行业背景的投资委员会(IC)成员**,不是行业专家。要求:

1. **中文为主**,专业名词第一次出现时附英文原词,并立刻用**大白话 + 类比**解释清楚"它是什么、为什么重要"。例:不能直接写"先进 die 的 wafer starts",要写成"晶圆(wafer,一整块圆形硅片,上面一次印出几百上千颗芯片)的产量"。
2. **像讲故事一样讲逻辑**:这东西到底做什么 → 难在哪 → 为什么是卡脖子 → 护城河为什么持久。不能靠堆砌术语显得专业。
3. **每篇开头一句话**用最朴实的比喻把这门生意讲清楚;**文末附术语速查表**。
4. 句子要通顺,杜绝中英夹杂导致语义不清。宁可啰嗦讲明白,不要简洁但看不懂。
5. 严谨性(TAM、priced-in 逆推、ceiling 表、bear case、变量假设)一个都不能少——只是把它们**讲人话**。

*探针卡 memo(`probe_cards_deepdive.md`)是符合本标准的范本。*

## 7. Deep-dive sequencing & deliverables

Per investor priority (optical first, then memory, then CPO/InP, then adjacent chokepoints), the deep-dive memos will be produced in this order, each following the house template (business description → demand bridge → TAM endpoints → reverse "priced-in" test → per-company ceiling table → bear case → variant perception → data-quality caveats), mirroring the existing Nittobo memos:

1. `optical_transceivers_deepdive.md` — incl. Innolight, Eoptolink, Coherent, Lumentum, 天孚
2. `inp_cpo_deepdive.md` — the laser/InP chokepoint + CPO threat/tailwind analysis
3. `memory_hbm_deepdive.md` — SK Hynix, Micron, Samsung; cycle-vs-content debate
4. `chokepoints_screen.md` — ASIC/connectivity, PCB/CCL, substrate, power, cooling, copper, test — screened, top 2–3 promoted to full memos
5. `synthesis_priced_in_scorecard.md` — the cross-segment "what's priced in / ranked by upside-after-risk" master scorecard; critical-thinker bear review + reviewer citation audit applied.

---

*Status: framework complete and populated with 26-May-2026 data packs (§5 scorecard, §5.2 valuation anchors, §6 hypothesis bank). Awaiting investor sign-off on the §5.3 focus ranking before launching the four deep-dive memos. All figures carry the data-quality caveats noted inline and in §5.2.*
