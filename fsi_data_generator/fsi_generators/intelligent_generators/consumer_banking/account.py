from .enums import AccountStatus, ProductType

from data_generator import DataGenerator
from typing import Any, Dict

import datetime
import random

from ..enterprise.enums import CurrencyCode
from ...helpers.constants import INSTITUTIONAL_BIC

# Static incrementing value for generated account numbers
_account_number_counter = 1

# Nickname choices based on product type
_nicknames_by_product_type = {
    "CHECKING": ["Daily Expenses", "Checking", "Main Account"],
    "SAVINGS": ["Rainy Day", "Savings", "Emergency Fund", "Vacation Fund"],
    "MONEY_MARKET": ["Investment Fund", "High Yield"],
    "CERTIFICATE_OF_DEPOSIT": ["Long-term Savings", "Secure Fund"],
    "IRA": ["Retirement", "Future Fund"],
    "HSA": ["Health Savings", "Medical Expenses"],
    "STUDENT": ["College Fund", "School Savings"],
    "YOUTH": ["My First Account", "Youth Savings"],
    "SENIOR": ["Golden Years", "Senior Savings"],
    "BUSINESS_CHECKING": ["Business Expenses", "Operations Account"],
    "BUSINESS_SAVINGS": ["Business Reserve", "Business Savings"],
    "PREMIUM": ["Elite Account", "Premium Savings"],
    "FOREIGN_CURRENCY": ["Travel Fund", "Foreign Exchange"],
    "SPECIALIZED": ["Special Projects", "Targeted Savings"]
}


def generate_random_account(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random consumer banking account with plausible values.

    Args:
        id_fields: Dictionary containing the required ID fields
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated account data
    """
    global _account_number_counter

    conn = dg.conn

    # Validate required fields
    if 'enterprise_account_id' not in id_fields:
        raise ValueError("enterprise_account_id is required")

    if 'consumer_banking_product_id' not in id_fields:
        raise ValueError("consumer_banking_product_id is required")

    enterprise_account_id = id_fields["enterprise_account_id"]
    consumer_banking_product_id = id_fields["consumer_banking_product_id"]

    cursor = conn.cursor()

    # Fetch the enterprise account to get its opened date
    cursor.execute("""
        SELECT opened_date 
        FROM enterprise.accounts
        WHERE enterprise_account_id = %s
    """, (enterprise_account_id,))
    result = cursor.fetchone()
    if not result:
        raise ValueError(f"Enterprise account ID {enterprise_account_id} not found")

    opened_date = result["opened_date"]

    cursor.execute("""
        SELECT enterprise_identifier_id
        FROM enterprise.identifiers
        WHERE scheme_name = 'BIC' AND identification = %s
        LIMIT 1
    """, (INSTITUTIONAL_BIC,))
    result = cursor.fetchone()
    if not result:
        raise RuntimeError(f"Institutional BIC identifier {INSTITUTIONAL_BIC} not found in enterprise.enterprise_identifiers")

    servicer_identifier_id = result["enterprise_identifier_id"]

    cursor.execute("""
        SELECT product_type, product_name, base_interest_rate
        FROM consumer_banking.products
        WHERE consumer_banking_product_id = %s
    """, (consumer_banking_product_id,))
    result = cursor.fetchone()
    if not result:
        raise ValueError(f"Product ID {consumer_banking_product_id} not found")

    product_type_str, product_name, base_interest_rate = result["product_type"], result["product_name"], result["base_interest_rate"]
    product_type = ProductType[product_type_str]

    nickname = random.choice(_nicknames_by_product_type.get(product_type_str, ["Account"]))

    account_number = f"CBA-{str(enterprise_account_id).zfill(6)}-{str(consumer_banking_product_id).zfill(4)}-{str(_account_number_counter).zfill(4)}"
    _account_number_counter += 1

    status = AccountStatus.get_random()
    delta_days = random.randint(5, 400)
    status_update_date_time = opened_date + datetime.timedelta(days=delta_days)

    # Generate displayName
    display_name = f"{product_name} ({account_number[-4:]})"

    # Interest-earning logic
    if product_type in [ProductType.SAVINGS, ProductType.CERTIFICATE_OF_DEPOSIT, ProductType.MONEY_MARKET]:
        annual_percentage_yield = base_interest_rate or round(random.uniform(0.01, 0.05), 5)
        interest_ytd = round(random.uniform(0, 500), 2)
    else:
        annual_percentage_yield = None
        interest_ytd = None

    # Time-bound product logic specifically for CDs
    if product_type == ProductType.CERTIFICATE_OF_DEPOSIT:
        term = random.choice([6, 12, 24, 36, 48, 60])
        maturity_date = opened_date + datetime.timedelta(days=30 * term)
    else:
        term = None
        maturity_date = None

    return {
        "enterprise_account_id": enterprise_account_id,
        "consumer_banking_product_id": consumer_banking_product_id,
        "opened_date": opened_date,
        "nickname": nickname,
        "displayName": display_name,
        "account_number": account_number,
        "account_category": "PERSONAL",
        "currency_code": CurrencyCode.USD.value,
        "status": status.value,
        "switch_status": "NOT_SWITCHED",
        "status_update_date_time": status_update_date_time,
        "servicer_identifier_id": servicer_identifier_id,
        "annualPercentageYield": round(annual_percentage_yield,3) if annual_percentage_yield is not None else None,
        "interestYtd": round(interest_ytd,5) if interest_ytd is not None else None,
        "term": term,
        "maturityDate": maturity_date,
    }
