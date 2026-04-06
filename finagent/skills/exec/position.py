"""持仓管理 | Position Management"""

from nanobot.agent.tools import tool

from finagent.db.database import position_list as db_position_list, position_add as db_position_add


@tool
async def skill_position_list() -> str:
    """获取当前全部持仓 | List all current positions"""
    positions = db_position_list()

    if not positions:
        return """📋 我的持仓 | My Positions

━━━━━━━━━━━━━━━━━━━━━━━━
⚪ 暂无持仓
━━━━━━━━━━━━━━━━━━━━━━━━
  使用 `加持仓 [代码] [成本] [数量]` 录入持仓
  例如: 加持仓 600519 1750 100
"""

    lines = []
    total_cost = 0
    for p in positions:
        total_cost += p.cost * p.qty
        lines.append(
            f"  {p.symbol} {p.name}  成本: {p.cost:.2f}  数量: {p.qty}  总成本: {p.cost * p.qty:,.2f}"
        )

    report = f"""📋 我的持仓 | My Positions

━━━━━━━━━━━━━━━━━━━━━━━━
{chr(10).join(lines)}

━━━━━━━━━━━━━━━━━━━━━━━━
  总持仓成本: {total_cost:,.2f}
  持仓数量: {len(positions)} 只
"""
    return report


@tool
async def skill_position_add(symbol: str, cost: float, qty: int) -> str:
    """
    录入持仓 | Add a position entry.

    Args:
        symbol: 股票代码 | Stock code
        cost: 成本价 | Cost price
        qty: 持有数量 | Quantity held
    """
    position = db_position_add(symbol=symbol, cost=cost, qty=qty)

    report = f"""✅ 持仓录入成功 | Position Added

━━━━━━━━━━━━━━━━━━━━━━━━
  代码: {position.symbol}
  成本: {position.cost:.2f}
  数量: {position.qty}
  总成本: {position.total_cost:,.2f}
  录入时间: {position.added_at}
"""
    return report
