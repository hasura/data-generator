from fsi_data_generator.fsi_generators.helpers import BaseEnum


class ApplicationType(BaseEnum):
    """Enum for mortgage application types."""
    PURCHASE = "PURCHASE"
    REFINANCE = "REFINANCE"
    CASH_OUT = "CASH_OUT"
    CONSTRUCTION = "CONSTRUCTION"
    HOME_IMPROVEMENT = "HOME_IMPROVEMENT"
    RENOVATION = "RENOVATION"
    REVERSE_MORTGAGE = "REVERSE_MORTGAGE"
    JUMBO = "JUMBO"
    FHA = "FHA"
    VA = "VA"
    USDA = "USDA"
    LAND = "LAND"
    OTHER = "OTHER"
