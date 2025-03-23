import random
from enum import Enum


class AgentStatus(str, Enum):
    """
    Enumeration of host agent statuses in the security schema
    as defined in the DBML
    """
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    PENDING = "PENDING"
    ERROR = "ERROR"
    DISCONNECTED = "DISCONNECTED"

    @classmethod
    def get_random(cls):
        """
        Return an agent status with realistic distribution
        """
        weights = {
            cls.ACTIVE: 0.7,
            cls.INACTIVE: 0.1,
            cls.PENDING: 0.1,
            cls.ERROR: 0.05,
            cls.DISCONNECTED: 0.05
        }
        return random.choices(
            list(weights.keys()),
            weights=list(weights.values()),
            k=1
        )[0]

    def to_display_value(self):
        """
        Convert enum value to lowercase display format
        """
        return self.value.lower()
