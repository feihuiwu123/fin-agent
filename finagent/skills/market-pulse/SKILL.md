---
name: market-pulse
description: Get A-share market overview, index data, sentiment analysis. Use for queries about "大盘", "market", "index", "today's market", "今天大盘".
---

# Market Pulse — A-Share Market Overview

Use this skill when the user asks about the overall market (大盘), index performance, or market sentiment.

**IMPORTANT**: Always use the venv python at `/home/finagent/fin-agent/.venv/bin/python3` to run these scripts. Never use `python3` directly.

## Step 1: Market breadth data

```bash
/home/finagent/fin-agent/.venv/bin/python3 /home/finagent/fin-agent/finagent/skills/scripts/query_market_breadth.py
```

## Step 2: Index data

```bash
/home/finagent/fin-agent/.venv/bin/python3 /home/finagent/fin-agent/finagent/skills/scripts/query_indices.py
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
