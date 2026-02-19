from __future__ import annotations

from collections import defaultdict
from threading import Lock
from typing import Dict

_LOCK = Lock()
_COUNTERS: Dict[str, int] = defaultdict(int)
_LATENCY_SUM_MS: Dict[str, float] = defaultdict(float)


def inc(key: str, by: int = 1) -> None:
    with _LOCK:
        _COUNTERS[key] += by


def observe_latency(tool: str, ms: float) -> None:
    with _LOCK:
        _COUNTERS[f"tool.{tool}.calls"] += 1
        _LATENCY_SUM_MS[f"tool.{tool}.latency_sum_ms"] += ms


def snapshot() -> dict:
    with _LOCK:
        return {
            "counters": dict(_COUNTERS),
            "latency_sum_ms": dict(_LATENCY_SUM_MS),
        }
