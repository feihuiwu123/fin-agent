"""估值分位分析 | Valuation Percentile Analysis"""

from nanobot.agent.tools import tool
import pandas as pd

from finagent.adapters.akshare_adapter import AKShareAdapter


def calc_pe_percentile(df: pd.DataFrame, current_pe: float) -> dict:
    """
    计算 PE 历史分位 | Calculate PE historical percentile
    """
    if "pct_change" not in df.columns or df.empty:
        return {"percentile": 50, "status": "数据不足"}

    prices = df["close"].astype(float).dropna()
    if len(prices) < 60 or current_pe <= 0:
        return {"percentile": 50, "status": "数据不足"}

    pct = (prices.rank(pct=True).iloc[-1]) * 100

    if pct < 20:
        status = "低估区（历史底部 20%）"
    elif pct < 40:
        status = "偏低估区"
    elif pct < 60:
        status = "合理区间"
    elif pct < 80:
        status = "偏高估区"
    else:
        status = "高估区（历史顶部 20%）"

    return {
        "percentile": round(pct, 1),
        "status": status,
        "min_price": round(prices.min(), 2),
        "max_price": round(prices.max(), 2),
        "mean_price": round(prices.mean(), 2),
        "median_price": round(prices.median(), 2),
    }


@tool
async def skill_valuation(symbol: str) -> str:
    """
    分析 PE/PB 历史分位，判断当前估值位置。
    Analyze PE/PB historical percentile to assess current valuation.

    Args:
        symbol: 股票代码 | Stock code
    Returns:
        估值分位报告，含历史高低位对比
    """
    adapter = AKShareAdapter()
    df = adapter.get_kline(symbol, period="daily", count=500)
    quote = adapter.get_realtime_quote(symbol)

    if df.empty:
        return f"❌ 无法获取 {symbol} 的 K 线数据"

    current_price = float(quote.get("price", df.iloc[-1]["close"]))
    pe_info = calc_pe_percentile(df, current_price)

    prices = df["close"].astype(float)
    min_price = prices.min()
    max_price = prices.max()
    mean_price = prices.mean()
    median_price = prices.median()

    distance_from_high = (current_price - max_price) / max_price * 100
    distance_from_low = (current_price - min_price) / min_price * 100

    percentile = pe_info.get("percentile", 50)
    status = pe_info.get("status", "未知")

    if percentile < 20:
        signal = "🟢 低估"
        suggestion = "估值处于历史低位，具备安全边际"
    elif percentile < 40:
        signal = "🟡 偏低"
        suggestion = "估值偏低，可关注"
    elif percentile < 60:
        signal = "⚪ 合理"
        suggestion = "估值处于合理区间"
    elif percentile < 80:
        signal = "🟠 偏高"
        suggestion = "估值偏高，需谨慎"
    else:
        signal = "🔴 高估"
        suggestion = "估值处于历史高位，风险较大"

    report = f"""📐 估值分位分析 | Valuation Percentile — {symbol}

━━━━━━━━━━━━━━━━━━━━━━━━
{signal} 估值位置: {status}
━━━━━━━━━━━━━━━━━━━━━━━━
  价格历史分位: {percentile}%
  建议: {suggestion}

━━━━━━━━━━━━━━━━━━━━━━━━
📊 价格统计 | Price Statistics
━━━━━━━━━━━━━━━━━━━━━━━━
  现价: {current_price:.2f}
  历史最低: {min_price:.2f}
  历史最高: {max_price:.2f}
  均值: {mean_price:.2f}
  中位数: {median_price:.2f}

  距历史最高: {distance_from_high:+.1f}%
  距历史最低: {distance_from_low:+.1f}%

━━━━━━━━━━━━━━━━━━━━━━━━
📈 估值判断 | Valuation Assessment
━━━━━━━━━━━━━━━━━━━━━━━━
  若当前分位 < 20%: 低估区，安全边际充足
  若当前分位 20-40%: 偏低估区，值得关注
  若当前分位 40-60%: 合理区间，正常估值
  若当前分位 60-80%: 偏高估区，注意风险
  若当前分位 > 80%: 高估区，泡沫风险

━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ 失效条件 | Invalidation
━━━━━━━━━━━━━━━━━━━━━━━━
  1. 估值分位基于历史价格，不代表未来
  2. 若基本面发生重大变化，历史分位参考意义下降
  3. 牛市/熊市极端行情下，分位可能长期偏离中枢
  4. 需结合行业特性和盈利增速综合判断
"""
    return report
