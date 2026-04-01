# Metrics, Rollout, and Operating Model

## KPI Definitions

### `repeat_visit_rate`

Measures the share of patients who return after an earlier visit.

### `bonus_redemption_rate`

Measures how much granted wallet value is actually used.

### `time_to_return`

Measures how long it takes a patient to return after a visit.

### `manual_adjustment_share`

Measures how often staff intervene manually in loyalty state.

### `revenue_influenced_by_loyalty`

Measures the revenue associated with loyalty-driven behavior and redemption flows.

## Pilot Phases

### Phase 1: Pilot

- one clinic or one branch
- roles configured
- basic accrual and redemption rules active
- patient cabinet available
- minimal KPI visibility
- real cases validated: normal visit, refund, manual adjustment, redemption, expiry

### Phase 2: Stabilization

- operator friction removed
- exclusions refined
- communication timing tuned
- KPI baselines reviewed

### Phase 3: Scale

- onboarding template formalized
- repeatable rollout process created
- multi-branch and packaged growth options added where justified

## SaaS Operating Model

The product is sold as an operational retention platform:

- onboarding fee for setup and training
- recurring subscription for continuous platform value
- scale packages based on clinics, branches, staff, patients, or modules
- optional paid extensions for integrations and advanced reporting

## Why the Operating Model Affects Architecture

- tenant isolation must exist from the start
- analytics must support owner-visible ROI
- audit must support supportability and trust
- rollout must be repeatable, not clinic-specific chaos

## Scope Guardrails

Keep in the early product:

- role-safe operations
- ledger truth
- communication triggers
- KPI visibility
- repeatable rollout

Push later:

- heavy white-label complexity
- custom per-clinic branches in core code
- advanced partner ecosystems
