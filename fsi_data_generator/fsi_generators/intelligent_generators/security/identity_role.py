from data_generator import DataGenerator, SkipRowGenerationError
from datetime import datetime, timedelta
from typing import Any, Dict, Set, Tuple

import logging
import random

# Track active role assignments to prevent duplicates
active_role_assignments: Set[Tuple[str, str]] = set()
logger = logging.getLogger(__name__)


def generate_random_identity_role(id_fields: Dict[str, Any], _dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random security.identity_roles record.

    Args:
        id_fields: Dictionary containing predetermined ID fields
                  (security_identity_role_id, security_identity_id, security_role_id, assigned_by_id)
        _dg: DataGenerator instance

    Returns:
        Dict containing a random identity role record
        (without ID fields)
    """
    security_identity_id = id_fields.get("security_identity_id")
    security_role_id = id_fields.get("security_role_id")

    if not security_identity_id or not security_role_id:
        raise ValueError("Both security_identity_id and security_role_id are required")

    # Generate start date (within the last 2 years)
    now = datetime.now()
    start_date = now - timedelta(days=random.randint(1, 730))

    # Determine if this assignment will have an end date
    has_end_date = random.random() < 0.25  # 25% chance of having an end date

    # Generate an end date for assignments that are no longer active
    end_date = None
    is_active = not has_end_date  # active if and only if there's no end date

    if has_end_date:
        # End date should be after start date but before now
        min_days = 30  # At least 30 days after start
        max_days = (now - start_date).days - 1

        # Ensure we have a valid range for random selection
        if max_days > min_days:
            days_after_start = random.randint(min_days, max_days)
            end_date = (start_date + timedelta(days=days_after_start)).isoformat()
        else:
            # If the start date is too recent, set end_date to None and keep active
            end_date = None
            is_active = True

    # Check for duplicate active role assignments
    if is_active:
        identity_role_pair = (str(security_identity_id), str(security_role_id))
        if identity_role_pair in active_role_assignments:
            # Skip this record - this identity already has this role actively assigned
            raise SkipRowGenerationError("Duplicate active role assignment")

        # Track this active assignment
        active_role_assignments.add(identity_role_pair)

    # Construct the identity role record
    identity_role = {
        "start_date": start_date.isoformat(),
        "end_date": end_date,
        "active": is_active
    }

    return identity_role
