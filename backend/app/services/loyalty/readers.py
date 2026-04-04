from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.app.db.base import ZERO_MONEY
from backend.app.db.models.loyalty import LoyaltyLedgerEntry, PatientWallet
from backend.app.db.models.patient import Patient
from backend.app.db.models.tenancy import Tenant
from backend.app.modules.loyalty_ledger.schemas import LedgerEntryResponse, LedgerFeedResponse
from backend.app.modules.loyalty_wallet.schemas import WalletSummaryResponse
from backend.app.services.loyalty.errors import PatientNotFoundError


def get_patient_wallet_summary(db: Session, tenant_id: str, patient_id: str) -> WalletSummaryResponse:
    patient = db.execute(
        select(Patient).where(Patient.tenant_id == tenant_id, Patient.id == patient_id)
    ).scalar_one_or_none()
    if patient is None:
        raise PatientNotFoundError(f"Patient {patient_id} was not found in tenant {tenant_id}.")

    currency_code = db.execute(select(Tenant.default_currency_code).where(Tenant.id == tenant_id)).scalar_one_or_none() or "KZT"
    wallet = db.execute(
        select(PatientWallet).where(PatientWallet.tenant_id == tenant_id, PatientWallet.patient_id == patient_id)
    ).scalar_one_or_none()
    if wallet is None:
        return WalletSummaryResponse(
            patient_id=patient_id,
            available_balance=ZERO_MONEY,
            lifetime_accrued=ZERO_MONEY,
            lifetime_redeemed=ZERO_MONEY,
            lifetime_expired=ZERO_MONEY,
            currency_code=currency_code,
            updated_at=None,
        )

    return WalletSummaryResponse(
        patient_id=patient_id,
        available_balance=wallet.available_balance,
        lifetime_accrued=wallet.lifetime_accrued,
        lifetime_redeemed=wallet.lifetime_redeemed,
        lifetime_expired=wallet.lifetime_expired,
        currency_code=currency_code,
        updated_at=wallet.updated_at,
    )


def get_patient_ledger_feed(db: Session, tenant_id: str, patient_id: str) -> LedgerFeedResponse:
    patient = db.execute(
        select(Patient).where(Patient.tenant_id == tenant_id, Patient.id == patient_id)
    ).scalar_one_or_none()
    if patient is None:
        raise PatientNotFoundError(f"Patient {patient_id} was not found in tenant {tenant_id}.")

    entries = db.execute(
        select(LoyaltyLedgerEntry)
        .where(LoyaltyLedgerEntry.tenant_id == tenant_id, LoyaltyLedgerEntry.patient_id == patient_id)
        .order_by(LoyaltyLedgerEntry.created_at.desc())
    ).scalars().all()

    return LedgerFeedResponse(
        items=[
            LedgerEntryResponse(
                ledger_entry_id=entry.id,
                entry_type=entry.entry_type,
                amount=entry.amount,
                balance_after=entry.balance_after,
                payment_id=entry.payment_id,
                reason_code=entry.reason_code,
                currency_code=entry.currency,
                created_at=entry.created_at,
                status=entry.status,
            )
            for entry in entries
        ]
    )
