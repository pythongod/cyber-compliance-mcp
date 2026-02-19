from __future__ import annotations

from typing import Dict, List

from .metadata import CONTROL_METADATA
from .errors import err, ok

FRAMEWORK_CONTROLS: Dict[str, List[str]] = {
    "nist_csf": [
        "GV.OV-01 Governance strategy defined",
        "ID.AM-01 Asset inventory maintained",
        "PR.AA-01 Identity and access managed",
        "DE.CM-01 Continuous monitoring enabled",
        "RS.RP-01 Incident response plan executed",
        "RC.RP-01 Recovery plan validated",
    ],
    "iso27001": [
        "5.1 Information security policies",
        "5.7 Threat intelligence",
        "8.9 Configuration management",
        "8.15 Logging",
        "8.16 Monitoring activities",
        "8.23 Web filtering",
    ],
    "soc2": [
        "CC1 Control environment",
        "CC2 Communication and information",
        "CC6 Logical and physical access controls",
        "CC7 System operations",
        "CC8 Change management",
        "A1 Additional criteria for availability",
    ],
    "cis_v8": [
        "1.1 Inventory and control of enterprise assets",
        "4.1 Secure configuration process",
        "5.1 Account management",
        "8.2 Audit log management",
        "12.1 Network infrastructure management",
        "17.1 Incident response process",
    ],
}


def get_framework_overview(framework: str) -> dict:
    key = framework.strip().lower()
    controls = FRAMEWORK_CONTROLS.get(key)
    if not controls:
        return err(
            "INVALID_FRAMEWORK",
            f"Unsupported framework: {framework}",
            allowed=sorted(FRAMEWORK_CONTROLS.keys()),
        )
    return ok(
        {
            "framework": key,
            "control_count": len(controls),
            "controls": controls,
        }
    )


def generate_checklist(framework: str, org_type: str = "saas") -> dict:
    key = framework.strip().lower()
    controls = FRAMEWORK_CONTROLS.get(key)
    if not controls:
        return err(
            "INVALID_FRAMEWORK",
            f"Unsupported framework: {framework}",
            allowed=sorted(FRAMEWORK_CONTROLS.keys()),
        )

    if not str(org_type).strip():
        return err("INVALID_ORG_TYPE", "org_type cannot be empty")

    checklist = []
    for c in controls:
        meta = CONTROL_METADATA.get(key, {}).get(c, {})
        checklist.append(
            {
                "control": c,
                "status": "not_started",
                "owner": meta.get("owner", "security"),
                "priority": meta.get("priority", "medium"),
                "evidence": [meta.get("evidence_example")] if meta.get("evidence_example") else [],
                "notes": f"Required for {org_type} environment",
            }
        )

    return ok(
        {
            "framework": key,
            "org_type": org_type,
            "checklist": checklist,
        }
    )


def calculate_risk_score(controls: List[dict]) -> dict:
    weights = {"implemented": 0, "partial": 5, "missing": 10}

    if controls is None:
        return err("INVALID_CONTROLS", "controls cannot be null")
    if not isinstance(controls, list):
        return err("INVALID_CONTROLS", "controls must be a list")
    if not controls:
        return ok({"risk_score": 0, "risk_level": "low", "summary": "No controls provided"})

    total = 0
    missing = 0
    partial = 0

    for c in controls:
        status = str(c.get("status", "missing")).lower()
        total += weights.get(status, 10)
        if status == "missing":
            missing += 1
        elif status == "partial":
            partial += 1

    max_score = len(controls) * 10
    pct = (total / max_score) * 100 if max_score else 0

    if pct < 25:
        level = "low"
    elif pct < 50:
        level = "medium"
    elif pct < 75:
        level = "high"
    else:
        level = "critical"

    return ok(
        {
            "risk_score": round(pct, 2),
            "risk_level": level,
            "controls_total": len(controls),
            "missing": missing,
            "partial": partial,
            "implemented": len(controls) - missing - partial,
        }
    )


def recommend_next_actions(framework: str, gaps: List[str]) -> dict:
    framework = framework.lower().strip()
    if framework not in FRAMEWORK_CONTROLS:
        return err(
            "INVALID_FRAMEWORK",
            f"Unsupported framework: {framework}",
            allowed=sorted(FRAMEWORK_CONTROLS.keys()),
        )
    if not isinstance(gaps, list):
        return err("INVALID_GAPS", "gaps must be a list")

    scored_actions = []
    for gap in gaps:
        g = gap.lower()
        if "asset" in g or "inventory" in g:
            action = "Implement automated asset discovery and CMDB sync"
            severity, effort = "high", "medium"
        elif "access" in g or "identity" in g:
            action = "Enable SSO + MFA everywhere and review privileged access"
            severity, effort = "critical", "medium"
        elif "log" in g or "monitor" in g:
            action = "Centralize logs in SIEM with 90+ day retention"
            severity, effort = "high", "high"
        elif "incident" in g:
            action = "Run incident response tabletop exercises quarterly"
            severity, effort = "high", "low"
        else:
            action = f"Define remediation owner and evidence plan for: {gap}"
            severity, effort = "medium", "low"

        sev_score = {"medium": 2, "high": 3, "critical": 4}[severity]
        eff_score = {"low": 1, "medium": 2, "high": 3}[effort]
        priority_score = (sev_score * 10) - (eff_score * 2)

        scored_actions.append(
            {
                "gap": gap,
                "action": action,
                "severity": severity,
                "effort": effort,
                "priority_score": priority_score,
            }
        )

    scored_actions.sort(key=lambda x: x["priority_score"], reverse=True)

    return ok(
        {
            "framework": framework,
            "gaps": gaps,
            "recommended_actions": [x["action"] for x in scored_actions],
            "recommended_actions_scored": scored_actions,
            "priority": "Start with high-impact missing controls and evidence collection",
        }
    )


def validate_inputs(framework: str, org_type: str | None = None) -> dict:
    """Validate common inputs and return normalized values/errors."""
    fw = str(framework or "").strip().lower()
    if fw not in FRAMEWORK_CONTROLS:
        return err(
            "INVALID_FRAMEWORK",
            f"Unsupported framework: {framework}",
            allowed=sorted(FRAMEWORK_CONTROLS.keys()),
        )

    if org_type is not None and not str(org_type).strip():
        return err("INVALID_ORG_TYPE", "org_type cannot be empty")

    return ok({"framework": fw, "org_type": org_type or "saas"})


def get_control_metadata(framework: str) -> dict:
    key = framework.strip().lower()
    if key not in FRAMEWORK_CONTROLS:
        return err(
            "INVALID_FRAMEWORK",
            f"Unsupported framework: {framework}",
            allowed=sorted(FRAMEWORK_CONTROLS.keys()),
        )

    return ok(
        {
            "framework": key,
            "metadata": CONTROL_METADATA.get(key, {}),
            "count": len(CONTROL_METADATA.get(key, {})),
        }
    )
