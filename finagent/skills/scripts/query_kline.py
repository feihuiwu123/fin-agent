#!/usr/bin/env python3
"""K-line data query script."""
import sys
import akshare as ak

code = sys.argv[1] if len(sys.argv) > 1 else "600519"
try:
    df = ak.stock_zh_a_hist(symbol=code, period="daily", adjust="qfq")
    if df is not None and not df.empty:
        last = df.tail(10)
        for _, r in last.iterrows():
            d = str(r.get("日期", ""))[:10]
            o = r.get("开盘", 0)
            c = r.get("收盘", 0)
            h = r.get("最高", 0)
            l = r.get("最低", 0)
            pct = r.get("涨跌幅", 0)
            vol = r.get("成交量", 0)
            print(f"{d} O:{o} H:{h} L:{l} C:{c} pct:{pct:+.2f}% vol:{vol:.0f}")
    else:
        print("无K线数据")
except Exception as e:
    print(f"K线数据获取失败: {e}")
