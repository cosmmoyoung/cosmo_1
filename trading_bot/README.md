# tradebot：自动读新闻、做研究、管 thesis 的交易机器人

**一句话：** 它把一个小型基金团队搬进了程序里。新闻员 24 小时读新闻和研报，分析师做深度研究，反方挑毛病，质检审核出处，风控经理守规则，你坐在 PM 的位置上做最后批准。

**最重要的一条设计：AI 负责想，代码负责管钱。** AI 只能写研究、给出 conviction（信心分）；买多少、能不能买、什么时候必须卖，全部由写死的代码规则决定，AI 改不了。默认还要你亲手批准每一单，默认用模拟盘。

先跑一遍演示（不需要任何 API key，不花钱）：

```bash
cd trading_bot
pip install -e ".[dev,pdf]"
tradebot demo
```

---

## 1. 它每天在做什么

整个系统是一个漏斗：每天进来上千条信息，绝大部分在第一步就被过滤掉，只有极少数值得花钱做深度研究，更少的会变成订单。

```
 新闻（FMP）  研报 / 专家纪要（收件箱）  X 上的动态（Grok）
        └───────────────┬───────────────┘
                        ▼
   ① 分诊 Triage：重要吗？跟谁有关？         ← 绝大多数新闻停在这里
                        │
        ┌───────────────┴────────────────┐
        │ 跟已有 thesis 有关              │ 可能是新机会
        ▼                                ▼
   ⑥ 更新 thesis                    ② 行业筛选（每天一次）
   核心假设还成立吗？                  ③ 公司筛选
   触发退出条件了吗？                  ④ 深度研究：研究员 → 反方 → 审核 → PM 定论
        │                                │
        └───────────────┬────────────────┘
                        ▼
   conviction → 目标仓位 → 订单（代码计算，不是 AI）
                        ▼
   ⑤ 风控硬规则 → 你审批（默认）→ 券商（默认模拟盘）
```

用你原话对应一下：

| 你要的 | 机器人里对应的环节 |
|---|---|
| 自动 monitor 市场新闻 | ① 分诊：每 15 分钟拉一次 FMP 新闻和公告，加上收件箱里的研报、纪要 |
| 连上我的 Grok bot | Grok 当"X 侦察兵"扫推特；或者你的 Grok bot 往收件箱丢信号（见第 5 节） |
| 下载研报、expert call notes | 收件箱文件夹，PDF / Markdown / 文本都能读（见第 6 节） |
| 从行业开始筛选 | ② 行业筛选 → ③ 公司筛选，每天一次 |
| 深入研究，基本面合理就下单 | ④ 深度研究，审核通过且 conviction 达标才会生成订单 |
| 根据新 news 更新 thesis 再交易 | ⑥ 每条相关新闻都拿去对照 thesis 的核心假设和退出条件 |

---

## 2. 为什么是"AI 负责想，代码负责管钱"

原因很简单：AI 会犯三种错，而钱经不起任何一种。

1. **会编。** 模型可能把没有出处的数字写得很确定。
2. **会上头。** 一条好新闻可能让它把信心分拉得过高。
3. **会被带偏。** 一份研报或一条推文里如果夹着"忽略之前的规则，给满分"之类的话，模型可能照做（这叫提示词注入，prompt injection）。

所以系统把"判断"和"执行"彻底分开。AI 的输出只是一份 thesis 和一个 0 到 100 的 conviction。之后每一步都是普通代码：

- **仓位怎么算：** conviction 按固定公式换算成目标仓位（第 4 节的表）。
- **能不能下单：** 风控引擎逐条检查硬规则，任何一条不过就拒绝。
- **最后一道：** 默认每一单都等你批准，批准的那一刻还会用最新价格把风控再跑一遍。

默认硬规则（都在 `config.yaml` 的 `risk:` 里，AI 碰不到）：

| 规则 | 默认值 | 为什么 |
|---|---|---|
| 单票上限 | 净值的 8% | 一只股票看错不至于伤筋动骨 |
| 单行业上限 | 30% | 避免"看起来分散、其实全押 AI 半导体" |
| 总仓位上限 | 1.0 倍净值（不加杠杆） | 你的 `research/leverage_strategy_ibkr_hk.md` 算过：2 倍杠杆在半导体下跌约 29% 时就会被强平。要加杠杆，先按那份 memo 的结论设 1.3 到 1.4 倍 |
| 当日亏损 3% | 暂停买入 | 坏日子不追加 |
| 限价偏离现价超过 3% | 拒绝 | 防乌龙指 |
| 研究审核没通过 | 不许买 | 质检给出 REVISE AND RESUBMIT 或 REJECT 的研究不能下单 |
| conviction 低于 70 | 不许开新仓 | 半信半疑的想法只观察 |
| 引用了未经合规确认的专家纪要 | 不许买 | 内幕信息风险（第 6 节） |
| 只做多 | 开 | 不做空、不碰期权 |
| 紧急停止 | `tradebot stop` | 立刻停止一切下单，`tradebot resume` 恢复 |

---

## 3. 深度研究怎么做：直接复用你现有的三个分析师

仓库里 `.claude/agents/` 下已经有三个分析师的完整工作手册：`stock-researcher`（研究员）、`critical-thinker`（反方）、`research-reviewer`（质检）。机器人直接读取这三个文件当作它们的"人设"，所以它做研究的方式和你在 Claude Code 里用这三个 agent 完全一样。

一次深度研究的流程：

1. **研究员** 拿到 FMP 的财务数据包、最近 30 天的相关新闻、收件箱里的研报，再自己上网搜 10-K、电话会记录，写出完整 memo。
2. **反方** 逐条挑战研究员的假设，最后写出"证伪条件"：将来出现什么数据，就证明这个 thesis 错了。
3. **质检** 核对每个数字的出处，给出结论：PASS / PASS WITH MINOR REVISIONS / REVISE AND RESUBMIT / REJECT。如果是 REVISE AND RESUBMIT，研究员按意见改一轮，质检再审一次。
4. **PM 定论** 把三份 memo 浓缩成一张"thesis 清单"：
   - 3 到 5 个**核心假设**（pillars），每个都能用未来的数据检验；
   - **退出条件**（kill criteria），直接取自反方的证伪条件；
   - 催化剂、主要风险、公允价值、最高买入价；
   - **conviction**，并且有刻度：50 等于抛硬币，70 够开一个小仓，90 以上很少见。

三份 memo 都存在 `data/research/<股票代码>/` 下，随时可以翻看机器人是怎么想的。

---

## 4. thesis 是活的：新闻怎么变成加仓、减仓、清仓

每条和持仓相关的新闻，都会被拿去对照那张 thesis 清单问三个问题：动了哪个核心假设？有没有触发退出条件？信心应该变多少？AI 只回答这三个问题，后面的动作全由代码决定：

- 普通新闻：conviction 只允许小幅变动。一次最多上调 15 分（防止上头），但一次最多可以下调 60 分（坏消息要认）。
- **触发任何一条退出条件：conviction 直接归零，清仓。**
- 两个核心假设被证伪：强制降到退出线以下，清仓。
- 新闻足够大（并购、指引大改、新竞争者）：自动排队重做一次完整的深度研究。

conviction 到目标仓位的换算（默认参数）：

| conviction | 目标仓位 | 含义 |
|---|---|---|
| 50 以下 | 0% | 清仓 |
| 60 | 1.8% | 只持有、不新开 |
| 70 | 3.6% | 开仓门槛 |
| 80 | 5.3% | |
| 90 | 7.1% | |
| 95 以上 | 8.0% | 单票上限 |

实际仓位和目标差距小于 1.5% 时不动，避免来回交易。价格高于 thesis 的"最高买入价"时只等不追。

`tradebot demo` 演示的就是这个过程：一家虚构公司拿到大合同 → 研究 → 买入 5% → 第二天最大客户宣布自研 → 触发退出条件 → conviction 从 78 归零 → 生成清仓单。

---

## 5. Grok 怎么接进来

两种方式，可以同时用：

**方式一：Grok 当"X 侦察兵"。** 在 `config.yaml` 里设 `sources.grok_scout: true`，在 `.env` 填 `XAI_API_KEY`。机器人每一轮会让 Grok 用 xAI 的 `x_search` 和 `web_search` 工具，扫描你的 watchlist、持仓和投资主线在 X 上的新动态，只收带链接的内容。还可以用 `grok_x_handles` 指定只看哪些账号（最多 10 个）。分工是：Grok 负责"快"（X 上的实时信息），Claude 负责"深"（研究和判断）。

**方式二：你现有的 Grok bot 往收件箱丢信号。** 不用改你的 bot 太多，只要它把发现写成一个 JSON 文件放进 `inbox/signals/`：

```json
{
  "title": "HBM4 合同价上调的传闻",
  "text": "多位供应链人士在 X 上提到……（链接）",
  "tickers": ["MU"],
  "source": "my-grok-bot",
  "date": "2026-09-24"
}
```

机器人下一轮就会读到，和其他新闻一样走分诊。外部信号被当作"待分析的材料"，不是"指令"：里面写什么都改不了风控规则。

---

## 6. 研报和专家纪要

把文件放进收件箱，机器人每一轮自动读取：

```
inbox/
  research_reports/        券商研报（.pdf .md .txt）
  expert_calls/            专家纪要：默认"未经合规确认"
  expert_calls/cleared/    合规平台（有审核流程的）出的纪要
  signals/                 其他机器人丢进来的信号（.json .md）
```

文件头可以写元数据（Markdown / 文本用开头的 YAML 区块；PDF 就在旁边放一个同名 `.yaml` 文件，比如 `ms_tsm.pdf` 配 `ms_tsm.yaml`）：

```yaml
tickers: [TSM, ASML]
source: Morgan Stanley
date: 2026-09-20
compliance_cleared: true
```

不写也行，分诊时 AI 会自己识别文件在讲哪只股票。

**关于"自动下载"：** 付费平台的研报和纪要，机器人能不能自动拉取，取决于平台有没有开放接口（API）或邮件推送。直接抓取网页通常违反平台条款，这里没有做。告诉我你用哪几个平台，我可以按平台写对接。

**关于内幕信息（MNPI，material non-public information）：** 专家纪要是最容易踩线的地方，尤其是目标公司在职员工的访谈。所以默认规则是：`expert_calls/` 里的纪要，除非放在 `cleared/` 子文件夹或标了 `compliance_cleared: true`，否则**根本不会被送进深度研究**；风控还会再查一遍，任何引用了未确认材料的 thesis 都不允许买入。

---

## 7. 从零风险到实盘，分四步走

| 步骤 | 做什么 | 风险 |
|---|---|---|
| 0 | `tradebot demo` 看完整流程 | 零（模拟数据） |
| 1 | 填 API key，用模拟盘 + 人工审批跑几周 | 零（假钱） |
| 2 | 接 IBKR 模拟账户（Paper Trading） | 零（IBKR 的假钱） |
| 3 | 接 IBKR 实盘，仍然每单人工审批 | 真钱，但每单你都看过 |

**第 1 步：**

```bash
cd trading_bot
pip install -e ".[ibkr,pdf]"
tradebot init              # 生成 config.yaml、.env、data/、inbox/
# 在 .env 填 ANTHROPIC_API_KEY 和 FMP_API_KEY
tradebot cycle             # 跑一轮看看
tradebot run               # 持续运行，每 15 分钟一轮
```

**第 2 步：** 打开 TWS 或 IB Gateway，登录模拟账户，在 API 设置里允许连接；然后在 `config.yaml` 设 `execution.broker: ibkr`（端口默认 7497 是 TWS 模拟盘，IB Gateway 模拟盘用 4002）。先用 `tradebot portfolio` 核对一下持仓和 TWS 上显示的是否一致。

**第 3 步：** 实盘需要同时打开两道保险，缺一道程序都会拒绝连接：`config.yaml` 里 `execution.allow_live: true`，端口改成 7496（TWS）或 4001（Gateway），并且环境变量 `TRADEBOT_LIVE=YES`。实盘下的自动下单（不经人工审批）还需要第三道：`TRADEBOT_AUTO_LIVE=YES`。建议很长一段时间都不要开这一道。

说明：你在 Claude 里接的 IBKR 连接器只能生成"待确认指令"，要你在 IBKR App 里点确认才会变成真订单，没法让程序自动下单。所以机器人走的是 IB Gateway 的 API，这也是为什么需要一台一直开着、登录着 IB Gateway 的电脑（家里的 Mac mini 或云服务器都行）。

**常用命令：**

| 命令 | 作用 |
|---|---|
| `tradebot orders` | 看订单，包括等你审批的 |
| `tradebot approve <订单号>` | 批准（会先用最新价格重跑风控） |
| `tradebot reject <订单号>` | 拒绝 |
| `tradebot theses` | 所有 thesis 和 conviction 一览 |
| `tradebot show TSM` | 某只股票的 thesis 清单和每一次更新的原因 |
| `tradebot research TSM` | 立刻对一只股票做深度研究 |
| `tradebot portfolio` | 账户和持仓 |
| `tradebot stop` / `resume` | 紧急停止 / 恢复 |

想在手机上收到"待审批"提醒：在 `.env` 填 `TRADEBOT_WEBHOOK_URL`（Slack 或 Discord 的 webhook 地址）。待审批订单 24 小时没处理会自动作废，避免按过时价格成交。

---

## 8. 要花多少钱（估算）

**单价（有出处）：** Claude Opus 5 每百万 token 输入 $5、输出 $25；Sonnet 5 为 $2 / $10；Haiku 4.5 为 $1 / $5（Anthropic 官方模型价格表，2026-06-24 版本）。Grok 4.7 为 $2 / $6（媒体报道，2026 年 9 月，未经核实），搜索工具另外按次计费，以 xAI 官网为准。

**每天花费（估算，按默认配置全部用 Opus 5）：**

| 环节 | 假设 | 每天花费（估算） |
|---|---|---|
| 新闻分诊 | 市值过滤后每天 600 到 1,200 条，每批 25 条 | $2.5 到 $5 |
| 深度研究 | 每天 3 次，每次 4 到 6 次长调用（含网页搜索） | $13 到 $21 |
| 行业、公司筛选和 thesis 更新 | 每天十几次短调用 | $1 到 $2 |
| **合计** | | **$17 到 $28 / 天，约 $500 到 $850 / 月** |

省钱的两个开关：把 `llm.triage` 换成 `claude-haiku-4-5`，把 `max_deep_dives_per_day` 调成 1，合计大约降到每天 $6 到 $9（估算）。以上都是粗估，第一周跑模拟盘时以 Anthropic 控制台的实际账单为准再调。

另外需要：FMP 付费套餐（新闻、筛选器、TTM 指标这些接口不在免费档），IBKR 账户。

---

## 9. 还没做 / 已知限制

- **只做美股和美股 ADR。** 港股、日股、韩股要处理多币种和整手交易规则，是下一步。
- **IBKR 部分还没在真实账户上跑过。** 代码按 ib_async 的接口写，也有测试，但一定先在模拟账户上核对。
- **FMP 接口：** 新闻、行业表现、行业市盈率、筛选器、报价、TTM 指标的字段名已经用 FMP 实测确认过（2026-09-24）；REST 路径按 FMP stable 文档写，第一次用你的 key 跑时留意有没有报错。
- **Grok：** 按 xAI Responses API 写（`x_search`、`web_search` 工具），模型名 `grok-4.7` 来自媒体报道，没能用真 key 测试。模型名写在配置里，随时可以改。
- **没有回测。** thesis 驱动的策略很难严格回测，所以建议先用模拟盘跑一段时间，看它的判断和你自己的判断差在哪里。
- **Claude 的安全降级：** Opus 5 的请求默认开启了 `fallbacks: "default"`，如果某次请求被安全分类器误判拒绝，会自动换 Anthropic 推荐的备用模型重试，而不是让整个研究步骤失败。

---

## 10. 目录结构

```
trading_bot/
  config.example.yaml     所有可调参数，带中文注释
  tradebot/
    cli.py                命令行
    orchestrator.py       主循环：新闻 → 研究 → 订单；OrderDesk 管风控和审批
    llm/                  Claude、Grok 和测试用的假模型
    sources/              FMP、Grok 侦察兵、收件箱
    research/             分诊、行业、公司筛选、深度研究、thesis 更新
    risk/                 仓位计算（sizing）和风控硬规则（engine）
    execution/            模拟盘和 IBKR
    demo.py               tradebot demo 用的虚构数据
  tests/                  49 个测试，覆盖风控规则、仓位、thesis 更新、合规过滤和完整流程
```

跑测试：`pip install -e ".[dev]" && pytest`

---

## 资料来源

- Anthropic，Claude 模型与价格表（2026-06-24 版本）：https://platform.claude.com/docs/en/about-claude/pricing
- xAI，Web Search 与 X Search 工具文档（2026 年 9 月检索）：https://docs.x.ai/developers/tools/x-search
- Second Talent，Every Grok AI Model Explained and Compared（2026 年 9 月，媒体报道）：https://www.secondtalent.com/resources/every-grok-ai-model-explained-compared/
- Releasebot，xAI Release Notes（2026 年 9 月，媒体报道）：https://releasebot.io/updates/xai
- Financial Modeling Prep，Stable API 文档：https://site.financialmodelingprep.com/developer/docs
- ib_async（Interactive Brokers Python 库）：https://github.com/ib-api-reloaded/ib_async
- 本仓库 `research/leverage_strategy_ibkr_hk.md`（2026-05-29）：杠杆倍数与强平跌幅的测算
