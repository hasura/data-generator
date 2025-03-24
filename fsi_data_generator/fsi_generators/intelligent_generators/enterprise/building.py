import datetime
import logging
import random
from typing import Any, Dict

import psycopg2
from faker import Faker

from data_generator import DataGenerator
from fsi_data_generator.fsi_generators.helpers.generate_unique_json_array import \
    generate_unique_json_array

from .enums import BuildingType

logger = logging.getLogger(__name__)
fake = Faker()  # Initialize Faker


def generate_random_building(_id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random "enterprise.buildings" record with reasonable values.

    Args:
        _id_fields: Dictionary containing the required ID fields (enterprise_building_id)
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated building data (without ID fields)
    """

    # Get connection for fetching related data
    conn = dg.conn

    # First, get existing building names to avoid duplicates
    existing_building_names = get_existing_building_names(conn)

    # Default fallback values for building names
    building_prefixes = ["Main", "Downtown", "Corporate", "Regional", "North", "South", "East", "West", "Central"]
    building_suffixes = ["Branch", "Office", "Tower", "Plaza", "Building", "Campus", "Center", "Facility"]

    # Try to use generate_unique_json_array for building names
    try:
        generated_building_names = generate_unique_json_array(
            dbml_string=dg.dbml,
            fully_qualified_column_name="enterprise.buildings.building_name - Names for bank buildings including branches, headquarters, and operational facilities",
            count=50,
            cache_key='building_names'
        )
        if generated_building_names:
            building_names = generated_building_names
        else:
            # Generate building names by combining prefixes and suffixes
            building_names = [f"{prefix} {suffix}" for prefix in building_prefixes for suffix in building_suffixes]
    except Exception as e:
        logger.error(f"Error generating building names: {e}")
        # Continue with fallback values
        building_names = [f"{prefix} {suffix}" for prefix in building_prefixes for suffix in building_suffixes]

    # Choose a building name and ensure it's unique
    available_names = [name for name in building_names if name not in existing_building_names]

    if not available_names:
        # If we've run out of available names, create a new unique name
        timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        building_name = f"{random.choice(building_prefixes)} {random.choice(building_suffixes)} {timestamp[-4:]}"
    else:
        building_name = random.choice(available_names)

    # Choose building type with appropriate weighting using enum
    # BRANCH should be the most common type
    building_type = BuildingType.get_random()

    # Generate phone number
    phone_number = fake.phone_number()

    # Generate dates
    today = datetime.date.today()

    # Buildings should have different likely ages based on type
    if building_type in [BuildingType.HEADQUARTERS, BuildingType.BRANCH]:
        # These could be very old
        max_years_ago = 50
    elif building_type in [BuildingType.OPERATIONS_CENTER, BuildingType.ADMINISTRATIVE]:
        # These might be moderately old
        max_years_ago = 30
    elif building_type in [BuildingType.DATA_CENTER, BuildingType.DISASTER_RECOVERY]:
        # These are likely newer
        max_years_ago = 15
    else:
        # Others have standard age range
        max_years_ago = 25

    years_ago = random.randint(1, max_years_ago)
    open_date = today - datetime.timedelta(days=years_ago * 365)

    # Different building types have different probabilities of being closed
    close_probabilities = {
        BuildingType.BRANCH: 0.1,  # 10% chance of being closed
        BuildingType.HEADQUARTERS: 0.02,  # 2% chance
        BuildingType.OPERATIONS_CENTER: 0.05,
        BuildingType.DATA_CENTER: 0.05,
        BuildingType.ADMINISTRATIVE: 0.1,
        BuildingType.WAREHOUSE: 0.15,
        BuildingType.TRAINING_CENTER: 0.1,
        BuildingType.DISASTER_RECOVERY: 0.05,
        BuildingType.CALL_CENTER: 0.1,
        BuildingType.ATM_LOCATION: 0.2,
        BuildingType.OTHER: 0.15
    }

    # Determine if building is closed based on its type
    is_closed = random.random() < close_probabilities.get(building_type, 0.1)

    # For closed buildings, close_date is between yesterday and 5 years ago
    close_date = None
    if is_closed:
        close_days_ago = random.randint(1, 5 * 365)
        close_date = today - datetime.timedelta(days=close_days_ago)

        # Ensure open_date is before close_date
        if close_date <= open_date:
            open_date = close_date - datetime.timedelta(days=random.randint(365, 20 * 365))

    # Create the building record
    building = {
        "building_name": building_name,
        "building_type": building_type.value,  # Use .value to get the string representation
        "phone_number": phone_number,
        "open_date": open_date,
        "close_date": close_date
        # Note: enterprise_entity_address_id is not generated here since it's a foreign key
        # that would be managed by the system or data insertion process
    }

    return building


def get_existing_building_names(conn) -> list:
    """
    Get all existing building names from the database.

    Args:
        conn: PostgreSQL connection object

    Returns:
        List of existing building names
    """
    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT building_name
            FROM enterprise.buildings
        """)

        results = cursor.fetchall()
        cursor.close()

        # Extract the names from the results
        return [result[0] for result in results] if results else []

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching existing building names: {error}")
        return []  # Return empty list on error to avoid blocking generation
