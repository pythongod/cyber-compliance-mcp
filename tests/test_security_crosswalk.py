import os

from cyber_compliance_mcp.crosswalk import get_framework_crosswalk
from cyber_compliance_mcp.security import request_context


def test_crosswalk_ok():
    out = get_framework_crosswalk("access_control")
    assert out["ok"] is True
    assert "nist_csf" in out["mapping"]


def test_crosswalk_bad_topic():
    out = get_framework_crosswalk("weird")
    assert out["ok"] is False
    assert out["error"]["code"] == "INVALID_TOPIC"


def test_request_context_auth_and_limits(monkeypatch):
    monkeypatch.setenv("CYBER_MCP_AUTH_REQUIRED", "true")
    monkeypatch.setenv("CYBER_MCP_API_TOKEN", "secret")
    monkeypatch.setenv("CYBER_MCP_CLIENT_TOKEN", "wrong")
    out = request_context("x", "a")
    assert out["ok"] is False
    assert out["error"]["code"] == "UNAUTHORIZED"
