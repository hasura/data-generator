from ....helpers import BaseEnum
from enum import auto


class ScheduledPaymentStatus(BaseEnum):
    """Status of scheduled payments."""
    PENDING = auto()
    PROCESSING = auto()
    COMPLETED = auto()
    FAILED = auto()
    CANCELED = auto()
    EXPIRED = auto()
    RECURRENCE_ENDED = auto()
    ON_HOLD = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        40.0,  # PENDING
        5.0,  # PROCESSING
        30.0,  # COMPLETED
        8.0,  # FAILED
        7.0,  # CANCELED
        5.0,  # EXPIRED
        3.0,  # RECURRENCE_ENDED
        2.0  # ON_HOLD
    ]
