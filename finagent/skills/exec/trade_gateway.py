"""交易网关（预留）| Trade Gateway (reserved for QMT/PTrade)"""

from finagent.db.database import trade_log_add
from finagent.skills.exec.risk_check import check_position_limit


async def place_order(
    symbol: str,
    side: str,
    qty: int,
    price: float,
    order_type: str = "limit",
    total_asset: float = 0,
) -> dict:
    """
    下单入口（HITL 人工确认）| Order entry (Human-In-The-Loop confirmation)

    Args:
        symbol: 股票代码 | Stock code
        side: buy / sell
        qty: 数量 | Quantity
        price: 价格 | Price
        order_type: limit / market
        total_asset: 总资产（用于风控检查）| Total asset for risk check
    """
    # 风控检查 | Risk control check
    if side == "buy" and total_asset > 0:
        amount = qty * price
        if not check_position_limit(symbol, amount, total_asset):
            return {
                "success": False,
                "reason": f"仓位超限: {amount:.2f} > {total_asset * 0.20:.2f} (20%)",
            }

    # 记录交易日志 | Log the trade
    trade_log_add(symbol=symbol, side=side, price=price, qty=qty, reason=f"{order_type} order")

    # TODO: 接入 QMT/PTrade 实际下单
    return {
        "success": True,
        "symbol": symbol,
        "side": side,
        "qty": qty,
        "price": price,
        "order_type": order_type,
        "status": "simulated (trade gateway not connected)",
    }


async def cancel_order(order_id: str) -> bool:
    """撤单 | Cancel an order"""
    # TODO: 接入 QMT/PTrade 实际撤单
    return False


async def get_positions() -> list:
    """获取交易账户持仓 | Get positions from trading account"""
    # TODO: 接入 QMT/PTrade 实际查询
    return []


async def get_account_info() -> dict:
    """获取交易账户信息 | Get trading account info"""
    # TODO: 接入 QMT/PTrade 实际查询
    return {"status": "trade gateway not connected"}
