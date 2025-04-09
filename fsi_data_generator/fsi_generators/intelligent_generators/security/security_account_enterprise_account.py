from data_generator import DataGenerator, SkipRowGenerationError
from datetime import datetime, timedelta
from faker import Faker
from typing import Any, Dict
import random

prev_account_assignments = set()

def generate_random_security_account_enterprise_account(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random security.security_account_enterprise_accounts record.

    Args:
        id_fields: Dictionary containing predetermined ID fields (auto-generated, included for reference)
        dg: DataGenerator instance

    Returns:
        Dict containing randomly generated security account enterprise account linkage data
        (without ID fields)
    """
    fake = Faker()

    # Define possible access levels
    access_levels = [
        "READ",
        "WRITE",
        "ADMIN",
        "EXECUTE"
    ]

    # Weighted selection for more common permissions
    access_level_weights = [0.6, 0.2, 0.15, 0.05]
    access_level = random.choices(access_levels, weights=access_level_weights, k=1)[0]

    # Assigned_at timestamp within the last year
    assigned_at = datetime.now() - timedelta(days=random.randint(0, 365),
                                             hours=random.randint(0, 23),
                                             minutes=random.randint(0, 59),
                                             seconds=random.randint(0, 59))

    # Active flag mostly true (90%)
    active = random.random() < 0.9

    # Check for duplicates
    key = (id_fields.get('security_account_id'), id_fields.get('enterprise_account_id'), access_level)
    if key in prev_account_assignments:
        raise SkipRowGenerationError

    prev_account_assignments.add(key)

    # Create the account-enterprise account linkage record
    security_account_enterprise_account = {
        "access_level": access_level,
        "assigned_at": assigned_at,
        "active": active
    }

    return security_account_enterprise_account
