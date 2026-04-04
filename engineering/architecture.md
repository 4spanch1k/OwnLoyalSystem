# Architecture

## Purpose

This document defines the canonical architecture for the dental loyalty and patient
retention platform.

The target stack is:

- Vue 3, TypeScript, Vite, Pinia, Vue Router
- Python 3.12, FastAPI, SQLAlchemy, Alembic, Pydantic Settings, PyJWT, psycopg
- PostgreSQL 16, Redis 7, Docker Compose (optional), Uvicorn

For package-level stack details, see `technology-stack.md`.

The standard local runtime path is:

- native `postgresql@16` via Homebrew
- backend `.venv`
- `DATABASE_URL=postgresql+psycopg://aspanch1k@/azamatai?host=/tmp`

Docker remains optional for CI, deployment, or isolated infrastructure, but it is not required for local development or loyalty validation.

## Current Repository Reality

The current repository contains a React/Vite frontend prototype. That prototype is
useful for validating visual flows, but it is not the canonical target architecture.

Engineering decisions in this folder should align with the target Vue 3 + FastAPI
platform, while the existing React code can remain as a temporary implementation
artifact until a dedicated migration is scheduled.

## Recommended Approach

Build the product as a modular monolith with clear business boundaries:

- one clinic operations frontend
- one patient-facing frontend surface
- one backend API and jobs layer
- one shared engineering language across docs, code, schemas, and events

The business backbone is:

`patient -> visit -> payment -> loyalty ledger -> communication -> return -> KPI`

## Core Architectural Concerns

- tenancy
- RBAC
- audit
- loyalty ledger truth
- communication triggers
- KPI traceability
- manual fallback

These are not cleanup tasks. They are part of the baseline architecture.

## System Surfaces

### Clinic Operations

Used by front desk and clinic managers.

Responsibilities:

- patient lookup and profile review
- visit status handling
- payment confirmation visibility
- redemption handling within policy limits
- manual adjustment with reason capture
- campaign visibility and operational follow-up

### Patient Surface

Used by patients.

Responsibilities:

- wallet balance visibility
- loyalty ledger history
- upcoming visits and reminders
- payment and visit history
- return-triggered offers and expiry warnings

### Owner Analytics

Used by owners and clinic leadership.

Responsibilities:

- repeat-visit KPI visibility
- bonus utilization and economic control
- manual-adjustment monitoring
- campaign impact visibility
- branch and tenant comparisons where applicable

### Platform Support

Used by internal support or implementation teams.

Responsibilities:

- tenant setup support
- rollout and onboarding support
- dispute investigation through audit and ledger visibility

## Module Boundaries

Keep the backend organized around explicit modules:

- `patients`
- `visits`
- `payments`
- `loyalty_wallet`
- `loyalty_ledger`
- `communications`
- `audit`
- `analytics`
- `rbac`
- `tenancy`

Each rule must have one clear home.

Examples:

- bonus accrual eligibility belongs in `loyalty_ledger`
- payment confirmation belongs in `payments`
- visit status transitions belong in `visits`
- role enforcement belongs in `rbac`
- tenant filtering belongs in `tenancy`
- reminder scheduling belongs in `communications`

## Frontend Responsibilities

The frontend should own:

- routing
- page composition
- local interaction state
- API integration
- client-side formatting
- optimistic UI only where backend truth remains authoritative

The frontend should not own:

- loyalty policy
- permission truth
- tenant boundary enforcement
- ledger truth
- KPI source calculations

## Backend Responsibilities

The backend should own:

- business rules
- API contracts
- tenant scoping
- role enforcement
- persistence
- event creation
- audit trail
- communication triggers
- KPI-supporting facts

## Ledger-Centric Loyalty Model

The loyalty balance must be derived from explicit operations, not stored as an opaque
number that changes without explanation.

Canonical operation types:

- `accrual`
- `redeem`
- `expire`
- `manual_adjustment`
- `rollback`

Every balance-changing operation must record:

- tenant
- patient
- operation type
- amount delta
- balance after operation
- source payment or visit if relevant
- actor or system source
- reason
- timestamp

## Event Model

Important actions should generate explicit events:

- `visit_completed`
- `payment_confirmed`
- `bonus_accrued`
- `bonus_redeemed`
- `payment_refunded`
- `bonus_rollback_created`
- `bonus_expired`
- `manual_adjustment_created`
- `patient_return_campaign_triggered`

These events support jobs, communication triggers, auditability, and KPI reporting.

## Data Stores

Use the infrastructure deliberately:

- PostgreSQL 16 for application truth, ledger data, audit, and analytics facts
- Redis 7 for queueing support, rate limits, caching, and short-lived workflow state

Do not split the product into multiple services before the modular monolith stops
being operationally clear.

## Safe Extension Rules

When adding a feature:

1. Check whether it belongs to an existing business module first.
2. Add backend rules and schemas before building complex frontend flows.
3. Keep communication and audit impact explicit.
4. Preserve tenant and role boundaries.
5. Update engineering docs when ownership or meaning changes.
