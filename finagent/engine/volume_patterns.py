"""量能形态算法 | Volume Pattern Recognition Algorithms"""

import pandas as pd


def classify_volume_pattern(df: pd.DataFrame, lookback: int = 5) -> list[str]:
    """
    识别每日量能形态 | Classify daily volume patterns

    形态分类:
    - 倍量: 当日成交量 >= 前5日均量的2倍
    - 缩倍量: 当日成交量 <= 前5日均量的1/2
    - 梯量: 连续3日成交量递增
    - 地量: 当日成交量为近60日最低
    - 平量: 当日成交量在前5日均量的 0.8~1.2 倍之间
    """
    patterns = []
    volume = df["volume"].astype(float)
    ma_vol = volume.rolling(window=lookback).mean()

    for i in range(len(df)):
        if i < lookback:
            patterns.append("数据不足")
            continue

        vol = volume.iloc[i]
        avg = ma_vol.iloc[i]
        prev_vols = volume.iloc[max(0, i - 3) : i].tolist()

        if vol >= avg * 2:
            patterns.append("倍量")
        elif vol <= avg * 0.5:
            patterns.append("缩倍量")
        elif len(prev_vols) >= 3 and all(
            prev_vols[j] < prev_vols[j + 1] for j in range(len(prev_vols) - 1)
        ):
            patterns.append("梯量")
        elif i >= 60 and vol == volume.iloc[i - 60 : i + 1].min():
            patterns.append("地量")
        elif avg > 0 and 0.8 <= vol / avg <= 1.2:
            patterns.append("平量")
        else:
            patterns.append("常态")

    return patterns


def add_volume_patterns(df: pd.DataFrame) -> pd.DataFrame:
    """将量能形态标注到 DataFrame | Annotate volume patterns on DataFrame"""
    result = df.copy()
    result["volume_pattern"] = classify_volume_pattern(result)
    return result
