import logging
import random
from datetime import datetime, timedelta
from typing import Any, Dict

from faker import Faker

from data_generator import DataGenerator, SkipRowGenerationError

# Track previously generated account ID strings for uniqueness
prev_account_id_strings = set()
logger = logging.getLogger(__name__)


def generate_random_account(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random security.accounts record.

    Args:
        id_fields: Dictionary containing predetermined ID fields
                  (security_account_id, security_identity_id, security_source_id)
        dg: DataGenerator instance

    Returns:
        Dict containing a random account record
        (without ID fields)
    """
    fake = Faker()

    # Try to fetch the related identity information if possible
    identity_info = _fetch_identity_info(id_fields.get('security_identity_id'), dg)

    # Try to fetch the source system information if possible
    source_info = _fetch_source_system_info(id_fields.get('security_source_id'), dg)

    # Generate account name based on identity info if available
    if identity_info and identity_info.get('name'):
        identity_name = identity_info.get('name')
        account_name = identity_name

        # Add source-specific prefix or suffix if available
        if source_info and source_info.get('application_name'):
            source_name = source_info.get('application_name')
            account_name = f"{identity_name} on {source_name}"
    else:
        # Fallback: generate generic account name
        account_name = f"Account-{fake.word()}-{fake.random_int(min=1000, max=9999)}"

    # Generate a unique account ID string
    account_id_prefix = "ACC"
    if source_info and source_info.get('application_name'):
        # Use source system abbreviation as prefix if available
        source_abbr = ''.join([c for c in source_info.get('application_name') if c.isupper()])
        if source_abbr:
            account_id_prefix = source_abbr[:3]

    account_id_string = f"{account_id_prefix}-{fake.random_int(min=10000, max=99999)}"

    # Ensure account_id_string is unique
    global prev_account_id_strings
    retries = 0
    while account_id_string in prev_account_id_strings and retries < 5:
        account_id_string = f"{account_id_prefix}-{fake.random_int(min=10000, max=99999)}"
        retries += 1

    if account_id_string in prev_account_id_strings:
        raise SkipRowGenerationError
    else:
        prev_account_id_strings.add(account_id_string)

    # Account status properties with weighted probabilities
    disabled = random.choices([True, False], weights=[0.2, 0.8])[0]
    locked = random.choices([True, False], weights=[0.1, 0.9])[0]
    privileged = random.choices([True, False], weights=[0.15, 0.85])[0]
    manually_correlated = random.choices([True, False], weights=[0.3, 0.7])[0]

    # Generate dates with realistic constraints
    now = datetime.now()

    # Account creation between 1-5 years ago
    created = now - timedelta(days=random.randint(365, 365 * 5))

    # Password last set between 1 day and 180 days ago
    password_last_set = now - timedelta(days=random.randint(1, 180))

    # Generate a reasonable status_update_date_time
    if disabled or locked:
        # For disabled or locked accounts, set status_update_date_time to sometime
        # between creation date and now, with bias toward more recent updates
        time_since_creation = (now - created).total_seconds()
        # 70% of status updates happened in the last 30% of account lifetime
        if random.random() < 0.7:
            random_seconds = int(time_since_creation * 0.7) + random.randint(0, int(time_since_creation * 0.3))
        else:
            random_seconds = random.randint(0, int(time_since_creation))

        status_update_date_time = created + timedelta(seconds=random_seconds)
    else:
        # For active accounts, status may have been updated at any point
        # Use creation date as the status update time 30% of the time
        if random.random() < 0.3:
            status_update_date_time = created
        else:
            # Otherwise, choose a random time between creation and now
            time_since_creation = (now - created).total_seconds()
            random_seconds = random.randint(0, int(time_since_creation))
            status_update_date_time = created + timedelta(seconds=random_seconds)

    # Construct the account record (without ID fields)
    account = {
        "name": account_name,
        "account_id_string": account_id_string,
        "disabled": disabled,
        "locked": locked,
        "privileged": privileged,
        "manually_correlated": manually_correlated,
        "password_last_set": password_last_set.isoformat(),
        "created": created.isoformat(),
        "status_update_date_time": status_update_date_time.isoformat()
    }

    return account


def _fetch_identity_info(identity_id: Any, dg: DataGenerator) -> Dict[str, Any]:
    """
    Fetch identity information from the database

    Args:
        identity_id: UUID of the identity
        dg: DataGenerator instance

    Returns:
        Dictionary with identity information, or empty dict if not found
    """
    if not identity_id:
        return {}

    try:
        # Try to query the identity information
        query = """
        SELECT name, display_name, owner_id
        FROM security.identities
        WHERE security_identity_id = %s
        """

        with dg.conn.cursor() as cursor:
            cursor.execute(query, (identity_id,))
            result = cursor.fetchone()

        return result

    except Exception as e:
        logger.error(e)
        # Handle connection errors or other issues
        pass

    return {}


def _fetch_source_system_info(source_id: Any, dg: DataGenerator) -> Dict[str, Any]:
    """
    Fetch source system information from the database

    Args:
        source_id: UUID of the source system (application)
        dg: DataGenerator instance

    Returns:
        Dictionary with source system information, or empty dict if not found
    """
    if not source_id:
        return {}

    try:
        # Try to query the application information
        query = """
        SELECT application_name, application_type
        FROM app_mgmt.applications
        WHERE app_mgmt_application_id = %s
        """

        with dg.conn.cursor() as cursor:
            cursor.execute(query, (source_id,))
            result = cursor.fetchone()

        return result

    except Exception as e:
        logger.error(e)
        # Handle connection errors or other issues
        pass

    return {}
