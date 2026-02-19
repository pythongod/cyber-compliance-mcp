# TODO (Updated)

## P0 — Next

1. Expand recommendations engine with **severity + effort scoring**.
2. Publish package to **PyPI** with signed release workflow.
3. Add deployment docs/examples for auth + rate-limit environment settings.
4. Add persistence backend abstraction (swap JSON file backend with DB adapter).

## P1 — Reliability

5. Add migration/versioning for persisted assessment records.
6. Add configurable storage path + lock-safe concurrent writes.
7. Add fuller request audit logs (tool args summary, latency, result status).
8. Add crosswalk expansion for additional topics and framework references.

## P2 — Platform

9. Add policy-driven authorization scopes per tool.
10. Add observability hooks (metrics endpoint / Prometheus-style counters).
