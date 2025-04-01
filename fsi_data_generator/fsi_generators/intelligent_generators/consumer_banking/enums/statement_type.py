from ....helpers import BaseEnum
from enum import auto


class StatementType(BaseEnum):
    """Types of account statements."""
    REGULAR = auto()
    INTERIM = auto()
    FINAL = auto()
    ANNUAL = auto()
    SUPPLEMENTARY = auto()
    TAX = auto()
    CORRECTED = auto()
    RECONCILIATION = auto()
    CONSOLIDATED = auto()
    OTHER = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        65.0,  # REGULAR
        10.0,  # INTERIM
        3.0,  # FINAL
        7.0,  # ANNUAL
        3.0,  # SUPPLEMENTARY
        5.0,  # TAX
        2.0,  # CORRECTED
        2.0,  # RECONCILIATION
        2.0,  # CONSOLIDATED
        1.0  # OTHER
    ]
