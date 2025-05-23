from fsi_data_generator.fsi_generators.helpers import BaseEnum


class IncomeType(BaseEnum):
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

    _DEFAULT_WEIGHTS = [
        0.50,  # SALARY
        0.06,  # BONUS
        0.05,  # COMMISSION
        0.05,  # OVERTIME
        0.10,  # SELF_EMPLOYMENT
        0.05,  # RENTAL
        0.03,  # INVESTMENT
        0.03,  # RETIREMENT
        0.02,  # PENSION
        0.03,  # SOCIAL_SECURITY
        0.01,  # DISABILITY
        0.01,  # ALIMONY
        0.01,  # CHILD_SUPPORT
        0.01,  # TRUST
        0.01,  # GOVERNMENT_ASSISTANCE
        0.01,  # ROYALTIES
        0.02  # OTHER
    ]
