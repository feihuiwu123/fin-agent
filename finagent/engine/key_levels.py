"""支撑压力位计算 | Support & Resistance Level Calculation"""

import pandas as pd


def calc_key_levels(df: pd.DataFrame, lookback: int = 60) -> dict:
    """
    计算关键支撑和压力位 | Calculate key support and resistance levels

    Returns:
        {
            "support": [支撑位列表],
            "resistance": [压力位列表],
            "pivot": 枢轴点,
        }
    """
    recent = df.tail(lookback).copy()
    high = recent["high"].astype(float)
    low = recent["low"].astype(float)
    close = recent["close"].astype(float)

    pivot = (high.iloc[-1] + low.iloc[-1] + close.iloc[-1]) / 3

    support_levels = sorted(low.nsmallest(3).tolist())
    resistance_levels = sorted(high.nlargest(3).tolist())

    return {
        "support": support_levels,
        "resistance": resistance_levels,
        "pivot": round(pivot, 2),
    }


def calc_pivot_points(df: pd.DataFrame) -> dict:
    """
    计算标准枢轴点 | Calculate standard pivot points (daily)

    Returns:
        {
            "pivot": 枢轴点,
            "r1": 第一压力位,
            "r2": 第二压力位,
            "r3": 第三压力位,
            "s1": 第一支撑位,
            "s2": 第二支撑位,
            "s3": 第三支撑位,
        }
    """
    last = df.iloc[-1]
    high = float(last["high"])
    low = float(last["low"])
    close = float(last["close"])

    pivot = (high + low + close) / 3
    r1 = 2 * pivot - low
    r2 = pivot + (high - low)
    r3 = high + 2 * (pivot - low)
    s1 = 2 * pivot - high
    s2 = pivot - (high - low)
    s3 = low - 2 * (high - pivot)

    return {
        "pivot": round(pivot, 2),
        "r1": round(r1, 2),
        "r2": round(r2, 2),
        "r3": round(r3, 2),
        "s1": round(s1, 2),
        "s2": round(s2, 2),
        "s3": round(s3, 2),
    }
