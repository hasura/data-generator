from enum import auto
from fsi_data_generator.fsi_generators.helpers import BaseEnum


class DirectDebitStatusCode(BaseEnum):
    ACTIVE = auto()
    PENDING = auto()
    CANCELED = auto()
    SUSPENDED = auto()
    REJECTED = auto()
    EXPIRED = auto()
    COMPLETED = auto()
    FAILED = auto()
    ON_HOLD = auto()
    AMENDED = auto()
    OTHER = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        50.0,  # ACTIVE
        10.0,  # PENDING
        15.0,  # CANCELED
        5.0,  # SUSPENDED
        3.0,  # REJECTED
        5.0,  # EXPIRED
        5.0,  # COMPLETED
        3.0,  # FAILED
        2.0,  # ON_HOLD
        1.0,  # AMENDED
        1.0  # OTHER
    ]
