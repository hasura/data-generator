from enum import auto

from fsi_data_generator.fsi_generators.helpers import BaseEnum


class AppraisalStatus(BaseEnum):
    ORDERED = auto()
    ASSIGNED = auto()
    SCHEDULED = auto()
    INSPECTION_COMPLETED = auto()
    IN_PROGRESS = auto()
    SUBMITTED = auto()
    UNDER_REVIEW = auto()
    REVISION_NEEDED = auto()
    COMPLETED = auto()
    REJECTED = auto()
    CANCELLED = auto()
    EXPIRED = auto()
    OTHER = auto()
