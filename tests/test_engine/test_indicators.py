"""Tests for calculation engine"""

import pandas as pd
import numpy as np

from finagent.engine.indicators import (
    calc_ma,
    calc_macd,
    calc_kdj,
    calc_boll,
    calc_rsi,
    calc_all_indicators,
)
from finagent.engine.volume_patterns import classify_volume_pattern, add_volume_patterns
from finagent.engine.key_levels import calc_key_levels, calc_pivot_points


def _make_sample_df(rows: int = 100) -> pd.DataFrame:
    np.random.seed(42)
    base = 100
    data = []
    for i in range(rows):
        base += np.random.normal(0, 1)
        data.append(
            {
                "date": pd.Timestamp("2024-01-01") + pd.Timedelta(days=i),
                "open": base + np.random.normal(0, 0.5),
                "high": base + abs(np.random.normal(0, 1)),
                "low": base - abs(np.random.normal(0, 1)),
                "close": base,
                "volume": np.random.randint(1000, 10000),
            }
        )
    return pd.DataFrame(data)


class TestIndicators:
    def test_calc_ma(self):
        df = _make_sample_df()
        result = calc_ma(df)
        assert "MA5" in result.columns
        assert "MA10" in result.columns
        assert "MA20" in result.columns
        assert "MA60" in result.columns
        assert result["MA5"].iloc[4] is not None

    def test_calc_macd(self):
        df = _make_sample_df()
        result = calc_macd(df)
        assert "DIF" in result.columns
        assert "DEA" in result.columns
        assert "MACD" in result.columns

    def test_calc_kdj(self):
        df = _make_sample_df()
        result = calc_kdj(df)
        assert "K" in result.columns
        assert "D" in result.columns
        assert "J" in result.columns

    def test_calc_boll(self):
        df = _make_sample_df()
        result = calc_boll(df)
        assert "BOLL_MID" in result.columns
        assert "BOLL_UP" in result.columns
        assert "BOLL_DN" in result.columns

    def test_calc_rsi(self):
        df = _make_sample_df()
        result = calc_rsi(df)
        assert "RSI" in result.columns
        assert 0 <= result["RSI"].dropna().iloc[-1] <= 100

    def test_calc_all_indicators(self):
        df = _make_sample_df()
        result = calc_all_indicators(df)
        assert "MA5" in result.columns
        assert "DIF" in result.columns
        assert "K" in result.columns
        assert "BOLL_MID" in result.columns
        assert "RSI" in result.columns


class TestVolumePatterns:
    def test_classify_volume_pattern(self):
        df = _make_sample_df(100)
        patterns = classify_volume_pattern(df)
        assert len(patterns) == len(df)
        assert patterns[0] == "数据不足"

    def test_add_volume_patterns(self):
        df = _make_sample_df(100)
        result = add_volume_patterns(df)
        assert "volume_pattern" in result.columns

    def test_surge_volume_detected(self):
        df = _make_sample_df(100)
        df.loc[99, "volume"] = df["volume"].iloc[94:99].mean() * 3
        patterns = classify_volume_pattern(df)
        assert patterns[-1] == "倍量"


class TestKeyLevels:
    def test_calc_key_levels(self):
        df = _make_sample_df(100)
        levels = calc_key_levels(df)
        assert "support" in levels
        assert "resistance" in levels
        assert "pivot" in levels
        assert len(levels["support"]) == 3
        assert len(levels["resistance"]) == 3

    def test_calc_pivot_points(self):
        df = _make_sample_df(100)
        pivots = calc_pivot_points(df)
        assert "pivot" in pivots
        assert "r1" in pivots
        assert "s1" in pivots
        assert pivots["r1"] > pivots["pivot"]
        assert pivots["s1"] < pivots["pivot"]
