from __future__ import annotations

import pandas as pd


def run_backtest(df: pd.DataFrame, signals):
    trades = []
    for s in signals:
        entry = s.entry
        sl = s.sl
        tp = s.tp
        side = s.side

        for i in range(len(df)):
            high = df.iloc[i]["high"]
            low = df.iloc[i]["low"]
            ts = df.iloc[i]["timestamp"]

            if side == "LONG":
                if low <= sl:
                    trades.append((s.time, ts, side, entry, sl, sl - entry))
                    break
                if high >= tp:
                    trades.append((s.time, ts, side, entry, tp, tp - entry))
                    break
            else:
                if high >= sl:
                    trades.append((s.time, ts, side, entry, sl, entry - sl))
                    break
                if low <= tp:
                    trades.append((s.time, ts, side, entry, tp, entry - tp))
                    break

    return trades