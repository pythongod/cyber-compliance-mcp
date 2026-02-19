import json
from pathlib import Path

from cyber_compliance_mcp import storage
from cyber_compliance_mcp.storage_backend import JsonFileStorageBackend


def test_storage_crud(tmp_path: Path, monkeypatch):
    db = tmp_path / "db.json"
    monkeypatch.setattr(storage, "DEFAULT_DB", db)

    c = storage.create_assessment("a1", "nist_csf")
    assert c["ok"] is True
    assert c["assessment_id"] == "a1"

    u = storage.update_control_status("a1", "GV.OV-01", "implemented")
    assert u["ok"] is True
    assert u["statuses"]["GV.OV-01"] == "implemented"

    g = storage.get_assessment("a1")
    assert g["ok"] is True
    assert g["assessment_id"] == "a1"

    lst = storage.list_assessments()
    assert lst["ok"] is True
    assert len(lst["assessments"]) == 1


def test_storage_validation_errors(tmp_path: Path, monkeypatch):
    db = tmp_path / "db.json"
    monkeypatch.setattr(storage, "DEFAULT_DB", db)

    bad = storage.create_assessment("", "nist_csf")
    assert bad["error"]["code"] == "INVALID_ASSESSMENT_ID"

    storage.create_assessment("ok-id", "nist_csf")
    bad2 = storage.update_control_status("ok-id", "", "implemented")
    assert bad2["error"]["code"] == "INVALID_CONTROL"

    bad3 = storage.update_control_status("ok-id", "GV.OV-01", "nope")
    assert bad3["error"]["code"] == "INVALID_STATUS"


def test_storage_env_path_backend(tmp_path: Path, monkeypatch):
    db = tmp_path / "env-db.json"
    monkeypatch.setenv("CYBER_MCP_DB_PATH", str(db))
    out = storage.create_assessment("env-id", "nist_csf")
    assert out["ok"] is True
    assert db.exists()


def test_storage_schema_version_and_migration(tmp_path: Path):
    db = tmp_path / "legacy.json"
    db.write_text(json.dumps({"assessments": {"a": {"assessment_id": "a", "framework": "nist_csf"}}}), encoding="utf-8")

    backend = JsonFileStorageBackend(db)
    data = backend.load()

    assert data["schema_version"] == 1
    assert "statuses" in data["assessments"]["a"]
