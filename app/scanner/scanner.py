from __future__ import annotations

from rich.table import Table
from rich.console import Console

from app.alerts.telegram import alert_if_new
from app.config import load_config
from app.providers.exchange import fetch_ohlcv, fetch_usdt_futures_symbols
from app.strategies.volume_absorption_break import generate_signals

def _build_alert_message(symbol: str, timeframe: str, signal) -> str:
    return (
        f"{symbol} {timeframe} {signal.side}\n"
        f"Entry: {signal.entry}\n"
        f"SL: {signal.sl}\n"
        f"TP: {signal.tp}\n"
        f"Reason: {signal.reason}\n"
        f"Time: {signal.time}"
    )

def run_scan():
    cfg = load_config()
    console = Console()
    table = Table(title="CRYPTO SIGNAL SCANNER")

    table.add_column("Symbol")
    table.add_column("Timeframe")
    table.add_column("Signal")
    table.add_column("Price")
    table.add_column("Reason")

    if cfg.scanner.use_all_usdt_futures:
        symbols = fetch_usdt_futures_symbols(cfg.exchange)
        market_type = "future"
    else:
        symbols = cfg.scanner.symbols
        market_type = None

    for symbol in symbols:
        for tf in cfg.scanner.timeframes:
            df = fetch_ohlcv(cfg.exchange, symbol, tf, market_type=market_type)
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
                s = signals[-1]
                table.add_row(symbol, tf, s.side, str(s.entry), s.reason)
                message = _build_alert_message(symbol, tf, s)
                alert_if_new(f"{symbol}:{tf}:{s.side}", message)

    console.print(table)