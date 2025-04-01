from enum import auto
from fsi_data_generator.fsi_generators.helpers import BaseEnum


class DirectDebitCategory(BaseEnum):
    ELECTRICITY = auto()
    GAS = auto()
    WATER = auto()
    INTERNET = auto()
    PHONE = auto()
    TV = auto()
    RENT = auto()
    MORTGAGE = auto()
    INSURANCE_HOME = auto()
    INSURANCE_HEALTH = auto()
    INSURANCE_LIFE = auto()
    INSURANCE_AUTO = auto()
    SUBSCRIPTION_MEDIA = auto()
    SUBSCRIPTION_SOFTWARE = auto()
    SUBSCRIPTION_MEMBERSHIP = auto()
    LOAN_PAYMENT = auto()
    CREDIT_CARD = auto()
    CHARITY = auto()
    TAX_PAYMENT = auto()
    PENSION = auto()
    INVESTMENT = auto()
    EDUCATION = auto()
    OTHER = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        8.0,  # ELECTRICITY
        7.0,  # GAS
        7.0,  # WATER
        10.0,  # INTERNET
        8.0,  # PHONE
        7.0,  # TV
        8.0,  # RENT
        5.0,  # MORTGAGE
        4.0,  # INSURANCE_HOME
        4.0,  # INSURANCE_HEALTH
        2.0,  # INSURANCE_LIFE
        5.0,  # INSURANCE_AUTO
        7.0,  # SUBSCRIPTION_MEDIA
        5.0,  # SUBSCRIPTION_SOFTWARE
        3.0,  # SUBSCRIPTION_MEMBERSHIP
        3.0,  # LOAN_PAYMENT
        4.0,  # CREDIT_CARD
        3.0,  # CHARITY
        2.0,  # TAX_PAYMENT
        2.0,  # PENSION
        1.0,  # INVESTMENT
        3.0,  # EDUCATION
        2.0  # OTHER
    ]
