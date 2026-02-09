from __future__ import annotations

from pathlib import Path
from typing import Any, Dict, List

import yaml
from pydantic import BaseModel, Field


class VolumeConfig(BaseModel):
    sma_period: int = 20
    multiplier: float = 2.0
    absorption_body_ratio: float = 0.3
    absorption_range_ratio: float = 0.4


class RiskConfig(BaseModel):
    initial_capital: float = 10000.0
    risk_per_trade: float = 0.01
    atr_multiplier: float = 1.5
    rr: float = 2.0


class ScannerConfig(BaseModel):
    symbols: List[str] = Field(default_factory=lambda: ["BTC/USDT"])
    timeframes: List[str] = Field(default_factory=lambda: ["15m"])
    use_all_usdt_futures: bool = False


class StrategyFilters(BaseModel):
    use_rsi: bool = True
    use_macd: bool = True
    allow_sideways: bool = True


class AppConfig(BaseModel):
    exchange: str = "binance"
    volume: VolumeConfig = VolumeConfig()
    risk: RiskConfig = RiskConfig()
    scanner: ScannerConfig = ScannerConfig()
    filters: StrategyFilters = StrategyFilters()


def load_config(path: str = "config.yaml") -> AppConfig:
    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    data: Dict[str, Any] = yaml.safe_load(config_path.read_text())
    return AppConfig(**data)