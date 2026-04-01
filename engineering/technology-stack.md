# Technology Stack

## Purpose

This document defines the canonical implementation stack for the dental loyalty
platform. It is the stack engineering documentation should target by default.

## Frontend

- Vue 3
- TypeScript
- Vite
- Pinia
- Vue Router

Use the frontend for:

- clinic operations UI
- patient-facing UI
- route composition
- local interaction state
- shared presentation logic

## Backend

- Python 3.12
- FastAPI
- SQLAlchemy
- Alembic
- Pydantic Settings
- PyJWT
- psycopg

Use the backend for:

- API contracts
- business rules
- tenant scoping
- RBAC
- audit
- loyalty ledger logic
- communication trigger orchestration
- KPI-supporting data facts

## Infrastructure

- PostgreSQL 16
- Redis 7
- Docker Compose
- Uvicorn

Infrastructure roles:

- PostgreSQL stores operational truth, ledger records, audit, and analytics facts
- Redis supports queues, cache, and short-lived workflow state
- Docker Compose is the standard local orchestration tool
- Uvicorn is the backend ASGI server for local and service execution

## Quality and Delivery

- pytest
- GitHub Actions CI

Expected checks:

- frontend build verification
- backend test verification
- migration safety verification
- smoke checks for critical flows when added

## Stack Notes

- The current repository still contains a React prototype. That does not change the
  canonical target stack defined here.
- Tailwind is not part of the canonical target stack.
- New engineering decisions should align with this document unless explicitly revised.
