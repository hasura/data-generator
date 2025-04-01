from enum import Enum

import random


class VerificationStatus(str, Enum):
    VERIFIED = "VERIFIED"
    PENDING = "PENDING"
    FAILED = "FAILED"
    UNVERIFIED = "UNVERIFIED"
    WAIVED = "WAIVED"
    EXPIRED = "EXPIRED"

    @classmethod
    def get_random(cls, weights: list = None):
        """Return a random status value, weighted toward ACTIVE"""
        choices = [
            (cls.VERIFIED, 70),
            (cls.PENDING, 0),
            (cls.FAILED, 0),
            (cls.UNVERIFIED, 3),
            (cls.WAIVED, 0),
            (cls.EXPIRED, 0),
        ]
        return random.choices(
            [status for status, _ in choices],
            weights=weights if weights else [weight for _, weight in choices],
            k=1
        )[0]
