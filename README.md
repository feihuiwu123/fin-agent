<p align="center">
  <img src="docs/assets/logo.png" alt="FinAgent Logo" width="120" />
</p>

<h1 align="center">FinAgent 📊</h1>

<p align="center">
  <strong>基于逻辑闭环的 A 股智能投研助理 | Logic-Closed-Loop A-Share Investment Research Assistant</strong>
</p>

<p align="center">
  <a href="#快速开始--quick-start">快速开始</a> •
  <a href="#核心功能--core-features">功能</a> •
  <a href="#系统架构--system-architecture">架构</a> •
  <a href="#技能清单--skill-list">技能</a> •
  <a href="#路线图--roadmap">路线图</a> •
  <a href="#贡献指南--contributing">贡献</a> •
  <a href="./README_EN.md">English</a>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.11+-blue.svg" alt="Python" />
  <img src="https://img.shields.io/badge/framework-nanobot-orange.svg" alt="Nanobot" />
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="License" />
  <img src="https://img.shields.io/badge/lang-中文%20%7C%20English-brightgreen.svg" alt="Bilingual" />
</p>

---

## 这是什么？ | What is this?

FinAgent 是一个开源的 A 股智能投研助理，基于 [Nanobot](https://github.com/HKUDS/nanobot) 轻量级 AI Agent 框架构建，通过飞书机器人进行交互。

**它不是另一个"AI选股工具"。** 市面上大多数 AI 炒股工具的做法是罗列指标、堆砌数据，然后给你一个模糊的"推荐买入"。FinAgent 不同——它的核心设计原则是**逻辑闭环**：每一条分析结论都必须有完整的因果推导链条，并且明确给出"什么情况下逻辑不成立"。

FinAgent is an open-source A-share intelligent investment research assistant built on the [Nanobot](https://github.com/HKUDS/nanobot) lightweight AI Agent framework, with Feishu (Lark) bot as its primary interface.

**It is NOT another "AI stock picker."** Most AI trading tools simply list indicators and give vague "buy" signals. FinAgent is different — its core design principle is the **Logic Closed-Loop**: every conclusion must come with a complete causal reasoning chain and explicit invalidation conditions.

```
📰 触发信号 (Trigger)
  → 🧠 第一性原理推导 (First-Principles Reasoning)
    → 🔗 产业链映射 (Industry Chain Mapping)
      → 📊 数据验证 (Data Validation)
        → 💰 估值与位置 (Valuation & Position)
          → ✅ 操作建议 + ❌ 失效条件 (Action + Invalidation)
```

---

## 核心功能 | Core Features

### 📊 逻辑分析 | Logic Analysis

输入一只股票代码，获得一份**逻辑闭环验证报告**，而不是传统研报。

Enter a stock code and get a **logic-closed-loop verification report**, not a traditional research note.

- **商业模式识别** — 这家公司赚钱的本质是什么？| What's the business model?
- **护城河评估** — 壁垒是在加强还是削弱？| Is the moat strengthening or weakening?
- **政策映射** — 有无国家级政策支撑？| Government policy support?
- **财务验证** — 数据是否支撑逻辑？| Do financials support the thesis?
- **闭环结论** — 赚钱逻辑是否成立 + 失效条件 | Conclusion + invalidation conditions

### 📡 市场雷达 | Market Radar

不是简单的新闻聚合，而是**从新闻/政策中推导投资逻辑链**。

Not a news aggregator, but **deriving investment logic chains from news/policy**.

- **大盘体温计** — 情绪指标（极度乐观/观望/恐慌）| Market sentiment
- **逻辑链推导** — 事件→产业影响→受益环节→具体标的 | Event → industry → targets
- **三梯队映射** — 直接受益 / 间接受益 / 主题受益 | Three-tier beneficiary mapping
- **持仓关联** — 自动交叉验证热点与你的持仓 | Cross-reference with your portfolio
- **每日推送** — 盘前08:30 / 盘后15:15 自动推送飞书 | Auto-push via Feishu

### 📈 K线决策 | Chart Decision

不是展示指标数值，而是**直接回答"现在该怎么操作"**。

Not displaying indicator values, but **directly answering "what should I do now"**.

- **量能形态** — 倍量 / 缩倍量 / 梯量 / 地量识别 | Volume pattern recognition
- **趋势判断** — 均线排列 + 多周期共振 | MA alignment + multi-timeframe
- **决策输出** — 持有/加仓/减仓/清仓 + 止盈止损位 + 盈亏比 | Action + levels + R:R ratio
- **逻辑回检** — 当初买入的逻辑是否还在？| Is the original thesis still valid?

### ⚡ 执行与风控 | Execution & Risk Control

- **飞书交互** — 自然语言指令（`查600519` / `看大盘` / `K线 300750`）| Feishu NL commands
- **条件预警** — 价格突破/跌破、倍量异动、MACD金叉等 | Conditional alerts
- **交易预留** — QMT/PTrade/通达信接口预留，HITL人工确认 | Trade gateway (reserved)
- **风控硬限** — 单股最大仓位、单日亏损上限、总回撤保护 | Hard risk limits

---

## 系统架构 | System Architecture

### 一个 Nanobot，四组 Skills | One Nanobot, Four Skill Groups

FinAgent 运行在**单个 Nanobot 实例**上。四个功能域不是四个独立进程，而是四组 Skill 集合，由同一个 Agent Loop 通过 SOUL.md 中的路由规则统一调度。

FinAgent runs on a **single Nanobot instance**. The four functional domains are four Skill groups, orchestrated by one Agent Loop via routing rules in SOUL.md.

```
┌─────────────────────────────────────────────────────┐
│              Nanobot Gateway (单实例)                 │
│              Nanobot Gateway (Single Instance)        │
├─────────────────────────────────────────────────────┤
│                                                       │
│  SOUL.md ── 角色定义 + 路由规则 + 输出规范              │
│              Role + Routing + Output Format            │
│                                                       │
│  ┌───────────┐ ┌───────────┐ ┌───────────┐ ┌────────┐│
│  │📊 逻辑分析 │ │📡 市场雷达 │ │📈 K线决策  │ │⚡ 执行  ││
│  │  Skills   │ │  Skills   │ │  Skills   │ │ Skills ││
│  └─────┬─────┘ └─────┬─────┘ └─────┬─────┘ └───┬────┘│
│        └──────────────┼──────────────┘           │     │
│                       ▼                          │     │
│              ┌────────────────┐                  │     │
│              │ Python 计算引擎 │                  │     │
│              │ pandas_ta/TA-Lib│                  │     │
│              └────────┬───────┘                  │     │
│                       ▼                          ▼     │
│  ┌──────────────────────────────────────────────────┐  │
│  │          统一数据层 Unified Data Layer             │  │
│  │  ┌─────┐ ┌────────┐ ┌──────┐ ┌─────┐ ┌──────┐  │  │
│  │  │ QMT │ │AKShare │ │PTrade│ │ TDX │ │ 美股 │  │  │
│  │  │ ✅  │ │  ✅    │ │ 预留 │ │ 预留 │ │ 预留 │  │  │
│  │  └─────┘ └────────┘ └──────┘ └─────┘ └──────┘  │  │
│  └──────────────────────────────────────────────────┘  │
│                                                       │
│  Channel: 飞书Bot    Cron: 定时任务    Memory: 持仓记忆  │
└─────────────────────────────────────────────────────┘
```

### 三层业务架构 | Three-Layer Business Architecture

| 层级 Layer | 职责 Responsibility | 关键组件 Key Components |
|-----------|--------------------|-----------------------|
| **L3 交互执行层** | 用户交互 + 交易执行 | 飞书Bot · Cron定时 · 交易网关(QMT/PTrade/TDX) |
| Interface & Execution | User interaction + Trade execution | Feishu Bot · Cron · Trade Gateway |
| **L2 智能推理层** | AI推理 + 指标计算 | Nanobot Agent Loop · LLM · Skills · pandas_ta |
| Intelligence & Reasoning | AI reasoning + Indicator calc | Nanobot Agent Loop · LLM · Skills · pandas_ta |
| **L1 统一数据层** | 数据获取 + 存储 | DataAdapter(QMT/AKShare/...) · SQLite · Memory |
| Unified Data | Data fetching + Storage | DataAdapter(QMT/AKShare/...) · SQLite · Memory |

### 数据适配器 | Data Adapter Pattern

所有行情数据源实现同一个抽象接口，新增市场只需实现子类：

All market data sources implement the same abstract interface. Adding a new market only requires implementing a subclass:

```python
class DataAdapter(ABC):
    """统一数据适配器接口 | Unified data adapter interface"""
    def get_kline(self, symbol, period, count) -> pd.DataFrame: ...
    def get_realtime_quote(self, symbol) -> dict: ...
    def get_financials(self, symbol) -> dict: ...
    def get_fund_flow(self, symbol) -> dict: ...
    def get_news(self, keywords, days) -> list: ...

class TradeAdapter(ABC):
    """统一交易接口 | Unified trade interface"""
    def place_order(self, symbol, side, qty, price, order_type): ...
    def cancel_order(self, order_id) -> bool: ...
    def get_positions(self) -> list: ...
    def get_account_info(self) -> dict: ...

# 一期实现 | Phase 1 Implementation
class QMTAdapter(DataAdapter): ...      # 迅投QMT (xtquant)
class AKShareAdapter(DataAdapter): ...  # AKShare (free)

# 预留 | Reserved
class PTradeAdapter(DataAdapter): ...   # 恒生PTrade
class TDXAdapter(DataAdapter): ...      # 通达信
class USStockAdapter(DataAdapter): ...  # 美股 (yfinance / IB)
class CryptoAdapter(DataAdapter): ...   # 加密货币 (CCXT)
```

---

## 快速开始 | Quick Start

### 前置条件 | Prerequisites

- Python 3.11+
- 一个 LLM API Key（推荐 DeepSeek / Qwen / OpenRouter）
- 飞书企业自建应用（用于Bot接入）

### 安装 | Installation

```bash
# 1. 克隆仓库 | Clone the repo
git clone https://github.com/yourname/finagent.git
cd finagent

# 2. 安装依赖 | Install dependencies
pip install -e .

# 3. 安装 Nanobot | Install Nanobot
pip install nanobot-ai

# 4. 初始化配置 | Initialize config
nanobot onboard
```

### 配置 | Configuration

编辑 `~/.nanobot/config.json`：

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

将 FinAgent 的 Skills 链接到 Nanobot workspace：

```bash
# 复制 Skills 和 SOUL.md 到 Nanobot workspace
cp -r finagent/skills/ ~/.nanobot/workspace/skills/
cp finagent/SOUL.md ~/.nanobot/workspace/SOUL.md
```

### 启动 | Launch

```bash
# 命令行模式（调试）| CLI mode (debug)
nanobot agent -m "查 600519"

# 启动网关（飞书Bot + 定时任务）| Start gateway (Feishu + Cron)
nanobot gateway
```

### 飞书指令 | Feishu Commands

| 指令 Command | 功能 Function | 示例 Example |
|-------------|--------------|-------------|
| `查 [代码]` | 个股逻辑分析 | `查 600519` |
| `看大盘` | 市场雷达 | `看大盘` |
| `K线 [代码]` | K线决策分析 | `K线 300750` |
| `K线 [代码] 周线` | 指定周期 | `K线 300750 周线` |
| `我的持仓` | 持仓一览 | `我的持仓` |
| `加持仓 [代码] [成本] [数量]` | 录入持仓 | `加持仓 600519 1750 100` |
| `设预警 [代码] [条件]` | 设置预警 | `设预警 600519 跌破1700` |
| `今日热点` | 热点逻辑链 | `今日热点` |

---

## 技能清单 | Skill List

### P0 — MVP（一期 Phase 1）

| 技能 Skill | 组 Group | 功能 Function |
|-----------|---------|--------------|
| `skill-biz-model` | 📊 逻辑分析 | 商业模式 + 闭环验证 / Business model + loop verification |
| `skill-financial` | 📊 逻辑分析 | 财务健康度（营收/ROE/负债率）/ Financial health check |
| `skill-valuation` | 📊 逻辑分析 | PE/PB 历史分位 / Valuation percentile |
| `skill-index-pulse` | 📡 市场雷达 | 大盘数据 + 情绪判断 / Index + sentiment |
| `skill-news-logic` | 📡 市场雷达 | 新闻 → 逻辑链 → 标的 / News → logic chain → targets |
| `skill-trend` | 📈 K线决策 | 均线排列 + 趋势 / MA alignment + trend |
| `skill-volume` | 📈 K线决策 | 量能形态（倍量/缩倍量/梯量/地量）/ Volume patterns |
| `skill-decision` | 📈 K线决策 | 操作建议 + 盈亏比 / Action + risk-reward ratio |
| `skill-feishu` | ⚡ 执行 | 飞书消息收发 / Feishu messaging |
| `skill-position` | ⚡ 执行 | 持仓管理 / Position management |
| `skill-alert` | ⚡ 执行 | 条件预警 / Conditional alerts |

### P1 — 二期增强 Phase 2

| 技能 Skill | 功能 Function |
|-----------|--------------|
| `skill-policy` | 政策扫描 + 受益映射 / Policy scan + beneficiary mapping |
| `skill-team` | 管理层 + 股东分析 / Management + shareholder analysis |
| `skill-moat` | 护城河深度分析 / Deep moat analysis |
| `skill-sector-flow` | 板块轮动 + 资金流 / Sector rotation + fund flow |
| `skill-portfolio-link` | 热点与持仓交叉 / Hot topics × portfolio cross-ref |
| `skill-signal` | MACD/KDJ/BOLL 综合 / Technical signal synthesis |
| `skill-risk-check` | 风控规则引擎 / Risk control engine |
| `skill-trade-gateway` | QMT 实盘交易 / QMT live trading |

### P2 — 长期扩展 Future

| 技能 Skill | 功能 Function |
|-----------|--------------|
| `skill-backtest` | 策略回测 / Strategy backtesting |
| `skill-sentiment` | 社区舆情 / Community sentiment |
| `skill-replay` | 交易复盘 / Trade review reports |
| `skill-us-stock` | 美股适配 / US stock adapter |
| `skill-hk-stock` | 港股适配 / HK stock adapter |
| `skill-crypto` | 加密货币适配 / Crypto adapter |
| `skill-ptrade` | PTrade 适配 / PTrade adapter |
| `skill-tdx` | 通达信适配 / TDX adapter |

---

## 项目结构 | Project Structure

```
finagent/
├── README.md                    # 本文件 | This file
├── README_EN.md                 # English version
├── LICENSE                      # MIT License
├── pyproject.toml               # Python 项目配置
├── CONTRIBUTING.md              # 贡献指南 | Contributing guide
├── SOUL.md                      # Nanobot 人格定义 | Agent personality
│
├── finagent/                  # 主代码 | Main source
│   ├── __init__.py
│   │
│   ├── adapters/                # 数据适配器 | Data adapters
│   │   ├── base.py              # 抽象接口 | Abstract interface
│   │   ├── qmt_adapter.py       # 迅投QMT
│   │   ├── akshare_adapter.py   # AKShare
│   │   ├── ptrade_adapter.py    # PTrade (预留 reserved)
│   │   └── tdx_adapter.py       # 通达信 (预留 reserved)
│   │
│   ├── skills/                  # 技能模块 | Skill modules
│   │   ├── logic/               # 📊 逻辑分析组
│   │   │   ├── biz_model.py     # 商业模式分析
│   │   │   ├── financial.py     # 财务健康度
│   │   │   └── valuation.py     # 估值分位
│   │   │
│   │   ├── radar/               # 📡 市场雷达组
│   │   │   ├── index_pulse.py   # 大盘体温计
│   │   │   └── news_logic.py    # 新闻逻辑链
│   │   │
│   │   ├── chart/               # 📈 K线决策组
│   │   │   ├── trend.py         # 趋势判断
│   │   │   ├── volume.py        # 量能形态
│   │   │   └── decision.py      # 综合决策
│   │   │
│   │   └── exec/                # ⚡ 执行风控组
│   │       ├── feishu.py        # 飞书交互
│   │       ├── position.py      # 持仓管理
│   │       ├── alert.py         # 条件预警
│   │       ├── risk_check.py    # 风控规则
│   │       └── trade_gateway.py # 交易网关 (预留)
│   │
│   ├── engine/                  # 计算引擎 | Calculation engine
│   │   ├── indicators.py        # 技术指标封装
│   │   ├── volume_patterns.py   # 量能形态算法
│   │   └── key_levels.py        # 支撑压力位
│   │
│   ├── db/                      # 数据存储 | Data storage
│   │   ├── models.py            # SQLite 数据模型
│   │   └── database.py          # 数据库操作
│   │
│   └── templates/               # 输出模板 | Output templates
│       ├── logic_report.md      # 逻辑分析报告模板
│       ├── market_brief.md      # 市场简报模板
│       └── chart_decision.md    # K线决策模板
│
├── config/                      # 配置文件 | Config files
│   ├── config.example.json      # Nanobot 配置示例
│   └── cron.example.json        # 定时任务示例
│
├── docs/                        # 文档 | Documentation
│   ├── architecture.md          # 架构详解
│   ├── skill-development.md     # Skill 开发指南
│   ├── data-adapters.md         # 数据适配器文档
│   ├── feishu-setup.md          # 飞书配置教程
│   ├── qmt-setup.md             # QMT 配置教程
│   └── assets/                  # 图片资源
│
└── tests/                       # 测试 | Tests
    ├── test_adapters/
    ├── test_skills/
    └── test_engine/
```

---

## 设计哲学 | Design Philosophy

### 逻辑闭环的五条铁律 | Five Iron Rules of Logic Closed-Loop

1. **可追溯** — 用户问"为什么推荐这个"，系统能给出 3 层以内推理  
   **Traceable** — The system can explain any recommendation within 3 reasoning layers

2. **可证伪** — 每个结论必须附带"逻辑失效条件"  
   **Falsifiable** — Every conclusion must include invalidation conditions

3. **不黑盒** — 不依赖不可解释的模型，优先用公开可理解的逻辑  
   **No black box** — Prefer explainable logic over opaque models

4. **中线定位** — 日线为主，周线确认，不做日内噪音  
   **Swing focus** — Daily chart primary, weekly confirmation, no intraday noise

5. **风险优先** — 先问"会亏多少"，再问"能赚多少"  
   **Risk first** — Ask "how much can I lose" before "how much can I gain"

### 逻辑链输出模板 | Logic Chain Output Template

参考实际运行效果（节选）：

```
📰 新闻核心要点：
  1. 国产大模型调用量连续一个月超过海外模型
  2. OpenClaw 是本轮 Token 消耗增长的核心驱动因素
  3. 模型厂商和云计算厂商先后宣布涨价

🧠 投资逻辑推导：
  OpenClaw需求 → Token消耗爆发（单任务100~1000倍）
    → 算力产能不足 → 算力涨价
      → 上游算力/电力/存储需求暴增

📊 受益板块分析：
  🔴 第一梯队（直接受益）
    ┌────────┬──────────────────┬──────────────┐
    │ 板块    │ 逻辑              │ A股标的       │
    ├────────┼──────────────────┼──────────────┤
    │ 算计算  │ 涨价周期开启       │ 中际旭创      │
    │ AI算力  │ Token需求暴增      │ 中科电气      │
    │ 光模块  │ 数据中心互联需求    │ 中马传动      │
    └────────┴──────────────────┴──────────────┘

  🟡 第二梯队（间接受益）  ...
  🔵 第三梯队（主题受益）  ...

🔗 与你持仓的关联：
  ┌──────────────┬──────────┬────────────────┐
  │ 持仓股        │ 关联度    │ 建议            │
  ├──────────────┼──────────┼────────────────┤
  │ 中国核电      │ 🔴 直接  │ 数据中心用电逻辑 │
  │ 奥瑞德       │ ⚪ 无关  │ 按计划操作       │
  └──────────────┴──────────┴────────────────┘

⚠️ 逻辑失效条件：
  1. 若涨价幅度不及预期（<5%），上游受益逻辑减弱
  2. 若 4月18日 调价未落地，短期情绪回落
```

---

## 技术栈 | Tech Stack

| 组件 Component | 选型 Choice | 说明 Note |
|---------------|------------|----------|
| Agent 框架 | [Nanobot](https://github.com/HKUDS/nanobot) | ~4000行Python，轻量级 OpenClaw 替代 |
| LLM | DeepSeek-V3 (主) / Qwen (备) | 中文理解强，API成本低 |
| 行情数据 | QMT (xtquant) + AKShare | QMT实时行情，AKShare免费补充 |
| 技术指标 | pandas_ta / TA-Lib | MA/MACD/KDJ/BOLL/量能计算 |
| 本地存储 | SQLite | 持仓、交易日志、预警配置，零配置 |
| 消息交互 | 飞书开放平台 | Bot接入，交互卡片，WebSocket长连接 |
| 交易接口 | QMT miniQMT (预留) | xtquant Python API |
| 部署 | Docker / systemd | 一键启动 |

---

## 路线图 | Roadmap

| 阶段 Phase | 目标 Goal | 周期 Duration |
|-----------|----------|--------------|
| **M0** | 🔧 环境搭建：Nanobot + 飞书 + AKShare 跑通 | 1 周 |
| | Setup: Nanobot + Feishu + AKShare integration | |
| **M1** | 📈 K线决策组上线（最易验证的模块） | 1 周 |
| | Chart Decision skills (easiest to validate) | |
| **M2** | 📊 逻辑分析组上线（核心差异化能力） | 2 周 |
| | Logic Analysis skills (core differentiator) | |
| **M3** | 📡 市场雷达组上线 + Cron推送 | 2 周 |
| | Market Radar skills + Cron auto-push | |
| **M4** | ⚡ 执行风控组 + 预警 + 交易模拟 | 1 周 |
| | Execution & Risk + Alerts + Trade simulation | |
| **M5** | 🧪 集成测试 + 文档 + 开源发布 | 1 周 |
| | Integration test + Docs + Open-source release | |

**总计约 8 周到达可用 MVP | ~8 weeks to usable MVP**

---

## 贡献指南 | Contributing

我们欢迎所有形式的贡献！| We welcome all forms of contribution!

### 如何贡献一个新 Skill | How to Contribute a Skill

1. Fork 本仓库
2. 在 `finagent/skills/` 对应目录下创建新文件
3. 实现 Skill 函数（遵循 [Skill 开发规范](docs/skill-development.md)）
4. 编写测试
5. 提交 Pull Request

```python
# Skill 模板 | Skill Template
from nanobot.agent.tools import tool

@tool
async def skill_example(symbol: str) -> str:
    """
    Skill 描述 | Skill description
    
    Args:
        symbol: 股票代码 | Stock symbol (e.g., "600519")
    Returns:
        分析结果 | Analysis result
    """
    # 1. 获取数据 | Fetch data
    # 2. 计算/推理 | Calculate/Reason
    # 3. 返回结果（必须包含 rationale + invalidation）
    #    Return (must include rationale + invalidation)
    return result
```

### 贡献方向 | Contribution Areas

- 🔌 **数据适配器** — PTrade / 通达信 / 美股 / 港股 / 加密货币
- 🧠 **分析 Skills** — 更多分析维度（行业对比、股东变动等）
- 🌐 **国际化** — 英文文档完善、多语言界面
- 📱 **Channel** — 微信 / Telegram / Discord 接入
- 🧪 **测试** — 单元测试、回测验证
- 📖 **文档** — 使用教程、视频教程

---

## 风险声明 | Disclaimer

> ⚠️ **FinAgent 仅供学习和研究使用，不构成任何投资建议。**
>
> ⚠️ **FinAgent is for educational and research purposes only. It does NOT constitute investment advice.**

- AI 分析存在"幻觉"风险，所有结论需人工验证
- 历史回测表现不代表未来收益
- 自动交易存在技术故障风险（网络中断、API异常、滑点等）
- 用户应始终对自己的投资决策负完全责任
- 股市有风险，入市需谨慎

- AI analysis carries "hallucination" risks; all conclusions require human verification
- Past backtest performance does not guarantee future returns
- Automated trading carries technical failure risks
- Users are fully responsible for their own investment decisions
- Investing involves risk; trade with caution

---

## 致谢 | Acknowledgments

- [Nanobot](https://github.com/HKUDS/nanobot) — 香港大学 HKUDS 实验室的轻量级 AI Agent 框架
- [OpenClaw](https://github.com/openclaw) — Skill 模块化设计思想的灵感来源
- [AKShare](https://github.com/akfamily/akshare) — 优秀的开源 A 股数据接口
- [迅投QMT](https://www.thinktrader.net/) — 量化交易接口
- [pandas_ta](https://github.com/twopirllc/pandas-ta) — 技术指标计算库

---

## 开源协议 | License

[MIT License](LICENSE) — 自由使用、修改和分发。

---

<p align="center">
  <strong>如果觉得有用，请给个 ⭐ Star！| If useful, give us a ⭐ Star!</strong>
</p>
