from enum import auto
from fsi_data_generator.fsi_generators.helpers import BaseEnum


class HardshipReason(BaseEnum):
    FINANCIAL_HARDSHIP = auto()
    JOB_LOSS = auto()
    MEDICAL_ISSUES = auto()
    NATURAL_DISASTER = auto()
    DIVORCE = auto()
    INCOME_REDUCTION = auto()
    DEATH_IN_FAMILY = auto()
    MILITARY_SERVICE = auto()
    BUSINESS_FAILURE = auto()
    DISABILITY = auto()
    INCREASED_EXPENSES = auto()
    RELOCATION = auto()
    PROPERTY_ISSUES = auto()
    OTHER = auto()
