from ....helpers import BaseEnum
from enum import auto


class AccountStatus(BaseEnum):
    ACTIVE = auto()
    PENDING = auto()
    INACTIVE = auto()
    SUSPENDED = auto()
    DORMANT = auto()
    FROZEN = auto()
    CLOSED = auto()
    ARCHIVED = auto()

    _DEFAULT_WEIGHTS = [0.7, 0.05, 0.05, 0.05, 0.05, 0.05, 0.03, 0.02]
