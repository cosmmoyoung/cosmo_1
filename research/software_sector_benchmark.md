# 全软件板块 AI 时代对标 benchmark —— 谁是 winner,谁是 loser(2026 年 5 月)

### 一张表看清:每家软件公司的业务本质、长期竞争力、财务指标、最新动态与 AI 判定
*作者:资深买方分析师*
*日期:2026 年 5 月 28 日。本表综合 4 路并行深度研究(平台+数据基础设施 / 应用 SaaS / 安全+开发工具 / 垂直+AI原生+通讯+被颠覆者),覆盖约 50 家上市与重点私有公司。所有数字均为各公司"最新已报告季度"(多为日历 2026 Q1 或对应财年季);margin 标注 GAAP / non-GAAP;私有 ARR 为未经审计的创始人/VC 口径。市值/估值为 5 月口径,需终端复核。沿用大白话标准、不用波浪号。*

> **这份报告回答一件事:在 AI(尤其 agent)趋势下,把每一家软件公司摊开来比——它到底做什么、长期有没有竞争力、增速/margin/模式/天花板各是什么、现在是"在增、margin 在提"还是"在被替代、在 defend",最后给一个鲜明的 winner/loser 分层。**

---

## 第〇部分:怎么读这张表(3 句话方法论)

> **1. 最锋利的判别规则:收入随"机器工作量 / 交易额 / 数据量"增长 = AI 受益;收入随"人类座席数"增长 = AI 被威胁。** AI 的目的就是减少人头——对前者顺风,对后者逆风。

> **2. NRR(净收入留存)是照妖镜。** 老客户今年比去年多付(NRR>110% 且在升)= AI 在帮它扩钱包;NRR 跌穿 100%(如 Asana 95%、ZoomInfo 90%)= 座席/数据在被侵蚀,藏不住。**但要小心:NRR 会被"涨价掩盖座席流失"美化,且财报滞后颠覆 12–24 个月——所以也要看 GRR(毛留存)和增速方向。**

> **3. 区分"财报颠覆"和"头条颠覆"。** 真正流血的(Chegg -48%、ZoomInfo NRR 90%、C3.ai 约 -46%)是"数据/内容垄断被去中介"或"纯座席被压缩";而头条最响的"Sierra 杀客服、Cursor 杀开发工具"——在多数上市在位者的财报里**还没兑现**(Five9 AI 收入 +68%、NICE AI ARR +66%、Twilio NRR 回到 114% 都在反驳)。**投资押财报,不押头条。**

**评级图例(winner→loser 五层):**
- 🟢 **核心赢家**:AI 赋能、增速加速、护城河 durable、有资源捕获 AI。
- 🔵 **稳健受益**:AI 赋能,但弹性略低或带一个 caveat。
- 🟡 **中性/硬币**:被争议,看执行;在 defend 但还没流血。
- 🟠 **承压/防守**:慢增长/座席暴露/融冰,靠 FCF + 回购续命。
- 🔴 **被颠覆/输家**:财报里已经在流血。

---

## 第一部分:一页纸结论 —— winner/loser 分层

> **重要:这是"质量×卡位"的分层,不是"按此价买入"的分层——两件事分开。** 所以单设一格区分"质地顶级但价格不过关"的名字(避免把 Palantir-97× 和 Google-29× 当成同一个 call)。每个 🟢 也都带了它最致命的那个 caveat,不给"无脑安全"的错觉。

| 层级 | 公司(按板块) |
|---|---|
| 🟢 **核心赢家** | Microsoft(带 capex/折旧压 margin caveat)、Alphabet/Google(带 open-weights + 搜索去中介 caveat)、Amazon(AWS)、Datadog(带云厂自带监控整合 caveat)、CrowdStrike、ServiceNow(带"净新增 vs 替代"未拆分 caveat)、Atlassian、Figma、Shopify、Veeva;**私有:Databricks** |
| 🟢\* **质地顶级、但价格不过关(quality-yes / price-no)** | **Palantir**(质地是 🟢、估值是 🔴:约 97× 前瞻、距高点 -34%,risk-adjusted 实为 🟡;见 §2.7 + `software_ai_era_deepdive.md` PEG 陷阱) |
| 🔵 **稳健受益** | **Snowflake**(带数据重力被 Iceberg/Databricks 侵蚀的 caveat,故未进 🟢)、Palo Alto、Fortinet、JFrog、HubSpot、Intuit、SAP、Klaviyo、Toast、Samsara、Twilio、MongoDB、Cloudflare、Oracle(带资产负债表/RPO 质量 caveat) |
| 🟡 **中性/硬币** | Salesforce、Workday、Adobe(便宜的逆向期权,见 §3)、Monday、SentinelOne、Zscaler、Okta、GitHub/Copilot、Elastic、Five9、NICE、DocuSign |
| 🟠 **承压/防守** | GitLab、Asana、Zoom、RingCentral、Dropbox、Sprout Social、UiPath、Gartner(早期去中介、核心研究仍 +5%,比另两个 🔴 轻) |
| 🔴 **被颠覆/输家** | Chegg、ZoomInfo、C3.ai |

> **一句话总览:价值正从"人类界面/按座席收费"流向"模型 + 数据 + 系统-of-record + 治理基底 + 按消耗/交易计价"。** 拥有后者的(超大规模云、数据层、安全、横向 SoR、垂直专有数据、take-rate 商务)是赢家;只卖"人类界面 + 通用数据 + 纯座席"的是输家。
>
> **但要诚实:"平台/数据/安全最安全"本身就是卖方共识。** 真正能赚钱的是变体观点(见 §3 末):做多被错杀的 Adobe、对"独立层被云厂整合"保持警惕(Datadog/Snowflake)、以及不把 Palantir 的高倍数当便宜。**这张表的价值不在"附和共识",而在标出哪里共识可能错。**

---

## 第二部分:分板块 benchmark

> 表内:增速=最新季 YoY 及方向(加速/减速/稳);margin=方向(升/降/平)+ 水平;模式=seat 座席 / consumption 消耗 / outcome 结果 / take-rate 抽成 / hybrid 混合。

### 2.1 平台 / 超大规模云(模型 + 云 + 分发,最稀缺那一层)

| 公司 | 业务本质 | 增速 | margin | 模式 | AI判定·评级 |
|---|---|---|---|---|---|
| **Microsoft** | 企业软件+Azure 云+M365/Copilot | +18%(Azure +40%,加速) | op约45% GAAP,升(capex 压 FCF) | hybrid 座席+消耗 | 🟢 AI 赋能:Azure 是推理铁轨,AI 直接拉消耗 |
| **Alphabet/Google** | 搜索/广告+GCP 云+Gemini | +22%(Cloud +63%,加速) | op 36% GAAP,升;Cloud 利润率 18→33% | take-rate+消耗 | 🟢 AI 赋能(TPU+Gemini);搜索有去中介尾部风险 |
| **Amazon/AWS** | 电商+AWS 云+广告 | +17%(AWS +28%,15 季最快) | AWS op 37.7%;整体 op 13% 升 | 消耗+take-rate | 🟢 AI 赋能:AWS+自研 Trainium 吃推理 |
| **Oracle** | 老 DB/ERP 转 OCI 云,AI-GPU 房东 | +22%(OCI infra +84%) | non-GAAP EPS +21%,**但 FCF 被 capex/债压** | license+消耗 | 🔵 AI 赋能,**但 RPO $553B 质量存疑(低毛利 GPU 租赁、预付撑)+ 客户集中** |

- **天花板:** 全企业 IT + AI 基础设施,最大、还在扩。**估值:** MSFT 约 22× 前瞻、GOOGL 约 29× trailing(最不贵)、AMZN 约 28× 前瞻、ORCL 约 25× 前瞻。
- **点评:** 这一层是"AI 时代最稀缺的模型+云+分发",**微软/谷歌/亚马逊三家是全软件最确定的赢家**(都在加速 + margin 在升)。但"最确定"不等于"无风险",每家带一个 caveat,别 mega-cap 抱团:
  - **Microsoft:** AI 年化约 $370 亿对约 $2700 亿收入,需求是否真增厚 margin、还是在用 Copilot 打包"送"出去保座席,尚待观察;**更关键的是约 $800 亿/年 capex 带来的折旧大坡 FY27–28 会压 GAAP 经营利润率**——"margin 在升"是当下、不是已锁定的未来。
  - **Alphabet/Google:** 两个真实尾部风险——**① open-weights 模型(Llama/DeepSeek/Qwen)若逼平前沿,模型层被商品化,削弱它最值钱的那一层;② 搜索被 AI 答案去中介**(它自己也是 Chegg/Gartner 死因的潜在对象,只是它有云+模型+芯片+数据闭环对冲)。所以 Google 是"🟢 带 caveat"。
  - **Oracle:** 用激进 capex + 举债抢 AI 房东生意,增速最猛但**是杠杆/低毛利的打法,质量最需警惕**。
  - **一条要守的纪律(避免双标):同样的"低毛利 GPU 产能 + 预付 + 客户集中"逻辑,不能只用来质疑 Oracle、却给三巨头免检。** 三巨头也在签低毛利 AI 产能大单(本表 §2.2 赞许引用的 Snowflake-on-AWS $60 亿大单就是一例)。区别是三巨头有高毛利基本盘 + 资产负债表去吸收,Oracle 是赌上公司——**所以 ORCL 的 🔵 + 三巨头的 🟢 都应带同一个"RPO 质量 + 集中度"星号,只是程度不同。**

### 2.2 数据 / 基础设施(AI 的燃料与铲子)

| 公司 | 业务本质 | 增速 | margin | 模式 | NRR | AI判定·评级 |
|---|---|---|---|---|---|---|
| **Snowflake** | 云数据仓库/分析+Cortex AI | 产品 +34%(26→30→34,加速) | non-GAAP op 12%,升;FCF 23% | 消耗 | 126%(注) | 🔵 AI 赋能:每次 AI 查询都烧 credit;**但 Iceberg/Databricks 侵蚀护城河,故列 🔵 不列 🟢** |
| **Databricks**(私) | 湖仓数据+AI 平台(Snowflake 头号对手) | 跑率 >$54 亿 +65%,加速 | 私有未披露 | 消耗 | >140% | 🟢 最强 AI-数据纯玩:AI ARR $14 亿(占 26%) |
| **Datadog** | 云可观测性(监控)+ AI agent 监控 | +32%,微加速 | non-GAAP op 22%;FCF 29% | 消耗 | 低120% | 🟢 中立铲子(带 caveat):AI 越多越要监控;但云厂自带监控+高盛看空 |
| **MongoDB** | NoSQL 文档数据库(Atlas 云) | +27%(Atlas +29%);**FY27 指引 16–18% 减速** | non-GAAP op 22.9%,升 | 消耗+订阅 | 121% | 🔵 AI 赋能但受争议(向量库竞争);减速是隐忧 |
| **Cloudflare** | 边缘网络/CDN+安全+开发者平台 | +34% | non-GAAP op 11.4%(低);**裁员 20%** | hybrid 订阅+消耗 | 118% | 🔵 AI 赋能(边缘推理),但"边增长边重组",最贵(约28× EV/S) |
| **Elastic** | 搜索/可观测/安全(向量搜索) | +18%(FY 指引约 17%) | non-GAAP op 中高位,升 | hybrid | 约110% | 🟡 AI 赋能(RAG/向量),但增速平、不加速;Q4 今日才出 |

- **天花板:** AI 数据/分析/监控,大且扩。**已并购:Confluent(实时流数据)2026/3 被 IBM 以约 $110 亿收购,并入 IBM Software,不再独立。**
- **点评:** **Databricks / Datadog 是这一层最干净的两张牌**,Snowflake 紧随但带护城河 caveat。Databricks 是 AI-数据最强纯玩(但要等 2H26 IPO),Datadog 是中立铲子。**两个必须说清的裂缝:**
  - **(注)消耗模式的 NRR 会骗人:** Snowflake 的 126%、Datadog 的低 120% 在客户"上量"时会机械性虚高、在客户"优化用量"时会骤降(本表 §4 引的 Twilio 优化先例就是)。**所以别把消耗 NRR 当干净的扩张证据——要配 GRR(毛留存)和"消耗绑没绑刚性负载"一起看。**
  - **结构裂缝:开放湖仓格式 Iceberg 正在瓦解数据重力护城河**(企业可以"Databricks 做 ELT/ML + Snowflake 做 SQL 服务"跑在共享的 Iceberg-on-S3 上),"锁定"在变弱、治理层(Unity Catalog)成新战场。**这正是 Snowflake 只给 🔵 不给 🟢、且与我们 deepdive 把它降到荣誉席一致的原因。** MongoDB/Cloudflare/Elastic 是次一档(各有减速/低 margin/不加速的瑕疵)。
  - **还有一个被低估的对手:超大规模云自己。** Datadog 对手是 CloudWatch/Azure Monitor/GCP Ops、Snowflake/Databricks 的存算都跑在云厂上——**"卖铲人"和"卖地人"是同一批,独立层被云厂垂直整合(参照 Google 买 Wiz、Palo Alto 买 CyberArk)是这三家(Datadog/Snowflake/CrowdStrike)共同的中期风险。高盛对 Datadog 的看空就是这条。**

### 2.3 安全(最 AI-durable 的板块)

| 公司 | 业务本质 | 增速 | margin | 模式 | NRR | AI判定·评级 |
|---|---|---|---|---|---|---|
| **CrowdStrike** | 云原生端点/XDR+Falcon 平台 | ARR +24%,加速;净新增 ARR +47% | non-GAAP op 25%,升;FCF 29% | hybrid+Flex 消耗 | 115% | 🟢 AI 赋能:Charlotte AgentWorks 治理安全 agent |
| **Palo Alto** | 平台化安全(网络+云+SecOps+身份) | NGS ARR +33%(报表 +56% 含并购) | 约30% non-GAAP op,升 | hybrid→平台 | 119% | 🟢 AI 赋能;已收购 CyberArk(身份第 4 支柱) |
| **Fortinet** | 防火墙(ASIC 硬件)+SecOps/SASE | +20%(产品 +41%,billings +31% 加速) | non-GAAP op 36% 创纪录;FCF 约55% | hybrid | n/a | 🔵 AI 中性(硬件护城河,AI-resistant 也 AI-light);最便宜(约30×) |
| **SentinelOne** | AI 原生自主端点/XDR | +20%(ARR +22%,略减速) | op 转正,+600bps | hybrid | 109% | 🟡 AI 赋能但被 CRWD/微软挤(#3) |
| **Zscaler** | 零信任 SASE(安全上网/内网) | +25%(ARR +25%,略减速) | FCF 16%(偏软) | 主要 seat 座席 | n/a | 🟡 中性偏威胁:per-user 模式最暴露 |
| **Okta** | 身份与访问管理(IAM) | +12%(转 GAAP 盈利) | 利润率创纪录,但增速低 | seat 座席 IAM | n/a | 🟡 被威胁 or 转型:人座席压缩 vs 治理机器/agent 身份 |

- **天花板:** 约 $240B 安全支出、+12.5%/年扩张(Gartner);**agent 身份(non-human identity)是 AI 时代新品类。已并购:CyberArk(特权/机器身份)2026/2 被 Palo Alto 约 $250 亿收购;Wiz(云安全)2026/3 被 Google 约 $320 亿收购(Google 史上最大并购)。**
- **点评:** **安全是公开市场最 AI-durable 的板块**——AI 扩大攻击面 + 制造海量要治理的 agent 身份 = 净新增需求,不是座席替代。**但模式决定输赢:消耗/平台玩家赢**(CrowdStrike Flex、Palo Alto 平台化 + CyberArk),**纯按座席的承压**(Okta 人座席、Zscaler per-user,都减速到低双位/中 20%,靠盈利和"能不能抓住机器身份"续命)。Fortinet 是被低估的稳健现金牛(硬件 + 创纪录 margin + 最便宜)。

### 2.4 开发工具(AI 原生颠覆者正在吃整个品类)

| 公司 | 业务本质 | 增速 | margin | 模式 | NRR | AI判定·评级 |
|---|---|---|---|---|---|---|
| **GitHub/Copilot**(微软) | 代码托管+Copilot AI 助手 | 付费订阅约 +75%(ARR 估近 $10 亿) | 并入微软 | **seat→消耗(6/1 转 usage)** | n/a | 🔵/🟡 AI 赋能但被 Cursor/Claude Code 抢心智;靠分发护城河 |
| **JFrog** | 制品/二进制管理+软件供应链 | +26%(云 +50%,加速) | non-GAAP 盈利,升 | hybrid 消耗偏 | 120% | 🔵 AI 赋能:AI 越多越多制品/模型要存+管;座席暴露小 |
| **GitLab** | 一体化 DevSecOps 平台 | +23%(**FY27 指引 +15–17% 急减速**) | non-GAAP op 20.5%,升 | seat→usage(Duo 晚) | 118% | 🟠 被颠覆/co-opting:AI 进场晚、裁员 7%、股价腰斩 |
| **AI 原生(私)** | Cursor / Cognition / Replit / Vercel | Cursor ARR 约 $30 亿(4 月口径,史上最快) | 私有 | 消耗 | — | 🟢 颠覆者:在吃整个品类(见 §5) |

- **天花板:** 开发者工具,正被 AI 重定义。**点评:** 这是**两极分化最剧烈**的板块。**AI 原生颠覆者在吞噬品类**(Cursor 0→约 $30 亿 ARR 是史上最快、SpaceX 出 $600 亿期权收购该公司;Cognition/Devin $4.92 亿;据 Pragmatic Engineer 约千人调研,**Claude Code 8 个月从 0 干到第一、超过 Copilot 和 Cursor**)。座席制在位者 **GitLab 被颠覆/在 defend**(进场晚、急减速、裁员、股价腰斩)。**JFrog(制品/供应链消耗)和转消耗的 GitHub Copilot 是 co-opt 得更好的**——价值单位从"座席"转向"任务/token"。

### 2.5 横向应用 SaaS(NRR 照妖镜最灵的板块)

| 公司 | 业务本质 | 增速 | margin | 模式 | NRR | AI判定·评级 |
|---|---|---|---|---|---|---|
| **ServiceNow** | 跨 IT/HR 工作流平台(单一数据模型) | 订阅 +19%cc;cRPO +22.5% | non-GAAP op 32%;FCF 44% | hybrid+消耗加价 | 续约98% | 🟢 AI 加价者:Now Assist $15 亿 ACV 是净增不是蚕食 |
| **Atlassian** | 开发/IT 协作(Jira/Confluence)+Rovo | +32%,加速(Cloud +29%) | non-GAAP op 约25%;RPO +37% | hybrid+credits | **>120% 升** | 🟢 AI 加价者:Rovo 用户 ARR 增速约 2 倍 |
| **Figma** | 协作界面/产品设计+AI(Weave/Make) | **+46%,加速(最快)** | 毛利约90%;FY 指引约35% | seat+AI credits | **139%(最高)** | 🟢 AI 赋能:AI 扩大面与用户,NDR 139% 证明扩张非侵蚀 |
| **HubSpot** | 中小企业 CRM/营销/销售套件 | 订阅 +23% | non-GAAP op 17.8%,升 | seat→hybrid | 103% 升 | 🔵/🟢 AI 加价(早期):credits +67% QoQ,座席仍增 |
| **Intuit** | 中小/消费金融(QuickBooks/TurboTax) | +10%(指引上调 +13–14%) | 高 op;**裁员 17%** 增杠杆 | 订阅+交易 | n/a | 🔵/🟢 AI 赋能:"AI+人类专家"颠覆代账/报税,非座席 |
| **SAP** | 企业 ERP(S/4HANA 云) | 云 +27%cc;backlog +25%cc | 高 op | 订阅+消耗 | n/a | 🔵 AI 中性/赋能:ERP 是治理 SoR,agent 离不开它的数据 |
| **Monday** | 工作管理/无代码工作流 | +24% | 创纪录盈利 | seat+消耗 agent | 110%(>$50K 116%) | 🔵/🟡 AI 加价(早)/轻度座席风险 |
| **Salesforce** | CRM 系统-of-record+Agentforce | +13%(**有机约 8%,减速**) | non-GAAP op 34.8%,升 | **seat→AWU 消耗** | 淡化(约90 区间) | 🟡 自我颠覆:自砍客服 9000→5000,赛跑重新货币化 |
| **Workday** | 云 HCM+财务 ERP(人/钱 SoR) | +13% | non-GAAP op 31.8%,升;FCF 27.5% | **按人头座席** | 毛留98% | 🟡 被威胁(座席嫌疑):按员工数计价,客户裁员=座席缩 |
| **Adobe** | 创意(PS/Firefly)+文档+营销云 | +11–12% | 毛利约88%、op约45% | seat+AI credits | n/a | 🟡 被威胁但在变现:Firefly ARR >$2.5 亿 +75%QoQ;最便宜(约10×) |
| **Asana** | 工作管理/项目协作 | **+9%,减速(最慢)** | 首次 non-GAAP op 转正 | **seat 座席** | **95%(<100!)** | 🟠 被威胁(头号嫌疑):NRR<100 = 老客座席在缩 |

- **天花板:** 横向企业应用,巨大但"座席天花板"受质疑。**已并购:Smartsheet 2025/1 被 Blackstone/Vista 以约 $84 亿私有化退市。**
- **点评(NRR 是关键裁决,但 NRR 也会骗人):** **真扩张(AI 当加价、座席还在涨,NRR≥103 且升):ServiceNow、Atlassian、Figma、HubSpot**——AI 是加法不是替代,是这一层最干净的赢家。**座席侵蚀(已显形或被掩盖):Asana(NRR 95、+9%,最差)、Salesforce(自砍座席、有机约 8%、淡化 NRR)、Workday(按人头=结构性风险)。**
  - **两个对自己 NRR 论点的诚实纠偏(否则就是双标):** ① **Figma 的 139% 是全表最该打折的 NRR**——它刚 IPO,NDR 受 cohort 选择 + credit 打包影响最大,别当"AI 扩张"的铁证,要等几个完整续费周期。② **ServiceNow 的 🟢 押在"Now Assist $15 亿 ACV 是净新增不是替代"——但这是管理层口径,没有"净新增 vs 替代座席"的拆分**(我们 deepdive 自己标过这是关键未观测变量)。所以 NOW 进 🟢 带这个星号。
  - **一个必须正面回答的反方(否则整层 SoR 逻辑悬空):"agent 一定要经由在位者的 SoR 吗?"** 多头论点是"agent 要读写 CRM/ERP/工作流,所以绕不开 ServiceNow/Salesforce/SAP/Veeva"。**但反方很硬:agent 完全可以自带状态/记忆层、绕过在位 SoR,只把它当一个商品化数据库读一次。** Nadella 那句"SaaS 退化成数据库+治理"是双刃的——**如果应用退化成商品数据库,价值就跑到"治理/编排层",而那一层越来越住着 agent 框架(LangGraph/MCP 之类),不一定是 ServiceNow。** 这是 NOW/CRM/SAP 这一簇最大的、本表此前没充分压力测试的尾部风险。
  - Salesforce 是**最重要的"硬币"**:握最强 CRM SoR + Agentforce ARR >$8 亿(+169%),但也是最赤裸的座席暴露——成败全看"座席→AWU 消耗"转得够不够快。**Adobe 是被恐惧打到约 10× 的争议名**(Firefly 在变现,但市场怕 genAI 商品化创作)——见 §3 的变体观点,这是全表最该逆向研究的便宜期权。

### 2.6 垂直 SaaS / 商务(专有数据 + take-rate,普遍最抗打)

| 公司 | 业务本质 | 增速 | margin | 模式 | NRR | AI判定·评级 |
|---|---|---|---|---|---|---|
| **Veeva** | 生命科学专用软件+数据(药企) | +16%(订阅 +17%) | non-GAAP op 29.4%,升 | hybrid 订阅 | n/a | 🟢 AI 赋能:在受监管专有数据上做 agent,对手复制不了;抢 Salesforce 份额 |
| **Shopify** | 商家电商平台 | +34%(GMV $1010 亿 +35%) | FCF 15%(连 4 季中位) | **take-rate+订阅** | n/a | 🟢 AI 赋能:Sidekick+agentic 商务是增量 |
| **Toast** | 餐饮 POS+支付平台 | +24%(ARR +26%,加速) | GAAP op 21%(首破 20%) | **take-rate+SaaS** | n/a | 🔵/🟢 AI 中性/赋能;盈利拐点 |
| **Klaviyo** | 电商营销自动化(邮件/短信) | +28% | non-GAAP op 16.3% 创纪录 | 消耗+seat | **110% 升** | 🔵 AI 赋能;NRR 在升(逆势) |
| **Procore** | 建筑工程管理 SaaS | +16% | non-GAAP op 17%(从 10%) | seat 座席 | 毛留95% | 🔵/🟡 AI 中性;margin 大幅扩张 |
| **Samsara** | 互联运营 IoT(车队/设备) | +30%(**FY27 指引减速约 21–22%**) | non-GAAP op 17%,升 | 订阅+设备 | n/a | 🔵 AI 赋能;物理世界数字化 |

- **天花板:** 各垂直行业数字化,渗透率低、还在扩。**点评:** 这一层**普遍最抗 AI 冲击**——要么有 take-rate(Shopify/Toast:商家提效→GMV→收入,跟座席无关),要么有 AI 拿不走的专有/受监管数据(Veeva)。**Veeva + Shopify 是核心赢家**;Toast/Klaviyo/Samsara/Procore 是稳健受益(各带一个减速或 margin 的小注脚)。

### 2.7 AI 原生 / 落地(两极:一个封神,一个崩盘)

| 公司 | 业务本质 | 增速 | margin | 模式 | AI判定·评级 |
|---|---|---|---|---|---|
| **Palantir** | AI/数据操作平台(政府+商业) | **+85%,加速;美商业 +133%** | 净利率 53% GAAP;FCF $9.25 亿 | outcome/消耗 | 🟢\* 质地顶级(Rule of 40 约145)/ 🔴 估值(约 97× 前瞻、距高点 -34%)= risk-adjusted 实为 🟡 |
| **C3.ai** | 企业 AI 应用软件 | **最新季约 -46% / FY26 指引约 -45%,崩盘** | 巨亏;撤指引;裁员 26% | 订阅 | 🔴 顶着 AI 名字却输掉 AI 应用市场 |

- **点评:** 极端分化。**Palantir 是质地最顶级的 AI 原生赢家**(增速、Rule of 40、现金流全是天花板级),但估值是全场最贵、最不容错(详见 `software_ai_era_deepdive.md` §6 的 Palantir 专章 + PEG 陷阱说明)。**C3.ai 是反面教材**——AI-named loser,最新季收入反而约 -46%(FY26 指引约 -45%)。

### 2.8 通讯 / 协作("被 AI 杀"的头条最多,但财报多在企稳/改善)

| 公司 | 业务本质 | 增速 | margin | 模式 | NRR | AI判定·评级 |
|---|---|---|---|---|---|---|
| **Twilio** | 通讯 API(CPaaS,短信/邮件) | +20%(有机 +16%,加速) | non-GAAP 毛利 +16% | **消耗** | **114% 回升** | 🔵/🟢 AI 赋能:AI 越多 API 流量越多 |
| **Five9** | 云客服中心(CCaaS) | +9%(**AI 收入 +68%、>$1.25 亿**) | op 6.1%(从 -1.9%) | seat+消耗 | 107% | 🔵/🟡 AI 赋能、未被颠覆:自己 AI 是增长最快线 |
| **NICE** | 客服/CX 云+WFM | +10%(云 +14.6%,**AI ARR +66%**) | non-GAAP op 26%(**-450bps,降**) | seat+订阅 | n/a | 🟡/🔵 AI 赋能未被颠覆,但 margin 因投入压缩 |
| **DocuSign** | 电子签名+协议管理(IAM) | +8%(IAM ARR $3.5 亿,占 10.8%) | non-GAAP EPS 超预期 | seat 座席 | n/a | 🟡 被威胁但在 defend:IAM 是 AI 时代再造 |
| **Zoom** | 视频/UCaaS+客服中心 | +5.5%(企业 +7.2%) | non-GAAP op 41.1%,升 | seat 座席 | n/a | 🟡/🟠 被威胁/中性:AI Companion 变现是胜负手;靠回购 |
| **RingCentral** | 云电话/UCaaS | +5%(AI ARR >10%,翻倍) | non-GAAP op 22.9%,升;FCF 21.8% | seat 座席 | n/a | 🟠/🟡 慢增长,靠 AI attach+FCF/回购 defend |

- **天花板:** 通讯/客服,成熟、部分见顶。**点评:** 这里**头条与财报最分裂**。"Sierra/Decagon 杀客服、Cursor 杀 CPaaS"的故事**在上市在位者财报里还没兑现**——Five9(AI 收入 +68%)、NICE(AI ARR +66%)、Twilio(NRR 回 114%、加速)的自家 AI 反而是增长最快的线。**NICE 唯一黄旗是 margin 为投入而压缩(非收入)。** Zoom/RingCentral 是低增长融冰、靠 FCF + 回购 defend。**真正的颠覆者(Sierra $158 亿估值/ARR >$1.5 亿、Decagon $45 亿)还很小**,解释了为什么在位者财报还没被打穿(见 §5)。

### 2.9 被颠覆 / 输家(财报里已经在流血)

| 公司 | 业务本质 | 增速 | margin/状态 | NRR | 机制·评级 |
|---|---|---|---|---|---|
| **Chegg** | 在线作业/学习订阅 | **-48%,subs -31%** | 靠裁员(45%)挤出微利 | n/a | 🔴 被 AI 抹掉:免费 LLM+谷歌 AI 概览毁掉产品+入口;距峰值约 -99% |
| **ZoomInfo** | B2B 销售情报/数据 | +1%(**指引下调到约 -4%**) | 裁员约 20% | **90%(连 3 季)** | 🔴 真流血:数据垄断租金归零,座席/数据双侵蚀 |
| **C3.ai** | 企业 AI 应用 | **约 -46%(FY 指引约 -45%)** | 巨亏、撤指引、裁 26% | n/a | 🔴 顶 AI 名却被 LLM 浪潮淘汰 |
| **UiPath** | RPA/agentic 自动化 | +14%(ARR +11%,减速) | non-GAAP op 改善 | **120→107** | 🟠 被威胁+转型:agent 既蚕食又是它的赌注 |
| **Gartner** | 辛迪加 IT 研究+咨询 | +2%(FX 中性 -1%) | 靠回购撑 EPS | n/a | 🟠 早期被去中介:合同价 CV +1% 是先兆,核心研究仍 +5% |
| **Dropbox** | 文件存储+Dash | +0.8%(约持平) | non-GAAP op 40%;FCF +69% | n/a | 🟠 融冰:存储商品化,Dash 未验证;靠回购 |
| **Sprout Social** | 社媒管理 SaaS | +11.2%,减速 | non-GAAP op 11.6% | n/a | 🟠 中小客户被 AI+预算侵蚀,转上市场 defend |

- **点评:** **真流血的(🔴):Chegg、ZoomInfo、C3.ai**——共同 DNA 是"卖数据/内容垄断"或"被 LLM 直接商品化"。**慢性病(🟠):UiPath(NRR 120→107)、Gartner(CV 减速)、Dropbox/Sprout(融冰)**——还在增长或靠 FCF 续命,但终局在缩。**别买它们的"便宜",那是价值陷阱。**

---

## 第三部分:鲜明判断 —— 最该买的、最该躲的、被错杀的

**🟢 最该长期布局的核心赢家(质地×天花板×卡位,不看估值):**
1. **平台三巨头:Microsoft / Google / Amazon** —— 拥有 AI 时代最稀缺的"模型+云+分发",都在加速 + margin 升,最确定(各带一个 caveat,见 §2.1)。Google 还是其中估值最不贵的。
2. **数据/铲子:Datadog(+ 私有 Databricks);Snowflake 次之** —— AI 的燃料与中立铲子;但 Snowflake 因 Iceberg/Databricks 侵蚀降为 🔵,数据层最强的牌可能是还没上市的 Databricks(2H26 IPO 必盯)。
3. **安全:CrowdStrike(+ Palo Alto)** —— 最 AI-durable 板块的消耗/平台整合者。
4. **横向 SoR:ServiceNow / Atlassian** —— AI 当净增 ACV 卖,NRR 在升的"加价者"(NOW 带"净新增 vs 替代"未拆分星号)。
5. **垂直/商务:Veeva / Shopify** —— 专有数据 + take-rate,AI 拿不走。
6. **设计:Figma** —— 全场增速最快(+46%)、NRR 最高(139%,但刚 IPO、该打折看)。
7. **AI 落地:Palantir(🟢\*)** —— 质地顶级,但**质地 🟢、估值 🔴**:约 97× 前瞻、risk-adjusted 实为 🟡,要么等回调、要么承认在为最高 offense 付最贵的票价。

**🔴 最该躲的(价值陷阱:便宜是因为终局在缩):** Chegg、ZoomInfo、C3.ai(真流血)、UiPath、Dropbox、Sprout Social(慢性病)。**它们的低估值不是机会,是终局定价。**(Gartner 单列:核心研究仍 +5%、是"早期预警"非"正在崩塌",比另几个轻,别一棍子打死。)

**🟡 变体观点 / 非共识 call —— 这才是能赚钱的地方(共识已知"平台最安全",不值钱):**
- **【做多】Adobe(约 10–12× 前瞻)—— 全表风险收益最好的逆向标的。** 市场把它当"被 genAI 杀的创意软件",但 Firefly ARR >$2.5 亿 +75%QoQ、DM ARR $192 亿仍 +11.5%——**这是赌"AI 幸存者"被错杀成"AI 受害者"的最便宜期权。如果只下一个非共识注,是它。**
- **【警惕/对冲】"独立层被超大规模云垂直整合"——利空 Datadog / Snowflake(甚至边际利空 CrowdStrike)。** 云厂自带监控(CloudWatch/Azure Monitor)、自建数据/安全(已买 Wiz/CyberArk),"卖铲人"和"卖地人"是同一批。高盛对 Datadog 的看空就是这条——所以 Datadog 是"🟢 带强空头",不是"无脑铲子"。
- **【别追】Palantir 的高倍数** —— 97× 已 price in 多年完美执行;质地不是问题,价格是。
- **【硬币】Salesforce(约 28×)** —— 握最强 CRM SoR + Agentforce +169%,但有机增速掉到约 8%。赌"座席→AWU 消耗"转得过来=巨大重估,转不过来=慢性座席侵蚀。**也是"agent 会不会绕过 SoR"这个尾部风险最直接的暴露名。**
- **【被忽视的稳健】Fortinet(约 30×)** —— 安全里最被忽视的现金牛(创纪录 margin + 最便宜)。
- **【模型层的真正归属】** 价值最终可能流向模型层本身——而最强的模型层(**Anthropic / OpenAI**)是私有、买不到;公开市场唯一干净的模型层敞口就是 Google(已在 🟢)。这是"价值上移到模型层"论点的逻辑终点,也是为什么 Google 这一票特别。

> **跟前几份 memo 的呼应与一处自我纠正:** 上一份软件 memo 的 Top 5+1(Microsoft、Google、ServiceNow、CrowdStrike、Datadog + 回补的 Palantir)在这张更大的对标里全部落在 🟢(Palantir 为 🟢\*),逻辑自洽。**一处刻意纠正:本表初稿曾把 Snowflake 也放进 🟢,但这与 deepdive 把 Snowflake 降到荣誉席(因 Iceberg/Databricks 侵蚀)自相矛盾——已改为 🔵,前后一致。** 这张表额外补出的高 conviction 名是 **Atlassian、Figma、Veeva、Shopify**(都进 🟢),以及私有的 **Databricks**(2H26 IPO 必盯)。

---

## 第四部分:收费模式的未来(谁卡位 = 谁赢)

**按座席收费被结构性威胁**(人少了、活儿还在,座席收入随人头缩)。硬证据:GitHub Copilot 2026/6/1 转消耗、微软 Nadella"任何按人头的业务都会变成按人头且按用量"、Salesforce 推 AWU(Agentic Work Units)、客服 deflection 60–80%。**未来 = 三层 settle-out:缩水的人类座席基线 + 计量消耗(token/动作)+ 结果定价(每解决一单)。**

- **天生顺风(已按消耗/take-rate):** 云三家、Snowflake、Databricks、Datadog、Cloudflare、Twilio、Shopify、Toast、Klaviyo、CrowdStrike(Flex)。
- **成功转型/加价(座席仍增、AI 当加法):** ServiceNow、Atlassian、HubSpot、Figma、Monday。
- **转型中、生死看转速:** Salesforce(AWU)、Workday(Flex Credits)、Adobe(credits)、GitHub(usage)。
- **逆风(纯座席+可自动化):** Asana、Zoom/RingCentral(UCaaS 座席)、Okta/Zscaler(per-seat 安全)、Workday(按人头)。

> **但消耗计价是双刃剑:** token 价格在通缩、客户会优化用量(Twilio 历史上 NRR 一度跌破 100% 就是优化所致)。**"已转消耗"是必要条件不是充分条件——还要看消耗绑在不绑"会持续放量、砍不掉"的刚性工作负载上**(这也是监控/安全/数据比可压缩 API 调用更优的原因)。

---

## 第五部分:私有 / 已并购名单(看不到但必须知道)

**高增长私有(估值锚 + 颠覆力):**
- **Databricks** —— 跑率 >$54 亿 +65%、AI ARR $14 亿、NRR >140%、$1340 亿估值(2025/12)、**S-1 目标 2H26**(必盯,会重设数据层估值锚)。
- **Cursor / Anysphere** —— ARR 约 $30 亿(4 月口径,史上最快 0→$30 亿);**SpaceX 出 $600 亿(估值)期权收购**(2026/4,抢在一轮 $20 亿融资前,未成交;注:$600 亿是收购估值、不是 ARR 目标)。
- **Cognition(Devin)** —— $4.92 亿 ARR 跑率、$260 亿估值(2026/5,53× ARR);收购了 Windsurf。
- **Replit** —— 约 $1.5 亿跑率冲 $10 亿、$90 亿估值;**Vercel** —— 约 $2 亿 ARR +82%、$93 亿估值。
- **AI 客服颠覆者:** Sierra($158 亿估值、ARR >$1.5 亿)、Decagon($45 亿、约 $0.35 亿 ARR)、Intercom Fin(ARR >$1 亿,$0.99/解决)——**增长快但相对在位者多十亿级基数仍小**,所以 Five9/NICE 财报还没被打穿。

**已被并购(从对标里移除):** Confluent → IBM(约 $110 亿,2026/3);CyberArk → Palo Alto(约 $250 亿,2026/2);Wiz → Google(约 $320 亿,2026/3);Smartsheet → Blackstone/Vista(约 $84 亿,2025/1)。

---

## 第六部分:大佬 / 行业观点(本表判断的依据)

1. **Satya Nadella(微软):** 业务应用本质是"带业务逻辑的 CRUD 数据库",agent 时代"所有逻辑上移到 AI 层",SaaS 退化成"数据库+治理";"任何按人头的业务都会变成按人头**且**按用量"。
2. **Martin Casado(a16z):** "座席不再是软件的原子单位"——AI 把活儿干了,定价从"访问权"转向"结果/用量"。
3. **Aaron Levie(Box):** 座席定价会死、但 SaaS 不死;"agent 用软件是人的 100 倍,无头化(headless)不可避免";"我们进入上下文时代,agent 要的是你非结构化数据里的 context"。
4. **Jamin Ball(Altimeter):** "按座席定价之死"——agent 不买座席、它做任务、用 token;座席沦为"预付消耗的打包方式",增长向量是"按结果/任务/token"。
5. **Tomasz Tunguz(Theory):** 2026 年"垂直软件跌 43%、工作流工具跌 39%"——纯工作流工具正落在 AI agent 的刀口上;**NRR/NDR 下滑是 AI 颠覆的领先指标**(本表第〇部分的方法论核心)。
6. **Klarna(自动化质量天花板):** 替掉约 700 客服后**回招人**——"过度追求效率和成本,结果质量下降、不可持续",转人机混合。**这是整个颠覆论的调速器:routine 高频低风险的活儿成本会崩,但有责任/品牌成本的活儿全自动有质量上限**(利好 Five9/NICE 这类混合,利空"纯替代"叙事)。
7. **服务即软件(a16z/Sequoia/Bain):** AI 把约 $4.6 万亿服务/劳动力市场"反转成软件",把 BPO 的 20–40% 毛利抬到 SaaS 的 70–90%;但收入更 lumpy、利润质量更杂。
8. **安全板块共识(Gartner / Cloud Security Alliance / Bessemer):** "保护 AI agent 是 2026 定义性的安全挑战";机器身份数量级超过人类且治理缺失——**支撑"安全是最 AI-durable 板块 + 机器身份是新品类"的判断**。
9. **Pragmatic Engineer(Gergely Orosz)约千人调研:** Claude Code 8 个月从 0 到第一、超过 Copilot/Cursor;95% 工程师每周用 AI、70% 同时用 2–4 个工具——**AI 原生编程对在位开发工具的颠覆是真实且快速的**。
10. **观测性多空之争:** 摩根士丹利上调 Datadog(目标 $225)——"agentic AI 触发监控需求第二波";高盛反驳——"AI 让客户自我埋点/整合,压制 Datadog"。**这是 🟢 里少数有强空头的名字。**

---

## 第七部分:看空 / 诚实的边界与数据质量

1. **财报是滞后指标(最大的认知风险):** 颠覆通常领先财报 12–24 个月。今天"财报没流血"不等于安全(尤其 Salesforce/Workday/Zoom 这类座席暴露名)。要盯 GRR(毛留存)和座席数本身,别等 NRR 跌穿 100% 才反应。
2. **私有 ARR 未经审计:** Cursor/Cognition/Sierra/Decagon/Databricks 的数字是创始人/VC/分析师口径,结果型 ARR 更 lumpy、未经一个完整续费周期检验,打折看。
3. **AI 收入跨公司不可比:** 多为"AI 集成客户占比"等定性口径,高估了真正 AI 驱动的收入;只有少数(Databricks $14 亿、Palantir、Now Assist $15 亿)是硬数。
4. **并购/口径噪音:** Palo Alto NGS ARR +56% 含 CyberArk/Chronosphere 并购(有机减速被掩盖);Salesforce 收入含 Informatica。表内已标注。
5. **财年错位 + 个别陈旧:** Veeva/C3.ai/Samsara/DocuSign/UiPath/Zoom/NICE 为非日历财年;**Asana 最新可核实季是 2025/4(约 1 年陈旧),新季未出**;Elastic Q4 今日(5/28)才出。Palantir 前瞻 PE 跨源在 82–99× 间(取 5/24 约 97×)。
6. **估值为 5 月多源近似、实时行情受限,需终端复核。** 评级是"质量×卡位"判断,非"此刻按此价买入"——入场点要叠加估值与回调时机。

---

## 附:术语速查
| 名词 | 大白话 |
|---|---|
| SoR(系统-of-record) | 某类企业数据的权威存放+流转中枢(CRM/ERP/HR) |
| NRR / NDR / DBNR | 净收入留存:老客户今年比去年多付还是少付;<100% = 基盘在缩 |
| GRR(毛留存) | 剥掉扩张后老客户还剩多少,识别座席流失更准 |
| ARR / cRPO / RPO | 年化经常性收入 / 当期+未来已签约未确认收入 |
| 座席/消耗/结果定价 | 按人头 / 按用量(token、动作)/ 按成果(每解决一单)收费 |
| take-rate | 按交易额抽成(Shopify/Toast),与座席无关 |
| 去中介化 | 某环节被技术绕过、价值被拿走 |
| agent / agentic AI | AI 智能体,能自主完成多步任务 |
| 数据重力 / Iceberg | 数据越多越吸引计算聚拢成护城河;Iceberg=开放湖仓格式,正瓦解这种锁定 |
| Rule of 40 | 增速 + 利润率 ≥40 即健康;Palantir 约 145 是天花板级 |

---

## 资料来源(关键,按板块)
**平台/数据:** 各家最新季 8-K/电话会(MSFT FY26Q3、GOOGL/AMZN 2026Q1、ORCL FY26Q3、SNOW FY27Q1、DDOG/NET/MDB/ESTC 最新季);Databricks PR + CNBC 估值;Confluent→IBM 8-K;Iceberg 互通(AnalyticsWeek);Datadog 多空(摩根士丹利/高盛)。
**安全/开发:** CRWD FY26Q4、PANW FY26Q2、FTNT/ZS/S/OKTA 最新季 8-K;CyberArk→PANW、Wiz→Google 并购确认;Pragmatic Engineer 2026 AI 工具调研;Gartner/CSA/Bessemer 安全展望;Cursor/Cognition/Replit/Vercel 私有 ARR(TechCrunch/CNBC/Bloomberg/Sacra)。
**应用/垂直/通讯/输家:** 各家最新季 8-K/6-K/电话会(CRM FY27Q1、NOW/TEAM/HUBS/ADBE/SAP/INTU/MNDY/FIG/ASAN、VEEV/SHOP/TOST/KVYO/PCOR/IOT、PLTR/AI、TWLO/ZM/DOCU/FIVN/NICE/RNG、CHGG/ZI/IT/PATH/DBX/SPT);Nadella(BG2)、Casado(a16z)、Levie(Box/TechCrunch)、Ball(Clouded Judgement)、Tunguz(Theory)、Klarna(Entrepreneur/SEC)、Sierra/Decagon(Sacra/TechCrunch)。

---

> **质量审查记录(QC):** 本表经 4 路并行深度研究(约 50 家公司)→ 综合分层 → critical-thinker 红队 challenge → research-reviewer 事实核查 → 迭代修订。
> **红队改了什么(已落地):** ①**Snowflake 从 🟢 降到 🔵**(消除与 deepdive 把它降荣誉席的自相矛盾,因 Iceberg/Databricks 侵蚀);②**Palantir 拆成"质地🟢/估值🔴"(🟢\*)**,不再与 Google-29× 混为一档;③**Google/Microsoft 的 🟢 加上 caveat**(open-weights+搜索去中介 / capex 折旧压 margin);④**Oracle 的 RPO 质疑对称地加到三巨头**(不双标);⑤**NRR 不再被当铁证**——Figma 139%(刚 IPO 该打折)、Snowflake/Datadog 消耗 NRR(上量虚高/优化骤降)都加了 GRR caveat;⑥**Datadog 加"云厂垂直整合+高盛看空"caveat**(不再"无脑铲子");⑦**正面压力测试"agent 是否必须经由在位 SoR"**(反方:agent 自带记忆层绕过),给 NOW/CRM 加星号;⑧**把变体观点(做多 Adobe、警惕独立层被整合、别追 Palantir 倍数)提进 §3 鲜明判断**,不再退回 mega-cap 共识。
> **事实核查改了什么(已落地):** C3.ai 增速从 -36% 更正为约 -46%(最新季)/约 -45%(FY 指引);Cursor ARR 从 $20 亿更新为约 $30 亿(4 月口径)、并澄清 $600 亿是 SpaceX 收购估值非 ARR 目标;Datadog NRR 从约 115% 更正为低 120%。**其余约 30 项高引用数字(三巨头增速、四起并购、Palantir/Figma/CrowdStrike 等)经核对全部 tie out,无捏造。**
> 数字为各公司最新已报告季、5 月口径,需终端复核;私有/AI 收入多为二手未审计。
