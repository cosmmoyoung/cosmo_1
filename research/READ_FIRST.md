# 📖 先读这份 —— 整个研究项目的总入口与阅读地图

*给:从未接触过 AI 硬件/半导体行业、第一次拿到这堆 memo 的读者(包括 IC 委员会、家人、其他基金的同事)*
*日期:2026 年 5 月。这不是一份独立报告,是 19 份研究 memo 的总入口。*

---

## 这堆 memo 在解决什么问题?

**一句话:** AI 这波热潮里,把整个产业链(从最上游材料到最下游软件)拆开看,**真正不可替代、长期能赚钱的环节是哪些;具体到上市公司,该买谁、什么价位、用什么仓位结构。**

研究的核心方法论是"**卡脖子理论**(chokepoint)"——不去赌"AI 哪家赢"(英伟达 vs AMD vs 谷歌),而是去找"**不管谁赢都要付钱给它**"的环节:芯片代工(台积电)、光刻机(ASML)、设计软件(Cadence/Synopsys)、HBM 存储(SK 海力士)、先进封装(BESI)、磷化铟激光(Coherent/Lumentum)等。

---

## 行业 30 秒入门(没背景也能跟上后面)

**AI 跑起来需要三样物理资源:① 算力(芯片)② 电力 ③ 数据中心(冷却、网络、机房)。** 每一样背后都有一条供应链,每条供应链上都有几个"卡脖子"环节——少数几家公司近乎垄断,且很难被替代。

- **算力侧:** 英伟达设计 GPU → 台积电(TSMC)制造 → 用 SK 海力士的 HBM 存储 → 用 BESI 的封装设备堆叠 → 用 Coherent/Lumentum 的光模块在机架间传数据。每一步都有一个或几个垄断玩家。
- **电力侧:** 数据中心耗电翻倍 → 需要 GE Vernova/Hitachi 的电力设备、Vertiv 的电源/散热 → 上游需要变压器(钢)、燃气轮机、燃料电池(Bloom)。
- **软件侧:** AI 颠覆传统软件(座席收费的会被替代),但 Microsoft/Google/ServiceNow 等"agent 必须经由它的数据/系统"的会赢。

**核心结论收敛在 `ten_year_chokepoint_conviction.md`:** 长期持有(10 年)的最高 conviction 三件套是 **TSMC(代工)+ ASML(光刻)+ Cadence/Synopsys(设计软件)**——每颗 AI 芯片必经,且架构无关(GPU 还是 ASIC 都用)。

---

## 阅读顺序建议(从入门到深入)

### 🟢 先读这 3 篇(看完就懂全局)
| # | 文件 | 看什么 | 难度 |
|---|---|---|---|
| 1 | **`ten_year_chokepoint_conviction.md`** | **最终结论**:十年视角下该买谁、为什么(TSMC+ASML+EDA 三件套) | ⭐ 入门 |
| 2 | `synthesis_top3_2030.md` | 上一版结论:弹性视角下选 3 只(BESI、SK 海力士、Coherent) | ⭐ 入门 |
| 3 | `serenity_leopold_profiles.md` | 两位市面知名 AI 投资者(@aleabitoreddit / Aschenbrenner)的思路对比+可执行性 | ⭐ 入门 |

### 🔵 再读这 4 篇(理解整个框架)
| 4 | `ai_supply_chain_framework.md` | 整套"卡脖子"分析框架 + 给出五维打分体系 | ⭐⭐ |
| 5 | `long_term_demand_2030.md` | 各环节到 2030 年需求复合增速预测 | ⭐⭐ |
| 6 | `software_sector_benchmark.md` | 约 50 家软件公司全板块 benchmark(谁赢谁输) | ⭐⭐ |
| 7 | `next_chokepoint_hunt.md` | 沿 Serenity/Leopold 思路找下一个卡脖子(散热/基板膜/连接器/测试) | ⭐⭐ |

### 🏆 80% 身家之战(2026 年 6 月 11 日,最终收口,4 篇一组)
| 文件 | 看什么 | 难度 |
|---|---|---|
| ⭐⭐ **`the_80_percent_bet.md`** | **最终答案**:暴富怎么压——两阶段打法(现在防守结构上场 + 2027-28 血里机械加仓上杠杆) | ⭐ 入门 |
| `token_demand_secular_test.md` | "token 需求停不下来"独立验证:需求被平反(+4-7 倍/年),裂缝在金融层 | ⭐⭐ |
| `next_elasticity_hunt_2026.md` | 全栈扫"还没涨的":只剩玻璃基板一个半;SMR 已崩 70-84% 当活标本 | ⭐⭐ |
| `eighty_percent_redteam.md` | 红队攻击:"既要又要"病、Kelly 数学、干火药共识陷阱、方案甲/乙 | ⭐⭐ |

### 🔴 存储专题(2026 年 6 月更新,4 篇一组,看 ⭐ 那篇即可懂全部)
| 文件 | 看什么 | 难度 |
|---|---|---|
| ⭐ **`storage_master_synthesis.md`** | **存储总结论(大白话)**:涨没涨完、缺不缺 5 年、买什么、PE/创业机会、该怎么做 —— 一页看清 | ⭐ 入门 |
| `storage_2026_durability_update.md` | "缺 5 年"论点压力测试(6 月最新数据;HBM4 三家认证、合约价、中国放量) | ⭐⭐ |
| `storage_investable_universe.md` | 全部能买的票(含中国 佰维/江波龙/兆易/澜起 + 模组/控制器/封测/台日利基 + 离岸可及性) | ⭐⭐ |
| `storage_pe_startup_angles.md` | PE/并购/Pre-IPO/创业机会(二手设备、工业内存、CXL/PIM、退役内存复用) | ⭐⭐ |

### 🟡 然后按兴趣挑深度报告
| 文件 | 主题 | 一句话 |
|---|---|---|
| `optical_industry_deepdive.md` | 光通讯 | 价值收敛到 InP 激光,Coherent/Lumentum/新易盛/中际旭创 |
| `memory_industry_deepdive.md` | 存储(旗舰背景) | HBM 量价齐升,SK 海力士、美光、三星;周期诅咒 —— **存储专题请先看上方 ⭐** |
| `inp_laser_deepdive.md` | 磷化铟激光芯片 | 光链最硬卡点,Coherent/Lumentum/AXT/源杰 |
| `glass_substrate_deepdive.md` | 玻璃基板 | 下一代封装基底,SKC/Absolics |
| `power_infrastructure_deepdive.md` | 电力设备 | GE Vernova/Vertiv/Hitachi/Eaton |
| `probe_cards_deepdive.md` | 探针卡 | 测试环节,FormFactor/Technoprobe |
| `software_ai_era_deepdive.md` | 软件行业 | AI 杀谁、不杀谁;Top 5: 微软/谷歌/ServiceNow/CrowdStrike/Datadog + Palantir |
| `bom_walk_chokepoints.md` | 全产业链扫描 | 20 个候选卡点的初步筛选 |
| `demand_growth_bottom_up.md` | 2026 年需求自底向上 | 每个环节增速核实 |

### 🟠 操作层面(怎么下单)
| `leverage_strategy_ibkr_hk.md` | IBKR 香港怎么用杠杆 | 2x 危险,1.3-1.4x 是甜区,LEAPS/Box 融资优于直接借保证金 |

### ⚪ 历史档案(可跳)
| `nittobo_base_case.md` / `nittobo_bear_case.md` | 日东纺多空双案 | 早期单标的研究 |

---

## 全局术语速查(看任何 memo 都能查)

### 公司速查(按字母)

| 简称/代码 | 公司全名 | 一句话讲它干嘛 |
|---|---|---|
| **ASML** | ASML Holding(荷兰) | 全球独家做 EUV 光刻机(造尖端芯片必备),每台约 $4 亿 |
| **ASMPT(0522.HK)** | ASMPT Ltd | 先进封装设备(TCB 热压键合),港股上市 |
| **AVGO** | Broadcom 博通 | 定制 AI 芯片(ASIC)+ 网络芯片,谷歌 TPU 它代工设计 |
| **Advantest(6857.T)** | 爱德万 | 全球最大芯片测试机厂(给 AI 芯片做"出厂体检"),日股 |
| **AXTI / AXT** | AXT Inc | 磷化铟(InP)衬底,Serenity 的代表股 |
| **BESI** | BE Semiconductor(荷兰) | 混合键合设备,3D 封装的"卖铲人" |
| **CDNS** | Cadence Design Systems | EDA 双寡头之一(设计芯片用的软件),美股 |
| **COHR** | Coherent Corp | 光模块+激光器,自有磷化铟产线,美股 |
| **CRWD** | CrowdStrike | 云端点安全 |
| **CRWV** | CoreWeave | 新型 GPU 云(neocloud),Aschenbrenner 重仓 |
| **DDOG** | Datadog | 云端可观测性/监控软件 |
| **GE Vernova(GEV)** | GE Vernova | GE 拆分出的电力设备(燃气轮机、电网) |
| **海力士(000660.KS)** | SK Hynix | HBM(高带宽存储)龙头,英伟达约 70% HBM 来自它,韩股 |
| **Hitachi(6501.T)** | 日立 | 电网设备(变压器、输电),日股 |
| **Ibiden(4062.T)** | Ibiden | 高端 IC 基板(英伟达 GPU 用),日股 |
| **InP** | 不是公司,是材料 | 磷化铟,做高速激光器的衬底,光通讯卡脖子 |
| **LITE** | Lumentum | 唯一量产 200G EML 激光器,美股 |
| **MSFT** | Microsoft | 全栈赢家:模型+云+应用+安全 |
| **NBIS** | Nebius | 新型 GPU 云(欧洲版 CoreWeave) |
| **NOW** | ServiceNow | 企业工作流软件,AI 当加价卖 |
| **PLTR** | Palantir | AI 应用层"落地"赢家,本体(ontology)平台 |
| **SIVE.ST** | Sivers Semiconductors | 瑞典小盘光子公司,Serenity 代表股 |
| **SNOW** | Snowflake | 云数据仓库 |
| **SNPS** | Synopsys | EDA 双寡头之另一家 |
| **TSM / TSMC** | Taiwan Semiconductor Manufacturing | 台积电,全球先进制程代工独占约 90% |
| **VRT** | Vertiv | 数据中心电源+散热(CDU 冷却液分配单元) |
| **AAOI** | Applied Optoelectronics | 光模块厂,Serenity 代表股 |
| **新易盛(300502)** | Eoptolink Technology | 中国光模块龙头,深股 |
| **中际旭创(300308)** | InnoLight Technology | 中国光模块全球第一,深股 |
| **天孚通信(300394)** | T&S Communications | 中国光器件,深股 |
| **Ajinomoto(2802.T)** | 味之素 | 食品公司,但有 ABF 膜(高端芯片基板必用)垄断,日股 |
| **Amphenol(APH)** | Amphenol | 高速连接器,英伟达 NVL72 机架连接器主供 |
| **Bloom Energy(BE)** | Bloom Energy | 燃料电池(数据中心现场供电),Aschenbrenner 第一大仓 |

### 关键名词(技术/金融)

**技术名词:**
- **AI accelerator / GPU / ASIC:** AI 训练/推理用的芯片。GPU=通用(英伟达),ASIC=定制(谷歌 TPU、亚马逊 Trainium)。
- **HBM(高带宽存储):** 一种叠很多层的特殊 DRAM,每颗 AI GPU 旁边必须配几颗,SK 海力士主导。
- **EUV 光刻机:** 用极紫外光在硅片上刻线路,做 3nm/2nm 芯片必须用,ASML 独家。
- **先进封装 / CoWoS / 混合键合:** 把 GPU 和 HBM 焊在一起的工艺,台积电(CoWoS)+ BESI(混合键合)主导。
- **光模块 / 光通讯 / CPO:** 数据中心里芯片之间用光纤传数据用的设备。可插拔模块 → CPO(共封装光学)是下一代。
- **InP / EML / CW 激光:** 光模块里发光那颗小芯片,材料是磷化铟(InP),AI 1.6T 必用 EML。
- **EDA 软件:** 芯片设计软件,工程师用 Cadence/Synopsys 设计每颗芯片。
- **测试 ATE / 探针卡:** 芯片造完出厂前要测试,Advantest 卖测试机,FormFactor 卖探针卡(消耗品)。
- **agent / agentic AI:** 能自主完成多步任务的 AI(不只是聊天)。
- **SoR(系统-of-record):** CRM/ERP/HR 等企业核心数据系统,agent 必须经过它读写。

**金融名词:**
- **倍数 P/E(市盈率):** 股价 ÷ 每股盈利。50× 意思是"按现在盈利,50 年回本"。**前瞻 PE(fwd P/E)** = 用未来 12 个月预期盈利算的;**trailing PE** = 用过去 12 个月已经实现的盈利算。
- **EV/S(企业价值/销售额)、EV/EBITDA:** 同类估值倍数,适合还没盈利或盈利不稳的公司。
- **NRR / 净收入留存:** SaaS 公司老客户今年比去年多付的比例。130% = 老客户多付 30%(健康);<100% = 基盘在缩(座席在被砍)。
- **GRR / 毛留存:** 剥掉扩张只看流失,识别座席侵蚀更准。
- **ARR / 年化经常性收入:** 订阅类公司的年度规模化收入。
- **TAM(总可寻址市场):** 整个市场的最大盘子。
- **Top-line / Bottom-line:** 收入 / 净利润。
- **杠杆 k:** 总持仓 ÷ 自有资金。2x = 借了等额的钱。
- **维持保证金率 m:** 券商要求"自己的钱"占总持仓的最低比例(大盘股约 25-30%)。
- **LEAPS:** 长期(1-2 年)期权,可作"股票替身"获得杠杆但不会被强平。
- **复利 / CAGR:** 复合年化增长率。

**研究框架名词:**
- **卡脖子(chokepoint):** 供应链里不可替代、一断供全停的环节。
- **架构无关(architecture-agnostic):** 不管哪种技术方案赢,这环节都要用到(收费站)。
- **单向棘轮:** 只增不减的趋势(如每颗芯片的测试次数)。
- **整合免疫力:** 这环节会不会被大客户(英伟达/台积电)自己做掉。
- **永久减值 vs 回撤:** 前者是十年后归零(真风险);后者是中途跌、会涨回(对长持是噪音)。

---

## 关键判断速览(一图看清最终结论)

**长期 10 年最高 conviction(`ten_year_chokepoint_conviction.md`):**
- 🟢 核心三件套:**TSMC + ASML + Cadence/Synopsys** —— 每颗 AI 芯片必经
- 🔵 卫星仓(等回调):Advantest 测试、KLA/Onto 量检测、Amphenol 连接器、BESI 混合键合
- 🟡 主题/事件仓:Ajinomoto ABF 膜、ASMPT、nVent 散热
- 🔴 别长持/已颠覆:杠杆 ETF、Astera Labs(被英伟达整合)、Chegg/ZoomInfo/C3.ai(被 AI 抹掉)

**弹性视角(`synthesis_top3_2030.md`):**
- BESI(混合键合)+ SK 海力士(HBM)+ Coherent(光链激光)

**软件层赢家(`software_ai_era_deepdive.md`):**
- Microsoft + Google + ServiceNow + CrowdStrike + Datadog + Palantir

---

## 写作风格说明

- 全部中文为主,英文术语首次出现用括号注;
- 不用半角波浪号(英文 tilde)——在某些 markdown 渲染下两个连用会变成删除线,影响阅读;
- 数字尽量带口径(前瞻 PE / trailing PE / non-GAAP / GAAP 区分);
- 每篇 memo 都有"质量审查记录"段说明哪些被红队 challenge 过、哪些数字未复核——**默认所有数字 5 月 2026 口径、需在彭博/万得终端复核后再下单。**

---

## 写给非专业读者的免责声明

这是研究框架,不是个性化投资建议。所有结论应基于自己的风险偏好、税务身份(本项目主要面向**香港居民、IBKR 账户**)、流动性需要再做判断。半导体股波动极大,单年回撤 40-50% 是常态——只有在心理上能扛住中途回撤,才适合做卡脖子长持。
