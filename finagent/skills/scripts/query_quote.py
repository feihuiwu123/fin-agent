#!/usr/bin/env python3
"""Stock quote query script."""
import sys
import akshare as ak

code = sys.argv[1] if len(sys.argv) > 1 else "600519"
df = ak.stock_zh_a_spot_em()
if df is not None and not df.empty:
    row = df[df["代码"] == code]
    if not row.empty:
        r = row.iloc[0]
        name = r.get("名称", "")
        price = r.get("最新价", 0)
        pct = r.get("涨跌幅", 0)
        high = r.get("最高", 0)
        low = r.get("最低", 0)
        open_p = r.get("今开", 0)
        prev = r.get("昨收", 0)
        amt = r.get("成交额", 0)
        amt_str = f"{amt/1e8:.2f}亿" if amt > 1e8 else f"{amt:.0f}"
        turnover = r.get("换手率", 0)
        pe = r.get("市盈率-动态", 0)
        pb = r.get("市净率", 0)
        print(f"name:{name}")
        print(f"price:{price}")
        print(f"pct:{pct}")
        print(f"high:{high}")
        print(f"low:{low}")
        print(f"open:{open_p}")
        print(f"prev:{prev}")
        print(f"amount:{amt_str}")
        print(f"turnover:{turnover}")
        print(f"pe:{pe}")
        print(f"pb:{pb}")
    else:
        print(f"未找到代码 {code}")
else:
    print("获取行情数据失败")
