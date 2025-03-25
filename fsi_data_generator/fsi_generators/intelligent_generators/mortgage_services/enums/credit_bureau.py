from enum import auto

from fsi_data_generator.fsi_generators.helpers import BaseEnum


class CreditBureau(BaseEnum):
    EQUIFAX = auto()
    EXPERIAN = auto()
    TRANSUNION = auto()
    INNOVIS = auto()
    CLEAR_REPORT = auto()
    OTHER = auto()
