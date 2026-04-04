from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.modules.loyalty_wallet.schemas import (
    BonusRulesResponse,
    ManualAdjustmentRequest,
    ManualAdjustmentResponse,
    WalletSummaryResponse,
)
from backend.app.modules.loyalty_wallet.service import LoyaltyWalletService
from backend.app.services.loyalty.errors import (
    ManualAdjustmentConflictError,
    ManualAdjustmentPermissionError,
    ManualAdjustmentValidationError,
    PatientNotFoundError,
)
from backend.app.shared.api.errors import not_implemented

router = APIRouter(tags=["loyalty-wallet"])
service = LoyaltyWalletService()


@router.get("/patients/{patient_id}/wallet", response_model=WalletSummaryResponse)
def get_patient_wallet(
    patient_id: str,
    db: Session = Depends(get_db),
    tenant_id: str = Header(alias="X-Tenant-Id"),
) -> WalletSummaryResponse:
    try:
        return service.get_wallet_summary(db=db, tenant_id=tenant_id, patient_id=patient_id)
    except PatientNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error


@router.post("/patients/{patient_id}/wallet/adjustments", response_model=ManualAdjustmentResponse)
def create_patient_wallet_adjustment(
    patient_id: str,
    payload: ManualAdjustmentRequest,
    db: Session = Depends(get_db),
    tenant_id: str = Header(alias="X-Tenant-Id"),
    actor_user_id: str | None = Header(default=None, alias="X-Actor-User-Id"),
) -> ManualAdjustmentResponse:
    try:
        return service.create_manual_adjustment(
            db=db,
            tenant_id=tenant_id,
            patient_id=patient_id,
            payload=payload,
            actor_user_id=actor_user_id,
        )
    except PatientNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except ManualAdjustmentPermissionError as error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(error)) from error
    except ManualAdjustmentConflictError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error
    except ManualAdjustmentValidationError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(error)) from error


@router.get("/me/wallet", response_model=WalletSummaryResponse)
def get_my_wallet() -> WalletSummaryResponse:
    raise not_implemented("Patient self-service wallet flow is not implemented yet.")


@router.get("/me/bonus-rules", response_model=BonusRulesResponse)
async def get_my_bonus_rules() -> BonusRulesResponse:
    return service.get_bonus_rules()
