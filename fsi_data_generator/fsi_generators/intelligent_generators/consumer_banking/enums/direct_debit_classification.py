from enum import auto
from fsi_data_generator.fsi_generators.helpers import BaseEnum


class DirectDebitClassification(BaseEnum):
    PERSONAL = auto()
    BUSINESS = auto()
    CHARITY = auto()
    HOUSEHOLD = auto()
    SUBSCRIPTION = auto()
    UTILITY = auto()
    INSURANCE = auto()
    MORTGAGE = auto()
    LOAN = auto()
    TAX = auto()
    OTHER = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        30.0,  # PERSONAL
        10.0,  # BUSINESS
        5.0,  # CHARITY
        15.0,  # HOUSEHOLD
        15.0,  # SUBSCRIPTION
        10.0,  # UTILITY
        5.0,  # INSURANCE
        3.0,  # MORTGAGE
        3.0,  # LOAN
        2.0,  # TAX
        2.0  # OTHER
    ]
