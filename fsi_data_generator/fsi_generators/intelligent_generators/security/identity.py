from data_generator import DataGenerator, SkipRowGenerationError
from datetime import datetime, timedelta, timezone
from faker import Faker
from typing import Any, Dict

import logging
import random

# Track previously generated identity names for uniqueness
prev_identity_names = set()
logger = logging.getLogger(__name__)


def generate_random_identity(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random "security.identities" record.

    Args:
        id_fields: Dictionary containing predetermined ID fields
                  (security_identity_id, owner, security_identity_profile_id)
        dg: DataGenerator instance

    Returns:
        Dict containing a random identity record
        (without ID fields)
    """
    fake = Faker()

    # Try to fetch the related owner information if possible
    owner_info = _fetch_owner_info(id_fields.get('owner_id'), dg)

    # Try to fetch the identity profile information if possible
    profile_info = _fetch_profile_info(id_fields.get('security_identity_profile_id'), dg)

    # Generate identity name formats
    name_formats = [
        # Personal identity formats
        lambda o: f"{o.get('first_name', fake.first_name())}.{o.get('last_name', fake.last_name())}",
        lambda o: f"{o.get('first_name', fake.first_name())[0]}{o.get('last_name', fake.last_name())}",
        lambda o: f"{o.get('first_name', fake.first_name())}{o.get('last_name', fake.last_name())[0]}",
        lambda o: f"{o.get('last_name', fake.last_name())}.{o.get('first_name', fake.first_name())}",
        # Service account formats
        lambda _: f"svc.{fake.word().lower()}.{fake.word().lower()}",
        lambda _: f"app.{fake.word().lower()}.{fake.domain_word().lower()}",
        lambda _: f"sys.{fake.word().lower()}.{random.randint(1000, 9999)}",
        lambda _: f"bot.{fake.word().lower()}.{fake.word().lower()}",
        # Generic formats
        lambda _: f"{fake.user_name()}"
    ]

    # Determine if this is a service account (30% chance if no owner info)
    is_service_account = False
    if not owner_info:
        is_service_account = random.random() < 0.3

    # Generate identity name
    if is_service_account:
        # Use service account naming formats
        name_format = random.choice(name_formats[4:8])
        internal_name = name_format({})
        display_name = f"Service: {internal_name.split('.')[1].title()}"
    elif owner_info:
        # Use personal identity naming formats based on owner
        name_format = random.choice(name_formats[0:4])
        internal_name = name_format(owner_info).lower()
        display_name = f"{owner_info.get('first_name', 'User')} {owner_info.get('last_name', 'Unknown')}"
    else:
        # Generic fallback
        name_format = name_formats[-1]
        internal_name = name_format({})
        display_name = f"{fake.first_name()} {fake.last_name()}"

    # Ensure name uniqueness
    global prev_identity_names
    retries = 0
    while internal_name in prev_identity_names and retries < 5:
        # Append random numbers to ensure uniqueness
        internal_name = f"{internal_name}{random.randint(1, 999)}"
        retries += 1

    if internal_name in prev_identity_names:
        raise SkipRowGenerationError
    else:
        prev_identity_names.add(internal_name)

    # Generate timestamps with realistic constraints
    now = datetime.now(timezone.utc)

    # Creation date between 1-5 years ago
    created = now - timedelta(days=random.randint(365, 365 * 5))

    # For inactive identities, compute when they became inactive
    inactive = random.random() < 0.15  # 15% chance of being inactive

    if inactive:
        # Inactive date is between creation and now, weighted toward recent
        time_since_creation = (now - created).total_seconds()
        # 70% of inactive dates in last 30% of identity lifetime
        if random.random() < 0.7:
            random_seconds = int(time_since_creation * 0.7) + random.randint(0, int(time_since_creation * 0.3))
        else:
            random_seconds = random.randint(0, int(time_since_creation))
        modified = created + timedelta(seconds=random_seconds)
    else:
        # Last modified between creation and now
        time_since_creation = (now - created).total_seconds()
        random_seconds = random.randint(0, int(time_since_creation))
        modified = created + timedelta(seconds=random_seconds)

    # Last sync time between last modification and now
    time_since_modified = (now - modified).total_seconds()
    if time_since_modified > 0:
        random_seconds = random.randint(0, int(time_since_modified))
        synced = modified + timedelta(seconds=random_seconds)
    else:
        synced = modified

    # 10% chance of identity being a fallback approver
    is_fallback_approver = random.random() < 0.1

    # Determine environment based on profile or random selection
    environment_options = ["production", "preproduction", "qa", "development"]
    if profile_info and profile_info.get('environment'):
        environment = profile_info.get('environment')
    else:
        # Weight production less heavily for service accounts
        if is_service_account:
            environment_weights = [0.3, 0.2, 0.2, 0.3]  # More evenly distributed
        else:
            environment_weights = [0.6, 0.2, 0.1, 0.1]  # Production heavily weighted

        environment = random.choices(
            environment_options,
            weights=environment_weights,
            k=1
        )[0]

    # Generate status
    statuses = [
        ("active", 0.7),
        ("pending", 0.1),
        ("provisioning", 0.05),
        ("deprovisioning", 0.05),
        ("suspended", 0.05),
        ("error", 0.05),
    ]

    if inactive:
        # Override: inactive identities have more restricted status options
        statuses = [
            ("inactive", 0.8),
            ("suspended", 0.1),
            ("deprovisioned", 0.1),
        ]

    status = random.choices(
        [s for s, _ in statuses],
        weights=[w for _, w in statuses],
        k=1
    )[0]

    # Construct the identity record (without ID fields)
    identity = {
        "name": internal_name,
        "display_name": display_name,
        "service_account": is_service_account,
        "environment": environment,
        "created": created.isoformat(),
        "inactive": inactive,
        "status": status,
        "modified": modified.isoformat(),
        "synced": synced.isoformat(),
        "is_fallback_approver": is_fallback_approver
    }

    return identity


def _fetch_owner_info(owner_id: Any, dg: DataGenerator) -> Dict[str, Any]:
    """
    Fetch owner information from the database

    Args:
        owner_id: Integer ID of the owner (enterprise associate)
        dg: DataGenerator instance

    Returns:
        Dictionary with owner information, or empty dict if not found
    """
    if not owner_id:
        return {}

    try:
        # Try to query the owner information
        query = """
        SELECT first_name, last_name, email, job_title
        FROM enterprise.associates
        WHERE enterprise_associate_id = %s
        """

        with dg.conn.cursor() as cursor:
            cursor.execute(query, (owner_id,))
            result = cursor.fetchone()

        return result

    except Exception as e:
        logger.error(e)
        # Handle connection errors or other issues
        pass

    return {}


def _fetch_profile_info(profile_id: Any, dg: DataGenerator) -> Dict[str, Any]:
    """
    Fetch identity profile information from the database

    Args:
        profile_id: UUID of the identity profile
        dg: DataGenerator instance

    Returns:
        Dictionary with profile information, or empty dict if not found
    """
    if not profile_id:
        return {}

    try:
        # Try to query the profile information
        query = """
        SELECT name, description, risk_level
        FROM security.identity_profiles
        WHERE security_identity_profile_id = %s
        """

        with dg.conn.cursor() as cursor:
            cursor.execute(query, (profile_id,))
            result = cursor.fetchone()

        return result

    except Exception as e:
        # Handle connection errors or other issues
        logger.error(e)
        pass

    return {}
