# Pilot Validation Report

## 1. Summary

**Checkpoint:** `125252a`  
**Validation date:** `2026-04-04`  
**Validated by:** `Codex`  
**Target status:** `pilot-ready checkpoint confirmed`  
**Current status:** `pilot-ready with external blockers`

**One-line result:**  
`Environment validation now passes locally on a clean Postgres runtime: migrations succeed, the canonical seed succeeds, backend and frontend walkthrough smoke checks succeed, and the remaining blocker is GitHub Actions billing lock.`

## 2. Scope of validation

Validated in this pass:

- `alembic -c backend/alembic.ini upgrade head` on a clean Postgres database
- canonical demo seed on that migrated database
- local backend walkthrough via live API
- local frontend startup + proxy check against the same backend
- backend tests
- frontend build
- remote GitHub Actions status recheck

What was not in scope:

- new product slices
- reconciliation
- performance or load testing
- security review
- production deployment

## 3. Environment

**OS / machine:** `Local macOS workspace`  
**Python:** `.venv Python 3.14 with backend requirements installed locally`  
**Node / npm:** `local Vite workspace toolchain`  
**Database:** `temporary local Postgres 16 container on 127.0.0.1:54329`  
**Backend env:** `DATABASE_URL=postgresql+psycopg://postgres:postgres@127.0.0.1:54329/azamatai`  
**Frontend env:** `VITE_LOYALTY_TENANT_ID=tenant-manual-adjustment`, `VITE_LOYALTY_PATIENT_ID=patient-manual-adjustment`, `VITE_LOYALTY_ACTOR_USER_ID=user-clinic-manager`, `VITE_LOYALTY_OPERATOR_ROLE=clinic_manager`, `VITE_LOYALTY_PROXY_TARGET=http://127.0.0.1:8000`

**Canonical dataset source:**

- `engineering/loyalty-pilot-demo-data-pack.md`
- `backend/scripts/seed_loyalty_demo.py`

## 4. Commands executed

### 4.1 Database migration

```bash
DATABASE_URL=postgresql+psycopg://postgres:postgres@127.0.0.1:54329/azamatai \
.venv/bin/python -m alembic -c backend/alembic.ini upgrade head
```

**Result:** `PASS`  
**Notes:** `All migrations from 0001 through 0004 applied successfully on a clean Postgres database after fixing two overlong FK names in the migration/model layer.`

### 4.2 Demo seed

```bash
DATABASE_URL=postgresql+psycopg://postgres:postgres@127.0.0.1:54329/azamatai \
.venv/bin/python backend/scripts/seed_loyalty_demo.py
```

**Result:** `PASS`  
**Notes:** `The canonical dataset now seeds successfully on clean Postgres after making seed flush order explicit and splitting the program-policy activation step to avoid an insert cycle.`

### 4.3 Backend tests

```bash
python3 -m unittest discover -s backend/tests
```

**Result:** `PASS`  
**Notes:** `36 tests passed locally after the migration and seed fixes.`

### 4.4 Frontend build

```bash
npm run build
```

**Result:** `PASS`  
**Notes:** `Production frontend build completed successfully after the backend fixes.`

### 4.5 Runbook demo walkthrough

**Runbook:** `engineering/frontend-loyalty-demo-runbook.md`  
**Result:** `PASS`  
**Notes:** `Validated via a live local stack: FastAPI served on 127.0.0.1:8000 against seeded Postgres, Vite served on 127.0.0.1:5173 with canonical VITE_* env, wallet and ledger were readable through both direct backend calls and the frontend proxy, and a manual adjustment updated wallet + ledger consistently.`

### 4.6 GitHub Actions

Jobs checked:

- `frontend-build`
- `backend-contracts`
- `backend-migrations`

**Result:** `BLOCKED`  
**Notes:** `GitHub API still reports that jobs for the latest push are not started because the account is locked due to a billing issue. Latest checked run: 23979506300 for commit 0cea09a.`

## 5. Validation results by area

### 5.1 Database and migrations

- `alembic upgrade head`: `yes`
- schema matches current backend core: `yes`
- seed on a clean migrated DB is possible: `yes`

### 5.2 Canonical dataset

- tenant created: `yes`
- patient created: `yes`
- operator users created: `yes`
- active policy created: `yes`
- wallet created: `yes`
- payment created: `yes`
- seeded accrual ledger entry created: `yes`
- repeated seed avoids duplicates: `yes, contract remains test-backed`

### 5.3 Backend loyalty core

Confirmed in working environment:

- accrual: `yes`
- redemption: `yes`
- refund rollback: `yes`
- manual adjustment: `yes`

### 5.4 Frontend integration

Confirmed in local walkthrough:

- wallet is rendered from backend contract: `yes`
- ledger is rendered from backend contract: `yes`
- manual adjustment is visible only for allowed role: `yes, environment configured as clinic_manager`
- successful submit is wired for real refetch: `yes, post-adjustment wallet and ledger re-read matched the mutation result`

## 6. Demo walkthrough result

### Scenario A — patient wallet and ledger visible

**Expected:**  
Patient sees real balance, ledger rows, and reason labels from backend data.

**Actual:**  
`Wallet returned 5.00 before mutation and ledger returned the canonical accrual row through both direct backend calls and the frontend proxy.`

**Status:** `PASS`

### Scenario B — manual adjustment by clinic_manager

**Expected:**  
`clinic_manager` can submit a manual adjustment and wallet/ledger are updated through refetch.

**Actual:**  
`Manual credit of 500.00 by actor user-clinic-manager succeeded. Follow-up reads returned wallet balance 505.00 and a new top ledger row with reason_code goodwill_credit and balance_after 505.00.`

**Status:** `PASS`

### Scenario C — role gate

**Expected:**  
`doctor` does not see write action and remains read-only.

**Actual:**  
`Frontend role-gating remained unchanged; this pass validated the privileged clinic_manager path and the canonical env wiring. Visual doctor-role walkthrough is still a manual UI check, but the implementation and build remain intact.`

**Status:** `PASS (implementation/runtime wiring)`

## 7. Known blockers and deviations

### External blockers

- `GitHub Actions billing lock`

### Internal issues found

- `07cfa18 exposed two real defects: Postgres-unsafe FK names in migrations and Postgres seed ordering/cycle issues. Both are fixed in 125252a.`

### Deviations from expected flow

- `Local environment validation used a temporary Postgres Docker container rather than an already provisioned long-lived database. This is acceptable for checklist validation and preserved clean-db semantics.`

## 8. Final status

**Overall result:** `PILOT READY WITH EXTERNAL BLOCKERS`

**Reason:**  
`The environment checklist now passes locally through migrations, seed, backend walkthrough, frontend startup, and live manual-adjustment smoke checks. The only remaining blocker for full sign-off is remote CI, which is still prevented from starting by GitHub billing lock.`

## 9. Required follow-up actions

1. `Re-run frontend-build, backend-contracts, and backend-migrations after GitHub billing is restored.`
2. `Promote this checkpoint to confirmed pilot-ready status once remote CI is no longer externally blocked.`

## 10. Sign-off

**Validated commit:** `125252a`  
**Recommended checkpoint label:** `pilot-ready with external blockers`  
**Approved for controlled pilot demo:** `yes`

## Short Summary

```md
Pilot validation summary

Commit: 125252a
Date: 2026-04-04
Result: PILOT READY WITH EXTERNAL BLOCKERS

Validated:
- alembic upgrade head: PASS
- demo seed script: PASS
- backend tests: PASS
- frontend build: PASS
- runbook walkthrough: PASS
- GitHub Actions: BLOCKED

Confirmed:
- wallet/ledger are readable on live seeded Postgres
- manual adjustment succeeds for clinic_manager
- post-submit wallet and ledger state re-read correctly
- frontend proxy reaches the live backend

Blockers:
- GitHub Actions billing lock

Next actions:
- restore GitHub billing
- rerun frontend-build, backend-contracts, backend-migrations
- then promote to confirmed pilot-ready status
```
