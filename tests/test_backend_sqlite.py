from pathlib import Path

from cyber_compliance_mcp.storage_backend import SQLiteStorageBackend


def test_sqlite_backend_roundtrip(tmp_path: Path):
    db = tmp_path / "assessments.db"
    backend = SQLiteStorageBackend(db)

    data = backend.load()
    assert data["schema_version"] >= 1

    data["assessments"]["x1"] = {"assessment_id": "x1", "framework": "nist_csf", "statuses": {}}
    backend.save(data)

    loaded = backend.load()
    assert "x1" in loaded["assessments"]


def test_sqlite_compact(tmp_path: Path):
    db = tmp_path / "assessments.db"
    backend = SQLiteStorageBackend(db)
    out = backend.compact()
    assert out["ok"] is True
    assert out["backend"] == "sqlite"
