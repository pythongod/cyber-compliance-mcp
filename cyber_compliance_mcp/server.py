from __future__ import annotations

from typing import Dict, List
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("cyber-compliance-mcp")

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


@mcp.tool()
def get_framework_overview(framework: str) -> dict:
    """Return controls overview for a framework.

    Supported: nist_csf, iso27001, soc2, cis_v8
    """
    key = framework.strip().lower()
    controls = FRAMEWORK_CONTROLS.get(key)
    if not controls:
        return {
            "error": "Unsupported framework",
            "supported": sorted(FRAMEWORK_CONTROLS.keys()),
        }
    return {
        "framework": key,
        "control_count": len(controls),
        "controls": controls,
    }


@mcp.tool()
def generate_checklist(framework: str, org_type: str = "saas") -> dict:
    """Generate a practical compliance checklist for the selected framework."""
    key = framework.strip().lower()
    controls = FRAMEWORK_CONTROLS.get(key)
    if not controls:
        return {
            "error": "Unsupported framework",
            "supported": sorted(FRAMEWORK_CONTROLS.keys()),
        }

    checklist = [
        {
            "control": c,
            "status": "not_started",
            "owner": "security",
            "evidence": [],
            "notes": f"Required for {org_type} environment",
        }
        for c in controls
    ]

    return {
        "framework": key,
        "org_type": org_type,
        "checklist": checklist,
    }


@mcp.tool()
def calculate_risk_score(controls: List[dict]) -> dict:
    """Calculate risk score from control status list.

    Expected each item: {"control": str, "status": "implemented|partial|missing"}
    """
    weights = {"implemented": 0, "partial": 5, "missing": 10}

    if not controls:
        return {"risk_score": 0, "risk_level": "low", "summary": "No controls provided"}

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

    return {
        "risk_score": round(pct, 2),
        "risk_level": level,
        "controls_total": len(controls),
        "missing": missing,
        "partial": partial,
        "implemented": len(controls) - missing - partial,
    }


@mcp.tool()
def recommend_next_actions(framework: str, gaps: List[str]) -> dict:
    """Recommend next actions based on identified control gaps."""
    framework = framework.lower().strip()
    actions = []
    for gap in gaps:
        g = gap.lower()
        if "asset" in g or "inventory" in g:
            actions.append("Implement automated asset discovery and CMDB sync")
        elif "access" in g or "identity" in g:
            actions.append("Enable SSO + MFA everywhere and review privileged access")
        elif "log" in g or "monitor" in g:
            actions.append("Centralize logs in SIEM with 90+ day retention")
        elif "incident" in g:
            actions.append("Run incident response tabletop exercises quarterly")
        else:
            actions.append(f"Define remediation owner and evidence plan for: {gap}")

    return {
        "framework": framework,
        "gaps": gaps,
        "recommended_actions": actions,
        "priority": "Start with high-impact missing controls and evidence collection",
    }


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
