from fsi_data_generator.fsi_generators.helpers import BaseEnum


class LoanType(BaseEnum):
    """Enum for mortgage loan types."""
    CONVENTIONAL = "CONVENTIONAL"
    FHA = "FHA"
    VA = "VA"
    USDA = "USDA"
    JUMBO = "JUMBO"
    CONSTRUCTION = "CONSTRUCTION"
    HOME_EQUITY = "HOME_EQUITY"
    REFINANCE = "REFINANCE"
    REVERSE_MORTGAGE = "REVERSE_MORTGAGE"
    OTHER = "OTHER"
