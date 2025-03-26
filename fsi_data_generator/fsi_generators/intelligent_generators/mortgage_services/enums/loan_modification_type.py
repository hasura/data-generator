from enum import auto

from fsi_data_generator.fsi_generators.helpers import BaseEnum


class LoanModificationType(BaseEnum):
    RATE_REDUCTION = auto()
    TERM_EXTENSION = auto()
    PRINCIPAL_REDUCTION = auto()
    INTEREST_ONLY_PERIOD = auto()
    CAPITALIZATION = auto()
    PAYMENT_DEFERRAL = auto()
    FORBEARANCE = auto()
    WORKOUT = auto()
    REFINANCE = auto()
    PRINCIPAL_FORGIVENESS = auto()
    BALLOON_MODIFICATION = auto()
    STEP_RATE = auto()
    OTHER = auto()
