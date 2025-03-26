import logging
import random
from typing import Any, Dict

import psycopg2
from faker import Faker

from data_generator import DataGenerator, SkipRowGenerationError
from fsi_data_generator.fsi_generators.helpers.generate_unique_json_array import \
    generate_unique_json_array

logger = logging.getLogger(__name__)
fake = Faker()  # Initialize Faker

prev_department = set()


def generate_random_department(_id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random "enterprise.departments" record with reasonable values.

    Args:
        _id_fields: Dictionary containing the required ID fields (enterprise_department_id)
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated department data (without ID fields)
    """
    # Get connection for fetching related data
    conn = dg.conn

    # First, get existing department names to avoid duplicates (as department_name is unique)
    existing_department_names = get_existing_department_names(conn)

    # Default fallback values for department names
    department_prefixes = [
        "Retail", "Commercial", "Corporate", "Investment", "Private", "Consumer",
        "Small Business", "Enterprise", "Digital", "Online", "Mobile", "Treasury",
        "Risk", "Compliance", "Legal", "Finance", "Accounting", "Operations",
        "Technology", "IT", "Information Security", "Cyber Security", "Data",
        "Analytics", "Marketing", "Sales", "Customer Service", "Human Resources",
        "Talent", "Learning", "Development", "Facilities", "Administration"
    ]

    department_suffixes = [
        "Banking", "Services", "Solutions", "Management", "Operations", "Department",
        "Division", "Group", "Team", "Support", "Analytics", "Strategy", "Systems"
    ]

    # Try to use generate_unique_json_array for department names
    try:
        generated_department_names = generate_unique_json_array(
            dbml_string=dg.dbml,
            fully_qualified_column_name="enterprise.departments.department_name - Banking department names including Retail Banking, Commercial Lending, Risk Management, Compliance, Treasury, IT, and Operations",
            count=50,
            cache_key='department_names'
        )
        if generated_department_names:
            department_names = generated_department_names
        else:
            # Generate department names by combining prefixes and suffixes
            department_names = [f"{prefix} {suffix}" for prefix in department_prefixes for suffix in
                                department_suffixes]
    except Exception as e:
        logger.error(f"Error generating department names: {e}")
        # Continue with fallback values
        department_names = [f"{prefix} {suffix}" for prefix in department_prefixes for suffix in department_suffixes]

    # Choose a department name and ensure it's unique
    available_names = [name for name in department_names if name not in existing_department_names]

    if not available_names:
        # If we've run out of available names, create a new unique name by combining random prefixes and suffixes
        while True:
            department_name = f"{random.choice(department_prefixes)} {random.choice(department_suffixes)}"
            if department_name not in existing_department_names:
                break
    else:
        department_name = random.choice(available_names)

    # Create the department record
    department = {
        "department_name": department_name
        # No need to generate enterprise_building_id as it will be provided
        # in _id_fields or managed by the system/data insertion process
    }

    if department_name in prev_department:
        raise SkipRowGenerationError

    prev_department.add(department_name)

    return department


def get_existing_department_names(conn) -> list:
    """
    Get all existing department names from the database.

    Args:
        conn: PostgreSQL connection object

    Returns:
        List of existing department names
    """
    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT department_name
            FROM enterprise.departments
        """)

        results = cursor.fetchall()
        cursor.close()

        # Extract the names from the results
        return [result[0] for result in results] if results else []

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching existing department names: {error}")
        return []  # Return empty list on error to avoid blocking generation
