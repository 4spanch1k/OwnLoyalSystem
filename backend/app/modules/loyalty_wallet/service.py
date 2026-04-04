from sqlalchemy.orm import Session

from backend.app.modules.loyalty_wallet.schemas import BonusRulesResponse, ManualAdjustmentRequest, ManualAdjustmentResponse, WalletSummaryResponse
from backend.app.services.loyalty.manual_adjustment import create_manual_adjustment
from backend.app.services.loyalty.readers import get_patient_wallet_summary


class LoyaltyWalletService:
    """Read-oriented wallet service for Slice 1."""

    def get_wallet_summary(self, db: Session, tenant_id: str, patient_id: str) -> WalletSummaryResponse:
        return get_patient_wallet_summary(db=db, tenant_id=tenant_id, patient_id=patient_id)

    def create_manual_adjustment(
        self,
        db: Session,
        tenant_id: str,
        patient_id: str,
        payload: ManualAdjustmentRequest,
        actor_user_id: str | None,
    ) -> ManualAdjustmentResponse:
        result = create_manual_adjustment(
            db=db,
            tenant_id=tenant_id,
            patient_id=patient_id,
            amount=payload.amount,
            direction=payload.direction,
            reason_code=payload.reason_code,
            comment=payload.comment,
            actor_user_id=actor_user_id,
        )
        return ManualAdjustmentResponse(
            adjustment_id=result.adjustment_id,
            patient_id=result.patient_id,
            wallet_id=result.wallet_id,
            direction=result.direction,
            amount=result.amount,
            balance_before=result.balance_before,
            wallet_balance_after=result.wallet_balance_after,
            reason_code=result.reason_code,
            comment=result.comment,
            ledger_entry_id=result.ledger_entry_id,
            audit_log_id=result.audit_log_id,
            applied_at=result.applied_at,
        )

    def get_bonus_rules(self) -> BonusRulesResponse:
        return BonusRulesResponse(
            program_name="Aster Bonus",
            accrual_rate_display="5%",
            redemption_cap_display="20%",
            expiry_days=180,
            exclusions_summary=[
                "Импланты и протезирование могут не участвовать в программе.",
                "Уже скидочные услуги могут быть исключены.",
            ],
            faq_items=[
                "Бонусы начисляются после подтверждённой оплаты.",
                "Бонусы используются на следующем подходящем визите.",
            ],
        )
