from cyber_compliance_mcp.core import generate_checklist, calculate_risk_score, get_framework_overview, get_control_metadata, validate_inputs


def test_framework_overview_supported():
    out = get_framework_overview("nist_csf")
    assert out["framework"] == "nist_csf"
    assert out["control_count"] > 0


def test_generate_checklist_default_status():
    out = generate_checklist("iso27001", org_type="saas")
    assert out["framework"] == "iso27001"
    assert all(x["status"] == "not_started" for x in out["checklist"])


def test_calculate_risk_score_weighting():
    out = calculate_risk_score([
        {"control": "a", "status": "implemented"},
        {"control": "b", "status": "partial"},
        {"control": "c", "status": "missing"},
    ])
    assert out["controls_total"] == 3
    assert out["risk_level"] in {"medium", "high"}

def test_generate_checklist_includes_metadata_fields():
    out = generate_checklist("nist_csf", org_type="saas")
    row = out["checklist"][0]
    assert "priority" in row
    assert "owner" in row


def test_get_control_metadata_supported():
    out = get_control_metadata("soc2")
    assert out["framework"] == "soc2"
    assert out["count"] >= 1


def test_validate_inputs_bad_framework():
    out = validate_inputs("bad_framework")
    assert out["ok"] is False
    assert out["error"]["code"] == "INVALID_FRAMEWORK"
