# First, create a new file called building_type.py
import random
from enum import Enum


class BuildingType(Enum):
    BRANCH = "BRANCH"
    HEADQUARTERS = "HEADQUARTERS"
    OPERATIONS_CENTER = "OPERATIONS_CENTER"
    DATA_CENTER = "DATA_CENTER"
    ADMINISTRATIVE = "ADMINISTRATIVE"
    WAREHOUSE = "WAREHOUSE"
    TRAINING_CENTER = "TRAINING_CENTER"
    DISASTER_RECOVERY = "DISASTER_RECOVERY"
    CALL_CENTER = "CALL_CENTER"
    ATM_LOCATION = "ATM_LOCATION"
    OTHER = "OTHER"

    @classmethod
    def get_random(cls):
        type_weights = {
            cls.BRANCH: 0.5,  # 50% chance
            cls.HEADQUARTERS: 0.05,  # 5% chance
            cls.OPERATIONS_CENTER: 0.1,
            cls.DATA_CENTER: 0.05,
            cls.ADMINISTRATIVE: 0.1,
            cls.WAREHOUSE: 0.05,
            cls.TRAINING_CENTER: 0.03,
            cls.DISASTER_RECOVERY: 0.02,
            cls.CALL_CENTER: 0.05,
            cls.ATM_LOCATION: 0.03,
            cls.OTHER: 0.02
        }

        return random.choices(
            population=list(type_weights.keys()),
            weights=list(type_weights.values()),
            k=1
        )[0]
