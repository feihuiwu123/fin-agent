#!/usr/bin/env python3
"""Financial news query script."""
import sys
import akshare as ak

code = sys.argv[1] if len(sys.argv) > 1 else ""
try:
    df = ak.stock_news_em(symbol=code)
    if df is not None and not df.empty:
        for _, row in df.head(15).iterrows():
            title = row.get("新闻标题", "")
            source = row.get("新闻来源", "")
            time = str(row.get("发布时间", ""))[:16]
            content = row.get("新闻内容", "")[:80]
            print(f"[{source}] {title}")
            if time:
                print(f"  时间: {time}")
            if content:
                print(f"  摘要: {content}...")
            print()
    else:
        print("暂无新闻")
except Exception as e:
    print(f"新闻获取失败: {e}")
