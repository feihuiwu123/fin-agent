"""迅投 QMT 数据适配器 | XunTou QMT Data Adapter"""
# 依赖：xtquant（需安装迅投 QMT 客户端）
# Requires: xtquant (XunTou QMT client must be installed)

import pandas as pd
from .base import DataAdapter


class QMTAdapter(DataAdapter):
    """迅投 QMT 行情适配器（一期主力数据源）"""

    def __init__(self):
        # TODO: 初始化 xtquant 连接
        pass

    def get_kline(self, symbol: str, period: str, count: int) -> pd.DataFrame:
        # TODO: 调用 xtquant 获取 K 线
        raise NotImplementedError

    def get_realtime_quote(self, symbol: str) -> dict:
        raise NotImplementedError

    def get_financials(self, symbol: str) -> dict:
        raise NotImplementedError

    def get_fund_flow(self, symbol: str) -> dict:
        raise NotImplementedError

    def get_news(self, keywords: list[str], days: int) -> list:
        raise NotImplementedError
