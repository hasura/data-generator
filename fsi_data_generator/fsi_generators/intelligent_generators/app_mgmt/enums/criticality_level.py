from ....helpers import BaseEnum
from enum import auto


class CriticalityLevel(BaseEnum):
    """
    Enum representing the criticality levels of application relationships.

    Each level indicates the impact of a relationship failure and recommended resolution timeframe.
    """
    NONE = auto()  # No impact: Resolution timeframe - Not applicable
    MINIMAL = auto()  # Minimal impact: Resolution timeframe - Within a week
    MINOR = auto()  # Minor impact: Resolution timeframe - Within 1-2 business days
    MODERATE = auto()  # Moderate impact: Resolution timeframe - Within 4-8 hours
    SIGNIFICANT = auto()  # Significant impact: Resolution timeframe - Within 1-2 hours
    CRITICAL = auto()  # Critical impact: Resolution timeframe - Immediately (15-30 minutes)

    _DEFAULT_WEIGHTS = [
        5.0,  # NONE
        10.0,  # MINIMAL
        20.0,  # MINOR
        30.0,  # MODERATE
        25.0,  # SIGNIFICANT
        10.0  # CRITICAL
    ]
