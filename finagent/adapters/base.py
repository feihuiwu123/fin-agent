"""统一数据适配器抽象接口 | Unified abstract interface for data adapters"""

from abc import ABC, abstractmethod
import pandas as pd


class DataAdapter(ABC):
    """统一数据适配器接口 | Unified data adapter interface"""

    @abstractmethod
    def get_kline(self, symbol: str, period: str, count: int) -> pd.DataFrame:
        """获取 K 线数据 | Fetch K-line (OHLCV) data"""
        ...

    @abstractmethod
    def get_realtime_quote(self, symbol: str) -> dict:
        """获取实时行情 | Fetch real-time quote"""
        ...

    @abstractmethod
    def get_financials(self, symbol: str) -> dict:
        """获取财务数据 | Fetch financial data"""
        ...

    @abstractmethod
    def get_fund_flow(self, symbol: str) -> dict:
        """获取资金流向 | Fetch fund flow data"""
        ...

    @abstractmethod
    def get_news(self, keywords: list[str], days: int) -> list:
        """获取新闻 | Fetch news"""
        ...


class TradeAdapter(ABC):
    """统一交易接口 | Unified trade interface"""

    @abstractmethod
    def place_order(self, symbol: str, side: str, qty: int, price: float, order_type: str):
        """下单 | Place an order"""
        ...

    @abstractmethod
    def cancel_order(self, order_id: str) -> bool:
        """撤单 | Cancel an order"""
        ...

    @abstractmethod
    def get_positions(self) -> list:
        """获取持仓 | Get positions"""
        ...

    @abstractmethod
    def get_account_info(self) -> dict:
        """获取账户信息 | Get account information"""
        ...
