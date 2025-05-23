from data_generator import DataGenerator, SkipRowGenerationError
from datetime import datetime, timedelta
from typing import Any, Dict, Set, Tuple

import logging
import random

# Track active role assignments to prevent duplicates
active_role_assignments: Set[Tuple[str, str]] = set()
logger = logging.getLogger(__name__)


def generate_random_identity_role(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random security.identity_roles record.

    Args:
        id_fields: Dictionary containing predetermined ID fields
                  (security_identity_role_id, security_identity_id, security_role_id, assigned_by_id)
        dg: DataGenerator instance

    Returns:
        Dict containing a random identity role record
        (without ID fields)
    """
    security_identity_id = id_fields.get("security_identity_id")

    if not security_identity_id:
        raise ValueError("security_identity_id is required")

    # Find the associate related to this identity
    try:
        identity_query = """
        SELECT owner_id FROM security.identities WHERE security_identity_id = %s
        """
        with dg.conn.cursor() as cursor:
            cursor.execute(identity_query, (security_identity_id,))
            identity_result = cursor.fetchone()

        if not identity_result:
            raise SkipRowGenerationError("Could not find identity information")

        associate_id = identity_result.get("owner_id")

        if not associate_id:
            raise SkipRowGenerationError("Identity does not have an owner")

        # Find department of this associate
        department_query = """
        SELECT enterprise_department_id FROM enterprise.associates WHERE enterprise_associate_id = %s
        """
        with dg.conn.cursor() as cursor:
            cursor.execute(department_query, (associate_id,))
            department_result = cursor.fetchone()

        if not department_result:
            raise SkipRowGenerationError("Could not find associate's department")

        department_id = department_result.get("enterprise_department_id")

        # Find all roles managed by applications in the same department directly
        role_query = """
        SELECT r.security_role_id 
        FROM security.roles r
        JOIN app_mgmt.applications a ON r.managing_application_id = a.app_mgmt_application_id  
        WHERE a.enterprise_department_id = %s
        AND r.status = 'ACTIVE'
        """
        with dg.conn.cursor() as cursor:
            cursor.execute(role_query, (department_id,))
            role_results = cursor.fetchall()

        logger.debug(f"Found {len(role_results)} roles for department {department_id}")

        if not role_results:
            # If no roles found, try without the department filter as a fallback
            broader_role_query = """
            SELECT security_role_id FROM security.roles WHERE status = 'ACTIVE' LIMIT 100
            """
            with dg.conn.cursor() as cursor:
                cursor.execute(broader_role_query)
                role_results = cursor.fetchall()

            logger.debug(f"Fallback: Found {len(role_results)} active roles across all departments")

            if not role_results:
                raise SkipRowGenerationError("No active roles found in the system")

        # Randomly select a role
        selected_role = random.choice(role_results)
        security_role_id = selected_role.get("security_role_id")

    except Exception as e:
        logger.error(f"Error finding role for identity: {e}")
        raise SkipRowGenerationError(f"Error finding role: {e}")

    # Check for duplicate active role assignments
    identity_role_pair = (str(security_identity_id), str(security_role_id))
    if identity_role_pair in active_role_assignments:
        # Skip this record - this identity already has this role actively assigned
        raise SkipRowGenerationError("Duplicate active role assignment")

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

    # Track this active assignment if it's active
    if is_active:
        active_role_assignments.add(identity_role_pair)

    # Override the security_role_id in id_fields with our derived one
    id_fields["security_role_id"] = security_role_id

    # Construct the identity role record
    identity_role = {
        "start_date": start_date.isoformat(),
        "end_date": end_date,
        "active": is_active
    }

    return identity_role
