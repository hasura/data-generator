from ....helpers import BaseEnum
from enum import auto


class IdentifierScheme(BaseEnum):
    IBAN = auto()
    BIC = auto()
    ACCOUNT_NUMBER = auto()
    ROUTING_NUMBER = auto()
    SORT_CODE = auto()
    CREDIT_CARD = auto()
    CLABE = auto()
    BSB = auto()
    IFSC = auto()
    CNAPS = auto()
    LEI = auto()
    TAX_ID = auto()
    CIF = auto()
    DDA = auto()
    PROPRIETARY = auto()
    PASSPORT = auto()
    DRIVERS_LICENSE = auto()
    NATIONAL_ID = auto()
    OTHER = auto()

    _DEFAULT_WEIGHTS = [
        15.0,  # IBAN - Common in international banking
        12.0,  # BIC - SWIFT usage, also very common
        10.0,  # ACCOUNT_NUMBER - Generic
        7.0,   # ROUTING_NUMBER - Common in US
        6.0,   # SORT_CODE - Common in UK
        5.0,   # CREDIT_CARD - Specific to card identifiers
        4.0,   # CLABE - Mexico
        3.0,   # BSB - Australia
        3.0,   # IFSC - India
        3.0,   # CNAPS - China
        3.0,   # LEI - Legal Entity ID
        4.0,   # TAX_ID - Common for individuals
        2.0,   # CIF - Internal bank identifier
        2.0,   # DDA - Specific to checking accounts
        2.0,   # PROPRIETARY - Rare custom format
        3.0,   # PASSPORT - Identity verification
        3.0,   # DRIVERS_LICENSE - Identity verification
        3.0,   # NATIONAL_ID - Country-specific
        2.0    # OTHER - Catchall
    ]
