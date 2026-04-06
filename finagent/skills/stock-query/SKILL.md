---
name: stock-query
description: Query A-share stock real-time quotes, financials, K-line data. Use for queries like "查 600519", stock codes, or company names.
---

# Stock Query — A-Share Stock Lookup

Use this skill when the user asks about a specific stock by code (e.g. "600519", "查 600519") or company name.

## Step 1: Find the stock by code or name

```bash
python3 -c "
import akshare as ak

code = '600519'  # Replace with user's stock code
df = ak.stock_zh_a_spot_em()
if df is not None and not df.empty:
    row = df[df['代码'] == code]
    if not row.empty:
        r = row.iloc[0]
        print(f'name:{r.get(\"名称\",\"\")}')
        print(f'price:{r.get(\"最新价\",0)}')
        print(f'pct:{r.get(\"涨跌幅\",0)}')
        print(f'high:{r.get(\"最高\",0)}')
        print(f'low:{r.get(\"最低\",0)}')
        print(f'open:{r.get(\"今开\",0)}')
        print(f'prev:{r.get(\"昨收\",0)}')
        amt = r.get('成交额', 0)
        amt_str = f'{amt/1e8:.2f}亿' if amt > 1e8 else f'{amt:.0f}'
        print(f'amount:{amt_str}')
        print(f'vol:{r.get(\"成交量\",0)}')
        print(f'turnover:{r.get(\"换手率\",0)}')
        print(f'pe:{r.get(\"市盈率-动态\",0)}')
        print(f'pb:{r.get(\"市净率\",0)}')
    else:
        print(f'未找到代码 {code}')
"
```

## Step 2: Get recent K-line data (30 days)

```bash
python3 -c "
import akshare as ak

code = '600519'  # Replace with user's stock code
try:
    df = ak.stock_zh_a_hist(symbol=code, period='daily', adjust='qfq')
    if df is not None and not df.empty:
        last = df.tail(10)
        for _, r in last.iterrows():
            d = str(r.get('日期',''))[:10]
            o = r.get('开盘',0); c = r.get('收盘',0)
            h = r.get('最高',0); l = r.get('最低',0)
            pct = r.get('涨跌幅',0); vol = r.get('成交量',0)
            print(f'{d} O:{o} H:{h} L:{l} C:{c} pct:{pct:+.2f}% vol:{vol:.0f}')
except Exception as e:
    print(f'K线数据获取失败: {e}')
"
```

## Step 3: Get financial summary

```bash
python3 -c "
import akshare as ak

code = '600519'  # Replace with user's stock code
try:
    df = ak.stock_financial_abstract_ths(symbol=code)
    if df is not None and not df.empty:
        print(df.tail(4).to_string(index=False))
except:
    try:
        df = ak.stock_financial_report_sina(stock=code, symbol='资产负债表')
        if df is not None and not df.empty:
            print(df.head(10).to_string(index=False))
    except Exception as e:
        print(f'财务数据获取失败: {e}')
"
```

## Response Format

Combine results into:

```
📊 个股查询 | Stock Query — 600519 贵州茅台
━━━━━━━━━━━━━━━━━━━━━━━━
  现价: XXX.XX  涨跌幅: +X.XX%
  今开: XXX  最高: XXX  最低: XXX  昨收: XXX
  成交额: XXX亿  换手率: X.XX%
  PE(动): XX.X  PB: X.XX

━━━━━━━━━━━━━━━━━━━━━━━━
📈 近10日K线
━━━━━━━━━━━━━━━━━━━━━━━━
  日期       开盘   最高   最低   收盘   涨跌幅
  2026-04-01  ...    ...    ...    ...    +X.XX%
  ...

⚠️ 失效条件: 数据为实时快照，盘中可能快速变化
```
