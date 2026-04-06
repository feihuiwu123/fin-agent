"""技术指标计算引擎 | Technical Indicator Calculation Engine"""

import pandas as pd
import numpy as np


def calc_ma(df: pd.DataFrame, windows: list[int] = [5, 10, 20, 60, 120, 250]) -> pd.DataFrame:
    """计算多条均线 | Calculate multiple moving averages"""
    result = df.copy()
    for w in windows:
        result[f"MA{w}"] = result["close"].rolling(window=w).mean()
    return result


def calc_macd(df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
    """计算 MACD | Calculate MACD"""
    result = df.copy()
    ema_fast = result["close"].ewm(span=fast, adjust=False).mean()
    ema_slow = result["close"].ewm(span=slow, adjust=False).mean()
    result["DIF"] = ema_fast - ema_slow
    result["DEA"] = result["DIF"].ewm(span=signal, adjust=False).mean()
    result["MACD"] = (result["DIF"] - result["DEA"]) * 2
    return result


def calc_kdj(df: pd.DataFrame, period: int = 9, smooth: int = 3) -> pd.DataFrame:
    """计算 KDJ 指标 | Calculate KDJ indicator"""
    result = df.copy()
    low_min = result["low"].rolling(window=period).min()
    high_max = result["high"].rolling(window=period).max()
    rsv = (result["close"] - low_min) / (high_max - low_min) * 100
    rsv = rsv.fillna(50)

    k = pd.Series(50.0, index=result.index)
    d = pd.Series(50.0, index=result.index)
    for i in range(1, len(result)):
        k.iloc[i] = k.iloc[i - 1] * (smooth - 1) / smooth + rsv.iloc[i] / smooth
        d.iloc[i] = d.iloc[i - 1] * (smooth - 1) / smooth + k.iloc[i] / smooth
    j = 3 * k - 2 * d

    result["K"] = k
    result["D"] = d
    result["J"] = j
    return result


def calc_boll(df: pd.DataFrame, period: int = 20, std_dev: float = 2.0) -> pd.DataFrame:
    """计算布林带 | Calculate Bollinger Bands"""
    result = df.copy()
    result["BOLL_MID"] = result["close"].rolling(window=period).mean()
    std = result["close"].rolling(window=period).std()
    result["BOLL_UP"] = result["BOLL_MID"] + std_dev * std
    result["BOLL_DN"] = result["BOLL_MID"] - std_dev * std
    return result


def calc_rsi(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
    """计算 RSI | Calculate RSI"""
    result = df.copy()
    delta = result["close"].diff()
    gain = delta.where(delta > 0, 0.0)
    loss = (-delta).where(delta < 0, 0.0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss.replace(0, np.inf)
    result["RSI"] = 100 - (100 / (1 + rs))
    return result


def calc_all_indicators(df: pd.DataFrame) -> pd.DataFrame:
    """计算所有技术指标 | Calculate all technical indicators"""
    df = calc_ma(df)
    df = calc_macd(df)
    df = calc_kdj(df)
    df = calc_boll(df)
    df = calc_rsi(df)
    return df
