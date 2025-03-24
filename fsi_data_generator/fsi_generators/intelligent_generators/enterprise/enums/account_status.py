import random


class AccountStatus:
    """
    Enum-like class for account status values that match the enterprise.account_status enum
    """
    ACTIVE = "ACTIVE"
    PENDING = "PENDING"
    INACTIVE = "INACTIVE"
    SUSPENDED = "SUSPENDED"
    DORMANT = "DORMANT"
    FROZEN = "FROZEN"
    CLOSED = "CLOSED"
    ARCHIVED = "ARCHIVED"

    @classmethod
    def get_random(cls):
        """Return a random status value, weighted toward ACTIVE"""
        choices = [
            (cls.ACTIVE, 70),  # 70% chance of active
            (cls.PENDING, 5),  # 5% chance of pending
            (cls.INACTIVE, 5),  # 5% chance of inactive
            (cls.SUSPENDED, 3),  # 3% chance of suspended
            (cls.DORMANT, 5),  # 5% chance of dormant
            (cls.FROZEN, 2),  # 2% chance of frozen
            (cls.CLOSED, 8),  # 8% chance of closed
            (cls.ARCHIVED, 2)  # 2% chance of archived
        ]
        return random.choices(
            [status for status, _ in choices],
            weights=[weight for _, weight in choices],
            k=1
        )[0]
