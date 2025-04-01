from ...helpers.generate_unique_json_array import generate_unique_json_array
from data_generator import DataGenerator
from typing import Any, Dict

import logging
import psycopg2
import random

logger = logging.getLogger(__name__)


def generate_random_permission(_id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random "enterprise.permissions" record with reasonable values.

    Args:
        _id_fields: Dictionary containing the required ID fields (enterprise_permission_id)
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated permission data (without ID fields)
    """
    # Get connection for fetching related data
    conn = dg.conn

    # First, get existing permission names to avoid duplicates
    existing_permission_names = get_existing_permission_names(conn)

    # Default fallback values for permission names
    permission_actions = ["read", "write", "update", "delete", "create", "view", "manage", "execute", "approve",
                          "reject", "modify", "export", "import", "list", "search"]
    permission_resources = ["accounts", "transactions", "balances", "parties", "customers", "loans", "deposits",
                            "cards", "users", "permissions", "reports", "documents", "applications", "settings",
                            "profiles"]

    # Try to use generate_unique_json_array for permission names
    try:
        generated_permission_names = generate_unique_json_array(
            dbml_string=dg.dbml,
            fully_qualified_column_name="enterprise.permissions.permission_name - Banking system permission names like read_balances, approve_loans, modify_customer_data, view_transactions, manage_accounts",
            count=50,
            cache_key='permission_names'
        )
        if generated_permission_names:
            permission_names = generated_permission_names
        else:
            # Generate permission names by combining actions and resources
            permission_names = [f"{action}_{resource}" for action in permission_actions for resource in
                                permission_resources]
    except Exception as e:
        logger.error(f"Error generating permission names: {e}")
        # Continue with fallback values
        permission_names = [f"{action}_{resource}" for action in permission_actions for resource in
                            permission_resources]

    # Choose a permission name and ensure it's unique
    available_names = [name for name in permission_names if name not in existing_permission_names]

    if not available_names:
        # If we've run out of available names, create a new unique combination
        while True:
            permission_name = f"{random.choice(permission_actions)}_{random.choice(permission_resources)}"
            if permission_name not in existing_permission_names:
                break
    else:
        permission_name = random.choice(available_names)

    # Create the permission record
    permission = {
        "permission_name": permission_name
    }

    return permission


def get_existing_permission_names(conn) -> list:
    """
    Get all existing permission names from the database.

    Args:
        conn: PostgreSQL connection object

    Returns:
        List of existing permission names
    """
    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT permission_name
            FROM enterprise.permissions
        """)

        results = cursor.fetchall()
        cursor.close()

        # Extract the names from the results
        return [result[0] for result in results] if results else []

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching existing permission names: {error}")
        return []  # Return empty list on error to avoid blocking generation
