from ....helpers import BaseEnum
from enum import auto


class PoliticalAffiliation(BaseEnum):
    """Political affiliation categories for demographic classification."""
    DEMOCRAT = auto()  # Affiliated with Democratic party
    REPUBLICAN = auto()  # Affiliated with Republican party
    INDEPENDENT = auto()  # Identifies as politically independent
    LIBERTARIAN = auto()  # Affiliated with Libertarian party
    GREEN = auto()  # Affiliated with Green party
    OTHER = auto()  # Other political affiliation
    NONE = auto()  # No political affiliation
    UNKNOWN = auto()  # Political affiliation is unknown or not provided

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        30.0,  # DEMOCRAT
        30.0,  # REPUBLICAN
        25.0,  # INDEPENDENT
        3.0,   # LIBERTARIAN
        2.0,   # GREEN
        3.0,   # OTHER
        5.0,   # NONE
        2.0    # UNKNOWN
    ]
