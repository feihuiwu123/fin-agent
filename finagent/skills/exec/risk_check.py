"""风控规则引擎 | Risk Control Engine"""

# 硬性风控参数 | Hard risk limits
MAX_SINGLE_POSITION_PCT = 0.20  # 单股最大仓位 20%
MAX_DAILY_LOSS_PCT = 0.03  # 单日最大亏损 3%
MAX_TOTAL_DRAWDOWN_PCT = 0.15  # 总回撤保护 15%


def check_position_limit(symbol: str, amount: float, total_asset: float) -> bool:
    """检查单股仓位是否超限 | Check if single-stock position exceeds limit"""
    return (amount / total_asset) <= MAX_SINGLE_POSITION_PCT


def check_daily_loss(today_pnl: float, total_asset: float) -> bool:
    """检查单日亏损是否超限 | Check daily loss limit"""
    return abs(today_pnl / total_asset) <= MAX_DAILY_LOSS_PCT
