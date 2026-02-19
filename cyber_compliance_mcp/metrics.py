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


def as_prometheus() -> str:
    with _LOCK:
        lines = [
            "# HELP cyber_mcp_requests_total Total request events.",
            "# TYPE cyber_mcp_requests_total counter",
        ]
        for k, v in sorted(_COUNTERS.items()):
            safe = k.replace(".", "_")
            lines.append(f"cyber_mcp_{safe} {v}")

        lines.append("# HELP cyber_mcp_latency_sum_ms Total observed latency per tool in ms.")
        lines.append("# TYPE cyber_mcp_latency_sum_ms gauge")
        for k, v in sorted(_LATENCY_SUM_MS.items()):
            safe = k.replace(".", "_")
            lines.append(f"cyber_mcp_{safe} {v}")

    return "\n".join(lines) + "\n"
