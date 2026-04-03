from fastapi import APIRouter

from backend.app.modules.loyalty_wallet.schemas import BonusRulesResponse, WalletSummaryResponse
from backend.app.modules.loyalty_wallet.service import LoyaltyWalletService

router = APIRouter(tags=["loyalty-wallet"])
service = LoyaltyWalletService()


@router.get("/patients/{patient_id}/wallet", response_model=WalletSummaryResponse)
async def get_patient_wallet(patient_id: str) -> WalletSummaryResponse:
    return service.get_wallet_summary(patient_id=patient_id)


@router.get("/me/wallet", response_model=WalletSummaryResponse)
async def get_my_wallet() -> WalletSummaryResponse:
    return service.get_wallet_summary(patient_id="me")


@router.get("/me/bonus-rules", response_model=BonusRulesResponse)
async def get_my_bonus_rules() -> BonusRulesResponse:
    return service.get_bonus_rules()
