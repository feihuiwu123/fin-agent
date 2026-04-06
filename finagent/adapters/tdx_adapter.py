"""通达信适配器（预留）| TongDaXin Adapter (reserved)"""

import pandas as pd
from .base import DataAdapter


class TDXAdapter(DataAdapter):
    """通达信适配器 — 待实现 (P1)"""

    def get_kline(self, symbol: str, period: str, count: int) -> pd.DataFrame:
        raise NotImplementedError("TDXAdapter 尚未实现 | Not yet implemented")

    def get_realtime_quote(self, symbol: str) -> dict:
        raise NotImplementedError

    def get_financials(self, symbol: str) -> dict:
        raise NotImplementedError

    def get_fund_flow(self, symbol: str) -> dict:
        raise NotImplementedError

    def get_news(self, keywords: list[str], days: int) -> list:
        raise NotImplementedError
