# Coding Standards

## Purpose

These rules keep the dental loyalty platform readable, testable, and safe as it grows
on the declared Vue 3 + FastAPI stack.

## Non-Negotiable Rules

### 0. Verify before you change code

- Run the smallest relevant baseline checks before editing.
- Record pre-existing failures clearly.
- Rerun the same checks after the change.
- Prefer narrow checks over unrelated full-suite rituals, but do not skip verification.

Examples:

- frontend UI change: run the frontend build and the closest smoke path
- backend loyalty policy change: run the relevant service and API tests
- tenant or auth change: run the nearest access-control regression path

### 1. Use descriptive names

- Name files, components, stores, services, schemas, and helpers by intent.
- Prefer `apply_bonus_redemption_policy` over `handle_redemption`.
- Prefer `PatientLedgerPanel.vue` over `Panel.vue`.
- Prefer `loyalty_ledger_service.py` over `helpers.py`.

### 2. Do not hardcode business values

- Do not scatter accrual rates, redemption caps, expiry windows, tenant IDs, or status strings.
- Put environment-backed values in config.
- Put domain constants near the owning module.
- Put UI-only constants in the owning frontend module.

### 3. Do not duplicate logic

- Duplicate loyalty predicates, role checks, tenant filters, event naming, or payload mapping must be consolidated.
- Extract shared logic only when the abstraction is clearer than repetition.

### 4. Keep units small

- Prefer functions under 40 lines.
- Investigate functions over 60 lines.
- Keep Vue route pages thin.
- Keep FastAPI routers thin.
- Split services and components before they mix orchestration, formatting, and policy in one block.

### 5. Separate concerns clearly

Frontend:

- pages and route views assemble screens
- components render UI
- composables manage reusable view logic
- Pinia stores hold shared client state
- API clients map requests and responses

Backend:

- routers handle HTTP concerns
- services orchestrate use cases
- repositories handle persistence
- domain policy holds non-trivial reusable business rules
- schemas validate boundaries

### 6. Keep imports clean

- Import only what the file uses.
- Prefer explicit imports.
- Remove dead imports immediately.
- Avoid circular dependencies.

### 7. Make conditionals readable

- Use guard clauses.
- Flatten nested branches.
- Name complex predicates.
- Replace repeated status chains with policy helpers.

### 8. Create composables, stores, services, and helpers deliberately

Create a Vue composable when:

- reusable reactive view logic appears
- a page becomes noisy with filters, forms, pagination, or tab state

Create a Pinia store when:

- state must survive route changes
- multiple routes or modules depend on the same client state

Create a backend service when:

- validation, persistence, and side effects belong to one use case

Create a repository when:

- queries are non-trivial
- data access must be reused or isolated for testing

Create a helper only when:

- the logic is pure
- the name is specific
- the helper does not hide business policy

### 9. Keep Vue code clean

- Use `script setup` for new Vue components.
- Type props, emits, store interfaces, and composable return values.
- Keep templates scannable.
- Avoid hidden business behavior in watchers.
- Prefer computed state for derived values.
- Keep module-specific UI inside the owning module.

### 10. Keep Python code clean

- Add type hints to public functions and methods.
- Keep FastAPI routers declarative and thin.
- Keep SQLAlchemy models focused on persistence.
- Keep repositories free of business rules.
- Keep services free of raw SQL and response formatting.
- Introduce `domain.py` only when real policy logic exists.

### 11. Be explicit about contracts

- Type API payloads and important frontend state.
- Use request and response schemas at HTTP boundaries.
- Use enums or value objects where status ambiguity would create bugs.
- Document important invariants next to the owning module and enforce them in backend code.

### 12. Event and ledger naming must stay consistent

- Use one canonical event name per business action.
- Use the same loyalty operation types everywhere.
- Never invent near-duplicate names such as `bonus_refund`, `refund_bonus`, and `rollback_bonus` for the same meaning.

### 13. Tenant and audit rules are not optional

- Tenant scope must be explicit in queries, services, and events.
- Manual balance changes must always carry actor, reason, and timestamp.
- Audit-sensitive behavior must stay visible in service flows.

### 14. Remove dead code

- Delete unused components, stores, schema fields, routes, and helpers.
- Do not keep commented-out alternatives.

### 15. Do not write misleading comments

- Comments must explain why, not restate the code.
- Delete stale comments with the same change that makes them stale.

### 16. No temporary hacks in final code

- No `temp`, `final2`, `quickFix`, or similar naming.
- No silent fallback that hides broken loyalty state.
- No fake tenant or role values hardcoded to bypass correct modeling.

## Definition of Clean Enough to Merge

Code is not ready if:

- baseline verification was skipped
- names are vague
- tenant or role logic is duplicated
- loyalty values are hardcoded in multiple places
- business rules live in the frontend
- event names drift across files
- manual adjustments are not audit-safe
- dead code or misleading comments remain
- the next engineer cannot see where to extend the feature
