from datetime import datetime, timezone

from backend.app.modules.loyalty_programs.schemas import LoyaltyProgramSnapshotResponse


class LoyaltyProgramService:
    """Contract-first service surface for active loyalty configuration."""

    def get_program_snapshot(self) -> LoyaltyProgramSnapshotResponse:
        return LoyaltyProgramSnapshotResponse(
            program_id="program-demo",
            program_name="Aster Bonus",
            policy_version_id="policy-v1",
            accrual_rate_bps=500,
            promo_accrual_rate_bps=700,
            redemption_cap_bps=2000,
            expiry_days=180,
            currency_code="KZT",
            updated_at=datetime.now(timezone.utc),
        )
