"""大盘体温计 | Market Index Pulse"""

from nanobot.agent.tools import tool
import akshare as ak


@tool
async def skill_index_pulse() -> str:
    """
    获取大盘数据，判断市场情绪（极度乐观/观望/恐慌）。
    Fetch index data and assess market sentiment (euphoria / neutral / panic).

    Returns:
        大盘情绪报告，含主要指数涨跌、成交量、情绪标签
    """
    index_data = {}
    index_codes = {
        "上证指数": "000001",
        "深证成指": "399001",
        "创业板指": "399006",
        "科创50": "000688",
        "沪深300": "000300",
    }

    for name, code in index_codes.items():
        try:
            df = ak.stock_zh_index_daily(
                symbol=f"sh{code}" if code.startswith("000") else f"sz{code}"
            )
            if df is not None and not df.empty:
                last = df.iloc[-1]
                prev = df.iloc[-2] if len(df) > 1 else last
                close = float(last.get("close", 0))
                prev_close = float(prev.get("close", close))
                change_pct = (close - prev_close) / prev_close * 100 if prev_close > 0 else 0
                index_data[name] = {
                    "value": round(close, 2),
                    "change_pct": round(change_pct, 2),
                }
        except Exception:
            continue

    try:
        market_df = ak.stock_zh_a_spot_em()
        if market_df is not None and not market_df.empty:
            total_stocks = len(market_df)
            up_count = len(market_df[market_df["涨跌幅"] > 0])
            down_count = len(market_df[market_df["涨跌幅"] < 0])
            flat_count = total_stocks - up_count - down_count
            limit_up = len(market_df[market_df["涨跌幅"] >= 9.9])
            limit_down = len(market_df[market_df["涨跌幅"] <= -9.9])
            avg_change = market_df["涨跌幅"].mean()
            total_amount = market_df["成交额"].sum()
        else:
            up_count = down_count = flat_count = limit_up = limit_down = 0
            avg_change = 0
            total_amount = 0
            total_stocks = 0
    except Exception:
        up_count = down_count = flat_count = limit_up = limit_down = 0
        avg_change = 0
        total_amount = 0
        total_stocks = 0

    if up_count + down_count > 0:
        up_ratio = up_count / (up_count + down_count) * 100
    else:
        up_ratio = 50

    if up_ratio > 70 and avg_change > 1.5 and limit_up > 50:
        sentiment = "极度乐观"
        sentiment_emoji = "🔴"
    elif up_ratio > 55 and avg_change > 0.5:
        sentiment = "偏乐观"
        sentiment_emoji = "🟠"
    elif up_ratio > 45:
        sentiment = "观望"
        sentiment_emoji = "🟡"
    elif up_ratio > 30:
        sentiment = "偏悲观"
        sentiment_emoji = "🔵"
    else:
        sentiment = "恐慌"
        sentiment_emoji = "🔴"

    index_lines = []
    for name, data in index_data.items():
        arrow = "🔺" if data["change_pct"] > 0 else "🔻" if data["change_pct"] < 0 else "➖"
        index_lines.append(f"  {arrow} {name}: {data['value']:.2f} ({data['change_pct']:+.2f}%)")

    if not index_lines:
        index_lines = ["  数据获取中..."]

    if total_amount > 1e12:
        amount_str = f"{total_amount / 1e12:.2f} 万亿"
    elif total_amount > 1e8:
        amount_str = f"{total_amount / 1e8:.2f} 亿"
    else:
        amount_str = f"{total_amount:.0f}"

    report = f"""🌡️ 大盘体温计 | Market Pulse

━━━━━━━━━━━━━━━━━━━━━━━━
{sentiment_emoji} 市场情绪: {sentiment}
━━━━━━━━━━━━━━━━━━━━━━━━
  上涨: {up_count} 家  下跌: {down_count} 家  平盘: {flat_count} 家
  涨停: {limit_up} 家  跌停: {limit_down} 家
  平均涨跌: {avg_change:+.2f}%
  上涨占比: {up_ratio:.1f}%

━━━━━━━━━━━━━━━━━━━━━━━━
📊 主要指数 | Major Indices
━━━━━━━━━━━━━━━━━━━━━━━━
{chr(10).join(index_lines)}

━━━━━━━━━━━━━━━━━━━━━━━━
💰 成交概况 | Volume
━━━━━━━━━━━━━━━━━━━━━━━━
  总成交额: {amount_str}

━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ 失效条件 | Invalidation
━━━━━━━━━━━━━━━━━━━━━━━━
  1. 情绪指标基于当日盘面，次日可能快速反转
  2. 极端行情下情绪指标可能失真
  3. 需结合消息面和政策面综合判断
"""
    return report
