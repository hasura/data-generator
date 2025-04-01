from ....helpers import BaseEnum
from enum import auto


class ExchangeRateType(BaseEnum):
    """Type of exchange rate applied to the transaction."""
    SPOT = auto()
    FORWARD = auto()
    AVERAGE = auto()
    REFERENCE = auto()
    FIXED = auto()
    PREFERENTIAL = auto()
    CUSTOM = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        60.0,  # SPOT
        5.0,  # FORWARD
        5.0,  # AVERAGE
        15.0,  # REFERENCE
        5.0,  # FIXED
        5.0,  # PREFERENTIAL
        5.0  # CUSTOM
    ]
