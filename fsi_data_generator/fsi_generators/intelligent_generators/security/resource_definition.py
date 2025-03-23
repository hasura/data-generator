import random
from typing import Any, Dict, List

from data_generator import DataGenerator


def generate_random_resource_definition(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random security.resource_definitions record with reasonable values.

    Args:
        id_fields: Dictionary containing the required ID fields (security_resource_id)
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated resource definition data (without ID fields or FK fields)
    """
    # Extract schema information from DBML
    schemas_and_tables = extract_schemas_and_tables(dg.dbml)

    # Decide whether to attach an application_id and/or host_id
    resource_type = random.choice(['APPLICATION', 'HOST', 'DATA', 'NETWORK_DEVICE'])

    if resource_type == 'APPLICATION':
        id_fields['host_id'] = None
        id_fields['network_device_id'] = None
    elif resource_type == 'NETWORK_DEVICE':
        id_fields['application_id'] = None
        id_fields['host_id'] = None
    elif resource_type == 'HOST':
        id_fields['application_id'] = None
        id_fields['network_device_id'] = None
    else:
        id_fields['application_id'] = None
        id_fields['host_id'] = None
        id_fields['network_device_id'] = None

    # Generate resource name and identifier based on the resource type and foreign keys
    if resource_type == "DATA":
        # Always use a real table for DATA resources
        schema = random.choice(list(schemas_and_tables.keys()))
        table = random.choice(schemas_and_tables[schema])
        resource_name = f"{schema.capitalize()} {table.replace('_', ' ').title()} Table"
        resource_identifier = f"/data/{schema}/{table}"

    elif resource_type == "APPLICATION":
        # For APPLICATION resources, use the application name
        resource_name = "Application Resource"  # Will be replaced with actual app name
        resource_identifier = f"/applications/app-resource/{id_fields['application_id']}"

    elif resource_type == "HOST":
        # For HOST resources, use the host ID
        resource_name = f"Host {id_fields['host_id']}"
        resource_identifier = f"/hosts/{id_fields['host_id']}"

    else:  # NETWORK_DEVICE
        # For NETWORK_DEVICE resources, use the id
        resource_name = "Network Device Resource"  # Will be replaced with actual host name
        resource_identifier = f"/network/{id_fields['network_device_id']}"

    # Generate a description based on the resource type and name
    descriptions = [
        f"A {resource_type.lower()} resource representing {resource_name} used for secure banking operations.",
        f"{resource_type.lower()} resource that provides {resource_name.lower()} functionality to authorized users.",
        f"Secure {resource_type.lower()} resource for {resource_name} with controlled access requirements.",
        f"{resource_name} {resource_type.lower()} resource with comprehensive audit logging and access controls.",
        f"Financial {resource_type.lower()} resource for {resource_name} requiring elevated permissions."
    ]
    description = random.choice(descriptions)

    # Create the resource definition record (content fields only)
    resource_definition = {
        "resource_name": resource_name,
        "resource_type": resource_type,
        "resource_identifier": resource_identifier,
        "description": description,
    }

    resource_definition.update(id_fields)

    return resource_definition


def extract_schemas_and_tables(dbml: str) -> Dict[str, List[str]]:
    """
    Extract schema and table names from the DBML.

    Args:
        dbml: DBML string containing the database schema

    Returns:
        Dictionary mapping schema names to lists of table names
    """
    schemas_tables = {}
    try:
        # Simple parsing to extract table definitions
        lines = dbml.split('\n')

        for line in lines:
            line = line.strip()

            # Look for table definitions
            if line.startswith('Table "') and '"."' in line:
                parts = line.split('"."')
                if len(parts) >= 2:
                    schema = parts[0].replace('Table "', '').strip()
                    table = parts[1].split('"')[0].strip()

                    if schema not in schemas_tables:
                        schemas_tables[schema] = []

                    schemas_tables[schema].append(table)

        # Make sure we have at least one entry in each schema
        for schema in list(schemas_tables.keys()):
            if not schemas_tables[schema]:
                del schemas_tables[schema]

        # If we have no schemas/tables at all, add some defaults
        if not schemas_tables:
            schemas_tables = {
                "consumer_banking": ["accounts", "transactions", "balances"],
                "credit_cards": ["card_accounts", "transactions", "statements"],
                "mortgage_services": ["applications", "loans", "property"]
            }

        return schemas_tables
    except Exception as _e:
        # Return default dict on parsing error
        return {
            "consumer_banking": ["accounts", "transactions", "balances"],
            "credit_cards": ["card_accounts", "transactions", "statements"],
            "mortgage_services": ["applications", "loans", "property"]
        }
