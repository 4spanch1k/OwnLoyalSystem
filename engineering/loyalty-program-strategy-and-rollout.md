# Loyalty Program Strategy and Rollout

## Purpose

This document defines the recommended loyalty program model, rollout sequence, and
operating rules for the dental loyalty and retention platform.

It complements:

- `system-overview.md`
- `project-principles.md`
- `loyalty-ledger-and-policy.md`
- `rbac-events-and-workflows.md`
- `metrics-rollout-and-operating-model.md`

## External Inputs

The recommendation below is informed by:

- [kassaofd.ru: customer loyalty program types](https://kassaofd.ru/blog/programmy-loyalnosti-dlya-klientov)
- [dentist-plus.com: dental clinic loyalty program guidance](https://dentist-plus.com/blog/programma-loyalnosti-v-stomatologii)

The generic market view matters because it shows the main mechanic families:

- discount
- bonus
- tiered
- paid membership
- partner-based
- cashback-style

The dental-specific view matters because clinics need a repeat-visit loop, CRM-backed
patient visibility, referral logic, and reminder-driven return behavior rather than a
generic retail-style discount.

## Product Thesis

Build a dental retention program around a transparent bonus wallet tied to confirmed
payments, not around uncontrolled discounts.

The first product proof should improve:

- repeat hygiene and preventive visits
- return rate after treatment
- treatment-plan follow-through
- referral-led acquisition

while keeping staff workflows simple and clinic margin protected.

## Assumed Clinic Context

Unless a tenant defines a more specific profile, the default target clinic is:

- general or family dentistry
- small to mid-sized urban clinic
- one or several branches
- mix of preventive, therapeutic, and elective services
- front-desk-led operations with limited time for manual loyalty management

This matters because the wrong mechanic for dentistry is usually either too generic
or too operationally heavy.

## Recommended Program Model

### Backbone Mechanic

Use one primary mechanic first:

- a bonus wallet with policy-controlled accrual and redemption

The patient promise should be simple:

- pay for an eligible visit
- receive bonus value after confirmed payment
- use part of that value on a later eligible visit
- receive reminders before bonus expiry or return windows

### Why This Model Wins

It wins over a pure discount program because:

- discounts are easy to understand but they train patients to wait for cheaper care
- flat discounts hide margin leakage on already low-margin services
- they do not create a visible wallet and return loop

It wins over a complex points or tier system because:

- dentistry does not need opaque math to drive recall
- staff adoption drops when program rules take too long to explain
- patients trust fixed bonus value more than abstract gamification

It wins over a paid membership as the initial MVP because:

- membership introduces billing, renewals, and plan design complexity
- many clinics need proof of retention value before selling subscriptions
- the wallet model matches the existing ledger-centered architecture already defined in
  this repository

### Supporting Mechanics After MVP Proof

After the wallet model is stable, add supporting mechanics in this order:

1. referral reward after the referred patient completes a paid visit
2. reactivation campaigns for inactive patients
3. family or household benefits
4. preventive membership plans if the clinic wants recurring revenue packages

Do not launch the product with all mechanic families at once.

## Default Pilot Rules

The first pilot should keep the rule set narrow and economically safe.

### Accrual Rules

- Default accrual rate: `5%` of patient-paid revenue on eligible services.
- Promotional accrual rate: up to `7%` only during bounded campaigns such as hygiene
  recall windows.
- Accrual happens only after `payment_confirmed`.
- No accrual on unpaid bookings, estimates, or treatment plans.
- No accrual on refunded revenue after rollback is applied.

### Redemption Rules

- Default redemption cap: up to `20%` of the current eligible invoice.
- Redemption cannot exceed available wallet balance.
- Redemption should be visible to staff before final confirmation.
- Redemption creates an explicit `redeem` operation in the ledger.
- The clinic should be able to disable redemption on excluded service categories.

### Expiry Rules

- Default expiry window: `180 days` from accrual.
- Reminder communication should be sent at `30 days` and `7 days` before expiry.
- Expiry should feel like a return nudge, not a surprise penalty.
- Expiry creates an explicit `expire` operation in the ledger.

### Exclusions and Guardrails

The pilot should exclude or strictly limit:

- already discounted services
- low-margin lab-heavy categories
- implant and large case categories if clinic economics are tight
- partner-funded or insurance-covered amounts where margin visibility is weak
- staff-created manual exceptions without reason capture

Program guardrails:

- no accrual before confirmed payment
- no silent balance mutation
- no unrestricted stacking with aggressive promotions
- no referral reward before the referred patient completes a paid visit
- no perpetual balances without expiry or liability controls

## Patient-Facing Offer

In the pilot, the patient should see a small set of understandable promises:

- earn bonus value after paid eligible care
- use bonus value on the next eligible visit
- see balance and history clearly in the cabinet
- receive reminders before bonus expiry or recall timing
- receive occasional targeted offers based on actual visit behavior

Avoid promising a broad catalog of gifts, statuses, and special cases at launch.

## Event and Workflow Model

The business loop remains:

`patient -> visit -> payment -> loyalty ledger -> communication -> return`

The loyalty program should run on explicit events:

- `visit_completed`
- `payment_confirmed`
- `bonus_accrued`
- `bonus_redeemed`
- `payment_refunded`
- `bonus_rollback_created`
- `bonus_expired`
- `manual_adjustment_created`
- `patient_return_campaign_triggered`

### Workflow: Enrollment

1. Patient is identified or created in the clinic system.
2. Front desk confirms consent and enrollment eligibility.
3. The patient sees the program rules in a short plain-language form.
4. The patient cabinet starts showing wallet status even if the balance is zero.

### Workflow: Accrual

1. Visit reaches completed status.
2. Payment becomes confirmed.
3. Loyalty policy checks eligibility, exclusions, and accrual rate.
4. Ledger creates `accrual`.
5. Wallet read model updates the available balance.
6. Communication can notify the patient about the new bonus value.

### Workflow: Redemption

1. Patient returns for an eligible visit.
2. Staff sees the allowed redemption amount based on wallet balance and policy cap.
3. Staff applies redemption.
4. Ledger creates `redeem`.
5. Audit records actor and context.
6. Payment and receipt reflect the discounted amount correctly.

### Workflow: Refund and Rollback

1. A confirmed payment is fully or partially refunded.
2. The payment module records the refund fact.
3. Loyalty policy calculates rollback impact.
4. Ledger creates `rollback`.
5. Wallet balance reflects the corrected state.
6. History remains readable instead of rewriting the past.

### Workflow: Expiry and Reactivation

1. A bonus expiry threshold approaches or a patient becomes inactive.
2. Communication rules schedule reminder or return outreach.
3. The patient receives a warning or a return offer.
4. If expiry is reached, the ledger creates `expire`.
5. Owner and manager reporting show both expiry and return impact.

## Role Model

### Patient

Should be able to:

- view wallet balance
- view accrual, redemption, rollback, and expiry history
- see upcoming expiry and eligible offers
- receive reminder and referral messages where consent exists

### Front Desk

Should be able to:

- see patient loyalty context at booking and checkout
- apply allowed redemption flows quickly
- explain the basic rules in under 30 seconds
- escalate unusual cases without breaking the workflow

### Clinic Manager

Should be able to:

- configure clinic-level policy within allowed limits
- review manual adjustments
- monitor redemption behavior, exclusions, and campaign usage
- tighten rules if margin or staff discipline drifts

### Owner

Should be able to:

- see repeat-visit ROI
- monitor bonus liability and redemption cost
- compare branches where applicable
- decide whether the pilot should scale, tighten, or stop

### Doctor

Should only see:

- minimal loyalty context relevant to treatment and patient conversation

Doctors should not manage loyalty economics.

## Required Product Modules

The loyalty rollout requires these modules as baseline product scope:

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

## Required Operator Surfaces

The clinic-facing product should include:

- program settings page
- patient profile with wallet summary
- ledger history view
- redemption action in checkout flow
- manual adjustment flow with reason capture
- campaign visibility for recall and expiry outreach
- owner KPI dashboard

## Required Patient Surface

The patient-facing product should include:

- current balance
- available-to-use balance
- ledger history
- upcoming expiry visibility
- referral entry point when referral mode is enabled
- reminder and return-offer visibility

## KPI Model

The pilot should be judged by a small KPI set tied to actual behavior:

- `repeat_visit_rate`
- `bonus_redemption_rate`
- `time_to_return`
- `revenue_influenced_by_loyalty`
- `manual_adjustment_share`

Add program-specific operating KPIs:

- referral conversion rate
- expiry warning delivery rate
- inactive-patient reactivation rate
- excluded-service share
- aged bonus liability by bucket: `0-90`, `91-180`, `180+`

## Unit Economics Guardrails

The product should remain financially safe for the clinic.

Default pilot guardrails:

- effective reward cost should stay bounded and visible at owner level
- high-cost service categories should remain excluded until economics are proven
- non-cash benefits are preferred over larger discounts when economics are weak
- redemption caps should be reviewed before increasing accrual rates
- referral rewards should be fixed-value and issued only after the referred patient
  completes a paid visit

If the clinic cannot explain the margin impact, the rule should not launch.

## Rollout Plan

### Stage 1: Program Design and Economics

Outcome:

- one agreed commercial objective
- one approved pilot rule set
- excluded categories and caps defined

Work:

- choose the pilot clinic segment
- confirm accrual rate, redemption cap, expiry window, and exclusions
- define operator scripts and patient-facing wording
- define legal and communication consent checks

### Stage 2: Ledger and Policy Foundation

Outcome:

- loyalty truth is backend-owned and auditable

Work:

- implement ledger operation types
- enforce accrual, redemption, expiry, rollback, and manual-adjustment invariants
- define policy configuration per tenant or clinic
- ensure refund-to-rollback behavior is explicit

### Stage 3: Clinic Operations MVP

Outcome:

- front desk can run the program during live visits

Work:

- patient wallet summary in clinic UI
- checkout redemption flow
- manual adjustment with reason capture
- manager-level policy visibility
- exception handling path for blocked workflows

### Stage 4: Patient Cabinet and Communication

Outcome:

- the patient sees transparent value and receives return nudges

Work:

- wallet and ledger history in patient-facing surface
- accrual and redemption notifications
- expiry reminders
- recall and inactivity campaigns

### Stage 5: Owner Reporting and Pilot Control

Outcome:

- clinic leadership can judge the program economically

Work:

- KPI dashboard
- liability aging
- campaign impact visibility
- branch and period filtering where applicable

### Stage 6: Pilot, Tuning, and Scale Decision

Outcome:

- the clinic decides whether to scale, simplify, or stop

Work:

- run one pilot branch or one clinic
- validate live cases: normal visit, redemption, refund, expiry, manual adjustment
- review staff friction and patient understanding
- tighten exclusions or communication timing where needed
- decide whether to add referral mode next

## Recommended Sequence for Product Expansion

Expand only after the base wallet program is stable:

1. referral rewards
2. inactive-patient reactivation playbooks
3. family benefits or shared household wallet
4. treatment-plan activation incentives
5. preventive membership plans
6. tiering only if visit volume and segmentation justify it

## Explicit Non-Goals Before Proof

Do not prioritize these before the base pilot proves value:

- generic cashback
- broad tier gamification
- partner marketplace rewards
- complex reward catalogs
- uncontrolled clinic-specific exceptions in core logic
- white-label feature sprawl

## Working Plan With the User

The implementation work with the user should follow this order:

1. Lock the pilot economics and rules.
2. Define tenant-level policy configuration and excluded categories.
3. Design the clinic operator flows.
4. Design the patient-facing wallet and history experience.
5. Implement communication triggers and templates.
6. Build owner analytics and pilot dashboards.
7. Run a pilot, collect friction, then decide the second mechanic.

## Next Decision to Make

Before implementation starts, confirm these product choices:

- which clinic segment is first: general, family, ortho, cosmetic, or implant-heavy
- whether the initial pilot includes referral rewards or keeps referral for phase two
- which service categories must be excluded from accrual and redemption on day one
- whether the first expiry window is `180 days` or a longer clinic-specific window
