from sqlalchemy.orm import Session

from backend.app.modules.loyalty_wallet.schemas import BonusRulesResponse, WalletSummaryResponse
from backend.app.services.loyalty.readers import get_patient_wallet_summary


class LoyaltyWalletService:
    """Read-oriented wallet service for Slice 1."""

    def get_wallet_summary(self, db: Session, tenant_id: str, patient_id: str) -> WalletSummaryResponse:
        return get_patient_wallet_summary(db=db, tenant_id=tenant_id, patient_id=patient_id)

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
