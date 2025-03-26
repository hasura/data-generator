from enum import auto

from fsi_data_generator.fsi_generators.helpers import BaseEnum


class PaymentType(BaseEnum):
    PRINCIPAL_AND_INTEREST= auto()
    PRINCIPAL_ONLY= auto()
    INTEREST_ONLY= auto()
    ESCROW= auto()
    LATE_FEE= auto()
    PREPAYMENT_PENALTY= auto()
    FULL_PAYOFF= auto()
    PARTIAL_PAYMENT= auto()
    BIWEEKLY= auto()
    FORBEARANCE= auto()
    LOAN_MODIFICATION= auto()
    BALLOON= auto()
    SERVICING_FEE= auto()
    EXTENSION_FEE= auto()
    OTHER= auto()
