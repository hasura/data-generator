from ....helpers import BaseEnum
from enum import auto


class InterestCalculationMethod(BaseEnum):
    """Methods for calculating interest on banking products."""
    DAILY_BALANCE = auto()
    AVERAGE_DAILY_BALANCE = auto()
    MINIMUM_BALANCE = auto()
    TIERED_RATE = auto()
    BLENDED_RATE = auto()
    STEPPED_RATE = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        30.0,  # DAILY_BALANCE
        40.0,  # AVERAGE_DAILY_BALANCE
        10.0,  # MINIMUM_BALANCE
        15.0,  # TIERED_RATE
        2.0,  # BLENDED_RATE
        3.0  # STEPPED_RATE
    ]
