from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from decimal import Decimal

from sqlalchemy import case, or_, select
from sqlalchemy.orm import Session

from backend.app.db.base import ZERO_MONEY
from backend.app.db.models.loyalty import LoyaltyPolicyServiceRule, LoyaltyPolicyVersion, LoyaltyProgram
from backend.app.db.models.payment import PaymentLine
from backend.app.services.loyalty.errors import PolicyNotFoundError

ACTIVE_PROGRAM_STATUS = "active"


@dataclass(frozen=True)
class ActivePolicyContext:
    program: LoyaltyProgram
    policy: LoyaltyPolicyVersion
    rules_by_category: Mapping[str, LoyaltyPolicyServiceRule]


@dataclass(frozen=True)
class RedemptionEligibilityResult:
    eligible_total: Decimal
    denied_categories: tuple[str, ...]


def get_active_policy_for_payment(db: Session, tenant_id: str, branch_id: str) -> ActivePolicyContext:
    program_statement = (
        select(LoyaltyProgram)
        .where(
            LoyaltyProgram.tenant_id == tenant_id,
            LoyaltyProgram.status == ACTIVE_PROGRAM_STATUS,
            LoyaltyProgram.active_policy_version_id.is_not(None),
        )
        .where(or_(LoyaltyProgram.branch_id == branch_id, LoyaltyProgram.branch_id.is_(None)))
        .order_by(case((LoyaltyProgram.branch_id == branch_id, 0), else_=1), LoyaltyProgram.created_at.desc())
    )
    program = db.execute(program_statement).scalars().first()
    if program is None or program.active_policy_version_id is None:
        raise PolicyNotFoundError("Active loyalty program is not configured for this payment.")

    policy = db.execute(
        select(LoyaltyPolicyVersion).where(
            LoyaltyPolicyVersion.tenant_id == tenant_id,
            LoyaltyPolicyVersion.id == program.active_policy_version_id,
            LoyaltyPolicyVersion.is_active.is_(True),
        )
    ).scalar_one_or_none()
    if policy is None:
        raise PolicyNotFoundError("Active loyalty policy version is missing for the selected program.")

    rules = db.execute(
        select(LoyaltyPolicyServiceRule).where(
            LoyaltyPolicyServiceRule.tenant_id == tenant_id,
            LoyaltyPolicyServiceRule.policy_version_id == policy.id,
        )
    ).scalars()
    rules_by_category = {rule.service_category: rule for rule in rules}
    return ActivePolicyContext(program=program, policy=policy, rules_by_category=rules_by_category)


def calculate_eligible_accrual_base(
    payment_lines: Sequence[PaymentLine],
    policy_rules: Mapping[str, LoyaltyPolicyServiceRule],
    *,
    default_allow: bool = True,
) -> Decimal:
    eligible_total = ZERO_MONEY
    for payment_line in payment_lines:
        rule = policy_rules.get(payment_line.service_category)
        if rule is None and not default_allow:
            continue
        if rule is not None and not rule.accrual_allowed:
            continue
        eligible_total += payment_line.line_total
    return eligible_total


def calculate_redemption_eligibility(
    payment_lines: Sequence[PaymentLine],
    policy_rules: Mapping[str, LoyaltyPolicyServiceRule],
    *,
    default_allow: bool = True,
) -> RedemptionEligibilityResult:
    eligible_total = ZERO_MONEY
    denied_categories: list[str] = []
    for payment_line in payment_lines:
        rule = policy_rules.get(payment_line.service_category)
        if rule is None and not default_allow:
            denied_categories.append(payment_line.service_category)
            continue
        if rule is not None and not rule.redemption_allowed:
            denied_categories.append(payment_line.service_category)
            continue
        eligible_total += payment_line.line_total

    return RedemptionEligibilityResult(
        eligible_total=eligible_total,
        denied_categories=tuple(sorted(set(denied_categories))),
    )
