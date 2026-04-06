"""财务健康度分析 | Financial Health Analysis"""

from nanobot.agent.tools import tool

from finagent.adapters.akshare_adapter import AKShareAdapter


@tool
async def skill_financial(symbol: str) -> str:
    """
    分析股票财务健康度（营收增速、ROE、负债率等）。
    Analyze financial health: revenue growth, ROE, debt ratio, etc.

    Args:
        symbol: 股票代码 | Stock code
    Returns:
        财务健康度评分及分析
    """
    adapter = AKShareAdapter()
    financials = adapter.get_financials(symbol)

    if "error" in financials:
        return f"❌ 无法获取 {symbol} 的财务数据: {financials['error']}"

    revenue = financials.get("revenue", 0)
    net_profit = financials.get("net_profit", 0)
    roe = financials.get("roe", 0)
    debt_ratio = financials.get("debt_ratio", 0)
    revenue_growth = financials.get("revenue_growth", 0)
    profit_growth = financials.get("profit_growth", 0)

    score = 0
    max_score = 100
    details = []

    if roe > 20:
        score += 25
        roe_grade = "A+"
    elif roe > 15:
        score += 20
        roe_grade = "A"
    elif roe > 10:
        score += 15
        roe_grade = "B"
    elif roe > 5:
        score += 10
        roe_grade = "C"
    else:
        score += 0
        roe_grade = "D"
    details.append(f"  ROE 评分: {roe_grade} ({roe:.1f}%)")

    if debt_ratio < 30:
        score += 25
        debt_grade = "A+"
    elif debt_ratio < 50:
        score += 20
        debt_grade = "A"
    elif debt_ratio < 60:
        score += 15
        debt_grade = "B"
    elif debt_ratio < 70:
        score += 10
        debt_grade = "C"
    else:
        score += 0
        debt_grade = "D"
    details.append(f"  负债率评分: {debt_grade} ({debt_ratio:.1f}%)")

    if revenue_growth > 30:
        score += 25
        growth_grade = "A+"
    elif revenue_growth > 20:
        score += 20
        growth_grade = "A"
    elif revenue_growth > 10:
        score += 15
        growth_grade = "B"
    elif revenue_growth > 0:
        score += 10
        growth_grade = "C"
    else:
        score += 0
        growth_grade = "D"
    details.append(f"  营收增速评分: {growth_grade} ({revenue_growth:+.1f}%)")

    if profit_growth > 30:
        score += 25
        profit_grade = "A+"
    elif profit_growth > 20:
        score += 20
        profit_grade = "A"
    elif profit_growth > 10:
        score += 15
        profit_grade = "B"
    elif profit_growth > 0:
        score += 10
        profit_grade = "C"
    else:
        score += 0
        profit_grade = "D"
    details.append(f"  利润增速评分: {profit_grade} ({profit_growth:+.1f}%)")

    if score >= 80:
        health = "优秀"
        emoji = "🟢"
    elif score >= 60:
        health = "良好"
        emoji = "🟡"
    elif score >= 40:
        health = "一般"
        emoji = "🟠"
    else:
        health = "较差"
        emoji = "🔴"

    if revenue > 1e8:
        revenue_str = f"{revenue / 1e8:.2f} 亿"
    else:
        revenue_str = f"{revenue / 1e4:.2f} 万"

    if net_profit > 1e8:
        profit_str = f"{net_profit / 1e8:.2f} 亿"
    else:
        profit_str = f"{net_profit / 1e4:.2f} 万"

    report = f"""💰 财务健康度分析 | Financial Health — {symbol}

━━━━━━━━━━━━━━━━━━━━━━━━
{emoji} 综合评分: {score}/{max_score} ({health})
━━━━━━━━━━━━━━━━━━━━━━━━
{chr(10).join(details)}

━━━━━━━━━━━━━━━━━━━━━━━━
📊 核心数据 | Core Data
━━━━━━━━━━━━━━━━━━━━━━━━
  营业收入: {revenue_str}
  净利润: {profit_str}
  ROE: {roe:.1f}%
  资产负债率: {debt_ratio:.1f}%
  营收增速: {revenue_growth:+.1f}%
  净利润增速: {profit_growth:+.1f}%

━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ 失效条件 | Invalidation
━━━━━━━━━━━━━━━━━━━━━━━━
  1. 若 ROE 连续下降，盈利质量恶化
  2. 若负债率快速上升，财务风险加大
  3. 若营收增速转负，成长性逻辑被证伪
  4. 财务数据基于最新报告期，需关注季报更新
"""
    return report
