from __future__ import annotations

import logging
import time
from typing import Any, Callable, List

from mcp.server.fastmcp import FastMCP

from .core import (
    calculate_risk_score as _calculate_risk_score,
    generate_checklist as _generate_checklist,
    get_control_metadata as _get_control_metadata,
    get_framework_overview as _get_framework_overview,
    recommend_next_actions as _recommend_next_actions,
)
from .crosswalk import get_framework_crosswalk as _get_framework_crosswalk
from .security import request_context
from .policy import enforce_scope
from .metrics import as_prometheus, inc, observe_latency, snapshot
from .requirements import get_requirements as _get_requirements, list_requirement_frameworks as _list_requirement_frameworks
from .storage import (
    compact_storage as _compact_storage,
    create_assessment as _create_assessment,
    get_assessment as _get_assessment,
    list_assessments as _list_assessments,
    update_control_status as _update_control_status,
)

logger = logging.getLogger("cyber_compliance_mcp")
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

mcp = FastMCP("cyber-compliance-mcp")


def _run_tool(tool_name: str, fn: Callable[[], dict], *args: Any) -> dict:
    inc("requests.total")
    ctx = request_context(tool_name, *args)
    if ctx.get("ok") is False:
        inc("requests.blocked")
        logger.warning(
            "request_id=%s tool=%s status=blocked error_code=%s",
            ctx.get("error", {}).get("request_id", "-"),
            tool_name,
            ctx.get("error", {}).get("code", "UNKNOWN"),
        )
        return ctx

    policy = enforce_scope(tool_name)
    if policy is not None:
        inc("requests.forbidden")
        return policy

    request_id = ctx.get("request_id")
    t0 = time.perf_counter()
    result = fn()
    elapsed_ms = round((time.perf_counter() - t0) * 1000, 2)

    observe_latency(tool_name, elapsed_ms)
    status = "ok" if result.get("ok") else "error"
    err_code = result.get("error", {}).get("code", "-") if status == "error" else "-"
    inc(f"requests.{status}")
    logger.info(
        "request_id=%s tool=%s status=%s latency_ms=%s arg_chars=%s error_code=%s",
        request_id,
        tool_name,
        status,
        elapsed_ms,
        sum(len(str(a)) for a in args),
        err_code,
    )
    return result


@mcp.tool()
def get_framework_overview(framework: str) -> dict:
    return _run_tool("get_framework_overview", lambda: _get_framework_overview(framework), framework)


@mcp.tool()
def get_control_metadata(framework: str) -> dict:
    return _run_tool("get_control_metadata", lambda: _get_control_metadata(framework), framework)


@mcp.tool()
def generate_checklist(framework: str, org_type: str = "saas") -> dict:
    return _run_tool("generate_checklist", lambda: _generate_checklist(framework, org_type), framework, org_type)


@mcp.tool()
def calculate_risk_score(controls: List[dict]) -> dict:
    return _run_tool("calculate_risk_score", lambda: _calculate_risk_score(controls), controls)


@mcp.tool()
def recommend_next_actions(framework: str, gaps: List[str]) -> dict:
    return _run_tool("recommend_next_actions", lambda: _recommend_next_actions(framework, gaps), framework, gaps)


@mcp.tool()
def create_assessment(assessment_id: str, framework: str, org_type: str = "saas") -> dict:
    return _run_tool(
        "create_assessment",
        lambda: _create_assessment(assessment_id, framework, org_type),
        assessment_id,
        framework,
        org_type,
    )


@mcp.tool()
def update_control_status(assessment_id: str, control: str, status: str) -> dict:
    return _run_tool(
        "update_control_status",
        lambda: _update_control_status(assessment_id, control, status),
        assessment_id,
        control,
        status,
    )


@mcp.tool()
def get_assessment(assessment_id: str) -> dict:
    return _run_tool("get_assessment", lambda: _get_assessment(assessment_id), assessment_id)


@mcp.tool()
def list_assessments() -> dict:
    return _run_tool("list_assessments", lambda: _list_assessments())


@mcp.tool()
def get_framework_crosswalk(topic: str) -> dict:
    return _run_tool("get_framework_crosswalk", lambda: _get_framework_crosswalk(topic), topic)


@mcp.tool()
def get_metrics() -> dict:
    """Return in-memory service metrics snapshot."""
    return _run_tool("get_metrics", lambda: {"ok": True, **snapshot()})


@mcp.tool()
def get_metrics_prometheus() -> dict:
    """Return Prometheus-format metrics text in `text` field."""
    return _run_tool("get_metrics_prometheus", lambda: {"ok": True, "text": as_prometheus()})


@mcp.tool()
def compact_storage() -> dict:
    """Compact/cleanup storage backend files."""
    return _run_tool("compact_storage", lambda: _compact_storage())


@mcp.tool()
def list_requirement_frameworks() -> dict:
    return _run_tool("list_requirement_frameworks", lambda: _list_requirement_frameworks())


@mcp.tool()
def get_requirements(framework: str, query: str = "") -> dict:
    return _run_tool("get_requirements", lambda: _get_requirements(framework, query), framework, query)


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
