from .enums import OccupancyType, PropertyType
from data_generator import DataGenerator, SkipRowGenerationError
from datetime import timedelta
from faker import Faker
from typing import Any, Dict

import datetime
import logging
import psycopg2
import random
import sys

# Set up logging
logger = logging.getLogger(__name__)

# Global set to track application IDs that have already been processed
# This will persist across multiple calls to generate_random_property
PROCESSED_APPLICATION_IDS = set()


def validate_property_association(application_id):
    """
    Validates if a property is already associated with the given mortgage application
    using the global set of processed application IDs.

    Args:
        application_id: ID of the mortgage application to check

    Returns:
        tuple: (is_valid, error_message)
            - is_valid (bool): True if application ID not already processed, False otherwise
            - error_message (str): Error message if validation fails, empty string otherwise
    """
    if not application_id:
        return False, "Mortgage application ID is required for validation"

    # Check if this application ID has already been processed
    if application_id in PROCESSED_APPLICATION_IDS:
        return False, f"Property already exists for application ID: {application_id}"

    return True, ""


def generate_random_property(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random, plausible property record based on the loan application and product type.

    Args:
        id_fields: Dictionary containing the required ID fields (mortgage_services_application_id)
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated property data (without ID fields)
    """
    # Initialize Faker for address generation
    fake = Faker()

    # Get the loan application from the application ID
    conn = dg.conn
    application_id = id_fields.get("mortgage_services_application_id")

    # Validate that no property has been generated for this application
    is_valid, error_message = validate_property_association(application_id)
    if not is_valid:
        raise SkipRowGenerationError

    lot_options = None
    lot_weights = None

    # Query the database for loan application details
    loan_application = {}
    if conn and application_id:
        cursor = conn.cursor()
        try:
            try:
                cursor.execute("""
                    SELECT * FROM mortgage_services.applications
                    WHERE mortgage_services_application_id = %s
                """, (application_id,))
            except psycopg2.ProgrammingError as e:
                logger.critical(f"Programming error detected in the SQL query: {e}")
                sys.exit(1)

            application_row = cursor.fetchone()
            if application_row:
                loan_application = dict(application_row)
        finally:
            cursor.close()

    # Extract relevant information from the application
    application_type = loan_application.get("application_type")
    loan_purpose = loan_application.get("loan_purpose")
    estimated_property_value = loan_application.get("estimated_property_value")

    # Get loan product information
    product_type = "conventional"  # default
    if loan_application.get("mortgage_services_loan_product_id"):
        cursor = conn.cursor()
        try:
            try:
                cursor.execute("""
                    SELECT * FROM mortgage_services.loan_products
                    WHERE mortgage_services_loan_product_id = %s
                """, (loan_application.get("mortgage_services_loan_product_id"),))
            except psycopg2.ProgrammingError as e:
                logger.critical(f"Programming error detected in the SQL query: {e}")
                sys.exit(1)

            product_row = cursor.fetchone()
            if product_row:
                product_dict = dict(product_row)
                loan_type = product_dict.get("loan_type", "").lower()
                if "jumbo" in loan_type:
                    product_type = "jumbo"
                elif "fha" in loan_type:
                    product_type = "fha"
                elif "va" in loan_type:
                    product_type = "va"
                elif "usda" in loan_type:
                    product_type = "usda"
                elif "construction" in loan_type:
                    product_type = "construction loan"
                elif "heloc" in loan_type:
                    product_type = "heloc"
                elif "reverse" in loan_type:
                    product_type = "reverse mortgage"
        finally:
            cursor.close()

    lot_size = None

    # Get property type and occupancy type using enums
    property_type_enum = PropertyType.get_random(product_type)
    occupancy_type_enum = OccupancyType.get_random(loan_purpose)

    # Generate a complete address using Faker
    # Customize based on property type
    if property_type_enum in [PropertyType.CONDO, PropertyType.TOWNHOUSE]:
        # Generate address with unit number for condos and townhouses
        street_address = fake.street_address()
        unit_number = f"Unit {random.choice(['A', 'B', 'C', '1', '2', '3'])}{random.randint(1, 999)}"
        city = fake.city()
        state = fake.state_abbr()
        zip_code = fake.zipcode()
        address = f"{street_address}, {unit_number}, {city}, {state} {zip_code}"
    elif product_type == "usda":
        # Generate rural address for USDA loans
        street_address = fake.street_address()
        city = fake.city()
        state = fake.state_abbr()
        zip_code = fake.zipcode()
        address = f"{street_address}, {city}, {state} {zip_code}"

        # Sometimes add rural route notation
        if random.random() < 0.3:
            address = f"RR {random.randint(1, 9)}, Box {random.randint(100, 999)}, {city}, {state} {zip_code}"
    else:
        # Standard address format for other property types
        address = fake.street_address() + ", " + fake.city() + ", " + fake.state_abbr() + " " + fake.zipcode()

    # Determine if new construction based on application type
    is_new_construction = False
    construction_completion_date = None

    if application_type == "Construction" or product_type == "construction loan":
        is_new_construction = True
        # Construction completion date is 6-18 months in the future
        now = datetime.datetime.now()
        completion_days = random.randint(180, 540)  # 6-18 months
        construction_completion_date = (now + timedelta(days=completion_days)).strftime("%Y-%m-%d")
    elif random.random() < 0.05:  # 5% chance of new construction for other loans
        is_new_construction = True
        now = datetime.datetime.now()
        completion_days = random.randint(30, 180)  # 1-6 months
        construction_completion_date = (now + timedelta(days=completion_days)).strftime("%Y-%m-%d")

    # Generate year built based on property value and type
    current_year = datetime.datetime.now().year

    if is_new_construction:
        year_built = current_year if random.random() < 0.7 else current_year + 1
    else:
        # Determine age distribution based on property type and value
        if property_type_enum in [PropertyType.PUD, PropertyType.CONDO] and (
                estimated_property_value and estimated_property_value > 1000000):
            # Luxury properties - either newer or completely renovated older homes
            if random.random() < 0.7:
                # Newer luxury homes (0-20 years old)
                year_built = random.randint(current_year - 20, current_year - 1)
            else:
                # Renovated historic or classic homes (20-100 years old)
                year_built = random.randint(current_year - 100, current_year - 20)
        elif property_type_enum in [PropertyType.CONDO, PropertyType.TOWNHOUSE]:
            # Condos and townhouses tend to be newer
            year_built = random.randint(current_year - 40, current_year - 1)
        elif property_type_enum == PropertyType.MANUFACTURED_HOME:
            # Manufactured homes tend to be newer
            year_built = random.randint(current_year - 30, current_year - 1)
        else:
            # Standard distribution for typical homes
            # Higher likelihood of homes in 10-50 year range
            age_options = [
                random.randint(current_year - 10, current_year - 1),  # 0-10 years
                random.randint(current_year - 50, current_year - 10),  # 10-50 years
                random.randint(current_year - 100, current_year - 50)  # 50-100 years
            ]
            age_weights = [0.2, 0.6, 0.2]
            year_built = random.choices(age_options, weights=age_weights)[0]

    # Generate bedrooms based on property type
    if property_type_enum == PropertyType.SINGLE_FAMILY:
        bedrooms = random.choices([2, 3, 4, 5, 6], weights=[0.05, 0.3, 0.4, 0.2, 0.05])[0]
    elif property_type_enum in [PropertyType.CONDO, PropertyType.TOWNHOUSE, PropertyType.MANUFACTURED_HOME]:
        bedrooms = random.choices([1, 2, 3, 4], weights=[0.1, 0.4, 0.4, 0.1])[0]
    elif property_type_enum == PropertyType.MULTI_FAMILY:
        bedrooms = random.randint(4, 8)  # Total across all units
    else:
        bedrooms = random.choices([2, 3, 4, 5], weights=[0.1, 0.4, 0.4, 0.1])[0]

    # Generate bathrooms (allowing for half baths)
    if property_type_enum in [PropertyType.PUD, PropertyType.COMMERCIAL]:
        # Luxury homes have more bathrooms
        bath_options = [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5]
        bath_weights = [0.05, 0.1, 0.2, 0.2, 0.2, 0.1, 0.1, 0.05]
    elif property_type_enum in [PropertyType.CONDO, PropertyType.TOWNHOUSE, PropertyType.MANUFACTURED_HOME]:
        bath_options = [1.0, 1.5, 2.0, 2.5, 3.0]
        bath_weights = [0.1, 0.2, 0.4, 0.2, 0.1]
    elif property_type_enum == PropertyType.MULTI_FAMILY:
        bath_options = [2.0, 3.0, 4.0, 5.0, 6.0]
        bath_weights = [0.1, 0.3, 0.3, 0.2, 0.1]
    else:
        bath_options = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5]
        bath_weights = [0.05, 0.1, 0.3, 0.3, 0.2, 0.05]

    bathrooms = random.choices(bath_options, weights=bath_weights)[0]

    # Generate square footage based on property type and bedrooms
    if property_type_enum in [PropertyType.PUD, PropertyType.COMMERCIAL]:
        base_sqft = 2500 + (bedrooms * 500)
        variation = random.uniform(0.8, 1.2)
    elif property_type_enum == PropertyType.CONDO:
        base_sqft = 1800 + (bedrooms * 400)
        variation = random.uniform(0.9, 1.1)
    elif property_type_enum in [PropertyType.CONDO, PropertyType.TOWNHOUSE]:
        base_sqft = 800 + (bedrooms * 300)
        variation = random.uniform(0.9, 1.1)
    elif property_type_enum == PropertyType.MANUFACTURED_HOME:
        base_sqft = 900 + (bedrooms * 200)
        variation = random.uniform(0.9, 1.1)
    elif property_type_enum == PropertyType.MULTI_FAMILY:
        base_sqft = 1200 + (bedrooms * 300)
        variation = random.uniform(0.9, 1.1)
    else:  # Standard single family
        base_sqft = 1000 + (bedrooms * 400)
        variation = random.uniform(0.9, 1.1)

    square_feet = int(base_sqft * variation)
    # Round to typical increments
    square_feet = (square_feet // 50) * 50

    # Generate lot size based on property type and location
    if property_type_enum in [PropertyType.CONDO, PropertyType.TOWNHOUSE]:
        # Condos and townhouses typically don't have significant lots
        lot_size = 0
    elif property_type_enum == PropertyType.MANUFACTURED_HOME:
        lot_options = [0.1, 0.25, 0.5, 1.0]  # Acres
        lot_weights = [0.4, 0.3, 0.2, 0.1]
    elif property_type_enum == PropertyType.MULTI_FAMILY:
        lot_options = [0.1, 0.25, 0.5, 0.75]  # Acres
        lot_weights = [0.3, 0.4, 0.2, 0.1]
    elif product_type == "usda":
        # USDA properties often have larger lots
        lot_options = [0.5, 1.0, 2.0, 5.0, 10.0]  # Acres
        lot_weights = [0.3, 0.3, 0.2, 0.15, 0.05]
    else:
        # Standard single family homes
        lot_options = [0.1, 0.25, 0.33, 0.5, 1.0, 2.0]  # Acres
        lot_weights = [0.15, 0.3, 0.2, 0.2, 0.1, 0.05]

    if property_type_enum not in [PropertyType.CONDO, PropertyType.TOWNHOUSE]:
        lot_size = random.choices(lot_options, weights=lot_weights)[0]

    # Generate HOA dues based on property type
    if property_type_enum in [PropertyType.CONDO, PropertyType.TOWNHOUSE]:
        if property_type_enum == PropertyType.CONDO:
            # Luxury condos have higher HOA dues
            hoa_base = random.randint(400, 1200)
        else:
            hoa_base = random.randint(150, 500)

        # Add randomness
        hoa_dues = (hoa_base // 25) * 25  # Round to nearest $25
    elif random.random() < 0.2:  # 20% chance of HOA for other property types
        hoa_base = random.randint(50, 200)
        hoa_dues = (hoa_base // 10) * 10  # Round to nearest $10
    else:
        hoa_dues = 0

    PROCESSED_APPLICATION_IDS.add(application_id)

    # Create the property dictionary with enum values - NO IDs included
    property_record = {
        "mortgage_services_application_id": application_id,
        "address": address,
        "property_type": property_type_enum.value,  # Use enum value directly
        "occupancy_type": occupancy_type_enum.value,  # Use enum value directly
        "year_built": year_built,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "square_feet": square_feet,
        "lot_size": lot_size,
        "hoa_dues": hoa_dues,
        "is_new_construction": is_new_construction,
        "construction_completion_date": construction_completion_date
    }

    return property_record
