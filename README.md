# AI Red Team Platform — Phase 2.3

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

## Phase 2.2 — Vendor Adapter Framework

Phase 2.2 introduces a common vendor adapter contract so the orchestrator is vendor-neutral.

### Adapter lifecycle

`discover → validate → execute → normalize`

Built-in adapters currently cover Promptfoo, PyRIT, Garak and Striker. The POC adapters execute the configured target HTTP surface while preserving a vendor-specific boundary; replacing an adapter with a real CLI/API integration does not require changing the campaign orchestrator.

### Vendor API

- `GET /api/vendors` — discover registered adapters and capabilities
- `GET /api/vendors/{name}/validate?scenario_category=...` — validate scenario/vendor compatibility

### Onboarding a new vendor

1. Implement `VendorAdapter` in `backend/app/adapters/`.
2. Define capabilities and execution modes.
3. Register the adapter in `registry.py`.
4. Add adapter tests.
5. No orchestrator changes are required.

This is the foundation for Phase 2.3: real provider execution, retry policies, timeouts, artifact capture, and queue-backed workers.

## Phase 2.3 — Real Execution Layer

Phase 2.3 replaces API background execution with a Redis-backed campaign queue and worker execution model.

### Execution architecture

`API → Redis Queue → Worker → Campaign Engine → Vendor Adapter → Target → Normalized TestRun`

### Real vendor CLI integration

Each built-in adapter supports an optional command template through environment variables:

- `PROMPTFOO_COMMAND`
- `PYRIT_COMMAND`
- `GARAK_COMMAND`
- `STRIKER_COMMAND`

Templates support `{prompt_file}`, `{target}`, `{scenario}`, `{attempt}` and `{output_file}`. The prompt is written to an artifact file rather than placed directly in the process command line.

If a command is not configured, the local HTTP fallback remains available for the sample target, making the demo runnable without installing external security tools.

### Reliability controls

- Redis queue decouples API requests from execution.
- Worker process supports graceful shutdown.
- Per-test timeout.
- Bounded retries for failed/time-out executions.
- Per-run artifact directory under `/artifacts/<campaign>/<test-run>`.
- Vendor stdout/stderr capture and optional JSON output capture.
- Normalized result contract remains unchanged for downstream findings/reporting.

### Example command template

Set a vendor command in `.env` according to the CLI/API version installed in your worker image. For example, a wrapper script can accept the platform placeholders and invoke the exact vendor CLI syntax required by your environment.

The platform deliberately does not hard-code a single vendor CLI version because Promptfoo, PyRIT, Garak and Striker installation/CLI interfaces can vary by release.


### Phase history
- Phase 2.1 — campaign builder and parallel orchestration
- Phase 2.2 — vendor-neutral adapter contract
- Phase 2.3 — real CLI execution boundary, Redis queue, worker execution, retries, timeouts and artifacts

## Phase 4 — Governance, Coverage & Reporting

Phase 4 adds an enterprise governance layer: risk register, remediation ownership/status, attack coverage, campaign risk trends, CSV export, and PDF executive reports.

### Governance APIs
- `GET /api/governance/risk-register`
- `PUT /api/governance/risk-register/{finding_id}`
- `GET /api/governance/coverage`
- `GET /api/governance/trends`
- `GET /api/governance/export.csv`
- `GET /api/export/campaign/{campaign_id}.pdf`

The UI now includes **Risk Register**, **Coverage**, and **Trends** pages.
