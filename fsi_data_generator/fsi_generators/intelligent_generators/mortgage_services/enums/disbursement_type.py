from enum import auto

from fsi_data_generator.fsi_generators.helpers import BaseEnum


class DisbursementType(BaseEnum):
    PROPERTY_TAX = auto()
    HOMEOWNERS_INSURANCE = auto()
    MORTGAGE_INSURANCE = auto()
    FLOOD_INSURANCE = auto()
    HOA_DUES = auto()
    HAZARD_INSURANCE = auto()
    CONDO_INSURANCE = auto()
    CITY_TAX = auto()
    COUNTY_TAX = auto()
    SCHOOL_TAX = auto()
    SPECIAL_ASSESSMENT = auto()
    GROUND_RENT = auto()
    ESCROW_REFUND = auto()
    ESCROW_SHORTAGE = auto()
    OTHER = auto()

    _DEFAULT_WEIGHTS = [0.4, 0.3, 0.1, 0.1, 0.05, 0.05, 0, 0, 0, 0, 0, 0, 0, 0, 0]
