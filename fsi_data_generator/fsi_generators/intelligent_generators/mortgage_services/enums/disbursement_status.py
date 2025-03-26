from enum import auto

from fsi_data_generator.fsi_generators.helpers import BaseEnum


class DisbursementStatus(BaseEnum):
    PENDING = auto()
    PROCESSING = auto()
    COMPLETED = auto()
    FAILED = auto()
    RETURNED = auto()
    CANCELED = auto()
    HOLD = auto()
    CLEARED = auto()
    VOID = auto()
    REISSUED = auto()
    PARTIAL = auto()
    SCHEDULED = auto()
    SENT = auto()
    OTHER = auto()
