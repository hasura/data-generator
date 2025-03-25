import random
from typing import List, Optional

from fsi_data_generator.fsi_generators.helpers.auto_name import AutoName


class BaseEnum(AutoName):
    """
    Base class for custom enums with additional utility methods.
    """

    @classmethod
    def get_random(cls, weights: Optional[List[float]] = None) -> 'BaseEnum':
        """
        Get a random enum value, optionally with weighted probabilities.

        Args:
            weights (Optional[List[float]]): Optional list of weights for each enum value.
                If not provided, equal weights are used.

        Returns:
            BaseEnum: Randomly selected enum value
        """
        if weights is None:
            return random.choice(list(cls))

        # Validate weights match the number of enum values
        if len(weights) != len(cls):
            raise ValueError(f"Number of weights must match number of enum values ({len(cls)})")

        return random.choices(list(cls), weights=weights)[0]
