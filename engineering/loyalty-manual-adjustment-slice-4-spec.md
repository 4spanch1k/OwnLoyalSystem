# Loyalty Manual Adjustment Slice 4 Spec

## Purpose

This document fixes the implementation scope for `Slice 4`.

Goal:

- add a safe backend flow for manual bonus balance adjustment with a required audit trail and immutable ledger trail

Related documents:

- `engineering/loyalty-ledger-and-policy.md`
- `engineering/rbac-events-and-workflows.md`
- `engineering/loyalty-domain-model-and-api.md`

## Constraints

- backend only
- single adjustment only
- append-only ledger behavior only
- no bulk adjustments
- no approval workflow
- no reconciliation engine
- no refund coupling
- no redemption rewrite
- no frontend or admin UI work
- no CSV import or mass operations

## Definition of Done

`Slice 4` is complete when:

- manual adjustment is available only to explicitly allowed roles
- every adjustment requires `actor`, `reason_code`, `comment`, and timestamped persistence
- the adjustment flow never edits `wallet` directly outside the service path
- every successful adjustment creates an immutable `ledger entry`
- every successful adjustment updates the wallet snapshot
- every successful adjustment creates an `audit log`
- wallet update, ledger write, and audit write happen in one database transaction
- debit adjustments cannot overspend the wallet
- tenant scoping is enforced on read and write paths
- tests cover RBAC, required reason and comment, balance safety, and wallet and ledger consistency

## Allowed Roles

### Can create manual adjustments

- `clinic_manager`
- `owner`

### Can read adjustment audit and investigate

- `clinic_manager`
- `owner`
- `platform_support` within approved support scope

### Can read patient wallet and ledger but cannot adjust

- `front_desk`

### No access to admin adjustment flow

- `patient`
- `doctor`

## Reason Codes

Only these `reason_code` values are allowed in `Slice 4`:

- `customer_support_correction`
- `billing_fix`
- `migration_fix`
- `goodwill_credit`
- `fraud_reversal`
- `admin_error_fix`

Rules:

- `reason_code` must come from the whitelist above
- free-form explanation lives only in `comment`
- `comment` is required and must not be blank after trimming

## API

### Endpoint

`POST /api/v1/patients/{patient_id}/wallet/adjustments`

### Request Body

- `amount`
- `direction` with allowed values `credit` or `debit`
- `reason_code`
- `comment`

### Response

- `wallet_balance_after`
- `ledger_entry_id`
- `audit_log_id`
- `applied_at`

### Error Semantics

- `403` when the actor role is not allowed
- `404` when the patient or wallet is outside tenant scope or not found
- `409` when a debit would overspend the wallet
- `422` when `amount`, `direction`, `reason_code`, or `comment` is invalid

## Service Flow

The backend flow must remain narrow:

1. check RBAC for the acting user
2. validate payload fields and reason whitelist
3. load patient and wallet within tenant scope
4. lock the wallet row for update
5. compute `balance_before` and `balance_after`
6. reject debit when `balance_after < 0`
7. create one immutable `ledger entry`
8. update the wallet snapshot
9. create one `audit log`
10. commit once

Implementation rules:

- one transaction owns wallet snapshot update, ledger write, and audit write
- the ledger remains append-only
- actor identity must be persisted on the audit record and reflected in the ledger metadata or actor field
- no hidden direct balance mutation is allowed outside this flow

## Tests

Minimum required coverage:

- allowed role can create manual credit
- allowed role can create manual debit within available balance
- forbidden role is rejected
- missing `reason_code` is rejected
- blank `comment` is rejected
- zero or invalid `amount` is rejected
- debit cannot overspend wallet
- ledger entry and audit log are both created on success
- wallet balance equals the last ledger balance after adjustment
- transaction stays atomic if one write fails

Duplicate-submit behavior:

- public idempotency is not required for `Slice 4`
- if the implementation adds duplicate-submit protection, it must be explicit and DB-backed rather than best-effort handler logic

## How to Verify

Local verification for this slice:

- `python3 -m unittest discover -s backend/tests`
- `npm run build`

When Alembic is available in the environment:

- `alembic -c backend/alembic.ini upgrade head`

## Non-Goals

This slice does not include:

- bulk adjustments
- multi-step approvals
- refund orchestration changes
- redemption reversal or rewrite
- reconciliation or debt recovery logic
- UI screens or admin panels
- import tooling
