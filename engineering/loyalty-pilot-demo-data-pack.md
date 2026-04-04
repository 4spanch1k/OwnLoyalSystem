# Loyalty Pilot Demo Data Pack

## Goal

Provide one canonical demo dataset that reproduces the current controlled pilot flow with minimal manual setup.

The target out-of-the-box scenario is:

- patient wallet is visible in the patient cabinet
- patient ledger is visible in the patient cabinet
- operator sees the same wallet and ledger in the internal cabinet
- `clinic_manager` can see the manual adjustment form
- manual adjustment succeeds
- frontend refetches wallet and ledger after submit

This document is not a generic seeding strategy for every future clinic.
It is the current demo pack for the existing prototype and the current backend core.

## Scope And Assumptions

Assumptions for this pack:

- one tenant
- one main branch
- one patient used by both patient-facing and operator-facing demo
- one active loyalty program
- one active policy version
- one eligible payment already represented in wallet and ledger
- one clinic manager actor for the write demo
- one owner actor for RBAC completeness
- one doctor actor for read-only role-gate verification

The pack is designed to match the current frontend defaults and backend test fixtures.

## Canonical Demo Dataset

Use these exact IDs first.

### Tenant and branch

| Entity | ID | Notes |
|---|---|---|
| tenant | `tenant-manual-adjustment` | Must match `VITE_LOYALTY_TENANT_ID` |
| branch | `branch-manual-adjustment` | Main branch for patient and staff memberships |

### Users and memberships

| Entity | ID | Role | Scope |
|---|---|---|---|
| owner user | `user-owner` | `owner` | tenant-wide |
| clinic manager user | `user-clinic-manager` | `clinic_manager` | tenant-wide or branch-wide for `branch-manual-adjustment` |
| doctor user | `user-doctor-demo` | `doctor` | same tenant, optional branch scope |

Recommended emails:

- `owner@example.com`
- `manager@example.com`
- `doctor@example.com`

### Patient

| Entity | ID | Notes |
|---|---|---|
| patient | `patient-manual-adjustment` | Must match `VITE_LOYALTY_PATIENT_ID` |
| wallet | `wallet-manual-adjustment` | Current wallet snapshot |
| visit | `visit-demo-1` | Source visit for the seeded payment |

Recommended patient values:

- first name: `Aruzhan`
- last name: `Patient`
- phone: `+77000000011`
- status: `active`
- branch: `branch-manual-adjustment`

### Loyalty program and policy

| Entity | ID | Notes |
|---|---|---|
| loyalty program | `program-demo-1` | Active for tenant |
| active policy version | `policy-demo-1` | Must be linked as active policy |
| excluded rule | `rule-demo-implants` | Shows excluded category behavior |

### Payment and line

| Entity | ID | Notes |
|---|---|---|
| payment | `payment-demo-1` | Source of seeded accrual |
| payment line | `payment-line-demo-1` | Eligible line |

### Seeded ledger row

| Entity | ID | Notes |
|---|---|---|
| accrual ledger entry | `ledger-accrual-demo-1` | Gives non-empty wallet and ledger before live manual adjustment |

## Required Entities

For the standard demo pack, these records should exist:

- `tenant`
- `branch`
- `owner`
- `clinic_manager`
- `doctor`
- `user_memberships` for all three users
- `patient`
- `loyalty_program`
- `active policy version`
- `loyalty policy service rule` for excluded category
- `wallet`
- `visit`
- `payment`
- `payment_line`
- one seeded `ledger entry` for visible history

Optional but useful:

- one `audit_log` row tied to the seeded accrual
- one second patient for selector demos

## Exact Relationships

Use this exact relationship shape:

- `tenant-manual-adjustment`
  - has branch `branch-manual-adjustment`
  - has users `user-owner`, `user-clinic-manager`, `user-doctor-demo`
  - has patient `patient-manual-adjustment`
  - has loyalty program `program-demo-1`

- `branch-manual-adjustment`
  - belongs to `tenant-manual-adjustment`
  - is the primary branch for `patient-manual-adjustment`

- `user-owner`
  - belongs to `tenant-manual-adjustment`
  - has active membership role `owner`

- `user-clinic-manager`
  - belongs to `tenant-manual-adjustment`
  - has active membership role `clinic_manager`
  - this is the actor used by `VITE_LOYALTY_ACTOR_USER_ID`

- `user-doctor-demo`
  - belongs to `tenant-manual-adjustment`
  - has active membership role `doctor`
  - this actor is for read-only role-gate validation

- `patient-manual-adjustment`
  - belongs to `tenant-manual-adjustment`
  - belongs to `branch-manual-adjustment`
  - owns wallet `wallet-manual-adjustment`
  - is linked to visit `visit-demo-1`

- `program-demo-1`
  - belongs to `tenant-manual-adjustment`
  - has active policy `policy-demo-1`

- `policy-demo-1`
  - belongs to `program-demo-1`
  - has excluded service rule `rule-demo-implants`

- `payment-demo-1`
  - belongs to `tenant-manual-adjustment`
  - belongs to `branch-manual-adjustment`
  - belongs to `patient-manual-adjustment`
  - belongs to `visit-demo-1`
  - has one eligible line `payment-line-demo-1`

- `ledger-accrual-demo-1`
  - belongs to `tenant-manual-adjustment`
  - belongs to `patient-manual-adjustment`
  - belongs to `wallet-manual-adjustment`
  - is linked to `payment-demo-1`
  - uses `policy-demo-1`

## Minimal Values

These values are enough for a stable demo.

### Loyalty policy values

- `accrual_rate_bps = 500`
- `redemption_cap_bps = 2000`
- `bonus_ttl_days = 180`
- `is_active = true`
- excluded category:
  - `service_category = implants`
  - `accrual_allowed = false`
  - `redemption_allowed = false`

### Payment values

Use:

- `status = confirmed`
- `currency = KZT`
- `total_amount = 100.00`
- `confirmed_at = now`

### Payment line values

Use one eligible line:

- `service_code = svc-demo-therapy-1`
- `service_category = therapy`
- `quantity = 1`
- `unit_price = 100.00`
- `line_total = 100.00`

### Wallet snapshot values

Use:

- `available_balance = 5.00`
- `lifetime_accrued = 5.00`
- `lifetime_redeemed = 0.00`
- `lifetime_expired = 0.00`

This matches a pre-seeded 5% accrual from a `100.00` eligible payment.

### Seeded accrual ledger entry values

Use:

- `entry_type = accrual`
- `direction = credit` logically, even though direction is derived in backend read model
- `amount = 5.00`
- `balance_after = 5.00`
- `payment_id = payment-demo-1`
- `reason_code = payment_confirmed`
- `status = posted`
- `policy_version_id = policy-demo-1`
- `idempotency_key = payment_confirmed:payment-demo-1:accrual:v1`

This one row is enough to make both wallet and ledger visible before the live manual adjustment demo.

## Creation Order

Create the dataset in this order:

1. `tenant`
2. `branch`
3. `users`
4. `user_memberships`
5. `patient`
6. `visit`
7. `loyalty_program`
8. `loyalty_policy_version`
9. `loyalty_policy_service_rule`
10. `payment`
11. `payment_line`
12. `patient_wallet`
13. `loyalty_ledger_entry`

If you also want auditable seed completeness:

14. `audit_log`

The critical rule is simple:

- create config entities first
- create operational entities second
- create wallet snapshot after you know the seeded ledger effect
- create ledger rows last so `balance_after` is explicit and explainable

## Canonical Demo Scenarios

### Scenario 1. Patient sees wallet and ledger

With the seeded dataset above:

- `GET /api/v1/patients/patient-manual-adjustment/wallet`
  - expected `available_balance = 5.00`
- `GET /api/v1/patients/patient-manual-adjustment/ledger`
  - expected at least one item
  - first seeded item should be:
    - `entry_type = accrual`
    - `reason_code = payment_confirmed`
    - `amount = 5.00`
    - `balance_after = 5.00`

This gives immediate visual proof in the patient dashboard.

### Scenario 2. Clinic manager applies manual credit

Use:

- actor user: `user-clinic-manager`
- frontend role: `clinic_manager`

Example request:

```http
POST /api/v1/patients/patient-manual-adjustment/wallet/adjustments
X-Tenant-Id: tenant-manual-adjustment
X-Actor-User-Id: user-clinic-manager
Content-Type: application/json

{
  "amount": "10.00",
  "direction": "credit",
  "reason_code": "goodwill_credit",
  "comment": "Demo credit for pilot walkthrough"
}
```

Expected result:

- response is `200`
- wallet becomes `15.00`
- latest ledger row becomes `manual_adjustment`
- latest `balance_after = 15.00`
- frontend refetch shows the updated value without optimistic patching

### Scenario 3. Role-gate verification

Switch frontend role to `doctor` while keeping the same patient and tenant.

Expected result:

- wallet and ledger stay readable
- manual adjustment form is hidden behind a read-only notice
- no write action is suggested in the UI

This validates the frontend role-safe default.

### Optional Scenario 4. Excluded category proof

If you want one backend-only example of exclusions, add:

- payment `payment-demo-excluded-1`
- line `payment-line-demo-implants-1`
- `service_category = implants`
- `total_amount = 200.00`

Expected backend behavior:

- confirm flow should produce `accrual_amount = 0.00`
- no accrual ledger entry
- optional audit skip event

This is not required for the main UI demo.

## Env Mapping

Use these frontend values to match the canonical dataset:

```bash
VITE_LOYALTY_TENANT_ID=tenant-manual-adjustment
VITE_LOYALTY_PATIENT_ID=patient-manual-adjustment
VITE_LOYALTY_ACTOR_USER_ID=user-clinic-manager
VITE_LOYALTY_OPERATOR_ROLE=clinic_manager
```

If you want to verify read-only role behavior:

```bash
VITE_LOYALTY_OPERATOR_ROLE=doctor
```

Optional extra patient:

```bash
VITE_LOYALTY_OPERATOR_PATIENT_ID=patient-second-demo
VITE_LOYALTY_OPERATOR_PATIENT_LABEL=Второй пациент для демонстрации
```

Backend values that must match:

- `tenant.id = tenant-manual-adjustment`
- `patient.id = patient-manual-adjustment`
- `user.id = user-clinic-manager`
- active membership role for `user-clinic-manager` must be `clinic_manager` or `owner`

## Verification Checklist

Use this checklist after seeding the pack.

### API checks

- `GET /health` returns `{"status":"ok"}`
- wallet endpoint returns `200`
- ledger endpoint returns `200`
- wallet payload shows `available_balance = 5.00`
- ledger payload contains at least one row
- first seeded row is explainable and linked to `payment-demo-1`

### Patient UI checks

- patient dashboard opens without raw backend errors
- balance card shows real numbers
- history card shows at least one real ledger item

### Operator UI checks

- internal cabinet opens
- `Пациенты` section shows the selected patient
- wallet summary matches the patient cabinet value
- ledger history matches the same patient state

### Manual adjustment checks

- with role `clinic_manager`, the form is visible
- after submit, success feedback appears
- wallet value changes after refetch
- latest ledger row appears at the top
- latest `balance_after` equals visible wallet balance

### Role-gate checks

- with role `doctor`, wallet and ledger still load
- with role `doctor`, manual adjustment is not available as an action

## Practical Recommendation

For the first reproducible demo, do not try to seed every possible flow.

Seed exactly this:

- one tenant
- one branch
- three users with memberships
- one patient
- one active policy
- one confirmed payment source
- one pre-seeded accrual ledger row
- one wallet snapshot that matches that accrual

That is enough to demonstrate:

- real read models
- role-safe operator UI
- live manual adjustment
- refetch-based consistency

Only after this works cleanly should you add optional demo data for:

- redemption
- rollback
- excluded category showcase
