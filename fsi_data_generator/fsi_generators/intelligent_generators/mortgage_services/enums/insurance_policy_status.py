from enum import auto

from fsi_data_generator.fsi_generators.helpers import BaseEnum


class InsurancePolicyStatus(BaseEnum):
    ACTIVE = auto()
    PENDING = auto()
    EXPIRED = auto()
    CANCELLED = auto()
    RENEWED = auto()
    LAPSED = auto()
    REINSTATED = auto()
    FORCE_PLACED = auto()
    UNDER_REVIEW = auto()
    CLAIM_IN_PROGRESS = auto()
    NON_RENEWAL = auto()
    OTHER = auto()
