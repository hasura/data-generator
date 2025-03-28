from enum import auto

from fsi_data_generator.fsi_generators.helpers import BaseEnum


class AccountStatus(BaseEnum):
    ACTIVE= auto()
    PENDING= auto()
    INACTIVE= auto()
    SUSPENDED= auto()
    DORMANT= auto()
    FROZEN= auto()
    CLOSED= auto()
    ARCHIVED= auto()

    _DEFAULT_WEIGHTS = [0.7, 0.05, 0.05, 0.05, 0.05, 0.05, 0.03, 0.02]
