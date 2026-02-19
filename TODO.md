# TODO (Prioritized Next 10)

## P0 — Immediate

1. Add **framework control metadata** (owner suggestions, evidence examples, priority tags).
2. Add **assessment persistence layer** (JSON file backend first, DB later).
3. Add MCP tools for CRUD:
   - `create_assessment`
   - `update_control_status`
   - `get_assessment`
   - `list_assessments`
4. Add input validation with clear typed errors for all tool arguments.

## P1 — Security + Ops

5. Add **auth guard / API token** pattern for non-local deployment.
6. Add **rate limiting** and request-size limits.
7. Add structured logging and request correlation IDs.

## P2 — Ecosystem

8. Add framework crosswalk endpoint (e.g., NIST ↔ ISO ↔ SOC2 ↔ CIS mapping hints).
9. Expand recommendations engine with severity + effort scoring.
10. Publish to **PyPI** with signed release workflow.
