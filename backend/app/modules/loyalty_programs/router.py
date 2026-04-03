from fastapi import APIRouter

from backend.app.modules.loyalty_programs.schemas import (
    LoyaltyProgramSnapshotResponse,
    LoyaltyProgramUpdateRequest,
    LoyaltyProgramUpdateResponse,
)
from backend.app.modules.loyalty_programs.service import LoyaltyProgramService
from backend.app.shared.api.errors import not_implemented

router = APIRouter(prefix="/loyalty/program", tags=["loyalty-programs"])
service = LoyaltyProgramService()


@router.get("", response_model=LoyaltyProgramSnapshotResponse)
async def get_active_loyalty_program() -> LoyaltyProgramSnapshotResponse:
    return service.get_program_snapshot()


@router.put("", response_model=LoyaltyProgramUpdateResponse)
async def update_loyalty_program(_: LoyaltyProgramUpdateRequest) -> LoyaltyProgramUpdateResponse:
    raise not_implemented("Program versioning write flow is not implemented yet.")
