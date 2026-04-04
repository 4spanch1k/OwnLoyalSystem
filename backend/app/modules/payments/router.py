from fastapi import APIRouter, Depends, Header, HTTPException, status
from sqlalchemy.orm import Session

from backend.app.db.session import get_db
from backend.app.modules.payments.schemas import ConfirmPaymentResponse
from backend.app.modules.payments.service import PaymentService
from backend.app.services.loyalty.errors import LoyaltyDomainError, PaymentNotFoundError, PaymentStateError, PolicyNotFoundError

router = APIRouter(tags=["payments"])
service = PaymentService()


@router.post("/payments/{payment_id}/confirm", response_model=ConfirmPaymentResponse)
def confirm_payment(
    payment_id: str,
    db: Session = Depends(get_db),
    tenant_id: str = Header(alias="X-Tenant-Id"),
    actor_user_id: str | None = Header(default=None, alias="X-Actor-User-Id"),
) -> ConfirmPaymentResponse:
    try:
        return service.confirm_payment(db=db, tenant_id=tenant_id, payment_id=payment_id, actor_user_id=actor_user_id)
    except PaymentNotFoundError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except (PaymentStateError, PolicyNotFoundError) as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error
    except LoyaltyDomainError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error)) from error
