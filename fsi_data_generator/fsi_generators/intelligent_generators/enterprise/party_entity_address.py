import logging
import random
from typing import Any, Dict

from data_generator import DataGenerator

logger = logging.getLogger(__name__)


def generate_random_party_entity_address(_id_fields: Dict[str, Any], _dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random enterprise.party_entity_addresses record with reasonable values.

    Args:
        _id_fields: Dictionary containing the required ID fields (enterprise_party_entity_address_id,
                   enterprise_party_id, enterprise_address_id)
        _dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated party_entity_address data (without ID fields)
    """
    # Define relationship types from the enum
    relationship_types = [
        "RESIDENTIAL",
        "MAILING",
        "BUSINESS",
        "BRANCH",
        "BILLING",
        "SHIPPING",
        "LEGAL",
        "SEASONAL",
        "VACATION",
        "PREVIOUS",
        "OTHER"
    ]

    # Choose a relationship type with weighted distribution
    # Some types are more common than others
    weights = {
        "RESIDENTIAL": 0.25,  # Common for individuals
        "MAILING": 0.20,  # Common for everyone
        "BUSINESS": 0.20,  # Common for organizations
        "BRANCH": 0.05,
        "BILLING": 0.10,
        "SHIPPING": 0.07,
        "LEGAL": 0.05,
        "SEASONAL": 0.02,
        "VACATION": 0.02,
        "PREVIOUS": 0.03,
        "OTHER": 0.01
    }

    relationship_type = random.choices(
        population=list(weights.keys()),
        weights=list(weights.values()),
        k=1
    )[0]

    # Create the party_entity_address record
    party_entity_address = {
        "relationship_type": relationship_type
        # enterprise_party_id and enterprise_address_id are not generated here
        # as they would be provided in _id_fields or managed separately
    }

    return party_entity_address
