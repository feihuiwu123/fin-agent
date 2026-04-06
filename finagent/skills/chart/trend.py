"""均线排列 + 趋势判断 | MA Alignment + Trend Analysis"""

from nanobot.agent.tools import tool

from finagent.adapters.akshare_adapter import AKShareAdapter
from finagent.engine.indicators import calc_all_indicators


@tool
async def skill_trend(symbol: str, period: str = "daily") -> str:
    """
    分析均线排列（多头/空头/纠结）和多周期趋势共振。
    Analyze MA alignment (bullish/bearish/tangled) and multi-timeframe resonance.

    Args:
        symbol: 股票代码 | Stock code
        period: 周期 daily/weekly | Timeframe
    Returns:
        趋势判断报告
    """
    adapter = AKShareAdapter()
    df = adapter.get_kline(symbol, period=period, count=250)

    if df.empty:
        return f"❌ 无法获取 {symbol} 的 K 线数据"

    df = calc_all_indicators(df)
    last = df.iloc[-1]

    ma5 = last.get("MA5", 0)
    ma10 = last.get("MA10", 0)
    ma20 = last.get("MA20", 0)
    ma60 = last.get("MA60", 0)
    ma120 = last.get("MA120", 0)
    ma250 = last.get("MA250", 0)
    close = last["close"]

    if ma5 > ma10 > ma20 > ma60:
        ma_alignment = "多头排列"
        ma_signal = "🟢"
    elif ma5 < ma10 < ma20 < ma60:
        ma_alignment = "空头排列"
        ma_signal = "🔴"
    else:
        ma_alignment = "纠结排列"
        ma_signal = "🟡"

    if ma60 > 0 and ma120 > 0:
        if ma60 > ma120:
            mid_trend = "中期向上"
        else:
            mid_trend = "中期向下"
    else:
        mid_trend = "中期趋势不明"

    if ma250 > 0:
        if close > ma250:
            long_trend = "长期牛市格局"
        else:
            long_trend = "长期熊市格局"
    else:
        long_trend = "长期趋势不明"

    dif = last.get("DIF", 0)
    dea = last.get("DEA", 0)
    if dif > dea:
        macd_status = "金叉（多头）"
    else:
        macd_status = "死叉（空头）"

    k_val = last.get("K", 0)
    d_val = last.get("D", 0)
    j_val = last.get("J", 0)
    if j_val > 80:
        kdj_status = "超买区"
    elif j_val < 20:
        kdj_status = "超卖区"
    else:
        kdj_status = "中性区"

    rsi = last.get("RSI", 0)
    if rsi > 70:
        rsi_status = "超买"
    elif rsi < 30:
        rsi_status = "超卖"
    else:
        rsi_status = "中性"

    report = f"""📈 趋势分析报告 | Trend Analysis — {symbol}

━━━━━━━━━━━━━━━━━━━━━━━━
📊 均线排列 | MA Alignment
━━━━━━━━━━━━━━━━━━━━━━━━
  {ma_signal} {ma_alignment}
  MA5:  {ma5:.2f}  MA10: {ma10:.2f}  MA20: {ma20:.2f}
  MA60: {ma60:.2f}  MA120: {ma120:.2f}  MA250: {ma250:.2f}
  现价: {close:.2f}

━━━━━━━━━━━━━━━━━━━━━━━━
🔗 多周期共振 | Multi-Timeframe Resonance
━━━━━━━━━━━━━━━━━━━━━━━━
  中期趋势: {mid_trend}
  长期趋势: {long_trend}

━━━━━━━━━━━━━━━━━━━━━━━━
📉 辅助指标 | Auxiliary Indicators
━━━━━━━━━━━━━━━━━━━━━━━━
  MACD: {macd_status}  (DIF={dif:.3f}, DEA={dea:.3f})
  KDJ:  {kdj_status}   (K={k_val:.1f}, D={d_val:.1f}, J={j_val:.1f})
  RSI:  {rsi_status}   (RSI={rsi:.1f})

━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ 失效条件 | Invalidation
━━━━━━━━━━━━━━━━━━━━━━━━
  1. 若 MA5 下穿 MA20，短线多头排列失效
  2. 若 MACD 出现死叉，动能转弱
  3. 若 RSI > 80 后回落，短期回调风险加大
"""
    return report
