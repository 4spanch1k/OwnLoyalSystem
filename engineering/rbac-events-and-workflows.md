# RBAC, Events, and Workflows

## Role Matrix

### `patient`

Can:

- view wallet balance
- view loyalty history
- view visit and payment history
- receive reminders and return nudges

Cannot:

- change loyalty policy
- perform manual adjustments

### `front_desk`

Can:

- view patient operational context
- process allowed redemption flows
- view payment and visit status
- trigger approved workflow actions

Cannot:

- change core program rules
- perform unrestricted financial overrides

### `clinic_manager`

Can:

- manage clinic-level loyalty configuration within allowed bounds
- review manual interventions
- monitor staff behavior and campaign usage

Cannot:

- bypass tenant or ownership constraints

### `owner`

Can:

- review KPI and revenue influence
- compare clinics or branches where applicable
- approve strategic configuration choices

Cannot:

- replace operational safeguards with ad hoc changes

### `doctor`

Can:

- view minimum patient program context relevant to treatment

Cannot:

- manage loyalty economics
- perform financial overrides

### `platform_support`

Can:

- support tenant setup and issue investigation
- inspect audit and ledger data within approved support scope

Cannot:

- perform untracked balance changes

## Canonical Events

- `visit_completed`
- `payment_confirmed`
- `bonus_accrued`
- `bonus_redeemed`
- `payment_refunded`
- `bonus_rollback_created`
- `bonus_expired`
- `manual_adjustment_created`
- `patient_return_campaign_triggered`

## Workflow: Visit to Accrual

1. Visit reaches completed state.
2. Payment is confirmed.
3. Eligibility policy is checked.
4. Accrual is created in the loyalty ledger.
5. Wallet read model reflects the new available value.
6. Patient communication can be triggered.

## Workflow: Redemption

1. Patient returns for a qualifying visit.
2. Allowed redemption amount is calculated from policy and available wallet value.
3. Authorized staff applies redemption.
4. Ledger records `redeem`.
5. Audit trail records actor and reason if required.

## Workflow: Refund to Rollback

1. A confirmed payment is refunded fully or partially.
2. Refund fact is recorded in `payments`.
3. Loyalty policy determines rollback amount.
4. Ledger records `rollback`.
5. Wallet read model is updated.
6. Audit and analytics remain historically explainable.

## Workflow: Expiry

1. Expiry window approaches.
2. Communication warning may be scheduled.
3. Expiry job executes at the correct threshold.
4. Ledger records `expire`.
5. Wallet view reflects the new state.

## Workflow: Return Campaign

1. Analytics or business timing identifies an inactive patient.
2. Communication trigger is created.
3. Campaign is delivered or queued.
4. Staff can see relevant return context where needed.

## Manual Fallback Rules

- If communication automation fails, staff must still be able to see the patient state and act manually.
- If a ledger-related workflow is blocked, the system must not guess or silently self-correct.
- If an exception requires human intervention, the correction path must remain authorized and auditable.
