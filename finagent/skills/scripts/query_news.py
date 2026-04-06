#!/usr/bin/env python3
"""Financial news query script — uses 财新 (caixin) source with links."""
import sys
import akshare as ak

code = sys.argv[1] if len(sys.argv) > 1 else ""
try:
    df = ak.stock_news_main_cx()
    if df is not None and not df.empty:
        for _, row in df.head(15).iterrows():
            tag = row.get("tag", "")
            summary = row.get("summary", "")
            url = row.get("url", "")
            print(f"[{tag}] {summary}")
            print(f"  🔗 {url}")
            print()
    else:
        print("暂无新闻")
except Exception as e:
    print(f"新闻获取失败: {e}")
