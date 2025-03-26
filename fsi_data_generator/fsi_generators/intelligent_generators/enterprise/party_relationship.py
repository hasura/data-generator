import logging
import random
from typing import Any, Dict

from data_generator import DataGenerator
from .enums import PartyRelationshipType

logger = logging.getLogger(__name__)


def generate_random_party_relationship(_id_fields: Dict[str, Any], _dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random enterprise.party_relationships record with reasonable values.

    Args:
        _id_fields: Dictionary containing the required ID fields (enterprise_party_relationship_id,
                    enterprise_party_id, related_party_id)
        _dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated party_relationship data (without ID fields)
    """

    # Choose a relationship type with weighted distribution
    # Some types are more common than others
    weights = {
        PartyRelationshipType.POWER_OF_ATTORNEY: 0.05,
        PartyRelationshipType.GUARDIAN: 0.03,
        PartyRelationshipType.TRUSTEE: 0.04,
        PartyRelationshipType.BENEFICIARY: 0.1,
        PartyRelationshipType.EXECUTOR: 0.02,
        PartyRelationshipType.CUSTODIAN: 0.02,
        PartyRelationshipType.AUTHORIZED_USER: 0.1,
        PartyRelationshipType.BUSINESS_PARTNER: 0.08,
        PartyRelationshipType.SPOUSE: 0.15,
        PartyRelationshipType.DEPENDENT: 0.07,
        PartyRelationshipType.CO_SIGNER: 0.06,
        PartyRelationshipType.EMPLOYER_EMPLOYEE: 0.07,
        PartyRelationshipType.AGENT: 0.04,
        PartyRelationshipType.PARENT_CHILD: 0.1,
        PartyRelationshipType.SIBLING: 0.05,
        PartyRelationshipType.CORPORATE_OFFICER: 0.03,
        PartyRelationshipType.MEMBER: 0.04,
        PartyRelationshipType.OWNER: 0.04,
        PartyRelationshipType.OTHER: 0.01
    }

    relationship_type = random.choices(
        population=list(weights.keys()),
        weights=list(weights.values()),
        k=1
    )[0]

    # For priority, assume most relationships are primary (1)
    # with decreasing likelihood of higher priority numbers
    priority_weights = [0.70, 0.20, 0.05, 0.03, 0.02]  # Weights for priorities 1-5
    priority = random.choices(
        population=range(1, 6),
        weights=priority_weights,
        k=1
    )[0]

    # Create the party_relationship record
    party_relationship = {
        "relationship_type": relationship_type.value,
        "priority": priority
        # enterprise_party_id and related_party_id are not generated here
        # as they would be provided in _id_fields or managed separately
    }

    return party_relationship
