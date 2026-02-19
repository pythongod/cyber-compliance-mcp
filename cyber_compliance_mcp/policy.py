from __future__ import annotations

import os
from typing import Dict, Set

from .errors import err

TOOL_SCOPE: Dict[str, str] = {
    "get_framework_overview": "read",
    "get_control_metadata": "read",
    "generate_checklist": "read",
    "calculate_risk_score": "read",
    "recommend_next_actions": "read",
    "get_framework_crosswalk": "read",
    "list_assessments": "read",
    "get_assessment": "read",
    "list_requirement_frameworks": "read",
    "get_requirements": "read",
    "create_assessment": "write",
    "update_control_status": "write",
    "compact_storage": "admin",
    "get_metrics": "admin",
    "get_metrics_prometheus": "admin",
}

PROFILE_SCOPES: Dict[str, Set[str]] = {
    "dev": {"read", "write", "admin"},
    "staging": {"read", "write"},
    "prod": {"read"},
}


def _allowed_scopes() -> Set[str]:
    explicit = os.getenv("CYBER_MCP_ALLOWED_SCOPES", "").strip()
    if explicit:
        return {x.strip() for x in explicit.split(",") if x.strip()}

    profile = os.getenv("CYBER_MCP_POLICY_PROFILE", "dev").strip().lower()
    return PROFILE_SCOPES.get(profile, PROFILE_SCOPES["dev"])


def enforce_scope(tool_name: str) -> dict | None:
    enabled = os.getenv("CYBER_MCP_POLICY_ENFORCE", "false").lower() == "true"
    if not enabled:
        return None

    allowed = _allowed_scopes()
    required = TOOL_SCOPE.get(tool_name, "read")
    if required not in allowed:
        return err(
            "FORBIDDEN",
            f"Scope '{required}' required for tool '{tool_name}'",
            required_scope=required,
            allowed_scopes=sorted(allowed),
            policy_profile=os.getenv("CYBER_MCP_POLICY_PROFILE", "dev"),
        )
    return None
