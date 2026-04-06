---
name: market-pulse
description: Get A-share market overview, index data, sentiment analysis. Use for queries about "大盘", "market", "index", "today's market", "今天大盘".
---

# Market Pulse — A-Share Market Overview

Use this skill when the user asks about the overall market (大盘), index performance, or market sentiment.

## How to use

Run this command to get current market data:

```bash
python3 -c "
import akshare as ak

# Market breadth
df = ak.stock_zh_a_spot_em()
if df is not None and not df.empty:
    total = len(df)
    up = len(df[df['涨跌幅'] > 0])
    down = len(df[df['涨跌幅'] < 0])
    flat = total - up - down
    limit_up = len(df[df['涨跌幅'] >= 9.9])
    limit_down = len(df[df['涨跌幅'] <= -9.9])
    avg = df['涨跌幅'].mean()
    amount = df['成交额'].sum()
    amt_str = f'{amount/1e12:.2f}万亿' if amount > 1e12 else f'{amount/1e8:.2f}亿'
    
    ratio = up/(up+down)*100 if up+down > 0 else 50
    if ratio > 70 and avg > 1.5 and limit_up > 50:
        sentiment = '极度乐观 🔴'
    elif ratio > 55 and avg > 0.5:
        sentiment = '偏乐观 🟠'
    elif ratio > 45:
        sentiment = '观望 🟡'
    elif ratio > 30:
        sentiment = '偏悲观 🔵'
    else:
        sentiment = '恐慌 🔴'
    
    print(f'🌡️ 大盘体温计')
    print(f'市场情绪: {sentiment}')
    print(f'上涨: {up} 下跌: {down} 平盘: {flat}')
    print(f'涨停: {limit_up} 跌停: {limit_down}')
    print(f'平均涨跌: {avg:+.2f}%')
    print(f'上涨占比: {ratio:.1f}%')
    print(f'总成交额: {amt_str}')
"
```

## Index Data

```bash
python3 -c "
import akshare as ak

indices = {'上证指数': 'sh000001', '深证成指': 'sz399001', '创业板指': 'sz399006', '沪深300': 'sh000300', '科创50': 'sh000688'}
for name, sym in indices.items():
    try:
        df = ak.stock_zh_index_daily(symbol=sym)
        if df is not None and not df.empty:
            last = df.iloc[-1]
            prev = df.iloc[-2] if len(df) > 1 else last
            close = float(last['close'])
            prev_close = float(prev['close'])
            pct = (close - prev_close) / prev_close * 100 if prev_close > 0 else 0
            arrow = '🔺' if pct > 0 else '🔻' if pct < 0 else '➖'
            print(f'{arrow} {name}: {close:.2f} ({pct:+.2f}%)')
    except: pass
"
```

## Response Format

Combine the results into a structured response:

```
🌡️ 大盘体温计 | Market Pulse
━━━━━━━━━━━━━━━━━━━━━━━━
🟡 市场情绪: 观望
━━━━━━━━━━━━━━━━━━━━━━━━
  上涨: XXX 家  下跌: XXX 家  平盘: XXX 家
  涨停: XX 家  跌停: XX 家
  平均涨跌: +X.XX%
  总成交额: X.XX 万亿

━━━━━━━━━━━━━━━━━━━━━━━━
📊 主要指数 | Major Indices
━━━━━━━━━━━━━━━━━━━━━━━━
  🔺 上证指数: XXXX.XX (+X.XX%)
  🔻 深证成指: XXXX.XX (-X.XX%)
  ...

⚠️ 失效条件: 情绪指标基于当日盘面，次日可能快速反转
```
