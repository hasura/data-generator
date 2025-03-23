import logging
import random
from datetime import datetime, timedelta
from typing import cast

import psycopg2
from faker import Faker
from psycopg2.extras import RealDictCursor

from data_generator import DataGenerator
from fsi_data_generator.fsi_generators.helpers.generate_unique_json_array import \
    generate_unique_json_array

# from data_generator import DataGenerator

fake = Faker()

logger = logging.getLogger(__name__)


def generate_borrower_asset(ids_dict, dg: DataGenerator):
    """
    Generate a single random, realistic borrower asset record for a mortgage application.
    The verification date will be set shortly after the application date.

    Args:
        ids_dict
        dg

    Returns:
        dict: A dictionary containing a realistic borrower asset record
    """
    try:
        try:
            conn = dg.conn
        except AttributeError:
            conn = dg

        # First, find the application date by following the relationship model
        application_date = get_application_date(ids_dict.get('mortgage_services_borrower_id'), conn)

        # Asset types commonly reported on mortgage applications
        asset_types = [
            "checking account", "savings account", "money market account",
            "certificate of deposit", "investment account", "retirement account",
            "stocks", "bonds", "mutual funds", "real estate property",
            "vehicle", "cash value life insurance"
        ]

        # Financial institutions
        financial_institutions = generate_unique_json_array(
            dbml_string=dg.dbml,
            fully_qualified_column_name='mortgage_services.borrower_assets.institution_name',
            count=50,
            cache_key='financial_institutions'
        )

        # Verification statuses
        verification_statuses = [
            "verified", "pending", "partial verification", "not verified"
        ]

        # Select an asset type
        asset_type = random.choice(asset_types)

        # Generate institution name based on asset type
        if asset_type in ["checking account", "savings account", "money market account", "certificate of deposit"]:
            # Banks more likely for deposit accounts
            institution_name = random.choice(financial_institutions[:12])
        elif asset_type in ["investment account", "retirement account", "stocks", "bonds", "mutual funds"]:
            # Investment firms more likely for investment accounts
            institution_name = random.choice(financial_institutions[12:18])
        elif asset_type == "cash value life insurance":
            # Insurance companies for life insurance
            institution_name = random.choice(financial_institutions[18:21])
        elif asset_type == "real estate property":
            # No institution for real estate
            institution_name = None
        elif asset_type == "vehicle":
            # No institution for vehicle
            institution_name = None
        else:
            institution_name = random.choice(financial_institutions)

        # Generate account number if applicable
        if asset_type in ["checking account", "savings account", "money market account",
                          "certificate of deposit", "investment account", "retirement account",
                          "cash value life insurance"]:
            account_number = "".join([str(random.randint(0, 9)) for _ in range(8)])
            # Sometimes mask part of the number for security
            if random.random() < 0.7:  # 70% chance of masking
                visible_digits = random.randint(2, 4)
                masked_part = "X" * (8 - visible_digits)
                account_number = masked_part + account_number[-visible_digits:]
        else:
            account_number = None

        # Generate current value based on asset type
        value_ranges = {
            "checking account": (500, 20000),
            "savings account": (1000, 50000),
            "money market account": (5000, 100000),
            "certificate of deposit": (1000, 50000),
            "investment account": (10000, 500000),
            "retirement account": (20000, 1000000),
            "stocks": (5000, 300000),
            "bonds": (10000, 200000),
            "mutual funds": (10000, 300000),
            "real estate property": (100000, 2000000),
            "vehicle": (5000, 75000),
            "cash value life insurance": (10000, 500000)
        }

        min_value, max_value = value_ranges[asset_type]
        current_value = round(random.uniform(min_value, max_value), 2)

        # Generate verification status
        verification_status = random.choice(verification_statuses)

        # Generate verification date only if verification status indicates completion
        if verification_status in ["verified", "partial verification"]:
            if application_date:
                verification_date = application_date + timedelta(days=random.randint(3, 30))
                verification_date_str = verification_date.strftime("%Y-%m-%d")
            else:
                # If we couldn't find application date, use a recent date
                verification_date_str = (datetime.now() - timedelta(days=random.randint(10, 90))).strftime("%Y-%m-%d")
        else:
            # For pending or not verified statuses, set verification_date to None
            verification_date_str = None

        # Note: We're not handling property_address_id as requested
        # For real estate property, the property_address_id would typically be set,
        # but we're assuming it's already populated

        # Create and return the asset record
        # Skip fields ending with _id as they're already populated
        asset_record = {
            "asset_type": asset_type,
            "institution_name": institution_name,
            "account_number": account_number,
            "current_value": current_value,
            "verification_status": verification_status,
            "verification_date": verification_date_str
        }

        return asset_record

    except Exception as e:
        logger.error(f"Error generating borrower asset: {e}")
        return {
            "asset_type": "checking account",
            "institution_name": "Default Bank",
            "account_number": "XXXX1234",
            "current_value": 10000.00,
            "verification_status": "pending",
            "verification_date": None  # No verification date for pending status
        }


def get_application_date(borrower_id, conn):
    """
    Get the application date by following the relationship model:
    borrower -> application_borrowers -> applications

    Args:
        borrower_id (int): The ID of the borrower
        conn: PostgreSQL database connection

    Returns:
        datetime: The application date or None if not found
    """

    cursor = None
    try:
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        # Query to get the application date through the relationship chain
        query = """
        SELECT a.creation_date_time 
        FROM mortgage_services.applications a
        JOIN mortgage_services.application_borrowers ab 
            ON a.mortgage_services_application_id = ab.mortgage_services_application_id
        WHERE ab.mortgage_services_borrower_id = %s
        ORDER BY a.creation_date_time DESC
        LIMIT 1
        """

        cursor.execute(query, (borrower_id,))
        result = cursor.fetchone()

        if result and result['creation_date_time']:
            return result['creation_date_time']
        else:
            # If no application found, return None
            return None

    except Exception as e:
        logger.error(f"Error getting application date: {e}")
        return None
    finally:
        if cursor:
            cursor.close()


# Removed get_random_address_id function as we're not handling _id fields

# Example usage
if __name__ == "__main__":
    # This would be replaced with actual database connection in production
    connection_string = "postgresql://postgres:password@localhost:5432/postgres"
    conn = None
    try:
        # Connect to the database
        conn = psycopg2.connect(connection_string)

        # Generate an asset record for borrower ID 123
        asset = generate_borrower_asset({'mortgage_services_borrower_id': 40}, cast(DataGenerator, {conn: conn}))

        # Print the generated asset record
        # logger.debug(json.dumps(asset, indent=2))

    except Exception as e:
        logger.error(f"Error: {e}")
    finally:
        if conn:
            conn.close()
