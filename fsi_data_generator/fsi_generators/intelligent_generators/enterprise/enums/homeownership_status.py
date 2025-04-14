from ....helpers import BaseEnum
from enum import auto


class HomeownershipStatus(BaseEnum):
    """Housing status categories for demographic classification."""
    OWNER = auto()  # Owns home outright
    MORTGAGED = auto()  # Owns home with mortgage
    RENTER = auto()  # Rents home
    LIVING_WITH_FAMILY = auto()  # Lives with family members
    OTHER = auto()  # Other housing arrangement
    UNKNOWN = auto()  # Housing status is unknown or not provided

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        20.0,  # OWNER
        35.0,  # MORTGAGED
        30.0,  # RENTER
        10.0,  # LIVING_WITH_FAMILY
        3.0,   # OTHER
        2.0    # UNKNOWN
    ]
