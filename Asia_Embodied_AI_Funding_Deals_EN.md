# Embodied AI in Asia — A Deal-by-Deal Funding Review
### January 2024 – May 2026 · Transaction-level detail · China / Japan / Korea / Southeast Asia / India

> **What this report is**: A deal-by-deal review of the major financing and capital-markets events in Asia's embodied-AI / humanoid-robotics industry over the past two years (Jan 2024 – May 2026). It is a companion to the *Embodied AI Industry Landscape Report*. If you are new to the industry, read that one first; Section 1 below also gives a one-minute primer on "what this industry is."
>
> **Date**: 30 May 2026 ｜ **Language**: This is the English edition; a full Chinese edition exists (`亚洲具身智能融资交易盘点_CN.md`).
>
> **Sources**: Private-market funding cross-checked from public reporting (Caixin, 36Kr, Securities Times/STCN, QbitAI, PEdaily, PRNewswire, TechCrunch, The Robot Report, CNBC, Nikkei, KED Global, DealStreetAsia, etc.); listed-company market caps / financials from Financial Modeling Prep (FMP), as of 29–30 May 2026.
>
> **Important notice**: Chinese private-market amounts are often vague ("nearly RMB X00 million / several hundred million"), and valuations are typically media-cited and **unaudited**. This report strictly separates 【Confirmed】 from 【Rumored / Unconfirmed / Conflicting】 and lists contradictory figures side by side. **This is not investment advice.** Verify key numbers against company filings / HKEX / ITjuzi / PitchBook.

---

## Table of Contents

1. [One-minute primer: what is this industry](#s1)
2. [Methodology & data conventions](#s2)
3. [Overview: Asia's embodied-AI funding landscape & trends](#s3)
4. [China · Bodies / OEMs / Full-stack players](#s4)
5. [China · Embodied software / foundation models / data](#s5)
6. [China · Upstream core components](#s6)
7. [China · IPOs / reverse mergers / placements](#s7)
8. [Japan](#s8)
9. [Korea](#s9)
10. [Southeast Asia](#s10)
11. [India](#s11)
12. [Most active investors](#s12)
13. [Valuation leaderboard](#s13)
14. [Cross-region comparison & assessment](#s14)
15. [Risks & data caveats](#s15)
16. [Key sources](#s16)

---

<a name="s1"></a>
## 1. One-minute primer: what is this industry

- **Embodied AI** = giving AI a body that can perceive and physically act. The flagship product is the **humanoid robot** (a human-shaped machine that can walk and grasp). Unlike "talking-only AI" such as ChatGPT, it has to do **real physical work** in factories, warehouses and homes.
- **The value chain has four layers**: ① **upstream components** (reducers, motors, screws, sensors, dexterous hands, chips — the robot's "bones, muscles, nerves, hands and brain-hardware"); ② **mid-stream body/OEM makers** (who assemble components into a complete robot, like a car OEM); ③ **downstream applications** (auto plants → logistics → services → homes); ④ a **software layer** spanning the whole chain (VLA foundation models, simulation, data — the robot's "soul").
- **Why capital is flooding in during 2024–2026**: foundation models finally gave robots a general-purpose "brain"; China's EV supply chain is driving hardware costs down fast; and Tesla's Optimus, via Musk's gravitational pull, lit up the whole sector. The past two years are the **most funding-dense period in the industry's history**.

> Frequent terms: **body** = the robot's hardware platform; **full-stack** = building both the body and the in-house brain; **VLA** = Vision-Language-Action model (the robot's general brain); **CVC** = corporate venture capital; **lead investor** = the party putting in the most money and setting the price in a round; **Pre-IPO** = the last private round before listing; **reverse merger / backdoor listing** = a private company going public by acquiring an already-listed shell.

---

<a name="s2"></a>
## 2. Methodology & data conventions

- **Window**: Jan 2024 – May 2026. A few highly representative deals that strictly fall in H2 2025 – 2026 (e.g., SoftBank's ABB Robotics acquisition; Skild's $14B round) are included and flagged.
- **Scope**: equity financings of Asia-domiciled or Asia-capital-led embodied-AI / humanoid companies across **bodies, software/foundation models, and core components**, plus IPOs / reverse mergers / placements / strategic acquisitions. Asian capital investing in overseas targets (e.g., SoftBank into US-based Skild) is included and flagged.
- **FX**: converted at roughly USD 1 ≈ RMB 7.1–7.2 ≈ JPY 150 ≈ KRW 1,350, for order-of-magnitude only.
- **Confidence tiers**: 【Confirmed】 = multiple consistent sources + a clear round; 【Rumored/Unconfirmed】 = single-source or company-unconfirmed; 【Conflicting】 = sources disagree, listed side by side.
- **Known limits**: many Chinese financial sites block automated fetching (403), so amounts/valuations rely on cross-source summary consistency rather than field-level audit of originals.

---

<a name="s3"></a>
## 3. Overview: Asia's embodied-AI funding landscape & trends

**Key takeaways (this review + industry statistics):**

1. **China is the densest private market in Asia (and the world).** Industry stats: Chinese embodied-AI + robotics saw **~77 rounds / ~RMB 20.9B disclosed in 2024**, exploding to **160+ rounds / RMB 40B+ in 2025** (~+400% YoY). This review alone catalogues **60+ verifiable headline deals**.

2. **"Round inflation" is rampant.** Leading companies often raise 3–6 rounds in 12–18 months; angel rounds get sliced into "A++++++," and doubling valuations within six months is routine (e.g., Spirit AI crossed RMB 10B in 26 months; AI2Robotics claims 12 rounds in a year).

3. **From H2 2025, an "IPO harvest" began.** Hong Kong has produced four listings — RoboSense, Horizon Robotics, Dobot, Manycore; Unitree is racing to become the "first humanoid stock" on STAR Market; AgiBot opened an A-share back door by taking control of listed Shangwei New Materials.

4. **The rest of Asia follows very different paths**: **Korea** runs on chaebol control stakes (Samsung–Rainbow, LG–Bear, Hyundai–Boston Dynamics) plus government funds — the most systematic; **Japan** runs on SoftBank "buying the world" (ABB Robotics, $5.375B); **Southeast Asia / India** have weak native supply, dominated by conglomerate incubation (Vietnam's Vingroup) or industrial-capital control stakes (India's Reliance–Addverb).

**Asia embodied-AI funding "heat map" (qualitative, this review's scope):**

```
China    ██████████████████████████  Very hot (bodies + models + components, 60+ deals)
Korea    ████████                    Systematic (chaebol stakes + gov't fund)
Japan    ██████                      M&A-driven (SoftBank); small-to-mid local startups
India    ███                         Industrial-capital-led, early-stage VC
SE Asia  ██                          Weak native supply; China's go-global springboard
```

---

<a name="s4"></a>
## 4. China · Bodies / OEMs / Full-stack players

> Note: Galbot, AgiBot, Spirit AI, X Square, AI2Robotics, TARS, RobotEra, Galaxea AI are "full-stack" (building both the body and an in-house embodied foundation model). Because their valuations are driven by "model + body" together, they are listed here; **pure software/data companies** are in Section 5.

### 4.1 Deal table (chronological)

| Date | Company (CN / EN) | Round | Amount (local / ≈USD) | Post-money valuation | Lead | Notable co-investors | Business in one line |
|---|---|---|---|---|---|---|---|
| 2024-04→09 | 智元 AgiBot | Series A set (A++++→A++++++) | >RMB 600M cumulative | >RMB 7.0B | Sequoia China et al. | BYD, Hillhouse, CDH, BAIC, SAIC, Baidu Ventures | General humanoid (Yuanzheng/Lingxi) + GO-1 model, full-stack |
| 2024-08 | 千寻 Spirit AI | Seed + Angel | ~RMB 200M / ≈$28M | — | Highlight Capital | Fortune, Qiancheng, Shunwei, Oasis | End-to-end VLA model + wheeled/humanoid body (Moz1) |
| 2024-08 | 星海图 Galaxea AI | Pre-A | >RMB 200M | — | Hillhouse, Ant Group | — | End-to-end embodied model + body (Tsinghua roots) |
| 2024-12-25 | 魔法原子 MagicLab (Dreame) | Angel | RMB 150M / ≈$21M | — | Dreame Ventures | Yipu Fund | Dreame-incubated industrial/commercial humanoid |
| 2025-01-07 | 傅利叶 Fourier | Series E | ~RMB 800M / ≈$110M | E3 pre-money RMB 8.0B | Guoxin, Pudong VC, Zhangjiang | Prosperity7 (Aramco), Junshan | Rehab-exoskeleton origins, pivoted to humanoid (GR series) |
| 2025-01-07 | 智平方 AI2Robotics | Pre-A (strategic) | Several hundred M RMB | — | Dachen, Dunhong | Cornerstone | "Most Tesla-like" full-stack embodied AI |
| 2025-02 | 灵宝 CASBOT | Angel | >RMB 100M | — | — | Lenovo Capital, SDIC, Henan Asset | General humanoid (CASBOT 01/02) |
| 2025-03-24 | 智元 AgiBot | Series B | undisclosed | **RMB 15.0B** | Tencent (first embodied bet) | Longcheer, Wolong, Huafa, Lanchi, TCL, Huajin | same |
| 2025-03-26 | 它石智航 TARS | Angel | **$120M** / ≈RMB 870M | — | Lanchi, Qiming | — | Self-driving team (Chen Yilun/Li Zhenyu) → embodied; record angel |
| 2025-03 | 千寻 Spirit AI | Pre-A | RMB 528M / ≈$74M | — | Prosperity7 (Aramco) | CMB Int'l, GF Xinde, Genbridge, Eastern Bell, Huakong | same |
| 2025-05 | 智元 AgiBot | Series B+ | undisclosed | >RMB 15.0B | JD.com, Shanghai Embodied AI Fund | existing investors | same |
| 2025-06 | 宇树 Unitree | Series C | ~RMB 700M / ≈$97M | pre RMB 12.0B, **post ~RMB 12.7B** | China Mobile, Tencent, Jinqiu, Alibaba, Ant, Geely Capital (6 co-leads) | many existing | Global quadruped leader + humanoid (G1/H1/H2) |
| 2025-06 | 银河通用 Galbot | New round | >RMB 1.1B / ≈$155M | already a unicorn | CATL (Contemporary Amperex / Puquan) | CDB, Beijing Robotics Fund, GGV | GraspVLA grasping model + wheeled humanoid (PKU Wang He team) |
| 2025-07 | 智元 AgiBot | Strategic | — | — | LG Electronics, Mirae Asset, CP Robotics | — | same |
| 2025-07 | 众擎 EngineAI | Pre-A++ & A1 | ~RMB 980M / ≈$140M | — | A1: JD.com; Pre-A++: XPeng's Xinghang | CATL Puquan, Yintai, Huakong, Dachen | Full-size humanoid (SE01/PM01) |
| 2025-07 | 千寻 Spirit AI | Pre-A+ | ~RMB 600M / ≈$83M | — | JD.com | CIC, Zhejiang fund, Huatai Zijin, Fosun Ruizheng | same |
| 2025-09 | 自变量 X Square | Series A+ | ~RMB 1.0B / ≈$140M | — | Alibaba Cloud (first embodied bet) | Sequoia China, Meituan, Legend Star, Junlian | General embodied model WALL-A (Megvii roots) |
| 2025-10-22 | 乐聚 Leju | Pre-IPO | ~RMB 1.5B / ≈$208M | — | Shenzhen Capital, Longhua, Qianhai (co-lead) | Eastern Gold, Tuopu, CITIC, Hefei Industry | Humanoid (Kuavo), racing to IPO |
| 2025-10-26 | 松延动力 Songyan | Pre-B | ~RMB 300M / ≈$42M | — | Fangguang Capital | — | Humanoid (N2 / Hobbs) |
| 2025-11 | 星动纪元 RobotEra | Series A+ | ~RMB 1.0B / ≈$140M | ~RMB 10B | Geely Capital | BAIC, Alibaba, Lenovo Capital | Full-stack humanoid (STAR1) |
| 2025-11-26 | 松延动力 Songyan | Pre-B+ | ~RMB 200M / ≈$28M | — | CICC Capital | Yuntai, Houwei (5th raise in a month) | same |
| 2025-12-19 | 银河通用 Galbot | New round | >$300M / ≈RMB 2.1B | **$3.0B (sector-high)** | China Mobile chain fund | CICC, CAS fund, Suzhou VC, CCTV media fund, Tianqi | ~$800M cumulative |
| 2026-01 | 自变量 X Square | Series A++ | RMB 1.0B / ≈$140M | — | ByteDance, Sequoia China | Beijing Info Industry Fund | >RMB 3.0B cumulative in 2 yrs; biggest 2026-opening embodied deal |
| 2026-02-02 | 逐际动力 LimX | Series B | **$200M** / ≈RMB 1.45B | — | mix of domestic/foreign | UAE Lei Shi, Eastern Bell, Cornerstone, JD strategic | Legged + full-size humanoid (TRON1/CL) |
| 2026-02-23/24 | 智平方 AI2Robotics | Series B set (5 rounds) | >RMB 1.0B / ≈$140M | **>RMB 10B** | Baidu Ventures, CRRC Capital | Yusys, Sentury, Yunbai, Guotai Haitong | claims 12 rounds in a year |
| 2026-02 | 千寻 Spirit AI | New round | ~RMB 2.0B / ≈$280M | **>RMB 10B** | (Jack Ma / Lei Jun-linked, reported) | — | RMB 3.0B in 30 days; >RMB 10B in 26 months |
| 2026-02 | 星海图 Galaxea AI | Series B | ~RMB 1.0B | RMB 10B | — | — | same |
| 2026-03-06 | 帕西尼 PaXini | Series B | >RMB 1.0B / ≈$140M | **>RMB 10B** | Huangpujiang, Kaitai, SDIC Xin'an | — | Tactile sensing + dexterous hand + humanoid (TORA-ONE) |
| 2026-03 | 魔法原子 MagicLab | Series A | RMB 500M / ≈$70M | post ~RMB 3.5B | Tiankong Factory VC | Tuopu, Jinyu, Asd | same |
| 2026-03 | 银河通用 Galbot | New round (reported) | RMB 2.5B / ≈$350M | reported >RMB 20B | National AI Industry Investment Fund ("Big Fund") | Sinopec, CITIC, BOC Asset, SAIC, SMIC fund | same |
| 2026-04 | 星海图 Galaxea AI | Series B+ | ~RMB 2.0B | **RMB 20B** | Hua Capital, Lens Tech et al. | CICC, Hongtai, Pohua, GF Qianhe | ~RMB 5.0B cumulative |
| 2026-04-09 | 开普勒 Kepler | Series A++ | RMB 100M-class | — | SAIF Partners | Nolly, Civil Explosive | same |
| 2026-04-16 | 它石智航 TARS | Pre-A | **$455M** / ≈RMB 3.2B | — | Hillhouse, Sequoia China | Meituan, CICC, Kailian, Eastern Bell, Junshan | one of the year's largest single rounds |

### 4.2 Company snapshots

- **Galbot**: three rounds in-window (Jun-25 >RMB 1.1B / Dec-25 >$300M at $3.0B / Mar-26 RMB 2.5B, reportedly >RMB 20B). **Top-tier on both valuation and cumulative funding in Chinese embodied AI.**
- **AgiBot**: Series A set (>RMB 7B) + B (Tencent, RMB 15B) + B+ (JD) + strategic (LG / Mirae / CP). **The most star-studded industrial cap table**; later went A-share via Shangwei (Section 7).
- **Unitree**: Series C (Jun-25, post ~RMB 12.7B), six co-leads; **racing to a STAR Market IPO** (Section 7).
- **Spirit AI**: **the most prolific fundraiser** (Seed→Pre-A→Pre-A+→~RMB 2B in 2026); >RMB 10B in 26 months.
- **TARS**: $120M angel (record) → $455M Pre-A (record single round).
- **X Square**: A (Meituan) → A+ (Alibaba Cloud) → A++ (ByteDance/Sequoia); >RMB 3B cumulative.

---

<a name="s5"></a>
## 5. China · Embodied software / foundation models / data

| Date | Company (CN / EN) | Round | Amount / ≈USD | Valuation | Lead | Co-investors | Business |
|---|---|---|---|---|---|---|---|
| 2024-2025 | 穹彻 Noematrix | Angel→Pre-A++ | several hundred M cumulative | — | Sequoia, Prosperity7 | Shengyu, Cingo, Joy, Yunqi, SHTI | Force-aware embodied model (SJTU/Stanford roots) |
| 2025-10 | 穹彻 Noematrix | New round | several hundred M | — | Alibaba | — | same |
| 2025-07 | 跨维 DexForce | A1 & A2 | several hundred M | — | Chengdu VC, Hongtai | Lenovo Capital, Tianying | Sim2Real synthetic data + embodied brain |
| 2025-11 | 光轮 Lightwheel | A & A+ | several hundred M | — | Eastern Bell, Jiupai | 37 Interactive, Amber, Chentao | Embodied synthetic-data infra (clients incl. NVIDIA/Figure) |
| 2026-03 | 光轮 Lightwheel | A++ & A+++ | RMB 1.0B | "global embodied-data unicorn" | New Hope Group, AUX | Jiantou Huake, Guofang | revenue +10x in 2025 |
| 2026-05 | 光轮 Lightwheel | New round | undisclosed | — | Ant Group | Jiantou, GBA fund, Linxin | same |
| 2024-11 | 灵初 Psi Robot | Angel | — | — | Hillhouse, Lanchi | — | RL + dexterous manipulation (PKU roots) |
| 2026-03 | 灵初 Psi Robot | Angel+Pre-A cumulative | **~RMB 2.0B** | up 6–7x in a year | Shanghai Xuhui Capital et al. | CDB Finance, Guozhong, CCTV fund, SDIC | logistics at scale |
| 2025-05 | 有鹿 Yulu | Angel | >RMB 100M | — | Baidu Ventures, Sinovation, Yuanjing | — | General embodied brain (outdoor cleaning) |
| 2025-03→2026-05 | 维他动力 Vbot | Seed→Pre-A | ~RMB 700M cumulative | — | Jinri / Eastern Jiafu, Huatai Zijin, Fosun | SAIC Shangqi, Cathay, Hillhouse | Consumer robot; began humanoid R&D |
| 2025-03 | 原力灵机 Dexmal | Angel | RMB 200M | — | Junlian, Ubiquant, Qiming | — | Megvii "genius" team (Fan Haoqiang) |
| 2025-09→11 | 原力灵机 Dexmal | A / A+ | ~RMB 1.0B (two rounds) | — | A: NIO Capital; A+: Alibaba (sole) | Hongtai, Lenovo Capital | same |

> **Highlights**: **data/simulation** has become a standalone track (Lightwheel, DexForce); **Alibaba** is aggressively buying into the software layer (Noematrix, Dexmal, X Square); the **RL route** (Psi) saw valuation up 6–7x in a year.

---

<a name="s6"></a>
## 6. China · Upstream core components

| Date | Company (CN / EN) | Round | Amount / ≈USD | Valuation | Lead | Co-investors | Business |
|---|---|---|---|---|---|---|---|
| 2025-04 | 因时 Inspire | B3 | ~RMB 100M | — | Shenqi Capital | Yuanhe, Huagai | Micro servo-cylinders + dexterous hands (>10k delivered in 2025) |
| 2025 H1 | 因时 Inspire | C1 & C2 | several hundred M | — | C1: China Mobile fund + Shenzhen Capital; C2: Beijing AI fund | Boyuan, Dachen, Chunhua, Qiming, TCL | same |
| 2025-09 | 强脑 BrainCo | Strategic | Daoshi RMB 213M | ~RMB 8.5B (2024) | Daoshi Technology | — | Non-invasive BCI + bionic hands ("Hangzhou 6 Little Dragons") |
| 2026-01 | 强脑 BrainCo | Pre-IPO/new | RMB 2.0B (reported) | post >$1.3B (~RMB 9.4B) | IDG, H Capital | Lens, Huazhu, Luxshare-ICT, TAL | listing guidance started |
| 2025-04 | 灵心巧手 Linkerhand | Seed | >RMB 100M | — | Sequoia Seed, Wankai | Lihe, Huacang | High-DoF dexterous hands (CloudMinds roots) |
| 2025-08 | 灵心巧手 Linkerhand | Angel | several hundred M | — | Ant Group | CICC, Defa, Sequoia Seed | mass-produced 1,000s |
| 2025 H2 | 灵心巧手 Linkerhand | A+ | several hundred M | — | — | Zhejiang VC, Leju, CDH, AUX | same |
| 2025-06→08 | 帕西尼 PaXini | Series A set | RMB 1.0B in 4 months | — | JD strategic | Puyao, Hongzhao, Newland, TCL, SenseTime | Multi-dim tactile sensors + humanoid (also Series B in §4) |
| 2025-07 | 蓝点触控 Link-touch | B | ~RMB 100M | — | four-party | GF Xinde, Fosun, Hefei VC, Huacang | 6-axis force sensors (>70% China share 2024) |
| 2025-11 | 蓝点触控 Link-touch | C | >RMB 100M | — | Sequoia China | Zhuhai Tech Group | same |
| 2026-04 | 蓝点触控 Link-touch | C+ | >RMB 100M | — | CATL (Puquan), AgiBot, Galbot (industrial) | Opt, Galaxy | same |
| 2025-02 | 坤维 KunWei | B | RMB 100M-class | — | — | Xiaomi, Sunny, Shenzhen Capital, Hillhouse | 6-axis force sensors (~30% cheaper than ATI) |
| 2025-06 | 本末 BenMo | B & B+ | several hundred M | — | Beijing Advanced Mfg Fund | Beijing Materials Fund, Shunxi, Legend Star | Direct-drive motors / joint modules |
| 2025 H2 | 灵足时代 Lingzu | Pre-A & Pre-A+ | tens of M, two rounds | — | Pre-A: Sequoia Seed; Pre-A+: Highlight | Xingniu, Innoangel, Yiwei | Joint modules/motors (Q3'25 shipments +500%) |

> **Highlights**: **dexterous hands + 6-axis force sensors + tactile** are the most capital-dense component niches; **industrial capital is investing upstream** (CATL, AgiBot, Galbot, JD, Xiaomi all backing component suppliers to lock supply).

---

<a name="s7"></a>
## 7. China · IPOs / reverse mergers / placements

| Date | Company | Event | Amount | Valuation/Mkt cap |
|---|---|---|---|---|
| 2024-01-05 | RoboSense (2498.HK) | HK IPO (first of 2024) | ~HK$985M (HK$43/sh) | IPO mkt cap ~HK$19.3B |
| 2024-10-24 | Horizon Robotics (9660.HK) | HK IPO (one of year's biggest tech) | **HK$5.41B** | pre-IPO $8.71B; day-1 ~HK$69B |
| 2024-12-23 | Dobot (2432.HK) | HK IPO (China's first cobot stock) | ~HK$720M | top-2 global cobot shipments |
| 2024-08→2025-11 | UBTech (9880.HK) | **6 placements in a year** | **>HK$7.0B cumulative** (e.g., HK$0.91B/2.47B/3.11B) | refinancing ~7x its IPO raise |
| 2025-07→11 | AgiBot → Shangwei (688585) | Share transfer + partial tender, **control stake** | ~RMB 2.1B (RMB 7.78/sh) | ~63.6%–67% stake; Deng Taihua becomes controller; target +10x in year |
| 2025-10-15 | AgiBot → Shangwei | Filing: no reverse-merger plan in 36 months (**denies backdoor**) | — | — |
| 2025-06 | Unitree | Series C (last pre-IPO) | ~RMB 694M | pre RMB 12B / post RMB 12.7B |
| 2026-03-20 | Unitree | **STAR Market IPO accepted** | raise **RMB 4.20B** | listing mkt cap ~RMB 42B; 2025 revenue RMB 1.71B (+335%), net profit RMB 600M, **profitable** |
| 2026-04-17 | Manycore (2367.HK) | HK IPO ("first spatial-intelligence stock") | ~HK$1.22B; retail 1,591x oversubscribed | day-1 +160%, ~HK$35B |
| 2025-12 | Dobot | Announced plan for Shenzhen A-share (dual listing) | — | >100k units deployed |
| (in prep) | BrainCo / Xinjian / Fourier / Leju / MagicLab | listing guidance / prep | — | — |

> **Rumor flags**: AgiBot also rumored to plan an HK IPO before Q3 2026 (target HK$40–50B) — **officially denied**; Unitree's "RMB 100B/200B" talk is investor cheerleading.

---

<a name="s8"></a>
## 8. Japan

| Date | Company | Type | Amount | Valuation | Parties | Business |
|---|---|---|---|---|---|---|
| 2025-10-08 | SoftBank acquires ABB Robotics | Acquisition (whole unit) | **$5.375B** | ABB Robotics ~$2.3B 2024 revenue | SoftBank (buyer) / ABB (seller) | SoftBank buys ABB's "Robotics & Discrete Automation"; Physical-AI thesis; pending regulators |
| 2025-01-28 | SoftBank → Skild AI (US) | Strategic lead | ~$500M | ~$4.0B | SoftBank | General robot "brain"; Asian capital into overseas target |
| 2026-01 ⚠️ | Skild AI (US) | Mega-round | **$1.4B** | **>$14B** | SoftBank lead, NVIDIA participates | ~3x valuation jump |
| 2025-12-02 | Mujin | Series D (first close) | **$233M** | $411M cumulative | NTT Group lead, Qatar's QIA co-lead | Industrial automation OS (MujinOS) |
| 2024-10/11 | GITAI (HQ moved to US) | Series B ext. | $15.5M (ext. total $60.5M) | ~$83M cumulative | Maezawa Fund | Space robotics / on-orbit servicing |
| 2025-09-30 | Telexistence × 7-Eleven | Strategic (non-funding) | undisclosed | — | Seven-Eleven Japan | Co-develop GenAI humanoid "Astra" |
| 2024-10-16 | Toyota TRI × Boston Dynamics | R&D partnership (non-funding) | — | — | TRI + Boston Dynamics | Train Atlas with Large Behavior Models |

> **Japan takeaway**: high activity, but heavily concentrated in **SoftBank's** "overseas investment + big M&A" (ABB Robotics, Skild, AutoStore, Agile Robots, Berkshire Grey). Local startups (Mujin, GITAI, Telexistence) are small-to-mid and skew industrial/logistics/space. Telexistence's last big round was its 2023-07 $170M Series B; no new round in-window.

---

<a name="s9"></a>
## 9. Korea

| Date | Company | Type | Amount | Valuation/Stake | Parties | Business |
|---|---|---|---|---|---|---|
| 2024-12-30 | Samsung raises Rainbow Robotics (277810.KQ) | Strategic/control (option exercise) | **KRW 267B ≈ $181.6M** | stake 14.7%→**35%** (top shareholder) | Samsung Electronics | Cobot/humanoid; created "Future Robotics Office" |
| 2024-03 / 2025-01 | LG acquires Bear Robotics (US/KR) | Two-step control buyout | $60M initial → option exercise | **51% control**, consolidated | LG Electronics | Delivery service robots, into LG CLoi |
| 2025-04-10 | K-Humanoid Alliance (gov't) | Gov't fund / consortium | ~**$770M** by 2030 (KRW 1T) | — | MOTIE + 40+ orgs | Build robot AI foundation model by 2028 |
| 2025-08 (CES2026) | Hyundai Mobis × Boston Dynamics | Strategic (actuator supply) | undisclosed | — | Hyundai Mobis + Boston Dynamics | Supply actuators for next-gen Atlas |
| 2025+ | Hyundai buys Boston Dynamics robots | Strategic procurement / capex | US: $6B framework; KR to 2030 ~$86.7B | — | Hyundai Motor Group | Buy "tens of thousands"; 30k/yr robot plant |
| 2026-05 ⚠️ | WIRobotics | Series B | **KRW 95B ≈ $68M** | (Series A 2024-03, KRW 13B) | (NVIDIA Physical AI Fellowship) | Humanoid platform ALLEX + exoskeleton |
| 2025-07 | AeiROBOT | Series A | $7.2M (cumulative ~$9.7M) | — | (GTC 2025 NVIDIA award) | Humanoid robot |
| 2023-10 (context) | Doosan Robotics (KOSPI IPO) | IPO | ~$318M | valuation >$2B | public market | Cobots; 2025 pivoting to "practical humanoid" |

> **Korea takeaway**: **the most systematic** — three chaebols enter via "control + consolidation" (Samsung–Rainbow 35%, LG–Bear 51%, Hyundai–Boston Dynamics), plus the K-Humanoid government fund ($770M). Rainbow Robotics is KOSDAQ-listed; its secondary-market cap reached ~$10B on the Samsung halo.

---

<a name="s10"></a>
## 10. Southeast Asia

| Date | Company | Country | Type | Amount | Parties | Business |
|---|---|---|---|---|---|---|
| 2026-03-10 ⚠️ | AgiBot × Singtel | CN×SG | Strategic (non-equity) | undisclosed | AgiBot + Singtel Enterprise | AgiBot embodied AI on Singtel's network; leasing in Singapore |
| 2025-01 | VinMotion (Vingroup) | Vietnam | Incorporation / capitalization | reg. capital ~$39M | Vingroup (with VinAI/VinFast) | Vietnam's first general humanoid developer |
| ongoing | Fourier | SG (hub) + Malaysia | Regional deployment / research | — | parent in Shanghai, China | SG regional HQ; research with Tan Tock Seng Hospital |
| 2024-2025 | Weston Robot | Singapore | Angel (no large round) | undisclosed | Lion City Angel | RaaS; showcased G1 humanoid |
| 2025 | Temasek / GIC / EDBI | Singapore | Indirect allocation | not separately disclosed | sovereign funds | Robotics/AI via global portfolios (**no confirmed single direct embodied bet**) |

> **SE Asia takeaway**: **weakest native supply**; the main story is **Chinese firms using it as a go-global springboard** (AgiBot×Singtel; Fourier's SG hub) and **Vietnam's Vingroup incubating VinMotion in-house**. Sovereign-fund single direct bets into embodied AI could not be verified deal-by-deal.

---

<a name="s11"></a>
## 11. India

| Date | Company | Type | Amount | Valuation/Stake | Lead/Parties | Business |
|---|---|---|---|---|---|---|
| 2024 | Reliance acquires Addverb | Control buyout | **$132M** | **54%** stake, post ~$270M | Reliance Retail Ventures | Warehouse automation → humanoid + defense; 60k/yr plant in Noida |
| 2025-01-22 | Ati Motors | Series B | **$20M** | ~$37M cumulative | Walden Catalyst, NGP Capital | Industrial AMR "Sherpa"; humanoid-inspired version 2025 |
| (recent) | CynLr | Series A | **$10M** | $15.2M cumulative | Pavestone, Athera | Machine vision + object manipulation |
| — | Svaya Robotics | Unfunded | no external funding | — | self-funded / DRDO | Cobots + general humanoid, DRDO collaboration |

> **India takeaway**: **industrial-capital-led**, with Reliance–Addverb ($132M/54%) the landmark; the rest are early/mid VC. Most start from industrial/warehouse AMRs; humanoids are still prototypes. India robotics VC was ~$117M in 2024 (vs ~$54M in 2023) — fast growth, small absolute base.

---

<a name="s12"></a>
## 12. Most active investors

**Internet/tech giants (CVC):**
- **Alibaba group (Alibaba/Alibaba Cloud/Ant)**: Unitree, X Square (A+), RobotEra, Noematrix, Dexmal (A+), Galaxea, Linkerhand — **most aggressive in the software layer**.
- **JD.com**: AgiBot (B+), Spirit AI (Pre-A+), EngineAI (A1), LimX, PaXini, Kepler (indirect).
- **Tencent**: AgiBot (B, first embodied bet), Unitree.
- **Meituan / Longzhu**: X Square (A), Galaxea (A4/A5), TARS.
- **ByteDance**: X Square (A++). **Baidu**: AI2Robotics (B), Yulu, Dexmal (indirect).

**Automakers / industrial capital**: Geely Capital (Unitree, RobotEra), BAIC (AgiBot, RobotEra, PaXini), SAIC (AgiBot, Galbot), BYD (AgiBot, PaXini), XPeng's Xinghang (EngineAI), **CATL / Puquan** (Galbot, EngineAI, Spirit AI, Link-touch), Tuopu (Leju, MagicLab).

**National team / chain funds**: **China Mobile chain fund** (Galbot, Inspire, Unitree), **National AI Industry Investment Fund ("Big Fund")** (Galbot), Shanghai Embodied AI Fund (AgiBot), Yizhuang SOE.

**Top financial VCs**: Sequoia China (all stages), Hillhouse (AgiBot, TARS, Psi, KunWei), Lanchi (TARS, Psi), Qiming (TARS, Dexmal), Shenzhen Capital, Dachen, Eastern Bell, Hongtai, Junlian, Lightspeed.

**Middle-East / overseas sovereign**: Prosperity7 (Saudi Aramco — Fourier, Spirit AI, Noematrix), Lei Shi Capital (UAE — LimX), Qatar QIA (Japan's Mujin), Infini Capital (UBTech).

> **In one line**: **JD and Alibaba are the most active corporate investors; China Mobile's chain fund and the National AI "Big Fund" are the most active "national-team" leads; Sequoia/Hillhouse have the broadest coverage; Middle-East sovereign capital keeps adding to leaders.**

---

<a name="s13"></a>
## 13. Valuation leaderboard (media-cited, unaudited)

**Private-market (unlisted) valuation ranking:**

| Rank | Company | Valuation | Timing | Status |
|---|---|---|---|---|
| 1 | Galbot | $3.0B (~RMB 21.3B); reportedly >RMB 20B after Mar-26 | Dec-25 / Mar-26 | $3.0B confirmed; >RMB 20B reported |
| 2 | Galaxea AI | RMB 20B | Apr-26 (B+) | reported |
| 3 | AgiBot | RMB 15B | Mar-25 (B) | confirmed |
| 4 | Spirit AI / AI2Robotics / PaXini | each ">RMB 10B" | early 2026 | reported |
| 5 | Unitree | post ~RMB 12.7B (IPO mkt cap ~RMB 42B) | Jun-25 / Mar-26 | confirmed |
| — | BrainCo | >$1.3B (~RMB 9.4B) | Jan-26 | reported |

**Public-market (listed) market caps (FMP, 29–30 May 2026):**

| Company | Code | Mkt cap (≈USD) |
|---|---|---|
| Rainbow Robotics (KR, Samsung-backed) | 277810.KQ | ~$10B |
| Horizon Robotics | 9660.HK | ~$8.5B |
| UBTech | 9880.HK | ~$5.6B |
| RoboSense | 2498.HK | ~$1.9B |

> **Caveat**: private valuations are **media-cited and unaudited**, and "round inflation" hurts comparability; public caps swing sharply on sentiment (UBTech 52-wk range HK$73.5→161). **Valuations already price in heavy future humanoid-volume expectations.**

---

<a name="s14"></a>
## 14. Cross-region comparison & assessment

**Activity ranking (systematization + deal scale): China >> Korea ≈ Japan > India > SE Asia (native).**

| Dimension | China | Japan | Korea | SE Asia | India |
|---|---|---|---|---|---|
| Main driver | Local-gov't guidance funds + internet/industrial giants + abundant VC | SoftBank "buy the world" M&A | 3 chaebols' control stakes + gov't fund | China's springboard + conglomerate incubation | Industrial-capital control + early VC |
| Signature deal | Galbot $3B; AgiBot→Shangwei; Unitree STAR IPO | SoftBank buys ABB Robotics $5.375B | Samsung → 35% of Rainbow | AgiBot×Singtel; VinMotion | Reliance buys Addverb |
| Target profile | Dense local OEM unicorns | Industrial/logistics/space | Chaebol control of overseas/local | Sparse native | Warehouse AMR → humanoid |
| Gov't role | Very strong | Mostly private capital | Strong (K-Humanoid) | Weak | Weak |

**Core assessment**:
1. **China is the undisputed home market** — dense funding across bodies, software and components; the most local OEM unicorns by count and valuation density — but also the highest round-inflation / valuation-bubble risk.
2. **Korea is the most systematic** — chaebol vertical integration + government fund, suited to M&A logic.
3. **Japan is "picks-and-shovels + capital going abroad"** — it controls the precision-component chokepoint at home (see the companion industry report) while SoftBank buys US/EU assets.
4. **SE Asia / India are incremental edge markets** — SE Asia as a springboard, India led by industrial capital (Reliance); absolute amounts remain small.

---

<a name="s15"></a>
## 15. Risks & data caveats

1. **Amounts/valuations are largely unaudited**: Chinese private "nearly RMB X00M" is vague; Galbot's RMB 20B, and the >RMB 10B tags for Spirit/AI2Robotics/Galaxea, are mainly media reports — verify against filings/ITjuzi/PitchBook.
2. **Round inflation**: angels sliced into "A++++++"; six-month doublings are common; comparability is poor.
3. **Conflicts listed side by side**: e.g., AgiBot→Shangwei stake 63.6% vs 67% (staged-deal lower/upper bound); Galbot's Dec round shown as "$300M/RMB 2.1B + $3.0B/RMB 20B" from different sources for the same round.
4. **Rumored items**: AgiBot HK IPO (officially denied); Unitree's "RMB 100B" talk; a single-source $242M TARS interim round (to verify); Telexistence down-round rumor (unconfirmed); 1X's $10B round (not closed).
5. **Out-of-window deals**: SoftBank-ABB, Skild $14B, WIRobotics Series B, AgiBot×Singtel partly fall in H2 2025–2026 (flagged ⚠️).
6. **UBTech placement figures are muddled**: single vs cumulative vs net proceeds vary across reports — defer to HKEX 9880 filings.

---

<a name="s16"></a>
## 16. Key sources

**China bodies/models**: Caixin, STCN, 36Kr, QbitAI, PEdaily, Sina Finance, Southern Metropolis (oeeee), Guancha, Wallstreetcn; company sites.
- Galbot: Caixin https://m.caixin.com/m/2025-12-19/102394886.html ; PEdaily https://news.pedaily.cn/202603/561274.shtml
- AgiBot Series B: oeeee https://m.mp.oeeee.com/a/BAAFRD0000202503241062442.html
- Unitree C/IPO: STCN https://www.stcn.com/article/detail/3735182.html ; SSE https://www.sse.com.cn/listing/renewal/ipo/
- TARS: TMTPost https://www.tmtpost.com/7954674.html
- Galaxea B+: STCN https://www.stcn.com/article/detail/3722732.html
- Lightwheel: BJD https://news.bjd.com.cn/2026/05/29/11773323.shtml

**China IPO/reverse merger**:
- AgiBot→Shangwei: STCN https://stcn.com/article/detail/2479539.html ; ThePaper (denies backdoor) https://m.thepaper.cn/newsDetail_forward_31142812
- Horizon IPO: Yicai https://www.yicai.com/news/102316876.html
- Dobot IPO: Futu https://www.futuhk.com/blog/detail-dobot-ipo-100-241206006
- Manycore IPO: HKEXnews https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0409/2026040900026_c.pdf
- UBTech placements: Sina https://finance.sina.com.cn/stock/bxjj/2025-11-25/doc-infyqiwh5876848.shtml

**Japan/Korea/SE Asia/India**:
- SoftBank–ABB: SoftBank PR https://group.softbank/en/news/press/20251008 ; CNBC https://www.cnbc.com/2025/10/08/softbank-to-buy-abb-robotics-unit-for-5point4-billion-in-ai-push.html
- SoftBank→Skild: TechCrunch https://techcrunch.com/2025/01/28/softbank-to-invest-500m-in-robotics-startup-skildai/ ; Businesswire https://www.businesswire.com/news/home/20260114335623/en/
- Mujin: https://mujin-corp.com/press-releases/mujin-raises-233-million-...
- Samsung–Rainbow: Samsung PR https://news.samsung.com/global/samsung-electronics-to-become-largest-shareholder-in-rainbow-robotics... ; KED https://www.kedglobal.com/robotics/newsView/ked202412310001
- LG–Bear: LG PR https://www.lgnewsroom.com/2025/01/lg-acquires-majority-stake-in-bear-robotics...
- K-Humanoid: Korea.net https://www.korea.net/NewsFocus/Sci-Tech/view?articleId=269677
- AgiBot×Singtel: PRNewswire https://www.prnewswire.com/apac/news-releases/agibot-signs-strategic-cooperation-agreement-with-singtel-enterprise-302708995.html
- Reliance–Addverb: https://addverb.com/press-release/reliance-acquires-54-stake-in-addverb-technologies-for-132-million/
- Ati Motors: TechCrunch https://techcrunch.com/2025/01/22/ati-motors-raises-20m-as-indias-robotics-industry-grows/

**Financial/market-cap data**: Financial Modeling Prep (FMP), as of 29–30 May 2026.

---

> **Disclaimer**: This AI-assisted report compiles public information for research reference only and **does not constitute investment advice or an offer**. Private-market amounts and valuations are largely media-reported and unaudited, with conventions that differ and remain uncertain. Any investment decision should rest on independent due diligence and professional advice.
>
> **End of English edition** ｜ Chinese edition: `亚洲具身智能融资交易盘点_CN.md`
