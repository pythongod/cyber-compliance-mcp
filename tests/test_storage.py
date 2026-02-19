from pathlib import Path

from cyber_compliance_mcp import storage


def test_storage_crud(tmp_path: Path, monkeypatch):
    db = tmp_path / "db.json"
    monkeypatch.setattr(storage, "DEFAULT_DB", db)

    c = storage.create_assessment("a1", "nist_csf")
    assert c["assessment_id"] == "a1"

    u = storage.update_control_status("a1", "GV.OV-01", "implemented")
    assert u["statuses"]["GV.OV-01"] == "implemented"

    g = storage.get_assessment("a1")
    assert g["assessment_id"] == "a1"

    lst = storage.list_assessments()
    assert len(lst["assessments"]) == 1
