import random
from enum import Enum


class EmploymentType(str, Enum):
    FULL_TIME = "FULL_TIME"
    PART_TIME = "PART_TIME"
    SELF_EMPLOYED = "SELF_EMPLOYED"
    CONTRACTOR = "CONTRACTOR"
    SEASONAL = "SEASONAL"
    COMMISSION = "COMMISSION"
    RETIRED = "RETIRED"
    UNEMPLOYED = "UNEMPLOYED"
    MILITARY = "MILITARY"
    OTHER = "OTHER"

    @classmethod
    def get_random(cls):
        """Return a random status value, weighted toward ACTIVE"""
        choices = [
            (cls.FULL_TIME, 65),
            (cls.PART_TIME, 10),
            (cls.SELF_EMPLOYED, 10),
            (cls.CONTRACTOR, 3),
            (cls.SEASONAL, 2),
            (cls.COMMISSION, 3),
            (cls.RETIRED, 2),
            (cls.UNEMPLOYED, 1),
            (cls.MILITARY, 2),
            (cls.OTHER, 1)
        ]
        return random.choices(
            [status for status, _ in choices],
            weights=[weight for _, weight in choices],
            k=1
        )[0]

