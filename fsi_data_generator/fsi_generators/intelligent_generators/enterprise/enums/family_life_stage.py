from ....helpers import BaseEnum
from enum import auto


class FamilyLifeStage(BaseEnum):
    """Family life stage categories for demographic classification."""
    SINGLE_NO_CHILDREN = auto()  # Single adult without children
    COUPLE_NO_CHILDREN = auto()  # Couple without children
    FAMILY_YOUNG_CHILDREN = auto()  # Family with young children (0-5 years)
    FAMILY_SCHOOL_CHILDREN = auto()  # Family with school-age children (6-17 years)
    FAMILY_ADULT_CHILDREN = auto()  # Family with adult children (18+ years)
    EMPTY_NEST = auto()  # Couple whose children have moved out
    RETIRED = auto()  # Retired individual or couple
    OTHER = auto()  # Other family life stage
    UNKNOWN = auto()  # Family life stage is unknown or not provided

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        20.0,  # SINGLE_NO_CHILDREN
        15.0,  # COUPLE_NO_CHILDREN
        12.0,  # FAMILY_YOUNG_CHILDREN
        15.0,  # FAMILY_SCHOOL_CHILDREN
        10.0,  # FAMILY_ADULT_CHILDREN
        13.0,  # EMPTY_NEST
        10.0,  # RETIRED
        3.0,   # OTHER
        2.0    # UNKNOWN
    ]
