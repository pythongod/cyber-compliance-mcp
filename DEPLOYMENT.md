# Deployment Guide

## Security controls

Set these environment variables for non-local deployment:

- `CYBER_MCP_AUTH_REQUIRED=true`
- `CYBER_MCP_API_TOKEN=<strong-secret>`
- `CYBER_MCP_CLIENT_TOKEN=<client-token>`
- `CYBER_MCP_RATE_LIMIT=60`
- `CYBER_MCP_RATE_WINDOW_SEC=60`
- `CYBER_MCP_MAX_CHARS=12000`
- `CYBER_MCP_BACKEND=json|sqlite`
- `CYBER_MCP_DB_PATH=/var/lib/cyber-mcp/assessments-db.json` (or `.db` for sqlite)
- `CYBER_MCP_POLICY_PROFILE=dev|staging|prod`

## Example

```bash
export CYBER_MCP_AUTH_REQUIRED=true
export CYBER_MCP_API_TOKEN='replace-me'
export CYBER_MCP_CLIENT_TOKEN='replace-me'
export CYBER_MCP_RATE_LIMIT=120
export CYBER_MCP_RATE_WINDOW_SEC=60
export CYBER_MCP_MAX_CHARS=20000
export CYBER_MCP_DB_PATH='./assessments-db.json'

cyber-compliance-mcp
```

## Notes

- When auth is enabled, missing/invalid client token returns `UNAUTHORIZED`.
- Rate limiting is per-tool and returns `RATE_LIMITED` with retry hints.
- Request size guards return `REQUEST_TOO_LARGE`.
- Storage uses advisory lock files (`*.lock`) for safer concurrent writes.
- Persistence format includes `schema_version` for migration readiness.
