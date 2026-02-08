from __future__ import annotations

from rich.table import Table
from rich.console import Console

from app.config import load_config
from app.providers.exchange import fetch_ohlcv
from app.strategies.volume_absorption_break import generate_signals


def run_scan():
    cfg = load_config()
    console = Console()
    table = Table(title="CRYPTO SIGNAL SCANNER")

    table.add_column("Symbol")
    table.add_column("Timeframe")
    table.add_column("Signal")
    table.add_column("Price")
    table.add_column("Reason")

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
                s = signals[-1]
                table.add_row(symbol, tf, s.side, str(s.entry), s.reason)

    console.print(table)