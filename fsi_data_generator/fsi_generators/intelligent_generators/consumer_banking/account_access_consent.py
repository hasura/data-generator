import datetime
import random
from typing import Dict, Any

from data_generator import DataGenerator

from .enums import ConsentStatus


def generate_random_account_access_consent(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random consumer banking account access consent with plausible values.

    Args:
        id_fields: Dictionary containing the required ID fields
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated account consent data
    """
    # Get database connection
    conn = dg.conn

    # Validate required fields
    if 'consumer_banking_account_id' not in id_fields:
        raise ValueError("consumer_banking_account_id is required")

    # Fetch the consumer banking account to get its opened date
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT opened_date 
            FROM consumer_banking.accounts 
            WHERE consumer_banking_account_id = %s
        """, (id_fields['consumer_banking_account_id'],))

        consumer_account = cursor.fetchone()

        if not consumer_account:
            raise ValueError(f"No consumer banking account found with ID {id_fields['consumer_banking_account_id']}")

        account_opened_date = consumer_account.get('opened_date')

        # Generate today's date
        today = datetime.datetime.now(datetime.timezone.utc)

        # Calculate days since account opened
        days_since_account_opened = (today - account_opened_date).days

        # Randomly choose a creation date between account opened date and now
        additional_days = random.randint(0, days_since_account_opened)
        creation_date_time = account_opened_date + datetime.timedelta(days=additional_days)

        # Determine consent status using the enum
        consent_status = ConsentStatus.get_random()

        # Status update date is after creation date
        days_since_creation = (today - creation_date_time).days
        status_update_days = random.randint(0, days_since_creation) if days_since_creation > 0 else 0
        status_update_date_time = creation_date_time + datetime.timedelta(days=status_update_days)

        # Generate expiration date (if applicable)
        # Most consents expire 90 days after creation, but we'll add some variation
        expiration_period = random.randint(30, 180)  # Between 1 month and 6 months
        expiration_date_time = creation_date_time + datetime.timedelta(days=expiration_period)

        # If status is EXPIRED, ensure expiration date is in the past
        if consent_status == ConsentStatus.EXPIRED:
            # Make sure expiration date is between creation date and today
            days_until_expiration = random.randint(1, days_since_creation) if days_since_creation > 1 else 1
            expiration_date_time = creation_date_time + datetime.timedelta(days=days_until_expiration)

            # Status update should be on or after expiration date for EXPIRED status
            status_update_date_time = max(status_update_date_time, expiration_date_time)

        # If status is REVOKED or TERMINATED, there should be no future expiration
        if consent_status in [ConsentStatus.REVOKED, ConsentStatus.TERMINATED, ConsentStatus.REJECTED]:
            # Status update should be before expiration
            if status_update_date_time >= expiration_date_time:
                expiration_date_time = None

        # Create the consent dictionary
        consent = {
            "creation_date_time": creation_date_time,
            "status": consent_status.value,
            "status_update_date_time": status_update_date_time,
            "expiration_date_time": expiration_date_time
        }

        return consent

    finally:
        cursor.close()
