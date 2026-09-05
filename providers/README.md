# Provider plugins

Each red-team engine is isolated behind a provider adapter.

Required lifecycle:

1. `validate`
2. `health_check`
3. `execute`
4. `parse_results`
5. `normalize`

Phase 1 contains container skeletons. Phase 2 will connect real execution and normalized result handling.
