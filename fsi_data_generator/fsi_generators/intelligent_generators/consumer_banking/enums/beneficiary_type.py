from ....helpers import BaseEnum
from enum import auto


class BeneficiaryType(BaseEnum):
    INDIVIDUAL = auto()
    ORGANIZATION = auto()
    GOVERNMENT = auto()
    TRUST = auto()
    ESTATE = auto()
    CHARITY = auto()
    FINANCIAL_INSTITUTION = auto()
    MERCHANT = auto()
    UTILITY = auto()
    EDUCATIONAL = auto()
    HEALTHCARE = auto()
    SELF = auto()
    OTHER = auto()

    _DEFAULT_WEIGHTS = [
        40.0,  # INDIVIDUAL
        15.0,  # ORGANIZATION
        5.0,  # GOVERNMENT
        3.0,  # TRUST
        2.0,  # ESTATE
        4.0,  # CHARITY
        5.0,  # FINANCIAL_INSTITUTION
        10.0,  # MERCHANT
        7.0,  # UTILITY
        3.0,  # EDUCATIONAL
        4.0,  # HEALTHCARE
        10.0,  # SELF
        2.0  # OTHER
    ]
