from ....helpers import BaseEnum
from enum import auto


class Frequency(BaseEnum):
    WEEKLY = auto()
    BI_WEEKLY = auto()
    SEMI_MONTHLY = auto()
    MONTHLY = auto()
    QUARTERLY = auto()
    SEMI_ANNUALLY = auto()
    ANNUALLY = auto()
    IRREGULAR = auto()
    ONE_TIME = auto()
    DAILY = auto()
    CUSTOM = auto()
    OTHER = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        5.0,  # WEEKLY
        10.0,  # BI_WEEKLY
        8.0,  # SEMI_MONTHLY
        50.0,  # MONTHLY
        15.0,  # QUARTERLY
        5.0,  # SEMI_ANNUALLY
        5.0,  # ANNUALLY
        2.0,  # IRREGULAR
        3.0,  # ONE_TIME
        1.0,  # DAILY
        0.5,  # CUSTOM
        0.5  # OTHER
    ]
