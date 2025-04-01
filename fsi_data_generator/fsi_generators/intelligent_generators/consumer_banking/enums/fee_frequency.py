from ....helpers import BaseEnum
from enum import auto


class FeeFrequency(BaseEnum):
    """Frequency of fee charges."""
    ONE_TIME = auto()
    MONTHLY = auto()
    QUARTERLY = auto()
    ANNUALLY = auto()
    PER_TRANSACTION = auto()
    CONDITIONAL = auto()
    OTHER = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        30.0,  # ONE_TIME
        25.0,  # MONTHLY
        10.0,  # QUARTERLY
        5.0,  # ANNUALLY
        20.0,  # PER_TRANSACTION
        8.0,  # CONDITIONAL
        2.0  # OTHER
    ]
