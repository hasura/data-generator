from ....helpers import BaseEnum
from enum import auto


class RateType(BaseEnum):
    """Types of rates applied to fees and interest."""
    FIXED = auto()
    VARIABLE = auto()
    TIERED = auto()
    PROMOTIONAL = auto()
    PENALTY = auto()
    STANDARD = auto()
    DISCOUNTED = auto()
    OTHER = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        35.0,  # FIXED
        20.0,  # VARIABLE
        10.0,  # TIERED
        15.0,  # PROMOTIONAL
        5.0,  # PENALTY
        10.0,  # STANDARD
        3.0,  # DISCOUNTED
        2.0  # OTHER
    ]
