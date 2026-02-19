from __future__ import annotations

import json
import os
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Protocol

CURRENT_SCHEMA_VERSION = 1


class StorageBackend(Protocol):
    def load(self) -> Dict[str, Any]: ...

    def save(self, data: Dict[str, Any]) -> None: ...


@contextmanager
def _advisory_lock(lock_path: Path):
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    f = lock_path.open("a+")
    try:
        try:
            import fcntl

            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        except Exception:
            # best-effort fallback when flock is unavailable
            pass
        yield
    finally:
        try:
            import fcntl

            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
        except Exception:
            pass
        f.close()


class JsonFileStorageBackend:
    def __init__(self, path: str | Path | None = None) -> None:
        env_path = os.getenv("CYBER_MCP_DB_PATH")
        self.path = Path(path or env_path or "assessments-db.json")
        self.lock_path = Path(str(self.path) + ".lock")

    def _normalize(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(data, dict):
            data = {}
        data.setdefault("assessments", {})
        current = int(data.get("schema_version", 0) or 0)
        if current < CURRENT_SCHEMA_VERSION:
            data = self._migrate(data)
        else:
            data.setdefault("schema_version", CURRENT_SCHEMA_VERSION)
        return data

    def _migrate(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # v0 -> v1: ensure root fields and assessment statuses shape
        data.setdefault("assessments", {})
        for _, entry in list(data["assessments"].items()):
            if not isinstance(entry, dict):
                continue
            entry.setdefault("statuses", {})
            if not isinstance(entry["statuses"], dict):
                entry["statuses"] = {}
        data["schema_version"] = CURRENT_SCHEMA_VERSION
        return data

    def load(self) -> Dict[str, Any]:
        with _advisory_lock(self.lock_path):
            if not self.path.exists():
                return {"schema_version": CURRENT_SCHEMA_VERSION, "assessments": {}}
            data = json.loads(self.path.read_text(encoding="utf-8"))
            normalized = self._normalize(data)
            if normalized.get("schema_version") != data.get("schema_version"):
                self.path.write_text(json.dumps(normalized, indent=2), encoding="utf-8")
            return normalized

    def save(self, data: Dict[str, Any]) -> None:
        normalized = self._normalize(data)
        with _advisory_lock(self.lock_path):
            self.path.parent.mkdir(parents=True, exist_ok=True)
            self.path.write_text(json.dumps(normalized, indent=2), encoding="utf-8")


def get_backend() -> StorageBackend:
    return JsonFileStorageBackend()
