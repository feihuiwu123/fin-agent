#!/usr/bin/env python3
"""Comprehensive stock analysis: quote, financials, industry peers, fund flow, analyst ratings."""
import sys
import json
import akshare as ak

code = sys.argv[1] if len(sys.argv) > 1 else "002202"
warnings = __import__("warnings"); warnings.filterwarnings("ignore")

# ===== 1. Basic Quote =====
try:
    df = ak.stock_zh_a_spot_em()
    if df is not None and not df.empty:
        row = df[df["代码"] == code]
        if not row.empty:
            r = row.iloc[0]
            info = {
                "name": r.get("名称", ""),
                "price": r.get("最新价", 0),
                "pct": r.get("涨跌幅", 0),
                "high": r.get("最高", 0),
                "low": r.get("最低", 0),
                "open": r.get("今开", 0),
                "prev": r.get("昨收", 0),
                "volume": r.get("成交量", 0),
                "amount": r.get("成交额", 0),
                "turnover": r.get("换手率", 0),
                "pe": r.get("市盈率-动态", 0),
                "pb": r.get("市净率", 0),
                "total_mv": r.get("总市值", 0),
                "circ_mv": r.get("流通市值", 0),
                "amplitude": r.get("振幅", 0),
                "volume_ratio": r.get("量比", 0),
            }
            print(f"QUOTE:{json.dumps(info, ensure_ascii=False)}")
except Exception as e:
    print(f"QUOTE_ERROR:{e}")

# ===== 2. K-line (10 days) =====
try:
    df = ak.stock_zh_a_hist(symbol=code, period="daily", adjust="qfq")
    if df is not None and not df.empty:
        klines = []
        for _, r in df.tail(10).iterrows():
            klines.append({
                "date": str(r.get("日期", ""))[:10],
                "open": r.get("开盘", 0),
                "high": r.get("最高", 0),
                "low": r.get("最低", 0),
                "close": r.get("收盘", 0),
                "pct": r.get("涨跌幅", 0),
                "amount": r.get("成交额", 0),
            })
        print(f"KLINE:{json.dumps(klines, ensure_ascii=False)}")
    else:
        print("KLINE:[]")
except Exception as e:
    print(f"KLINE_ERROR:{e}")

# ===== 3. Fund Flow (recent 5 days) =====
try:
    df = ak.stock_individual_fund_flow(stock=code, market="sz" if code.startswith(("00", "30")) else "sh")
    if df is not None and not df.empty:
        flows = []
        for _, r in df.tail(5).iterrows():
            flows.append({
                "date": str(r.get("日期", ""))[:10],
                "close": r.get("收盘价", 0),
                "pct": r.get("涨跌幅", 0),
                "main_inflow": r.get("主力净流入-净额", 0),
                "main_inflow_pct": r.get("主力净流入-净占比", 0),
                "super_large": r.get("超大单净流入-净额", 0),
                "small_outflow": r.get("小单净流入-净额", 0),
            })
        print(f"FUND_FLOW:{json.dumps(flows, ensure_ascii=False)}")
    else:
        print("FUND_FLOW:[]")
except Exception as e:
    print(f"FUND_FLOW_ERROR:{e}")

# ===== 4. Financial Summary =====
try:
    df = ak.stock_financial_abstract_ths(symbol=code)
    if df is not None and not df.empty and not df.empty:
        latest = df.tail(1)
        if not latest.empty:
            r = latest.iloc[0]
            fin = {
                "period": r.get("报告期", ""),
                "revenue": f"{r.get('营业总收入', 0):.2f}亿" if isinstance(r.get("营业总收入", 0), (int, float)) else r.get("营业总收入", ""),
                "revenue_yoy": r.get("营业总收入同比增长率", ""),
                "net_profit": f"{r.get('净利润', 0):.2f}亿" if isinstance(r.get("净利润", 0), (int, float)) else r.get("净利润", ""),
                "net_profit_yoy": r.get("净利润同比增长率", ""),
                "gross_margin": r.get("销售毛利率", ""),
                "net_margin": r.get("销售净利率", ""),
                "roe": r.get("净资产收益率", ""),
                "debt_ratio": r.get("资产负债率", ""),
                "eps": r.get("基本每股收益", ""),
            }
            print(f"FINANCIAL:{json.dumps(fin, ensure_ascii=False)}")
    else:
        print("FINANCIAL:{}")
except Exception as e:
    print(f"FINANCIAL_ERROR:{e}")

# ===== 5. Industry Board Peers =====
try:
    df_info = ak.stock_individual_info_em(symbol=code)
    industry = ""
    if not df_info.empty:
        row = df_info[df_info["item"] == "行业"]
        if not row.empty:
            industry = str(row.iloc[0]["value"])

    if not industry:
        print("INDUSTRY:unknown")
    else:
        # Get industry board constituents
        df_board = ak.stock_board_industry_cons_em(symbol=industry)
        if df_board is not None and not df_board.empty:
            peers = []
            for _, r in df_board.iterrows():
                if str(r.get("代码", "")) == code:
                    continue
                peers.append({
                    "code": r.get("代码", ""),
                    "name": r.get("名称", ""),
                    "price": r.get("最新价", 0),
                    "pct": r.get("涨跌幅", 0),
                    "pe": r.get("市盈率-动态", 0),
                    "pb": r.get("市净率", 0),
                    "turnover": r.get("换手率", 0),
                    "amount": r.get("成交额", 0),
                })
            print(f"INDUSTRY:{industry}")
            print(f"PEERS:{json.dumps(peers, ensure_ascii=False)}")
        else:
            print(f"INDUSTRY:{industry}")
            print("PEERS:[]")
except Exception as e:
    print(f"INDUSTRY_ERROR:{e}")
    print("PEERS:[]")

# ===== 6. Analyst Sentiment =====
try:
    df = ak.stock_comment_em()
    if df is not None and not df.empty:
        match = df[df["代码"] == code]
        if not match.empty:
            r = match.iloc[0]
            sentiment = {
                "comment_score": r.get("综合得分", 0),
                "institution_participation": r.get("机构参与度", 0),
                "attention_index": r.get("关注指数", 0),
                "pe": r.get("市盈率", 0),
                "main_cost": r.get("主力成本", 0),
                "rank": r.get("目前排名", 0),
                "rising": r.get("上升", 0),
            }
            print(f"SENTIMENT:{json.dumps(sentiment, ensure_ascii=False)}")
        else:
            print("SENTIMENT:{}")
    else:
        print("SENTIMENT:{}")
except Exception as e:
    print(f"SENTIMENT_ERROR:{e}")

# ===== 7. Concept Boards =====
try:
    df_concept = ak.stock_board_concept_name_em()
    if df_concept is not None and not df_concept.empty:
        # Get top concept by name matching
        concepts = []
        # Try to find related concepts - look at top performing ones
        for _, r in df_concept.head(20).iterrows():
            concepts.append({
                "name": r.get("板块名称", ""),
                "pct": r.get("涨跌幅", 0),
                "total_mv": r.get("总市值", 0),
                "turnover": r.get("换手率", 0),
            })
        if concepts:
            print(f"TOP_CONCEPTS:{json.dumps(concepts, ensure_ascii=False)}")
except Exception as e:
    print(f"CONCEPTS_ERROR:{e}")

# ===== 8. Market Breadth =====
try:
    df = ak.stock_zh_a_spot_em()
    if df is not None and not df.empty:
        total = len(df)
        up = len(df[df["涨跌幅"] > 0])
        down = len(df[df["涨跌幅"] < 0])
        flat = total - up - down
        limit_up = len(df[df["涨跌幅"] >= 9.9]) if "涨跌幅" in df.columns else 0
        limit_down = len(df[df["涨跌幅"] <= -9.9]) if "涨跌幅" in df.columns else 0
        total_amt = df["成交额"].sum()
        print(f"BREADTH:涨:{up} 跌:{down} 平:{flat} 涨停:{limit_up} 跌停:{limit_down} 总额:{total_amt/1e12:.2f}万亿")
except Exception as e:
    print(f"BREADTH_ERROR:{e}")
