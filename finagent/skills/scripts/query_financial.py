#!/usr/bin/env python3
"""Financial summary query script."""
import sys
import akshare as ak

code = sys.argv[1] if len(sys.argv) > 1 else "600519"
try:
    df = ak.stock_financial_abstract_ths(symbol=code)
    if df is not None and not df.empty:
        print(df.tail(4).to_string(index=False))
    else:
        print("无财务摘要数据")
except Exception:
    try:
        df = ak.stock_financial_report_sina(stock=code, symbol="资产负债表")
        if df is not None and not df.empty:
            print(df.head(10).to_string(index=False))
        else:
            print("无财务数据")
    except Exception as e:
        print(f"财务数据获取失败: {e}")
