from ....helpers import BaseEnum
from enum import auto


class AccountFeeSchedule(BaseEnum):
    """Fee structures for banking products."""
    STANDARD = auto()
    REDUCED = auto()
    WAIVED_WITH_MINIMUM_BALANCE = auto()
    WAIVED_WITH_DIRECT_DEPOSIT = auto()
    WAIVED_WITH_RELATIONSHIP = auto()
    NO_FEE = auto()
    ACTIVITY_BASED = auto()
    TIERED = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        30.0,  # STANDARD
        15.0,  # REDUCED
        20.0,  # WAIVED_WITH_MINIMUM_BALANCE
        15.0,  # WAIVED_WITH_DIRECT_DEPOSIT
        5.0,  # WAIVED_WITH_RELATIONSHIP
        5.0,  # NO_FEE
        5.0,  # ACTIVITY_BASED
        5.0  # TIERED
    ]
