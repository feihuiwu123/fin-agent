---
name: hot-topics
description: Get daily hot news summary, global macro environment, key national policies, affected sectors, and direct/indirect beneficiary stock recommendations. Use for queries like "今日热点", "每日新闻总结", "global macro", "政策影响", "热点推送".
---

# Hot Topics — Daily News & Macro Analysis

Use this skill when the user asks about daily hot news, global macro environment, policy impacts, or sector recommendations.

**IMPORTANT**: Always use the venv python at `/home/finagent/fin-agent/.venv/bin/python3` to run these scripts. Never use `python3` directly.

## Step 1: Get hot topics (news + hot stocks + hot concepts)

```bash
/home/finagent/fin-agent/.venv/bin/python3 /home/finagent/fin-agent/finagent/skills/scripts/query_hot_topics.py
```

## Step 2: Get market breadth for context

```bash
/home/finagent/fin-agent/.venv/bin/python3 /home/finagent/fin-agent/finagent/skills/scripts/query_market_breadth.py
```

## Step 3: Get sector performance

```bash
/home/finagent/fin-agent/.venv/bin/python3 /home/finagent/fin-agent/finagent/skills/scripts/query_sectors.py
```

## Response Format

Combine all results into a comprehensive report:

```
📰 每日热点总结 | Daily Hot Topics — 2026-04-06
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📋 核心新闻摘要 (Top 5)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  1. [标签] 新闻摘要
  2. ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔥 今日热门股票 (Top 10)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  #1 股票名(代码) 现价:XX 涨跌:+X.XX%
  ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 热门概念板块 (Top 10)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  概念名(代码) 热度:XXX
  ...

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📈 市场概况
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  情绪: XXX
  上涨:XX 下跌:XX 涨停:XX 跌停:XX
  成交额: X.XX万亿

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎯 板块与标的分析
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  🔴 直接受益板块:
    • 板块名 (逻辑: XXX)
    • 相关个股: 股票名(代码)
  🟡 间接受益板块:
    • 板块名 (逻辑: XXX)
    • 相关个股: 股票名(代码)

⚠️ 失效条件: 热点驱动行情通常较短(1-5个交易日)，需持续跟踪
⚠️ 本分析仅供学习研究，不构成投资建议
```
