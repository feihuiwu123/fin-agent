# FinAgent — Agent Instructions

## Project Overview

FinAgent is a Python package for A-share (Chinese stock market) investment research, built on the **Nanobot AI Agent framework**. Core principle: every conclusion must have a **complete causal reasoning chain** and **explicit invalidation conditions**.

## Dev Setup

```bash
pip install -e ".[dev]"     # Install with dev dependencies
pip install nanobot-ai      # Separate dependency
nanobot onboard             # Initialize Nanobot config (~/.nanobot/config.json)
```

## Commands

```bash
ruff check .                 # Lint (configured in pyproject.toml)
ruff format .                # Format (line-length=100, py311)
pytest                        # Test (no tests exist yet)
mypy finagent/               # Typecheck
```

## Tooling Config

- **Linter/Formatter**: Ruff (`pyproject.toml` — no separate config)
- **Python**: 3.11+
- **Build**: setuptools>=68, wheel

## Package Structure

```
finagent/
├── skills/
│   ├── logic/       # Business model, financial, valuation (route: `查 [code]`)
│   ├── radar/       # Market pulse, news (route: `看大盘`, `今日热点`)
│   ├── chart/       # Trend, volume, decision (route: `K线 [code]`)
│   └── exec/        # Position, alerts, risk control (route: `我的持仓`, `设预警`)
├── adapters/        # Data sources (QMT, AKShare, PTrade, TDX — unimplemented)
├── db/              # Database layer (planned)
└── engine/          # Calculation engine (planned)
```

## Skill Development

Skills use `@tool` decorator from `nanobot.agent.tools`. Template:

```python
from nanobot.agent.tools import tool

@tool
async def skill_xxx(symbol: str) -> str:
    """
    Description (Chinese + English)
    Args:
        symbol: 股票代码 | Stock code (e.g., "600519")
    Returns:
        分析结果（必须包含 rationale + invalidation）
    """
    # 1. 获取数据 | Fetch data
    # 2. 计算/推理 | Calculate/Reason
    # 3. 返回结果 | Return result
    return result
```

All skills currently raise `NotImplementedError`.

## Linking Skills to Nanobot

```bash
cp -r finagent/skills/ ~/.nanobot/workspace/skills/
cp docs/SOUL.md ~/.nanobot/workspace/SOUL.md
```

## Running

```bash
nanobot agent -m "查 600519"   # CLI debug mode
nanobot gateway                 # Feishu bot + cron mode
```

## Risk Control Constants

Defined in `finagent/skills/exec/risk_check.py`:
- `MAX_SINGLE_POSITION_PCT = 0.20` (20% max per stock)
- `MAX_DAILY_LOSS_PCT = 0.03` (3% max daily loss)
- `MAX_TOTAL_DRAWDOWN_PCT = 0.15` (15% total drawdown)

## Routing Rules (from SOUL.md)

| Command | Skill Group |
|---------|------------|
| `查 [code]` | logic/* |
| `看大盘` | radar/index_pulse |
| `K线 [code]` | chart/trend → volume → decision |
| `我的持仓` | exec/position |
| `今日热点` | radar/news_logic |

## Key Files

- `SOUL.md` — Agent personality and routing rules
- `CONTRIBUTING.md` — Skill template and contribution guide
- `pyproject.toml` — All tooling config (no separate config files)
