---
name: stock-query
description: Query A-share stock real-time quotes, financials, K-line data. Use for queries like "查 600519", stock codes, or company names.
---

# Stock Query — A-Share Stock Lookup

Use this skill when the user asks about a specific stock by code (e.g. "600519", "查 600519") or company name.

**IMPORTANT**: Always use the venv python at `/home/finagent/fin-agent/.venv/bin/python3` to run these scripts. Never use `python3` directly.

## Step 1: Find the stock by code

```bash
/home/finagent/fin-agent/.venv/bin/python3 /home/finagent/fin-agent/finagent/skills/scripts/query_quote.py 600519
```

Replace `600519` with the user's stock code.

## Step 2: Get recent K-line data (10 days)

```bash
/home/finagent/fin-agent/.venv/bin/python3 /home/finagent/fin-agent/finagent/skills/scripts/query_kline.py 600519
```

Replace `600519` with the user's stock code.

## Step 3: Get financial summary

```bash
/home/finagent/fin-agent/.venv/bin/python3 /home/finagent/fin-agent/finagent/skills/scripts/query_financial.py 600519
```

Replace `600519` with the user's stock code.

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
