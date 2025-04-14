from ....helpers import BaseEnum
from enum import auto


class IncomeBracket(BaseEnum):
    """Income brackets for demographic classification."""
    UNDER_15K = auto()  # Annual income under $15,000
    INCOME_15K_25K = auto()  # Annual income between $15,000 and $24,999
    INCOME_25K_35K = auto()  # Annual income between $25,000 and $34,999
    INCOME_35K_50K = auto()  # Annual income between $35,000 and $49,999
    INCOME_50K_75K = auto()  # Annual income between $50,000 and $74,999
    INCOME_75K_100K = auto()  # Annual income between $75,000 and $99,999
    INCOME_100K_150K = auto()  # Annual income between $100,000 and $149,999
    INCOME_150K_200K = auto()  # Annual income between $150,000 and $199,999
    INCOME_200K_250K = auto()  # Annual income between $200,000 and $249,999
    INCOME_250K_PLUS = auto()  # Annual income $250,000 and above
    UNKNOWN = auto()  # Income is unknown or not provided

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        10.0,  # UNDER_15K
        12.0,  # INCOME_15K_25K
        14.0,  # INCOME_25K_35K
        16.0,  # INCOME_35K_50K
        18.0,  # INCOME_50K_75K
        12.0,  # INCOME_75K_100K
        8.0,   # INCOME_100K_150K
        4.0,   # INCOME_150K_200K
        2.0,   # INCOME_200K_250K
        1.0,   # INCOME_250K_PLUS
        3.0    # UNKNOWN
    ]
