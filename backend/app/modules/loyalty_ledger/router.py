from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
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
from backend.app.services.loyalty.errors import PatientNotFoundError
from backend.app.shared.api.errors import not_implemented

router = APIRouter(tags=["loyalty-ledger"])
service = LoyaltyLedgerService()


@router.get("/patients/{patient_id}/ledger", response_model=LedgerFeedResponse)
def get_patient_ledger(
    patient_id: str,
    db: Session = Depends(get_db),
    tenant_id: str = Header(alias="X-Tenant-Id"),
) -> LedgerFeedResponse:
    try:
        return service.get_patient_ledger(db=db, tenant_id=tenant_id, patient_id=patient_id)
    except PatientNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error


@router.post("/redemptions/quote", response_model=RedemptionQuoteResponse)
async def quote_redemption(payload: RedemptionQuoteRequest) -> RedemptionQuoteResponse:
    return service.quote_redemption(payload=payload)


@router.post("/redemptions", response_model=RedemptionCreateResponse)
async def create_redemption(_: RedemptionCreateRequest) -> RedemptionCreateResponse:
    raise not_implemented("Redemption write flow is not implemented yet.")


@router.post("/manual-adjustments", response_model=ManualAdjustmentCreateResponse)
async def create_manual_adjustment(_: ManualAdjustmentCreateRequest) -> ManualAdjustmentCreateResponse:
    raise not_implemented("Manual adjustment write flow is not implemented yet.")
