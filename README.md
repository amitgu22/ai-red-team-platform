# AI Red Team Platform — Phase 2.1

Phase 2.1 turns the Phase 2 POC into a usable campaign-building flow:

**Target → Scenarios → Strategy → Providers → Campaign → Parallel execution → Normalized test runs**

### Included
- Provider registry for Promptfoo, PyRIT, Garak and Striker.
- Authorized sample target registry.
- Scenario library with prompt-injection, data-leakage, agent/tool-abuse and jailbreak coverage.
- Execution strategies: Baseline, Fast Scan, Maximum Coverage and Deep Adaptive.
- Visual Test Configuration builder: target, providers, scenarios, strategy and attempts.
- Campaign launch through FastAPI background execution so the UI remains responsive.
- Parallel provider/scenario fan-out when the selected strategy enables it.
- Normalized `TestRun` records with provider, scenario, attempt, status, severity, request, response and evidence.
- Campaign polling and run-detail view in the UI.
- Safe local demo execution: the POC only calls the configured sample target endpoint.
- Startup migration for the Phase 2.1 `test_runs.attempt` field when an existing PostgreSQL volume is reused.

## Run

```bash
docker compose up --build
```

Open http://localhost:3000

## Phase 2 workflow

1. Open **Test Configurations**.
2. Select the authorized target.
3. Select one or more providers.
4. Select one or more attack scenarios.
5. Select an execution strategy and number of attempts.
6. Save the configuration.
7. Open **Campaigns** and launch it.
8. Watch progress and inspect normalized runs.

## API highlights

- `GET /api/providers`
- `GET /api/targets`
- `GET /api/scenarios`
- `GET /api/strategies`
- `GET /api/test-configurations`
- `POST /api/test-configurations`
- `GET /api/campaigns`
- `POST /api/campaigns`
- `POST /api/campaigns/{id}/start`
- `GET /api/campaigns/{id}/runs`

## Next phase

Phase 3 will connect normalized runs to **findings, risk scoring, MITRE ATLAS mapping, recommendations and audit-ready reports**. Real vendor adapters should only be enabled for targets the operator is authorized to assess.

## GitHub

```bash
git add .
git commit -m "Complete Phase 2.1 campaign builder and parallel orchestration"
git push
```
