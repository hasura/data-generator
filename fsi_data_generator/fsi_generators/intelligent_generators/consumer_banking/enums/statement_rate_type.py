from enum import auto
from fsi_data_generator.fsi_generators.helpers import BaseEnum


class StatementRateType(BaseEnum):
    """Types of statement rates."""
    APR = auto()
    CASH_ADVANCE_APR = auto()
    BALANCE_TRANSFER_APR = auto()
    PENALTY_APR = auto()
    PROMOTIONAL_APR = auto()
    SAVINGS_RATE = auto()
    CD_RATE = auto()
    EXCHANGE_RATE = auto()
    INTRODUCTORY_RATE = auto()
    VARIABLE_RATE_INDEX = auto()
    MARGIN = auto()
    DEFAULT_RATE = auto()
    REWARD_RATE = auto()
    EFFECTIVE_RATE = auto()
    OTHER = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        20.0,  # APR
        12.0,  # CASH_ADVANCE_APR
        12.0,  # BALANCE_TRANSFER_APR
        8.0,  # PENALTY_APR
        10.0,  # PROMOTIONAL_APR
        5.0,  # SAVINGS_RATE
        3.0,  # CD_RATE
        5.0,  # EXCHANGE_RATE
        8.0,  # INTRODUCTORY_RATE
        3.0,  # VARIABLE_RATE_INDEX
        3.0,  # MARGIN
        2.0,  # DEFAULT_RATE
        5.0,  # REWARD_RATE
        3.0,  # EFFECTIVE_RATE
        1.0  # OTHER
    ]
