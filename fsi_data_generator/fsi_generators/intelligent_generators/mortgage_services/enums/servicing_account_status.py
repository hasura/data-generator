from enum import auto
from fsi_data_generator.fsi_generators.helpers import BaseEnum


class ServicingAccountStatus(BaseEnum):
    ACTIVE = auto()
    DELINQUENT = auto()
    DEFAULT = auto()
    FORECLOSURE = auto()
    BANKRUPTCY = auto()
    PAID_OFF = auto()
    TRANSFERRED = auto()
    MODIFICATION_IN_PROCESS = auto()
    LOSS_MITIGATION = auto()
    FORBEARANCE = auto()
    REO = auto()
    SHORT_SALE = auto()
    CHARGE_OFF = auto()
    SATISFIED = auto()
    SUSPENDED = auto()
