# Project Principles

## Purpose

These principles define how the dental loyalty platform is shaped when product scope,
architecture, delivery speed, and clinic operations compete.

Use this document before:

- adding a new module
- changing ownership boundaries
- expanding the MVP
- introducing new infrastructure
- changing loyalty policy guardrails
- changing role or tenant boundaries

## Product Principles

- Build a retention and repeat-revenue platform, not a generic bonus feature.
- Keep the first proof centered on one outcome: more repeat visits and better patient return behavior.
- Stay pilot-first, but keep the system tenancy-ready from day one so pilot success can scale without a rewrite.
- Optimize for daily clinic operations. A feature that adds staff burden without measurable retention lift should not enter the MVP.
- Treat the value exchange as three-sided:
  - patient sees transparent value and a trustworthy cabinet
  - clinic staff gets fast, low-friction workflows
  - clinic owner gets measurable ROI and operational control
- Prefer clear loyalty logic over broad incentive catalogs or complicated point math.
- Reject uncontrolled discounting. Loyalty must protect clinic economics, not hide margin leakage.

## Platform Principles

- Build the product as a small modular monolith.
- Use one repository for frontend, backend, infrastructure, and engineering docs.
- Make the backend the source of truth for loyalty rules, permissions, tenant scope, audit, and KPI-supporting events.
- Keep the frontend focused on workflow speed, visibility, and trust. It should not own business policy.
- Keep tenant scope, RBAC, audit, and rollback behavior as first-class concerns from the start.
- Treat the loyalty ledger as the financial truth for bonus balance and dispute resolution.
- Make communications part of the product, not an afterthought. Reminders and return triggers are part of the retention loop.
- Add asynchronous infrastructure only where it solves a real problem such as reminders, expiry jobs, retries, or provider delivery.

## Delivery Principles

- Deliver in thin vertical slices that can be demonstrated end to end.
- Update engineering docs before code when a rule, module owner, workflow meaning, or role boundary changes.
- Prefer explicit code over framework ceremony and speculative abstraction.
- Keep one clear owner for every rule.
- Preserve a manual fallback for pilot-critical operations such as reminder delivery, correction of balances, or rollback review.
- Extract shared code only after real duplication appears.
- Keep the MVP small enough to validate retention proof quickly, but not so small that operator trust is missing.

## Loyalty Economics Principles

- Accrual happens only after confirmed payment.
- Redemption must be capped so clinic margin remains visible and controllable.
- Expiry is allowed only when it creates healthy return pressure and remains transparent to the patient.
- Manual adjustments require actor, timestamp, and reason.
- Refunds and canceled-money scenarios must produce explicit rollback behavior.
- Service-category exclusions must be configurable where economics require them.
- The system must always be able to explain why a balance changed.

## Quality Principles

- Protect business invariants at the backend boundary and cover them with tests.
- Keep side effects visible through services, events, and logs.
- Prefer service-level tests for loyalty policy and API tests for contracts, roles, and tenant scoping.
- Keep important business behavior out of UI watchers, generic helpers, and ad hoc scripts.
- Make metrics traceable to explicit domain events.
- Favor code and docs that a new engineer or operator can understand without reconstructing hidden context.

## Decision Filters

Before accepting a feature, refactor, or infrastructure change, answer these questions:

1. Which retention KPI can this move?
2. Which actor becomes more effective: patient, front desk, clinic manager, owner, or doctor?
3. Which module owns the rule?
4. Is the rule implemented once in the backend source of truth?
5. Can the clinic still operate if an automation fails?
6. Does the change preserve tenant, role, and audit boundaries?
7. Does the change protect or weaken loyalty economics?

If the answers are weak, reduce scope or stop the change.

## Explicit Anti-Goals Before Product Proof

- generic cashback programs with weak clinic economics
- complex points math that staff or patients cannot explain
- uncontrolled manual balance editing
- hidden bonus rules in frontend code
- communication flows that depend on perfect manual execution
- marketplace expansion before retention proof
- feature sprawl before pilot ROI is visible
- white-label complexity before the operational model is stable
- AI scoring before the event model and KPIs are trustworthy

## Update Rule

Update this document and the linked engineering docs when any of these change:

- product thesis
- target stack
- core modules
- role matrix
- tenant model
- loyalty operation types
- KPI definitions
- rollout phases
