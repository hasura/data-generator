from .party_type import PartyType
from enum import Enum

import random


class PartyStatus(Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"
    PENDING = "PENDING"
    SUSPENDED = "SUSPENDED"
    DECEASED = "DECEASED"  # for individuals
    DISSOLVED = "DISSOLVED"  # for organizations

    @classmethod
    def get_random(cls, party_type: PartyType):
        if random.random() < 0.8:
            party_status = PartyStatus.ACTIVE
        else:
            # Choose from remaining statuses
            party_status = random.choice([s for s in cls.valid_statuses(party_type) if s != PartyStatus.ACTIVE])
        return party_status

    @classmethod
    def valid_statuses(cls, party_type: PartyType):
        party_statuses = [party_status for party_status in cls]

        # Select appropriate status options based on party_type
        if party_type == PartyType.INDIVIDUAL:
            valid_statuses = [s for s in party_statuses if s != cls.DISSOLVED]
        else:  # ORGANIZATION
            valid_statuses = [s for s in party_statuses if s != cls.DECEASED]

        return valid_statuses
