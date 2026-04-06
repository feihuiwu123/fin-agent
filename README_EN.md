<p align="center">
  <img src="docs/assets/logo.png" alt="FinAgent Logo" width="120" />
</p>

<h1 align="center">FinAgent 📊</h1>

<p align="center">
  <strong>Logic-Closed-Loop A-Share Investment Research Assistant</strong>
</p>

<p align="center">
  <a href="#quick-start">Quick Start</a> •
  <a href="#core-features">Features</a> •
  <a href="#system-architecture">Architecture</a> •
  <a href="#skill-list">Skills</a> •
  <a href="#roadmap">Roadmap</a> •
  <a href="#contributing">Contributing</a> •
  <a href="./README.md">中文</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.11+-blue.svg" alt="Python" />
  <img src="https://img.shields.io/badge/framework-nanobot-orange.svg" alt="Nanobot" />
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License" />
</p>

---

## What is this?

FinAgent is an open-source A-share (Chinese stock market) intelligent investment research assistant, built on the [Nanobot](https://github.com/HKUDS/nanobot) lightweight AI Agent framework, with Feishu (Lark) bot as its primary interface.

**It is NOT another "AI stock picker."** Most AI trading tools simply list indicators, pile up data, and give you a vague "recommend buy." FinAgent is different — its core design principle is the **Logic Closed-Loop**: every conclusion must come with a complete causal reasoning chain and explicit invalidation conditions.

```
📰 Trigger Signal
  → 🧠 First-Principles Reasoning
    → 🔗 Industry Chain Mapping
      → 📊 Data Validation
        → 💰 Valuation & Position
          → ✅ Action + ❌ Invalidation Conditions
```

---

## Core Features

### 📊 Logic Analysis

Enter a stock code and get a **logic-closed-loop verification report**, not a traditional research note.

- **Business Model Identification** — What's the essence of how this company makes money?
- **Moat Assessment** — Is the competitive barrier strengthening or weakening?
- **Policy Mapping** — Is there national-level policy support?
- **Financial Verification** — Do the numbers support the thesis?
- **Closed-Loop Conclusion** — Does the money-making logic hold + invalidation conditions

### 📡 Market Radar

Not a news aggregator, but **deriving investment logic chains from news and policy**.

- **Market Thermometer** — Sentiment indicator (euphoria / neutral / panic)
- **Logic Chain Derivation** — Event → industry impact → beneficiary segments → specific targets
- **Three-Tier Mapping** — Direct / indirect / thematic beneficiaries
- **Portfolio Cross-Reference** — Auto cross-reference hot topics with your holdings
- **Daily Push** — Pre-market 08:30 / Post-market 15:15 auto-push via Feishu

### 📈 Chart Decision

Not displaying indicator values, but **directly answering "what should I do now."**

- **Volume Patterns** — Surge / shrink / staircase / floor volume recognition
- **Trend Judgment** — MA alignment + multi-timeframe resonance
- **Decision Output** — Hold / add / reduce / clear + TP/SL levels + risk-reward ratio
- **Logic Re-check** — Is the original buying thesis still valid?

### ⚡ Execution & Risk Control

- **Feishu Interaction** — Natural language commands (`查600519` / `看大盘` / `K线 300750`)
- **Conditional Alerts** — Price break/breakdown, volume surge, MACD golden cross, etc.
- **Trade Gateway Reserved** — QMT/PTrade/TDX interface reserved, HITL confirmation
- **Hard Risk Limits** — Max single position, daily loss cap, total drawdown protection

---

## System Architecture

### One Nanobot, Four Skill Groups

FinAgent runs on a **single Nanobot instance**. The four functional domains are four Skill groups, orchestrated by one Agent Loop via routing rules in SOUL.md.

```
┌─────────────────────────────────────────────────────┐
│              Nanobot Gateway (Single Instance)        │
├─────────────────────────────────────────────────────┤
│                                                       │
│  SOUL.md ── Role + Routing + Output Format            │
│                                                       │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌────────┐│
│  │📊 Logic   │ │📡 Market  │ │📈 Chart   │ │⚡ Exec  ││
│  │  Analysis │ │  Radar    │ │ Decision  │ │ Skills ││
│  └─────┬─────┘ └─────┬─────┘ └─────┬─────┘ └───┬────┘│
│        └──────────────┼──────────────┘           │     │
│                       ▼                          │     │
│              ┌────────────────┐                  │     │
│              │ Python Engine  │                  │     │
│              │ pandas_ta/TA-Lib│                  │     │
│              └────────┬───────┘                  │     │
│                       ▼                          ▼     │
│  ┌──────────────────────────────────────────────────┐  │
│  │           Unified Data Layer                      │  │
│  │  ┌─────┐ ┌────────┐ ┌──────┐ ┌─────┐ ┌──────┐  │  │
│  │  │ QMT │ │AKShare │ │PTrade│ │ TDX │ │ US   │  │  │
│  │  │ ✅  │ │  ✅    │ │Reserved│ │Reserved│ │Reserved││
│  │  └─────┘ └────────┘ └──────┘ └─────┘ └──────┘  │  │
│  └──────────────────────────────────────────────────┘  │
│                                                       │
│  Channel: FeishuBot    Cron: Scheduled    Memory: Positions│
└─────────────────────────────────────────────────────┘
```

### Three-Layer Business Architecture

| Layer | Responsibility | Key Components |
|-------|---------------|----------------|
| **L3 Interface & Execution** | User interaction + Trade execution | Feishu Bot · Cron · Trade Gateway (QMT/PTrade/TDX) |
| **L2 Intelligence & Reasoning** | AI reasoning + Indicator calculation | Nanobot Agent Loop · LLM · Skills · pandas_ta |
| **L1 Unified Data** | Data fetching + Storage | DataAdapter (QMT/AKShare/...) · SQLite · Memory |

### Data Adapter Pattern

All market data sources implement the same abstract interface. Adding a new market only requires implementing a subclass:

```python
class DataAdapter(ABC):
    """Unified data adapter interface"""
    def get_kline(self, symbol, period, count) -> pd.DataFrame: ...
    def get_realtime_quote(self, symbol) -> dict: ...
    def get_financials(self, symbol) -> dict: ...
    def get_fund_flow(self, symbol) -> dict: ...
    def get_news(self, keywords, days) -> list: ...

class TradeAdapter(ABC):
    """Unified trade interface"""
    def place_order(self, symbol, side, qty, price, order_type): ...
    def cancel_order(self, order_id) -> bool: ...
    def get_positions(self) -> list: ...
    def get_account_info(self) -> dict: ...

# Phase 1 Implementation
class QMTAdapter(DataAdapter): ...      # XunTou QMT (xtquant)
class AKShareAdapter(DataAdapter): ...  # AKShare (free)

# Reserved
class PTradeAdapter(DataAdapter): ...   # Hundsun PTrade
class TDXAdapter(DataAdapter): ...      # TongDaXin
class USStockAdapter(DataAdapter): ...  # US Stocks (yfinance / IB)
class CryptoAdapter(DataAdapter): ...   # Crypto (CCXT)
```

---

## Quick Start

### Prerequisites

- Python 3.11+
- An LLM API Key (DeepSeek / Qwen / OpenRouter / OpenCode recommended)
- Feishu enterprise self-built app (for Bot integration)

### Installation

```bash
# 1. Clone the repo
git clone https://github.com/yourname/finagent.git
cd finagent

# 2. Install dependencies
pip install -e .

# 3. Install Nanobot
pip install nanobot-ai

# 4. Initialize config
nanobot onboard
```

### Configuration

Copy the environment variable template and fill in your credentials:

```bash
cp .env.example .env
# Edit the .env file with your API Key
```

The `.env` file is included in `.gitignore` and will never be committed to Git, keeping your keys safe:

```bash
# .env — Credentials (never uploaded to Git)
LLM_PROVIDER=deepseek
LLM_API_KEY=sk-your-key-here
LLM_API_BASE=https://api.deepseek.com/v1
LLM_MODEL=deepseek/deepseek-chat

FEISHU_ENABLED=false
FEISHU_APP_ID=your-feishu-app-id
FEISHU_APP_SECRET=your-feishu-app-secret
```

The deploy script automatically reads configuration from `.env`. If you need to manually configure `~/.nanobot/config.json`:

```jsonc
{
  "providers": {
    "deepseek": {
      "apiKey": "sk-xxx",
      "apiBase": "https://api.deepseek.com/v1"
    }
  },
  "agents": {
    "defaults": {
      "model": "deepseek/deepseek-chat",
      "temperature": 0.3,
      "maxTokens": 8192,
      "memoryWindow": 50
    }
  },
  "channels": {
    "feishu": {
      "enabled": true,
      "appId": "YOUR_FEISHU_APP_ID",
      "appSecret": "YOUR_FEISHU_APP_SECRET"
    }
  },
  "tools": {
    "restrictToWorkspace": false
  }
}
```

Link FinAgent Skills to Nanobot workspace:

```bash
cp -r finagent/skills/ ~/.nanobot/workspace/skills/
cp finagent/SOUL.md ~/.nanobot/workspace/SOUL.md
```

### Launch

```bash
# CLI mode (debug)
nanobot agent -m "查 600519"

# Start gateway (Feishu Bot + Cron)
nanobot gateway
```

### Feishu Commands

| Command | Function | Example |
|---------|----------|---------|
| `查 [code]` | Stock logic analysis | `查 600519` |
| `看大盘` | Market radar | `看大盘` |
| `K线 [code]` | Chart decision analysis | `K线 300750` |
| `K线 [code] 周线` | Specify timeframe | `K线 300750 周线` |
| `我的持仓` | List positions | `我的持仓` |
| `加持仓 [code] [cost] [qty]` | Add position | `加持仓 600519 1750 100` |
| `设预警 [code] [condition]` | Set alert | `设预警 600519 跌破1700` |
| `今日热点` | Hot topic logic chain | `今日热点` |

---

## Skill List

### P0 — MVP (Phase 1)

| Skill | Group | Function |
|-------|-------|----------|
| `skill-biz-model` | 📊 Logic Analysis | Business model + loop verification |
| `skill-financial` | 📊 Logic Analysis | Financial health (revenue/ROE/debt ratio) |
| `skill-valuation` | 📊 Logic Analysis | PE/PB historical percentile |
| `skill-index-pulse` | 📡 Market Radar | Index data + sentiment judgment |
| `skill-news-logic` | 📡 Market Radar | News → logic chain → targets |
| `skill-trend` | 📈 Chart Decision | MA alignment + trend |
| `skill-volume` | 📈 Chart Decision | Volume patterns (surge/shrink/staircase/floor) |
| `skill-decision` | 📈 Chart Decision | Action + risk-reward ratio |
| `skill-feishu` | ⚡ Execution | Feishu messaging |
| `skill-position` | ⚡ Execution | Position management |
| `skill-alert` | ⚡ Execution | Conditional alerts |

### P1 — Phase 2 Enhancements

| Skill | Function |
|-------|----------|
| `skill-policy` | Policy scan + beneficiary mapping |
| `skill-team` | Management + shareholder analysis |
| `skill-moat` | Deep moat analysis |
| `skill-sector-flow` | Sector rotation + fund flow |
| `skill-portfolio-link` | Hot topics × portfolio cross-reference |
| `skill-signal` | MACD/KDJ/BOLL comprehensive signal |
| `skill-risk-check` | Risk control engine |
| `skill-trade-gateway` | QMT live trading |

### P2 — Future Extensions

| Skill | Function |
|-------|----------|
| `skill-backtest` | Strategy backtesting |
| `skill-sentiment` | Community sentiment |
| `skill-replay` | Trade review reports |
| `skill-us-stock` | US stock adapter |
| `skill-hk-stock` | HK stock adapter |
| `skill-crypto` | Crypto adapter |
| `skill-ptrade` | PTrade adapter |
| `skill-tdx` | TDX adapter |

---

## Project Structure

```
finagent/
├── README.md                    # Chinese version
├── README_EN.md                 # This file (English)
├── LICENSE                      # MIT License
├── pyproject.toml               # Python project config
│
├── docs/                        # Documentation
│   ├── AGENTS.md                # Agent development instructions
│   ├── CONTRIBUTING.md          # Contributing guide (Chinese)
│   ├── CONTRIBUTING_EN.md       # Contributing guide (English)
│   ├── SOUL.md                  # Agent personality (Chinese)
│   └── SOUL_EN.md               # Agent personality (English)
│
├── scripts/                     # Scripts
│   └── deploy.sh                # One-click deploy script
│
├── config/                      # Config examples
│   ├── config.example.json
│   └── cron.example.json
│
├── finagent/                    # Main source code
│   ├── __init__.py
│   │
│   ├── adapters/                # Data adapters
│   │   ├── base.py              # Abstract interface
│   │   ├── qmt_adapter.py       # XunTou QMT
│   │   ├── akshare_adapter.py   # AKShare
│   │   ├── ptrade_adapter.py    # PTrade (reserved)
│   │   └── tdx_adapter.py       # TongDaXin (reserved)
│   │
│   ├── skills/                  # Skill modules
│   │   ├── logic/               # 📊 Logic Analysis
│   │   │   ├── biz_model.py     # Business model analysis
│   │   │   ├── financial.py     # Financial health
│   │   │   └── valuation.py     # Valuation percentile
│   │   │
│   │   ├── radar/               # 📡 Market Radar
│   │   │   ├── index_pulse.py   # Market thermometer
│   │   │   └── news_logic.py    # News logic chain
│   │   │
│   │   ├── chart/               # 📈 Chart Decision
│   │   │   ├── trend.py         # Trend judgment
│   │   │   ├── volume.py        # Volume patterns
│   │   │   └── decision.py      # Integrated decision
│   │   │
│   │   └── exec/                # ⚡ Execution & Risk
│   │       ├── feishu.py        # Feishu messaging
│   │       ├── position.py      # Position management
│   │       ├── alert.py         # Conditional alerts
│   │       ├── risk_check.py    # Risk control rules
│   │       └── trade_gateway.py # Trade gateway (reserved)
│   │
│   ├── engine/                  # Calculation engine
│   │   ├── indicators.py        # Technical indicators
│   │   ├── volume_patterns.py   # Volume pattern algorithms
│   │   └── key_levels.py        # Support & resistance levels
│   │
│   ├── db/                      # Data storage
│   │   ├── models.py            # SQLite data models
│   │   └── database.py          # Database operations
│   │
│   └── templates/               # Output templates
│       ├── logic_report.md      # Logic analysis report
│       ├── market_brief.md      # Market brief
│       └── chart_decision.md    # Chart decision
│
├── config/                      # Config files
│   ├── config.example.json      # Nanobot config example
│   └── cron.example.json        # Cron job example
│
├── docs/                        # Documentation
│   ├── architecture.md          # Architecture details
│   ├── skill-development.md     # Skill development guide
│   ├── data-adapters.md         # Data adapter docs
│   ├── feishu-setup.md          # Feishu setup tutorial
│   ├── qmt-setup.md             # QMT setup tutorial
│   └── assets/                  # Image assets
│
└── tests/                       # Tests
    ├── test_adapters/
    ├── test_skills/
    └── test_engine/
```

---

## Design Philosophy

### Five Iron Rules of Logic Closed-Loop

1. **Traceable** — The system can explain any recommendation within 3 reasoning layers
2. **Falsifiable** — Every conclusion must include invalidation conditions
3. **No Black Box** — Prefer explainable logic over opaque models
4. **Swing Focus** — Daily chart primary, weekly confirmation, no intraday noise
5. **Risk First** — Ask "how much can I lose" before "how much can I gain"

### Logic Chain Output Template

Example output (excerpt):

```
📰 Key News Points:
  1. Domestic LLM API calls exceeded foreign models for a consecutive month
  2. OpenClaw is the core driver of this Token consumption surge
  3. Model vendors and cloud providers announced price hikes

🧠 Investment Logic Derivation:
  OpenClaw demand → Token consumption explosion (100~1000x per task)
    → Insufficient compute capacity → Compute price hike
      → Surge in upstream compute/power/storage demand

📊 Beneficiary Sector Analysis:
  🔴 First Tier (Direct Beneficiaries)
    ┌────────┬──────────────────┬──────────────┐
    │ Sector │ Logic            │ A-Share Target│
    ├────────┼──────────────────┼──────────────┤
    │ AI Comp│ Price hike cycle │ Zhongji Innolight│
    │ AI Comp│ Token demand surge│ Zhongke Electric│
    │ Optical│ Data center interconnect│ Zhongma Transmission│
    └────────┴──────────────────┴──────────────┘

  🟡 Second Tier (Indirect Beneficiaries)  ...
  🔵 Third Tier (Thematic Beneficiaries)  ...

🔗 Correlation with Your Portfolio:
  ┌──────────────┬──────────┬────────────────┐
  │ Holding      │ Correlation│ Suggestion     │
  ├──────────────┼──────────┼────────────────┤
  │ China Nuclear│ 🔴 Direct │ Data center power│
  │ Aoruide      │ ⚪ None   │ Trade as planned│
  └──────────────┴──────────┴────────────────┘

⚠️ Invalidation Conditions:
  1. If price increase falls short of expectation (<5%), upstream logic weakens
  2. If April 18 price adjustment doesn't materialize, short-term sentiment fades
```

---

## Tech Stack

| Component | Choice | Note |
|-----------|--------|------|
| Agent Framework | [Nanobot](https://github.com/HKUDS/nanobot) | ~4000 lines of Python, lightweight OpenClaw alternative |
| LLM | DeepSeek-V3 (primary) / Qwen (backup) | Strong Chinese understanding, low API cost |
| Market Data | QMT (xtquant) + AKShare | QMT real-time quotes, AKShare free supplement |
| Technical Indicators | pandas_ta / TA-Lib | MA/MACD/KDJ/BOLL/volume calculation |
| Local Storage | SQLite | Positions, trade logs, alert configs, zero-config |
| Messaging | Feishu Open Platform | Bot integration, interactive cards, WebSocket |
| Trade Interface | QMT miniQMT (reserved) | xtquant Python API |
| Deployment | Docker / systemd | One-click start |

---

## Roadmap

| Phase | Goal | Duration |
|-------|------|----------|
| **M0** | 🔧 Setup: Nanobot + Feishu + AKShare integration | 1 week |
| **M1** | 📈 Chart Decision skills (easiest to validate) | 1 week |
| **M2** | 📊 Logic Analysis skills (core differentiator) | 2 weeks |
| **M3** | 📡 Market Radar skills + Cron auto-push | 2 weeks |
| **M4** | ⚡ Execution & Risk + Alerts + Trade simulation | 1 week |
| **M5** | 🧪 Integration test + Docs + Open-source release | 1 week |

**~8 weeks to usable MVP**

---

## Contributing

We welcome all forms of contribution!

### How to Contribute a Skill

1. Fork this repository
2. Create a new file under `finagent/skills/` in the appropriate directory
3. Implement the Skill function (follow the [Skill Development Guide](docs/skill-development.md))
4. Write tests
5. Submit a Pull Request

```python
# Skill Template
from nanobot.agent.tools import tool

@tool
async def skill_example(symbol: str) -> str:
    """
    Skill description

    Args:
        symbol: Stock symbol (e.g., "600519")
    Returns:
        Analysis result
    """
    # 1. Fetch data
    # 2. Calculate / Reason
    # 3. Return (must include rationale + invalidation)
    return result
```

### Contribution Areas

- 🔌 **Data Adapters** — PTrade / TDX / US Stocks / HK Stocks / Crypto
- 🧠 **Analysis Skills** — More analysis dimensions (industry comparison, shareholder changes, etc.)
- 🌐 **Internationalization** — Improved English docs, multi-language UI
- 📱 **Channels** — WeChat / Telegram / Discord integration
- 🧪 **Testing** — Unit tests, backtest validation
- 📖 **Documentation** — User tutorials, video guides

---

## Disclaimer

> ⚠️ **FinAgent is for educational and research purposes only. It does NOT constitute investment advice.**

- AI analysis carries "hallucination" risks; all conclusions require human verification
- Past backtest performance does not guarantee future returns
- Automated trading carries technical failure risks (network interruption, API anomalies, slippage, etc.)
- Users are fully responsible for their own investment decisions
- Investing involves risk; trade with caution

---

## Acknowledgments

- [Nanobot](https://github.com/HKUDS/nanobot) — Lightweight AI Agent framework from HKU HKUDS Lab
- [OpenClaw](https://github.com/openclaw) — Inspiration for Skill modular design
- [AKShare](https://github.com/akfamily/akshare) — Excellent open-source A-share data interface
- [XunTou QMT](https://www.thinktrader.net/) — Quantitative trading interface
- [pandas_ta](https://github.com/twopirllc/pandas-ta) — Technical indicator library

---

## License

[MIT License](LICENSE) — Free to use, modify, and distribute.

---

<p align="center">
  <strong>If you find this useful, please give us a ⭐ Star!</strong>
</p>
