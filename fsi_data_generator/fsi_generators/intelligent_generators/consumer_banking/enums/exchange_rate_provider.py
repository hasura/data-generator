from ....helpers import BaseEnum
from enum import auto


class ExchangeRateProvider(BaseEnum):
    """Provider of exchange rate used for currency conversion."""
    BANK = auto()
    VISA = auto()
    MASTERCARD = auto()
    AMEX = auto()
    REUTERS = auto()
    BLOOMBERG = auto()
    ECB = auto()
    FEDERAL_RESERVE = auto()
    CUSTOM = auto()
    OTHER = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        15.0,  # BANK
        25.0,  # VISA
        25.0,  # MASTERCARD
        10.0,  # AMEX
        5.0,  # REUTERS
        5.0,  # BLOOMBERG
        5.0,  # ECB
        5.0,  # FEDERAL_RESERVE
        3.0,  # CUSTOM
        2.0  # OTHER
    ]
