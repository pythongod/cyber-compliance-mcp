from cyber_compliance_mcp.metrics import as_prometheus, snapshot, inc, observe_latency
from cyber_compliance_mcp.policy import enforce_scope


def test_metrics_snapshot_updates():
    inc("requests.total")
    observe_latency("get_framework_overview", 12.5)
    s = snapshot()
    assert s["counters"].get("requests.total", 0) >= 1
    assert s["latency_sum_ms"].get("tool.get_framework_overview.latency_sum_ms", 0) >= 12.5


def test_policy_forbidden(monkeypatch):
    monkeypatch.setenv("CYBER_MCP_POLICY_ENFORCE", "true")
    monkeypatch.setenv("CYBER_MCP_ALLOWED_SCOPES", "read")
    out = enforce_scope("update_control_status")
    assert out is not None
    assert out["ok"] is False
    assert out["error"]["code"] == "FORBIDDEN"


def test_policy_profile_prod(monkeypatch):
    monkeypatch.setenv("CYBER_MCP_POLICY_ENFORCE", "true")
    monkeypatch.delenv("CYBER_MCP_ALLOWED_SCOPES", raising=False)
    monkeypatch.setenv("CYBER_MCP_POLICY_PROFILE", "prod")
    out = enforce_scope("update_control_status")
    assert out is not None and out["ok"] is False


def test_prometheus_export_has_metrics():
    text = as_prometheus()
    assert "cyber_mcp_" in text
