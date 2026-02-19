from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, Protocol


class StorageBackend(Protocol):
    def load(self) -> Dict[str, Any]: ...

    def save(self, data: Dict[str, Any]) -> None: ...


class JsonFileStorageBackend:
    def __init__(self, path: str | Path | None = None) -> None:
        env_path = os.getenv("CYBER_MCP_DB_PATH")
        self.path = Path(path or env_path or "assessments-db.json")

    def load(self) -> Dict[str, Any]:
        if not self.path.exists():
            return {"assessments": {}}
        data = json.loads(self.path.read_text(encoding="utf-8"))
        if not isinstance(data, dict):
            return {"assessments": {}}
        data.setdefault("assessments", {})
        return data

    def save(self, data: Dict[str, Any]) -> None:
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def get_backend() -> StorageBackend:
    return JsonFileStorageBackend()
