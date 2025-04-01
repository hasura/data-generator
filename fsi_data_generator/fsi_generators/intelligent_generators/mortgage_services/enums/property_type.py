from enum import Enum

import random


class PropertyType(str, Enum):
    """
    Enum for mortgage_services.property_type in the database
    """
    SINGLE_FAMILY = "SINGLE_FAMILY"
    CONDO = "CONDO"
    TOWNHOUSE = "TOWNHOUSE"
    MULTI_FAMILY = "MULTI_FAMILY"
    APARTMENT_BUILDING = "APARTMENT_BUILDING"
    MANUFACTURED_HOME = "MANUFACTURED_HOME"
    COOPERATIVE = "COOPERATIVE"
    PUD = "PUD"
    VACANT_LAND = "VACANT_LAND"
    COMMERCIAL = "COMMERCIAL"
    MIXED_USE = "MIXED_USE"
    FARM = "FARM"
    OTHER = "OTHER"

    @classmethod
    def get_random(cls, product_type=None):
        """
        Return a random property type value, weighted by product type

        Args:
            product_type (str): The loan product type to influence the weighting

        Returns:
            PropertyType: A randomly selected property type
        """
        if product_type == "jumbo":
            # Jumbo loans are often for larger, luxury properties
            choices = [cls.SINGLE_FAMILY, cls.CONDO, cls.TOWNHOUSE, cls.MULTI_FAMILY]
            weights = [0.75, 0.15, 0.05, 0.05]
        elif product_type == "fha":
            # FHA loans are often for modest starter homes
            choices = [cls.SINGLE_FAMILY, cls.CONDO, cls.TOWNHOUSE, cls.MULTI_FAMILY]
            weights = [0.6, 0.2, 0.15, 0.05]
        elif product_type == "va":
            # VA loans typically for residential properties
            choices = [cls.SINGLE_FAMILY, cls.CONDO, cls.TOWNHOUSE, cls.MULTI_FAMILY]
            weights = [0.7, 0.15, 0.1, 0.05]
        elif product_type == "usda":
            # USDA loans are for rural properties
            choices = [cls.SINGLE_FAMILY, cls.MANUFACTURED_HOME, cls.FARM]
            weights = [0.8, 0.15, 0.05]
        elif product_type == "heloc" or product_type == "reverse mortgage":
            # These typically apply to existing homes
            choices = [cls.SINGLE_FAMILY, cls.CONDO, cls.TOWNHOUSE, cls.MULTI_FAMILY]
            weights = [0.75, 0.15, 0.05, 0.05]
        elif product_type == "construction loan":
            # Construction loans are for new builds
            choices = [cls.SINGLE_FAMILY, cls.PUD, cls.CONDO]
            weights = [0.8, 0.15, 0.05]
        else:  # conventional
            choices = [cls.SINGLE_FAMILY, cls.CONDO, cls.TOWNHOUSE, cls.MULTI_FAMILY, cls.MANUFACTURED_HOME]
            weights = [0.65, 0.15, 0.1, 0.05, 0.05]

        return random.choices(choices, weights=weights)[0]
