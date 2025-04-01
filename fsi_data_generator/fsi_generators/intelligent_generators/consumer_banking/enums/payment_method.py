from ....helpers import BaseEnum
from enum import auto


class PaymentMethod(BaseEnum):
    """Methods for executing payments."""
    ACH = auto()
    WIRE = auto()
    INTERNAL = auto()
    CHECK = auto()
    CARD = auto()
    DIGITAL_WALLET = auto()
    OTHER = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        35.0,  # ACH
        10.0,  # WIRE
        25.0,  # INTERNAL
        15.0,  # CHECK
        8.0,  # CARD
        5.0,  # DIGITAL_WALLET
        2.0  # OTHER
    ]
