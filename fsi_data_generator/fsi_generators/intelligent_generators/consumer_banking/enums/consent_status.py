from enum import auto

from fsi_data_generator.fsi_generators.helpers import BaseEnum


class ConsentStatus(BaseEnum):
    PENDING = auto()
    AUTHORIZED = auto()
    ACTIVE = auto()
    SUSPENDED = auto()
    EXPIRED = auto()
    REVOKED = auto()
    TERMINATED = auto()
    SUPERSEDED = auto()
    REJECTED = auto()
    ERROR = auto()

    _DEFAULT_WEIGHTS = [0.05, 0.1, 0.5, 0.05, 0.05, 0.1, 0.05, 0.03, 0.05, 0.02]
