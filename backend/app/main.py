from fastapi import FastAPI

from backend.app.core.config import get_settings
from backend.app.modules.loyalty_ledger.router import router as loyalty_ledger_router
from backend.app.modules.loyalty_programs.router import router as loyalty_programs_router
from backend.app.modules.loyalty_wallet.router import router as loyalty_wallet_router
from backend.app.modules.payments.router import router as payments_router

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
)


@app.get("/health")
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(loyalty_programs_router, prefix=settings.api_v1_prefix)
app.include_router(loyalty_wallet_router, prefix=settings.api_v1_prefix)
app.include_router(loyalty_ledger_router, prefix=settings.api_v1_prefix)
app.include_router(payments_router, prefix=settings.api_v1_prefix)
