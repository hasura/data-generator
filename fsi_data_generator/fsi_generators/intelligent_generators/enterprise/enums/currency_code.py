from ....helpers import BaseEnum
from enum import auto


class CurrencyCode(BaseEnum):
    """ISO 4217 currency codes for major currencies."""
    USD = auto()  # United States Dollar
    EUR = auto()  # Euro
    GBP = auto()  # British Pound Sterling
    JPY = auto()  # Japanese Yen
    AUD = auto()  # Australian Dollar
    CAD = auto()  # Canadian Dollar
    CHF = auto()  # Swiss Franc
    CNY = auto()  # Chinese Yuan Renminbi
    HKD = auto()  # Hong Kong Dollar
    NZD = auto()  # New Zealand Dollar
    SEK = auto()  # Swedish Krona
    NOK = auto()  # Norwegian Krone
    DKK = auto()  # Danish Krone
    SGD = auto()  # Singapore Dollar
    MXN = auto()  # Mexican Peso
    BRL = auto()  # Brazilian Real
    INR = auto()  # Indian Rupee
    RUB = auto()  # Russian Ruble
    ZAR = auto()  # South African Rand
    TRY = auto()  # Turkish Lira
    KRW = auto()  # South Korean Won
    PLN = auto()  # Polish Zloty
    ILS = auto()  # Israeli Shekel
    AED = auto()  # United Arab Emirates Dirham
    SAR = auto()  # Saudi Riyal
    THB = auto()  # Thai Baht
    MYR = auto()  # Malaysian Ringgit
    IDR = auto()  # Indonesian Rupiah
    PHP = auto()  # Philippine Peso
    ARS = auto()  # Argentine Peso

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        50.0,  # USD
        25.0,  # EUR
        15.0,  # GBP
        12.0,  # JPY
        8.0,  # AUD
        8.0,  # CAD
        7.0,  # CHF
        10.0,  # CNY
        5.0,  # HKD
        4.0,  # NZD
        4.0,  # SEK
        3.0,  # NOK
        3.0,  # DKK
        5.0,  # SGD
        5.0,  # MXN
        5.0,  # BRL
        7.0,  # INR
        4.0,  # RUB
        3.0,  # ZAR
        3.0,  # TRY
        4.0,  # KRW
        3.0,  # PLN
        2.0,  # ILS
        3.0,  # AED
        3.0,  # SAR
        2.0,  # THB
        2.0,  # MYR
        2.0,  # IDR
        2.0,  # PHP
        2.0  # ARS
    ]
