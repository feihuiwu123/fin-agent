"""AKShare 数据适配器 | AKShare Data Adapter (free, open-source)"""

import pandas as pd
import akshare as ak
from datetime import datetime, timedelta
from .base import DataAdapter


class AKShareAdapter(DataAdapter):
    """AKShare 免费行情适配器（MVP 主力数据源）"""

    def _normalize_symbol(self, symbol: str) -> str:
        """确保股票代码为 6 位字符串 | Ensure symbol is 6-digit string"""
        return symbol.zfill(6)

    def get_kline(self, symbol: str, period: str = "daily", count: int = 250) -> pd.DataFrame:
        """
        获取 A 股 K 线数据 | Fetch A-share K-line data via AKShare

        Args:
            symbol: 股票代码，如 "600519" | Stock code
            period: daily / weekly / monthly
            count: 返回 K 线数量 | Number of candles
        """
        symbol = self._normalize_symbol(symbol)
        period_map = {"daily": "日", "weekly": "周", "monthly": "月"}
        ak_period = period_map.get(period, "日")

        end_date = datetime.now().strftime("%Y%m%d")
        start_date = (datetime.now() - timedelta(days=count * 2)).strftime("%Y%m%d")

        df = ak.stock_zh_a_hist(
            symbol=symbol,
            period=ak_period,
            start_date=start_date,
            end_date=end_date,
            adjust="qfq",
        )

        df = df.rename(
            columns={
                "日期": "date",
                "开盘": "open",
                "收盘": "close",
                "最高": "high",
                "最低": "low",
                "成交量": "volume",
                "成交额": "amount",
                "振幅": "amplitude",
                "涨跌幅": "pct_change",
                "涨跌额": "change",
                "换手率": "turnover",
            }
        )

        df["date"] = pd.to_datetime(df["date"])
        df = df.sort_values("date").reset_index(drop=True)

        return df.tail(count)

    def get_realtime_quote(self, symbol: str) -> dict:
        """获取实时行情 | Fetch real-time quote"""
        symbol = self._normalize_symbol(symbol)
        df = ak.stock_zh_a_spot_em()
        row = df[df["代码"] == symbol]
        if row.empty:
            return {}
        row = row.iloc[0]
        return {
            "symbol": symbol,
            "name": row.get("名称", ""),
            "price": float(row.get("最新价", 0)),
            "change_pct": float(row.get("涨跌幅", 0)),
            "volume": float(row.get("成交量", 0)),
            "amount": float(row.get("成交额", 0)),
            "high": float(row.get("最高", 0)),
            "low": float(row.get("最低", 0)),
            "open": float(row.get("今开", 0)),
            "prev_close": float(row.get("昨收", 0)),
        }

    def get_financials(self, symbol: str) -> dict:
        """获取财务数据 | Fetch financial data"""
        symbol = self._normalize_symbol(symbol)

        try:
            df = ak.stock_financial_abstract_ths(symbol=symbol)
            if df is not None and not df.empty:
                latest = df.iloc[0] if len(df) > 0 else {}
                return {
                    "symbol": symbol,
                    "revenue": float(latest.get("营业收入", 0)) if "营业收入" in latest else 0,
                    "net_profit": float(latest.get("净利润", 0)) if "净利润" in latest else 0,
                    "roe": float(latest.get("净资产收益率", 0)) if "净资产收益率" in latest else 0,
                    "debt_ratio": float(latest.get("资产负债率", 0))
                    if "资产负债率" in latest
                    else 0,
                    "revenue_growth": float(latest.get("营业收入同比增长", 0))
                    if "营业收入同比增长" in latest
                    else 0,
                    "profit_growth": float(latest.get("净利润同比增长", 0))
                    if "净利润同比增长" in latest
                    else 0,
                }
        except Exception:
            pass

        return {"symbol": symbol, "error": "财务数据获取失败"}

    def get_fund_flow(self, symbol: str) -> dict:
        """获取资金流向 | Fetch fund flow data"""
        symbol = self._normalize_symbol(symbol)
        try:
            df = ak.stock_individual_fund_flow(
                stock=symbol, market="sh" if symbol.startswith("6") else "sz"
            )
            if df is not None and not df.empty:
                latest = df.iloc[-1]
                return {
                    "symbol": symbol,
                    "main_net_inflow": float(latest.get("主力净流入-净额", 0)),
                    "main_net_pct": float(latest.get("主力净流入-净占比", 0)),
                    "super_large_net": float(latest.get("超大单净流入-净额", 0)),
                    "large_net": float(latest.get("大单净流入-净额", 0)),
                    "medium_net": float(latest.get("中单净流入-净额", 0)),
                    "small_net": float(latest.get("小单净流入-净额", 0)),
                }
        except Exception:
            pass

        return {"symbol": symbol, "error": "资金流向数据获取失败"}

    def get_news(self, keywords: list[str] | None = None, days: int = 7) -> list:
        """获取财经新闻 | Fetch financial news"""
        try:
            df = ak.stock_news_em(symbol="")
            if df is not None and not df.empty:
                cutoff = datetime.now() - timedelta(days=days)
                df["发布时间"] = pd.to_datetime(df["发布时间"], errors="coerce")
                df = df[df["发布时间"] >= cutoff]

                if keywords:
                    mask = df["新闻标题"].str.contains("|".join(keywords), case=False, na=False)
                    df = df[mask]

                news_list = []
                for _, row in df.head(50).iterrows():
                    news_list.append(
                        {
                            "title": row.get("新闻标题", ""),
                            "content": row.get("新闻内容", ""),
                            "source": row.get("文章来源", ""),
                            "time": str(row.get("发布时间", "")),
                            "url": row.get("新闻链接", ""),
                        }
                    )
                return news_list
        except Exception:
            pass

        return []
