import datetime
import random
from datetime import timedelta

from faker import Faker


def generate_random_property(loan_application):
    """
    Generate a random, plausible property record based on the loan application and product type.

    Args:
        loan_application (dict): The loan application data

    Returns:
        dict: A dictionary with property details
    """
    # Initialize Faker for address generation
    fake = Faker()

    # Extract relevant information from the application
    application_type = loan_application.get("application_type")
    loan_purpose = loan_application.get("loan_purpose")
    estimated_property_value = loan_application.get("estimated_property_value")
    product_type = loan_application.get("loan_product", "conventional").lower()
    lot_options = None
    lot_weights = None
    lot_size = None

    # Determine plausible property type based on loan product and purpose
    # Property types with weights - adjust based on product type
    if product_type == "jumbo":
        # Jumbo loans are often for larger, luxury properties
        property_types = {
            "single family": 0.7,
            "condo": 0.15,
            "townhouse": 0.05,
            "multi-family": 0.05,
            "luxury condo": 0.05
        }
    elif product_type == "fha":
        # FHA loans are often for modest starter homes
        property_types = {
            "single family": 0.6,
            "condo": 0.2,
            "townhouse": 0.15,
            "multi-family (2-4 units)": 0.05
        }
    elif product_type == "va":
        # VA loans typically for residential properties
        property_types = {
            "single family": 0.7,
            "condo": 0.15,
            "townhouse": 0.1,
            "multi-family (2-4 units)": 0.05
        }
    elif product_type == "usda":
        # USDA loans are for rural properties
        property_types = {
            "single family": 0.85,
            "manufactured home": 0.1,
            "modular home": 0.05
        }
    elif product_type == "heloc" or product_type == "reverse mortgage":
        # These typically apply to existing homes
        property_types = {
            "single family": 0.75,
            "condo": 0.15,
            "townhouse": 0.05,
            "multi-family (2-4 units)": 0.05
        }
    elif product_type == "construction loan":
        # Construction loans are for new builds
        property_types = {
            "single family": 0.8,
            "custom home": 0.15,
            "luxury home": 0.05
        }
    else:  # conventional
        property_types = {
            "single family": 0.65,
            "condo": 0.15,
            "townhouse": 0.1,
            "multi-family (2-4 units)": 0.05,
            "manufactured home": 0.05
        }

    # Select property type based on weights
    property_type = random.choices(
        list(property_types.keys()),
        weights=list(property_types.values())
    )[0]

    # Determine occupancy type based on loan purpose
    if loan_purpose == "primary residence":
        occupancy_type = "primary residence"
    elif loan_purpose == "second home":
        occupancy_type = "second home"
    elif loan_purpose == "investment property":
        occupancy_type = "investment"
    elif loan_purpose == "home improvement" and random.random() < 0.9:
        occupancy_type = "primary residence"  # Most home improvement loans are for primary homes
    elif loan_purpose == "refinancing" or loan_purpose == "cash-out refinancing":
        # For refinancing, use the original occupancy of the home
        occupancy_options = ["primary residence", "second home", "investment"]
        occupancy_weights = [0.8, 0.15, 0.05]  # Most refinances are for primary homes
        occupancy_type = random.choices(occupancy_options, weights=occupancy_weights)[0]
    else:
        # Default or fallback based on weighted probabilities
        occupancy_options = ["primary residence", "second home", "investment"]
        occupancy_weights = [0.7, 0.15, 0.15]
        occupancy_type = random.choices(occupancy_options, weights=occupancy_weights)[0]

    # Generate a complete address using Faker
    # Customize based on property type
    if property_type in ["condo", "townhouse", "luxury condo"]:
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
        if property_type in ["luxury home", "luxury condo", "custom home"] or (
                estimated_property_value and estimated_property_value > 1000000):
            # Luxury properties - either newer or completely renovated older homes
            if random.random() < 0.7:
                # Newer luxury homes (0-20 years old)
                year_built = random.randint(current_year - 20, current_year - 1)
            else:
                # Renovated historic or classic homes (20-100 years old)
                year_built = random.randint(current_year - 100, current_year - 20)
        elif property_type in ["condo", "townhouse"]:
            # Condos and townhouses tend to be newer
            year_built = random.randint(current_year - 40, current_year - 1)
        elif property_type == "manufactured home":
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
    if property_type in ["single family", "custom home", "luxury home"]:
        bedrooms = random.choices([2, 3, 4, 5, 6], weights=[0.05, 0.3, 0.4, 0.2, 0.05])[0]
    elif property_type in ["condo", "townhouse", "manufactured home"]:
        bedrooms = random.choices([1, 2, 3, 4], weights=[0.1, 0.4, 0.4, 0.1])[0]
    elif property_type == "multi-family (2-4 units)":
        bedrooms = random.randint(4, 8)  # Total across all units
    else:
        bedrooms = random.choices([2, 3, 4, 5], weights=[0.1, 0.4, 0.4, 0.1])[0]

    # Generate bathrooms (allowing for half baths)
    if property_type in ["luxury home", "luxury condo", "custom home"]:
        # Luxury homes have more bathrooms
        bath_options = [2.0, 2.5, 3.0, 3.5, 4.0, 4.5, 5.0, 5.5]
        bath_weights = [0.05, 0.1, 0.2, 0.2, 0.2, 0.1, 0.1, 0.05]
    elif property_type in ["condo", "townhouse", "manufactured home"]:
        bath_options = [1.0, 1.5, 2.0, 2.5, 3.0]
        bath_weights = [0.1, 0.2, 0.4, 0.2, 0.1]
    elif property_type == "multi-family (2-4 units)":
        bath_options = [2.0, 3.0, 4.0, 5.0, 6.0]
        bath_weights = [0.1, 0.3, 0.3, 0.2, 0.1]
    else:
        bath_options = [1.0, 1.5, 2.0, 2.5, 3.0, 3.5]
        bath_weights = [0.05, 0.1, 0.3, 0.3, 0.2, 0.05]

    bathrooms = random.choices(bath_options, weights=bath_weights)[0]

    # Generate square footage based on property type and bedrooms
    if property_type in ["luxury home", "custom home"]:
        base_sqft = 2500 + (bedrooms * 500)
        variation = random.uniform(0.8, 1.2)
    elif property_type == "luxury condo":
        base_sqft = 1800 + (bedrooms * 400)
        variation = random.uniform(0.9, 1.1)
    elif property_type in ["condo", "townhouse"]:
        base_sqft = 800 + (bedrooms * 300)
        variation = random.uniform(0.9, 1.1)
    elif property_type == "manufactured home":
        base_sqft = 900 + (bedrooms * 200)
        variation = random.uniform(0.9, 1.1)
    elif property_type == "multi-family (2-4 units)":
        base_sqft = 1200 + (bedrooms * 300)
        variation = random.uniform(0.9, 1.1)
    else:  # Standard single family
        base_sqft = 1000 + (bedrooms * 400)
        variation = random.uniform(0.9, 1.1)

    square_feet = int(base_sqft * variation)
    # Round to typical increments
    square_feet = (square_feet // 50) * 50

    # Generate lot size based on property type and location
    if property_type in ["condo", "townhouse", "luxury condo"]:
        # Condos and townhouses typically don't have significant lots
        lot_size = 0
    elif property_type == "manufactured home":
        lot_options = [0.1, 0.25, 0.5, 1.0]  # Acres
        lot_weights = [0.4, 0.3, 0.2, 0.1]
    elif property_type == "multi-family (2-4 units)":
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

    if property_type not in ["condo", "townhouse", "luxury condo"]:
        lot_size = random.choices(lot_options, weights=lot_weights)[0]

    # Generate HOA dues based on property type
    if property_type in ["condo", "townhouse", "luxury condo"]:
        if property_type == "luxury condo":
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

    # Create the property dictionary
    _property_record = {
        "address": address,
        "property_type": property_type,
        "occupancy_type": occupancy_type,
        "year_built": year_built,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "square_feet": square_feet,
        "lot_size": lot_size,
        "hoa_dues": hoa_dues,
        "is_new_construction": is_new_construction,
        "construction_completion_date": construction_completion_date
    }

    # Include application ID if provided in the loan application
    if "mortgage_services_application_id" in loan_application:
        _property_record["mortgage_services_application_id"] = loan_application["mortgage_services_application_id"]

    return _property_record
