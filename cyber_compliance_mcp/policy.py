from __future__ import annotations

import os
from typing import Dict

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
    "create_assessment": "write",
    "update_control_status": "write",
    "get_metrics": "admin",
}


def enforce_scope(tool_name: str) -> dict | None:
    enabled = os.getenv("CYBER_MCP_POLICY_ENFORCE", "false").lower() == "true"
    if not enabled:
        return None

    allowed = {x.strip() for x in os.getenv("CYBER_MCP_ALLOWED_SCOPES", "read,write,admin").split(",") if x.strip()}
    required = TOOL_SCOPE.get(tool_name, "read")
    if required not in allowed:
        return err(
            "FORBIDDEN",
            f"Scope '{required}' required for tool '{tool_name}'",
            required_scope=required,
            allowed_scopes=sorted(allowed),
        )
    return None
