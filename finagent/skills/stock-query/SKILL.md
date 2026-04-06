---
name: stock-query
description: Query A-share stock real-time quotes, financials, K-line data. Use for queries like "查 600519", stock codes, or company names.
---

# Stock Query — A-Share Stock Lookup

Use this skill when the user asks about a specific stock by code (e.g. "600519", "查 600519") or company name.

**IMPORTANT**: Always use the venv python at `/home/finagent/fin-agent/.venv/bin/python3` to run these scripts. Never use `python3` directly.

## Step 1: Run comprehensive analysis

```bash
/home/finagent/fin-agent/.venv/bin/python3 /home/finagent/fin-agent/finagent/skills/scripts/query_stock_analysis.py 600519
```

Parse all lines starting with `QUOTE:`, `KLINE:`, `FUND_FLOW:`, `FINANCIAL:`, `INDUSTRY:`, `PEERS:`, `SENTIMENT:`, `TOP_CONCEPTS:`, `BREADTH:`.

## Step 2: Industry board context

If the INDUSTRY value is known (e.g. "风电设备"), fetch the industry board constituents:

```bash
/home/finagent/fin-agent/.venv/bin/python3 -c "
import akshare as ak, json, warnings; warnings.filterwarnings('ignore')
df = ak.stock_board_industry_cons_em(symbol='风电设备')
print(json.dumps(df.to_dict(orient='records'), ensure_ascii=False))
"
```

Replace "风电设备" with the actual industry name.

## Star Rating System — 10 Core Dimensions

Quantify all metrics. Use 1-5 stars (★★★★★). Fill in each dimension based on parsed data and your knowledge:

| Dimension | ★★★★★ | ★★★★ | ★★★ | ★★ | ★ |
|-----------|-------|------|-----|----|---|
| PE估值 | PE低于同行均值30%+ | PE低于同行10-30% | PE接近同行均值 | PE高于同行10-30% | PE高于同行30%+ |
| PB估值 | PB<1(破净) | PB低于同行30% | PB接近同行 | PB高于同行30% | PB高于同行50%+ |
| 成长速度 | 营收YoY>30% 净利YoY>50% | 营收YoY>20% 净利YoY>30% | 营收YoY>10% | 营收YoY>0% | 营收/净利同比均为负 |
| 盈利能力 | 毛利率>50% ROE>20% | 毛利>30% ROE>15% | 毛利>20% ROE>10% | 毛利>10% ROE>5% | 毛利<10% 或亏损 |
| 财务健康 | 负债率<30% 经营现金为正 | 负债率<50% 经营现金为正 | 负债率<60% | 负债率<75% | 负债率>75% 或经营现金大幅为负 |
| 资金流向 | 近5日主力净流入占比>5% | 近5日主力净流入占比>2% | 主力流入流出均衡 | 主力净流出占比>2% | 主力净流出占比>5% |
| 市场热度 | 综合得分>70 排名前500 | 排名500-1500 | 排名1500-3000 | 排名3000-4000 | 排名4000+ 关注指数低 |
| 波动风险 | 近10日振幅<3% | 振幅3-5% | 振幅5-8% | 振幅8-12% | 振幅>12% |
| 技术壁垒 | 专利/技术护城河极深 不可替代 | 技术领先 追赶需3-5年 | 技术成熟 有一定优势 | 技术同质化 靠规模/渠道 | 纯加工无技术壁垒 |
| 行业空间 | 行业规模万亿+ YoY增速>20% | 规模万亿+ 增速10-20% | 规模5000亿+ 增速5-10% | 规模3000亿 增速<5% | 行业萎缩或天花板明确 |

**Additional dimensions (apply as relevant):**

| Dimension | ★★★★★ | ★★★★ | ★★★ | ★★ | ★ |
|-----------|-------|------|-----|----|---|
| 政策支撑 | 国家级战略+专项补贴 | 国家政策明确支持 | 行业规范/准入限制少 | 政策中性或边际管控 | 政策打压/限制性政策 |
| 题材催化 | 3+个热门概念且当日涨停/领涨 | 2-3个概念跟涨 | 1-2个概念相关 | 题材已过热度期 | 无热点概念或利空 |
| 客户集中度 | 前五大客户占比<20% 分散 | <40% 分散合理 | 40-60% 适中 | >60% 集中度高 | 单一客户依赖>50% |
| 同业排位 | PE/PB排名行业前20% | 排名20-40% | 排名40-60% | 排名60-80% | 排名80-100% 最贵 |
| 国际环境 | 海外市场收入占比>50%+无贸易壁垒/汇率利好 | 海外收入30-50%/无重大制裁风险/汇率稳定 | 海外收入10-30%/存在关税摩擦但可控 | 海外收入<10%但核心部件依赖进口/汇率波动影响成本 | 海外市场受制裁/核心原材料被卡脖子/地缘冲突直接冲击 |

**国际环境适用条件：**
- ★★★★★: 出海顺利且受益于一带一路/RCEP，无制裁风险
- ★★★★: 海外业务稳健，主要贸易关系良好，汇率中性
- ★★★: 有少量关税/汇率波动，但可通过定价转移
- ★★: 关键原材料/芯片受海外垄断或出口管制
- ★: 被制裁/禁运/关税大幅上调，海外业务直接受损

判断依据: 海外收入占比(财报中查询)、是否受贸易关税影响、是否依赖海外核心零部件/芯片/原材料

## Response Format

All content must be data-driven tables. NO filler sentences, NO empty analysis. Every rating must cite the actual number that justifies it.

```
📊 个股深度 | 000001 股票名 | 2026-04-06
─── 行情 ───
| 现价 | 涨跌幅 | 成交额 | 换手率 | PE | PB | 振幅 | 量比 | 总市值 | 流通市值 |
| XX.XX | +X.XX% | XX.XX亿 | X.XX% | XX.X | X.XX | X.XX% | X.XX | XXXX亿 | XXXX亿 |

─── K线(近10日) ───
| 日期 | 收盘 | 涨跌幅 | 振幅 | 成交额 |
| 2026-04-06 | XX.XX | +X.XX% | X.XX% | XX.X亿 |
(10 rows)

─── 资金流(近5日) ───
| 日期 | 收盘 | 主力净流入 | 主力占比 | 超大单 | 小单净流入 |
| 2026-04-06 | XX.XX | +XX万 | +X.X% | XX万 | XX万 |
(5 rows)

─── 同业对比 ───
| 公司 | PE | PB | 换手率 | 涨跌幅 | 成交额 | 总市值 |
|------|----|----|--------|--------|--------|--------|
| 股票名(本股) | XX | X.XX | X.XX% | +X.XX% | XX亿 | XXXX亿 |
| 同行A | | | | | | |
| 同行B | | | | | | |
| 同行C | | | | | | |
(排序:按PE从低到高, 同行数据从INDUSTRY board获取)

─── 财务摘要 ───
| 报告期 | 营收 | 营收YoY | 净利润 | 净利YoY | 毛利率 | ROE | 负债率 | 每股经营现金流 |
| 2025年报 | XXX亿 | +XX% | XX亿 | +XX% | XX% | X% | XX% | X.XX |
| 2025三季报 | | | | | | | | |

─── 维度评估 ───
| 维度 | 评级 | 依据数据 | 行业均值 | 百分位 |
|------|------|---------|---------|--------|
| PE估值 | ★★★★☆ | PE=XX | 行业PE=XX | 低于均值X%,优于X%同行 |
| PB估值 | ★★★☆☆ | PB=X.XX | 行业PB=X.XX | X%分位 |
| 成长速度 | ★★★★☆ | 净利YoY+XX% | 行业净利YoY=XX% | — |
| 盈利能力 | ★★★☆☆ | 毛利XX% ROE=X% | 毛利=XX% | — |
| 财务健康 | ★★★★☆ | 负债率XX% 经营现金X.XX | 负债率=XX% | — |
| 资金流向 | ★★☆☆☆ | 5日主力净流出占比-X% | — | — |
| 市场热度 | ★★★☆☆ | 排名XXXX 关注XX | — | — |
| 波动风险 | ★★☆☆☆ | 振幅X% | 行业振幅=X% | — |
| 技术壁垒 | ★★★★☆ | [用数据说明:专利数/研发投入占比/技术代差] | — | — |
| 行业空间 | ★★★★☆ | [行业规模XXX亿 增速X%] | — | — |
| 政策支撑 | ★★★★★ | [具体政策名称/文件号/补贴金额] | — | — |
| 题材催化 | ★★★☆☆ | [概念名/是否涨停/领涨排名] | — | — |
| 客户集中度 | ★★★☆☆ | [前五大客户占比XX%] | — | — |
| 同业排位 | ★★★☆☆ | PE排名X/XX PB排名X/XX | — | — |

⚠️ 数据为实时快照盘中可能快速变化。本分析仅供学习研究不构成投资建议。
```
