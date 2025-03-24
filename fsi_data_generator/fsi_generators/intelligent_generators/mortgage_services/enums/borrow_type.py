from enum import Enum


class BorrowerType(Enum):
    PRIMARY = "PRIMARY"
    CO_BORROWER = "CO_BORROWER"
    GUARANTOR = "GUARANTOR"
    COSIGNER = "COSIGNER"
