from app.config import load_config
from app.providers.exchange import fetch_ohlcv
from app.strategies.volume_absorption_break import generate_signals
from app.backtest.engine import run_backtest

if __name__ == "__main__":
    cfg = load_config()
    symbol = cfg.scanner.symbols[0]
    timeframe = cfg.scanner.timeframes[0]
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
    trades = run_backtest(df, signals)
    print(f"Trades generated: {len(trades)}")