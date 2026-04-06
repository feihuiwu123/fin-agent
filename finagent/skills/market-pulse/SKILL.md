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
🌡️ 大盘 — 2026-04-06
─── 情绪 ───
市场情绪: 观望
涨:XXX 跌:XXX 平:XXX 涨停:XX 跌停:XX
平均:+X.XX% 成交:X.XX万亿

─── 主要指数 ───
🔺 上证指数: XXXX.XX (+X.XX%)
🔻 深证成指: XXXX.XX (-X.XX%)
...

⚠️ 情绪指标基于当日盘面，次日可能反转
```
