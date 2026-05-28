# AI 时代的软件行业 —— 什么能活、什么被杀,以及最值得长期布局的 Top 5
### 战略深度报告:不只看财务,看的是"在 agentic AI 浪潮里,软件的护城河往哪迁移"
*作者:资深买方分析师*
*日期:2026 年 5 月 28 日。供没有技术背景的投资委员会(IC)读者,大白话标准,不用波浪号。本报告综合 5 路深度研究(战略框架+大佬观点 / 应用 SaaS / 数据基础设施 / 安全+开发工具 / AI 原生颠覆者),提炼判断 guideline、做全行业 mapping、并给出 Top 5(按你的要求:不看估值,只看天花板×质量×卡位×资源×赋能而非替代×捕获 AI 的能力)。市值/数字为 2026 年 5 月口径,需终端复核。*

> **本报告回答:** ①AI 时代什么软件有核心竞争力、能活;什么会被替代? ②提炼一套判断 guideline。 ③把现有软件公司逐一 mapping(受益/中性/被杀)。 ④Datadog/Snowflake 这类"铲子股"到底是不是受益? ⑤未来 AI 时代软件的收费/商业模式怎么变,谁最受益? ⑥Top 5。

> **质量审查记录(QC):** 本报告经 5 路并行深度研究 → 综合成文 → critical-thinker 红队 challenge → 据此修订。**红队改了什么(已落地):** ①Top 5 补入 **Google**(初稿漏了最便宜、最可拥有的模型层敞口,与"价值上移到模型层"的核心结论自相矛盾);②**Snowflake、Palantir 从 Top 5 降到荣誉席**(理由是商业模式 / 竞争,非估值——见第六部分);③用 **Datadog** 取代 Snowflake 作"中立铲子";④**收窄 ServiceNow 的论点**(durable 的是它的数据 / 权限 / 审计 SoR,不是工作流界面);⑤补"**财报是滞后指标、要盯 GRR 不是 NRR**"的反向纠偏(第〇 / 五部分);⑥补"**消耗计价是双刃剑**"(token 通缩 + 客户优化,Twilio 反例,第三部分);⑦补"**开放权重模型商品化模型层**"这一贯穿 Top 5 的风险(第六 / 八部分);⑧把"硬件褪去 → 资金轮动进软件"明确为**一个情景而非机械规律**(第七部分)。数字 / 市值为 2026 年 5 月口径,多处私有数据为二手,需终端复核。

---

## 第〇部分:三句话先讲清楚(以及一个最关键的纠偏)

> **1. 最锋利的判别规则:收入随"机器工作量/交易额/数据量"增长的软件 = AI 受益;收入随"人类座席数"增长的 = AI 被威胁。** 因为 AI 的明确目的就是减少人头——对前者是顺风,对后者是逆风。

> **2. 护城河在迁移,不是消失:AI 杀死的是"界面护城河"(人点进去操作的 UI、按座席收费),但加深"数据/系统-of-record/治理基底护城河"(agent 必须经由它行动的那层)。** 大佬其实不冲突:Nadella 说"业务逻辑上移到 AI 层"、Casado 说"按座席的计价单位失效"、Levie 说"数据和上下文基底更值钱"——三句话同时成立。

> **3. 一个必须纠偏的关键事实(这是最容易犯的错):把"头条里的颠覆"当成"财报里的颠覆"。** 真正在财报里流血的公司(Chegg、ZoomInfo、Gartner、C3.ai、UiPath、Asana)被杀的机制是**"数据/内容垄断被去中介"或"纯座席被压缩"**;而头条最响的"Sierra 杀接触中心、Cursor 杀开发工具"——在 listed 在位者的财报里**还没兑现**(NICE 的 AI ARR +66%、Five9、Twilio NRR 升到 114%、Figma +46% 都在反驳)。**投资上要押财报,不要押头条——但配一个反向纠偏:财报是滞后指标(颠覆通常领先财报 12 到 24 个月才显形),而且 NRR 会被"涨价掩盖座席流失"美化。所以要盯 GRR(gross retention,毛留存,剥掉扩张后老客户的钱还剩多少)和座席数本身,别等 NRR 跌穿 100% 才反应——那时已经晚了。**

---

## 第一部分:大白话 —— AI 对软件到底意味着什么(大佬之争的调和)

**(名词:SaaS = 软件即服务,按订阅/座席收费;agent = AI 智能体,能自主完成任务;system of record / SoR = 系统-of-record,企业某类数据的权威存放与流转中枢,如 CRM、ERP、HR 系统。)**

过去两年的大辩论,表面对立,其实在讲**软件栈的不同层**:
- **"会塌"派(Nadella / a16z / Sequoia):** 微软 CEO Nadella(2024/12 BG2 播客)说业务应用"本质是带业务逻辑的 CRUD 数据库",agent 时代"所有逻辑都上移到 AI 层",SaaS 退化成"数据库+治理"。a16z 的 Rampell 把蛋糕重新定义:SaaS 约 $3000 亿/年,而它现在能攻打的是约 $13 万亿的**劳动力市场**——"软件开始吃劳动力"。Sequoia:AI"把劳动力变成软件",TAM 是以万亿计的服务市场。
- **"更难被颠覆"派(Aaron Levie / 垂直 SaaS):** Box 的 Levie**承认座席定价会死,但否认 SaaS 会死**——软件难不在 UI,而在"编码了业务流程、合规、运营现实",这些不会消失;agent 反而**需要**上下文和数据,他预测"agent 数量是人的 100 到 1000 倍",所以软件要"无头化(headless,可被 agent 调用)"——这杀死按座席、却放大用量。

**调和(本报告的立场):agent 杀死"界面护城河",但加深"数据+系统-of-record+治理护城河"。** 输家是把价值押在"人类界面 + 按座席收费 + 可导入的通用数据"上的软件;赢家是拥有"agent 必须经由它行动的数据/SoR/治理基底"、且已按消耗/结果计价的软件。**Klarna 案例双向证明了天花板:** 它一度宣称 AI 替掉 700 个客服、砍掉 Salesforce/Workday,后来又**回招人**承认"质量天花板"——routine 高频低风险的活儿成本崩塌是真的,但全自动在有责任/品牌成本的活儿上有质量上限。**这是整个颠覆论最重要的"调速器"。**

---

## 第二部分:生存 vs 淘汰框架(7 维评分 rubric)

每维 0(AI 暴露)到 2(AI 占优)。合计 10+/14 = AI 赋能(agent 放大它);低于约 6 = AI 被颠覆(agent 绕过它或把座席压到零)。

| # | 维度 | 0 分(暴露) | 2 分(占优) |
|---|---|---|---|
| 1 | **专有数据/"轨迹"护城河** | 通用、可导入的数据 | 独家生成的数据 + "活儿是怎么干的"记录(可喂 RL/微调) |
| 2 | **系统-of-record + 工作流锁定** | 流程便利工具 | 权威 SoR,带合规/权限逻辑 |
| 3 | **受监管/任务关键** | 自由裁量、低风险 | 受审计/监管、出错代价高 |
| 4 | **核心活儿能否被 agent 自动化** | 产品=可自动化的活儿本身 | 产品是 agent 仍需要的编排/治理 |
| 5 | **计价模式暴露** | 纯按可自动化的座席收费 | 已按消耗/结果/agent 计价 |
| 6 | **分发/装机基盘** | 每轮都要重新赢新客 | 拥有渠道/装机,把 agent 叠上去 |
| 7 | **集成深度("薄壳"测试)** | 薄 LLM 套壳,易复制 | 深度多系统集成,高转换成本 |

> **一句话压缩成一个最关键问题:这个软件的核心活儿,是"按人头座席收费去执行可被自动化的劳动",还是"做那个受信任、受监管、拥有数据、agent 必须经由它行动的基底"?** 前者死或剧烈重定价;后者随 agent 用量爆发而更值钱。

---

## 第三部分:收费/商业模式前瞻(这是核心 —— 谁卡位)

**为什么按座席定价被结构性威胁:** 按座席=假设一个人对应一个许可证。当 agent 把活儿干了,**人数下降而工作量上升**——按座席的收入随人头缩水,哪怕交付的价值在涨。硬证据:客服 deflection 60 到 80%(Decagon 约 80%、Intercom Fin 67%);GitHub Copilot 2026/6/1 转**消耗计价**(在位者亲口承认按座席的经济学崩了);微软 Nadella(FY26 Q3)"我们任何按人头的业务,都会变成按人头**且按用量**"。

**未来模式 = 三层 settle-out:**
1. **缩水的"人类座席基线"**(监督 agent 的人);
2. **计量消耗**(token/算力/动作)——随 agent 活动量增长;
3. **结果/agent 定价**(每解决一张工单、每成一单)。

**谁卡位最好(已按消耗/take-rate 计价 = 顺风;纯座席 = 逆风):**
- **顺风(用量越大收入越多):** Snowflake、Databricks、Datadog、Cloudflare、Twilio、云三家、Shopify(GMV take-rate)、Toast、Klaviyo、ServiceNow(AI 当升级 SKU 卖)。
- **逆风(座席+可自动化):** Asana、Zendesk、Smartsheet、Okta/Zscaler(per-seat 安全)、以及任何"座席=可自动化的活儿"的应用。
- **转型中(波动):** Salesforce(转 Agentforce 消耗/AELA)、Workday(按人头=最差暴露,转 Flex Credits)、HubSpot(已转结果定价,基本中和)、Adobe(座席+信用对冲)、微软(座席+Azure 消耗两头通吃)。

**但消耗计价是把双刃剑,别把它当无脑利好:** ①**token / 算力价格在持续通缩**——同样的活儿,客户明年付的钱可能更少(单价跌得比用量涨得快,收入就缩);②**客户会主动优化用量**(缓存、用更小的模型、砍冗余调用),消耗收入因此可能"先冲高、后回落"。历史上的反例就是 Twilio:消耗模式在客户优化短信 / 验证用量时,NRR 一度跌破 100%。**所以"已转消耗"是必要条件、不是充分条件——还要看这家的消耗是不是绑在"会持续放量、且不易被优化掉"的刚性工作负载上**(这也是为什么我更偏"监控 / 安全 / 数据这类越用越多、且砍不掉"的消耗,而非"可被压缩的 API 调用")。

---

## 第四部分:全行业 mapping(受益 / 中性 / 被杀,逐名)

### A. AI 赋能 —— 护城河随 AI 加深(durable 赢家)
| 公司 | 为什么赋能 | 关键证据 |
|---|---|---|
| **Microsoft** | 平台:既卖铲子(Azure+模型)又卖应用;座席通缩用 Copilot+Azure 消耗两头通吃 | AI 业务年化 $370 亿(+123%);Copilot 座席 2000 万(+33% 环比) |
| **ServiceNow** | 横向 SoR + AI 编排层;AI 当升级 SKU 卖,不是被蚕食 | Now Assist ACV 上调到 $15 亿;$1M+ AI 客户 +130% |
| **CrowdStrike / Palo Alto** | 安全=最 AI-durable 品类(AI 扩大攻击面、关键任务、非自由裁量);整合者 | CRWD ARR $52.5 亿/+24%、Flex 消耗;PANW NGS ARR +56%、$250 亿买 CyberArk=agent 身份 |
| **Snowflake / Databricks** | 数据重力:AI 需要数据;纯消耗;agent 查询/向量都烧 credit | SNOW 产品收入 +34% 加速、NRR 升到 126%;Databricks >65%、AI ARR $14 亿(2H26 IPO) |
| **Datadog** | "AI 越多、要监控的东西越多";纯消耗;不管谁赢都受益的中立铲子 | +32% 加速、ARR >$40 亿;风险=OpenAI 集中度约 10% |
| **Palantir** | AI 部署/本体(ontology)层:把模型变成生产级 agentic 工作流 | 收入 +85%、US 商业 +133%(争议全在估值) |
| **Shopify / Toast** | take-rate 模式:商家提效→GMV→公司收入;agentic 商务是增量 | SHOP +34%、GMV +35%;Toast +22% |
| **Veeva** | 受监管垂直数据护城河;还在抢 Salesforce 份额 | +16%;Vault CRM 抢 10/前 20 大药企 |
| **Atlassian / JFrog** | 开发系统-of-record + AI 信用升级(反驳开发座席萎缩) | TEAM 云 +29% 加速、NRR>120%;FROG 云 +50%、NDR 120% |
| **Twilio / Cloudflare** | 消耗定价;agent 是它们产品的净消费者 | TWLO NRR 升到 114%;NET +34%、agentic 边缘 |
| **SAP** | ERP=最不可自动化的 SoR;AI(Joule)是迁移加速器 | 云 +27% cc;Joule 进 30% 的单 |

### B. 中性 / 硬币 —— 握 SoR 但座席暴露大,看转型
| 公司 | 张力 |
|---|---|
| **Salesforce** | 握 CRM SoR + Agentforce $34 亿 ARR(+200%),但座席暴露大、订阅增速降到 8-9%;转消耗是关键 |
| **Adobe** | Firefly 信用变现 +75% QoQ vs Canva/Midjourney/Sora 民主化——真正的 coin-flip;"AI 幸存者,非 AI 赢家" |
| **Workday** | 按人头计价=最差座席暴露 + Klarna 伤疤;转 Flex Credits 缓解 |
| **HubSpot** | 已主动把座席依赖拆掉、转结果定价($0.5/解决),+23%——基本中和 |
| **Figma** | +46%、AI 反而扩座席——其实偏赋能(反驳"AI 杀设计") |
| **Monday** | 座席但 +24%,平台广度顶住;Asana 是反例 |
| **GitLab / 微软GitHub** | 开发 SoR durable,但增速降、AI 变现尚早(GitLab);微软"受益但转守" |

### C. 被杀 —— 财报里已经在流血(按"已兑现的颠覆"排序)
| 排名 | 公司 | 机制 | 硬证据 | 状态 |
|:-:|---|---|---|---|
| 1 | **Chegg (CHGG)** | 免费 LLM + 谷歌 AI 概览毁掉产品+入口 | 收入 **-48% YoY**、股价约 $1、距峰值 -99% | **已死(机制铁证)** |
| 2 | **ZoomInfo (ZI)** | LLM+爬虫把"联系人记录"价格打到零,数据垄断租金归零 | 单日 -29%、FY26 收入指引 -4%、**NRR 90%**、裁 600 人 | **正在流血** |
| 3 | **Gartner (IT)** | LLM 去中介化辛迪加研究("问 AI"替代分析师电话) | 一年 -64%、合同价增速连 4 季 8%→1%、证券集体诉讼 | **正在流血,Chegg 翻版** |
| 4 | **C3.ai (AI)** | 前-LLM 时代的"AI"厂商被 LLM 浪潮淘汰 | 收入 -19%、**撤回全年指引**、CEO 动荡 | **自伤+过时** |
| 5 | **UiPath (PATH)** | agent 让脆弱的"屏幕抓取"RPA 过时 | **NRR 120%→107%**、AI 仅占 ARR $2 亿、管理层称"对 FY26 不重要" | **缓慢结构性侵蚀** |
| 6 | **Asana (ASAN)** | 纯座席工作管理;AI 缩知识工人人头=缩座席 TAM | **NRR 96%(基盘在缩)**、+9%、AI Studio 仅 $600 万 ARR、股价 2026 -50% | **座席挤压,真实** |
| 7 | **Sprout Social (SPT)** | 社媒管理被 AI 内容/agent 商品化 | 指引降到 +9-10%(2023 还 31%)、NRR 降到 100% | **减速、脆弱** |
| 8 | **Dropbox (DBX)** | 存储工具被 Glean/AI 知识层去中介 | 收入 +0.8%(约持平)、靠回购撑 EPS | **停滞(非崩塌)** |

---

## 第五部分:关键纠偏 —— 头条颠覆 vs 财报颠覆 + Klarna 天花板

**最容易犯的错:把头条最响的颠覆当成正在发生的颠覆。** 注意上面"被杀名单"里**没有** Zendesk/NICE/Five9/Twilio/Salesforce——这些"接触中心/CRM 被 Sierra/Cursor 杀"的故事,在 listed 在位者的财报里**还没兑现**(它们自己的 AI 线是增长最快的)。真正流血的(ZI/Gartner/Chegg/Asana)是另一种 DNA:**卖"数据/内容垄断"或"纯座席"**,被 LLM 直接商品化。

- **AI 原生颠覆者增长最快的两个品类:编程(Cursor 约 $20 亿 ARR、Claude Code 约 $25 亿)和客服(Sierra+Decagon+Fin 合计约 $3.85 亿 ARR,结果定价)。** 但"颠覆者增长最快"≠"在位者受损最快"——这两类里 listed 在位者都在 co-opt(吸收)这波。
- **被高估的空头(threat overstated):** 接触中心(NICE AI ARR +66%)、法律(RELX/Thomson Reuters 的 corpus 是 Harvey 必须授权的,两家 AI 驱动双位数增长;RELX 甚至投资了 EvenUp)、Salesforce/HubSpot/Figma(agent 必须写回它们的 SoR)。
- **真正会咬的两个空头(高 conviction):数据垄断去中介(ZoomInfo、Gartner)+ 纯座席 TAM 压缩(Asana,慢慢轮到 UiPath)。**
- **Klarna 天花板:** 替掉约 700 客服后回招人——任何有责任/品牌成本的活儿(客服升级、法律、财务、医疗),全自动 agent 有质量上限。这是整个颠覆论的调速器,多头系统性忽略它。

**一个重要的"铲子"警示(来自数据基础设施研究):Pinecone(纯向量数据库)崩了**(ARR $2660 万→$1400 万、在找买家)——**说明"AI 原语"会被有数据重力+分发的平台做成"功能"而非"产品"。** 利好平台(Snowflake/MongoDB/Datadog),利空单一功能创业公司。

---

## 第六部分:Top 5(不看估值,只看天花板×质量×卡位×资源×赋能而非替代×捕获 AI)

按你的标准——纯从"行业天花板 + 公司质量 + 卡位 + 手上资源 + 被替代还是被赋能 + 是否 well-positioned to capture AI + 前瞻收费模式"——我选这 5 家。**(明确三件事:①这是"质量×卡位"排序,不是"现在该按这个价买入"——估值/入场点见第七部分;②我把初稿里的 Snowflake、Palantir 从 Top 5 降到荣誉席,理由是商业模式/竞争而非估值,下面讲清楚;③这 5 家的共同点是:要么拥有 agent 必须经由它的模型/数据/SoR/治理基底,要么按消耗计价直接吃到 agent 用量爆发。)**

### 🥇 1. Microsoft(MSFT)—— 唯一同时拥有模型、云、应用、开发、安全、身份的平台
- **天花板/卡位:** 它不在某一层竞争,它**拥有整个栈**——Azure(托管 OpenAI+Anthropic 模型)、Windows、M365/Copilot、GitHub、安全、Entra 身份。Nadella 说"软件吃劳动力"的 $13 万亿 TAM,微软站在最好的位置去捕获。
- **赋能而非替代 + 收费模式:** **它是唯一能把"座席通缩"两头通吃的公司**——人少了用 Copilot 升级 + Azure 消耗补上;已明确转"按人头且按用量"。AI 业务年化 $370 亿(+123%)。
- **资源:** 资产负债表、模型准入、分发,全软件业第一。**最确定、最 well-positioned。**

### 🥈 2. Alphabet / Google(GOOGL)—— 公开市场里最可拥有的"模型层 + 云 + 芯片 + 分发"全栈
- **为什么补进来(初稿漏了它,这是最大的纠偏):** 整篇报告的核心结论是"价值正从应用层上移到模型层"——但模型层的最终归属(Anthropic / OpenAI)大多买不到。**Google 是唯一一个公开市场就能买到的、自有前沿模型(Gemini)+ 自有云(GCP)+ 自有 AI 芯片(TPU,不看英伟达脸色)+ 三个十亿级分发入口(搜索 / 安卓 / YouTube)的全栈赢家。** 论"拥有 agent 时代最稀缺那一层 + 有资源和分发去捕获",它和微软是仅有的两家。
- **必须正面回答的张力(否则自相矛盾):** 本报告把"搜索被 AI 去中介"列为 Chegg / Gartner 的死因——那 Google 的搜索不也危险吗?**答案:Google 是少数能"自己把自己去中介、再用 AI 答案重新变现"的公司**——AI Overviews 已铺到主搜索、Gemini 月活破数亿、且它握着被颠覆者没有的东西(云 + 模型 + 芯片 + 数据闭环)。它面对的是"利润率结构变化"风险,不是 Chegg 那种"产品被整个抹掉"的存亡风险。
- **赋能 + 资源:** 自研 TPU 让它的 AI 单位成本结构是全行业最优之一(不付英伟达的"过路费");Cloud 增速重新加速、Gemini 在重写搜索 query 的变现方式。**论"被赋能而非被替代 + capture AI 的资源",它还是 Top 5 里估值最不极端的一个(虽说你让我别看估值)。**

### 🥉 3. ServiceNow(NOW)—— 企业 agent 的横向工作流 SoR(护城河是"数据/权限/审计",不是"界面")
- **天花板/卡位:** agent 要在企业里跨 IT/HR/客服干活,需要一个带合规、权限、审计轨迹的工作流 SoR 去读写——这正是 ServiceNow 卖的,它把自己定位成"企业 AI 的编排层"。
- **一个必须收窄的论点(红队纠偏):把 Nadella 的逻辑对称地用在它身上**——如果"业务逻辑会上移到 AI 层",那 ServiceNow **可被替代的部分恰恰是"工作流编排 / 界面"**(agent 自己也能编排),真正 durable 的是它底下的**配置管理数据库(CMDB)、身份 / 权限、审计记录**这些 agent 绕不过去的 SoR 数据。**所以它进 Top 5 的理由要钉在"它拥有那层数据",而不是"它的 UI 好用"。**
- **赋能 + 收费:** AI 当**升级 SKU** 卖(Now Assist ACV 上调到 $15 亿、$1M+ AI 客户 +130%)——AI 是加价,不是蚕食;订阅 +22% 还在加速。

### 🏅 4. CrowdStrike(CRWD)—— 押"最 AI-durable 的品类:安全"
- **天花板/卡位:** 安全是公开市场最 AI-durable 的品类——**AI 扩大了它要卖的问题**(每个 agent 都是新攻击面 + 需治理的非人类身份),且是关键任务/受监管/非自由裁量(提效也不砍预算)。CrowdStrike 单 agent 数据图谱 + Falcon Flex 消耗 + Charlotte AgentWorks(agent 治理)= 整合者。
- **赋能 + 收费:** Flex 消耗承诺把它从座席风险里隔离;ARR $52.5 亿(+24%)、NRR 115%、Flex ARR +120%。
- **为什么是它(vs Palo Alto):** 数据护城河 + 单 agent 架构最纯;Palo Alto(买 CyberArk=agent 身份最直接玩法)是同样强的第二选择,二选一看你更信"端点+SOC 数据图谱"还是"平台化+身份"。

### 🏅 5. Datadog(DDOG)—— 不管谁赢都受益的"中立铲子",纯消耗计价
- **为什么是它,而不是 Snowflake:** 数据 / 基础设施这一层我要的是**最干净的消耗逻辑 + 最中立的卡位**。Datadog 卖的是可观测性(observability,监控软件 / AI 跑得好不好)——**"AI 部署得越多、要监控的东西就越多",不管最后是 OpenAI 还是 Anthropic、是 Snowflake 还是 Databricks 赢,监控的账单都在涨**;且基本按用量计价,是"agent = 机器级用量爆发"的直接受益者。+32% 加速、ARR 破 $40 亿。
- **赋能 + 收费 + 诚实风险:** 纯消耗 = 顺风;风险是 OpenAI 单一大客户约占 10%(集中度),以及消耗计价的双刃(客户会主动优化用量、token 价格在通缩)。但论"中立、不赌哪家模型赢、whoever wins 都吃到",它比 Snowflake 干净。

> **为什么把 Snowflake 和 Palantir 从初稿 Top 5 降到荣誉席(讲清楚):**
> - **Snowflake** 仍是好公司(产品收入 +34% 加速、NRR 126%、$60 亿 AWS 大单),但"数据层"这个名额我更想要中立铲子(Datadog),因为**连本报告都承认 Databricks(私有、>65% 增长、AI ARR $14 亿、2H26 IPO)在 AI-数据工作负载上赢得更快**,且开放湖仓格式 Iceberg 在侵蚀它的存储护城河。数据层最强的牌可能是还没上市的 Databricks——**与其现在锁定 Snowflake,不如把这一票留给 Databricks 的 IPO**,Datadog 作"中立、已上市、whoever-wins"的占位。
> - **Palantir** 论天花板 / offense / 卡位其实够格(收入 +85%、US 商业 +133%、本体层是"AI 落地"最纯的赢家),我降它**不是因为估值**(你让我别看)——而是因为它的**商业模式偏 bookings / 服务、lumpy,不是这套筛子要的"纯消耗铲子"**,且收入集中度高。**如果你给"最高 offense / 天花板"最大权重,Palantir 就是毫无争议的第 6 名、随时换得进来。**

> **Top 5 一句话:Microsoft(平台通吃)+ Google(最可拥有的模型层 + 云 + 芯片 + 分发)+ ServiceNow(横向工作流 SoR,押它的数据不是界面)+ CrowdStrike(最 durable 的安全)+ Datadog(whoever-wins 的中立消耗铲子)。** 共同点:要么拥有 agent 必须经由它的模型 / 数据 / SoR / 治理基底,要么按消耗计价吃到 agent 用量爆发,且都有资源和卡位去**捕获**而非被捕获。
>
> **荣誉席(很强、可进可出,按风格切换):Palantir(最高 offense)、Snowflake(数据重力)、Shopify(take-rate 商务)、Veeva(受监管垂直数据、最抗跌)、Atlassian、Cloudflare、Palo Alto;私有里盯 Databricks(2H26 IPO 会重设数据层估值锚)+ 模型层(Anthropic / OpenAI 才是编程 / 客服价值的最终归属)。**
>
> **一个贯穿 Top 5 的新风险(开放权重模型):** 如果开源 / 开放权重模型(Llama、DeepSeek、Qwen 等)持续逼近前沿,**模型层本身会被商品化**——这会削弱"价值上移到模型层"的论点(利空纯模型租金,中性偏利好拥有数据 / 分发 / SoR 的应用层和铲子)。这是 Google 这一票最大的反方风险,也是为什么 Top 5 里只放一个纯模型层敞口。

---

## 第七部分:投资时点 —— 你的"硬件褪去、软件接棒"判断对吗?

**你的观点(软件估值被杀很久、现在低位;硬件热潮褪去后软件接棒、有巨大机会)——方向我同意,但要加一个关键纠偏:**
- **"便宜的软件"分两种,千万别买错:** 被 AI 结构性颠覆的软件(座席/数据垄断:ZoomInfo、Gartner、Asana、UiPath、Chegg)便宜是**价值陷阱**——它们便宜是因为终局在缩;而 AI 赋能的赢家(上面 Top 5 + 荣誉席)**大多并不便宜**,但那才是该布局的地方。**别把"低估值"和"好公司"混为一谈——在 AI 时代这俩经常是反的。**
- **时点逻辑是一个"情景",不是机械规律(必须说清楚):** "硬件消化 → 钱轮动进软件"是一个**合理的、有历史基础的情景**,不是必然——硬件 capex 一旦消化,钱也可能去现金 / 债 / 或整个风险资产一起 de-rate(软件跟着杀),不保证乖乖轮进软件。**所以正确的姿势是"看到兑现信号再加仓",而不是"赌一个轮动时点"。** 当硬件 capex 出现消化期(我们在电力 / 光通讯 / 存储 memo 里反复指出的 2026–27 风险)、且下面的兑现信号同时出现时,才是 AI 赋能赢家(Top 5)最好的分批建仓窗口——**而不是去抄被颠覆者的"便宜"。**
- **要盯的兑现信号(软件接棒的发令枪):** ①AI 收入从"实验性 ERR(Experimental Run Rate)"转成"可续费 ARR"(看 NRR 是否随 AI 上升,而非靠座席);②座席→消耗/结果定价的转换是否带来净扩张(微软/Salesforce/HubSpot 的口径);③在位者 SoR 上的 agent 用量是否真变现(ServiceNow Now Assist、Salesforce Agentforce 的"净新增 vs 替代"拆分)。

---

## 第八部分:看空 / 风险与诚实的边界

1. **私有颠覆者的 ARR 是创始人/VC 营销口径、未经审计**(Sierra "$1.5 亿"、Cursor "$20 亿");结果型 ARR 比座席 ARR 更 lumpy、留存未经一个完整续费周期检验——打折看。
2. **在位者没有披露 NRR 里"座席流失 vs 提价/扩张"的拆分**——我们还看不到 Salesforce/Asana 的座席数是否在头条 NRR 底下悄悄缩。这是最大的未观测变量。
3. **AI 收入跨公司不可比**:只有 Databricks 给了硬 AI-ARR($14 亿);其余多为定性或"AI 集成客户占比"(高估了 AI 驱动的收入)。
4. **Klarna 天花板 vs a16z 的 $13 万亿**:服务即软件的 TAM 是真的、但更 lumpy、利润率更低、客服成本更重——扩 TAM、但收入质量下降。
5. **开放权重模型(open-weights)是对整套论点的系统性风险:** 如果 Llama / DeepSeek / Qwen 等持续逼近前沿,模型层会被商品化——利空"价值上移到模型层"的论点(尤其 Google 那一票),但中性偏利好拥有数据 / 分发 / SoR 的应用层和铲子。**这是 Top 5 里唯一只放一个纯模型层敞口的原因。**
6. **本报告是综合既有研究 + 大佬观点的战略判断,估值/数字为 5 月口径,需终端复核;多处私有数据为二手。**

---

## 附:本报告术语速查
| 名词 | 大白话 |
|---|---|
| SaaS | 软件即服务,按订阅/座席收费 |
| agent / agentic AI | AI 智能体,能自主完成多步任务 |
| system of record (SoR) | 系统-of-record,某类企业数据的权威存放+流转中枢(CRM/ERP/HR) |
| 座席定价 / 消耗定价 / 结果定价 | 按人头 / 按用量(token、动作)/ 按成果(每解决一单)收费 |
| NRR / 净收入留存 | 老客户今年比去年多付还是少付;<100% = 基盘在缩(座席萎缩的铁证) |
| ERR | Experimental Run Rate,实验性(非可续费)AI 收入,脆弱 |
| 数据重力 | 数据越多越吸引应用和计算聚拢,形成护城河 |
| 向量数据库 / RAG | 存"语义向量"供 AI 检索;检索增强生成 |
| take-rate | 平台按交易额抽成(Shopify/Toast),非按座席 |
| 去中介化 | 某环节被技术绕过、价值被拿走 |
| ontology(本体) | Palantir 给企业数据/流程/决策建的"语义地图" |
| 卡位 | 在产业链/价值链里占据的战略位置 |

---

## 资料来源(关键,按主题)
**战略框架/大佬:** Nadella(BG2 播客 2024/12;微软 FY26 Q3 "按人头且按用量");a16z(Rampell"软件吃劳动力"2025/10;Casado"AI 颠覆 SaaS 定价");Sequoia("$600B 问题"、"生成式 AI 第二幕/推理时代");Aaron Levie(TechCrunch/Axios 2025"agent 需要上下文、软件要无头化");Jamin Ball(Clouded Judgement"按座席定价之死"、ERR);Tomasz Tunguz("轨迹成为新护城河"、纯工作流工具 -39%);Bessemer(State of AI 2025);Gergely Orosz(Claude Code 数月内超越 Copilot/Cursor);Klarna(砍 Salesforce/Workday 后回招人,Entrepreneur/CX Today/SEC 6-K)。
**应用 SaaS:** 各家 Q1-CY2026/最新季 8-K 与电话会(MSFT、ServiceNow、Salesforce、Adobe、SAP、Workday、HubSpot、Atlassian、Shopify、Veeva、Toast、Procore、Klaviyo、Monday、Asana、DocuSign、Dropbox、Twilio、Intuit、Figma)。
**数据基础设施:** Datadog Q1'26(+32%、ARR>$40 亿、OpenAI 约 10% 集中);Snowflake Q1 FY27(产品 +34%、NRR 126%、$60 亿 AWS);Databricks(>65%、$54 亿运行率、AI ARR $14 亿、2H26 S-1);MongoDB/Cloudflare/Elastic/Palantir/Teradata;Pinecone(ARR 崩、找买家);Confluent 被 IBM $110 亿收购。
**安全+开发工具:** CrowdStrike(ARR $52.5 亿/+24%、Charlotte AgentWorks)、Palo Alto(NGS +56%、$250 亿买 CyberArk)、Google $320 亿买 Wiz、Zscaler/Fortinet/SentinelOne/Okta;GitHub 转消耗(2026/6)、GitLab/Atlassian/JFrog;颠覆者 Cursor/Claude Code/Cognition/Replit/Vercel。
**AI 原生颠覆者/被杀名单:** Sierra($158 亿估值)/Decagon/Intercom Fin;Harvey($110 亿)/EvenUp(RELX 投资);Chegg(-48%)、ZoomInfo(NRR 90%)、Gartner(合同价 8%→1%、诉讼)、C3.ai、UiPath(NRR→107%)、Asana(NRR→96%)、Sprout、Dropbox;Klarna 回招人(质量天花板)。
