from enum import auto

from fsi_data_generator.fsi_generators.helpers import BaseEnum


class EscrowAnalysisStatus(BaseEnum):
    PENDING = auto()
    COMPLETED = auto()
    REVIEWED = auto()
    APPROVED = auto()
    REJECTED = auto()
    IN_PROGRESS = auto()
    CANCELLED = auto()
    CUSTOMER_NOTIFIED = auto()
    ADJUSTMENT_PENDING = auto()
    ADJUSTMENT_APPLIED = auto()
    EXCEPTION = auto()
    EXPIRED = auto()
    OTHER = auto()
