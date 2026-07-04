"""规则引擎:不花一分钱的机械筛选,负责"什么值得看"。

它不判断买卖,只把异动挑出来交给 LLM(或你自己)做判断。
每条信号:{symbol, theme, kind, detail, price, change_pct}
"""


def screen_market(market: list[dict], rules: dict) -> list[dict]:
    signals = []
    for r in market:
        pct = r.get("change_pct") or 0.0
        price, hi, lo = r.get("price"), r.get("year_high"), r.get("year_low")

        if abs(pct) >= rules["big_move_pct"]:
            direction = "上涨" if pct > 0 else "下跌"
            signals.append(_sig(r, "单日异动", f"单日{direction} {abs(pct):.1f}%"))

        if price and hi:
            off_high = (hi - price) / hi * 100
            if off_high <= rules["near_52w_high_pct"]:
                signals.append(_sig(r, "接近新高", f"距 52 周高点仅 {off_high:.1f}%"))
            elif off_high >= rules["off_52w_high_pct"]:
                signals.append(_sig(r, "深度回调", f"较 52 周高点回撤 {off_high:.0f}%"))

        avg50, avg200 = r.get("avg50"), r.get("avg200")
        if price and avg50 and avg200 and avg200 > 0:
            if price < avg50 < avg200 * 1.02 and price > avg200:
                signals.append(_sig(r, "均线位置", "价格跌破 50 日线、逼近 200 日线"))

    return signals


def _sig(row: dict, kind: str, detail: str) -> dict:
    return {
        "symbol": row["symbol"], "theme": row.get("theme", ""),
        "kind": kind, "detail": detail,
        "price": row.get("price"), "change_pct": row.get("change_pct"),
    }
