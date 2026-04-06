"""量能形态识别 | Volume Pattern Recognition"""

from nanobot.agent.tools import tool

from finagent.adapters.akshare_adapter import AKShareAdapter
from finagent.engine.volume_patterns import add_volume_patterns


@tool
async def skill_volume(symbol: str, period: str = "daily") -> str:
    """
    识别量能形态：倍量、缩倍量、梯量、地量。
    Identify volume patterns: surge, shrink, staircase, floor volume.

    Args:
        symbol: 股票代码 | Stock code
        period: 周期 | Timeframe
    Returns:
        量能形态分析报告
    """
    adapter = AKShareAdapter()
    df = adapter.get_kline(symbol, period=period, count=120)

    if df.empty:
        return f"❌ 无法获取 {symbol} 的 K 线数据"

    df = add_volume_patterns(df)

    recent = df.tail(10)
    avg_vol_5 = df["volume"].tail(5).mean()
    avg_vol_20 = df["volume"].tail(20).mean()
    current_vol = df["volume"].iloc[-1]
    current_pattern = df["volume_pattern"].iloc[-1]

    vol_ratio_5 = current_vol / avg_vol_5 if avg_vol_5 > 0 else 0
    vol_ratio_20 = current_vol / avg_vol_20 if avg_vol_20 > 0 else 0

    pattern_desc = {
        "倍量": "成交量放大至均量的2倍以上，通常伴随价格突破或趋势加速",
        "缩倍量": "成交量萎缩至均量的1/2以下，可能预示变盘或洗盘结束",
        "梯量": "连续递增的成交量，表明资金持续进场",
        "地量": "成交量为近期最低，市场交投清淡，可能接近底部",
        "平量": "成交量与均量基本持平，趋势延续概率大",
        "常态": "无明显量能特征",
        "数据不足": "数据不足以判断",
    }

    recent_patterns = []
    for _, row in recent.iterrows():
        date_str = str(row["date"])[:10] if "date" in row else ""
        pat = row["volume_pattern"]
        vol = row["volume"]
        recent_patterns.append(f"  {date_str}  量能: {pat}  成交量: {vol:,.0f}")

    if vol_ratio_5 >= 2:
        vol_signal = "🔴 倍量异动"
    elif vol_ratio_5 <= 0.5:
        vol_signal = "🟡 缩量观望"
    else:
        vol_signal = "🟢 量能正常"

    report = f"""📊 量能形态分析 | Volume Analysis — {symbol}

━━━━━━━━━━━━━━━━━━━━━━━━
{vol_signal} 当前量能状态
━━━━━━━━━━━━━━━━━━━━━━━━
  今日量能: {current_pattern}
  今日成交量: {current_vol:,.0f}
  5日均量: {avg_vol_5:,.0f}  20日均量: {avg_vol_20:,.0f}
  量比(5日): {vol_ratio_5:.2f}x  量比(20日): {vol_ratio_20:.2f}x

  量能含义: {pattern_desc.get(current_pattern, "")}

━━━━━━━━━━━━━━━━━━━━━━━━
📋 近10日量能记录
━━━━━━━━━━━━━━━━━━━━━━━━
{chr(10).join(recent_patterns)}

━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ 失效条件 | Invalidation
━━━━━━━━━━━━━━━━━━━━━━━━
  1. 倍量后若价格不跟进，可能是诱多
  2. 地量后若继续缩量，可能进入长期盘整
  3. 量能分析需结合价格形态综合判断
"""
    return report
