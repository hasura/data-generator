from ....helpers import BaseEnum
from enum import auto


class OfferType(BaseEnum):
    LOAN = auto()
    BALANCE_TRANSFER = auto()
    CREDIT_LIMIT_INCREASE = auto()
    INTEREST_RATE_REDUCTION = auto()
    OVERDRAFT = auto()
    INVESTMENT = auto()
    SAVINGS = auto()
    INSURANCE = auto()
    CASHBACK = auto()
    REWARDS = auto()
    PREMIUM_ACCOUNT = auto()
    FEE_WAIVER = auto()
    BUNDLE = auto()
    PREAPPROVAL = auto()
    PROMOTIONAL = auto()
    OTHER = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        15.0,  # LOAN
        10.0,  # BALANCE_TRANSFER
        12.0,  # CREDIT_LIMIT_INCREASE
        10.0,  # INTEREST_RATE_REDUCTION
        8.0,  # OVERDRAFT
        5.0,  # INVESTMENT
        8.0,  # SAVINGS
        5.0,  # INSURANCE
        7.0,  # CASHBACK
        8.0,  # REWARDS
        6.0,  # PREMIUM_ACCOUNT
        5.0,  # FEE_WAIVER
        3.0,  # BUNDLE
        5.0,  # PREAPPROVAL
        2.0,  # PROMOTIONAL
        1.0  # OTHER
    ]
