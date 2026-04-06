#!/usr/bin/env python3
"""Daily hot topics summary script."""
import akshare as ak

# 1. 财新财经新闻
print("=== 财经新闻 ===")
try:
    df = ak.stock_news_main_cx()
    if df is not None and not df.empty:
        for _, row in df.head(10).iterrows():
            tag = row.get("tag", "")
            summary = row.get("summary", "")[:100]
            url = row.get("url", "")
            print(f"[{tag}] {summary}")
            print(f"  链接: {url}")
            print()
    else:
        print("无新闻数据")
except Exception as e:
    print(f"财新新闻获取失败: {e}")

# 2. 热门股票排行
print("=== 热门股票排行 ===")
try:
    df = ak.stock_hot_rank_em()
    if df is not None and not df.empty:
        for _, row in df.head(10).iterrows():
            rank = row.get("当前排名", "")
            code = row.get("代码", "")
            name = row.get("股票名称", "")
            price = row.get("最新价", "")
            pct = row.get("涨跌幅", "")
            print(f"#{rank} {name}({code}) 现价:{price} 涨跌:{pct:+.2f}%")
    else:
        print("无热门股票数据")
except Exception as e:
    print(f"热门股票获取失败: {e}")

# 3. 热门概念板块
print("=== 热门概念板块 ===")
try:
    df = ak.stock_hot_keyword_em()
    if df is not None and not df.empty:
        # Get unique concepts sorted by heat
        concepts = df.groupby("概念名称").agg({"热度": "max", "概念代码": "first"}).reset_index()
        concepts = concepts.sort_values("热度", ascending=False)
        for _, row in concepts.head(10).iterrows():
            name = row.get("概念名称", "")
            code = row.get("概念代码", "")
            heat = row.get("热度", "")
            print(f"  {name}({code}) 热度:{heat}")
    else:
        print("无热门概念数据")
except Exception as e:
    print(f"热门概念获取失败: {e}")
