# 贡献指南

感谢你考虑为 FinAgent 做出贡献！

> 🌐 [English Contributing Guide](./CONTRIBUTING_EN.md)

## 如何贡献一个新 Skill

1. Fork 本仓库
2. 在 `finagent/skills/` 对应目录下创建新文件
3. 实现 Skill 函数（遵循下方规范）
4. 编写测试（`tests/test_skills/`）
5. 提交 Pull Request

## Skill 开发规范

```python
from nanobot.agent.tools import tool

@tool
async def skill_example(symbol: str) -> str:
    """
    Skill 描述

    Args:
        symbol: 股票代码 (e.g., "600519")
    Returns:
        分析结果（必须包含 rationale + invalidation）
    """
    # 1. 获取数据
    # 2. 计算/推理
    # 3. 返回结果
    return result
```

## 贡献方向

- 🔌 数据适配器 — PTrade / 通达信 / 美股 / 港股 / 加密货币
- 🧠 分析 Skills — 更多分析维度
- 🌐 国际化 — 英文文档完善、多语言界面
- 📱 Channel — 微信 / Telegram / Discord
- 🧪 测试 — 单元测试、回测验证
- 📖 文档 — 使用教程、视频教程

## 行为准则

请保持友善、包容的交流氛围。
