"""条件预警 | Conditional Price Alerts"""

from nanobot.agent.tools import tool
import re

from finagent.db.database import alert_add as db_alert_add, alert_list as db_alert_list


def parse_condition(condition: str) -> tuple[str, str, float | None]:
    """
    解析预警条件 | Parse alert condition

    Returns:
        (condition_type, description, target_price)
    """
    condition = condition.strip()
    prices = re.findall(r"[\d,]+\.?\d*", condition.replace(",", ""))
    target_price = float(prices[0]) if prices else None

    if "跌破" in condition or "低于" in condition or "下破" in condition:
        return ("price_below", condition, target_price)
    elif "突破" in condition or "高于" in condition or "上破" in condition or "涨" in condition:
        return ("price_above", condition, target_price)
    elif "倍量" in condition:
        return ("volume_surge", condition, None)
    elif "金叉" in condition:
        return ("macd_golden_cross", condition, None)
    elif "死叉" in condition:
        return ("macd_death_cross", condition, None)
    else:
        return ("custom", condition, target_price)


@tool
async def skill_alert_set(symbol: str, condition: str) -> str:
    """
    设置价格/信号预警条件。
    Set a price or signal alert condition.

    Args:
        symbol: 股票代码 | Stock code
        condition: 预警条件描述，如"跌破1700"| Alert condition, e.g. "跌破1700"
    Returns:
        预警设置确认 | Alert confirmation
    """
    cond_type, desc, target_price = parse_condition(condition)
    alert = db_alert_add(
        symbol=symbol, condition=desc, condition_type=cond_type, target_price=target_price
    )

    report = f"""✅ 预警设置成功 | Alert Set

━━━━━━━━━━━━━━━━━━━━━━━━
  代码: {alert.symbol}
  条件: {alert.condition}
  类型: {alert.condition_type}
  目标价: {alert.target_price if alert.target_price else "N/A"}
  状态: 已激活
  创建时间: {alert.created_at}
"""
    return report


@tool
async def skill_alert_list() -> str:
    """查看当前所有预警 | List all current alerts"""
    alerts = db_alert_list(active_only=True)

    if not alerts:
        return """🔔 我的预警 | My Alerts

━━━━━━━━━━━━━━━━━━━━━━━━
⚪ 暂无预警
━━━━━━━━━━━━━━━━━━━━━━━━
  使用 `设预警 [代码] [条件]` 设置预警
  例如: 设预警 600519 跌破1700
"""

    lines = []
    for a in alerts:
        price_str = f" @ {a.target_price}" if a.target_price else ""
        lines.append(f"  {a.symbol}  {a.condition}{price_str}  ({a.condition_type})")

    report = f"""🔔 我的预警 | My Alerts

━━━━━━━━━━━━━━━━━━━━━━━━
{chr(10).join(lines)}

━━━━━━━━━━━━━━━━━━━━━━━━
  活跃预警: {len(alerts)} 个
"""
    return report
