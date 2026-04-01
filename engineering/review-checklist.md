# Review Checklist

Use this checklist for pull requests, manual reviews, and AI-generated changes.

## Baseline Verification

- Were relevant baseline checks run before the change?
- Were the same checks rerun after the change?
- If something was already broken, was that recorded clearly?

## Product and Architecture Fit

- Does the change strengthen the retention-platform model rather than broaden it into generic bonus sprawl?
- Does the code fit the owning module?
- Does the change preserve the modular-monolith direction?
- Does it respect the declared Vue 3 + FastAPI stack and repository conventions?

## Naming and Readability

- Are files, functions, services, stores, schemas, and components named by intent?
- Would a new developer understand the role of the code in one pass?

## Tenant and RBAC Safety

- Is tenant scope explicit and enforced?
- Are role checks done in the right layer?
- Does any code accidentally cross tenant boundaries?

## Loyalty Ledger Correctness

- Are loyalty operations represented with canonical types?
- Is balance truth derived from explicit operations rather than hidden mutations?
- Do accrual, redemption, expiry, rollback, and manual adjustment paths stay consistent?

## Refund and Rollback Safety

- Do refund flows create explicit rollback behavior?
- Can a reader trace the rollback from payment event to ledger result?
- Are partial and full refund rules handled coherently?

## Communication Trigger Visibility

- Are reminder and return-campaign triggers explicit?
- Are important communication side effects hidden in UI code or generic helpers?
- Is there a manual fallback if automation fails?

## Hardcoding and Config

- Are business values, URLs, limits, and tenant identifiers extracted properly?
- Are environment-backed settings read at the correct boundary?

## Separation of Concerns

- Are Vue pages thin?
- Are Pinia stores used deliberately rather than as a dumping ground?
- Are FastAPI routers thin?
- Are repositories limited to persistence?
- Is policy logic kept out of generic shared code?

## KPI Traceability

- Can repeat visit rate, redemption rate, time to return, manual adjustment share, and revenue influence be traced to explicit facts or events?
- Does the change help or hurt future KPI reporting?

## Maintainability

- If the feature changes in two months, is the correct file obvious?
- Does the implementation use the smallest structure that stays clear?
- Are docs updated when ownership or terminology changed?

## Merge Rule

Request changes if the code works but:

- breaks tenant or role safety
- weakens loyalty economics
- hides rollback logic
- hides communication side effects
- introduces naming drift
- spreads hardcoded policy values
- leaves engineering docs internally inconsistent
