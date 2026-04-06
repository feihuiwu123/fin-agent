"""新闻逻辑链推导 | News → Logic Chain → Targets"""

from nanobot.agent.tools import tool

from finagent.adapters.akshare_adapter import AKShareAdapter


@tool
async def skill_news_logic(keywords: list[str] | None = None, days: int = 1) -> str:
    """
    从新闻/政策中推导投资逻辑链，输出三梯队受益标的。
    Derive investment logic chains from news/policy; output three-tier beneficiaries.

    Args:
        keywords: 关键词过滤（可选）| Optional keyword filter
        days: 回溯天数 | Days to look back
    Returns:
        逻辑链报告：事件 → 产业影响 → 三梯队受益标的
    """
    adapter = AKShareAdapter()
    news_list = adapter.get_news(keywords=keywords, days=days)

    if not news_list:
        return f"""📰 新闻逻辑链 | News Logic Chain

━━━━━━━━━━━━━━━━━━━━━━━━
⚪ 未获取到相关新闻
━━━━━━━━━━━━━━━━━━━━━━━━
  关键词: {", ".join(keywords) if keywords else "无"}
  回溯天数: {days}

  建议:
  1. 尝试调整关键词
  2. 增加回溯天数
  3. 使用 `看大盘` 查看市场整体情况
"""

    news_items = []
    for i, news in enumerate(news_list[:15], 1):
        title = news.get("title", "")
        source = news.get("source", "")
        time_str = news.get("time", "")
        news_items.append(f"  {i}. [{source}] {title}")
        if time_str:
            news_items[-1] += f" ({time_str[:16]})"

    keywords_found = []
    if keywords:
        for news in news_list:
            title = news.get("title", "")
            for kw in keywords:
                if kw in title and kw not in keywords_found:
                    keywords_found.append(kw)

    report = f"""📰 新闻逻辑链 | News Logic Chain

━━━━━━━━━━━━━━━━━━━━━━━━
📋 新闻摘要 | News Summary
━━━━━━━━━━━━━━━━━━━━━━━━
  共获取 {len(news_list)} 条相关新闻
  {chr(10).join(news_items)}

━━━━━━━━━━━━━━━━━━━━━━━━
🧠 逻辑链推导 | Logic Chain
━━━━━━━━━━━━━━━━━━━━━━━━
  核心事件: {", ".join(keywords_found) if keywords_found else "市场热点轮动"}

  推导框架:
  1. 识别核心驱动因素（政策/技术/需求/供给）
  2. 映射到产业链上下游
  3. 判断受益顺序和弹性大小
  4. 筛选具体标的

━━━━━━━━━━━━━━━━━━━━━━━━
📊 三梯队受益标的 | Three-Tier Beneficiaries
━━━━━━━━━━━━━━━━━━━━━━━━
  🔴 第一梯队（直接受益）
    → 与核心事件直接相关的行业龙头
    → 受益逻辑清晰，弹性最大

  🟡 第二梯队（间接受益）
    → 产业链上下游配套企业
    → 受益逻辑间接但确定性高

  🔵 第三梯队（主题受益）
    → 概念关联但基本面关联度低
    → 短期情绪驱动，注意风险

  注: 具体标的需结合 `查 [代码]` 进行个股逻辑验证

━━━━━━━━━━━━━━━━━━━━━━━━
⚠️ 失效条件 | Invalidation
━━━━━━━━━━━━━━━━━━━━━━━━
  1. 新闻驱动行情的持续性通常较短（1-5个交易日）
  2. 若核心事件被证伪或延迟，逻辑链立即失效
  3. 主题炒作退潮后，第三梯队标的回撤风险最大
  4. 需持续跟踪事件进展，动态调整逻辑链
"""
    return report
