from enum import auto
from fsi_data_generator.fsi_generators.helpers import BaseEnum


class DisclosureType(BaseEnum):
    LOAN_ESTIMATE = auto()
    CLOSING_DISCLOSURE = auto()
    CHANGE_IN_TERMS = auto()
    REVISED_CLOSING_DISCLOSURE = auto()
    CORRECTED_CLOSING_DISCLOSURE = auto()
    FEE_ESTIMATE = auto()
    INITIAL_ESCROW_STATEMENT = auto()
    OTHER = auto()
