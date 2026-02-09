from __future__ import annotations

import time
from pathlib import Path
from typing import Optional

import ccxt
import pandas as pd

from app.utils.logger import setup_logger

logger = setup_logger()

def _cache_path(symbol: str, timeframe: str) -> Path:
    safe_symbol = symbol.replace("/", "_").replace(":", "_")
    return Path("app/data") / f"{safe_symbol}_{timeframe}.csv"

def _build_exchange(exchange_name: str, market_type: Optional[str] = None) -> ccxt.Exchange:
    exchange_class = getattr(ccxt, exchange_name)
    config = {"enableRateLimit": True}
    if market_type:
        config["options"] = {"defaultType": market_type}
    return exchange_class(config)

def fetch_usdt_futures_symbols(exchange_name: str) -> list[str]:
    exchange = _build_exchange(exchange_name, market_type="future")
    markets = exchange.load_markets()
    symbols: list[str] = []
    for market in markets.values():
        if not market.get("active", True):
            continue
        if not market.get("contract"):
            continue
        if market.get("quote") != "USDT":
            continue
        if not market.get("linear", False):
            continue
        symbols.append(market["symbol"])
    return sorted(symbols)

def fetch_ohlcv(
    exchange_name: str,
    symbol: str,
    timeframe: str,
    limit: int = 500,
    use_cache: bool = True,
    market_type: Optional[str] = None,
) -> pd.DataFrame:
    cache_file = _cache_path(symbol, timeframe)
    if use_cache and cache_file.exists():
        return pd.read_csv(cache_file)

    exchange = _build_exchange(exchange_name, market_type=market_type)

    for attempt in range(3):
        try:
            data = exchange.fetch_ohlcv(symbol, timeframe=timeframe, limit=limit)
            df = pd.DataFrame(
                data, columns=["timestamp", "open", "high", "low", "close", "volume"]
            )
            df["timestamp"] = pd.to_datetime(df["timestamp"], unit="ms")
            cache_file.parent.mkdir(parents=True, exist_ok=True)
            df.to_csv(cache_file, index=False)
            return df
        except (ccxt.RequestTimeout, ccxt.DDoSProtection) as e:
            logger.warning(f"Retry {attempt+1}/3 due to: {e}")
            time.sleep(2)

    raise RuntimeError("Failed to fetch OHLCV data after retries.")