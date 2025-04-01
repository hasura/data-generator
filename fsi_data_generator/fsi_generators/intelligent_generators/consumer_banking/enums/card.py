from enum import auto
from fsi_data_generator.fsi_generators.helpers import BaseEnum


class CardSchemeName(BaseEnum):
    VISA = auto()
    MASTERCARD = auto()
    AMEX = auto()
    DISCOVER = auto()
    DINERS = auto()
    JCB = auto()
    UNIONPAY = auto()
    MAESTRO = auto()
    INTERAC = auto()
    ELO = auto()
    MIR = auto()
    RUPAY = auto()
    OTHER = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        30.0,  # VISA
        25.0,  # MASTERCARD
        10.0,  # AMEX
        8.0,   # DISCOVER
        2.0,   # DINERS
        3.0,   # JCB
        5.0,   # UNIONPAY
        5.0,   # MAESTRO
        3.0,   # INTERAC
        2.0,   # ELO
        2.0,   # MIR
        3.0,   # RUPAY
        2.0    # OTHER
    ]


class AuthorizationType(BaseEnum):
    PIN = auto()
    SIGNATURE = auto()
    PIN_AND_SIGNATURE = auto()
    ONLINE = auto()
    CONTACTLESS = auto()
    CHIP = auto()
    MAGNETIC_STRIPE = auto()
    TOKENIZED = auto()
    BIOMETRIC = auto()
    RECURRING = auto()
    MANUAL_ENTRY = auto()
    OTHER = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        15.0,  # PIN
        10.0,  # SIGNATURE
        5.0,   # PIN_AND_SIGNATURE
        20.0,  # ONLINE
        25.0,  # CONTACTLESS
        15.0,  # CHIP
        5.0,   # MAGNETIC_STRIPE
        10.0,  # TOKENIZED
        3.0,   # BIOMETRIC
        5.0,   # RECURRING
        5.0,   # MANUAL_ENTRY
        2.0    # OTHER
    ]
