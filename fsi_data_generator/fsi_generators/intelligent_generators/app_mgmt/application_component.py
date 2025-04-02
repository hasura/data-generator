from .enums import DependencyType
from data_generator import DataGenerator
from typing import Any, Dict


def generate_random_application_component(_id_fields: Dict[str, Any], _dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random app_mgmt application_component record with reasonable values.

    This creates a relationship between an application and a component without
    generating any ID fields or foreign keys.

    Args:
        _id_fields: Dictionary containing the required ID fields
                  (application_id, app_mgmt_component_id)
        _dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated application-component relationship data
        (without ID fields or FK fields)
    """
    # Get a random dependency type using the weighted selection
    dependency_type = DependencyType.get_random()

    # Create the application component record (content fields only)
    # Note: This is a junction table so it only has the dependency_type as content
    application_component = {
        "dependency_type": dependency_type.name
    }

    return application_component
