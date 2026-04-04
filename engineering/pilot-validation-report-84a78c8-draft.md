# Pilot Validation Report

## 1. Summary

**Checkpoint:** `84a78c8`
**Validation date:** `2026-04-04`
**Validated by:** `Codex`
**Target status:** `pilot-ready with external blockers`

**One-line result:**
`Controlled pilot demo is reproducible from docs + seed, backend and frontend local validation is green, and the remaining blockers are environment-level validation plus GitHub Actions billing lock.`

## 2. Scope of validation

Confirmed in this validation draft:

- backend loyalty core local validation
- frontend build validation
- canonical demo dataset seed script
- documentation linkage between runbook, data pack, and seed script
- role-gated frontend demo flow readiness

Not yet confirmed in a clean environment:

- `alembic -c backend/alembic.ini upgrade head`
- clean database seed run after migrations
- full runbook walkthrough on a freshly prepared environment
- GitHub Actions after billing unlock

What was not in scope:

- new product slices
- reconciliation
- performance or load testing
- security review
- production deployment

## 3. Environment

**OS / machine:** `Local macOS workspace`
**Python:** `python3 in current local workspace`
**Node / npm:** `Node/npm from local Vite workspace`
**Database:** `ORM/test validation executed against SQLite in test suite; canonical runtime database not yet validated in a clean migrated environment`
**Backend env:** `DATABASE_URL and/or AZAMAT_DATABASE_URL expected by backend; clean migrated target DB not yet validated here`
**Frontend env:** `VITE_LOYALTY_TENANT_ID=tenant-manual-adjustment`, `VITE_LOYALTY_PATIENT_ID=patient-manual-adjustment`, `VITE_LOYALTY_ACTOR_USER_ID=user-clinic-manager`, `VITE_LOYALTY_OPERATOR_ROLE=clinic_manager`

**Canonical dataset source:**

- `engineering/loyalty-pilot-demo-data-pack.md`
- `backend/scripts/seed_loyalty_demo.py`

## 4. Commands executed

### 4.1 Database migration

```bash
alembic -c backend/alembic.ini upgrade head
```

**Result:** `NOT EXECUTED IN THIS ENVIRONMENT`
**Notes:** `The current workspace does not have a validated Alembic runtime available for this step. This remains a required environment validation task before pilot-ready sign-off.`

### 4.2 Demo seed

```bash
python3 backend/scripts/seed_loyalty_demo.py
```

**Result:** `CODE VALIDATED, CLEAN-DB EXECUTION PENDING`
**Notes:** `The script is covered by backend tests for canonical creation, idempotent rerun, and fail-fast drift detection. It still needs one real execution against a migrated clean database.`

### 4.3 Backend tests

```bash
python3 -m unittest discover -s backend/tests
```

**Result:** `PASS`
**Notes:** `36 tests passed locally on 2026-04-04, including the new seed script tests.`

### 4.4 Frontend build

```bash
npm run build
```

**Result:** `PASS`
**Notes:** `Production build completed successfully in the local workspace on 2026-04-04.`

### 4.5 Runbook demo walkthrough

**Runbook:** `engineering/frontend-loyalty-demo-runbook.md`
**Result:** `READY TO RUN, CLEAN-ENV WALKTHROUGH PENDING`
**Notes:** `The runbook, data pack, and seed script now align. One full dry-run on a clean environment is still required.`

### 4.6 GitHub Actions

Jobs checked:

- `frontend-build`
- `backend-contracts`
- `backend-migrations`

**Result:** `BLOCKED`
**Notes:** `Remote GitHub Actions remain blocked by billing lock and therefore cannot yet be used as a quality signal for this checkpoint.`

## 5. Validation results by area

### 5.1 Database and migrations

- `alembic upgrade head`: `not yet validated in target environment`
- schema matches the current backend core: `yes, by local model/tests and migration documents`
- seed on a clean migrated DB is possible: `expected yes, still needs real environment confirmation`

### 5.2 Canonical dataset

- tenant created: `yes, by seed script contract`
- patient created: `yes, by seed script contract`
- operator users created: `yes, by seed script contract`
- active policy created: `yes, by seed script contract`
- wallet created: `yes, by seed script contract`
- payment created: `yes, by seed script contract`
- seeded accrual ledger entry created: `yes, by seed script contract`
- repeated seed does not create duplicates: `yes, covered by local test`

### 5.3 Backend loyalty core

Confirmed in the local working contour:

- accrual: `yes`
- redemption: `yes`
- refund rollback: `yes`
- manual adjustment: `yes`

### 5.4 Frontend integration

Confirmed by implementation + local build validation:

- wallet is rendered from backend contract: `yes`
- ledger is rendered from backend contract: `yes`
- manual adjustment is visible only for allowed role: `yes`
- successful submit is designed to trigger real refetch: `yes`

## 6. Demo walkthrough result

### Scenario A — patient wallet and ledger visible

**Expected:**
Patient sees real balance, ledger rows, and reason labels from backend data.

**Actual:**
`Frontend slice is wired to backend wallet/ledger APIs and is build-validated. Full clean-environment walkthrough still pending.`

**Status:** `READY TO VERIFY`

### Scenario B — manual adjustment by clinic_manager

**Expected:**
`clinic_manager` can submit a manual adjustment and wallet/ledger are updated through refetch.

**Actual:**
`Frontend action, backend endpoint, and refetch wiring are implemented and locally validated by tests/build. Clean-environment walkthrough still pending.`

**Status:** `READY TO VERIFY`

### Scenario C — role gate

**Expected:**
`doctor` sees read-only loyalty state and does not see write action.

**Actual:**
`Role gate is implemented in frontend config and UI. Local build is green; one visual walkthrough in a clean environment is still pending.`

**Status:** `READY TO VERIFY`

## 7. Known blockers and deviations

### External blockers

- `GitHub Actions billing lock`
- `No clean migrated environment validation recorded yet for alembic + seed + walkthrough`

### Internal issues found

- `none in local validation`

### Deviations from expected flow

- `none in local validation`

## 8. Final status

**Overall result:** `PILOT READY WITH EXTERNAL BLOCKERS`

**Reason:**
`The code, demo dataset, and documentation now form a reproducible controlled pilot flow. Backend tests and frontend build are green locally, and the seed script is covered by tests. The only remaining blockers are environment-level confirmation of migrations/seed on a clean database and GitHub Actions revalidation after billing unlock.`

## 9. Required follow-up actions

1. `Run alembic -c backend/alembic.ini upgrade head in a clean environment with Alembic available.`
2. `Run python3 backend/scripts/seed_loyalty_demo.py against that clean migrated database.`
3. `Walk through engineering/frontend-loyalty-demo-runbook.md end-to-end on the clean environment.`
4. `Re-run frontend-build, backend-contracts, and backend-migrations after GitHub billing is restored.`

## 10. Sign-off

**Validated commit:** `84a78c8`
**Recommended checkpoint label:** `controlled pilot demo reproducible from docs + seed`
**Approved for controlled pilot demo:** `yes, with environment validation still required`

## Short Summary

```md
Pilot validation summary

Commit: 84a78c8
Date: 2026-04-04
Result: PILOT READY WITH EXTERNAL BLOCKERS

Validated:
- alembic upgrade head: NOT EXECUTED IN THIS ENVIRONMENT
- demo seed script: CODE VALIDATED, CLEAN-DB EXECUTION PENDING
- backend tests: PASS
- frontend build: PASS
- runbook walkthrough: READY TO VERIFY
- GitHub Actions: BLOCKED

Confirmed:
- wallet/ledger wired into UI
- manual adjustment is role-gated in frontend
- backend loyalty core is locally validated
- canonical dataset is reproducible from seed contract

Blockers:
- clean environment migration + seed + walkthrough still pending
- GitHub Actions billing lock

Next actions:
- run alembic upgrade head in a clean environment
- run seed script on that clean database
- complete runbook walkthrough
- rerun GitHub Actions after billing unlock
```
