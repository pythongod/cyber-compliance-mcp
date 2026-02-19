from __future__ import annotations

import json
import os
import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Protocol

CURRENT_SCHEMA_VERSION = 1


class StorageBackend(Protocol):
    def load(self) -> Dict[str, Any]: ...

    def save(self, data: Dict[str, Any]) -> None: ...

    def compact(self) -> Dict[str, Any]: ...


@contextmanager
def _advisory_lock(lock_path: Path):
    lock_path.parent.mkdir(parents=True, exist_ok=True)
    f = lock_path.open("a+")
    try:
        try:
            import fcntl

            fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        except Exception:
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

    def compact(self) -> Dict[str, Any]:
        data = self.load()
        self.save(data)
        return {"ok": True, "backend": "json", "path": str(self.path)}


class SQLiteStorageBackend:
    def __init__(self, path: str | Path | None = None) -> None:
        env_path = os.getenv("CYBER_MCP_DB_PATH")
        self.path = Path(path or env_path or "assessments.db")

    def _conn(self) -> sqlite3.Connection:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        conn = sqlite3.connect(str(self.path))
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute(
            "CREATE TABLE IF NOT EXISTS kv (k TEXT PRIMARY KEY, v TEXT NOT NULL)"
        )
        return conn

    def _normalize(self, data: Dict[str, Any]) -> Dict[str, Any]:
        if not isinstance(data, dict):
            data = {}
        data.setdefault("assessments", {})
        data.setdefault("schema_version", CURRENT_SCHEMA_VERSION)
        return data

    def load(self) -> Dict[str, Any]:
        with self._conn() as conn:
            row = conn.execute("SELECT v FROM kv WHERE k='db' LIMIT 1").fetchone()
            if not row:
                data = {"schema_version": CURRENT_SCHEMA_VERSION, "assessments": {}}
                conn.execute("INSERT OR REPLACE INTO kv(k,v) VALUES('db',?)", (json.dumps(data),))
                conn.commit()
                return data
            data = json.loads(row[0])
            data = self._normalize(data)
            return data

    def save(self, data: Dict[str, Any]) -> None:
        normalized = self._normalize(data)
        with self._conn() as conn:
            conn.execute("INSERT OR REPLACE INTO kv(k,v) VALUES('db',?)", (json.dumps(normalized),))
            conn.commit()

    def compact(self) -> Dict[str, Any]:
        with self._conn() as conn:
            conn.execute("VACUUM")
        return {"ok": True, "backend": "sqlite", "path": str(self.path)}


def get_backend() -> StorageBackend:
    kind = os.getenv("CYBER_MCP_BACKEND", "json").strip().lower()
    if kind == "sqlite":
        return SQLiteStorageBackend()
    return JsonFileStorageBackend()
