from fsi_data_generator.fsi_generators.helpers import BaseEnum


class LoanPurpose(BaseEnum):
    """Enum for loan purposes."""
    PRIMARY_RESIDENCE = "PRIMARY_RESIDENCE"
    SECOND_HOME = "SECOND_HOME"
    INVESTMENT_PROPERTY = "INVESTMENT_PROPERTY"
    RENTAL = "RENTAL"
    VACATION_HOME = "VACATION_HOME"
    MULTI_FAMILY = "MULTI_FAMILY"
    RELOCATION = "RELOCATION"
    OTHER = "OTHER"
