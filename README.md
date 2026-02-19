# cyber-compliance-mcp

A cybersecurity compliance MCP server that provides practical compliance tools for:

- NIST CSF 2.0
- ISO 27001:2022
- SOC 2
- CIS Controls v8

## Features

- Compliance checklist generation
- Risk scoring by control status
- Framework mapping helpers
- Recommendation engine with severity/effort scoring
- MCP tool interface for agent workflows
- Pluggable persistence backend (JSON backend included)

## Quickstart

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
cyber-compliance-mcp
```

## Example Tools

- `get_framework_overview(framework)`
- `generate_checklist(framework, org_type)`
- `calculate_risk_score(controls)`
- `recommend_next_actions(framework, gaps)` (returns scored + ordered recommendations)
- `create_assessment(assessment_id, framework, org_type="saas")`
- `update_control_status(assessment_id, control, status)`
- `get_assessment(assessment_id)`
- `list_assessments()`
- `get_framework_crosswalk(topic)`

## Persistence tools

Data is stored in `assessments-db.json` in the working directory by default.
Override with:

```bash
export CYBER_MCP_DB_PATH=/path/to/assessments-db.json
```

## Control metadata + validation

New capabilities:
- `get_control_metadata(framework)` for owner/priority/evidence hints
- Structured validation errors with `code/message/allowed` where applicable

Example error shape:

```json
{
  "ok": false,
  "error": {
    "code": "INVALID_FRAMEWORK",
    "message": "Unsupported framework: xyz",
    "allowed": ["cis_v8", "iso27001", "nist_csf", "soc2"]
  }
}
```

## Security and operations controls

Environment flags:
- `CYBER_MCP_AUTH_REQUIRED=true|false`
- `CYBER_MCP_API_TOKEN=<server token>`
- `CYBER_MCP_CLIENT_TOKEN=<client token>`
- `CYBER_MCP_RATE_LIMIT=60`
- `CYBER_MCP_RATE_WINDOW_SEC=60`
- `CYBER_MCP_MAX_CHARS=12000`
- `CYBER_MCP_DB_PATH=/var/lib/cyber-mcp/assessments-db.json`

Added:
- request auth guard (token pattern)
- per-tool rate limiting
- request size limit
- structured logs with `request_id`
- `get_framework_crosswalk(topic)` MCP tool

## Unified response contract

All tools return a consistent envelope:

Success:
```json
{"ok": true, "...": "payload"}
```

Failure:
```json
{"ok": false, "error": {"code": "...", "message": "..."}}
```

## Deployment

See `DEPLOYMENT.md` for secure non-local deployment settings (auth, rate limits, request size, DB path).

## License

MIT
