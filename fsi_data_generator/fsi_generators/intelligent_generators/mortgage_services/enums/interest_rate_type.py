from fsi_data_generator.fsi_generators.helpers import BaseEnum


class InterestRateType(BaseEnum):
    """Enum for interest rate types."""
    FIXED = "FIXED"
    ADJUSTABLE = "ADJUSTABLE"
    HYBRID = "HYBRID"
    INTEREST_ONLY = "INTEREST_ONLY"
    STEP_RATE = "STEP_RATE"
    BALLOON = "BALLOON"
    OTHER = "OTHER"
