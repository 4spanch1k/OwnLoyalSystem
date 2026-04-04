# Pilot Validation Report

## 1. Summary

**Checkpoint:** `07cfa18`  
**Validation date:** `2026-04-04`  
**Validated by:** `Codex`  
**Target status:** `pilot-ready checkpoint confirmed`  
**Current status:** `pilot validation package ready, pending environment execution`

**One-line result:**  
`Environment pass was attempted strictly by checklist order and is currently blocked by infrastructure, not by product code: local backend tests and frontend build are green, but migrations cannot run in this environment and remote GitHub Actions are still blocked by account billing.`

## 2. Scope of validation

This pass attempted only:

- database migration validation
- seed execution on a clean database
- runbook walkthrough readiness
- remote GitHub Actions recheck
- local baseline verification

What was not in scope:

- new product slices
- reconciliation
- performance or load testing
- security review
- production deployment

## 3. Environment

**OS / machine:** `Local macOS workspace`  
**Python:** `python3 (Homebrew Python 3.14 in current workspace)`  
**Node / npm:** `local Vite workspace toolchain`  
**Database:** `target runtime database not available in a validated local environment during this pass`  
**Backend env:** `DATABASE_URL / AZAMAT_DATABASE_URL supported by backend config; clean migrated DB still unavailable here`  
**Frontend env:** `VITE_LOYALTY_TENANT_ID=tenant-manual-adjustment`, `VITE_LOYALTY_PATIENT_ID=patient-manual-adjustment`, `VITE_LOYALTY_ACTOR_USER_ID=user-clinic-manager`, `VITE_LOYALTY_OPERATOR_ROLE=clinic_manager`

**Canonical dataset source:**

- `engineering/loyalty-pilot-demo-data-pack.md`
- `backend/scripts/seed_loyalty_demo.py`

## 4. Commands executed

### 4.1 Database migration

```bash
alembic -c backend/alembic.ini upgrade head
```

**Result:** `BLOCKED`  
**Notes:** `The current environment does not have alembic or psycopg available. Direct checks for import/runtime failed, and installing backend requirements failed because package downloads are not available in this environment.`

### 4.2 Demo seed

```bash
python3 backend/scripts/seed_loyalty_demo.py
```

**Result:** `BLOCKED`  
**Notes:** `This step depends on a clean migrated database from step 1. Because migrations could not be run here, seed execution on a checklist-compliant clean database could not be honestly validated.`

### 4.3 Backend tests

```bash
python3 -m unittest discover -s backend/tests
```

**Result:** `PASS`  
**Notes:** `36 tests passed locally on 2026-04-04. This confirms the code baseline remains green.`

### 4.4 Frontend build

```bash
npm run build
```

**Result:** `PASS`  
**Notes:** `Production frontend build completed successfully in the local workspace on 2026-04-04.`

### 4.5 Runbook demo walkthrough

**Runbook:** `engineering/frontend-loyalty-demo-runbook.md`  
**Result:** `BLOCKED`  
**Notes:** `Without a clean migrated database and seeded canonical dataset, the end-to-end walkthrough cannot be confirmed honestly in this environment.`

### 4.6 GitHub Actions

Jobs checked:

- `frontend-build`
- `backend-contracts`
- `backend-migrations`

**Result:** `BLOCKED`  
**Notes:** `GitHub API confirms the workflow run for commit 07cfa18 exists, but jobs are not starting because the account is locked by a billing issue. The latest checked run was 23979053114 on 2026-04-04.`

## 5. Validation results by area

### 5.1 Database and migrations

- `alembic upgrade head`: `blocked by environment`
- schema matches current backend core: `yes, by local code/tests baseline`
- seed on a clean migrated DB is possible: `expected yes, still blocked in this environment`

### 5.2 Canonical dataset

- tenant contract exists in seed script: `yes`
- patient contract exists in seed script: `yes`
- operator users contract exists in seed script: `yes`
- active policy contract exists in seed script: `yes`
- wallet contract exists in seed script: `yes`
- payment contract exists in seed script: `yes`
- seeded accrual ledger contract exists in seed script: `yes`
- repeated seed avoids duplicates: `yes, covered by local tests`

### 5.3 Backend loyalty core

Confirmed by local baseline:

- accrual: `yes`
- redemption: `yes`
- refund rollback: `yes`
- manual adjustment: `yes`

### 5.4 Frontend integration

Confirmed by implementation + local build baseline:

- wallet is rendered from backend contract: `yes`
- ledger is rendered from backend contract: `yes`
- manual adjustment is visible only for allowed role: `yes`
- successful submit is wired for real refetch: `yes`

## 6. Demo walkthrough result

### Scenario A — patient wallet and ledger visible

**Expected:**  
Patient sees real balance, ledger rows, and reason labels from backend data.

**Actual:**  
`Implementation is present and local build is green, but the clean-environment walkthrough is blocked until migrations and seed can run.`

**Status:** `BLOCKED`

### Scenario B — manual adjustment by clinic_manager

**Expected:**  
`clinic_manager` can submit a manual adjustment and wallet/ledger are updated through refetch.

**Actual:**  
`Frontend/backend flow is implemented and test-backed, but clean-environment execution is blocked until the canonical DB is prepared.`

**Status:** `BLOCKED`

### Scenario C — role gate

**Expected:**  
`doctor` does not see write action and remains read-only.

**Actual:**  
`Role gate is implemented and build-validated locally. Visual walkthrough in the target environment is still blocked by the missing migrated dataset.`

**Status:** `BLOCKED`

## 7. Known blockers and deviations

### External blockers

- `No alembic runtime available in the current environment`
- `No psycopg runtime available in the current environment`
- `Package installation blocked by lack of network access in the current environment`
- `GitHub Actions billing lock`

### Internal issues found

- `none in local baseline validation`

### Deviations from expected flow

- `Environment checklist could not proceed past step 1 because the required runtime dependencies are unavailable here`

## 8. Final status

**Overall result:** `PENDING ENVIRONMENT EXECUTION`

**Reason:**  
`The code baseline remains healthy: backend tests and frontend build pass locally, the seed contract exists, and the runbook/dataset/docs are aligned. The checklist could not be completed because environment prerequisites for migrations are missing here and remote CI jobs are blocked by billing.`

## 9. Required follow-up actions

1. `Prepare an environment with alembic, psycopg, and an accessible database.`
2. `Run alembic -c backend/alembic.ini upgrade head in that environment.`
3. `Run python3 backend/scripts/seed_loyalty_demo.py against the clean migrated database.`
4. `Walk through engineering/frontend-loyalty-demo-runbook.md end-to-end.`
5. `Re-run frontend-build, backend-contracts, and backend-migrations after GitHub billing is restored.`

## 10. Sign-off

**Validated commit:** `07cfa18`  
**Recommended checkpoint label:** `pilot validation package ready, pending environment execution`  
**Approved for controlled pilot demo:** `not yet`

## Short Summary

```md
Pilot validation summary

Commit: 07cfa18
Date: 2026-04-04
Result: PENDING ENVIRONMENT EXECUTION

Validated:
- alembic upgrade head: BLOCKED
- demo seed script: BLOCKED
- backend tests: PASS
- frontend build: PASS
- runbook walkthrough: BLOCKED
- GitHub Actions: BLOCKED

Confirmed:
- code is not the cause of the current blocker
- backend tests remain green
- frontend build remains green
- canonical dataset, runbook, and seed contract remain aligned

Blockers:
- no local alembic runtime
- no local psycopg runtime
- no network to install backend requirements
- GitHub Actions billing lock

Next actions:
- prepare an environment with alembic, psycopg, and a reachable DB
- rerun the checklist from step 1 without reordering
- finalize the validation report after environment execution
```
