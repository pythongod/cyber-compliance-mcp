from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict


DEFAULT_DB = Path("assessments-db.json")


def _load_db(path: Path = DEFAULT_DB) -> Dict[str, Any]:
    if not path.exists():
        return {"assessments": {}}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return {"assessments": {}}
    data.setdefault("assessments", {})
    return data


def _save_db(data: Dict[str, Any], path: Path = DEFAULT_DB) -> None:
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def create_assessment(assessment_id: str, framework: str, org_type: str = "saas") -> Dict[str, Any]:
    db = _load_db()
    assessments = db.setdefault("assessments", {})
    if assessment_id in assessments:
        return {"error": "assessment_exists", "assessment_id": assessment_id}

    assessments[assessment_id] = {
        "assessment_id": assessment_id,
        "framework": framework,
        "org_type": org_type,
        "statuses": {},
    }
    _save_db(db)
    return assessments[assessment_id]


def update_control_status(assessment_id: str, control: str, status: str) -> Dict[str, Any]:
    status = status.lower().strip()
    if status not in {"implemented", "partial", "missing"}:
        return {"error": "invalid_status", "allowed": ["implemented", "partial", "missing"]}

    db = _load_db()
    assessments = db.setdefault("assessments", {})
    entry = assessments.get(assessment_id)
    if not entry:
        return {"error": "assessment_not_found", "assessment_id": assessment_id}

    entry.setdefault("statuses", {})[control] = status
    _save_db(db)
    return entry


def get_assessment(assessment_id: str) -> Dict[str, Any]:
    db = _load_db()
    entry = db.get("assessments", {}).get(assessment_id)
    if not entry:
        return {"error": "assessment_not_found", "assessment_id": assessment_id}
    return entry


def list_assessments() -> Dict[str, Any]:
    db = _load_db()
    return {"assessments": list(db.get("assessments", {}).values())}
