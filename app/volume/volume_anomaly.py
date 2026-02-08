from __future__ import annotations

import pandas as pd


def volume_anomaly(df: pd.DataFrame, sma_period: int, multiplier: float) -> pd.Series:
    sma = df["volume"].rolling(sma_period).mean()
    return df["volume"] > sma * multiplier