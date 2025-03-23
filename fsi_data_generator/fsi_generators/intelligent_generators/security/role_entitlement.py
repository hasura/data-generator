import logging
import random
from datetime import datetime, timedelta
from typing import Any, Dict, Set, Tuple

from data_generator import DataGenerator, SkipRowGenerationError

# Track active role-entitlement pairs to prevent duplicates
active_role_entitlement_pairs: Set[Tuple[str, str]] = set()
logger = logging.getLogger(__name__)


def generate_random_role_entitlement(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random security.role_entitlements record.

    Args:
        id_fields: Dictionary containing predetermined ID fields
                  (security_role_entitlement_id, security_role_id, security_entitlement_id, created_by_id, updated_by_id)
        dg: DataGenerator instance

    Returns:
        Dict containing a random role entitlement record
        (without ID fields)
    """
    # Extract required ID fields
    security_role_id = id_fields.get('security_role_id')
    security_entitlement_id = id_fields.get('security_entitlement_id')

    if not security_role_id or not security_entitlement_id:
        raise ValueError("Both security_role_id and security_entitlement_id are required")

    # Get current timestamp to ensure no future dates
    now = datetime.now()

    # Generate created_at timestamp (between 1 day and 2 years ago)
    created_at = now - timedelta(days=random.randint(1, 730))

    # Generate started_at timestamp (can be same as created_at or later, but not future)
    # 80% chance of starting immediately, 20% chance of delayed start
    if random.random() < 0.8:
        started_at = created_at
    else:
        # Start between creation and now, but at least 1 day after creation
        max_delay = min(90, (now - created_at).days - 1)  # Maximum 90 days delay, but not future
        if max_delay > 0:
            delay_days = random.randint(1, max_delay)
            started_at = created_at + timedelta(days=delay_days)
        else:
            # If max_delay is not positive, use created_at
            started_at = created_at

    # Determine if this entitlement has ended
    has_ended = random.random() < 0.15  # 15% chance of being ended

    # Generate ended_at timestamp if applicable (between started_at and now)
    ended_at = None
    if has_ended:
        # End between start date and now, but at least 1 day after start
        min_duration = 1  # At least 1 day active
        max_duration = (now - started_at).days - 1

        if max_duration >= min_duration:
            duration_days = random.randint(min_duration, max_duration)
            ended_at = started_at + timedelta(days=duration_days)

    # Set active status correctly based on ended_at
    active = ended_at is None

    # Check for duplicate active role-entitlement pairs
    if active:
        role_entitlement_pair = (str(security_role_id), str(security_entitlement_id))
        if role_entitlement_pair in active_role_entitlement_pairs:
            # Skip this record - this role-entitlement pair is already active
            raise SkipRowGenerationError("Duplicate active role-entitlement pair")

        # Track this active pair
        active_role_entitlement_pairs.add(role_entitlement_pair)

    # Construct the role entitlement record
    role_entitlement = {
        "created_at": created_at.isoformat(),
        "started_at": started_at.isoformat(),
        "ended_at": ended_at.isoformat() if ended_at else None,
        "active": active
    }

    return role_entitlement
