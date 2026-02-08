from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Signal:
    side: str
    entry: float
    sl: float
    tp: float
    reason: str
    time: str


class StrategyBase:
    def generate(self, df):
        raise NotImplementedError