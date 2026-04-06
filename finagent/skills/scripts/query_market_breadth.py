#!/usr/bin/env python3
"""Market breadth query script."""
import akshare as ak

df = ak.stock_zh_a_spot_em()
if df is not None and not df.empty:
    total = len(df)
    up = len(df[df["涨跌幅"] > 0])
    down = len(df[df["涨跌幅"] < 0])
    flat = total - up - down
    limit_up = len(df[df["涨跌幅"] >= 9.9])
    limit_down = len(df[df["涨跌幅"] <= -9.9])
    avg = df["涨跌幅"].mean()
    amount = df["成交额"].sum()
    amt_str = f"{amount/1e12:.2f}万亿" if amount > 1e12 else f"{amount/1e8:.2f}亿"

    ratio = up / (up + down) * 100 if up + down > 0 else 50
    if ratio > 70 and avg > 1.5 and limit_up > 50:
        sentiment = "极度乐观 🔴"
    elif ratio > 55 and avg > 0.5:
        sentiment = "偏乐观 🟠"
    elif ratio > 45:
        sentiment = "观望 🟡"
    elif ratio > 30:
        sentiment = "偏悲观 🔵"
    else:
        sentiment = "恐慌 🔴"

    print(f"sentiment:{sentiment}")
    print(f"up:{up}")
    print(f"down:{down}")
    print(f"flat:{flat}")
    print(f"limit_up:{limit_up}")
    print(f"limit_down:{limit_down}")
    print(f"avg:{avg:+.2f}")
    print(f"ratio:{ratio:.1f}")
    print(f"amount:{amt_str}")
else:
    print("获取市场数据失败")
