# Phase 5 — Enterprise Security & Governance

Phase 5 hardens the platform for enterprise-style operation.

## Capabilities
- API-key authentication enabled by default
- Admin / analyst / auditor roles
- Persistent API audit trail
- Policy-as-code registry
- Scheduled assessment registry with cron expressions
- Security & Governance UI
- Environment-based secrets/configuration
- Existing Redis worker and vendor-adapter architecture retained

## Endpoints
- `GET /api/auth/me`
- `GET /api/platform/audit`
- `GET /api/platform/policies`
- `POST /api/platform/policies` (admin)
- `GET /api/platform/schedules`
- `POST /api/platform/schedules` (admin)

## Production checklist
1. Replace all example API keys.
2. Put the API behind TLS and an identity-aware gateway.
3. Store keys in a secrets manager rather than `.env`.
4. Restrict CORS to the deployed frontend origin.
5. Run PostgreSQL and Redis on private networks.
6. Connect the persisted schedule registry to the Redis worker/controller.
7. Forward audit logs to SIEM for immutable retention.
8. Add OIDC/JWT at the gateway for enterprise SSO.
