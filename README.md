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
- MCP tool interface for agent workflows

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
- `recommend_next_actions(framework, gaps)`

## License

MIT


## Persistence tools

New MCP tools for persisted assessments:

- `create_assessment(assessment_id, framework, org_type="saas")`
- `update_control_status(assessment_id, control, status)`
- `get_assessment(assessment_id)`
- `list_assessments()`

Data is stored in `assessments-db.json` in the working directory.


## Control metadata + validation

New capabilities:
- `get_control_metadata(framework)` for owner/priority/evidence hints
- Structured validation errors with `code/message/allowed` where applicable

Example error shape:

```json
{
  "error": {
    "code": "INVALID_FRAMEWORK",
    "message": "Unsupported framework: xyz",
    "allowed": ["cis_v8", "iso27001", "nist_csf", "soc2"]
  }
}
```


### Storage tool error contract

All storage CRUD tools now return structured errors:

```json
{
  "error": {
    "code": "INVALID_ASSESSMENT_ID",
    "message": "assessment_id cannot be empty"
  }
}
```

Common codes:
- `INVALID_ASSESSMENT_ID`
- `INVALID_FRAMEWORK`
- `INVALID_ORG_TYPE`
- `INVALID_CONTROL`
- `INVALID_STATUS`
- `ASSESSMENT_EXISTS`
- `ASSESSMENT_NOT_FOUND`


## Unified response contract

All tools now return a consistent envelope:

Success:
```json
{"ok": true, "...": "payload"}
```

Failure:
```json
{"ok": false, "error": {"code": "...", "message": "..."}}
```
