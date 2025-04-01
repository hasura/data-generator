from enum import auto
from fsi_data_generator.fsi_generators.helpers import BaseEnum


class AppraisalType(BaseEnum):
    FULL_APPRAISAL = auto()
    DRIVE_BY = auto()
    DESKTOP = auto()
    BPO = auto()
    AVM = auto()
    APPRAISAL_UPDATE = auto()
    FIELD_REVIEW = auto()
    DESK_REVIEW = auto()
    RECERTIFICATION = auto()
    FHA_APPRAISAL = auto()
    VA_APPRAISAL = auto()
    USDA_APPRAISAL = auto()
    OTHER = auto()
