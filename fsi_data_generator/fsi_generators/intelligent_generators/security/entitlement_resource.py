import random
from typing import Any, Dict, List, Optional

from data_generator import DataGenerator, SkipRowGenerationError

prev_entitlement_resources = set()


def generate_random_entitlement_resource(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random security.entitlement_resources record with context-aware values.

    Args:
        id_fields: Dictionary containing the required ID fields
                   (security_entitlement_resource_id, security_entitlement_id, security_resource_id)
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated entitlement resource data
        (without ID fields or FK fields)
    """
    # Define base permission types from the DBML enum
    base_permission_types = [
        "READ",
        "WRITE",
        "DELETE",
        "EXECUTE",
        "ADMIN",
        "MASKED"  # New permission type
    ]

    # Fetch the resource definition for the given resource_id
    resource_definition = _fetch_resource_definition(
        id_fields.get('security_resource_id'),
        dg.conn
    )

    # Get the resource type
    resource_type = resource_definition.get('resource_type', 'DATA')
    resource_name = resource_definition.get('resource_name', 'Undefined Resource')
    resource_identifier = resource_definition.get('resource_identifier', 'undefined')

    # Adjust permission types based on resource type
    permission_types = _adjust_permission_types_for_resource(
        resource_type,
        base_permission_types,
        resource_identifier
    )

    # Generate random permission type
    permission_type = random.choice(permission_types)

    # Generate context conditions and resource details based on resource type
    context_conditions = _generate_context_conditions(resource_type, resource_name)
    resource_details = _generate_resource_details(resource_type, resource_name)

    # Truncate strings to 1000 characters to match VARCHAR(1000)
    context_conditions = context_conditions[:1000]
    resource_details = resource_details[:1000]

    # Entitlement resources record
    entitlement_resource = {
        "permission_type": permission_type,
        "context_conditions": context_conditions,
        "resource_details": resource_details
    }

    key = (id_fields.get('security_entitlement_id'), id_fields.get('security_resource_id'), permission_type)
    if key in prev_entitlement_resources:
        raise SkipRowGenerationError

    prev_entitlement_resources.add(key)

    return entitlement_resource


def _fetch_resource_definition(resource_id: Optional[str], conn) -> Dict[str, Any]:
    """
    Fetch the resource definition for a given resource ID from the database.

    Args:
        resource_id: UUID of the resource
        conn: Database connection object

    Returns:
        Dictionary with resource definition details
    """
    if not resource_id:
        raise ValueError("No resource_id provided")

    # SQL query to fetch resource definition
    query = """
    SELECT 
        resource_type, 
        resource_name, 
        resource_identifier 
    FROM security.resource_definitions 
    WHERE security_resource_id = %s
    """

    # Execute the query with the resource_id
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, (resource_id,))
            result = cursor.fetchone()

        # If no result found, raise an exception
        if not result:
            raise ValueError(f"No resource definition found for resource_id: {resource_id}")

        return result

    except Exception as e:
        # Handle potential database errors
        raise ValueError(f"Error fetching resource definition: {str(e)}")


def _adjust_permission_types_for_resource(
        resource_type: str,
        permission_types: List[str],
        resource_identifier: str
) -> List[str]:
    """
    Adjust permission types based on resource type, with special consideration for DATA resources.

    Args:
        resource_type: Type of resource (DATA, APPLICATION, INFRASTRUCTURE)
        permission_types: Initial list of permission types
        resource_identifier: Identifier of the specific resource

    Returns:
        Filtered and potentially modified list of permission types
    """
    if resource_type == 'DATA':
        # Define more nuanced data-specific permission strategies
        data_permission_strategies = {
            # Highly sensitive customer data - masked access
            'customers': {
                'permissions': ['READ', 'MASKED'],
                'rationale': 'Sensitive personal information with partial visibility'
            },
            # Financial transaction tables - restricted with potential masking
            'transactions': {
                'permissions': ['READ', 'MASKED'],
                'rationale': 'Sensitive financial data requiring partial obscurity'
            },
            # Aggregate or reporting tables
            'reports': {
                'permissions': ['READ', 'EXECUTE', 'MASKED'],
                'rationale': 'Analytical data with potential need for masked access'
            },
            # Configurable system tables
            'configurations': {
                'permissions': ['READ', 'WRITE', 'ADMIN'],
                'rationale': 'System settings require more flexible access'
            },
            # Default strategy for unrecognized data resources
            'default': {
                'permissions': ['READ', 'WRITE', 'MASKED'],
                'rationale': 'Balanced access with potential masking for data resources'
            }
        }

        # Match resource to a strategy, defaulting if no specific match
        matched_strategy = next(
            (strategy for key, strategy in data_permission_strategies.items()
             if key in resource_identifier.lower()),
            data_permission_strategies['default']
        )

        return matched_strategy['permissions']

    elif resource_type == 'INFRASTRUCTURE':
        return ["READ", "EXECUTE", "ADMIN"]

    elif resource_type == 'APPLICATION':
        return ["READ", "WRITE", "EXECUTE", "ADMIN"]

    return [pt for pt in permission_types if pt != "MASKED"]  # Remove MASKED for non-DATA resources


def _generate_context_conditions(resource_type: str, resource_name: str) -> str:
    """
    Generate context conditions based on resource type.

    Args:
        resource_type: Type of the resource (DATA, APPLICATION, INFRASTRUCTURE)
        resource_name: Name of the resource

    Returns:
        String of context conditions
    """
    if resource_type == 'DATA':
        conditions = [
            f"data_sensitivity:high",
            f"access_level:restricted",
            f"resource:{resource_name}",
            f"compliance:data_protection",
            f"data_classification:pii",
            f"masking_level:partial"
        ]
    elif resource_type == 'APPLICATION':
        conditions = [
            f"environment:production",
            f"authentication:two_factor",
            f"access_method:internal_network",
            f"application:{resource_name}",
            f"user_role:manager"
        ]
    elif resource_type == 'INFRASTRUCTURE':
        conditions = [
            f"location:us_datacenter",
            f"network:secure_zone",
            f"access_method:vpn_only",
            f"server:{resource_name}",
            f"maintenance_window:off_hours"
        ]
    else:
        conditions = [
            f"generic_condition:default",
            f"resource_name:{resource_name}"
        ]

    # Randomly select and combine conditions
    selected_conditions = random.sample(conditions, k=min(3, len(conditions)))
    return ", ".join(selected_conditions)


def _generate_resource_details(resource_type: str, resource_name: str) -> str:
    """
    Generate resource details based on resource type.

    Args:
        resource_type: Type of the resource (DATA, APPLICATION, INFRASTRUCTURE)
        resource_name: Name of the resource

    Returns:
        String of resource details
    """
    if resource_type == 'DATA':
        details = [
            f"column_filter:sensitive_columns",
            f"row_access:department_level",
            f"data_masking:partial",
            f"table:{resource_name}",
            f"encryption:required",
            f"mask_strategy:last_four_digits",
            f"pii_protection:active"
        ]
    elif resource_type == 'APPLICATION':
        details = [
            f"module_access:limited",
            f"feature_flags:controlled",
            f"logging:full_audit",
            f"application:{resource_name}",
            f"performance_tier:high"
        ]
    elif resource_type == 'INFRASTRUCTURE':
        details = [
            f"monitoring:critical",
            f"backup_frequency:hourly",
            f"failover:enabled",
            f"server:{resource_name}",
            f"patch_level:latest"
        ]
    else:
        details = [
            f"generic_detail:default",
            f"resource_name:{resource_name}"
        ]

    # Randomly select and combine details
    selected_details = random.sample(details, k=min(3, len(details)))
    return ", ".join(selected_details)
