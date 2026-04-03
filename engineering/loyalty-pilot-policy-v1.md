# Loyalty Pilot Policy v1

## Purpose

This document defines the recommended first pilot policy for the dental loyalty
program.

This is not a generic strategy note. It is a concrete proposed configuration that can
be accepted, edited, or rejected before implementation.

## Status

- proposed version: `v1`
- intended use: first live pilot
- target duration: `90 days` operational pilot with `180 days` retention readout

## Assumptions

This pilot is designed for:

- a general or family dental clinic
- a Kazakhstan-like pricing context
- patient-paid services as the primary revenue source
- one clinic or one branch for the first rollout

If the clinic is implant-heavy, ortho-heavy, or highly insurance-driven, this policy
should be tightened before launch.

## Pilot Objective

The first pilot should prove one thing:

- the clinic can increase repeat visits and return behavior without training patients
  to wait for permanent discounts

The operational proof should focus on:

- better hygiene return behavior
- better second-visit conversion after paid treatment
- visible patient wallet engagement

## Proposed Program Name

Use a simple patient-facing name:

- `Aster Bonus`

Patient-facing promise:

- pay for eligible treatment
- receive bonuses after payment
- use bonuses on the next eligible visit

## Core Rules Summary

| Policy item | Proposed default |
| --- | --- |
| Backbone mechanic | Bonus wallet |
| Accrual rate | `5%` |
| Promo accrual rate | Up to `7%` during bounded campaigns |
| Redemption cap per invoice | `20%` |
| Bonus expiry | `180 days` |
| Accrual trigger | `payment_confirmed` only |
| Referral mode | Phase 2, not included in base pilot |
| Wallet visibility | Patient cabinet + clinic profile |
| Manual adjustments | Allowed only with reason and authorization |

## Enrollment Policy

- Every new and existing patient can be enrolled unless blocked by policy or consent.
- Enrollment should happen at reception, checkout, online cabinet registration, or
  lead form conversion.
- The patient must see short rules before activation.
- The wallet should exist even with zero balance so the program remains visible.

Recommended minimum patient explanation:

- bonuses are credited after payment for eligible services
- bonuses can be used on future eligible visits
- some categories are excluded
- bonuses expire after `180 days`

## Accrual Policy

### Base Rule

- Accrue `5%` of patient-paid revenue on eligible services.
- Accrual happens only after `payment_confirmed`.
- Accrual uses the actual patient-paid amount, not list price.
- Accrual is blocked for refunded revenue after rollback.

### Promo Rule

- Limited campaigns may increase accrual to `7%`.
- Promo accrual must have a start date, end date, and eligible category list.
- Promo accrual cannot stack with other reward multipliers.

### Accrual Examples

- invoice `40,000 KZT` on eligible services -> `2,000 KZT` bonus
- invoice `80,000 KZT` during a `7%` campaign -> `5,600 KZT` bonus

## Eligible Services for Accrual

Start with broad accrual and narrow redemption.

Accrual should be allowed on:

- professional hygiene
- therapeutic dentistry
- pediatric dentistry
- diagnostics that are part of paid treatment flow
- selected cosmetic add-ons with healthy margin

Accrual should be blocked on:

- implants
- prosthetics
- aligners and orthodontic packages
- services with significant lab cost
- already discounted packages
- partner-funded services
- insurance-paid portions
- installment-financed cases until economics are reviewed

## Redemption Policy

### Base Rule

- The patient can redeem up to `20%` of the current eligible invoice.
- Redemption cannot exceed the available wallet balance.
- Redemption is allowed only on future visits, never on the same invoice that created
  the accrual.
- Redemption must be shown to staff before final confirmation.

### Recommended Redemption Floor

- Do not block small balances from redemption.
- If a clinic wants a minimum, use a soft suggestion like `1,000 KZT`, not a hard
  barrier.

### Redemption Examples

- eligible invoice `30,000 KZT` -> max redemption `6,000 KZT`
- wallet balance `4,500 KZT` -> patient can use up to `4,500 KZT`
- wallet balance `12,000 KZT` -> patient can use up to `6,000 KZT`

## Eligible Services for Redemption

Redemption should be allowed on:

- professional hygiene
- therapeutic treatment
- pediatric treatment
- diagnostics on follow-up care
- selected elective add-ons with healthy margin

Redemption should be blocked on:

- implantology
- prosthetics
- orthodontics
- surgery with high direct cost
- already discounted services
- promotional bundles
- third-party financed treatment

This structure protects margin while still giving the patient a real reason to return.

## Expiry Policy

- Standard expiry window: `180 days` from each accrual date.
- Expiry should apply per accrual batch, not as a hidden wallet reset.
- The patient should receive expiry reminders `30 days` and `7 days` before expiry.
- Expired bonuses must remain visible in history.

Do not use a shorter window in the first pilot unless the clinic has a very short
visit cycle.

## Refund and Rollback Policy

- A full refund must trigger full loyalty rollback for the affected accrual.
- A partial refund must trigger proportional rollback.
- Rollback must create its own ledger operation.
- The system must never rewrite the original accrual silently.

## Manual Adjustment Policy

- Only `clinic_manager` or another explicitly authorized role can create a manual
  adjustment.
- Every manual adjustment requires:
  - actor
  - timestamp
  - reason
  - patient
  - amount
- Front desk should not have unrestricted manual balance editing rights.

Manual adjustment should be used only for:

- migration corrections
- dispute resolution
- approved customer-service recovery

## Reactivation Policy

Reactivation should be included in the pilot as communication, not as a separate
financial mechanic.

Inactive segments:

- `9-12 months` since last completed visit
- `12-18 months`
- `18+ months`

Recommended offer:

- reminder-led offer first
- small bonus accelerator second

Recommended sequence:

1. reminder message without discount
2. if no booking, time-boxed bonus boost valid for `14 days`
3. one follow-up reminder

Do not send the same reactivation offer to every inactive patient.

## Referral Policy

Referral should be held for phase 2, but the recommended default is:

- reward only after the referred patient completes a paid visit
- minimum qualifying paid visit: `25,000 KZT`
- reward for referrer: `3,000 KZT`
- reward for referred patient: `3,000 KZT`
- no reward on no-show, free consult only, or duplicate patient record

Referral guardrails:

- block self-referrals
- block same-phone and same-household abuse where applicable
- cap rewards per patient per quarter if abuse appears
- review local healthcare advertising and referral restrictions before launch

## Communication Policy

The pilot should include these communications:

### Transactional

- welcome or enrollment confirmation
- accrual confirmation after payment
- redemption confirmation
- expiry warning at `30 days`
- expiry warning at `7 days`

### Retention

- hygiene recall reminder around month `5`
- overdue recall reminder around month `6`
- reactivation flow for inactive segments

### Optional, Not Required for v1

- birthday offer
- review request flow
- referral invitation campaign

## Front Desk Script

Use one short explanation:

- after each paid eligible visit you receive bonuses
- you can use them on the next eligible visit
- bonuses are visible in your account and valid for `180 days`

Front desk should not explain edge cases unless the patient asks. The system should
show the answer.

## Manager Controls

The clinic manager should control:

- accrual rate within allowed range
- category exclusions
- redemption cap within allowed range
- promo campaigns with bounded dates
- manual adjustment approval
- communication on or off by channel where consent exists

The manager should not control:

- raw ledger mutation without audit
- hidden overrides outside policy

## Owner KPI Targets

Use these pilot targets as the first scorecard:

| KPI | Target |
| --- | --- |
| Enrollment rate of eligible patients | `70%+` |
| Manual adjustment share | `<3%` of balance-changing events |
| Bonus redemption rate | `15-35%` |
| Effective redeemed reward cost | `<=3%` of eligible patient-paid revenue |
| Repeat-visit lift in pilot cohort | `+10%` or better vs baseline |
| Recall booking rate lift | `+10%` or better vs baseline |

Healthy interpretation:

- very low redemption can mean patients do not understand or trust the program
- very high redemption can mean margin leakage or over-aggressive accrual
- high manual adjustment share means the workflow is not operationally clean

## Liability Guardrail

Outstanding unused bonuses should remain visible by aging bucket:

- `0-90 days`
- `91-180 days`
- `180+ days`

Recommended owner guardrail:

- total outstanding bonus liability should stay below `5%` of trailing `3 months`
  eligible patient-paid revenue

If liability climbs too fast, tighten one of:

- accrual rate
- redemption eligibility
- excluded categories
- promo usage

## Stop or Tighten Rules

Tighten the program if any of these happen:

- effective redeemed reward cost rises above `3%`
- manual adjustments rise above `3%`
- excluded high-cost services start leaking into accrual or redemption
- front desk needs frequent manager intervention to complete checkout

Pause or redesign the pilot if:

- patient understanding remains weak after staff training
- margin impact becomes unclear
- refund and rollback cases become operationally messy

## Implementation Priority

Build in this exact order:

1. policy configuration
2. ledger operations and rollback rules
3. clinic UI for balance visibility and redemption
4. patient cabinet visibility
5. transactional communication
6. recall and reactivation campaigns
7. owner KPI dashboard

## Decisions Required From You

Approve or edit these items:

1. keep the base accrual at `5%` or change it
2. keep the redemption cap at `20%` or tighten it to `15%`
3. keep expiry at `180 days` or extend it to `365 days`
4. keep referral in phase 2 or include it in the initial pilot
5. confirm whether implants, prosthetics, and orthodontics stay excluded on day one
