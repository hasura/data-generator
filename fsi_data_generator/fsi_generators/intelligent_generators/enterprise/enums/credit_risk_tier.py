from ....helpers import BaseEnum
from enum import auto


class CreditRiskTier(BaseEnum):
    """Credit risk tier categories for credit classification."""
    SUPER_PRIME = auto()  # Excellent credit, lowest risk tier (typically 781-850)
    PRIME = auto()  # Very good credit, low risk tier (typically 661-780)
    NEAR_PRIME = auto()  # Good credit with some risk factors (typically 601-660)
    SUBPRIME = auto()  # Fair credit with significant risk factors (typically 501-600)
    DEEP_SUBPRIME = auto()  # Poor credit with high risk factors (typically below 500)
    NO_SCORE = auto()  # Insufficient credit history to generate score
    UNKNOWN = auto()  # Credit risk tier is unknown or not provided

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        15.0,  # SUPER_PRIME
        35.0,  # PRIME
        20.0,  # NEAR_PRIME
        15.0,  # SUBPRIME
        8.0,   # DEEP_SUBPRIME
        5.0,   # NO_SCORE
        2.0    # UNKNOWN
    ]
