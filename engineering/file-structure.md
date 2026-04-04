# File Structure

## Purpose

This document defines the target repository shape for the dental loyalty platform.

The repository may temporarily contain prototype code that does not match this shape.
New production work should align with the structure below.

## Top-Level Structure

```text
engineering/
frontend/
backend/
infrastructure/
.github/
```

## `engineering/`

Use for:

- architecture decisions
- project principles
- stack definition
- module ownership
- loyalty policy
- event model
- RBAC and workflow rules
- KPI and rollout definitions

Recommended contents:

```text
engineering/
  project-principles.md
  technology-stack.md
  architecture.md
  file-structure.md
  system-overview.md
  loyalty-program-strategy-and-rollout.md
  loyalty-pilot-policy-v1.md
  loyalty-domain-model-and-api.md
  modules-and-boundaries.md
  loyalty-ledger-and-policy.md
  loyalty-manual-adjustment-slice-4-spec.md
  rbac-events-and-workflows.md
  metrics-rollout-and-operating-model.md
  coding-standards.md
  review-checklist.md
```

## `frontend/`

The canonical frontend stack is Vue 3 + TypeScript + Vite.

Recommended structure:

```text
frontend/
  src/
    app/
    router/
    stores/
    modules/
    shared/
  public/
```

### `frontend/src/app/`

Use for:

- app bootstrap
- providers
- layout shell
- high-level app initialization

Do not put domain logic here.

### `frontend/src/router/`

Use for:

- Vue Router setup
- route guards
- route definitions

Keep route files thin. Business behavior belongs in modules and backend services.

### `frontend/src/stores/`

Use for:

- Pinia stores with app-wide or cross-route state
- auth/session state
- global UI state that is truly shared

Do not turn stores into a dumping ground for business rules.

### `frontend/src/modules/`

Use for domain-specific frontend code.

Recommended modules:

- `patients`
- `visits`
- `payments`
- `loyalty`
- `communications`
- `analytics`
- `auth`

Each module can contain:

```text
modules/loyalty/
  api/
  components/
  composables/
  constants/
  types/
```

### `frontend/src/shared/`

Use only for domain-neutral code reused across modules.

Suggested contents:

```text
shared/
  api/
  ui/
  utils/
  types/
  constants/
```

Keep shared code small and generic.

## `backend/`

The canonical backend stack is Python 3.12 + FastAPI.

Recommended structure:

```text
backend/
  app/
    main.py
    core/
    modules/
    shared/
  tests/
```

### `backend/app/main.py`

Use for:

- FastAPI bootstrap
- router registration
- middleware wiring

Do not place business rules here.

### `backend/app/core/`

Use for:

- Pydantic Settings config
- database setup
- auth wiring
- logging
- Redis and queue setup
- shared infrastructure concerns

### `backend/app/modules/`

Use for business modules:

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

Recommended module shape:

```text
modules/payments/
  router.py
  service.py
  repository.py
  schemas.py
  models.py
  domain.py
```

`domain.py` is optional and should exist only when policy logic is meaningful.

### `backend/tests/`

Use for:

- service tests
- API tests
- module-level repository tests
- tenant and RBAC regression tests
- loyalty policy and rollback tests

## `infrastructure/`

Use for:

- Docker Compose
- local deployment wiring
- service config templates
- operational bootstrap scripts

## `.github/`

Use for:

- GitHub Actions CI
- checks for frontend build, backend tests, and migration safety

## Structure Rules

- If code speaks the language of one module, keep it in that module.
- Keep backend policy out of frontend code.
- Keep tenant and audit handling out of generic helpers.
- Shared folders must remain domain-neutral.
- Update this document whenever the target stack or repository shape changes.
