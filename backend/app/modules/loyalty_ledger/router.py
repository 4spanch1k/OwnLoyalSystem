from fastapi import APIRouter

from backend.app.modules.loyalty_ledger.schemas import (
    LedgerFeedResponse,
    ManualAdjustmentCreateRequest,
    ManualAdjustmentCreateResponse,
    RedemptionCreateRequest,
    RedemptionCreateResponse,
    RedemptionQuoteRequest,
    RedemptionQuoteResponse,
)
from backend.app.modules.loyalty_ledger.service import LoyaltyLedgerService
from backend.app.shared.api.errors import not_implemented

router = APIRouter(tags=["loyalty-ledger"])
service = LoyaltyLedgerService()


@router.get("/patients/{patient_id}/ledger", response_model=LedgerFeedResponse)
async def get_patient_ledger(patient_id: str) -> LedgerFeedResponse:
    return service.get_patient_ledger(patient_id=patient_id)


@router.post("/redemptions/quote", response_model=RedemptionQuoteResponse)
async def quote_redemption(payload: RedemptionQuoteRequest) -> RedemptionQuoteResponse:
    return service.quote_redemption(payload=payload)


@router.post("/redemptions", response_model=RedemptionCreateResponse)
async def create_redemption(_: RedemptionCreateRequest) -> RedemptionCreateResponse:
    raise not_implemented("Redemption write flow is not implemented yet.")


@router.post("/manual-adjustments", response_model=ManualAdjustmentCreateResponse)
async def create_manual_adjustment(_: ManualAdjustmentCreateRequest) -> ManualAdjustmentCreateResponse:
    raise not_implemented("Manual adjustment write flow is not implemented yet.")
