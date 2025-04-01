from enum import Enum

import random


class OccupancyType(str, Enum):
    """
    Enum for mortgage_services.occupancy_type in the database
    """
    PRIMARY_RESIDENCE = "PRIMARY_RESIDENCE"
    SECONDARY_RESIDENCE = "SECONDARY_RESIDENCE"
    INVESTMENT = "INVESTMENT"
    NOT_APPLICABLE = "NOT_APPLICABLE"

    @classmethod
    def get_random(cls, loan_purpose=None):
        """
        Return a random occupancy type value, weighted based on loan purpose

        Args:
            loan_purpose (str): The loan purpose to influence the weighting

        Returns:
            OccupancyType: A randomly selected occupancy type
        """
        if loan_purpose == "primary residence":
            return cls.PRIMARY_RESIDENCE
        elif loan_purpose == "second home":
            return cls.SECONDARY_RESIDENCE
        elif loan_purpose == "investment property":
            return cls.INVESTMENT
        elif loan_purpose == "home improvement" and random.random() < 0.9:
            return cls.PRIMARY_RESIDENCE  # Most home improvement loans are for primary homes
        elif loan_purpose in ["refinancing", "cash-out refinancing"]:
            # For refinancing, use the original occupancy of the home
            choices = [cls.PRIMARY_RESIDENCE, cls.SECONDARY_RESIDENCE, cls.INVESTMENT]
            weights = [0.8, 0.15, 0.05]  # Most refinances are for primary homes
            return random.choices(choices, weights=weights)[0]
        else:
            # Default or fallback based on weighted probabilities
            choices = [cls.PRIMARY_RESIDENCE, cls.SECONDARY_RESIDENCE, cls.INVESTMENT]
            weights = [0.7, 0.15, 0.15]
            return random.choices(choices, weights=weights)[0]
