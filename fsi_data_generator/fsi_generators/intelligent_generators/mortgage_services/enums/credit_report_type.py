from enum import auto

from fsi_data_generator.fsi_generators.helpers import BaseEnum


class CreditReportType(BaseEnum):
    TRI_MERGE = auto()
    SINGLE_BUREAU = auto()
    MERGED_BUREAU = auto()
    EXPANDED = auto()
    CUSTOM = auto()
    OTHER = auto()

    _DEFAULT_WEIGHTS = [0.4, 0.3, 0.15, 0.1, 0.025, 0.025]  # Favoring TRI_MERGE and SINGLE_BUREAU
