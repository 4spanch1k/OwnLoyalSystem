
  # Сайт стоматологии Aster Dental

  This is a code bundle for Сайт стоматологии Aster Dental. The original project is available at https://www.figma.com/design/rKjrFw4MfvSGbMhT9kJjPF/%D0%A1%D0%B0%D0%B9%D1%82-%D1%81%D1%82%D0%BE%D0%BC%D0%B0%D1%82%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D0%B8-Aster-Dental.

  ## Running the code

  Native local path is the default development/runtime setup for this repository.

  ### No-Docker Local Bootstrap

  1. Install backend requirements into `.venv`:

  ```bash
  python3 -m venv .venv
  .venv/bin/python -m pip install -r backend/requirements.txt
  ```

  2. Start native PostgreSQL 16 through Homebrew:

  ```bash
  brew services start postgresql@16
  /opt/homebrew/opt/postgresql@16/bin/psql -d postgres -c "CREATE DATABASE azamatai;"
  ```

  3. Point backend tooling to the native local database:

  ```bash
  export DATABASE_URL='postgresql+psycopg://aspanch1k@/azamatai?host=/tmp'
  ```

  4. Apply migrations and seed the canonical demo dataset:

  ```bash
  .venv/bin/python -m alembic -c backend/alembic.ini upgrade head
  .venv/bin/python backend/scripts/seed_loyalty_demo.py
  ```

  5. Start backend and frontend:

  ```bash
  .venv/bin/python -m uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
  npm run dev
  ```

  Run `npm i` to install the frontend dependencies if needed.

  Docker is now optional and should be treated as a fallback path for CI, deployment,
  or isolated local infrastructure when native PostgreSQL is not available.

  ## Documentation

  Key engineering documents live in `engineering/`.

  Start with:

  - `engineering/loyalty-program-strategy-and-rollout.md`
  - `engineering/loyalty-pilot-policy-v1.md`
  - `engineering/loyalty-domain-model-and-api.md`
  - `engineering/architecture.md`
  - `engineering/loyalty-ledger-and-policy.md`
  - `engineering/loyalty-manual-adjustment-slice-4-spec.md`
  - `engineering/frontend-loyalty-integration-slice.md`
  - `engineering/frontend-loyalty-demo-runbook.md`
  - `engineering/loyalty-pilot-demo-data-pack.md`
  - `engineering/loyalty-demo-seed-script.md`
  - `engineering/pilot-validation-report-125252a-draft.md`
  
