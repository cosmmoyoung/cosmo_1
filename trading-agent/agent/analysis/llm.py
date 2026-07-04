"""LLM 分析层:把行情、规则信号、新闻、大佬发言全部喂给 Claude,
让它站在"你的投资主题"的视角做交叉分析。

没有 ANTHROPIC_API_KEY 时降级为简单模板汇总,流水线不中断。
"""
import json

SYSTEM_PROMPT = """你是一位为个人投资者服务的市场研究助理。你收到四类材料:
1. 投资主题(用户的核心思路)
2. 今日行情快照(watchlist 全量)
3. 规则引擎筛出的异动信号
4. 叙事材料(科技大佬/VC 的公开发言、新闻标题)

你的任务是写一份中文晨报分析,结构如下:
## 今日叙事焦点
叙事材料中和投资主题相关的 2-4 个要点,注明来源。区分"事实"和"观点"。

## 价格与叙事的交叉验证
逐条评估规则信号:这个异动有没有叙事支撑?是主题内的结构性变化,
还是普通波动?明确说出你的置信度(高/中/低)和理由。

## 关注建议(不是投资建议)
最多 3 条,每条格式:标的 / 方向(关注做多机会|关注风险|继续观察)/
一句话理由 / 建议的下一步动作(如"等财报确认""查 HBM 定价数据")。

## 反方视角
用两三句话攻击你自己上面的判断,指出最可能错在哪。

原则:宁可说"信号不足",不要编造;所有引用注明来源;
不使用"必涨""抄底"等词;你输出的是研究线索,不是交易指令。"""


def analyze(cfg: dict, market: list[dict], rule_signals: list[dict],
            news: list[dict], x_posts: list[dict]) -> dict:
    """返回 {text: 分析正文, mode: 'llm'|'rules-only'}"""
    payload = _build_payload(cfg, market, rule_signals, news, x_posts)

    if cfg["env"]["anthropic_key"]:
        try:
            return {"text": _ask_claude(cfg, payload), "mode": "llm"}
        except Exception as e:
            print(f"[warn] LLM 调用失败,降级为规则汇总: {e}")

    return {"text": _fallback_summary(rule_signals, news, x_posts), "mode": "rules-only"}


def _build_payload(cfg, market, rule_signals, news, x_posts) -> str:
    return json.dumps({
        "投资主题": cfg["thesis"],
        "今日行情": [
            {k: r[k] for k in ("symbol", "theme", "price", "change_pct", "year_high", "year_low")}
            for r in market
        ],
        "规则信号": rule_signals,
        "大佬发言": [
            {k: p[k] for k in ("name", "why", "text", "created_at")} for p in x_posts
        ],
        "新闻标题": [
            {k: n.get(k, "") for k in ("source", "title", "summary", "published")}
            for n in news[:25]
        ],
    }, ensure_ascii=False, indent=1)


def _ask_claude(cfg: dict, payload: str) -> str:
    import anthropic

    client = anthropic.Anthropic()  # 自动读 ANTHROPIC_API_KEY
    msg = client.messages.create(
        model=cfg["llm"]["model"],
        max_tokens=cfg["llm"]["max_tokens"],
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": f"今日材料如下:\n{payload}"}],
    )
    return msg.content[0].text


def _fallback_summary(rule_signals, news, x_posts) -> str:
    """没有 LLM key 时的朴素汇总:只罗列事实,不做判断。"""
    lines = ["> ⚠️ 未配置 ANTHROPIC_API_KEY,以下为规则引擎的机械汇总,无分析判断。\n"]
    lines.append("## 规则信号一览")
    if rule_signals:
        for s in rule_signals:
            lines.append(f"- **{s['symbol']}**({s['theme']})[{s['kind']}] {s['detail']}")
    else:
        lines.append("- 今日无触发规则的异动。")
    if x_posts:
        lines.append("\n## 追踪人物最新发言(未分析)")
        for p in x_posts[:10]:
            lines.append(f"- **{p['name']}**: {p['text'][:120]}")
    if news:
        lines.append("\n## 新闻标题(未分析)")
        for n in news[:10]:
            lines.append(f"- [{n['source']}] {n['title']}")
    return "\n".join(lines)
