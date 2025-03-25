from enum import auto

from fsi_data_generator.fsi_generators.helpers import BaseEnum


class CreditReportType(BaseEnum):
    TRI_MERGE = auto()
    SINGLE_BUREAU = auto()
    MERGED_BUREAU = auto()
    EXPANDED = auto()
    CUSTOM = auto()
    OTHER = auto()
