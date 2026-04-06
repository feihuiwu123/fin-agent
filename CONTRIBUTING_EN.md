# Contributing Guide

Thank you for considering contributing to FinAgent!

> 🌐 [中文贡献指南](./CONTRIBUTING.md)

## How to Contribute a Skill

1. Fork this repository
2. Create a new file under `finagent/skills/` in the appropriate directory
3. Implement the Skill function (see template below)
4. Write tests (`tests/test_skills/`)
5. Submit a Pull Request

## Skill Template

```python
from nanobot.agent.tools import tool

@tool
async def skill_example(symbol: str) -> str:
    """
    Skill description

    Args:
        symbol: Stock code (e.g., "600519")
    Returns:
        Analysis result (must include rationale + invalidation)
    """
    # 1. Fetch data
    # 2. Calculate / Reason
    # 3. Return result
    return result
```

## Contribution Areas

- 🔌 Data Adapters — PTrade / TDX / US Stocks / HK Stocks / Crypto
- 🧠 Analysis Skills — More analysis dimensions
- 🌐 Internationalization — Improved docs, multi-language UI
- 📱 Channels — WeChat / Telegram / Discord
- 🧪 Testing — Unit tests, backtest validation
- 📖 Documentation — User tutorials, video guides

## Code of Conduct

Please maintain a friendly and inclusive environment.
