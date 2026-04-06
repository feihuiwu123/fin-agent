---
name: news-research
description: Get A-share financial news, policy news, market events. Use for queries about "新闻", "政策", "消息", "热点", "今日热点".
---

# News & Research — A-Share Market News

Use this skill when the user asks about market news, policy changes, or hot topics.

**IMPORTANT**: Always use the venv python at `/home/finagent/fin-agent/.venv/bin/python3` to run these scripts. Never use `python3` directly.

## Get Recent Financial News

```bash
/home/finagent/fin-agent/.venv/bin/python3 /home/finagent/fin-agent/finagent/skills/scripts/query_news.py
```

## Get News for Specific Stock

```bash
/home/finagent/fin-agent/.venv/bin/python3 /home/finagent/fin-agent/finagent/skills/scripts/query_news.py 600519
```

Replace `600519` with the user's stock code.

## Response Format

```
📰 新闻 — 2026-04-06
─── 新闻摘要 ───
1. [来源] 标题 (时间)
   摘要: ...
   🔗 链接
2. ...

─── 逻辑链 ───
核心事件: XXX
影响板块: XXX
受益标的: 结合 查[代码] 验证

⚠️ 新闻驱动行情通常较短(1-5日)，需持续跟踪
```
