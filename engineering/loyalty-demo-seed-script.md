# Loyalty Demo Seed Script

## Goal

Provide one idempotent backend script that creates the canonical loyalty demo dataset matching:

- `loyalty-pilot-demo-data-pack.md`
- `frontend-loyalty-demo-runbook.md`
- current `VITE_*` loyalty env values
- current backend loyalty model

This script is for the controlled pilot demo only.

## Script Location

The script lives here:

- `backend/scripts/seed_loyalty_demo.py`

Module entrypoint:

```bash
python3 -m backend.scripts.seed_loyalty_demo
```

Direct file entrypoint:

```bash
python3 backend/scripts/seed_loyalty_demo.py
```

## Prerequisites

Before running the seed:

1. the target database must exist
2. schema migrations must already be applied
3. `DATABASE_URL` or `AZAMAT_DATABASE_URL` must point to the target backend database

Recommended order:

```bash
alembic -c backend/alembic.ini upgrade head
python3 backend/scripts/seed_loyalty_demo.py
```

## What The Script Creates

The script creates exactly one canonical demo dataset:

- tenant `tenant-manual-adjustment`
- branch `branch-manual-adjustment`
- owner user `user-owner`
- clinic manager user `user-clinic-manager`
- doctor user `user-doctor-demo`
- active memberships for those users
- patient `patient-manual-adjustment`
- visit `visit-demo-1`
- loyalty program `program-demo-1`
- active policy version `policy-demo-1`
- excluded category rule for `implants`
- wallet `wallet-manual-adjustment`
- payment `payment-demo-1`
- payment line `payment-line-demo-1`
- seeded accrual ledger entry `ledger-accrual-demo-1`

The seeded wallet is consistent with the seeded ledger.

## Idempotency Behavior

The script is idempotent for the canonical dataset:

- it uses fixed IDs
- it reuses existing canonical rows
- it does not create duplicates on repeated runs

Important limitation:

- the script is intentionally fail-fast if the canonical demo patient already has non-canonical extra loyalty history
- this is deliberate to avoid destructive reset behavior

In practice this means:

- repeated runs are safe on a clean or unchanged demo dataset
- repeated runs are not meant to silently overwrite a dataset that was already mutated by live demo actions

## Conflict Model

The script fails with non-zero exit code if it finds a conflict such as:

- the expected tenant slug exists under a different id
- the expected branch code exists under a different id
- the expected user email exists under a different id
- the expected payment number exists under a different id
- the demo patient already has extra ledger activity beyond the canonical seeded accrual

This is better than silently creating a broken mixed dataset.

## Expected Output

On success the script prints a short summary:

- tenant id
- patient id
- clinic manager id
- payment id
- wallet balance
- ledger entry count
- `ready for demo: yes/no`

If post-seed validation fails, the process exits with non-zero status.

## Verification After Seed

Minimum verification:

1. run the seed script
2. start backend
3. start frontend
4. open patient cabinet
5. confirm wallet is visible
6. confirm ledger is visible
7. switch operator role to `clinic_manager`
8. apply manual adjustment
9. confirm wallet and ledger refetch

Use the full walkthrough from:

- `frontend-loyalty-demo-runbook.md`

Use the data reference from:

- `loyalty-pilot-demo-data-pack.md`

## Example Dry Run

```bash
alembic -c backend/alembic.ini upgrade head
python3 backend/scripts/seed_loyalty_demo.py
npm run dev
python3 -m uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

Frontend env should match the seeded IDs:

```bash
VITE_LOYALTY_TENANT_ID=tenant-manual-adjustment
VITE_LOYALTY_PATIENT_ID=patient-manual-adjustment
VITE_LOYALTY_ACTOR_USER_ID=user-clinic-manager
VITE_LOYALTY_OPERATOR_ROLE=clinic_manager
```

## Notes

This script does not:

- reset demo data
- seed multiple patients
- seed redemption UI scenarios
- seed rollback scenarios
- seed random fake data

That is intentional. The current goal is one reproducible pilot dataset, not a generic fixture framework.
