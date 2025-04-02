from ....helpers import BaseEnum
from enum import auto


class OperatingUnit(BaseEnum):
    """Operating units within the enterprise organization."""
    HR = auto()
    IT = auto()
    OPS = auto()
    RISK = auto()
    LEGAL = auto()
    CONSUMER_BANKING = auto()
    CONSUMER_LENDING = auto()
    SMALL_BUSINESS_BANKING = auto()
    CREDIT_CARDS = auto()
    MORTGAGE_SERVICES = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        10.0,  # HR
        15.0,  # IT
        20.0,  # OPS
        10.0,  # RISK
        10.0,  # LEGAL
        15.0,  # CONSUMER_BANKING
        10.0,  # CONSUMER_LENDING
        5.0,   # SMALL_BUSINESS_BANKING
        5.0,   # CREDIT_CARDS
        5.0    # MORTGAGE_SERVICES
    ]
