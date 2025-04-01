from ....helpers import BaseEnum
from enum import auto


class BalanceSubType(BaseEnum):
    """Subtypes of account balances."""
    INTRA_DAY = auto()
    OPENING = auto()
    INTERIM = auto()
    FORWARD = auto()
    EXPECTED = auto()
    AUTHORISED = auto()
    PREVIOUS_DAY = auto()
    THRESHOLD = auto()
    SWEEP = auto()
    LIMIT = auto()
    CREDIT_LINE = auto()
    CUSHION = auto()
    VALUE_DATED = auto()
    NET = auto()
    NONE = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        10.0,  # INTRA_DAY
        15.0,  # OPENING
        5.0,  # INTERIM
        8.0,  # FORWARD
        10.0,  # EXPECTED
        12.0,  # AUTHORISED
        10.0,  # PREVIOUS_DAY
        5.0,  # THRESHOLD
        3.0,  # SWEEP
        8.0,  # LIMIT
        7.0,  # CREDIT_LINE
        5.0,  # CUSHION
        7.0,  # VALUE_DATED
        10.0,  # NET
        15.0  # NONE
    ]
