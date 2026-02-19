from __future__ import annotations

import os
import time
import uuid
from collections import defaultdict, deque
from typing import Any

from .errors import err

REQUESTS: dict[str, deque[float]] = defaultdict(deque)


def _now() -> float:
    return time.time()


def request_context(tool_name: str, *args: Any) -> dict:
    request_id = str(uuid.uuid4())[:8]

    token_required = os.getenv("CYBER_MCP_AUTH_REQUIRED", "false").lower() == "true"
    expected = os.getenv("CYBER_MCP_API_TOKEN", "")
    provided = os.getenv("CYBER_MCP_CLIENT_TOKEN", "")

    if token_required:
        if not expected:
            return err("AUTH_CONFIG_ERROR", "CYBER_MCP_API_TOKEN is required when auth is enabled", request_id=request_id)
        if provided != expected:
            return err("UNAUTHORIZED", "Invalid or missing CYBER_MCP_CLIENT_TOKEN", request_id=request_id)

    # request size limits
    max_chars = int(os.getenv("CYBER_MCP_MAX_CHARS", "12000"))
    total_chars = sum(len(str(a)) for a in args)
    if total_chars > max_chars:
        return err("REQUEST_TOO_LARGE", f"Request exceeds char limit ({max_chars})", request_id=request_id)

    # naive rate limit (per tool)
    limit = int(os.getenv("CYBER_MCP_RATE_LIMIT", "60"))
    window = int(os.getenv("CYBER_MCP_RATE_WINDOW_SEC", "60"))
    dq = REQUESTS[tool_name]
    ts = _now()
    while dq and dq[0] < ts - window:
        dq.popleft()
    if len(dq) >= limit:
        return err("RATE_LIMITED", f"Too many requests for {tool_name}", request_id=request_id, retry_after_sec=window)
    dq.append(ts)

    return {"ok": True, "request_id": request_id}
