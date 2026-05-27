# AI Server BOM Walk — Hidden "Nittobo-Template" Chokepoint Screen
*Author: senior buy-side analyst*
*As of 26 May 2026. Companion to `ai_supply_chain_framework.md` (tests Hypothesis #5). Covers the GB200/GB300 NVL72 + Rubin rack BOM, line by line, hunting for the under-the-radar chokepoints — the "tiny BOM line that gates a $40k+ server."*

---

## 0. What we were looking for, and the one finding that matters

We walked the AI-rack BOM across two layers — (A) materials & advanced-packaging, (B) discrete components & back-end equipment — looking for repeats of the **Nittobo template**: a *tiny* absolute TAM, supplied by a *monopoly/oligopoly*, that *gates* the whole server, with demonstrable *pricing power*. We added a fifth, decisive screen the framework underweights: **investability as a clean pure-play.**

**The single most important conclusion:** there is an **"investability gap."** The *truest* monopolies in the AI BOM — Ajinomoto's ABF film (约95%), AGC/Hoya EUV mask blanks (约93%), Resonac's MR-MUF underfill — are **buried inside giant diversified companies where the chokepoint is <5% of group revenue.** Their scarcity rent is real but **does not move the parent stock.** Owning them is *not* how you express the BOM-walk thesis.

Conversely, a *small* number of chokepoints are **both structurally tight AND cleanly listed as near-pure-plays.** That intersection is where the BOM walk actually pays. The screen produces essentially **three** of them — **probe cards (FormFactor / Technoprobe), die-to-wafer hybrid bonding (BESI), and — as the diversified-but-earnings-driven basket — Resonac.** Everything else is either un-investable, a margin-mix tailwind on a mega-cap, an eroding monopoly, or commoditizing.

---

## 1. Master scorecard (all candidates, both layers)

Scored 1–5: **T** = TAM-tininess (5 = sub-$1bn), **M** = monopoly/oligopoly concentration, **G** = gating/criticality, **P** = pricing-power evidence (lead-times, price hikes, margins), **I** = investability as a clean listed pure-play. **The investor's filter rewards high T·M·G·P *and* high I** — a 5/5/5/5 chokepoint with I=1 is real but un-ownable.

| # | Chokepoint | Best listed name | T | M | G | P | **I** | Verdict |
|---|---|---|:-:|:-:|:-:|:-:|:-:|---|
| 1 | **Probe cards** (HBM/2nm wafer test) | FormFactor `FORM` 约$10.5bn; Technoprobe `TPRO.MI` 约$12bn | 4 | 4 | 5 | 4 | **5** | ★ **TRUE & ownable — top pick of the walk** |
| 2 | **D2W hybrid bonding** (next-gen HBM/logic stacking) | BESI `BESI.AS` (hybrid-bond 约⅓ of co by '26) | 4 | 4 | 4 | 4 | **3** | ★ **TRUE forward chokepoint — owns the *next* node** |
| 3 | **AI back-end materials basket** (MR-MUF + EMC + films) | Resonac `4004.T` 约$19bn (segment >30% sales, +74% profit Q1'26) | 4 | 4 | 4 | 4 | **3** | ★ **Best diversified way to own several at once** |
| 4 | **ABF build-up film** | Ajinomoto `2802.T` 约$23bn (film <5% of group) | 5 | 5 | 5 | 5 | **2** | TRUE archetype, but *buried in a food co* + consensus |
| 5 | **EUV mask blanks** | AGC `5201.T` / Hoya `7741.T` (each <5% of group) | 5 | 5 | 5 | 4 | **1** | TRUE 93% duopoly — *un-investable cleanly* |
| 6 | **HVLP5 copper foil** | Mitsui Kinzoku `5706.T` 约$3.5bn (foil 约10–15%, smelting drag) | 4 | 5 | 4 | 4 | **3** | TRUE at top grade; equity diluted by smelting |
| 7 | **High-cap MLCC** (≥10µF small-case) | Murata `6981.T`; Samsung EM `009150.KS` | 2 | 4 | 4 | 5 | **2** | TRUE squeeze (price +15–35% Apr'26) — *not tiny, not pure-play* |
| 8 | **HBM MR-MUF underfill** | Resonac/Namics `4004.T` | 5 | 4 | 5 | 3 | **2** | TRUE material monopoly — *exclusivity reportedly expiring* |
| 9 | **EUV pellicle** | Mitsui Chemicals `4183.T` 约$6bn | 5 | 4 | 4 | 4 | **2** | TRUE 70–80% oligopoly — buried in commodity chem |
| 10 | **CoWoS EMC / back-end films** | Sumitomo Bakelite `4203.T`; Resonac | 3 | 3 | 4 | 4 | **3** | Partial → true on specific sub-lines |
| 11 | **224G connectors / NVLink twinax** | Amphenol `APH` 约$100bn+ | 2 | 4 | 5 | 4 | **2** | Real sole-source yield-gate — *but not tiny, mega-cap* |
| 12 | **Vertical power delivery (VPD)** | Vicor `VICR` 约$14bn | 4 | 3 | 5 | 3 | **4** | "Gating *if* it wins Rubin socket" — binary optionality |
| 13 | **Low-loss resin (PPE/BMI)** | Mitsubishi Gas Chem `4182.T` 约$4bn | 3 | 3 | 4 | 4 | **2** | Pricing power via tight supply, *not* monopoly |
| 14 | **Optical micro-optics / isolators** | Tianfu `300394.SZ` 约$38bn | 3 | 3 | 4 | 3 | **2** | Tight (isolators) but proxy is a crowded large-cap |
| 15 | **Test/burn-in sockets** | ISC `095340.KQ`; Leeno `058470.KQ` | 4 | 3 | 4 | 2 | **3** | Small & gating but too fragmented |
| 16 | **HBM TC bonder** | Hanmi `042700.KQ` 约$25bn | 4 | 3↓ | 4 | 3 | **4** | ⚠ **Monopoly BREAKING (71%→20–30% SKH '26)** |
| 17 | **MPO/MTP connectors** | US Conec (private) | 4 | 4 | 4 | 2 | **1** | Near-mono on IP — *private, un-investable* |
| 18 | **Quick disconnects (UQD)** | Stäubli/CPC (private/buried) | 4 | 4 | 4 | 3 | **1** | Qualification moat — no clean listed pure-play |
| 19 | **Ceramic ferrules** | (Kyocera/Tianfu/三环) | 5 | 2 | 3 | 1 | 2 | ✗ Commoditizing — value migrated to micro-optics |
| 20 | **CMP slurry/pads, sputtering targets, quartz crucibles, TIM** | (various) | 3 | 2 | 2 | 2 | 2 | ✗ Too fragmented / multi-sourced / not rack-gating |

*Caveats: market-research-mill TAMs (Valuates/QYResearch/OpenPR) are directional only and several conflate "ABF film" with "ABF substrate." High-conviction structural facts (Hanmi share, Amphenol sole-source, Murata price hikes, BESI D2W lead, Ajinomoto 约95%) cross-check to TrendForce/DigiTimes/Bloomberg/company IR. Market caps are May-2026 indicative — verify on a terminal. "% of group" figures marked elsewhere as [EST].*

---

## 2. The shortlist — where the BOM walk actually pays

### 2.1 ⭐ Probe cards — FormFactor (FORM) / Technoprobe (TPRO.MI) — *the top finding*
- **Why it's the best:** the *only* candidate that clears all five screens, including investability. 约$4–5bn TAM (2026), top-3 ≈ 60% share, MEMS-tip IP moat, bespoke-per-device + consumable (recurring), and **rising structurally with HBM stack KGD test + chiplet/2.5D test intensity.** Technoprobe won 约30% of TSMC 2nm quals.
- **The variant perception:** the market models probe cards as *cyclical WFE/test capex*. But test *intensity* (test-seconds per advanced die, KGD requirements for HBM stacking) is a **content story that rises every node regardless of unit cyclicality** — more like a consumable razor-blade than a capex tool. If that re-rates from "cyclical equipment multiple" to "consumable-content multiple," there's multiple expansion on top of volume.
- **Risk:** Technoprobe/FormFactor compete; not a true monopoly. Memory-test cyclicality still bleeds through.
- → **Promote to a full deep-dive memo.**

### 2.2 ⭐ BESI (BESI.AS) — die-to-wafer hybrid bonding
- **Why:** the *forward* gate. As HBM4 → HBM4E and logic move from micro-bump TCB to copper-to-copper hybrid bonding, BESI leads D2W (<10nm placement, next-gen 约50nm in 2026), partnered with Applied Materials. Hybrid-bond revenue €36m (2023) → 约€476m (2026E), 约⅓ of the company — small base, exploding, and a cleaner equity than the diversified materials names.
- **The edge vs. Hanmi:** don't own the *incumbent* TCB monopoly (Hanmi, eroding — see §3); own the *next-node* share-gainer.
- **Risk:** ASMPT #2 and ASML reportedly eyeing entry; hybrid bonding still a minority of BESI today, so timing/ramp is the swing.
- → **Promote to deep-dive (paired with the HBM memo's packaging section).**

### 2.3 ⭐ Resonac (4004.T) — the diversified back-end-materials basket
- **Why:** the only name where the AI back-end-materials chokepoints are *actually the earnings engine* (semis & electronic materials >30% of sales, segment profit +74% YoY Q1'26), spanning MR-MUF underfill (SK Hynix HBM), EMC, and back-end films where Resonac is #1 in several niches. You get *several* tiny monopolies in one investable wrapper — solving the §0 "investability gap."
- **Risk:** still a diversified chemicals co; petrochemical/graphite-electrode cyclicality dilutes; MR-MUF exclusivity reportedly expiring.

### 2.4 Watch / second-tier (true chokepoint, but flawed expression)
- **High-cap MLCC (Murata 6981.T):** strongest *pricing-power* evidence in the entire walk — lead times 8→40 weeks, utilization >80%, **explicit 15–35% price hikes effective 1-Apr-2026.** But it's a margin/mix tailwind on a diversified large-cap, not a tiny pure-play. Own it for the *earnings revision*, not for a 10x-base story.
- **Mitsui Kinzoku HVLP5 foil (5706.T):** 约80% of the top grade, sold-out, guidance raised on it — but base-metal smelting dilutes the equity. A "chokepoint with a cyclical anchor strapped to it."
- **Vicor (VICR):** the truest "gating-*if*-it-wins" line — Rubin's 2,000A+ at <1V cannot be delivered laterally, and Vicor holds key VPD IP (+ Kyocera Power-on-Package). But the socket is *contested* (MPS/ADI/Infineon), so it's binary optionality already priced for a partial win. Highest beta in the walk.

---

## 3. The trap list — "chokepoints" that fail on closer inspection

| Trap | Why it fails |
|---|---|
| **Hanmi Semiconductor (HBM TC bonder)** | The textbook HBM monopoly (约71%) is **actively breaking in 2026** — ASMPT took 约half of SK Hynix HBM4 TCB sets; Micron going BESI sole-source; Hanmi–Hanwha patent fight; SK Hynix share may fall to 20–30%. **Owning the eroding incumbent is the wrong trade; own the share-gainer (BESI/ASMPT).** A live example of "monopoly decay" risk. |
| **The buried monopolies** (ABF film/Ajinomoto, mask blanks/AGC-Hoya, pellicle/Mitsui Chem, MR-MUF/Resonac at <5% of group) | Real scarcity rent, but <5% of a giant diversified parent → **the chokepoint doesn't move the stock.** Right insight, wrong instrument. |
| **Amphenol 224G / NVLink copper** | Genuine sole-source, yield-gated technical chokepoint — but TAM is *not* tiny and the proxy is a 约$100bn+ diversified mega-cap. Plus copper is a **bridge** technology (physics reach-limit pushes scale-up to optics over time). |
| **Ceramic ferrules, CMP slurry, sputtering targets, quartz crucibles, TIM** | Either commoditizing/multi-sourced (ferrules, CMP, targets, TIM) or upstream-of-wafers not rack-gating (quartz crucibles). Fail the "1–3 suppliers AND the $40k server doesn't ship" test. |
| **MPO/MTP connectors (US Conec), quick-disconnects (Stäubli/CPC)** | Genuine IP/qualification moats — but **private / un-investable as pure-plays.** |

---

## 4. How this feeds the master thesis

- **Confirms Hypothesis #5** (`ai_supply_chain_framework.md` §6): the Nittobo template *does* repeat — but the actionable payoff is narrower than the long list of "true chokepoints" suggests, because of the **investability gap.**
- **Adds three names to the deep-dive pipeline that were not on the original §5.3 list:** FormFactor / Technoprobe (probe cards), BESI (hybrid bonding), Resonac (back-end materials basket). Probe cards in particular is arguably a *cleaner* expression of the investor's "high-elasticity × chokepoint × small-base × ownable" filter than several of the original headline sectors.
- **Adds a transferable risk lens — "monopoly decay":** Hanmi shows that an AI-supply-chain monopoly can be competed away faster than the multiple assumes. Every chokepoint long must be underwritten against *who could take share by 2027* — this becomes a standing question for the critical-thinker pass on every name.

### Proposed deep-dive additions
1. `probe_cards_deepdive.md` — FormFactor + Technoprobe; test-intensity-as-content thesis; cyclical-vs-consumable re-rating.
2. Fold **BESI** into the HBM/packaging deep-dive (the TCB→hybrid-bonding transition + Hanmi share-decay).
3. **Resonac** as a stand-alone "back-end materials basket" note if the investor wants a lower-beta, diversified expression.

---

*Status: BOM walk complete; tests framework Hypothesis #5. Awaiting investor steer on whether to fold probe cards / BESI / Resonac into the deep-dive queue alongside the original InP-EML → optical → HBM → Nittobo sequence. Data-quality caveats per §1.*
