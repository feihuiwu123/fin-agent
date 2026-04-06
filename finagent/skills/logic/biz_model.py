"""商业模式分析 + 逻辑闭环验证 | Business Model Analysis + Logic Loop Verification"""

from nanobot.agent.tools import tool

from finagent.adapters.akshare_adapter import AKShareAdapter


@tool
async def skill_biz_model(symbol: str) -> str:
    """
    分析股票的商业模式，输出逻辑闭环报告。
    Analyze the business model of a stock and output a logic closed-loop report.

    Args:
        symbol: 股票代码，如 "600519" | Stock code, e.g. "600519"
    Returns:
        包含商业模式、护城河、失效条件的分析报告
    """
    adapter = AKShareAdapter()
    quote = adapter.get_realtime_quote(symbol)
    financials = adapter.get_financials(symbol)

    name = quote.get("name", symbol)
    price = quote.get("price", 0)
    change_pct = quote.get("change_pct", 0)

    revenue = financials.get("revenue", 0)
    net_profit = financials.get("net_profit", 0)
    roe = financials.get("roe", 0)
    debt_ratio = financials.get("debt_ratio", 0)
    revenue_growth = financials.get("revenue_growth", 0)
    profit_growth = financials.get("profit_growth", 0)

    if revenue > 1e8:
        revenue_str = f"{revenue / 1e8:.2f} 亿"
    elif revenue > 1e4:
        revenue_str = f"{revenue / 1e4:.2f} 万"
    else:
        revenue_str = f"{revenue:.2f}"

    if net_profit > 1e8:
        profit_str = f"{net_profit / 1e8:.2f} 亿"
    elif net_profit > 1e4:
        profit_str = f"{net_profit / 1e4:.2f} 万"
    else:
        profit_str = f"{net_profit:.2f}"

    if roe > 15:
        roe_rating = "优秀"
    elif roe > 10:
        roe_rating = "良好"
    elif roe > 5:
        roe_rating = "一般"
    else:
        roe_rating = "偏弱"

    if debt_ratio < 40:
        debt_rating = "安全"
    elif debt_ratio < 60:
        debt_rating = "适中"
    elif debt_ratio < 80:
        debt_rating = "偏高"
    else:
        debt_rating = "危险"

    if revenue_growth > 20:
        growth_rating = "高增长"
    elif revenue_growth > 10:
        growth_rating = "稳健增长"
    elif revenue_growth > 0:
        growth_rating = "低速增长"
    else:
        growth_rating = "负增长"

    moat_score = 0
    moat_factors = []
    if roe > 15:
        moat_score += 2
        moat_factors.append("高 ROE 表明盈利能力强")
    if revenue_growth > 15:
        moat_score += 1
        moat_factors.append("营收高增长表明市场扩张能力强")
    if debt_ratio < 50:
        moat_score += 1
        moat_factors.append("负债率健康，财务风险可控")
    if net_profit > 0 and profit_growth > 0:
        moat_score += 1
        moat_factors.append("盈利持续为正且增长")

    if moat_score >= 4:
        moat_level = "宽护城河"
    elif moat_score >= 3:
        moat_level = "中等护城河"
    elif moat_score >= 2:
        moat_level = "窄护城河"
    else:
        moat_level = "无明显护城河"

    report = f"""🏢 商业模式分析 | Business Model — {symbol} {name}

━━━━━━━━━━━━━━━━━━━━━━━━
📊 基本信息 | Basic Info
━━━━━━━━━━━━━━━━━━━━━━━━
  现价: {price:.2f}  涨跌幅: {change_pct:+.2f}%
  营收: {revenue_str}  净利润: {profit_str}

━━━━━━━━━━━━━━━━━━━━━━━━
📈 财务核心指标 | Key Financial Metrics
━━━━━━━━━━━━━━━━━━━━━━━━
  ROE: {roe:.1f}%  ({roe_rating})
  资产负债率: {debt_ratio:.1f}%  ({debt_rating})
  营收增速: {revenue_growth:+.1f}%  ({growth_rating})
  净利润增速: {profit_growth:+.1f}%

━━━━━━━━━━━━━━━━━━━━━━━━
🏰 护城河评估 | Moat Assessment
━━━━━━━━━━━━━━━━━━━━━━━━
  护城河等级: {moat_level} (评分: {moat_score}/5)
  支撑因素:
{chr(10).join(f"    • {f}" for f in moat_factors)}

━━━━━━━━━━━━━━━━━━━━━━━━
🔗 逻辑闭环 | Logic Closed-Loop
━━━━━━━━━━━━━━━━━━━━━━━━
  赚钱逻辑: {"成立" if moat_score >= 3 else "存疑"}
  核心驱动: {"ROE + 增长双轮驱动" if roe > 15 and revenue_growth > 15 else "需观察盈利质量"}

━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ 失效条件 | Invalidation
━━━━━━━━━━━━━━━━━━━━━━━━
  1. 若 ROE 连续两季度下降至 10% 以下，护城河逻辑失效
  2. 若资产负债率突破 70%，财务风险急剧上升
  3. 若营收增速转负，增长逻辑被证伪
  4. 若行业政策发生重大不利变化，需重新评估
"""
    return report
