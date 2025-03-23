import random
from typing import Any, Dict

from data_generator import DataGenerator


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
    # Define dependency types
    dependency_types = [
        "runtime",
        "build",
        "test",
        "development",
        "optional",
        "provided",
        "system",
        "import",
        "compile",
        "annotationProcessor"
    ]

    # Choose a random dependency type
    dependency_type = random.choice(dependency_types)

    # Generate a reasonable quantity - typically this would be 1
    # but occasionally components might be used multiple times
    quantity_weights = [0.85, 0.10, 0.03, 0.01, 0.01]  # weights for [1, 2, 3, 4, 5]
    quantity = random.choices([1, 2, 3, 4, 5], weights=quantity_weights, k=1)[0]

    # Create the component dependency record (content fields only)
    component_dependency = {
        "quantity": quantity,
        "dependency_type": dependency_type
    }

    return component_dependency
