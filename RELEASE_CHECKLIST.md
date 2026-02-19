# Release Checklist (MCP)

## One-time GitHub/PyPI setup

1. Create PyPI project: `cyber-compliance-mcp`.
2. In GitHub repo settings, create environment: `pypi`.
3. Restrict environment to tags matching `v*.*.*`.
4. In PyPI trusted publishing, add this GitHub repo/workflow:
   - workflow: `.github/workflows/publish-pypi.yml`
   - environment: `pypi`

## Per-release flow

1. Run tests:
   ```bash
   pytest -q
   ```
2. Bump version in `pyproject.toml`.
3. Update changelog/release notes.
4. Commit + push.
5. Tag + push tag:
   ```bash
   git tag vX.Y.Z
   git push origin vX.Y.Z
   ```
6. Verify publish workflow + signed artifacts.

## Security checks before tagging

- Confirm `CYBER_MCP_AUTH_REQUIRED` behavior is tested
- Confirm rate limit and request size guards
- Confirm policy scope enforcement behavior
