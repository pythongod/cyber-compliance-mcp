from __future__ import annotations

from typing import List

from mcp.server.fastmcp import FastMCP

from .core import (
    calculate_risk_score as _calculate_risk_score,
    generate_checklist as _generate_checklist,
    get_framework_overview as _get_framework_overview,
    get_control_metadata as _get_control_metadata,
    recommend_next_actions as _recommend_next_actions,
)
from .storage import (
    create_assessment as _create_assessment,
    get_assessment as _get_assessment,
    list_assessments as _list_assessments,
    update_control_status as _update_control_status,
)

mcp = FastMCP("cyber-compliance-mcp")


@mcp.tool()
def get_framework_overview(framework: str) -> dict:
    """Return controls overview for a framework.

    Supported: nist_csf, iso27001, soc2, cis_v8
    """
    return _get_framework_overview(framework)


@mcp.tool()
def get_control_metadata(framework: str) -> dict:
    """Return owner/priority/evidence metadata for controls in a framework."""
    return _get_control_metadata(framework)


@mcp.tool()
def generate_checklist(framework: str, org_type: str = "saas") -> dict:
    """Generate a practical compliance checklist for the selected framework."""
    return _generate_checklist(framework, org_type)


@mcp.tool()
def calculate_risk_score(controls: List[dict]) -> dict:
    """Calculate risk score from control status list.

    Expected each item: {"control": str, "status": "implemented|partial|missing"}
    """
    return _calculate_risk_score(controls)


@mcp.tool()
def recommend_next_actions(framework: str, gaps: List[str]) -> dict:
    """Recommend next actions based on identified control gaps."""
    return _recommend_next_actions(framework, gaps)


@mcp.tool()
def create_assessment(assessment_id: str, framework: str, org_type: str = "saas") -> dict:
    """Create a persisted assessment record."""
    return _create_assessment(assessment_id, framework, org_type)


@mcp.tool()
def update_control_status(assessment_id: str, control: str, status: str) -> dict:
    """Update control status in persisted assessment."""
    return _update_control_status(assessment_id, control, status)


@mcp.tool()
def get_assessment(assessment_id: str) -> dict:
    """Get a persisted assessment by id."""
    return _get_assessment(assessment_id)


@mcp.tool()
def list_assessments() -> dict:
    """List persisted assessments."""
    return _list_assessments()


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
