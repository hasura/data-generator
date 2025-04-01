from enum import auto
from fsi_data_generator.fsi_generators.helpers import BaseEnum


class ConditionStatus(BaseEnum):
    PENDING = auto()
    IN_PROCESS = auto()
    SUBMITTED = auto()
    ACCEPTED = auto()
    REJECTED = auto()
    WAIVED = auto()
    EXPIRED = auto()
    CLEARED = auto()
    OTHER = auto()
