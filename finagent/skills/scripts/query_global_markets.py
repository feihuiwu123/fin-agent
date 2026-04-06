#!/usr/bin/env python3
"""Global markets overview script."""
import akshare as ak

# US indices (via东方财富)
us_indices = {"道琼斯": "100", "纳斯达克": "101", "标普500": "102"}
print("=== 美股 ===")
for name, code in us_indices.items():
    try:
        df = ak.stock_us_index_daily_em(symbol=code)
        if df is not None and not df.empty:
            last = df.iloc[-1]
            prev = df.iloc[-2] if len(df) > 1 else last
            close = float(last.get("close", 0))
            prev_close = float(prev.get("close", close))
            pct = (close - prev_close) / prev_close * 100 if prev_close > 0 else 0
            arrow = "up" if pct > 0 else "down" if pct < 0 else "flat"
            print(f"{arrow}|{name}|{close:.2f}|{pct:+.2f}")
    except Exception:
        pass

# Europe
print("=== 欧股 ===")
eu_indices = {"富时100": "103", "德国DAX": "104", "法国CAC40": "105"}
for name, code in eu_indices.items():
    try:
        df = ak.stock_us_index_daily_em(symbol=code)
        if df is not None and not df.empty:
            last = df.iloc[-1]
            prev = df.iloc[-2] if len(df) > 1 else last
            close = float(last.get("close", 0))
            prev_close = float(prev.get("close", close))
            pct = (close - prev_close) / prev_close * 100 if prev_close > 0 else 0
            arrow = "up" if pct > 0 else "down" if pct < 0 else "flat"
            print(f"{arrow}|{name}|{close:.2f}|{pct:+.2f}")
    except Exception:
        pass

# Asia
print("=== 亚太 ===")
asia_indices = {"日经225": "106", "韩国KOSPI": "107", "恒生指数": "108"}
for name, code in asia_indices.items():
    try:
        df = ak.stock_us_index_daily_em(symbol=code)
        if df is not None and not df.empty:
            last = df.iloc[-1]
            prev = df.iloc[-2] if len(df) > 1 else last
            close = float(last.get("close", 0))
            prev_close = float(prev.get("close", close))
            pct = (close - prev_close) / prev_close * 100 if prev_close > 0 else 0
            arrow = "up" if pct > 0 else "down" if pct < 0 else "flat"
            print(f"{arrow}|{name}|{close:.2f}|{pct:+.2f}")
    except Exception:
        pass

# Commodities
print("=== 大宗商品 ===")
try:
    df = ak.futures_foreign_hist(symbol="CL")
    if df is not None and not df.empty:
        last = df.iloc[-1]
        print(f"原油|{float(last.get('收盘',0)):.2f}")
except Exception:
    pass

try:
    df = ak.futures_foreign_hist(symbol="GC")
    if df is not None and not df.empty:
        last = df.iloc[-1]
        print(f"黄金|{float(last.get('收盘',0)):.2f}")
except Exception:
    pass
