from ....helpers import BaseEnum
from enum import auto


class PaymentFrequency(BaseEnum):
    """Frequency of recurring payments."""
    DAILY = auto()
    WEEKLY = auto()
    BI_WEEKLY = auto()
    MONTHLY = auto()
    QUARTERLY = auto()
    SEMI_ANNUALLY = auto()
    ANNUALLY = auto()
    CUSTOM = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        5.0,  # DAILY
        20.0,  # WEEKLY
        15.0,  # BI_WEEKLY
        40.0,  # MONTHLY
        10.0,  # QUARTERLY
        5.0,  # SEMI_ANNUALLY
        3.0,  # ANNUALLY
        2.0  # CUSTOM
    ]
