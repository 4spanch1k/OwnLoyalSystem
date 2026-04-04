# Frontend Loyalty Demo Runbook

## Goal

Show the current loyalty product slice in a controlled demo:

- patient sees real wallet data
- patient sees real ledger history
- operator sees the same loyalty state
- authorized operator applies a manual adjustment
- frontend refetches wallet and ledger after submit

This runbook is for the current prototype shape.
It does not assume a separate admin app or a dedicated manager route.

## Current Scope

Included in the demo:

- patient wallet read
- patient ledger read
- operator wallet read
- operator ledger read
- manual adjustment create
- automatic refetch after successful adjustment

Not included in this demo:

- redemption UI
- refund UI
- expiry UI
- bulk actions
- approvals
- CSV import

## Preconditions

The demo will only work if frontend env and backend data point to the same tenant and patient.

Important:

- the project does not ship a live seeded demo database
- if `tenant_id`, `patient_id`, or `actor_user_id` do not exist in the running backend database, the UI will show a safe empty or error state

Fastest setup path:

- start native `postgresql@16` through Homebrew
- activate `.venv`
- set `DATABASE_URL=postgresql+psycopg://aspanch1k@/azamatai?host=/tmp`
- apply migrations
- run `python3 backend/scripts/seed_loyalty_demo.py`
- then start backend and frontend

Before the demo, make sure the backend database contains:

- one tenant
- one patient inside that tenant
- one wallet for that patient, or at least wallet-readable patient data
- one or more ledger entries if you want non-empty history
- one actor user with membership role `clinic_manager` or `owner` if you want to demo manual adjustment

The canonical dataset is documented in:

- `loyalty-pilot-demo-data-pack.md`

The seed command is documented in:

- `loyalty-demo-seed-script.md`

## Local Startup

### 1. Start native PostgreSQL

```bash
brew services start postgresql@16
/opt/homebrew/opt/postgresql@16/bin/psql -d postgres -c "CREATE DATABASE azamatai;"
```

Use this runtime path by default. Docker is optional and not required for the local demo flow.

### 2. Activate backend env and prepare data

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r backend/requirements.txt
export DATABASE_URL='postgresql+psycopg://aspanch1k@/azamatai?host=/tmp'
.venv/bin/python -m alembic -c backend/alembic.ini upgrade head
.venv/bin/python backend/scripts/seed_loyalty_demo.py
```

### 3. Start backend

From the project root:

```bash
.venv/bin/python -m uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```

Health check:

```bash
curl -s http://127.0.0.1:8000/health
```

Expected response:

```json
{"status":"ok"}
```

### 4. Start frontend

Use the existing Vite app:

```bash
npm run dev
```

The dev proxy already forwards `/api` to `http://127.0.0.1:8000` by default.

If backend runs on another target, set:

```bash
VITE_LOYALTY_PROXY_TARGET=http://127.0.0.1:8001
```

For the native local path, keep the default proxy target on `http://127.0.0.1:8000`.

## Frontend Env For Demo

Set the loyalty demo env values either in the shell or in a local Vite env file.

Minimum required values:

```bash
VITE_LOYALTY_TENANT_ID=tenant-manual-adjustment
VITE_LOYALTY_PATIENT_ID=patient-manual-adjustment
VITE_LOYALTY_ACTOR_USER_ID=user-clinic-manager
VITE_LOYALTY_OPERATOR_ROLE=clinic_manager
```

Optional values:

```bash
VITE_LOYALTY_OPERATOR_PATIENT_ID=patient-second-demo
VITE_LOYALTY_OPERATOR_PATIENT_LABEL=Второй пациент для демонстрации
VITE_LOYALTY_API_BASE_URL=
VITE_LOYALTY_PROXY_TARGET=http://127.0.0.1:8000
```

Role behavior:

- `clinic_manager` or `owner`: manual adjustment form is visible
- `doctor`, `front_desk`, or `viewer`: loyalty data stays visible, manual adjustment is hidden behind a read-only notice
- if role is missing, frontend defaults to `doctor`

That default is intentional and safe.

## Demo Flow

### A. Patient wallet and ledger

1. Open the public page in the browser.
2. Go to the patient auth block.
3. Submit the patient login form with any values.
4. The prototype will open the patient cabinet.
5. Stay on the `Мой кабинет` section.

What to point at:

- bonus balance card now loads real backend data
- wallet card shows available balance
- wallet card shows lifetime accrued and lifetime redeemed
- ledger card shows real operations with type, date, reason, amount, and balance after

Expected screen behavior:

- loading: placeholders appear first
- success: real amounts appear
- empty: history card explains that there are no operations yet
- error: safe Russian error text appears instead of raw backend detail

### B. Operator wallet and ledger

1. Return to the public page.
2. Use the staff login block.
3. Submit the employee form with any values.
4. The prototype will open the internal cabinet.
5. Open the `Пациенты` section.

What to point at:

- patient selector card
- operator wallet summary
- loyalty ledger history for the selected patient

If `VITE_LOYALTY_OPERATOR_ROLE` is not privileged:

- the page still works as a read-only loyalty view
- the manual adjustment action is replaced by an explanatory warning

### C. Manual adjustment demo

This part requires:

- `VITE_LOYALTY_OPERATOR_ROLE=clinic_manager` or `owner`
- matching backend actor membership

Steps:

1. In the internal cabinet, open `Пациенты`.
2. Select the configured patient.
3. In `Ручная корректировка`, choose `Добавить бонусы` or `Списать бонусы`.
4. Enter an amount such as `500.00`.
5. Choose a reason.
6. Add a comment with at least 5 characters.
7. Submit the form.

Expected result after success:

- success message appears in the card
- frontend does not fake the new state
- wallet is reloaded from backend
- ledger is reloaded from backend
- the updated balance is visible in the wallet summary
- a new ledger row appears in history

## How To Verify Refetch

Use this exact smoke check during the demo:

1. Note the wallet balance before submit.
2. Submit a manual credit or debit.
3. Wait for the success message.
4. Confirm that the wallet value changed in the summary card.
5. Confirm that the latest ledger row appears at the top.
6. Confirm that `balance_after` in the latest row matches the visible wallet balance.

This is the key proof that the screen is reading backend state after mutation.

## Recommended Demo Script

Use this short narrative:

1. "Сначала покажу кабинет пациента: баланс и история уже идут из backend."
2. "Теперь открою внутренний кабинет сотрудника и покажу ту же loyalty-историю с операционной стороны."
3. "Дальше покажу ручную корректировку от роли менеджера."
4. "После сохранения интерфейс не подставляет новые цифры сам, а перечитывает wallet и ledger из backend."

## Common Failure Cases

### Wallet or ledger shows patient-not-found

Most likely cause:

- frontend env points to a patient id that is absent in the running backend database

Check:

- `VITE_LOYALTY_TENANT_ID`
- `VITE_LOYALTY_PATIENT_ID`
- backend test/demo data

### Manual adjustment form is missing

Most likely cause:

- frontend role is not privileged

Check:

- `VITE_LOYALTY_OPERATOR_ROLE`

If you want the action visible, use:

- `clinic_manager`
- `owner`

### Manual adjustment is visible but request fails with permission error

Most likely cause:

- frontend role is privileged, but backend actor membership does not exist or has the wrong role/branch scope

Check:

- `VITE_LOYALTY_ACTOR_USER_ID`
- backend `user_memberships`

### History is empty

Most likely cause:

- the selected patient has no loyalty ledger entries yet

That is valid behavior. The UI should still render a clean empty state.

## Local Verification

Before and after changes to this slice, use:

```bash
python3 -m unittest discover -s backend/tests
npm run build
```

When a full environment is available again, also run:

```bash
alembic -c backend/alembic.ini upgrade head
```

And after GitHub billing is restored, re-run:

- `frontend-build`
- `backend-contracts`
- `backend-migrations`
