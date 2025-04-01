from enum import auto
from fsi_data_generator.fsi_generators.helpers import BaseEnum


class StatementDateType(BaseEnum):
    """Types of statement dates."""
    STATEMENT_DATE = auto()
    DUE_DATE = auto()
    PAYMENT_CUTOFF_DATE = auto()
    CLOSE_DATE = auto()
    NEXT_STATEMENT_DATE = auto()
    MINIMUM_PAYMENT_DATE = auto()
    GRACE_PERIOD_END = auto()
    LATE_FEE_DATE = auto()
    CYCLE_START_DATE = auto()
    LAST_PAYMENT_DATE = auto()
    OTHER = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        15.0,  # STATEMENT_DATE
        15.0,  # DUE_DATE
        5.0,  # PAYMENT_CUTOFF_DATE
        10.0,  # CLOSE_DATE
        8.0,  # NEXT_STATEMENT_DATE
        10.0,  # MINIMUM_PAYMENT_DATE
        8.0,  # GRACE_PERIOD_END
        5.0,  # LATE_FEE_DATE
        15.0,  # CYCLE_START_DATE
        8.0,  # LAST_PAYMENT_DATE
        1.0  # OTHER
    ]
