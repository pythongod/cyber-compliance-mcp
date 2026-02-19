from cyber_compliance_mcp.requirements import get_requirements, list_requirement_frameworks


def test_list_requirement_frameworks_contains_expected():
    out = list_requirement_frameworks()
    assert out["ok"] is True
    assert "nist_csf" in out["frameworks"]
    assert "pci_dss" in out["frameworks"]


def test_get_requirements_pci_query():
    out = get_requirements("pci_dss", "cryptography")
    assert out["ok"] is True
    assert out["count"] >= 1


def test_get_requirements_invalid_framework():
    out = get_requirements("foo")
    assert out["ok"] is False
    assert out["error"]["code"] == "INVALID_FRAMEWORK"
