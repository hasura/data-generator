import datetime
import random
from typing import Dict, Any

from data_generator import DataGenerator

from .enums import AccountStatus


def generate_random_account(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random consumer banking account with plausible values.

    Args:
        id_fields: Dictionary containing the required ID fields
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated account data
    """
    # Get database connection
    conn = dg.conn

    # Validate required fields
    if 'enterprise_account_id' not in id_fields:
        raise ValueError("enterprise_account_id is required")

    if 'consumer_banking_product_id' not in id_fields:
        raise ValueError("consumer_banking_product_id is required")

    # Fetch the enterprise account to get its opened date
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT opened_date 
            FROM enterprise.accounts 
            WHERE enterprise_account_id = %s
        """, (id_fields['enterprise_account_id'],))

        enterprise_account = cursor.fetchone()

        if not enterprise_account:
            raise ValueError(f"No enterprise account found with ID {id_fields['enterprise_account_id']}")

        enterprise_opened_date = enterprise_account['opened_date']

        # Generate today's date
        today = datetime.datetime.now(datetime.timezone.utc)

        # Calculate days since enterprise account opened
        days_since_enterprise_opened = (today - enterprise_opened_date).days

        # Randomly choose a date between enterprise account opened date and now
        additional_days = random.randint(0, days_since_enterprise_opened)
        opened_date = enterprise_opened_date + datetime.timedelta(days=additional_days)

        # Determine account status using the enum
        status = AccountStatus.get_random()

        # Status update date is after or on opened date
        days_since_opened = (today - opened_date).days
        status_update_days = random.randint(0, days_since_opened)
        status_update_date_time = opened_date + datetime.timedelta(days=status_update_days)

        # Create the account dictionary
        account = {
            "enterprise_account_id": id_fields['enterprise_account_id'],
            "consumer_banking_product_id": id_fields['consumer_banking_product_id'],
            "opened_date": opened_date,
            "status": status.value,
            "status_update_date_time": status_update_date_time
        }

        return account

    finally:
        cursor.close()
