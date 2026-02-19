from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any, Dict

from .errors import err, ok

DEFAULT_DB = Path("assessments-db.json")
ALLOWED_STATUSES = {"implemented", "partial", "missing"}
ASSESSMENT_ID_RE = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9._:-]{1,63}$")


def _validate_assessment_id(assessment_id: str) -> Dict[str, Any] | None:
    if not assessment_id or not str(assessment_id).strip():
        return err("INVALID_ASSESSMENT_ID", "assessment_id cannot be empty")
    if not ASSESSMENT_ID_RE.match(str(assessment_id)):
        return err(
            "INVALID_ASSESSMENT_ID",
            "assessment_id must match ^[a-zA-Z0-9][a-zA-Z0-9._:-]{1,63}$",
        )
    return None


def _validate_control(control: str) -> Dict[str, Any] | None:
    if not control or not str(control).strip():
        return err("INVALID_CONTROL", "control cannot be empty")
    return None


def _validate_status(status: str) -> Dict[str, Any] | None:
    normalized = str(status).lower().strip()
    if normalized not in ALLOWED_STATUSES:
        return err(
            "INVALID_STATUS",
            f"Unsupported status: {status}",
            allowed=sorted(ALLOWED_STATUSES),
        )
    return None


def _load_db(path: Path | None = None) -> Dict[str, Any]:
    path = path or DEFAULT_DB
    if not path.exists():
        return {"assessments": {}}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        return {"assessments": {}}
    data.setdefault("assessments", {})
    return data


def _save_db(data: Dict[str, Any], path: Path | None = None) -> None:
    path = path or DEFAULT_DB
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def create_assessment(assessment_id: str, framework: str, org_type: str = "saas") -> Dict[str, Any]:
    bad_id = _validate_assessment_id(assessment_id)
    if bad_id:
        return bad_id
    if not framework or not str(framework).strip():
        return err("INVALID_FRAMEWORK", "framework cannot be empty")
    if not org_type or not str(org_type).strip():
        return err("INVALID_ORG_TYPE", "org_type cannot be empty")

    db = _load_db()
    assessments = db.setdefault("assessments", {})
    if assessment_id in assessments:
        return err("ASSESSMENT_EXISTS", "assessment already exists", assessment_id=assessment_id)

    assessments[assessment_id] = {
        "assessment_id": assessment_id,
        "framework": framework,
        "org_type": org_type,
        "statuses": {},
    }
    _save_db(db)
    return ok(assessments[assessment_id])


def update_control_status(assessment_id: str, control: str, status: str) -> Dict[str, Any]:
    bad_id = _validate_assessment_id(assessment_id)
    if bad_id:
        return bad_id
    bad_control = _validate_control(control)
    if bad_control:
        return bad_control
    bad_status = _validate_status(status)
    if bad_status:
        return bad_status

    db = _load_db()
    assessments = db.setdefault("assessments", {})
    entry = assessments.get(assessment_id)
    if not entry:
        return err("ASSESSMENT_NOT_FOUND", "assessment not found", assessment_id=assessment_id)

    entry.setdefault("statuses", {})[control] = str(status).lower().strip()
    _save_db(db)
    return ok(entry)


def get_assessment(assessment_id: str) -> Dict[str, Any]:
    bad_id = _validate_assessment_id(assessment_id)
    if bad_id:
        return bad_id

    db = _load_db()
    entry = db.get("assessments", {}).get(assessment_id)
    if not entry:
        return err("ASSESSMENT_NOT_FOUND", "assessment not found", assessment_id=assessment_id)
    return ok(entry)


def list_assessments() -> Dict[str, Any]:
    db = _load_db()
    return ok({"assessments": list(db.get("assessments", {}).values())})
