from __future__ import annotations

import pandas as pd


def absorption_candle(df: pd.DataFrame, body_ratio: float, range_ratio: float) -> pd.Series:
    candle_range = df["high"] - df["low"]
    body = (df["close"] - df["open"]).abs()
    small_body = body / candle_range < body_ratio
    small_range = candle_range / candle_range.rolling(20).mean() < range_ratio
    return small_body & small_range