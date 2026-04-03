from enum import StrEnum


class VisitStatus(StrEnum):
    SCHEDULED = "scheduled"
    CHECKED_IN = "checked_in"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"


class PaymentStatus(StrEnum):
    PENDING = "pending"
    CONFIRMED = "confirmed"
    PARTIALLY_REFUNDED = "partially_refunded"
    FULLY_REFUNDED = "fully_refunded"
    CANCELLED = "cancelled"
    FAILED = "failed"


class ProgramStatus(StrEnum):
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    ARCHIVED = "archived"


class LoyaltyOperationType(StrEnum):
    ACCRUAL = "accrual"
    REDEEM = "redeem"
    EXPIRE = "expire"
    MANUAL_ADJUSTMENT = "manual_adjustment"
    ROLLBACK = "rollback"


class LedgerDirection(StrEnum):
    CREDIT = "credit"
    DEBIT = "debit"


class RedemptionStatus(StrEnum):
    DRAFT = "draft"
    QUOTED = "quoted"
    APPLIED = "applied"
    CANCELLED = "cancelled"
    ROLLED_BACK = "rolled_back"


class ConsentChannel(StrEnum):
    SMS = "sms"
    WHATSAPP = "whatsapp"
    EMAIL = "email"
    TELEGRAM = "telegram"
    PHONE = "phone"


class ConsentType(StrEnum):
    SERVICE_NOTIFICATIONS = "service_notifications"
    MARKETING = "marketing"
    LOYALTY_UPDATES = "loyalty_updates"


class ConsentStatus(StrEnum):
    GRANTED = "granted"
    REVOKED = "revoked"
