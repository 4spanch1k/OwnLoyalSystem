# Loyalty Ledger and Policy

## Purpose

This document is the canonical source of truth for loyalty balance behavior.

## Core Rule

The patient balance is the result of explicit loyalty operations. It must never change
without an explainable record.

## Canonical Operation Types

- `accrual`
- `redeem`
- `expire`
- `manual_adjustment`
- `rollback`

## Required Fields for Every Ledger Entry

- tenant identifier
- patient identifier
- operation type
- amount delta
- balance after operation
- actor or system source
- reason
- timestamp
- related payment or visit when relevant

## Accrual Policy

- Accrual happens only after `payment_confirmed`.
- Accrual must never be granted on an unconfirmed payment.
- Service-category exclusions may block accrual.
- Accrual rate must be configurable, not scattered through code.

## Redemption Policy

- Redemption is allowed only within configured limits.
- Redemption should protect clinic economics through caps or exclusions.
- Redemption must remain visible to staff before confirmation.
- Redemption must create an explicit ledger operation.

## Expiry Policy

- Expiry exists to encourage healthy return behavior, not to surprise patients.
- Expiry windows must be configurable.
- Patients should receive warning communication before expiry where the workflow supports it.
- Expiry must create an explicit ledger operation.

## Manual Adjustment Policy

- Manual adjustments require authorization.
- Manual adjustments require reason capture.
- Manual adjustments must be auditable.
- Manual adjustments must never be silent corrections.

## Rollback Policy

- Refunds must create explicit rollback behavior.
- Rollback must reference the triggering payment or financial reversal.
- Partial refunds must have defined partial rollback behavior.
- Rollback must preserve a readable historical trail instead of rewriting history.

## Exclusions

Policy may exclude:

- low-margin services
- selected categories
- scenarios defined by clinic economics

Exclusions must live in policy configuration, not in scattered conditional branches.

## Invariants

- no accrual without confirmed payment
- no silent balance mutation
- no manual adjustment without actor and reason
- no tenant leakage
- no ledger mutation without timestamped traceability
- no rollback that hides the original operation

## Failure Handling

- If an automated communication fails, the ledger truth must remain correct.
- If a downstream reminder job fails, the clinic must still see the correct wallet state.
- If a payment integration is delayed, accrual must wait for confirmed truth rather than guess.
