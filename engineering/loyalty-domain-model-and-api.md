# Loyalty Domain Model and API

## Purpose

This document defines the canonical backend domain model, relational schema shape,
event contracts, and API boundaries for the dental loyalty pilot.

Use it after:

- `loyalty-program-strategy-and-rollout.md`
- `loyalty-pilot-policy-v1.md`
- `architecture.md`
- `modules-and-boundaries.md`
- `loyalty-ledger-and-policy.md`

This is the bridge between product policy and implementation.

## Scope and Assumptions

The recommended implementation context is:

- multi-tenant SaaS platform
- one tenant can have multiple branches
- one patient belongs to one tenant and can visit multiple branches inside that tenant
- backend is the source of truth for loyalty rules, balances, audit, and RBAC
- wallet balance is a derived read model, not the source of truth

For the first pilot:

- the core mechanic is a bonus wallet
- referral remains phase 2
- treatment-plan activation remains later
- patient-facing and clinic-facing reads can be optimized after the write model is safe

## Core Domains

The loyalty pilot depends on these domains:

- `tenancy`
- `rbac`
- `patients`
- `visits`
- `payments`
- `loyalty_programs`
- `loyalty_wallet`
- `loyalty_ledger`
- `communications`
- `audit`
- `analytics`

## Relationship Summary

The minimum relationship shape is:

- one `tenant` has many `branches`
- one `tenant` has many `users`
- one `tenant` has many `patients`
- one `patient` has many `visits`
- one `visit` can have one or many `payments`
- one `tenant` has one active `loyalty_program`
- one `loyalty_program` has many `loyalty_policy_versions`
- one `patient` has one `patient_wallet`
- one `patient_wallet` has many `loyalty_ledger_entries`
- one `payment` can produce zero or many `loyalty_ledger_entries`
- one `redemption` is linked to one visit and one applied ledger debit
- one privileged balance change must generate both `audit_log` and `loyalty_ledger_entry`

## Recommended Tables

The write model should stay normalized first.

## `tenants`

Purpose:

- top-level clinic tenant boundary

Required columns:

- `id`
- `name`
- `slug`
- `status`
- `default_currency_code`
- `timezone`
- `created_at`
- `updated_at`

Notes:

- currency must be tenant-configured and never hardcoded in UI or API responses
- current React mock uses `₽`; production implementation should use tenant currency

## `branches`

Purpose:

- operational clinic branches inside a tenant

Required columns:

- `id`
- `tenant_id`
- `name`
- `code`
- `address_line`
- `phone`
- `is_active`
- `created_at`
- `updated_at`

## `users`

Purpose:

- authenticated operator identities

Required columns:

- `id`
- `tenant_id`
- `email`
- `password_hash`
- `full_name`
- `status`
- `last_login_at`
- `created_at`
- `updated_at`

## `user_memberships`

Purpose:

- explicit role assignment with tenant and optional branch scope

Required columns:

- `id`
- `tenant_id`
- `user_id`
- `branch_id`
- `role_code`
- `is_active`
- `created_at`
- `updated_at`

Notes:

- `branch_id` can be null for tenant-wide roles
- do not encode authorization in free-text user flags

## `patients`

Purpose:

- patient master profile used by loyalty and clinic workflows

Required columns:

- `id`
- `tenant_id`
- `primary_branch_id`
- `external_patient_code`
- `first_name`
- `last_name`
- `middle_name`
- `birth_date`
- `phone`
- `email`
- `status`
- `registered_at`
- `created_at`
- `updated_at`

Optional but useful:

- `preferred_language`
- `household_id`
- `source_channel`

## `patient_consents`

Purpose:

- consent and preference state for messaging and marketing

Required columns:

- `id`
- `tenant_id`
- `patient_id`
- `channel`
- `consent_type`
- `status`
- `granted_at`
- `revoked_at`
- `source`
- `created_at`

Recommended values:

- `channel`: `sms`, `whatsapp`, `email`, `telegram`, `phone`
- `consent_type`: `service_notifications`, `marketing`, `loyalty_updates`
- `status`: `granted`, `revoked`

## `visits`

Purpose:

- completed or scheduled patient encounters used by operations and loyalty

Required columns:

- `id`
- `tenant_id`
- `branch_id`
- `patient_id`
- `doctor_user_id`
- `appointment_id`
- `visit_number`
- `visit_status`
- `scheduled_start_at`
- `completed_at`
- `cancelled_at`
- `created_at`
- `updated_at`

Recommended statuses:

- `scheduled`
- `checked_in`
- `completed`
- `cancelled`
- `no_show`

## `payments`

Purpose:

- payment facts that can trigger accrual or rollback

Required columns:

- `id`
- `tenant_id`
- `branch_id`
- `patient_id`
- `visit_id`
- `payment_number`
- `payment_status`
- `gross_amount`
- `patient_paid_amount`
- `currency_code`
- `payment_method`
- `confirmed_at`
- `refunded_amount`
- `refunded_at`
- `created_at`
- `updated_at`

Recommended statuses:

- `pending`
- `confirmed`
- `partially_refunded`
- `fully_refunded`
- `cancelled`
- `failed`

## `payment_lines`

Purpose:

- service-category granularity for eligibility checks

Required columns:

- `id`
- `tenant_id`
- `payment_id`
- `visit_id`
- `service_code`
- `service_name`
- `service_category`
- `quantity`
- `gross_amount`
- `discount_amount`
- `patient_paid_amount`
- `is_discounted`
- `is_financed`
- `is_insurance_paid`
- `created_at`

Why this table exists:

- loyalty policy needs category-level exclusions
- one payment can contain both eligible and non-eligible items

## `loyalty_programs`

Purpose:

- one high-level loyalty program per tenant

Required columns:

- `id`
- `tenant_id`
- `name`
- `program_status`
- `effective_from`
- `effective_to`
- `created_at`
- `updated_at`

Recommended statuses:

- `draft`
- `active`
- `paused`
- `archived`

## `loyalty_policy_versions`

Purpose:

- versioned policy settings used by ledger decisions

Required columns:

- `id`
- `tenant_id`
- `loyalty_program_id`
- `version_number`
- `accrual_rate_bps`
- `promo_accrual_rate_bps`
- `redemption_cap_bps`
- `expiry_days`
- `base_currency_code`
- `allow_same_day_redemption`
- `policy_status`
- `effective_from`
- `effective_to`
- `created_by_user_id`
- `created_at`

Notes:

- use basis points for percentages
- store policy version on every accrual or redemption decision for auditability
- the pilot defaults are `500 bps`, `700 bps`, `2000 bps`, `180 days`

## `loyalty_policy_service_rules`

Purpose:

- per-category or per-service eligibility overrides

Required columns:

- `id`
- `tenant_id`
- `loyalty_policy_version_id`
- `match_type`
- `match_value`
- `accrual_allowed`
- `redemption_allowed`
- `accrual_rate_bps_override`
- `redemption_cap_bps_override`
- `priority`
- `created_at`

Recommended `match_type` values:

- `service_code`
- `service_category`
- `branch_id`

## `patient_wallets`

Purpose:

- patient-level wallet summary read model

Required columns:

- `id`
- `tenant_id`
- `patient_id`
- `program_id`
- `currency_code`
- `available_balance`
- `pending_balance`
- `expired_balance_total`
- `redeemed_balance_total`
- `last_ledger_entry_id`
- `updated_at`

Notes:

- this table is derived from ledger truth
- keep one wallet per patient per active program

## `loyalty_ledger_entries`

Purpose:

- immutable source of truth for all wallet value movement

Required columns:

- `id`
- `tenant_id`
- `patient_id`
- `wallet_id`
- `branch_id`
- `visit_id`
- `payment_id`
- `redemption_id`
- `policy_version_id`
- `operation_type`
- `direction`
- `amount_delta`
- `balance_after`
- `currency_code`
- `source_event_type`
- `source_event_id`
- `reason_code`
- `reason_text`
- `effective_at`
- `expires_at`
- `created_by_user_id`
- `created_by_type`
- `created_at`

Canonical `operation_type` values:

- `accrual`
- `redeem`
- `expire`
- `manual_adjustment`
- `rollback`

Recommended `direction` values:

- `credit`
- `debit`

Invariants:

- never update historical amount fields silently
- every balance mutation must create exactly one ledger row
- tenant and patient scope must always be explicit

## `loyalty_redemptions`

Purpose:

- workflow record for bonus usage at checkout

Required columns:

- `id`
- `tenant_id`
- `patient_id`
- `wallet_id`
- `visit_id`
- `payment_id`
- `requested_amount`
- `approved_amount`
- `applied_amount`
- `currency_code`
- `redemption_status`
- `requested_by_user_id`
- `approved_by_user_id`
- `applied_at`
- `cancelled_at`
- `created_at`
- `updated_at`

Recommended statuses:

- `draft`
- `quoted`
- `applied`
- `cancelled`
- `rolled_back`

Notes:

- a redemption workflow record is separate from the final debit ledger row
- this keeps checkout behavior and audit readable

## `loyalty_manual_adjustments`

Purpose:

- explicit operator-initiated adjustment workflow

Required columns:

- `id`
- `tenant_id`
- `patient_id`
- `wallet_id`
- `adjustment_type`
- `amount`
- `currency_code`
- `reason_code`
- `reason_text`
- `requested_by_user_id`
- `approved_by_user_id`
- `applied_ledger_entry_id`
- `created_at`
- `applied_at`

Recommended `adjustment_type` values:

- `credit`
- `debit`

## `communication_triggers`

Purpose:

- durable queue of communication work generated by business events

Required columns:

- `id`
- `tenant_id`
- `patient_id`
- `branch_id`
- `trigger_type`
- `channel`
- `template_code`
- `payload_json`
- `scheduled_for`
- `delivery_status`
- `source_event_type`
- `source_event_id`
- `attempts_count`
- `last_error_text`
- `created_at`
- `updated_at`

Recommended `trigger_type` values:

- `accrual_confirmation`
- `redemption_confirmation`
- `expiry_warning`
- `recall_reminder`
- `reactivation_offer`

## `audit_logs`

Purpose:

- privileged action trail

Required columns:

- `id`
- `tenant_id`
- `branch_id`
- `actor_user_id`
- `actor_role_code`
- `resource_type`
- `resource_id`
- `action_code`
- `before_json`
- `after_json`
- `reason_text`
- `request_id`
- `created_at`

## `analytics_loyalty_daily_facts`

Purpose:

- daily KPI support model for owner reporting

Required columns:

- `id`
- `tenant_id`
- `branch_id`
- `fact_date`
- `eligible_patient_paid_revenue`
- `accrued_amount`
- `redeemed_amount`
- `expired_amount`
- `rollback_amount`
- `new_enrollments`
- `active_wallets`
- `repeat_visit_count`
- `manual_adjustment_count`
- `created_at`

Notes:

- this is a derived reporting table
- it must never replace ledger truth

## Read Models

The first optimized read models should be:

- `patient_wallet_summary_view`
- `patient_ledger_feed_view`
- `owner_loyalty_summary_view`
- `loyalty_liability_aging_view`

These can be implemented as SQL views, materialized views, or service-level queries.

## Canonical Status and Value Types

Use one enum set consistently across backend code, APIs, tests, and docs.

## `operation_type`

- `accrual`
- `redeem`
- `expire`
- `manual_adjustment`
- `rollback`

## `payment_status`

- `pending`
- `confirmed`
- `partially_refunded`
- `fully_refunded`
- `cancelled`
- `failed`

## `visit_status`

- `scheduled`
- `checked_in`
- `completed`
- `cancelled`
- `no_show`

## `program_status`

- `draft`
- `active`
- `paused`
- `archived`

## `redemption_status`

- `draft`
- `quoted`
- `applied`
- `cancelled`
- `rolled_back`

## Event Contracts

Use explicit domain events and keep names aligned with existing engineering docs.

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

## Minimum Event Envelope

Every domain event should include:

- `event_id`
- `event_name`
- `occurred_at`
- `tenant_id`
- `branch_id`
- `actor_type`
- `actor_user_id`
- `patient_id`
- `correlation_id`
- `payload`

## Event Payload Requirements

### `payment_confirmed`

Payload should include:

- `payment_id`
- `visit_id`
- `patient_paid_amount`
- `currency_code`
- `payment_line_ids`

### `bonus_accrued`

Payload should include:

- `ledger_entry_id`
- `wallet_id`
- `payment_id`
- `visit_id`
- `policy_version_id`
- `accrual_amount`
- `expires_at`

### `bonus_redeemed`

Payload should include:

- `ledger_entry_id`
- `redemption_id`
- `wallet_id`
- `visit_id`
- `payment_id`
- `redeemed_amount`

### `bonus_rollback_created`

Payload should include:

- `ledger_entry_id`
- `payment_id`
- `original_ledger_entry_id`
- `rollback_amount`

### `bonus_expired`

Payload should include:

- `ledger_entry_id`
- `wallet_id`
- `expired_amount`
- `expired_source_ledger_entry_id`

## API Boundaries

The backend should expose separate surfaces for:

- clinic operations
- patient cabinet
- owner analytics
- internal jobs or support tooling

## Clinic Operations API

### `GET /api/v1/patients/{patient_id}/wallet`

Purpose:

- return patient wallet summary for reception or checkout

Response shape:

- `patient_id`
- `wallet_id`
- `available_balance`
- `pending_balance`
- `currency_code`
- `next_expiry_at`
- `next_expiry_amount`
- `program_name`

### `GET /api/v1/patients/{patient_id}/ledger`

Purpose:

- return chronological loyalty history

Query params:

- `cursor`
- `limit`
- `operation_type`

Response item shape:

- `ledger_entry_id`
- `operation_type`
- `amount_delta`
- `balance_after`
- `effective_at`
- `expires_at`
- `reason_text`
- `related_visit_id`
- `related_payment_id`

### `POST /api/v1/redemptions/quote`

Purpose:

- calculate how much can be redeemed before operator confirms checkout

Request:

- `patient_id`
- `visit_id`
- `payment_line_ids`
- `gross_amount`
- `currency_code`

Response:

- `available_balance`
- `max_redeemable_amount`
- `eligible_invoice_amount`
- `redemption_cap_amount`
- `policy_version_id`
- `warnings`

### `POST /api/v1/redemptions`

Purpose:

- apply the final redemption

Request:

- `patient_id`
- `visit_id`
- `payment_id`
- `requested_amount`
- `currency_code`
- `reason_text`

Response:

- `redemption_id`
- `ledger_entry_id`
- `applied_amount`
- `balance_after`

### `POST /api/v1/manual-adjustments`

Purpose:

- create an audit-safe privileged balance adjustment

Request:

- `patient_id`
- `adjustment_type`
- `amount`
- `currency_code`
- `reason_code`
- `reason_text`

Response:

- `adjustment_id`
- `ledger_entry_id`
- `balance_after`

### `GET /api/v1/loyalty/program`

Purpose:

- fetch current tenant-level program settings for clinic UI

### `PUT /api/v1/loyalty/program`

Purpose:

- create a new effective policy version

Request:

- `program_name`
- `accrual_rate_bps`
- `promo_accrual_rate_bps`
- `redemption_cap_bps`
- `expiry_days`
- `service_rules`

Important rule:

- update by creating a new policy version, not by mutating history

## Patient Cabinet API

### `GET /api/v1/me/wallet`

Purpose:

- show patient wallet summary

### `GET /api/v1/me/ledger`

Purpose:

- show patient wallet history

### `GET /api/v1/me/bonus-rules`

Purpose:

- return patient-facing explanation of the active program

Suggested response:

- `program_name`
- `accrual_rate_display`
- `redemption_cap_display`
- `expiry_days`
- `exclusions_summary`
- `faq_items`

### `GET /api/v1/me/offers`

Purpose:

- return active recall, expiry, or reactivation offers when available

## Owner Analytics API

### `GET /api/v1/analytics/loyalty/summary`

Purpose:

- return top-level KPI summary for selected period

Suggested response:

- `repeat_visit_rate`
- `bonus_redemption_rate`
- `time_to_return`
- `revenue_influenced_by_loyalty`
- `manual_adjustment_share`

### `GET /api/v1/analytics/loyalty/liability`

Purpose:

- show outstanding liability and aging buckets

Suggested response:

- `total_outstanding_balance`
- `aging_0_90`
- `aging_91_180`
- `aging_180_plus`

### `GET /api/v1/analytics/loyalty/branches`

Purpose:

- compare branches inside the same tenant

## Permissions and Access Boundaries

Keep the first permission map explicit.

## `patient`

Can:

- read own wallet
- read own ledger
- read own offers and patient-facing rules

Cannot:

- redeem without clinic workflow
- change policy
- perform manual adjustments

## `front_desk`

Can:

- read patient wallet
- read patient ledger
- request and apply allowed redemption

Cannot:

- change program policy
- perform unrestricted manual adjustments

## `clinic_manager`

Can:

- update policy versions within allowed range
- create manual adjustments
- review redemptions and exceptions
- read branch and clinic metrics

## `owner`

Can:

- read tenant-wide analytics
- read liability and branch comparisons
- approve strategic policy changes where required

## `platform_support`

Can:

- read audit and investigate issues within support scope

Cannot:

- mutate balances silently

## Audit and Compliance Requirements

The backend must always capture:

- actor
- tenant
- patient
- balance delta
- balance after
- reason
- timestamp
- source event or workflow record

Sensitive actions requiring audit records:

- manual adjustments
- policy version changes
- redemption cancellation or rollback
- payment refund that causes rollback
- patient merge if ever added later

## Recommended Backend Module Shape

The backend module layout should follow:

```text
backend/app/modules/
  loyalty_programs/
    router.py
    service.py
    repository.py
    schemas.py
    models.py
    domain.py
  loyalty_wallet/
    router.py
    service.py
    repository.py
    schemas.py
    models.py
  loyalty_ledger/
    router.py
    service.py
    repository.py
    schemas.py
    models.py
    domain.py
```

Suggested ownership:

- `loyalty_programs` owns configuration and policy versioning
- `loyalty_wallet` owns summary reads
- `loyalty_ledger` owns accrual, redemption, expiry, rollback, and adjustment truth

## Recommended Migration Order

Implement in this order:

1. `tenants`, `branches`, `users`, `user_memberships`
2. `patients`, `patient_consents`
3. `visits`, `payments`, `payment_lines`
4. `loyalty_programs`, `loyalty_policy_versions`, `loyalty_policy_service_rules`
5. `patient_wallets`, `loyalty_ledger_entries`
6. `loyalty_redemptions`, `loyalty_manual_adjustments`
7. `communication_triggers`, `audit_logs`
8. `analytics_loyalty_daily_facts`

## Implementation Notes

- Make `payment_confirmed` idempotent so repeated webhook or operator actions do not
  double-accrue bonuses.
- Make refund processing idempotent so partial refund retries do not double-rollback.
- Do not calculate eligibility in controllers or frontend code.
- Store policy version references on ledger rows so historical decisions remain
  explainable after policy changes.
- Keep payout-like referral logic out of the base wallet implementation until phase 2.

## First Backend Tickets to Create

1. Define SQLAlchemy models and Alembic migrations for the loyalty write model.
2. Implement `payment_confirmed -> accrual` service flow.
3. Implement redemption quote and apply flow.
4. Implement refund to rollback flow.
5. Implement patient wallet and ledger read endpoints.
6. Implement manager-safe manual adjustment flow.
7. Implement expiry job and warning trigger generation.
8. Implement owner KPI summary endpoints.

## Open Questions Requiring Product Confirmation

- is one patient allowed to share one household wallet later, or should household stay
  separate from the pilot wallet
- should policy ranges be globally limited by platform config or only by tenant config
- should branch managers be allowed to change policy or only tenant-level managers
- is payment confirmation manual, integration-driven, or both in the first release
- which exact service categories map to excluded categories in the tenant catalog
