import logging
import random
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

from faker import Faker

from data_generator import DataGenerator
from fsi_data_generator.fsi_generators.helpers.generate_unique_json_array import \
    generate_unique_json_array
from fsi_data_generator.fsi_generators.intelligent_generators.mortgage_services.enums.asset_type import \
    AssetType
from fsi_data_generator.fsi_generators.intelligent_generators.mortgage_services.enums.verification_status import \
    VerificationStatus

fake = Faker()
logger = logging.getLogger(__name__)


def generate_borrower_asset(ids_dict: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a single random, realistic borrower asset record for a mortgage application.
    The verification date will be set shortly after the application date.

    Args:
        ids_dict: Dictionary containing the required ID fields
        dg: DataGenerator instance

    Returns:
        dict: A dictionary containing a realistic borrower asset record
    """
    try:
        conn = dg.conn

        # First, find the application date by following the relationship model
        application_date = _get_application_date(ids_dict.get('mortgage_services_borrower_id'), conn)

        # Financial institutions
        financial_institutions = generate_unique_json_array(
            dbml_string=dg.dbml,
            fully_qualified_column_name='mortgage_services.borrower_assets.institution_name',
            count=50,
            cache_key='financial_institutions'
        )

        # Select an asset type using weighted random choice
        asset_type = AssetType.get_random()

        # Generate institution name based on asset type
        if asset_type in [AssetType.CHECKING_ACCOUNT, AssetType.SAVINGS_ACCOUNT, AssetType.MONEY_MARKET,
                          AssetType.CERTIFICATE_OF_DEPOSIT]:
            # Banks more likely for deposit accounts
            institution_name = random.choice(financial_institutions[:12])
        elif asset_type in [AssetType.BROKERAGE_ACCOUNT, AssetType.RETIREMENT_ACCOUNT, AssetType.STOCK_EQUITY,
                            AssetType.BONDS, AssetType.MUTUAL_FUND]:
            # Investment firms more likely for investment accounts
            institution_name = random.choice(financial_institutions[12:18])
        elif asset_type == AssetType.LIFE_INSURANCE:
            # Insurance companies for life insurance
            institution_name = random.choice(financial_institutions[18:21])
        elif asset_type in [AssetType.INVESTMENT_PROPERTY, AssetType.PRIMARY_RESIDENCE, AssetType.SECONDARY_RESIDENCE,
                            AssetType.VEHICLE, AssetType.OTHER_REAL_ESTATE]:
            # No institution for real estate or vehicles
            institution_name = None
        else:
            institution_name = random.choice(financial_institutions)

        # Generate account number if applicable
        if asset_type in [
            AssetType.CHECKING_ACCOUNT, AssetType.SAVINGS_ACCOUNT, AssetType.MONEY_MARKET,
            AssetType.CERTIFICATE_OF_DEPOSIT, AssetType.BROKERAGE_ACCOUNT, AssetType.RETIREMENT_ACCOUNT,
            AssetType.LIFE_INSURANCE, AssetType.TRUST_ACCOUNT
        ]:
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
            AssetType.CHECKING_ACCOUNT: (500, 20000),
            AssetType.SAVINGS_ACCOUNT: (1000, 50000),
            AssetType.MONEY_MARKET: (5000, 100000),
            AssetType.CERTIFICATE_OF_DEPOSIT: (1000, 50000),
            AssetType.BROKERAGE_ACCOUNT: (10000, 500000),
            AssetType.RETIREMENT_ACCOUNT: (20000, 1000000),
            AssetType.STOCK_EQUITY: (5000, 300000),
            AssetType.BONDS: (10000, 200000),
            AssetType.MUTUAL_FUND: (10000, 300000),
            AssetType.INVESTMENT_PROPERTY: (100000, 2000000),
            AssetType.OTHER_REAL_ESTATE: (100000, 2000000),
            AssetType.PRIMARY_RESIDENCE: (150000, 3000000),
            AssetType.SECONDARY_RESIDENCE: (100000, 2000000),
            AssetType.VEHICLE: (5000, 75000),
            AssetType.LIFE_INSURANCE: (10000, 500000),
            AssetType.TRUST_ACCOUNT: (50000, 1000000),
            AssetType.CRYPTOCURRENCY: (1000, 100000),
            AssetType.BUSINESS_EQUITY: (20000, 1000000),
            AssetType.OTHER: (1000, 50000)
        }

        min_value, max_value = value_ranges.get(asset_type, (1000, 50000))
        current_value = round(random.uniform(min_value, max_value), 2)

        verification_status = VerificationStatus.get_random([0.4, 0.3, 0.1, 0.15, 0.05, 0.0])

        # Generate verification date only if verification status indicates completion
        verification_date_str = None
        if verification_status not in [VerificationStatus.UNVERIFIED, VerificationStatus.PENDING]:
            if application_date:
                verification_date = application_date + timedelta(days=random.randint(3, 30))
                verification_date_str = verification_date.strftime("%Y-%m-%d")
            else:
                # If we couldn't find application date, use a recent date
                verification_date_str = (datetime.now() - timedelta(days=random.randint(10, 90))).strftime("%Y-%m-%d")

        # Determine if we need a property address ID
        property_address = None
        if asset_type in [AssetType.OTHER_REAL_ESTATE, AssetType.INVESTMENT_PROPERTY, AssetType.PRIMARY_RESIDENCE,
                          AssetType.SECONDARY_RESIDENCE]:
            property_address = fake.address()

        # Create and return the asset record
        asset_record = {
            "asset_type": asset_type.value,  # Store enum value as string
            "institution_name": institution_name,
            "account_number": account_number,
            "current_value": current_value,
            "verification_status": verification_status.value,  # Store enum value as string
            "verification_date": verification_date_str,
            "property_address": property_address
        }

        return asset_record

    except Exception as e:
        logger.error(f"Error generating borrower asset: {e}")
        # Return a default record using enum values
        return {
            "asset_type": AssetType.CHECKING_ACCOUNT.value,
            "institution_name": "Default Bank",
            "account_number": "XXXX1234",
            "current_value": 10000.00,
            "verification_status": VerificationStatus.PENDING.value,
            "verification_date": None,
            "property_address": None
        }


def _get_application_date(borrower_id: Optional[int], conn) -> Optional[datetime]:
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
        cursor = conn.cursor()

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
