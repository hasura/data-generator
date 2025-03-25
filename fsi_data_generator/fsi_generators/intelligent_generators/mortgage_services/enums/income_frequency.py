import random
from enum import Enum


class IncomeFrequency(str, Enum):
    WEEKLY = "WEEKLY"
    BI_WEEKLY = "BI_WEEKLY"
    SEMI_MONTHLY = "SEMI_MONTHLY"
    MONTHLY = "MONTHLY"
    QUARTERLY = "QUARTERLY"
    SEMI_ANNUALLY = "SEMI_ANNUALLY"
    ANNUALLY = "ANNUALLY"
    IRREGULAR = "IRREGULAR"

    @classmethod
    def get_random(cls):
        """Return a random status value, weighted toward ACTIVE"""
        choices = [income_type for income_type in cls]
        weights = [0.1, 0.25, 0.15, 0.3, 0.05, 0.03, 0.07, 0.05]
        return random.choices(choices, weights=weights, k=1)[0]
