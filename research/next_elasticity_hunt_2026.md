# 下一个"2023 年 HBM"在哪?—— AI 基础设施栈"早期弹性"再猎(2026 年 6 月版)

### 给想压 80% 身家、要爆发力、不要 NVIDIA/指数的高净值客户:此刻还有没有真·早期的 3-10x?

*作者:资深买方分析师*
*日期:2026 年 6 月 11 日(收盘价口径)。本文是对 `synthesis_top3_2030.md`(BESI/海力士/Coherent)、`next_chokepoint_hunt.md`(散热/ABF/连接器/测试)、`storage_master_synthesis.md`(存储已晚)、`power_infrastructure_deepdive.md`(电力已定价)四份基线的 UPDATE,不重复其结论,只补"哪里还早"。沿用大白话标准、不用波浪号。价格为 6 月多源口径,需终端复核。*

---

## 🎯 先把最硬的结论给你(读这一段就够了)

> **残酷的真相:到 2026 年 6 月,AI 基础设施栈里"已经被广泛认知 + 公开可买"的环节,几乎全部已经 repriced 完了——大多数过去 12 个月涨了 3-10 倍。你要找的那个"2023 年初的 HBM",在公开市场里已经基本不存在了。**

但不是完全没有。把"结构弹性 × 还没 price in × 质地 × kill-risk"四维叠起来,**只有一个环节同时满足"真·0→1 拐点 + 还没像存储那样涨 10 倍":玻璃基板(glass substrate)。** 它在 2026 年从"PPT"变成"AMD MI400 / Intel 18A 真出货",而最干净的上市表达(SKC)只从低点涨了约 60%——相对存储/光模块的 5-10 倍,这是全栈唯一还在 S 曲线"脚踝"的主题。

其余你列的候选——CPO 光模块、Astera/Credo、Navitas/GaN、台系液冷、机器人减速器、SMR 核电——**要么已经涨 3-10 倍(光模块、AVC、绿的谐波),要么已经涨完又崩(SMR:Oklo $194→$56、NuScale $57→$9),要么基本面撑不起估值(Navitas 分析师目标价 $14 vs 现价 $21)。** 详见第三部分"别追"清单,附 12 个月倍数当铁证。

**一句话:此刻唯一还算"早"的真·拐点是玻璃基板;次选是 CPO 上游的激光/ELS 稀缺(但被埋在已 50x 的 Coherent/Lumentum 里);真正最早的(微流道散热)还是私有、买不到——"可投资性缺口"这个老主题又一次出现。**

---

## 第一部分:全候选排名表(四维打分,1-5 分)

维度:**E 结构弹性**(content-per-GPU 上升 / 渗透 0→1,越高越好)· **P 还没 price in**(过去 12 个月涨得越少、估值越合理,越高)· **Q 质地/护城河** · **K kill-risk 低**(越安全越高)。**重点看 P 那一列——它就是"还早不早"的量化。**

| 候选 | 是什么(大白话) | E | P | Q | K | 合计 | 过去 12 个月已涨 | 一句话裁决 |
|---|---|:-:|:-:|:-:|:-:|:-:|---|---|
| **玻璃基板(SKC 011790.KS)** | 芯片下面那块板,2026 从有机 ABF 转玻璃,AMD MI400 已用 | 5 | **4** | 3 | 2 | **14** | 仅约 +60%(从 4 月低点) | **全栈唯一真·早期拐点,本报告首选关注** |
| **TGV 激光钻孔设备(LPKF)** | 给玻璃打孔的唯一量产级设备(LIDE) | 5 | 1 | 4 | 2 | 12 | **+255% YTD** | 卡点对,但已先涨,小盘德股 |
| **CPO 激光/ELS(Coherent/Lumentum)** | CPO 必须的外置激光源,InP 被英伟达锁到 2027+ | 5 | 1 | 4 | 3 | 13 | 已 50x PE(见基线) | 敞口最好但估值已透支,等回调 |
| **CPO 光器件(Browave 3163.TW)** | CPO 的光纤阵列/shuffle box | 5 | 1 | 3 | 2 | 11 | **+510%** | 卡点真,但已涨 5 倍,2027 才放量 |
| **微流道散热(Corintis 私有)** | 把冷却液刻进硅片背面,3x 散热 | 5 | 5 | 4 | 2 | 16* | 买不到 | *真·最早,但私有,uninvestable |
| **CPO 光模块(中际旭创/新易盛/天孚)** | 机柜间光纤收发器 | 4 | 1 | 2 | 2 | 9 | **+750-950%** | 最经典"已涨疯",别碰 |
| **Fabrinet(FN)** | 光模块代工厂,CPO 也要它组装 | 3 | 3 | 3 | 4 | 13 | 约 +150%($232→$579) | 相对最理性的光链表达,但非纯弹性 |
| **800V GaN(Navitas NVTS)** | 800V 直供电的 GaN 功率板 | 4 | 1 | 2 | 1 | 8 | **+242%** | 叙事满分、基本面 $14 目标 vs $21 价,投机 |
| **scale-up retimer(Astera ALAB)** | XPU 互联的信号芯片 | 4 | 1 | 3 | 2 | 10 | $84→$338(约 4x),PE 230 | 已涨完,被整合风险 |
| **AEC 铜缆(Credo CRDO)** | 机架内有源铜缆 | 4 | 2 | 3 | 2 | 11 | 营收 +157%,股价已重估 | 转型光学有看点,但已不便宜 |
| **台系液冷(AVC 3017 / Auras 3324)** | 冷板/均热片 | 4 | 1 | 2 | 2 | 9 | AVC 约 +230%、Auras 约 2x | 已涨,且冷板会商品化 |
| **中国液冷(英维克 002837)** | 液冷整机龙头 | 4 | 1 | 2 | 1 | 8 | **+290% 后 Q1 净利 -82%** | 泡沫已现裂缝,回避 |
| **机器人减速器(绿的谐波 688017)** | 人形机器人关节谐波减速器 | 4 | 1 | 4 | 1 | 10 | **+273%** | 故事最性感、已炒、量产证伪未到 |
| **机器人执行器(三花/拓普)** | Optimus 旋转/直线执行器 | 4 | 2 | 3 | 2 | 11 | 三花约 +95% | 比减速器没那么疯,但仍是叙事赌 Tesla 量产 |
| **SMR 核电(Oklo/NuScale)** | 小型模块化核反应堆 | 3 | 3 | 1 | 1 | 8 | **已崩:$194→$56 / $57→$9** | 已涨完又崩 70-80%,典型 |
| **铀(Cameco CCJ)** | 铀矿 | 2 | 2 | 3 | 3 | 10 | 已到 $135 高点回落 $102 | 已被燃料叙事 price in |

> **看 P 列(还没 price in):全场只有玻璃基板(SKC)拿到 4 分,微流道拿 5 但买不到。其余几乎全是 1-2 分——这就是"全栈已重估"的量化铁证。**

---

## 第二部分:还算"早"的 Top 3-5(深一点)

### 🥇 #1 玻璃基板 —— 全栈唯一真·0→1 拐点(2026 正在发生)

- **是什么(大白话):** 芯片底下那块承载板(substrate)。过去十年用有机材料(味之素 ABF 膜),但 AI 超级芯片越做越大、越叠越多,有机板撑不住翘曲和散热。**玻璃基板是把那块板换成玻璃**——更平、更硬、能打更密的孔、散热更好。这是封装基底的一次范式迁移,跟当年"从引线键合到 CoWoS"是同级别的事。
- **为什么现在是拐点(不是 PPT 了):** 2026 年 1 月起,**Intel 在 Chandler 投了 >$10 亿的玻璃基板试产线已在为 18A/14A 出玻璃核;Absolics(SKC 子公司,AMAT 入股)的乔治亚州 $6 亿厂已量产爬坡到 2 万片/月,并开始给 AMD MI400 系列送量产样品。** 这是"真出货"信号,不是路演。(来源:[Wedbush](https://investor.wedbush.com/wedbush/article/tokenring-2026-1-8-the-glass-revolution-why-intel-and-skc-are-abandoning-organic-materials-for-the-next-generation-of-ai)、[MIT Tech Review](https://www.technologyreview.com/2026/03/13/1134230/future-ai-chips-could-be-built-on-glass/))
- **弹性来源:** 渗透率从约 0 → 起步,基数极小;每代芯片越大,玻璃用量越多(content 棘轮);叠加 ABF 缺口(2028 预计 -42%)的替代需求。**这是 `synthesis_top3` 里 SKC 拿 E=5/B=5 的同一个逻辑,现在多了"真出货"的催化。**
- **现在涨了多少 / 估值:** **关键差异——SKC(011790.KS)现价约 ₩123,700,只从 4 月低点涨约 60%**,而且 5 月刚做 1.2 万亿韩元配股扩产。**相对存储/光模块的 5-10 倍,这是全栈唯一还在 S 曲线"脚踝"、还没被炒到天上的真拐点。** 设备端 LPKF(打孔)已 +255% YTD、先跑了。
- **怎么买(可投资性缺口又来了):** **最干净的纯玩家(Absolics)是 SKC 子公司,你买不到纯的,只能买 SKC 母公司(被 CMP slurry、化工业务稀释——跟"Ajinomoto 食品稀释 ABF"一模一样的故事)。** 设备端可看 LPKF(德股小盘,但已先涨)、DISCO、Onto(metrology)、AMAT(太大稀释)。玻璃原片是 Schott/Corning/AGC/NEG(都被稀释)。
- **kill-risk(为什么 K 只给 2):** ①良率——玻璃易裂,laser-drilling 速度和"玻璃搬运机器人"还是瓶颈,大规模量产到百万片/月需要 2027-28;②味之素自己还在 +50% 扩 ABF,转换可能比 bull 慢;③SKC 是负债重的化工集团,执行/财务风险真实(刚配股说明缺钱)。**这是"前瞻赌注",不是确定性——但它是全栈唯一你还能在"早期"上车的。**

### 🥈 #2 CPO 激光 / ELS —— 卡点最硬,但被埋在已 50x 的 Coherent/Lumentum 里

- **是什么:** CPO(共封装光学)把光器件焊到交换芯片旁边,2026 年随英伟达 Quantum-X / Spectrum-X 真出货,**Feynman(2028)是 scale-up 光化的真拐点**。CPO 必须配"外置激光源(ELS)"——把发光的激光器单独做成可换模块。而所有激光都用磷化铟(InP)。
- **为什么还有看点:** **英伟达正在把全球顶级 EML/CW 激光产能预订到 2027 年以后,InP 外延产能被拉爆**——这是真·结构短缺、真·content 棘轮(每个 CPO 端口要更多激光)。Northland 估 ELS 单一市场就 >$10 亿/年。(来源:[photoncap](https://photoncap.net/p/the-silicon-photonics-light-source)、[Lumentum ELSFP](https://www.lumentum.com/en/products/external-laser-source-els-module-ultra-high-power-laser))
- **为什么 P 只给 1:** 卡点对,但**最好的上市表达 Coherent(约 51x non-GAAP)、Lumentum(约 50x 且 5 月从 $400 冲到 $970)已在基线里被钉死"估值透支、等回调"。** CPO 对它俩是利好(CPO 也要它们的激光),所以比纯光模块抗 CPO 风险——但"敞口好 ≠ 此刻估值好"。
- **裁决:** 这是"对的卡点、错的价格"。放 watchlist,等一次 AI capex air-pocket 回调再进。纯弹性的 Browave(光纤阵列)已涨 510%、2027 才放量,不追。

### 🥉 #3 Fabrinet(FN)—— 光链里相对最理性的弹性表达

- **是什么:** 全球光模块/光器件代工龙头(给 Coherent/Lumentum/Nvidia 组装),CPO 时代它照样接组装活。
- **为什么列入:** **过去 12 个月约 +150%($232→$579),相对中际旭创/新易盛的 +750-950%,FN 是光链里少数还没被炒到"市梦率"的。** Q3 FY26 营收 $12.1 亿(+39% YoY)、光通讯 +35%、HPC 环比 +25%。它是"架构无关"的——不管 CPO 还是可插拔赢,组装活都在它这。
- **kill-risk:** 代工毛利薄(约 12-13%),弹性不如纯器件;客户集中(Nvidia/Cisco)。**它是"睡得着的光链 beta",不是 10x 弹性王。** K 给 4(最稳),E 只给 3。

### 🏅 真·最早但买不到:微流道/两相散热(Corintis 等,私有)

- **是什么:** 把冷却液的微通道直接刻进硅片背面(仿叶脉),离热点只有几十微米。**微软已和瑞士 Corintis 验证 3x 冷板散热、峰值硅温降 65%。** 这是 `next_chokepoint_hunt` 里"散热是下一道墙"的最前沿表达——比冷板/快接头更前瞻。
- **为什么是真·最早:** Rubin Ultra Kyber 机架奔 600kW、单芯片 2000W,冷板物理极限将至,微流道是下一代。Corintis 刚 A 轮 $2400 万,还在量产前。(来源:[IEEE Spectrum](https://spectrum.ieee.org/microfluidics-cooling-ai-chips-corintis)、[DCD](https://www.datacenterdynamics.com/en/news/microsoft-partners-with-corintis-for-bio-inspired-in-chip-microfluidic-cooling/))
- **裁决:** **这是全栈"P 维度"唯一拿 5 分的——真早、content 从 0 起。但它私有,买不到。** 又一次"最硬的早期机会买不到"。能做的:盯它后续融资/被收购、关注上市供应链(谁做微流道的 manifold/工质),或当 VC 跟投标的(只用能承受归零的钱)。

---

## 第三部分:"已经涨完,别追"清单(附 12 个月倍数当铁证)

> **这是本报告最重要的一页——你天天看的博主喊的那些,基本都在这。涨了 3-10 倍之后再喊"确定性高",是周期顶最典型的声音。**

| 标的 | 12 个月已涨 | 现价/估值 | 为什么别追 |
|---|---|---|---|
| **中际旭创/新易盛/天孚** | **+750% ~ +950%**(2025/4-2026/4) | 旭创破千元 | 光模块会被 CPO 商品化,已炒到极致 |
| **Browave(3163.TW)** | **+510%**(52 周 164→1,315) | 现约 NT$1,020 | 卡点真,但 CPO 2027 才放量,已先涨 5 倍 |
| **AVC(3017.TW)** | 约 **+230%**(52 周低 713→2,360) | NT$2,360 | 冷板高 beta,英伟达多供应商化侵蚀份额 |
| **Auras(3324.TW)** | 约 **2x**(530→1,010,ATH 1,305) | 已从高点回落 | 同上,冷板商品化陷阱 |
| **英维克(002837)** | **+290%** 后 **Q1 净利 -82%** | 市值破千亿后跌停 | 泡沫已现裂缝,利润证伪 thesis |
| **绿的谐波(688017)** | **+273%**(52 周 113→450) | 约 ¥424 | 机器人量产证伪未到,纯叙事估值 |
| **三花智控(002050)** | 约 **+95%** | 约 ¥46 | 比减速器温和,但仍赌 Tesla Optimus 量产 |
| **Navitas(NVTS)** | **+242%**(1 年) | $21,分析师目标 **$14** | 营收小、亏损,叙事 vs 数字差几个量级 |
| **Astera Labs(ALAB)** | 约 **4x**($84→$338) | PE **230** | 已重估,GB200 删过一次 retimer 的整合风险 |
| **Credo(CRDO)** | 营收 **+157%**,股价大幅重估 | 约 $250 | 转光学有看点,但已不便宜 |
| **Oklo(OKLO)** | **崩了:$194→$56**(-71%) | $56 | 已涨完又崩,无营收的核电期权 |
| **NuScale(SMR)** | **崩了:$57→$9**(-84%) | $9.2,Citi 砍目标 | 同上,SMR 叙事退潮活标本 |
| **Cameco(CCJ)** | 已到 $135 回落 $102 | 已 price in | 铀燃料叙事已被定价 |
| **LPKF(玻璃打孔设备)** | **+255% YTD** | 已先涨 | 卡点对、但设备端已抢跑 |

---

## 第四部分:诚实的总结 —— 2026 年 6 月,还有真·早期的交易吗?

**裁决:基本没有了,只剩一个半。**

我们这个 project 反复撞到同一堵墙:**每挖一个"卡脖子",查 12 个月价格,发现已经涨 5-10 倍。** 这次再扫一轮 A-I 全部候选,结论一致——**整个 AI 基础设施栈,凡是"公开可买 + 被广泛认知"的,都已经 repriced 完了。** 你要找的"2023 年初的 HBM"(还没人信、还没涨、content 即将 0→1),在公开市场里已经被抽干。证据就在第三部分:光模块 +950%、Browave +510%、AVC +230%、绿的谐波 +273%、Navitas +242%……这些不是"机会被发现",是"机会已经被吃完"。

**唯一的例外是玻璃基板:** 它满足"真 0→1 拐点(2026 AMD/Intel 真出货)+ 最干净表达(SKC)只涨 60%、还没被炒疯"。这是全栈唯一你还能在 S 曲线脚踝上车的。**代价是:①纯玩家(Absolics)买不到,只能买被化工稀释的 SKC;②良率/量产是 2027-28 的事,前瞻执行风险真实;③SKC 财务弱(刚配股)。** 它不是"睡得着的确定性",是"高弹性前瞻赌注"——但如果你就是要爆发力、要 0→1,这是唯一还早的那个。

**"半个"例外是微流道散热:** P 维度全场唯一满分(真·最早),但私有、买不到——又是"可投资性缺口"。

**给你 80% 身家的实话:**
1. **不要把 80% 压进任何已涨 5-10 倍的东西**(光模块、台系液冷、机器人、SMR)——那是周期顶 FOMO,不是 conviction。SMR 已经给你演示了"涨完又崩 80%"(Oklo/NuScale)长什么样。
2. **如果你坚持要一个"还早"的高弹性 0→1,公开市场唯一选项是玻璃基板(SKC + 设备链),但用"能承受腰斩 + 前瞻可能落空"的心态、控制仓位,不是 all-in。**
3. **次选:把光链/CPO 激光(Coherent/Lumentum)放 watchlist,等 AI capex air-pocket 回调再进——它们卡点最硬,只是此刻 50x 太贵。**
4. **真正最早的(微流道)买不到——盯它融资/上市供应链,或当 VC 跟投。**
5. **总开关不变:AI capex 指引的二阶导。一旦转负,所有这些先杀估值——届时才是买玻璃/激光的更好时点。**

> **一句话钉墙上:2026 年 6 月,AI 硬件栈的"早期交易"已经基本被抽干——你不是在故事开头,是在第七、八章。公开市场唯一还在 S 曲线脚踝的真 0→1 是玻璃基板(SKC),但它是前瞻赌注不是确定性;最硬的卡点(CPO 激光)太贵要等回调;最早的(微流道)买不到。要爆发力可以,但别把"已经涨完"当成"确定性高",更别 all-in——SMR 刚演示了那条路怎么 -80%。**

---

## 资料来源(关键 URL)

**玻璃基板:** [Wedbush: Intel/SKC 弃有机转玻璃](https://investor.wedbush.com/wedbush/article/tokenring-2026-1-8-the-glass-revolution-why-intel-and-skc-are-abandoning-organic-materials-for-the-next-generation-of-ai)、[MIT Tech Review: 玻璃 AI 芯片](https://www.technologyreview.com/2026/03/13/1134230/future-ai-chips-could-be-built-on-glass/)、[SemiEngineering: Race to Glass](https://semiengineering.com/the-race-to-glass-substrates/)、[SKC 1.2 万亿配股](https://en.sedaily.com/finance/2026/05/12/skc-raises-12-trillion-won-to-fund-glass-substrate-push)、[TGV/LPKF LIDE](https://photoncap.net/p/the-glass-beneath-ai-chips-the-255)。
**CPO/光:** [NVIDIA Vera Rubin CPO 时代(Radiant)](https://radiant.co/blog/nvidia-vera-rubin-ultra-ushers-in-the-cpo-era)、[SemiAnalysis CPO](https://newsletter.semianalysis.com/p/co-packaged-optics-cpo-book-scaling)、[InP/ELS 激光短缺(photoncap)](https://photoncap.net/p/the-silicon-photonics-light-source)、[NVIDIA CPO 伙伴生态(含 Browave/TFC)](https://developer.nvidia.com/blog/how-industry-collaboration-fosters-nvidia-co-packaged-optics/)、[Fabrinet Q3 FY26](https://stockstotrade.com/news/credo-technology-group-holding-ltd-crdo-news-2026_06_11/)。
**散热:** [Corintis 微流道(IEEE)](https://spectrum.ieee.org/microfluidics-cooling-ai-chips-corintis)、[微软 Corintis(DCD)](https://www.datacenterdynamics.com/en/news/microsoft-partners-with-corintis-for-bio-inspired-in-chip-microfluidic-cooling/)、[Boyd NVL72](https://www.boydcorp.com/uncategorized/boyd-validated-for-nvidia-gb200-nvl72-recommended-vendor-list.html)、英维克 [跌停/泡沫(钛媒体)](https://www.tmtpost.com/7961257.html)。
**800V/功率:** [Navitas GTC 2026 800V-6V](https://navitassemi.com/navitas-debuts-revolutionary-800-v-6-v-power-delivery-board-at-nvidia-gtc-2026/)、[NVIDIA 800VDC 架构](https://developer.nvidia.com/blog/nvidia-800-v-hvdc-architecture-will-power-the-next-generation-of-ai-factories/)。
**scale-up:** Astera/Credo/Navitas 价格 via Yahoo Finance / stockanalysis / marketbeat(2026/6/11 口径)。
**机器人:** 绿的谐波/三花/拓普(东方财富,2026/1-5)。
**核电:** Oklo/NuScale/Cameco/GEV 价格 via Yahoo/Robinhood/Motley Fool(2026/6 口径,[NuScale -20%](https://www.fool.com/investing/2026/06/04/nuscale-is-down-20-is-it-finally-time-to-buy/))。

> **质量审查记录(QC):** 本文为单轮广筛 UPDATE(玻璃/CPO/800V/液冷/scale-up/机器人/核电 7 路 + 上游),价格为 2026/6/11 多源口径需终端复核;12 个月倍数取 52 周低点/区间,方向性看;第三方 TAM/份额为机构估算。[待 critical-thinker 红队 + research-reviewer 核查]。
