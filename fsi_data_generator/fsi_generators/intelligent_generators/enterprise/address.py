import logging
import random
import re
from typing import Any, Dict

from faker import Faker

from data_generator import DataGenerator
from fsi_data_generator.fsi_generators.helpers.parse_address import \
    parse_address

from .enums import AddressType

logger = logging.getLogger(__name__)
fake = Faker()  # Initialize Faker


def generate_random_address(_id_fields: Dict[str, Any], _dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random "enterprise.addresses" record with reasonable values.

    Args:
        _id_fields: Dictionary containing the required ID fields (enterprise_address_id)
        _dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated address data (without ID fields)
    """

    # Choose a random address type
    address_type = AddressType.get_random()

    # Generate a standard street address (keep trying until we get one)
    parsed_address = None
    attempts = 0
    max_attempts = 10

    while not parsed_address and attempts < max_attempts:
        full_address = fake.address()
        parsed = parse_address(full_address)

        # Check if this is a standard street address (not PO Box or military)
        if ('street_address' in parsed and
                'PO Box' not in parsed['street_address'] and
                not any(x in parsed.get('city', '') for x in ['APO', 'FPO', 'DPO'])):

            # Verify we have a building number
            street_match = re.match(r'^(\d+)\s+(.+)$', parsed.get('street_address', ''))
            if street_match:
                parsed_address = parsed

        attempts += 1

    # If we couldn't get a standard address after max attempts, use the last one anyway
    if not parsed_address:
        parsed_address = parsed

    # Extract building number and street name
    street_match = re.match(r'^(\d+)\s+(.+)$', parsed_address.get('street_address', ''))
    if street_match:
        building_number = street_match.group(1)
        street_name = street_match.group(2)
    else:
        # Default case if we couldn't extract properly
        building_number = ""
        street_name = parsed_address.get('street_address', '')

    # Generate additional fields based on probability
    has_department = random.random() < 0.15  # 15% chance
    has_sub_department = has_department and random.random() < 0.3  # 30% of those with department
    has_building_name = random.random() < 0.2  # 20% chance
    has_floor = random.random() < 0.15  # 15% chance
    has_room = random.random() < 0.1  # 10% chance
    has_town_location = random.random() < 0.25  # 25% chance
    has_care_of = random.random() < 0.1  # 10% chance

    # Generate optional fields
    department = fake.company_suffix() if has_department else None
    sub_department = f"{department} Division" if has_sub_department else None
    building_name = f"{fake.last_name()} Building" if has_building_name else None
    floor = str(random.randint(1, 50)) if has_floor else None
    room = f"Suite {random.randint(100, 999)}" if has_room else None

    # For US addresses, only generate town_location_name for specific cities
    # (e.g., NYC boroughs, Chicago neighborhoods, etc.)
    town_location_name = None
    if has_town_location:
        city = parsed_address.get('city', '').lower()
        if 'new york' in city or 'nyc' in city:
            # NYC boroughs
            town_location_name = random.choice(["Manhattan", "Brooklyn", "Queens", "Bronx", "Staten Island"])
        elif 'chicago' in city:
            # Chicago neighborhoods
            town_location_name = random.choice([
                "Loop", "Lincoln Park", "Wicker Park", "Hyde Park", "Lakeview",
                "River North", "Gold Coast", "Uptown", "Pilsen", "Bucktown"
            ])
        elif 'los angeles' in city:
            # LA neighborhoods
            town_location_name = random.choice([
                "Hollywood", "Venice", "Downtown", "Silver Lake", "Echo Park",
                "Koreatown", "Westwood", "Beverly Hills", "Brentwood", "Los Feliz"
            ])
        elif 'san francisco' in city:
            # SF neighborhoods
            town_location_name = random.choice([
                "Mission", "Marina", "SOMA", "Nob Hill", "Castro",
                "Haight-Ashbury", "North Beach", "Chinatown", "Financial District", "Richmond"
            ])
        elif 'boston' in city:
            # Boston neighborhoods
            town_location_name = random.choice([
                "Back Bay", "Beacon Hill", "North End", "South End", "Fenway",
                "Allston", "Brighton", "Roxbury", "Charlestown", "Jamaica Plain"
            ])

    care_of = f"C/O {fake.name()}" if has_care_of else None

    # Check for unit/apt number in street name
    unit_number = None
    if street_name:
        unit_match = re.search(r'(Apt\.?|Apartment|Unit|Suite|#)\s*([0-9A-Za-z-]+)', street_name)
        if unit_match:
            unit_number = f"{unit_match.group(1)} {unit_match.group(2)}"
            street_name = street_name.replace(unit_match.group(0), '').strip()

    # Create the address record
    address = {
        "address_type": address_type.value,
        "department": department,
        "sub_department": sub_department,
        "street_name": street_name,
        "building_number": building_number,
        "building_name": building_name,
        "floor": floor,
        "room": room,
        "unit_number": unit_number,
        "post_box": None,  # We're focusing on standard addresses
        "town_location_name": town_location_name,
        "district_name": None,  # No district_name for US addresses
        "care_of": care_of,
        "post_code": parsed_address.get('post_code', ''),
        "town_name": parsed_address.get('city', ''),
        "country_sub_division": parsed_address.get('state', ''),
        "country": "US"  # Default to US
    }

    return address
