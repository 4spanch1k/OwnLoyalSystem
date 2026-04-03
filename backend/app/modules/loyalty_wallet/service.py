from datetime import datetime, timezone

from backend.app.modules.loyalty_wallet.schemas import BonusRulesResponse, WalletSummaryResponse


class LoyaltyWalletService:
    """Read-oriented wallet contract scaffold."""

    def get_wallet_summary(self, patient_id: str) -> WalletSummaryResponse:
        return WalletSummaryResponse(
            patient_id=patient_id,
            wallet_id="wallet-demo",
            available_balance=124000,
            pending_balance=0,
            currency_code="KZT",
            next_expiry_at=datetime(2026, 9, 30, tzinfo=timezone.utc),
            next_expiry_amount=24000,
            program_name="Aster Bonus",
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
