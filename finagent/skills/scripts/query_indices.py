#!/usr/bin/env python3
"""Index data query script."""
import akshare as ak

indices = {"上证指数": "sh000001", "深证成指": "sz399001", "创业板指": "sz399006", "沪深300": "sh000300", "科创50": "sh000688"}
for name, sym in indices.items():
    try:
        df = ak.stock_zh_index_daily(symbol=sym)
        if df is not None and not df.empty:
            last = df.iloc[-1]
            prev = df.iloc[-2] if len(df) > 1 else last
            close = float(last["close"])
            prev_close = float(prev["close"])
            pct = (close - prev_close) / prev_close * 100 if prev_close > 0 else 0
            arrow = "up" if pct > 0 else "down" if pct < 0 else "flat"
            print(f"{arrow}|{name}|{close:.2f}|{pct:+.2f}")
    except Exception:
        pass
