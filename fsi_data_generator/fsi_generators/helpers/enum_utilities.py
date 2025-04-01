from typing import List, Optional

import random


class EnumUtilities:
    """
    Mixin class to provide utility methods for Enums.
    This includes methods like `get_random()`.
    """
    _DEFAULT_WEIGHTS: Optional[List[float]] = None

    @classmethod
    def get_random(cls, weights: Optional[List[float]] = None):
        """
        Get a random member of the enum, optionally using weights.

        Args:
            weights (Optional[List[float]]): A list of weights for weighted random selection.

        Returns:
            The randomly selected enum member.
        """
        # Get all enum members
        enum_members = [member for member in cls if not member.name.startswith("_")]

        # If no weights are provided, fall back to DEFAULT_WEIGHTS or uniform distribution
        weights = weights or (cls._DEFAULT_WEIGHTS and cls._DEFAULT_WEIGHTS.value)
        if weights is None:
            return random.choice(enum_members)

        # Ensure weights match number of enum members
        if len(weights) != len(enum_members):
            raise ValueError(
                f"Number of weights ({len(weights)}) must match the number of enum values ({len(enum_members)})")

        # Perform weighted random choice
        return random.choices(enum_members, weights=weights)[0]
