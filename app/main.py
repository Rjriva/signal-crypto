from __future__ import annotations

from fastapi import FastAPI
from app.config import load_config
from app.providers.exchange import fetch_ohlcv
from app.strategies.volume_absorption_break import generate_signals

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/scan")
def scan():
    cfg = load_config()
    results = []
    for symbol in cfg.scanner.symbols:
        for tf in cfg.scanner.timeframes:
            df = fetch_ohlcv(cfg.exchange, symbol, tf)
            signals = generate_signals(
                df,
                cfg.volume.multiplier,
                cfg.risk.atr_multiplier,
                cfg.risk.rr,
                cfg.filters.use_rsi,
                cfg.filters.use_macd,
                cfg.filters.allow_sideways,
            )
            if signals:
                results.append(
                    {"symbol": symbol, "timeframe": tf, "signal": signals[-1].side}
                )
    return results


@app.get("/backtest")
def backtest(symbol: str, timeframe: str):
    cfg = load_config()
    df = fetch_ohlcv(cfg.exchange, symbol, timeframe)
    signals = generate_signals(
        df,
        cfg.volume.multiplier,
        cfg.risk.atr_multiplier,
        cfg.risk.rr,
        cfg.filters.use_rsi,
        cfg.filters.use_macd,
        cfg.filters.allow_sideways,
    )
    return {"symbol": symbol, "timeframe": timeframe, "trades": len(signals)}