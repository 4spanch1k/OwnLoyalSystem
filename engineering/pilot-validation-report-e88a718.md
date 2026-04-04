# Pilot Validation Report

## 1. Summary

**Checkpoint:** `e88a718`  
**Validation date:** `2026-04-05`  
**Validated by:** `Codex`  
**Target status:** `pilot-ready for controlled demo; locally validated on native Postgres; remote GitHub Actions unavailable due to billing lock`

**One-line result:**  
`The controlled demo path is validated locally on native PostgreSQL: migrations pass, the canonical seed passes, backend tests pass, frontend build passes, and the runbook smoke walkthrough succeeds on a live local stack. Remote GitHub Actions remain unavailable and are now treated as an optional remote check instead of a release blocker.`

## 2. Scope of validation

Validated in this pass:

- `alembic -c backend/alembic.ini upgrade head`
- canonical demo seed on native PostgreSQL
- `python3 -m unittest discover -s backend/tests`
- `npm run build`
- live smoke walkthrough for wallet, ledger, manual adjustment, and post-submit refetch
- frontend proxy reachability against the live backend

Not in scope:

- new product slices
- reconciliation
- performance or load testing
- security review
- production deployment

## 3. Environment

**OS / machine:** `Local macOS workspace`  
**Python:** `.venv Python with backend requirements installed locally`  
**Node / npm:** `local Vite toolchain from package.json`  
**Database:** `native PostgreSQL 16 via Homebrew`  
**Backend env:** `DATABASE_URL=postgresql+psycopg://aspanch1k@/azamatai?host=/tmp`  
**Frontend env:** `VITE_LOYALTY_TENANT_ID=tenant-manual-adjustment`, `VITE_LOYALTY_PATIENT_ID=patient-manual-adjustment`, `VITE_LOYALTY_ACTOR_USER_ID=user-clinic-manager`, `VITE_LOYALTY_OPERATOR_ROLE=clinic_manager`, `VITE_LOYALTY_PROXY_TARGET=http://127.0.0.1:8000`

**Canonical dataset source:**

- `engineering/loyalty-pilot-demo-data-pack.md`
- `backend/scripts/seed_loyalty_demo.py`

## 4. Commands executed

### 4.1 Database migration

```bash
DATABASE_URL=postgresql+psycopg://aspanch1k@/azamatai?host=/tmp \
.venv/bin/python -m alembic -c backend/alembic.ini upgrade head
```

**Result:** `PASS`

### 4.2 Demo seed

```bash
DATABASE_URL=postgresql+psycopg://aspanch1k@/azamatai?host=/tmp \
.venv/bin/python backend/scripts/seed_loyalty_demo.py
```

**Result:** `PASS`

**Observed summary:**

- `tenant id: tenant-manual-adjustment`
- `patient id: patient-manual-adjustment`
- `clinic_manager id: user-clinic-manager`
- `payment id: payment-demo-1`
- `wallet balance: 5.00`
- `ledger entry count: 1`
- `ready for demo: yes`

### 4.3 Backend tests

```bash
python3 -m unittest discover -s backend/tests
```

**Result:** `PASS`

**Notes:** `36 tests passed locally.`

### 4.4 Frontend build

```bash
npm run build
```

**Result:** `PASS`

### 4.5 Live smoke walkthrough

**Runbook:** `engineering/frontend-loyalty-demo-runbook.md`  
**Result:** `PASS`

**Smoke steps executed:**

1. Started FastAPI on `127.0.0.1:8000` against native PostgreSQL.
2. Started Vite dev server with canonical `VITE_*` values.
3. Confirmed backend health: `{"status":"ok"}`.
4. Read seeded wallet from backend: balance `5.00`.
5. Read seeded ledger from backend: one accrual row with `payment_confirmed`.
6. Read wallet through the frontend proxy: same balance `5.00`.
7. Submitted manual credit through the frontend proxy:
   - amount `500.00`
   - direction `credit`
   - reason `goodwill_credit`
   - comment `Smoke demo credit`
8. Re-read wallet through the frontend proxy: balance became `505.00`.
9. Re-read ledger through the frontend proxy: latest row is the new manual adjustment and `balance_after` is `505.00`.

### 4.6 GitHub Actions

Jobs checked:

- `frontend-build`
- `backend-contracts`
- `backend-migrations`

**Result:** `UNAVAILABLE`

**Notes:** `Remote GitHub Actions are unavailable because the account is still reporting a billing lock for hosted jobs. They are treated as an optional remote check and not part of the critical local demo path.`

## 5. Validation results by area

### 5.1 Database and migrations

- `alembic upgrade head`: `yes`
- schema matches the current backend core: `yes`
- seed on a migrated native PostgreSQL database is possible: `yes`

### 5.2 Canonical dataset

- tenant created: `yes`
- patient created: `yes`
- operator users created: `yes`
- active policy created: `yes`
- wallet created: `yes`
- payment created: `yes`
- seeded accrual ledger entry created: `yes`
- repeat seed path remains supported: `yes`

### 5.3 Backend loyalty core

Confirmed locally:

- accrual: `yes`
- redemption: `yes`
- refund rollback: `yes`
- manual adjustment: `yes`

### 5.4 Frontend integration

Confirmed locally:

- wallet is rendered from backend data: `yes`
- ledger is rendered from backend data: `yes`
- manual adjustment path works for allowed role: `yes`
- post-submit refetch updates wallet and ledger from backend state: `yes`
- frontend proxy reaches the live backend: `yes`

## 6. Demo walkthrough result

### Scenario A — patient wallet and ledger visible

**Expected:**  
Patient sees real balance and real ledger rows from backend state.

**Actual:**  
`Wallet returned 5.00 before mutation and ledger returned the seeded accrual row with reason_code payment_confirmed.`

**Status:** `PASS`

### Scenario B — manual adjustment by clinic_manager

**Expected:**  
`clinic_manager` can submit a manual adjustment and wallet/ledger update through refetch.

**Actual:**  
`Manual credit of 500.00 succeeded through the frontend proxy. Follow-up reads returned wallet balance 505.00 and a new top ledger row with reason_code goodwill_credit and balance_after 505.00.`

**Status:** `PASS`

### Scenario C — proxy-backed refetch

**Expected:**  
Frontend proxy returns live backend state before and after mutation.

**Actual:**  
`Wallet read through http://127.0.0.1:4174/api/v1/... matched backend state before mutation at 5.00 and after mutation at 505.00.`

**Status:** `PASS`

## 7. Known blockers and deviations

### External blockers

- `GitHub-hosted remote checks are unavailable due to billing lock`

### Internal issues found

- `none during this local validation pass`

### Deviations from expected flow

- `Vite selected port 4174 instead of 4173 because 4173 was already occupied locally; the proxy validation still passed on 4174.`

## 8. Final status

**Overall result:** `PILOT-READY FOR CONTROLLED DEMO`

**Reason:**  
`The project is fully validated on the canonical local path: native PostgreSQL, canonical seed, backend test suite, frontend build, and a live smoke walkthrough through backend and frontend proxy all pass. Remote GitHub Actions remain unavailable, but they are no longer treated as a blocker for the controlled local demo path.`

## 9. Required follow-up actions

1. `Use this local validation path as the source of truth for controlled demos.`
2. `When GitHub billing is restored, re-run frontend-build, backend-contracts, and backend-migrations as optional remote checks.`

## 10. Sign-off

**Validated commit:** `e88a718`  
**Recommended checkpoint label:** `pilot-ready for controlled demo; locally validated on native Postgres; remote GitHub Actions unavailable due to billing lock`  
**Approved for controlled pilot demo:** `yes`
