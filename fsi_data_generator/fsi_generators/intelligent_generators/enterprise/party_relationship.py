import logging
import random
from typing import Any, Dict

from data_generator import DataGenerator

logger = logging.getLogger(__name__)


def generate_random_party_relationship(_id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random enterprise.party_relationships record with reasonable values.

    Args:
        _id_fields: Dictionary containing the required ID fields (enterprise_party_relationship_id,
                    enterprise_party_id, related_party_id)
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated party_relationship data (without ID fields)
    """
    # Define relationship types from the enum
    relationship_types = [
        "POWER_OF_ATTORNEY",
        "GUARDIAN",
        "TRUSTEE",
        "BENEFICIARY",
        "EXECUTOR",
        "CUSTODIAN",
        "AUTHORIZED_USER",
        "BUSINESS_PARTNER",
        "SPOUSE",
        "DEPENDENT",
        "CO_SIGNER",
        "EMPLOYER_EMPLOYEE",
        "AGENT",
        "PARENT_CHILD",
        "SIBLING",
        "CORPORATE_OFFICER",
        "MEMBER",
        "OWNER",
        "OTHER"
    ]

    # Choose a relationship type with weighted distribution
    # Some types are more common than others
    weights = {
        "POWER_OF_ATTORNEY": 0.05,
        "GUARDIAN": 0.03,
        "TRUSTEE": 0.04,
        "BENEFICIARY": 0.1,
        "EXECUTOR": 0.02,
        "CUSTODIAN": 0.02,
        "AUTHORIZED_USER": 0.1,
        "BUSINESS_PARTNER": 0.08,
        "SPOUSE": 0.15,
        "DEPENDENT": 0.07,
        "CO_SIGNER": 0.06,
        "EMPLOYER_EMPLOYEE": 0.07,
        "AGENT": 0.04,
        "PARENT_CHILD": 0.1,
        "SIBLING": 0.05,
        "CORPORATE_OFFICER": 0.03,
        "MEMBER": 0.04,
        "OWNER": 0.04,
        "OTHER": 0.01
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
        "relationship_type": relationship_type,
        "priority": priority
        # enterprise_party_id and related_party_id are not generated here
        # as they would be provided in _id_fields or managed separately
    }

    return party_relationship
