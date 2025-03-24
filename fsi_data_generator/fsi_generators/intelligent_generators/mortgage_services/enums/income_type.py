import random
from enum import Enum


class IncomeType(str, Enum):
    SALARY = "SALARY"
    BONUS = "BONUS"
    COMMISSION = "COMMISSION"
    OVERTIME = "OVERTIME"
    SELF_EMPLOYMENT = "SELF_EMPLOYMENT"
    RENTAL = "RENTAL"
    INVESTMENT = "INVESTMENT"
    RETIREMENT = "RETIREMENT"
    PENSION = "PENSION"
    SOCIAL_SECURITY = "SOCIAL_SECURITY"
    DISABILITY = "DISABILITY"
    ALIMONY = "ALIMONY"
    CHILD_SUPPORT = "CHILD_SUPPORT"
    TRUST = "TRUST"
    GOVERNMENT_ASSISTANCE = "GOVERNMENT_ASSISTANCE"
    ROYALTIES = "ROYALTIES"
    OTHER = "OTHER"

    @classmethod
    def get_random(cls):
        """Return a random status value, weighted toward ACTIVE"""
        choices = [income_type for income_type in cls]
        weights = [0.3, 0.08, 0.07, 0.05, 0.1, 0.1, 0.05, 0.05, 0.03, 0.04, 0.02, 0.02, 0.02, 0.01, 0.02, 0.01,
                           0.03]
        return random.choices(choices,weights=weights,k=1)[0]
