from enum import Enum

import random


class AccountIdentifierScheme(Enum):
    IBAN = "IBAN"
    BIC = "BIC"
    ACCOUNT_NUMBER = "ACCOUNT_NUMBER"
    ROUTING_NUMBER = "ROUTING_NUMBER"
    SORT_CODE = "SORT_CODE"
    CREDIT_CARD = "CREDIT_CARD"
    CLABE = "CLABE"
    BSB = "BSB"
    IFSC = "IFSC"
    CNAPS = "CNAPS"
    LEI = "LEI"
    TAX_ID = "TAX_ID"
    CIF = "CIF"
    DDA = "DDA"
    PROPRIETARY = "PROPRIETARY"
    PASSPORT = "PASSPORT"
    DRIVERS_LICENSE = "DRIVERS_LICENSE"
    NATIONAL_ID = "NATIONAL_ID"
    OTHER = "OTHER"

    @classmethod
    def get_random(cls):
        """
        Get a random account identifier scheme with weighted distribution.
        Some schemes are more common than others.

        Returns:
            AccountIdentifierScheme: A randomly selected account identifier scheme
        """
        weights = {
            cls.IBAN: 0.15,
            cls.BIC: 0.07,
            cls.ACCOUNT_NUMBER: 0.25,
            cls.ROUTING_NUMBER: 0.1,
            cls.SORT_CODE: 0.05,
            cls.CREDIT_CARD: 0.08,
            cls.CLABE: 0.01,
            cls.BSB: 0.01,
            cls.IFSC: 0.01,
            cls.CNAPS: 0.01,
            cls.LEI: 0.03,
            cls.TAX_ID: 0.05,
            cls.CIF: 0.05,
            cls.DDA: 0.05,
            cls.PROPRIETARY: 0.03,
            cls.PASSPORT: 0.01,
            cls.DRIVERS_LICENSE: 0.01,
            cls.NATIONAL_ID: 0.02,
            cls.OTHER: 0.01
        }

        return random.choices(
            population=list(weights.keys()),
            weights=list(weights.values()),
            k=1
        )[0]
