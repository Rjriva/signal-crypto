from __future__ import annotations

import pandas as pd

from app.indicators.ema import ema
from app.indicators.rsi import rsi
from app.indicators.macd import macd
from app.indicators.atr import atr
from app.volume.volume_anomaly import volume_anomaly
from app.volume.volume_profile import absorption_candle
from app.strategies.base import Signal


def generate_signals(
    df: pd.DataFrame,
    volume_multiplier: float,
    atr_multiplier: float,
    rr: float,
    use_rsi: bool,
    use_macd: bool,
    allow_sideways: bool,
):
    df = df.copy()
    df["ema200"] = ema(df["close"], 200)
    df["ema50"] = ema(df["close"], 50)
    df["ema20"] = ema(df["close"], 20)
    df["rsi"] = rsi(df["close"])
    _, _, df["macd_hist"] = macd(df["close"])
    df["atr"] = atr(df)
    df["volume_anomaly"] = volume_anomaly(df, 20, volume_multiplier)
    df["absorption"] = absorption_candle(df, 0.3, 0.4)

    signals = []

    for i in range(2, len(df)):
        prev = df.iloc[i - 1]
        curr = df.iloc[i]

        trend_long = curr["close"] > curr["ema200"] or allow_sideways
        trend_short = curr["close"] < curr["ema200"] or allow_sideways

        if prev["volume_anomaly"] and prev["absorption"]:
            # LONG
            if trend_long and curr["high"] > prev["high"]:
                if (not use_rsi or curr["rsi"] > 50) and (
                    not use_macd or curr["macd_hist"] > 0
                ):
                    entry = prev["high"]
                    sl = prev["low"] - curr["atr"] * atr_multiplier
                    tp = entry + (entry - sl) * rr
                    signals.append(
                        Signal("LONG", entry, sl, tp, "Absorption break LONG", str(curr["timestamp"]))
                    )
            # SHORT
            if trend_short and curr["low"] < prev["low"]:
                if (not use_rsi or curr["rsi"] < 50) and (
                    not use_macd or curr["macd_hist"] < 0
                ):
                    entry = prev["low"]
                    sl = prev["high"] + curr["atr"] * atr_multiplier
                    tp = entry - (sl - entry) * rr
                    signals.append(
                        Signal("SHORT", entry, sl, tp, "Absorption break SHORT", str(curr["timestamp"]))
                    )

    return signals