import random
from enum import Enum


class BaseEnum(Enum):
    @classmethod
    def get_random(cls):
        """Returns a random member of the Enum."""
        return random.choice(list(cls))
