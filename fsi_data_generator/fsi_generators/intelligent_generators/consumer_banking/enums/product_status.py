from ....helpers import BaseEnum
from enum import auto


class ProductStatus(BaseEnum):
    """Status of banking products in their lifecycle."""
    ACTIVE = auto()
    GRANDFATHERED = auto()
    PROMOTIONAL = auto()
    DISCONTINUED = auto()
    ARCHIVED = auto()
    PILOT = auto()
    SEASONAL = auto()

    # Default weights for random selection
    _DEFAULT_WEIGHTS = [
        70.0,  # ACTIVE
        10.0,  # GRANDFATHERED
        5.0,  # PROMOTIONAL
        5.0,  # DISCONTINUED
        3.0,  # ARCHIVED
        5.0,  # PILOT
        2.0  # SEASONAL
    ]
