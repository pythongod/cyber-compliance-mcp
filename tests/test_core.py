from cyber_compliance_mcp.core import generate_checklist, calculate_risk_score, get_framework_overview


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
