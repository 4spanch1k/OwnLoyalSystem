class LoyaltyDomainError(Exception):
    """Base class for loyalty domain failures."""


class PaymentNotFoundError(LoyaltyDomainError):
    """Raised when a tenant-scoped payment does not exist."""


class PatientNotFoundError(LoyaltyDomainError):
    """Raised when a tenant-scoped patient does not exist."""


class PolicyNotFoundError(LoyaltyDomainError):
    """Raised when no active policy can be resolved for a payment."""


class PaymentStateError(LoyaltyDomainError):
    """Raised when a payment cannot enter the requested loyalty flow."""


class RedemptionConflictError(LoyaltyDomainError):
    """Raised when a redemption request violates wallet or policy constraints."""


class RollbackConflictError(LoyaltyDomainError):
    """Raised when a refund-driven rollback cannot be safely applied."""
