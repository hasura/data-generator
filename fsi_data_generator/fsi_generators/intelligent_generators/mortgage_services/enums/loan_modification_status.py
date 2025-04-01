from enum import auto
from fsi_data_generator.fsi_generators.helpers import BaseEnum


class LoanModificationStatus(BaseEnum):
    PENDING = auto()
    APPROVED = auto()
    DENIED = auto()
    COMPLETED = auto()
    IN_PROGRESS = auto()
    SUSPENDED = auto()
    PARTIAL = auto()
    CANCELED = auto()
    EXPIRED = auto()
    TRIAL_PERIOD = auto()
    BORROWER_ACCEPTED = auto()
    BORROWER_REJECTED = auto()
    OTHER = auto()
