"""SQLite 数据模型 | SQLite Data Models"""

from datetime import datetime
from dataclasses import dataclass, field, asdict
from typing import Optional


@dataclass
class Position:
    """持仓记录 | Position record"""

    id: Optional[int] = None
    symbol: str = ""
    name: str = ""
    cost: float = 0.0
    qty: int = 0
    added_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())

    @property
    def total_cost(self) -> float:
        return self.cost * self.qty

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Alert:
    """预警记录 | Alert record"""

    id: Optional[int] = None
    symbol: str = ""
    condition: str = ""
    condition_type: str = ""
    target_price: Optional[float] = None
    active: bool = True
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    triggered_at: Optional[str] = None

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class TradeLog:
    """交易日志 | Trade log"""

    id: Optional[int] = None
    symbol: str = ""
    side: str = ""
    price: float = 0.0
    qty: int = 0
    reason: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())

    def to_dict(self) -> dict:
        return asdict(self)
