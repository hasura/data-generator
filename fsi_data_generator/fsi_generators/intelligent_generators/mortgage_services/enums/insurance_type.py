from enum import auto

from fsi_data_generator.fsi_generators.helpers import BaseEnum


class InsuranceType(BaseEnum):
    HAZARD = auto()
    FLOOD = auto()
    WIND = auto()
    EARTHQUAKE = auto()
    PMI = auto()
    LENDERS_PLACED = auto()
    OTHER = auto()
