# Logisteed Pre-IPO 投资 — Downside Protection / Preferred 替代结构 Brainstorm 与可行性分析

**主题:** 我们作为 financial sponsor 在 KKR 旗下 Logisteed（原 Hitachi Transport System，日立物流）的 Pre-IPO 一轮投进去，如何在"价格被 Japan Post 的 12.5x 锚死"的前提下，拿到 downside protection / minimum return，且不被东京交易所（TSE）以"IPO 前 cap table 里有优先股"为由 challenge。

**日期:** 2026-06-16　|　**性质:** 内部 brainstorm / negotiation prep。下文区分（a）已 verify 的事实，（b）口径存疑/单一来源的数据，（c）我方判断。所有需要日本 counsel 出正式意见的点在第 7 节单列。

---

## 0. TL;DR（一页纸结论）

1. **"日本交易所不喜欢 IPO 前 cap table 里有优先股"——这个说法 substantially true，但不是 TSE 的明文硬规则。** 真正的约束是两层叠加：(i) **主承销商（主幹事証券会社）几乎一定会要求 IPO 前把所有优先股通过取得条項强制转成普通股**；(ii) **会社法的硬约束**（财源规制 Art. 461 + 股东平等 Art. 109）让公司层面根本无法合法地给某个股东保底或现金回购。所以与其说"交易所禁止"，不如说"上市主体（issuer）层面的优先权在上市那一刻必须干净地消失"。

2. **这恰恰给了我们设计方向。** 任何 downside protection 只要满足三条红线就能与 IPO 共存：
   - **红线 1 — obligor 不是上市主体（issuer），而是 KKR 的 sponsor/基金/控股 SPV；**
   - **红线 2 — 不与上市后二级市场股价直接挂钩（no post-listing price link）；**
   - **红线 3 — 可披露、不是暗箱（避开日本 tobashi/簿外 的违法红线）。**
   满足这三条的结构（典型是 **sponsor-level 回购/补足保证 + structured secondary**）在 HK 已有成熟先例（HKEX GL43-12 框架下"survive-IPO 的 return guarantee"），日本没有明文禁止、但需要 counsel 确认 FIEA 披露口径。

3. **在动结构之前，先把"fairness"这个前提 reframe——我方有三个被低估的议价支点：**
   - **Japan Post 是 strategic、我们是 financial：** Japan Post 这 19.9% 是**带 capital & business alliance**（车辆/站点共享、客户交叉销售）进来的，它付的价里含**协同溢价**；我们作为纯财务投资者拿不到这些协同，凭什么付一样的价？"same price = fair" 是 apples-to-oranges。
   - **Japan Post 这笔是 secondary，卖方就是 KKR：** 2025 年 10 月 Japan Post 是从 **KKR 手里买**的老股（¥142.3bn / 19.9%），所以 KKR 说"不能让你比 Japan Post 便宜"本质是在维护**它自己的 realization 标价**——这是 self-serving，不是中立的公平。
   - **从 ¥670bn（2023 KKR 收购）到 ¥715bn（2025 Japan Post）只涨了 ~7%（2.5 年）：** 这个极小的 step-up 本身说明市场/战略方都不愿为 Logisteed 付大溢价，反过来削弱"12.5x 是地板价"的叙事。再叠加 **12.5x 是 "pre-IFRS cash EBITDA"** 口径（分母偏小→倍数显高），换算到可比的 IFRS-16 口径可能只有 ~9–10x，**与日本同业 6–10x 的差距被会计口径放大了**。坚持 like-for-like 口径，是把名义 12.5x 谈下来的"软"路径。

4. **可落地度排序（详见第 5 节）：**
   - **① Sponsor-level put / make-whole（"fund/SPV 层面保底"）+ structured secondary（递延/或有对价）** —— 最干净、最贴合你提的"fund level guarantee"，但 KKR 大概率不肯用整支基金 guarantee（cross-collateralization 伤 LP），更现实是从 deal SPV 或以 deferred purchase price 形式给。
   - **② Co-investment side letter（合规版"抽屉协议"）：KKR 以 IPO 后按约定价向我方转让/收购股份来补到 min MOIC/IRR。** 关键是**必须可披露**，绝不能做成日本式 tobashi。
   - **③ 进入价格机制：名义 12.5x 进，但用 valuation true-up / anti-embarrassment（以 IPO 定价回看调整 effective entry price，差额在 sponsor 层面结算）。**
   - **④ 退一步的"软"保护：用 IFRS 口径 reframe 把有效倍数谈低 + 谈 governance/info/lock-up 协调权。**

---

## 1. 事实底座（先把 background 钉准，几处与初始 framing 有出入）

| 项目 | 事实 | 来源/状态 |
|---|---|---|
| KKR 收购 | 2022 年宣布、2023 年 2–3 月完成对日立物流（HTS, 9086）的 take-private，要约价 ¥8,913/股（约 166% 溢价于 12 个月均价），equity value 约 **¥670bn（~$5.2bn）**；日立 Ltd 回滚约 **10%** 投票权，KKR 持约 90% | Bloomberg / BusinessWire / AVCJ（已 verify） |
| 更名 | 2023 年 4 月更名 **LOGISTEED** | 多源确认 |
| Japan Post 入股 | **2025 年 10 月**，Japan Post 以 **¥142.3bn 收购 19.9%**（从 KKR 手里买的 **secondary**，附 capital & business alliance），隐含 **equity value ~¥715bn** | Nikkei / Mingtiandi / Simpson Thacher（已 verify 价格与比例） |
| "12.5x Pre-IFRS cash EBITDA" | **公开来源未独立验证**；各方只披露价格与比例，未披露 EBITDA 或倍数。注意 ¥715bn 报的是 **equity value 不是 EV**，所以 12.5x 到底套在哪个分母/分子上需向 deal 材料确认 | **(b) 口径存疑——见 §1.1** |
| IPO 计划 | KKR 已聘 **Morgan Stanley** 筹备 **TSE 上市，最早 2027**；有评论认为 Japan Post 这笔反而可能让 near-term float 复杂化 | Private Equity Wire / The Loadstar |
| 财务 | 9M（截至 2024/12）收入 **¥669bn**、净利 **¥28bn**；年化收入约 ¥850–890bn，经营利润率 mid-single-digit；按 IFRS 报表 | TI-Insight（press 级数据） |
| 业务结构 | 约 **55% 国内 3PL/合同物流 + ~42% global/forwarding**；forwarding 在 2021–22 受运价周期拉动，之后回归常态（"peak EBITDA"风险） | HTS IR / TI-Insight |

### 1.1 "12.5x pre-IFRS cash EBITDA" 这个口径必须先夯实——它直接决定"fairness"论点的强弱

- **Pre-IFRS cash EBITDA** = 把租赁当作经营费用（扣掉现金租金）的 EBITDA，即 IFRS 16 资本化**之前**的口径（也叫 EBITDAR-adjusted / frozen-GAAP / cash EBITDA）。它**小于** IFRS-16 报表 EBITDA。
- 3PL 仓库/车队租赁体量大，两口径差异**很大**（可达 2–4 个 turn）。用**偏小的 pre-IFRS 分母**算出来的倍数会**显得高**：12.5x pre-IFRS cash EBITDA ≈ IFRS-16 口径下的约 **9–10x**（示意）。
- 而我们拿来对比的"日本同业 6–10x、全球十几倍、forwarder ~20x"，多数 screen 是不同租赁口径混着的。**EV 与 EBITDA 必须同口径**（pre-IFRS 下租赁负债不进 net debt/EV；post-IFRS 下要进）——混用是这类比较里最常见、也最致命的错误。
- **结论（议价用）：** 在统一到 IFRS-16 可比口径后，Logisteed 相对日本同业的"溢价"可能被显著压缩。**第一步不是谈结构，而是先要 deal team / counsel 把 12.5x 的精确口径（哪个 EBITDA、EV 还是 equity、含不含租赁）摊开**，很可能"12.5x 听起来很贵"本身就有水分。

### 1.2 同业估值（已 verify，区间略收紧）

- **日本上市物流同业 EV/EBITDA（LTM, 近似）：** NX/日本通运 ~6.0–6.2x、SG Holdings(佐川) ~7.5x、Senko ~7.6x、Yamato ~9.7x。→ 用户说的"4–9x"**大体成立，但实际更像 6–10x，没看到当前有 4x 的样本**。
- **全球同业 EV/EBITDA（LTM, 近似）：** DSV ~19x、Expeditors ~13–14x、GXO ~13.3x（纯 3PL/合同）、Kuehne+Nagel ~8.5–11x、DHL ~6.7x、C.H. Robinson ~20s（但其 EBITDA 处于周期低位，倍数被动抬高）。→ "全球十几倍、forwarder ~20x"**对 asset-light 的 forwarder/broker（DSV/EXPD/CHRW/GXO）成立**；但 DHL、K+N 这类**重资产巨头并不在十几倍**，反而贴近日本水平。
- **差距成因：** 日本市场治理折价 + 业务以国内、低增长、重资产为主；全球高倍数样本是 asset-light forwarding/brokerage（ROIC 高、并购驱动增长）；IFRS-16 口径差异；以及部分高倍数其实是周期低谷 EBITDA 的产物。
- **对 thesis 的含义：** ¥715bn 这个标价把 Logisteed 放在**日本同业之上、向全球 asset-light 区间靠**——这正是整个 IPO 叙事的赌点（公募市场到底按"全球 3PL"还是"日本物流"给倍数）。我们的 downside 担忧因此是**合理且 well-founded** 的。

---

## 2. Q1 验证:TSE 真的会 challenge "IPO 前 cap table 里有优先股"吗?

**裁决：说法 substantially TRUE，但不是 TSE 的一刀切硬规则。准确表述见下。**（结论经三组独立 research 三角验证：JPX 规则 + 律所评论 + 会社法。）

| 命题 | 状态 |
|---|---|
| TSE 只要 cap table 里**曾经**有过优先股就**禁止上市** | **错误**——无此规则 |
| TSE 规则**允许**在条件下上市种类股/投票权差异股 | **真**（硬规则；有価証券上場規程 第205条、第3編；外加实质审查） |
| **投票权双层结构（dual-class）** 面临 TSE 明确且极严的条件（breakthrough ~75%、sunset/解消预期、不得用于经营层固守、保护少数股东） | **真——硬规则**；**CyberDyne (2014) 是唯一显著先例**，12 年来基本无人再用 |
| 公司**必须**在 IPO 前把优先股转普通股，是 **TSE 的法定强制** | **作为"TSE 法定强制"不成立** |
| 公司**实务上**几乎一律在 IPO 前把优先股转普通股，是**主承销商**要求（通过取得条項） | **真——市场惯例**（near-universal） |
| 经济性优先权（优先清算/优先分红）在上市时被**专门禁止** | **错误**——无专门禁令；靠"转普通股"这一动作被 unwind |
| VC/PE 的优先权能**带过 IPO** | **错误**——上市时放弃；只在 M&A/trade-sale 退出场景（みなし清算）才兑现 |

**两个底层机理（这决定了我们结构怎么设计）：**

1. **承销商习惯层：** 日本优先股普遍内置 **取得条項（会社法 Art. 108(1)(6)）**，以"董事会决议申请上市"为触发，**公司强制收购全部优先股、换发普通股（一斉転換，通常 1:1）**。主承销商坚持这么做，因为公募市场要的是干净的单一类普通股。

2. **会社法硬约束层（比交易所规则更刚性）：**
   - **财源规制（Art. 461）：** 公司分红 + 回购自家股，总额不得超过**分配可能額**。Pre-IPO 公司常常没有可分配盈余 → **公司层面无法合法用现金赎回/回购**优先股。硬来的话董事按 **Art. 462/465** 承担连带恢复责任，且超额部分**全体股东一致同意也不能豁免**（这是保护债权人的强行法）。
   - **股东平等（Art. 109）：** 公司不得对**同一类**股东里的某几个给保底/固定回报，否则**无效**。差异化只能通过**种类股**（法定例外）实现；而种类股在上市时又要被 unwind（见上）。再叠加**资本维持原则（出資の払戻し禁止）**与**出資法**（向公众募集时承诺保本/保收益本身可能违法）。
   - **关键豁免（这是全篇的钥匙）：** 取得請求権/取得条項在**对价是公司自家股票（share-for-share，即转普通股）时，不受财源规制限制**；只有用现金/其它财产对价时才受限。**这正是"IPO 前把优先股转普通股"在法律上唯一干净的路径，也正是"公司层面现金保底走不通"的根因。**

> **对我们的核心 takeaway：** 任何依赖**上市主体（issuer）**给我们经济保护的结构（优先清算、公司回购、公司层面 ratchet），在日本要么被会社法卡死、要么被承销商在 IPO 前强制 unwind。**所以 downside protection 必须搬到 issuer 之外（sponsor/基金/控股 SPV 层面），或者放在 IPO 之前的私有期并接受其在上市时消失。** 这把可选项一下子收敛到第 4 节的 B 类。

---

## 3. 设计原则:三条红线（任何提案先过这三关）

来自跨法域先例（HKEX GL43-12、中国 VAM 清理、日本 tobashi、US Wharf/MBIA）的共同规律——一个 downside 安排能否与 IPO 共存，**不取决于它存不存在，而取决于下面三点：**

- **红线 1｜Obligor ≠ 上市主体。** 义务人必须是 **KKR 的 sponsor/基金/控股 SPV 或老股东**，不能是 Logisteed 本身。issuer 层面的 put/赎回/保证在 NVCA 实务、HKEX GL43-12、中国 CSRC（2021.9 起）都必须在上市前终止/转股；会社法在日本更是直接卡死。**股东对股东（shareholder-to-shareholder）的安排才能 survive。**
- **红线 2｜不挂钩上市后股价。** 与 post-listing market price / 市值直接联动的保证（典型的"跌破 X 价就补"）即便放在股东层面，在 HKEX 也明确不允许 survive（违反股东平等/制造同股两价）。要做"return guarantee"，锚定**固定 entry price + 约定 IRR/MOIC**，而不是二级股价。
- **红线 3｜可披露，不做暗箱。** 日本有惨痛先例：**tobashi（飛ばし）/ 簿外 买回协议**（Olympus ~$1.7bn 隐损案）——秘密的回购/保底承诺在日本**明确违法**，可致民事赔偿与刑责。美国 Wharf、MBIA、Morgan Stanley "parking" 同样把**未披露的回购/保底 side deal 当证券欺诈**。"抽屉协议"这个词本身没问题（side letter 与主合同同等效力），**致命的是"抽屉里藏着、与披露内容相矛盾"**。我们要做的是**披露过的 sponsor-level side letter**，不是 tobashi。

**一个跨亚洲都通用的起草装置——"上市时终止 + IPO 失败自动恢复"（reactivation / 恢复条款 / revival clause）：** 中港印的市场标准做法是把 pre-IPO 特殊权利（put/回购/对赌）**在 IPO 申报时终止，但写明若 IPO 失败（撤回/被否/长停日前未完成）则自动恢复**——既让上市主体在上市期"干净"，又保住"IPO 没成"这个尾部场景下投资人的保护。中国 CSRC IPO审核50条允许保留 VAM 的**四条件**（① 发行人非义务方 ② 不含可致控制权变更条款 ③ 不与市值挂钩 ④ 不损害发行人持续经营/其他投资者）几乎与上文三条红线一一对应；HKEX GL43-12 明确允许"divestment right 上市时终止、IPO 不成则 revive"。**这给我们一个具体抓手：把 sponsor-level 保护拆成两段——(a) IPO 成功路径：靠 B 类 sponsor 层面经济补偿；(b) IPO 失败路径：靠一个 reactivation 的 put 回 KKR。** 需 counsel 确认日本是否同样接受（日本无与 HK GL43-12 同等细度的成文 pre-IPO 指引，但方向一致）。

---

## 4. 结构清单 — 按"义务放在哪一层"逐个评估

四层：**A 上市主体层（基本不可行）｜B Sponsor/基金层（正解区）｜C 进入价格层｜D 上市后对冲层**。每个给：mechanics → 先例 → 在日本 realistic 吗 → 对我方 → 对 KKR/公司的 consideration → 障碍。

### A 类｜上市主体（issuer）层面 —— 结论：在日本基本走不通，列出供排除

**A1. 可转优先股 + 优先清算权（convertible preferred w/ liq pref）**
- *Mechanics：* 进可转优先股，带 1x（或参与型）优先清算权，IPO 时按取得条項转普通股。
- *先例/事实：* 这是 VC 标准件；但**优先权在 IPO 时全部消失**，只在 trade-sale/不上市场景（みなし清算）兑现。Kioxia（TSE, 2024.12）的 Series 1/2 优先股在上市后被**回购注销 ~¥330.4bn**——印证特殊股不会作为上市股留存。
- *日本 realistic？* 作为**纯 downside 工具不 realistic**——上市即归零。会社法还让现金赎回基本不可行。
- *对我方：* 仅在"IPO 失败、改走 M&A"的尾部场景有用；IPO 成功场景下零保护。
- *对 KKR/公司：* 承销商会要求 IPO 前清理；留着反而拖累上市叙事。
- *障碍：* 红线 1 直接撞墙。**→ 不作为主方案。**

**A2. IPO ratchet / 转股比例调整（公司层面）**
- *Mechanics：* 若 IPO 定价低于我方 entry（或低于"entry + 约定回报"门槛），上市时调高转股比例、给我方**补发普通股**，把我方补到 minimum value。
- *先例（已 verify）：* **Square/Block 2015** 是教科书案例——Series E $15.46 进、门槛 $18.56（≈+20% 保底回报），IPO 定 $9 → 触发**多发 ~10.3M 股、约 $92.7M**（受益方含 Rizvi Traverse、JPMorgan）。Box 2015、Chegg 2013 亦有触发。Fenwick 数据：2014–15 约 30% 独角兽轮带 IPO ratchet。
- *日本 realistic？* **不理想。** 长島·大野·常松（Nagashima Ohno）明确指出：在日本"优先股 IPO 前必须强制转普通股"的结构下，**美式 IPO ratchet 难以直接落地**。且补发会**稀释**其他股东、**必须在招股书披露**（招股书要做 price-sensitivity 表）、直接**打击 IPO 定价与 optics**——KKR 几乎一定抗拒。
- *对我方：* 经济上正中下怀（精准补到目标价），但落地与披露摩擦大。
- *对 KKR/公司：* 上市叙事杀手；定价越低、我方拿越多股，与所有其他人利益冲突，承销商不欢迎。
- *障碍：* 红线 1（issuer 发股）。**→ 若要保留 ratchet 的经济效果，应搬到 B 类的 sponsor 层面结算（见 B3），而非公司发股。**

### B 类｜Sponsor / 基金 / 控股 SPV 层面 —— 正解区（这是你说的"fund level guarantee"该落地的地方）

> 核心思路（HKEX GL43-12 已验证的"survive-IPO 的 return guarantee"路径）：把保底义务做成 **KKR 控股方对我方的纯股东间合同**，不碰 issuer 资产负债表、不挂钩上市后股价、做合规披露 → 可与 IPO 共存。

**B1. Sponsor/基金层面 PUT（我方按 entry + min IRR 把股份 put 回 KKR 控股方）**
- *Mechanics：* 触发事件（如 X 年内未 IPO、或 IPO 定价/退出实现值低于 entry+约定 IRR）发生时，我方有权把股份**按预定价（实现目标 IRR/MOIC）卖回给 KKR 的控股 SPV 或基金**。
- *先例：* HK 实务的标准做法（Hong Kong Lawyer 专文）；中国 VAM 也已演进为"由**控股股东/实控人**而非公司或 GP 承担回购"（GP 自己保底可能因"共担风险"原则被判无效，第三方/控股股东补足则不受此限）。
- *日本 realistic？* **结构上可行**（股东对股东、不碰 issuer），但要 counsel 确认 **FIEA/TSE 对大股东间 side agreement 的披露要求**，以及**绝不能做成 tobashi**（红线 3）。
- *对我方：* 最干净的真·minimum return；信用风险从"Logisteed 资产负债表"变成"KKR 控股方信用"。
- *对 KKR/公司：* 不影响上市主体 cap table，是它能接受的形态；但 KKR 要在自己（或基金）层面背一个或有负债。
- *障碍/谈判点：* **KKR 大概率不肯用整支 flagship 基金 guarantee**——会 cross-collateralize、伤其他 LP、影响基金 IRR 报告。更现实的落点是 **deal-specific SPV/holdco 担保**，或把它做成 B2/B3 的 deferred/contingent 对价。要 KKR 给 enforceability + 偿付能力陈述（参考 Duane Morris/Dechert 对 sponsor guarantee 的处理）。

**B2. Structured secondary：递延 / 或有对价（deferred / contingent purchase price）**
- *Mechanics：* 我方名义按 12.5x 进（保住 KKR/Japan Post 的 fairness 面子），但**实际成交价通过递延付款 + 或有调整**实现——例如部分对价在 IPO 后按实现估值结算，若 IPO 定价低于门槛，则我方少付/KKR 退还差额（earn-in / deferred consideration）。
- *先例：* M&A 里 deferred/contingent consideration 是常规；SPAC 的 non-redemption agreement 是"sponsor 用自己份额补足投资者结果"的**公开披露**版（8-K Ex.10.1），证明 sponsor-funded 的 downside 安排**透明做就合法**。
- *日本 realistic？* 可行；本质是买卖双方价格条款，不进 issuer cap table。需 counsel 看会计/披露与是否触发关联交易规则。
- *对我方：* 把"名义高价"与"有效低价"分离——既给对方台阶，又压低我方真实成本。
- *对 KKR/公司：* 保住对外 headline 倍数（对 IPO 叙事、对 Japan Post 的 MFN 友好）；代价是 KKR 实际 realize 的现金被递延/打折。
- *障碍：* 若 KKR 在意的是"账面 mark"而非现金，这条很有吸引力；若在意现金落袋，则抵触。

**B3. Co-investment side letter = 合规版"抽屉协议"（sponsor make-whole / top-up）**
- *Mechanics：* KKR 控股方以 side letter 承诺：**IPO 后在约定窗口内，通过向我方按约定价转让额外股份、或现金 top-up，把我方补到 min MOIC/IRR**。把 A2 ratchet 的经济效果搬到 sponsor 层面结算（KKR 自己的股票/现金补，而不是公司增发）。
- *先例：* co-investment side letter 是 PE 常规（ABA/Dechert）；HKEX 框架下"控股股东 return guarantee"可 survive（须披露、不挂股价）。
- *日本 realistic？* 可行**但 red-line 3 最敏感**——必须**披露**、不可暗箱，否则正落入 tobashi/簿外 的违法地带。务必 counsel 出 FIEA 披露意见。
- *对我方：* 灵活、可精确锚定目标回报；信用敞口在 KKR。
- *对 KKR/公司：* 不碰 issuer；但若需在招股书/大股东文件披露，KKR 可能不愿让市场看到"有人被保底"（影响其他 IPO 投资者观感与定价）。**披露义务与保密诉求之间的张力，是这条的核心谈判难点。**
- *障碍：* 披露 vs 保密；以及"被保底者"信号对 IPO book 的负面影响。

**B4. Total-Return-Swap 式安排（sponsor 承担经济上下行）**
- *Mechanics：* 我方持法律名义股，但通过 swap 式现金流，**KKR 承担参考资产（Logisteed 股）的上下行、付我方固定回报**；或反向部分对冲下行。
- *日本 realistic？* 概念可行，但是**衍生品**，触发 FIEA/衍生品监管与会计并表问题，复杂度高、对 KKR 而言等于全额背风险——KKR 接受度低。
- *评估：* 列为理论项，**优先级低**；除非只对冲一部分下行。

### C 类｜进入价格 / 估值机制层面 —— 不碰 cap table 结构，改"价怎么实现"

**C1. Valuation true-up / anti-embarrassment（以 IPO 定价回看调整 effective entry）**
- *Mechanics：* 约定若 **IPO（或后续私募轮）定价低于我方 entry**，则**回看下调我方有效 entry price**，差额在 **sponsor 层面**（非公司）以现金或转股结算。等于"只对 IPO/后续轮 reprice 的 MFN"。
- *先例：* anti-embarrassment / MFN 在 secondary 与 late-stage 常见；但要注意别滑回"挂钩二级股价"（红线 2）——**锚定一级发行价（IPO offer price）而非上市后交易价**是关键区别。
- *评估：* 可行，是 B3 的"价格版"；同样需披露与 sponsor 背书。

**C2. IPO cornerstone（改为上市时进，而非 pre-IPO）**
- *Mechanics：* 不做 pre-IPO，等 IPO 时做 cornerstone，按发行价进、锁定 allocation。日本对应机制是 **oyabike（親引け）**（2022 年 JSDA 放宽，可向"提升公司治理/企业价值的机构"配售）与 **indication of interest**——可视为日本版 cornerstone，但**比 HK 的 cornerstone（保证配售 + 6 个月锁定 + 强制披露）要松/弱**。
- *评估：* **不解决 downside**——cornerstone 只给"配售确定性 + 定价信号"，按发行价进、承担全部市场风险，锁定期内还不能对冲。**与我方诉求（minimum return）正交**，但可作为"如果谈不拢 pre-IPO 保底，就退到 IPO cornerstone"的 fallback。

### D 类｜上市之后的对冲层面 —— 受锁定期限制，只能管"锁定期之后"

**D1. Collar / Prepaid Variable Forward (PVF) / TRS**
- *Mechanics：* 上市后用 costless collar（买 put 设地板 + 卖 call 设天花板）、或 PVF（今天先拿 ~75–85% 现金、到期按区间交可变股数）、或 TRS 对冲集中持仓下行。
- *先例：* Ronald Lauder、Tyson 家族都用过 PVF（SEC 13D/A 披露）。
- *日本/通用约束：* **lock-up（通常 180 天）内几乎一律禁止任何对冲**（lock-up 协议 + 内幕/反对冲政策）。**锁定期内的 downside 这条完全管不了**；只能覆盖锁定期之后。pre-IPO 受限股做 forward 还可能触发"security-based swap"重定性。
- *评估：* 只能作为**锁定期后**的补充对冲，**不替代** pre-IPO 的保底安排。

---

## 5. 推荐的可落地方案（排序）+ packaging

**主推组合（建议作为 term sheet 起点）：**

> **名义按 12.5x（pre-IFRS cash EBITDA）进 + KKR 控股 SPV 层面的 minimum-return 保证（put / make-whole，锚定 entry + 约定 IRR，非挂钩二级股价，做合规披露）+ 以 structured secondary（递延/或有对价）把有效成本压到统一 IFRS 口径下的合理水平。**

理由：既给足 KKR/Japan Post "fairness"的台阶（headline 倍数不破），又把我方的真实下行风险转移到 **sponsor 信用**而非 issuer，绕开会社法与承销商在 IPO 前的强制 unwind。

**落地优先级：**

1. **① B1 + B2（sponsor-level put + structured secondary）：** 最贴合你说的"fund level guarantee / minimum return"。**谈判预期：KKR 不会给整支基金 guarantee**，争取 deal SPV/holdco 层面背书 + 递延/或有对价 + KKR 偿付能力与 enforceability 陈述。
2. **② B3（合规披露的 sponsor make-whole side letter）：** 把 ratchet 的经济效果搬到 KKR 层面结算。**死磕点：FIEA 披露口径与 KKR 的保密诉求之间的平衡。**
3. **③ C1（valuation true-up，锚定 IPO 发行价、sponsor 层面结算）：** 作为 ②的价格化变体或叠加项。
4. **④ "软"保护打底（无论结构谈成与否都要拿）：**
   - 用 **IFRS-16 统一口径**把名义 12.5x 的有效倍数谈到更可比的水平（§1.1）；
   - 谈 **governance / information rights / IPO 时点与 lock-up 的协调权**、**anti-dilution 至 IPO**、**tag-along / co-sale**、**IPO 失败的替代退出（M&A 场景的 みなし清算 优先权）**；
   - **fallback：** 若 pre-IPO 保底完全谈不拢，退到 **IPO cornerstone/oyabike**（C2）+ 锁定期后 collar（D1）。

**Packaging（怎么把"公平"讲回给 KKR）：**
- "我们尊重 Japan Post 的 12.5x，headline 我们不破——**但 Japan Post 是 strategic、拿了 business alliance 协同，我们是 financial 拿不到这些**，纯财务投资者按战略价进，对我们的 LP 才是 not fair。所以**名义对齐、经济上由 sponsor 层面做对称补偿**，是同时满足两边'fairness'的唯一解。"（呼应 §0.3）

---

## 6. 对双方的 trade-off 总表

| 方案 | 我方收益 | 我方残余风险 | 对 KKR 的代价 | 对公司/IPO 叙事 | 红线/障碍 |
|---|---|---|---|---|---|
| A1 可转优先股+清算权 | 仅 M&A 尾部场景 | IPO 成功即归零 | 低（但要 IPO 前清理） | 中性偏负 | 撞红线 1 |
| A2 公司层 IPO ratchet | 精准补到目标价 | 披露/落地摩擦 | 高（稀释+定价杀手） | **负**（招股书披露、optics 差） | 撞红线 1；日本难落地 |
| **B1 sponsor put/保证** | **真·minimum return** | KKR 信用风险 | 或有负债（拒整基金担保） | 中性（不碰 cap table） | 红线 3 披露；基金 vs SPV |
| **B2 递延/或有对价** | 有效成本下降 | 结算/会计风险 | 现金递延/打折 | **正**（保住 headline 倍数） | 关联交易/会计 |
| **B3 sponsor make-whole side letter** | 灵活锚定回报 | 披露暴露"被保底"信号 | 或有负债 | 中性偏负（若须披露） | **红线 3 最敏感** |
| B4 TRS | 全额对冲下行 | 复杂/监管 | 全额背风险 | 衍生品并表 | 接受度低 |
| C1 valuation true-up | reprice 保护 | 同 B3 | 同 B2/B3 | 正（锚发行价） | 别挂二级价 |
| C2 IPO cornerstone | 配售确定性 | **无下行保护** | 低 | 正（背书定价） | 不解决诉求 |
| D1 collar/PVF | 锁定期后对冲 | **锁定期内无用** | 无（我方自做） | 中性 | lock-up 禁对冲 |
| 软保护(口径/治理) | 压低有效倍数+治理权 | — | 让步估值口径 | 中性 | 谈判强度 |

---

## 7. 必须由日本 counsel / deal team 闭环的 open questions

1. **12.5x 的精确口径：** 哪个 EBITDA（pre-IFRS cash vs IFRS-16）、EV 还是 equity、含不含租赁负债？——直接决定"溢价"真伪与谈判基线。（向 deal 材料 / Japan Post 2025-11-14 日文 IR、Logisteed FY2024 Integrated Report 取数。）
2. **FIEA / TSE 对大股东间 side agreement 的披露要求（已有初步答案，仍需 counsel 定稿）：** 关键轴是 **issuer 是不是合同一方**。FIEA 的强制披露 line item 都挂在"发行人是合同方/对象"上：
   - **2023 年"重要な契約"披露新规**（开示府令修订，适用 FY 截至 ≥2025/3/31）首次明确把"公司与股东之间"的治理协议、股份处分/增持协议（含 lock-up、买回权）纳入披露——**但明确豁免"公司不是一方"的纯股东间/个人间协议**（三浦 & パートナーズ 解读）。
   - **关连当事者注记（ASBJ 11 号）** 同样只管"涉及公司"的交易；**纯股东对股东、不涉公司的交易在披露范围外**。
   - **结论：** 一个 KKR↔我方、issuer 不参与、不涉 Logisteed 股份/治理、不上 issuer 资产负债表的 sponsor-level 保证，**从强制 line item 看大概率可不披露**；
   - **但这个豁免脆弱：** ① 若保证嵌在 issuer 也签字的 SHA 里、② 若实质构成对 issuer 的交易/负担、③ 若扭曲了须披露的"价格算定根拠"、④ 若其存在对投资者"重大"（FIEA Art. 18/21 重大遗漏 backstop），都会被拉回披露；且 **TSE 上市审查 + 主承销商尽调几乎一定会问到**，未披露的保底还可能面临 enforceability 风险（参照 HK 经验）。**实操结论：按"会被尽调问到、必要时须披露"来设计，把 issuer 严格隔离在外、不挂股价，把 issuer-vs-shareholder 这条线当作"免于强制 line item 的盾"，而非"永不披露的保证"。**
3. **KKR 能背到哪一层：** 整支基金 guarantee（几乎不可能）vs deal SPV/holdco vs deferred consideration——以及对 KKR 其他 LP / co-investor 的 MFN 触发。
4. **我方是 primary 还是 secondary：** 若是从 KKR 买 secondary，则 KKR 天然是 obligor，B 类更顺；若 primary 注资进公司，则要额外安排 sponsor 背书。
5. **会社法细节：** 任何 IPO 前的私有期优先权设计，确认取得条項/取得請求権、財源規制（Art. 461）、股东平等（Art. 109）边界（建议 counsel 直接核对 e-Gov 会社法原文与 有価証券上場規程 第205条/第3編、上場審査ガイドライン 现行版）。
6. **税务：** 递延/或有对价、sponsor top-up 的日本税务与我方基金层面处理。

---

## 附录 A — 先例库（已 verify / 已标注口径）

| 先例 | 要点 | 对我们的用处 |
|---|---|---|
| **Square/Block (2015, US)** | Series E $15.46 进、门槛 $18.56(+20%)、IPO 定 $9 → 触发多发 ~10.3M 股 ≈ $92.7M | IPO ratchet 经济效果与"招股书必须披露 price-sensitivity"的教科书；说明为何要搬到 sponsor 层面 |
| **Kioxia (TSE, 2024.12)** | Bain 牵头；SK Hynix 通过 Bain SPC 持**可转债**+ LP commitment，把经济敞口放在**上市普通股之外**；优先股上市后回购注销 ~¥330.4bn | 日本"特殊工具不作上市股留存"+"敞口放 issuer 之外"的本土印证 |
| **HKEX GL43-12** | issuer 层面 put/赎回/价格调整须 IPO 前终止；**股东对股东、不挂二级价、且披露**的 return guarantee 可 survive | 我方 B 类结构的**直接法理模板** |
| **中国 VAM/对赌** | 2021.9 起禁"issuer 作回购义务人"；演进为**控股股东/实控人**回购；秘密挂市价 VAM 被判无效 | 印证"obligor 搬到控股方""不可挂市价""不可暗箱" |
| **Olympus / tobashi (日本)** | ~$1.7bn 隐损，靠**簿外买回承诺**多年隐藏 → 明确违法、刑责 | 红线 3 的反面教材：side letter 必须可披露 |
| **Wharf / MBIA / Morgan Stanley parking (US)** | 未披露的口头/秘密回购、保底 side deal = 证券欺诈 | 同上，跨法域佐证 |
| **SPAC non-redemption agreements** | sponsor 用自有份额补足投资者、**公开披露**(8-K Ex.10.1) | "sponsor-funded downside，透明做就合法"的正面模板 |
| **NTT DoCoMo v. Tata Sons (印度)** | DoCoMo（日本投资人）SHA put 要求 Tata 以"≥50% of cost"接盘；KPI 未达，LCIA 裁 **~$1.17bn**，Delhi 高院 2017 **作为"违约赔偿"强制执行**（绕过 FEMA 保底禁令） | **股东对股东的 minimum-return put 是可诉、可执行的**——但注意印度对外资有 FMV 上限（我方若为离岸基金需查类似限制）；把保底设计成"违约赔偿"而非"保证回报价"更稳 |
| **SoftBank / WeWork ratchet** | down-round ratchet 估值约 $200–500m；IPO 撤回后 SoftBank 救助、tender 又取消、被起诉、和解 | **ratchet 只保"价格下行"、不保"insolvency/IPO 不成"**——必须叠加 reactivation put 覆盖"IPO 失败"尾部 |
| **中国 STAR 板 reactivation 先例** | 铂力特(688333)/伟测科技/双元科技：特殊权利"上市申报时终止、IPO 失败自动恢复(自动恢复效力)"获放行；传音/博瑞被否后改"自始无效不可恢复" | "上市终止 + IPO 失败恢复"是可被监管接受的成文先例；但 revival 要写清四条件 |
| **CyberDyne (TSE, 2014)** | 唯一显著 dual-class 上市；B 类股单元更小→10x 投票权；75% breakthrough 转普通股 | 说明日本 voting 双层结构极难、且不为我们这种目的所用 |
| **日本 PE relisting 通例（Kokusai/Rigaku/WingArc/Dexerials/Skymark）** | 几乎全部以**单一普通股**上市；co-investor 经济/治理放在**上市时失效的股东间协议 / 資本業務提携**里，或 holdco 层工具 | 印证：上市主体只能是 clean common；保护必须在 issuer 之外。注意 **資本業務提携(资本业务合作)** 正是 Japan Post 进 Logisteed 的形态 |

## 附录 B — 主要来源（节选；完整 URL 见各 research 工作底稿）

- **JPX/TSE：** 有価証券上場規程（含第205条、第3編 優先株等）、上場審査等に関するガイドライン、議決権種類株式制度（2008 报告、2014 修订）、CyberDyne 上场资料（SAA / AMT / Plutus）。
- **会社法：** Art. 108 / 166 / 170（取得条項・取得請求権、share-for-share 豁免）、Art. 461/462/465（財源規制与董事责任）、Art. 109（股东平等）；建议以 e-Gov（法令 ID 417AC0000000086）与 japaneselawtranslation.go.jp 官方英译核对原文。
- **Pre-IPO 保护结构：** Fenwick "Terms Behind the Unicorn Valuations"；Square 424B4（SEC EDGAR）；Hong Kong Lawyer "How to Structure a Return Guarantee that Survives an IPO"；HKEX GL43-12；Mayer Brown 2017 Pre-IPO Guidance；中国 law.asia / Mondaq VAM 系列；Dechert/Duane Morris sponsor guarantee；ABA/Dechert co-investment side letters；NVCA Model Docs；PwC redeemable preferred。
- **Logisteed/估值：** Bloomberg/BusinessWire/AVCJ（KKR 收购）；Nikkei/Mingtiandi/Simpson Thacher（Japan Post 19.9%/¥142.3bn/¥715bn）；Private Equity Wire/The Loadstar（MS IPO mandate）；TI-Insight（财务/分部）；GuruFocus/stockanalysis.com/multiples.vc（同业倍数）。

> **数据质量提示：** 本环境下 WebFetch 对 JPX/SEC/HKEX/律所站点多被 403，上述事实来自 search 抽取并多源交叉印证；正式对外（IC 材料）前，建议由 counsel 直接调取 ① 有価証券上場規程第205条/ガイドライン原文、② HKEX GL43-12 原文、③ Square 424B4 章程语言、④ Japan Post 2025-11-14 IR 与 Logisteed FY2024 报告以锁定 12.5x 口径。"12.5x pre-IFRS cash EBITDA"为 client-supplied、公开来源未独立验证。
