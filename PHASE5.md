# Phase 5 — Enterprise Platform Hardening

## Included
- API-key authentication with explicit roles: admin, analyst, auditor
- Role-protected governance operations
- Persistent audit trail for API activity
- Policy-as-code registry
- Assessment schedule registry (cron expression + enablement state)
- `/api/auth/me`, `/api/platform/audit`, `/api/platform/policies`, `/api/platform/schedules`
- Production-oriented environment configuration

## Security model
`X-API-Key` is required by default. Set `AUTH_REQUIRED=false` only for isolated local development.
Keys are configured through `REDTEAM_API_KEYS`; never commit production secrets.

## Example
```bash
curl -H 'X-API-Key: change-me' http://localhost:8000/api/auth/me
```

The scheduler registry deliberately stores schedules separately from execution. A production deployment can connect it to the Redis worker/cron controller without coupling scheduling to the API process.
