#!/usr/bin/env python3
"""Sector performance query script."""
import akshare as ak

try:
    df = ak.stock_board_industry_name_em()
    if df is not None and not df.empty:
        # Sort by change percentage, get top 10 and bottom 10
        df_sorted = df.sort_values("涨跌幅", ascending=False)
        print("=== 涨幅前10板块 ===")
        for _, row in df_sorted.head(10).iterrows():
            name = row.get("板块名称", "")
            pct = float(row.get("涨跌幅", 0))
            print(f"up|{name}|{pct:+.2f}")
        print("=== 跌幅前10板块 ===")
        for _, row in df_sorted.tail(10).iterrows():
            name = row.get("板块名称", "")
            pct = float(row.get("涨跌幅", 0))
            print(f"down|{name}|{pct:+.2f}")
except Exception as e:
    print(f"板块数据获取失败: {e}")
