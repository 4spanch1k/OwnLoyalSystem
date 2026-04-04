# Frontend Loyalty Integration Slice

## Purpose

This document fixes the narrow frontend integration scope for the existing loyalty backend.

Goal:

- connect the current frontend to real loyalty API reads and one real write action
- keep the existing visual language unchanged
- avoid mixing patient and operator behavior into one ambiguous screen

## Scope

This slice includes only:

- patient wallet read
- patient ledger read
- one manual adjustment operator flow
- loading, empty, success, and error states for those blocks
- refetch after successful manual adjustment

This slice does not include:

- redemption UI
- refund UI
- expiry UI
- redesign or new visual system
- optimistic money updates
- complex frontend state management

## Current Frontend Reality

The current frontend codebase is implemented as a Vite React + TypeScript app, not as a Vue module tree.

The relevant live surfaces today are:

- `src/app/components/Dashboard.tsx` for the patient-facing cabinet
- `src/app/components/DoctorCabinet.tsx` for the internal staff-facing cabinet shell

Important constraint:

- there is no dedicated `clinic_manager` or owner screen yet
- `DoctorCabinet.tsx` is visually an internal cabinet, but semantically it is doctor-facing
- backend RBAC already allows manual adjustment only for `clinic_manager` and `owner`

Because of that, the frontend plan must keep patient reads and operator write action clearly separated.

## Recommended Integration Shape

### Patient surface

Use `Dashboard.tsx` for read-only loyalty data:

- real wallet balance
- wallet freshness timestamp
- real ledger history

Do not place manual adjustment UI inside the patient cabinet.

### Internal operator surface

Use the existing `DoctorCabinet.tsx` shell only as a temporary internal workflow host for pilot integration.

Recommended placement:

- replace the current placeholder content in the `patients` section with a loyalty patient lookup and manual adjustment card

Important note:

- this is acceptable only as a temporary internal pilot surface
- the UI copy should be neutral and operational, not patient-facing
- backend RBAC remains the actual source of truth

If a dedicated manager cabinet appears later, the manual adjustment block should move there without changing the backend contract.

## Definition of Done

This slice is complete when:

- patient cabinet shows real wallet data from backend
- patient cabinet shows real ledger history from backend
- internal operator flow can submit manual adjustment to backend
- successful manual adjustment triggers fresh wallet and ledger refetch
- loading, empty, and error states are visible and readable in the current design language
- no new visual direction is introduced
- local `npm run build` stays green
- local `python3 -m unittest discover -s backend/tests` stays green

## File-Level Plan

### 1. API layer

Add a small explicit frontend service layer.

Recommended files:

- `src/app/services/loyaltyApi.ts`
- `src/app/services/loyaltyTypes.ts`

Responsibilities:

- define request and response types for wallet, ledger, and manual adjustment
- keep `fetch` calls out of presentation-heavy components
- centralize headers such as tenant and actor identifiers for the pilot environment

Required functions:

- `fetchPatientWallet(patientId: string)`
- `fetchPatientLedger(patientId: string)`
- `createManualAdjustment(patientId: string, payload)`

### 2. Patient loyalty read hook

Add one narrow composable hook for patient-facing reads.

Recommended file:

- `src/app/hooks/usePatientLoyalty.ts`

Responsibilities:

- load wallet and ledger together
- expose `loading`, `error`, `wallet`, `ledger`, and `refetch`
- stay read-only

This keeps `Dashboard.tsx` from turning into a large fetch-and-transform file.

### 3. Dashboard components

Extract the loyalty-related UI from `Dashboard.tsx` into small components without changing the visual rhythm.

Recommended files:

- `src/app/components/dashboard/PatientWalletCard.tsx`
- `src/app/components/dashboard/PatientLedgerCard.tsx`
- `src/app/components/dashboard/PatientLoyaltyEmptyState.tsx`

Responsibilities:

- `PatientWalletCard.tsx`
  - current bonus balance
  - optional lifetime accrued and redeemed when it fits cleanly
  - updated time
- `PatientLedgerCard.tsx`
  - rows for `entry_type`, `amount`, `balance_after`, `created_at`, `reason_code`
  - readable labels for operation types and reasons
- `PatientLoyaltyEmptyState.tsx`
  - no balance yet
  - no history yet
  - quiet fallback in the existing card style

### 4. Dashboard integration point

Update:

- `src/app/components/Dashboard.tsx`

Recommended changes:

- replace the static `PATIENT.bonus` display inside `BonusCard` with backend wallet data
- add a ledger card below the existing bonus card or in the same main column after `BonusCard`
- keep the current blue hero card and white content cards
- do not add a new navigation item

Recommended render order on the `main` section:

1. greeting
2. visit reminder
3. wallet card
4. ledger card
5. existing appointments and payments cards

## Operator Flow Plan

### 5. Operator hook

Add one small internal workflow hook.

Recommended file:

- `src/app/hooks/useManualAdjustment.ts`

Responsibilities:

- submit manual adjustment
- expose `submitting`, `successMessage`, `errorMessage`
- trigger external `refetch` callback after success

### 6. Operator components

Recommended files:

- `src/app/components/doctor-cabinet/LoyaltyPatientLookupCard.tsx`
- `src/app/components/doctor-cabinet/ManualAdjustmentForm.tsx`
- `src/app/components/doctor-cabinet/OperatorPatientLedgerCard.tsx`

Responsibilities:

- `LoyaltyPatientLookupCard.tsx`
  - choose a patient from current pilot data or typed id
  - show which patient is currently selected
- `ManualAdjustmentForm.tsx`
  - direction
  - amount
  - reason code
  - comment
  - submit button
  - inline success and error feedback
- `OperatorPatientLedgerCard.tsx`
  - operator-readable recent loyalty operations for the selected patient

### 7. Internal screen integration point

Update:

- `src/app/components/DoctorCabinet.tsx`

Recommended changes:

- keep `dashboard`, `schedule`, and `notes` as they are
- replace the placeholder `patients` section with:
  - patient lookup card
  - wallet summary card
  - manual adjustment form
  - recent ledger history

Important guardrail:

- keep labels neutral, such as `Баланс пациента`, `История бонусов`, `Ручная корректировка`
- do not present this block as a doctor treatment workflow
- do not expose it in the patient cabinet

## UI States

### Wallet block

- loading: skeleton-style card or muted placeholder card
- success: real balance and timestamp
- empty: `0.00` balance and a short “история пока пуста”
- error: compact alert card with safe copy such as `Не удалось загрузить бонусный баланс`

### Ledger block

- loading: list placeholders
- success: rows
- empty: simple empty card
- error: compact error row or card

### Manual adjustment form

- idle
- submitting
- success
- validation error
- API error

After successful submit:

- clear the form
- refetch wallet
- refetch ledger

Do not use optimistic updates for money state.

## Mapping Rules for Backend Data

Frontend should map backend values into readable Russian labels.

Recommended `entry_type` labels:

- `accrual` -> `Начисление`
- `redeem` -> `Списание`
- `rollback` -> `Откат`
- `manual_adjustment` -> `Ручная корректировка`
- `expire` -> `Сгорание`

Recommended `reason_code` labels:

- `payment_confirmed` -> `Подтверждённая оплата`
- `payment_refund_full` -> `Полный возврат`
- `payment_refund_partial` -> `Частичный возврат`
- `customer_support_correction` -> `Корректировка поддержки`
- `billing_fix` -> `Исправление оплаты`
- `migration_fix` -> `Исправление миграции`
- `goodwill_credit` -> `Компенсация пациенту`
- `fraud_reversal` -> `Аннулирование спорной операции`
- `admin_error_fix` -> `Исправление ошибки администратора`

Do not show raw backend strings directly when a readable label is available.

## Data and Header Assumptions

For the pilot frontend slice, the API layer will need:

- `X-Tenant-Id`
- `X-Actor-User-Id` for manual adjustment requests

Because the current frontend has no auth/session wiring for these headers yet, the integration should use a narrow temporary configuration source rather than spreading literals through components.

Recommended file:

- `src/app/services/loyaltyConfig.ts`

This file can hold temporary pilot identifiers until real auth wiring exists.

## Implementation Order

1. add `loyaltyTypes.ts`
2. add `loyaltyConfig.ts`
3. add `loyaltyApi.ts`
4. add `usePatientLoyalty.ts`
5. extract patient wallet and ledger cards
6. wire `Dashboard.tsx` to real wallet and ledger
7. add `useManualAdjustment.ts`
8. add operator loyalty components for the internal cabinet
9. wire the `patients` section in `DoctorCabinet.tsx`
10. run local verification

## Verification

Required:

- `npm run build`
- `python3 -m unittest discover -s backend/tests`

Manual verification:

1. open patient cabinet
2. confirm real wallet balance is shown
3. confirm real ledger history is shown
4. open internal cabinet `patients` section
5. submit one manual credit
6. confirm wallet and ledger refresh
7. submit an invalid or overspend debit
8. confirm error feedback stays readable and the UI remains consistent

## Risks and Guardrails

Main risks:

- adding too much new frontend architecture for one slice
- putting operator actions into the patient cabinet
- using optimistic state for money updates
- surfacing raw backend error text
- redesigning cards and spacing during integration

Guardrails:

- preserve current inline style language and layout density
- create only the smallest service and hook layer needed
- keep one canonical operator write path
- keep patient surface read-only
