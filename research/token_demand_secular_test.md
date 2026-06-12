# AI 算力/推理需求是否"secular-explosive 到压倒硬件供应链历史周期性"——用数据证伪/证实

### 对投资人论点的独立压力测试:"这次不一样,AI token 消耗爆炸、没人停得下来、人类永远需要更多数据中心,需求可能多年真实跑赢供给"

*作者:资深买方分析师 | 日期:2026 年 6 月 11 日*
*本文沿用 `long_term_demand_2030.md` / `storage_2026_durability_update.md` 的大白话 + 表格 + 带 URL 来源的风格。配套但不重复存储那两篇——这里只回答一个问题:**到 2030 年,AI 推理需求够不够"长期爆炸",以至于压倒硬件供应链的历史周期性?** 我不预设"周期派"是对的,两边都用硬数字 steelman。*

---

## 📖 三分钟先讲结论(给没时间读全文的人)

**一句话裁决:投资人的"这次不一样"论点 —— 在"需求侧"是 TRUE 且被低估了;在"=多年全栈无周期"上是 OVERSTATED。最诚实的读法是 (b):需求是 secular(真长期),但供给是 lumpy(一阵阵地来),所以是"结构性向上 + 中途有消化年(大概率 2027 末–2028)",不是"5 年一条直线无回调",也不是"经典泡沫"。**

| 投资人的子命题 | 裁决 | 证据强度 |
|---|---|---|
| ① "token 消耗在爆炸,且还在加速" | **TRUE,而且比多数人想象的猛** | 极强(已实现硬数据,见 §1) |
| ② "成本降→用量升更多(Jevons),没人停得下来" | **TRUE** | 强(§2) |
| ③ "需求长到 2028–30 有真金白银的承诺撑着" | **TRUE,但其中 OpenAI 那部分融资是循环/脆弱的** | 中-强(§3) |
| ④ "供给受物理封顶,涨不快→短缺结构性" | **方向 TRUE,这是论点最硬的一块** | 强(§4)——供给天花板 30–40%/年 vs 需求 100%+/年 |
| ⑤ "所以全栈多年无周期、可重仓硬 hold 到 2030" | **OVERSTATED**——会在某一年被"capex 消化 + 折旧重置 + 中国供给"打回调 | 这是论点最弱的一环(§5) |

**最关键的一句独立判断:** 把"需求是真的"和"所以不会有周期"画等号,是论点的逻辑漏洞。**1995–2000 的互联网需求也是真的、也确实长了 20 年,但中间 2000–2002 照样腰斩。需求 secular ≠ 没有 air-pocket。** 真正决定有没有回调的,不是"人类要不要 AI"(要),而是"**供给/资本投入有没有阶段性跑到需求前面**"——而 2026 年的 capex($725bn,YoY +77%)增速已经快过任何收入指标的增速,这是埋下消化年的种子。

---

## §1 TOKEN 需求硬数据:不仅爆炸,而且在加速(对投资人有利,且被低估)

这是投资人论点里最扎实的一块。**不是叙事,是各家自己披露的实测数字。**

**谷歌(最权威,CEO 公开数字):**
| 时点 | 月处理 token | 同比 |
|---|---|---|
| 2024 年 5 月(I/O) | **9.7 万亿(9.7T)/月** | — |
| 2025 年 5 月(I/O) | **约 480 万亿(480T)/月** | **约 50×** |
| 2026 年 5 月(I/O) | **超 3,200 万亿(3.2 quadrillion)/月** | **约 7×** |

- 来源:[Shacknews,2026/5](https://www.shacknews.com/article/149205/google-3-2-quadrillion-monthly-ai-tokens) / [GIGAZINE,2026/5/20](https://gigazine.net/gsc_news/en/20260520-google-monthly-tokens-processed/) / [keepingupwith.ai](https://keepingupwith.ai/articles/googles-agentic-gemini-era-token-consumption-surges-to-32-quadrillion-monthly/)
- 配套:**API 每分钟约 190 亿 token;850 万开发者在用;过去 12 个月有 375+ 个云客户各自处理超 1 万亿 token。** [来源](https://blog.google/innovation-and-ai/sundar-pichai-io-2026/)
- **一个诚实的"减速"注脚:** 从 9.7T→480T 是约 50×;从 480T→3,200T 是约 7×。**绝对基数在涨、但同比"倍数"在收敛(50× → 7×)。** 这很正常(基数大了),7×(=+600%/年)仍然是天文增速,但"加速"这个词要打个引号——**是"高速但增速在放缓",不是"越来越快"。** 这一点对投资人的"还在加速"小命题是温和的反证。

**OpenRouter(第三方路由,最干净的"市场总量"代理,因为它不含自家偏向):**
- **周 token 量:2025/4 约 5T → 2026/4 超 20T(YoY 约 4×);2026/5 已到 25T/周(约 100T/月),近 6 个月 5T→25T = 半年 5×。** 全年跑步机约 1–1.5 quadrillion token。 [Yahoo/Fundraise,2026/5/26](https://finance.yahoo.com/sectors/technology/articles/openrouter-raises-113-million-capitalg-131500093.html) / [TechStartups](https://techstartups.com/2026/05/26/openrouter-raises-113m-as-ai-token-usage-surges-to-100-trillion-monthly/) / [Menlo Ventures](https://menlovc.com/perspective/openrouter-now-processes-more-than-a-quadrillion-tokens-a-year/)
- **意义:OpenRouter 不卖芯片、不建数据中心,纯第三方,它的 4–5×/年 是最难造假的"真实需求"温度计。**

**微软 Azure Foundry:** 250+ 客户今年将各处理超 1 万亿 token;百万美元/季客户数 YoY +约 80%。 [Futurum,MSFT Q2 FY26](https://futurumgroup.com/insights/microsoft-q2-fy-2026-cloud-surpasses-50b-azure-up-38-cc/)
**Anthropic:** 年化收入从 2025 末约 90 亿美元 → 2026 年化逼近 **450 亿美元**(远超 OpenAI 2 月的 250 亿年化)。 [Sacra](https://sacra.com/c/anthropic/) / [Investing.com](https://www.investing.com/analysis/the-ai-token-pricing-crisis-behind-openai-and-anthropics-revenue-race-200680777)

**§1 小结:** token 实测增速 **YoY 约 4–7×(=+300%~+600%/年)**,跨三个独立来源(谷歌自报、OpenRouter 第三方、微软企业端)互相印证。**这个数字本身就足以击穿"AI 只是又一个普通周期"的简单类比——没有任何历史半导体周期的终端需求是以 4–7×/年增长的。投资人在这一点上对了,而且共识低估了它。**

---

## §2 推理经济学:成本 10×/年下降 × Jevons = 用量增长 > 成本下降(对投资人有利)

- **成本下降:等性能推理成本约 **10×/年** 下降(a16z 称 "LLMflation")。三年前 60 美元/百万 token 的东西,现在约 0.06 美元。** [oplexa,2026](https://oplexa.com/ai-inference-cost-crisis-2026/) / [agenticaipricing](https://www.agenticaipricing.com/pricing-ai-products-when-model-costs-fall-every-quarter/)
- **Jevons 实证(关键):** 多个 2026 来源给出同一形态——**"单 token 价格降到 1/3,token 消耗量翻了 5 倍 → 总账单不降反升"。** 这是 Jevons 悖论的硬证据:降价没有省钱,而是放大了总需求。 [softwareseni](https://www.softwareseni.com/why-ai-gross-margins-are-so-much-lower-than-saas-and-what-that-means-for-your-business/) / [priscasolutionsai](https://www.priscasolutionsai.com/blog/tokenomics-for-humans-jevons-paradox)
- **token 乘数(reasoning / agent / 视频):**
  - **推理(reasoning)模型:** 推理时再分配算力(inference-time scaling),一次"思考"比一次普通问答多吃几个数量级 token。
  - **Agent 已规模化(2026 已发生,不是 PPT):** 97% 高管说过去一年部署了 AI agent,52% 员工已在用。 [WRITER 2026 调研](https://writer.com/blog/enterprise-ai-adoption-2026/) 企业在跑"agent 舰队",每天数千次 LLM 调用;为控成本用"frontier 模型规划 + 便宜模型执行"的 Plan-and-Execute,把成本降 90%——**但这恰恰意味着 agent 把任务做大了,总 token 不降反爆。** [machinelearningmastery 2026](https://machinelearningmastery.com/7-agentic-ai-trends-to-watch-in-2026/)
  - **量级:** 一个 agentic query 的 token 消耗约是一次 chat 的 100–1000×。当 agent 从"试点"变"生产",token 曲线会再上一个台阶。

**§2 小结:** 投资人的"没人停得下来"在经济学上成立——**降价不是需求的敌人,是需求的燃料(Jevons)。** 再叠加 reasoning + agent 的 100–1000× 乘数,**单位需求强度还在结构性上移。这一段对"this time is different"是真正的实锤。**

---

## §3 需求侧承诺:2026–28 的钱是真投了,但 OpenAI 那块融资是循环/脆弱的(一半利好、一半警告)

**真金白银的 capex(已指引,不是吹):**
| 主体 | 2026 capex 指引 | 备注 |
|---|---|---|
| 四大(谷歌/亚马逊/微软/Meta)合计 | **约 7,250 亿美元,YoY +77%**(2025 约 4,100 亿) | [Tom's Hardware](https://www.tomshardware.com/tech-industry/big-tech/big-techs-ai-spending-plans-reach-725-billion) / [CNBC](https://www.cnbc.com/2026/02/06/google-microsoft-meta-amazon-ai-cash.html) |
| 亚马逊 | 约 2,000 亿 | 同上 |
| 微软 / 谷歌 | 各约 1,900 亿 | 同上 |
| Meta | 1,150–1,350 亿 | 同上 |
| **2027 展望** | **大行预测合计破 1 万亿美元**;摩根士丹利测 Alphabet 单家 2027 最高 2,500 亿 | [CNBC,2026/4/30](https://www.cnbc.com/2026/04/30/ai-boom-big-tech-capital-expenditures-now-seen-topping-1-trillion-in-2027-.html) |

- **需求被供给封住的铁证:微软自曝有约 800 亿美元 Azure 订单因缺电交付不了(backlog)。** [Tom's Hardware](https://www.tomshardware.com/tech-industry/big-tech/big-techs-ai-spending-plans-reach-725-billion) — 这是"需求 > 供给"最直接的官方供词,对投资人极其有利。

**OpenAI:这块要单独拎出来打问号(投资人论点的脆弱点):**
- 2025 末 Altman 喊出 8 年约 **1.4 万亿美元**基建承诺(Stargate 5,000 亿 + Oracle 3,000 亿五年云 + AWS 380 亿 + Azure 余额 2,000 亿+)。 [TechRepublic](https://www.techrepublic.com/article/news-openai-foxconn-stargate-data-center/)
- **但 2026 年 2 月,OpenAI 把口径下调到"2030 年前约 6,000 亿总算力支出,且明确与收入增长挂钩"——从 1.4 万亿砍到 6,000 亿,并从"自建"转向"租"(opex,不是 capex)。** [TechTimes,2026/5/19](https://www.techtimes.com/articles/316807/20260519/openai-cut-stargates-spending-pledge-14-trillion-600-billion-now-renting-what-it-vowed-build.htm)
- **对账:OpenAI 2025 收入 131 亿,2026 初年化约 250 亿。** 用 250 亿收入去扛 6,000 亿–1.4 万亿承诺,**杠杆是惊人的;且很多是"A 投 B、B 买 A 芯片"的循环结构。** [tech-insider](https://tech-insider.org/openai-revenue-miss-friar-altman-stargate-2026/)

**§3 小结:** **超大规模厂(谷歌/亚马逊/微软/Meta)的 7,250 亿是自有现金流支撑的真需求,这块很硬。** 但 **OpenAI/Stargate 那一层是"承诺 >> 收入"的循环融资,是整个需求大厦里最容易先裂的一块砖。** 投资人说"需求有承诺撑着"——对一半(hyperscaler),错一半(OpenAI 的承诺已经自己缩水 57% 了)。**这是论点第一道裂缝。**

---

## §4 供给响应:这是投资人论点最硬的一块——供给物理上涨不快

**核心论证(量化版):如果需求 +100~600%/年,而供给最多 +30~80%/年,那么无论周期与否,短缺都会结构性持续。** 逐环节查证:

| 环节 | 供给最大可行增速 | 数据 / 来源 |
|---|---|---|
| **台积电 CoWoS 先进封装** | 2024 末约 35k 片/月 → 2026 末约 130k 片/月(约 3.7×,两年);2026→2027 约 130 万→200 万单位(约 +54%);2022–27 CAGR 约 80% | [TrendForce](https://www.trendforce.com/news/2026/05/14/news-tsmc-sees-ai-wafer-demand-rising-11x-from-2022-2026/) / [FinancialContent](https://markets.financialcontent.com/stocks/article/tokenring-2026-2-5-tsmc-to-quadruple-advanced-packaging-capacity-reaching-130000-cowos-wafers-monthly-by-late-2026) |
| **HBM(物理天花板)** | 2026 合计约 31–36M 晶圆当量/年 → 约 9–10 亿个 12-Hi stack → 按 Rubin 每颗 12 stack,**全年物理上限约 750–800 万颗 Rubin 级 GPU**。三家 2026 产能 Q1 即全部售罄 | [tech-insider](https://tech-insider.org/memory-chip-shortage-2026-ai-consumer-electronics/) / [Tom's Hardware](https://www.tomshardware.com/tech-industry/artificial-intelligence/samsung-and-sk-hynix-warn-ai-driven-memory-shortages-could-last-until-2027-and-beyond) |
| **电力(真正的总闸)** | 数据中心耗电 IEA:2025 约 485 TWh → 2030 约 950 TWh(翻倍,装机约 +20%/年);**美国 2028 需求约 74 GW vs 供电缺口约 49 GW**;并网排队 2–3 年 | [IEA](https://www.iea.org/reports/energy-and-ai/energy-demand-from-ai) / [Morgan Stanley via tech-insider](https://tech-insider.org/ai-data-center-power-crisis-2026/) |

**算术对账(投资人论点的核心,我替他算清楚):**
- 需求侧(token / 算力强度):+300~600%/年(§1)。
- 供给侧上限:CoWoS 约 +54~80%/年(已经是全行业最快扩的环节);HBM 受晶圆封顶;**电力只有约 +20%/年,而且并网排队 2–3 年,是最低的那块板。**
- **结论:木桶最短板是电力(+约20%/年)。即使 CoWoS/HBM 拼命扩,整个系统的"可部署算力"被电力锁在约 +20~40%/年。需求增速(数百%)远高于这个上限 → 在 *能效改进消化掉的部分之外*,瓶颈环节(HBM、先进封装、电力设备)的结构性紧张是真实的、且可持续多年。**

**§4 小结:投资人在这里是对的,而且是论点里最有含金量的一块。** "供给物理封顶 → 瓶颈环节多年紧"成立。**但请注意一个致命区分:这论证的是"*瓶颈环节*(HBM、CoWoS、电力设备、变压器)结构性紧",不是"*整条供应链每个环节*都无周期"。** 商品 DRAM/NAND、通用服务器、甚至 GPU 整机,会被新 fab(2027–28 落地)和中国供给(CXMT/长江存储)在某个时点松动——这正是把"瓶颈紧"误推成"全栈无周期"的逻辑跳跃。

---

## §5 空头数据:裂缝在哪、有多大(对投资人不利,逐条对账)

**裂缝 1:capex 增速 >> 收入增速,"$600bn 问题"在 2026 是扩大的。**
- Sequoia 的 Cahn 框架:要 justify 当前 capex,需约 6,000 亿/年 AI 收入。 [Cahn/Sequoia 框架](https://tooldirectory.ai/blog/ai-capex-bubble-2026-where-the-revenue-actually-is)
- 实际 AI 云收入(真实、且高增):AWS 约 1,500 亿年化(+28%)、Google Cloud 约 800 亿(+63%)、Azure AI 约 370 亿年化(+123%)。 [同上,Q1'26]
- **但 capex(7,250 亿)增速(+77%)快过这些收入增速,缺口 2026 在*扩大*不是收窄。** 这不证明是泡沫,但证明 **"投入跑在收入前面"——这正是消化年(air-pocket)的标准前置条件。**

**裂缝 2:企业 ROI——比"MIT 95% 失败"那条旧 stat 更新、但仍喜忧参半。**
- 旧 stat 已被纠偏:MIT NANDA 的 95% 只衡量"6 个月内有没有 P&L 暴击",且样本偏销售/营销(最低 ROI 区)。 [WRITER 复盘](https://writer.com/blog/enterprise-ai-adoption-2026/)
- 2026 新数:**只有 29% 组织从 GenAI 看到显著 ROI、23% 从 agent 看到**;但 **66% 用 agent 的公司有可测的生产力提升**,做对的组织 ROI 达 5–10×。 [onereach 2026](https://onereach.ai/blog/agentic-ai-adoption-rates-roi-market-trends/) / [Futurum](https://futurumgroup.com/press-release/enterprise-ai-roi-shifts-as-agentic-priorities-surge/)
- **判读:ROI 在变好(直接财务影响占比近翻倍到约 22%),但"普遍显著 ROI"还没到。需求由"少数赢家 + FUD/军备竞赛"双驱动,后者一旦退潮会放大回调。**

**裂缝 3:Burry 的折旧论——老化得"部分正确"。**
- Burry(2025/11):hyperscaler 把 GPU 按 5–6 年折,真实经济寿命更像 2–3 年(英伟达 12–18 月迭代,Rubin 2026 下半年出);估 2026–28 少提折旧约 1,760 亿,虚增利润约 20%,正常化会砍 MSFT/GOOGL 2026–28 EPS 约 15–25%。 [CNBC](https://www.cnbc.com/2025/11/11/big-short-investor-michael-burry-accuses-ai-hyperscalers-of-artificially-boosting-earnings) / [247wallst](https://247wallst.com/investing/2026/03/24/was-michael-burry-right-about-ai-stocks-for-the-wrong-reason/)
- **但反证(关键 tell):用 GPU 寿命没那么短。** 二手 A100(2020 年发布、6 岁)仍是二级市场交易最活跃的卡之一,二手 80GB 约 4,000–9,000 美元、6–9 月回本,且推理需求还在租它。 [hashrateindex](https://hashrateindex.com/blog/used-gpu-market-pricing-deprecation-secondary-ai/) / [jarvislabs](https://jarvislabs.ai/blog/a100-price)
- **判读:Burry 的*会计*警告对(折旧确实偏松,会有某一家先 write-down 引爆波动);但他的*物理*前提(GPU 2–3 年变废铁)被二手市场证伪——老卡降价但没归零、还在推理端干活。所以这是"利润质量风险"(EPS 重置),不是"资产瞬间报废"。**

**裂缝 4(最重要的实时温度计):GPU 租金在涨,不在跌——强烈支持多头。**
- **H100 租金:2024 初约 7 美元/时 → 但 2026 年没有继续崩;1 年合约价 2026/1 月底突破 2 美元/时,2 月环比再 +15–20%,3 月又预计 +15–20%,到 3 月"任何期限都租不到 H100/H200/B200"。** [SemiAnalysis](https://newsletter.semianalysis.com/p/the-great-gpu-shortage-rental-capacity) / [Thunder Compute](https://www.thundercompute.com/blog/ai-gpu-rental-market-trends)
- **这是最难造假的实时供需信号:如果是泡沫/过剩,租金会塌;现实是连两代前的 H100 租金都在涨、租不到货。** 对投资人论点是最有力的实时证据。
- **唯一反向裂缝(neocloud 财务):CoreWeave 债务/股本 >7×,2026 有约 42 亿到期墙,经营现金流靠借新还旧;微软曾全球性收缩部分数据中心租约(但 CoreWeave 称已找到替代买家、属微软孤例)。** [Wedbush](https://investor.wedbush.com/wedbush/article/finterra-2026-2-23-the-gpu-debt-wall-a-deep-dive-into-coreweave-crwv-and-the-2026-ai-financing-crisis) / [DCD](https://www.datacenterdynamics.com/en/news/microsoft-steps-back-from-data-center-developments-globally-report/)
- **判读:实物层(GPU/租金/HBM)零裂缝、全线紧张;裂缝在*金融层*(neocloud 杠杆、OpenAI 循环融资、折旧会计)。** 这正是"需求真、但融资结构脆弱"的画像——也是为什么回调更可能由"融资事件"触发,而非"需求消失"。

---

## §6 裁决:三种情景 + 概率 + 哪层硬件受益

**我把所有数据归位后,最诚实的概率分布是:**

| 情景 | 描述 | 概率(我的判断) | 哪层硬件受益 |
|---|---|---|---|
| **(a) 需求 secular + 供给封顶 = 全栈多年短缺(投资人原版)** | 需求数百%/年,供给约 20–40%/年,2026–30 一路紧 | **约 25%** | 全栈;但要素是"瓶颈层定价权一直在" |
| **(b) 需求 secular,但供给 lumpy = 结构性向上 + 中途消化年(我的基准)** | 趋势真、长期向上;但 2027 末–2028 因 capex 透支 + 新 fab/中国供给 + 折旧重置,出现 1 个 air-pocket 后再上行 | **约 55%(最高)** | **瓶颈层穿越周期:HBM、先进封装(CoWoS)、电力设备/变压器、光互联;商品 DRAM/NAND/通用服务器会先回调** |
| **(c) 经典泡沫(需求被高估、capex 崩、类 2000)** | AI 收入永远追不上 capex,融资链断、需求证伪 | **约 20%** | 几乎无;现金流硬的台积电/电力公用事业相对抗跌 |

**为什么基准是 (b) 而不是投资人的 (a):**
1. **需求侧 (a)/(b) 没分歧——token 4–7×/年、Jevons、agent 规模化、供给物理封顶,全都成立(§1/2/4)。投资人在"需求 secular"上完胜周期派。**
2. **分歧只在"会不会有中途回调"。** (a) 要求"供给*永远*追不上"。但数据显示瓶颈是*分层错峰解除*的:CoWoS 两年 3.7×、新 fab 2027–28 落地、中国 CXMT/长江存储 2027 放量、电力 2028–30 上 onsite gas。**任何一层在某季度从"缺"转"够",叠加 capex 增速(+77%)已远超收入增速(+28~123%)埋下的消化压力,就足以触发一个 air-pocket——尤其经由脆弱的金融层(OpenAI 循环融资缩水 57%、neocloud 42 亿债务墙、折旧 write-down)引爆。**
3. **历史不是"类比",是"机制":需求真(互联网 1995–2025 都真)从不阻止周期(2000–02 照样腰斩)。决定回调的是"资本投入有没有阶段性超前",而 2026 已经超前了。**

**一句话给投资人的独立回话:** 你"需求这次真不一样"是对的,且被低估——别让周期派用"历史都是周期"这种懒惰类比把你劝退。**但你从"需求 secular"跳到"全栈多年无周期、可无脑硬 hold"是一步过头。** 正确的下注不是"赌没有回调",而是 **"赌瓶颈层(HBM/CoWoS/电力/光)穿越那个回调",并在 2027 末–2028 的消化年用商品端(DRAM/NAND/通用服务器/高杠杆 neocloud)的回调来加仓瓶颈层。** 最该盯的实时信号:**GPU 1 年期租金由涨转跌(目前在涨,§5 裂缝 4)= 周期顶的第一声;以及第一家 hyperscaler 的 GPU 折旧 write-down(Burry 引信)= 利润重置的发令枪。**

---

## 附:最该盯的 5 个 dated 信号(谁先动谁就是拐点)

| 信号 | 现状(2026/6) | 触发含义 |
|---|---|---|
| **① GPU 1 年期租金 QoQ 由涨转平/跌** | **在涨**(突破 $2/时,连月 +15–20%) | 实时供需最灵敏的顶部信号;一旦转跌即数字化的"周期顶" |
| **② 任一 hyperscaler 下调 2027 capex 指引** | 未触发(2027 共识破万亿) | 需求引擎单点失效 |
| **③ 首家 hyperscaler GPU 折旧 write-down** | 未触发(Burry 引信) | 利润重置,"history they move in packs" |
| **④ OpenAI/Stargate 融资进一步缩水或违约** | **部分触发**(1.4T→0.6T,转租赁) | 最脆弱金融层先裂 |
| **⑤ 中国 CXMT/长江存储 + 新 fab 2027 放量** | 临近(2027) | 商品端见顶、瓶颈分层解除 |

*免责:本文为研究框架与概率判断,非买卖建议。所有"我的判断/基准"均已与"已实现硬数据/共识预期"显式区分。*
