# Modules and Boundaries

## Purpose

This document defines the owning responsibilities for each core module.

## `patients`

Owns:

- patient profile
- contacts
- clinic relationship
- segmentation inputs

Depends on:

- tenancy
- RBAC

Does not own:

- payment truth
- loyalty policy

## `visits`

Owns:

- visit scheduling references
- visit status lifecycle
- doctor association
- completed-visit facts

Depends on:

- patients
- tenancy

Does not own:

- payment confirmation
- ledger mutations

## `payments`

Owns:

- payment records
- payment confirmation
- refund records
- payment method references

Depends on:

- visits
- patients

Does not own:

- accrual policy
- redemption policy

## `loyalty_wallet`

Owns:

- patient-visible balance view
- available balance rules for presentation
- balance summary read model

Depends on:

- loyalty ledger

Does not own:

- the source of truth for balance changes

## `loyalty_ledger`

Owns:

- accrual
- redemption
- expiry
- manual adjustment
- rollback
- balance truth
- loyalty invariants

Depends on:

- payments
- visits
- RBAC
- tenancy
- audit

Does not own:

- campaign copy
- UI presentation

## `communications`

Owns:

- reminder scheduling
- expiry warnings
- return campaigns
- delivery orchestration

Depends on:

- visits
- loyalty ledger
- analytics signals

Does not own:

- loyalty balance truth
- clinic pricing logic

## `audit`

Owns:

- actor/action trail
- sensitive action logs
- reason capture for manual interventions

Depends on:

- all sensitive modules

Does not own:

- loyalty rules themselves

## `analytics`

Owns:

- KPI definitions
- repeat behavior facts
- redemption behavior facts
- operator and clinic performance slices

Depends on:

- visits
- payments
- loyalty ledger
- communications

Does not own:

- live operational workflows

## `rbac`

Owns:

- role definitions
- permission checks
- action-level authorization rules

Depends on:

- tenancy

Does not own:

- frontend display rules

## `tenancy`

Owns:

- tenant boundaries
- branch and clinic scope rules
- tenant-aware filtering and persistence boundaries

Depends on:

- core auth/session context

Does not own:

- loyalty policy
- UI navigation

## Cross-Module Rules

- `payments` confirms money; `loyalty_ledger` decides what that means for bonuses.
- `visits` confirms operational completion; `communications` decides when to remind or reactivate.
- `audit` records sensitive actions; it does not replace owning business logic.
- `analytics` consumes facts and events; it must not become the only place where meaning exists.
- No module may bypass `tenancy` or `rbac`.
