---
name: news-research
description: Get A-share financial news, policy news, market events. Use for queries about "新闻", "政策", "消息", "热点", "今日热点".
---

# News & Research — A-Share Market News

Use this skill when the user asks about market news, policy changes, or hot topics.

## Get Recent Financial News

```bash
python3 -c "
import akshare as ak

try:
    df = ak.stock_news_em(symbol='')
    if df is not None and not df.empty:
        for _, row in df.head(15).iterrows():
            title = row.get('新闻标题', '')
            source = row.get('新闻来源', '')
            time = str(row.get('发布时间', ''))[:16]
            content = row.get('新闻内容', '')[:80]
            print(f'[{source}] {title}')
            if time:
                print(f'  时间: {time}')
            if content:
                print(f'  摘要: {content}...')
            print()
    else:
        print('暂无新闻')
except Exception as e:
    print(f'新闻获取失败: {e}')
"
```

## Get News for Specific Stock

```bash
python3 -c "
import akshare as ak

code = '600519'  # Replace with user's stock code
try:
    df = ak.stock_news_em(symbol=code)
    if df is not None and not df.empty:
        for _, row in df.head(10).iterrows():
            title = row.get('新闻标题', '')
            source = row.get('新闻来源', '')
            time = str(row.get('发布时间', ''))[:16]
            print(f'[{source}] {title} ({time})')
    else:
        print(f'未找到 {code} 的相关新闻')
except Exception as e:
    print(f'新闻获取失败: {e}')
"
```

## Response Format

```
📰 新闻逻辑链 | News Logic Chain
━━━━━━━━━━━━━━━━━━━━━━━━
📋 新闻摘要 (共 X 条)
━━━━━━━━━━━━━━━━━━━━━━━━
  1. [来源] 新闻标题 (时间)
     摘要: ...
  2. ...

━━━━━━━━━━━━━━━━━━━━━━━━
🧠 逻辑链推导
━━━━━━━━━━━━━━━━━━━━━━━━
  核心事件: XXX
  影响板块: XXX
  受益标的: 结合 查[代码] 进行个股验证

⚠️ 失效条件: 新闻驱动行情通常较短(1-5个交易日)，需持续跟踪
```
