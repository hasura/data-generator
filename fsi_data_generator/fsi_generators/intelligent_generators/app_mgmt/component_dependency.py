from data_generator import DataGenerator
from .enums import DependencyType
from typing import Any, Dict

import random


def generate_random_component_dependency(_id_fields: Dict[str, Any], _dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random app_mgmt component dependency record with reasonable values.

    This creates a relationship between parent and child components without
    generating any ID fields or foreign keys.

    Args:
        _id_fields: Dictionary containing the required ID fields
                  (parent_component_id, child_component_id)
        _dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated component dependency data
        (without ID fields or FK fields)
    """
    # Get a random dependency type using the weighted selection
    dependency_type = DependencyType.get_random()

    # Generate a reasonable quantity - typically this would be 1
    # but occasionally components might be used multiple times
    quantity_weights = [0.85, 0.10, 0.03, 0.01, 0.01]  # weights for [1, 2, 3, 4, 5]
    quantity = random.choices([1, 2, 3, 4, 5], weights=quantity_weights, k=1)[0]

    # Create the component dependency record (content fields only)
    component_dependency = {
        "quantity": quantity,
        "dependency_type": dependency_type.name
    }

    return component_dependency
