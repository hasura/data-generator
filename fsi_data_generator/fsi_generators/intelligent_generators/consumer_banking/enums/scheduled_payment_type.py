from ....helpers import BaseEnum
from enum import auto


class ScheduledPaymentType(BaseEnum):
    """Types of scheduled payments."""
    SINGLE = auto()
    RECURRING = auto()
    INSTALLMENT = auto()
    CONDITIONAL = auto()
    VARIABLE = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        50.0,  # SINGLE
        30.0,  # RECURRING
        10.0,  # INSTALLMENT
        5.0,  # CONDITIONAL
        5.0  # VARIABLE
    ]
