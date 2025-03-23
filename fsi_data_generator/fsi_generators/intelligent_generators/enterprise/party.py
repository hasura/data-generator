import datetime
import logging
import random
import string
from typing import Any, Dict

import psycopg2
from faker import Faker

from data_generator import DataGenerator

logger = logging.getLogger(__name__)
fake = Faker()  # Initialize Faker


def generate_random_party(_id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random enterprise.parties record with reasonable values.

    Args:
        _id_fields: Dictionary containing the required ID fields (enterprise_party_id)
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated party data (without ID fields)
    """
    # Get connection for fetching related data
    conn = dg.conn

    # First, get existing party names to avoid duplicates
    existing_party_names = get_existing_party_names(conn)

    # Define party types - simple enum with just two values
    party_types = ["INDIVIDUAL", "ORGANIZATION"]

    # Choose party type with roughly equal distribution
    party_type = random.choice(party_types)

    # Generate name based on party type
    if party_type == "INDIVIDUAL":
        name = f"{fake.first_name()} {fake.last_name()}"
        full_business_legal_name = None
    else:  # ORGANIZATION
        # Generate a company name and make sure it's unique
        name = fake.company()

        # Check for uniqueness and regenerate if needed
        attempts = 0
        while name in existing_party_names and attempts < 10:
            name = fake.company()
            attempts += 1

        # If still not unique, add a timestamp
        if name in existing_party_names:
            timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            name = f"{name} {timestamp[-4:]}"

        full_business_legal_name = name + (", LLC" if random.random() < 0.5 else ", Inc.")

    # Generate email address
    if party_type == "INDIVIDUAL":
        email_address = fake.email()
    else:
        company_domain = name.lower().replace(" ", "").replace(",", "").replace(".", "")
        company_domain = ''.join(c for c in company_domain if c.isalnum())
        email_address = f"info@{company_domain}.com"

    # Generate phone and mobile with proper format
    phone = fake.phone_number()

    # Mobile more likely for individuals, less likely for organizations
    mobile_chance = 0.8 if party_type == "INDIVIDUAL" else 0.3
    mobile = fake.phone_number() if random.random() < mobile_chance else None

    # Generate party_number (alphanumeric identifier)
    party_number = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))

    # For individuals, generate date_of_birth
    date_of_birth = None
    if party_type == "INDIVIDUAL":
        date_of_birth = fake.date_of_birth(minimum_age=18, maximum_age=80)

    # For individuals, generate SSN
    ssn = None
    if party_type == "INDIVIDUAL" and random.random() < 0.7:
        ssn = fake.ssn()

    # Define party status enum
    party_statuses = [
        "ACTIVE",
        "INACTIVE",
        "PENDING",
        "SUSPENDED",
        "DECEASED",  # for individuals
        "DISSOLVED"  # for organizations
    ]

    # Select appropriate status options based on party_type
    if party_type == "INDIVIDUAL":
        valid_statuses = [s for s in party_statuses if s != "DISSOLVED"]
    else:  # ORGANIZATION
        valid_statuses = [s for s in party_statuses if s != "DECEASED"]

    # Weight toward ACTIVE status (80% chance)
    if random.random() < 0.8:
        party_status = "ACTIVE"
    else:
        # Choose from remaining statuses
        party_status = random.choice([s for s in valid_statuses if s != "ACTIVE"])

    # For organizations, set legal structure and LEI
    legal_structure = None
    lei = None
    beneficial_ownership = None

    if party_type == "ORGANIZATION":
        # Using the legal_structure enum from DBML
        legal_structures = [
            "SOLE_PROPRIETORSHIP",
            "GENERAL_PARTNERSHIP",
            "LIMITED_PARTNERSHIP",
            "LIMITED_LIABILITY_PARTNERSHIP",
            "LIMITED_LIABILITY_COMPANY",
            "C_CORPORATION",
            "S_CORPORATION",
            "PROFESSIONAL_CORPORATION",
            "NONPROFIT_CORPORATION",
            "BENEFIT_CORPORATION",
            "COOPERATIVE",
            "JOINT_VENTURE",
            "TRUST",
            "ESTATE",
            "ASSOCIATION",
            "GOVERNMENT_ENTITY",
            "FOREIGN_ENTITY",
            "NOT_APPLICABLE",
            "OTHER"
        ]
        legal_structure = random.choice(legal_structures)

        # 40% chance to have an LEI for organizations
        if random.random() < 0.4:
            lei = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))

        # 50% chance to have beneficial ownership flag set for organizations
        beneficial_ownership = random.choice([True, False]) if random.random() < 0.5 else None

    # For individuals, set marital_status and citizenship_status
    marital_status = None
    citizenship_status = None

    if party_type == "INDIVIDUAL":
        # Using the marital_status enum from DBML
        marital_statuses = [
            "SINGLE",
            "MARRIED",
            "DOMESTIC_PARTNERSHIP",
            "SEPARATED",
            "DIVORCED",
            "WIDOWED",
            "NOT_SPECIFIED"
        ]
        marital_status = random.choice(marital_statuses)

        # Using the citizenship_status enum from DBML
        citizenship_statuses = [
            "US_CITIZEN",
            "US_PERMANENT_RESIDENT",
            "US_TEMPORARY_RESIDENT",
            "NON_RESIDENT_ALIEN",
            "FOREIGN_NATIONAL",
            "DUAL_CITIZEN_US",
            "REFUGEE_ASYLEE",
            "TEMPORARY_PROTECTED_STATUS",
            "DACA_RECIPIENT",
            "UNDOCUMENTED",
            "NOT_SPECIFIED"
        ]
        citizenship_status = random.choice(citizenship_statuses)

    # Create the party record
    party = {
        "party_number": party_number,
        "party_type": party_type,
        "name": name,
        "full_business_legal_name": full_business_legal_name,
        "legal_structure": legal_structure,
        "lei": lei,
        "beneficial_ownership": beneficial_ownership,
        "email_address": email_address,
        "phone": phone,
        "mobile": mobile,
        "date_of_birth": date_of_birth,
        "ssn": ssn,
        "marital_status": marital_status,
        "citizenship_status": citizenship_status,
        "party_status": party_status
    }

    return party


def get_existing_party_names(conn) -> list:
    """
    Get all existing party names from the database.

    Args:
        conn: PostgreSQL connection object

    Returns:
        List of existing party names
    """
    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT name
            FROM enterprise.parties
        """)

        results = cursor.fetchall()
        cursor.close()

        # Extract the names from the results
        return [result[0] for result in results] if results else []

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching existing party names: {error}")
        return []  # Return empty list on error to avoid blocking generation
