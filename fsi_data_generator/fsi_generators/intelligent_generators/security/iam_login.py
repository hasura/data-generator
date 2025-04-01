from data_generator import DataGenerator
from datetime import datetime, timedelta
from typing import Any, Dict

import logging
import random

logger = logging.getLogger(__name__)


def generate_random_iam_login(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random security.iam_logins record.

    Args:
        id_fields: Dictionary containing predetermined ID fields
                  (security_login_id, security_account_id)
        dg: DataGenerator instance

    Returns:
        Dict containing a random IAM login record
        (without ID fields)
    """
    # Fetch information about the account referenced by security_account_id
    account_info = _fetch_account_info(id_fields.get('security_account_id'), dg)

    # Current timestamp
    now = datetime.now()

    # Determine the latest possible login time based on account status
    if account_info.get('disabled', False) or account_info.get('locked', False):
        # If account is disabled or locked, login must be before the status update time
        status_update_time = account_info.get('status_update_date_time')
        if status_update_time:
            # Convert string timestamp to datetime if needed
            if isinstance(status_update_time, str):
                try:
                    status_update_time = datetime.fromisoformat(status_update_time)
                except ValueError:
                    status_update_time = now - timedelta(days=30)
            latest_possible_login = status_update_time
        else:
            # Fallback if status update time is somehow missing
            latest_possible_login = now - timedelta(days=30)
    else:
        # If account is active and not locked, login could be up to now
        latest_possible_login = now

    # Generate login timestamp (within the last 90 days, but before account was disabled/locked)
    earliest_login_time = now - timedelta(days=90)

    # Make sure we respect the account creation date as well
    account_created = account_info.get('created')
    if account_created:
        # Convert string timestamp to datetime if needed
        if isinstance(account_created, str):
            try:
                account_created = datetime.fromisoformat(account_created)
            except ValueError:
                account_created = earliest_login_time

        # Logins can't happen before the account was created
        if account_created > earliest_login_time:
            earliest_login_time = account_created

    if latest_possible_login < earliest_login_time:
        # Edge case: if latest possible login is before the earliest login time
        # (e.g., account was disabled/locked very soon after creation)
        login_time = latest_possible_login - timedelta(
            hours=random.randint(0, 24),
            minutes=random.randint(0, 59)
        )
    else:
        # Generate a random time between earliest_login_time and latest_possible_login
        time_range = (latest_possible_login - earliest_login_time).total_seconds()
        random_seconds = random.randint(0, int(time_range))
        login_time = earliest_login_time + timedelta(seconds=random_seconds)

    # Determine if there was a logout (80% chance)
    has_logout = random.random() < 0.8

    # Generate logout time if applicable (0-8 hours after login)
    logout_time = None
    if has_logout:
        session_duration = timedelta(minutes=random.randint(1, 480))
        logout_time = login_time + session_duration

        # Ensure logout time isn't after the account was disabled/locked
        if (account_info.get('disabled', False) or account_info.get('locked',
                                                                    False)) and logout_time > latest_possible_login:
            logout_time = latest_possible_login

        # Ensure logout time isn't in the future
        if logout_time > now:
            logout_time = now

    # Login methods with weighted distributions
    login_methods = [
        ("password", 0.5),
        ("sso", 0.2),
        ("mfa", 0.15),
        ("certificate", 0.05),
        ("api-key", 0.05),
        ("token", 0.03),
        ("biometric", 0.02)
    ]

    login_method = random.choices(
        [method for method, _ in login_methods],
        weights=[weight for _, weight in login_methods],
        k=1
    )[0]

    # Get username from account information
    user_name = account_info.get('name') or account_info.get('account_id_string')

    # Construct the IAM login record (without ID fields)
    iam_login = {
        "user_name": user_name,
        "login_time": login_time.isoformat(),
        "logout_time": logout_time.isoformat() if logout_time else None,
        "login_method": login_method
    }

    return iam_login


def _fetch_account_info(account_id: Any, dg: DataGenerator) -> Dict[str, Any]:
    """
    Fetch information about a specific account from the database

    Args:
        account_id: UUID of the account
        dg: DataGenerator instance

    Returns:
        Dictionary with account information, or an empty dict if not found
    """
    if not account_id:
        return {}

    try:
        # Try to query the account information
        query = """
        SELECT name, account_id_string, disabled, locked, security_source_id, 
               status_update_date_time, created  
        FROM security.accounts
        WHERE security_account_id = %s
        """

        with dg.conn.cursor() as cursor:
            cursor.execute(query, (account_id,))
            result = cursor.fetchone()

        return result

    except Exception as e:
        # Handle connection errors or other issues
        logger.error(f"Error fetching account info: {e}")
        pass

    # Return empty dict if account not found
    return {}
