from fsi_data_generator.fsi_generators.helpers import BaseEnum


class MaritalStatus(BaseEnum):
    SINGLE = "SINGLE"
    MARRIED = "MARRIED"
    DOMESTIC_PARTNERSHIP = "DOMESTIC_PARTNERSHIP"
    SEPARATED = "SEPARATED"
    DIVORCED = "DIVORCED"
    WIDOWED = "WIDOWED"
    NOT_SPECIFIED = "NOT_SPECIFIED"
