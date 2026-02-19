from __future__ import annotations

from typing import Any, Dict


def ok(payload: Dict[str, Any]) -> Dict[str, Any]:
    return {"ok": True, **payload}


def err(code: str, message: str, **extra: Any) -> Dict[str, Any]:
    detail: Dict[str, Any] = {"code": code, "message": message}
    if extra:
        detail.update(extra)
    return {"ok": False, "error": detail}
