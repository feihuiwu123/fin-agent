"""综合 K 线操作建议 | Integrated Chart Decision"""

from nanobot.agent.tools import tool

from finagent.adapters.akshare_adapter import AKShareAdapter
from finagent.engine.indicators import calc_all_indicators
from finagent.engine.key_levels import calc_key_levels, calc_pivot_points
from finagent.engine.volume_patterns import classify_volume_pattern


@tool
async def skill_decision(symbol: str, period: str = "daily") -> str:
    """
    综合趋势、量能、逻辑，输出操作建议 + 止盈止损位 + 盈亏比。
    Combine trend, volume, and logic to output: action + TP/SL levels + R:R ratio.

    Args:
        symbol: 股票代码 | Stock code
        period: 周期 | Timeframe
    Returns:
        操作建议（持有/加仓/减仓/清仓）+ 价位 + 盈亏比 + 逻辑回检
    """
    adapter = AKShareAdapter()
    df = adapter.get_kline(symbol, period=period, count=250)

    if df.empty:
        return f"❌ 无法获取 {symbol} 的 K 线数据"

    df = calc_all_indicators(df)
    last = df.iloc[-1]
    close = last["close"]

    key_levels = calc_key_levels(df)
    pivots = calc_pivot_points(df)

    vol_patterns = classify_volume_pattern(df)
    current_vol_pattern = vol_patterns[-1] if vol_patterns else "常态"

    ma5 = last.get("MA5", 0)
    ma10 = last.get("MA10", 0)
    ma20 = last.get("MA20", 0)
    ma60 = last.get("MA60", 0)

    if ma5 > ma10 > ma20 > ma60:
        ma_alignment = "多头"
        ma_score = 3
    elif ma5 < ma10 < ma20 < ma60:
        ma_alignment = "空头"
        ma_score = -3
    else:
        ma_alignment = "纠结"
        ma_score = 0

    dif = last.get("DIF", 0)
    dea = last.get("DEA", 0)
    macd_score = 1 if dif > dea else -1

    rsi = last.get("RSI", 50)
    if rsi > 70:
        rsi_score = -1
    elif rsi < 30:
        rsi_score = 1
    else:
        rsi_score = 0

    vol_score = (
        1 if current_vol_pattern == "倍量" else (-1 if current_vol_pattern == "缩倍量" else 0)
    )

    total_score = ma_score + macd_score + rsi_score + vol_score

    support = key_levels["support"]
    resistance = key_levels["resistance"]

    if total_score >= 3:
        action = "加仓"
        action_emoji = "🟢"
        sl = support[0] if support else close * 0.95
        tp = resistance[-1] if resistance else close * 1.10
    elif total_score >= 1:
        action = "持有"
        action_emoji = "🟡"
        sl = support[0] if support else close * 0.93
        tp = resistance[-1] if resistance else close * 1.08
    elif total_score <= -3:
        action = "清仓"
        action_emoji = "🔴"
        sl = close * 0.97
        tp = resistance[0] if resistance else close * 1.03
    else:
        action = "减仓"
        action_emoji = "🟠"
        sl = support[0] if support else close * 0.95
        tp = resistance[0] if resistance else close * 1.05

    risk = abs(close - sl)
    reward = abs(tp - close)
    rr_ratio = reward / risk if risk > 0 else 0

    report = f"""🎯 K线综合决策 | Chart Decision — {symbol}

━━━━━━━━━━━━━━━━━━━━━━━━
{action_emoji} 操作建议: {action}
━━━━━━━━━━━━━━━━━━━━━━━━
  现价: {close:.2f}
  止盈位: {tp:.2f}
  止损位: {sl:.2f}
  盈亏比: 1:{rr_ratio:.2f}

━━━━━━━━━━━━━━━━━━━━━━━━
📊 评分明细 | Scoring Breakdown
━━━━━━━━━━━━━━━━━━━━━━━━
  均线排列({ma_alignment}): {ma_score:+d}
  MACD({"金叉" if macd_score > 0 else "死叉"}): {macd_score:+d}
  RSI({rsi:.1f}): {rsi_score:+d}
  量能({current_vol_pattern}): {vol_score:+d}
  ─────────
  总分: {total_score:+d}

━━━━━━━━━━━━━━━━━━━━━━━━
📐 关键价位 | Key Levels
━━━━━━━━━━━━━━━━━━━━━━━━
  支撑位: {", ".join(f"{s:.2f}" for s in support)}
  压力位: {", ".join(f"{r:.2f}" for r in resistance)}
  枢轴点: {pivots["pivot"]:.2f}

━━━━━━━━━━━━━━━━━━━━━━━━
🔍 逻辑回检 | Logic Re-check
━━━━━━━━━━━━━━━━━━━━━━━━
  1. 当前均线{ma_alignment}排列，趋势方向明确
  2. 量能为{current_vol_pattern}，配合价格动作
  3. 盈亏比 {rr_ratio:.2f}:1，{"合理" if rr_ratio >= 2 else "偏低，需谨慎"}

━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ 失效条件 | Invalidation
━━━━━━━━━━━━━━━━━━━━━━━━
  1. 若价格跌破 {sl:.2f}，本决策逻辑失效，应执行止损
  2. 若 MACD 出现反向信号，需重新评估
  3. 若量能出现异常（倍量下跌/地量上涨），逻辑需修正
"""
    return report
