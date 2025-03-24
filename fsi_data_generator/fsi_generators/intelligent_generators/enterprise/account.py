import logging
import random
from datetime import datetime, timedelta
from typing import Any, Dict, Set

import anthropic

from data_generator import DataGenerator
from fsi_data_generator.fsi_generators.helpers.generate_unique_json_array import \
    generate_unique_json_array

from .enums import AccountStatus

# Track previously generated account descriptions for uniqueness if needed
prev_account_descriptions: Set[str] = set()
logger = logging.getLogger(__name__)


def generate_random_account(_id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random "enterprise.accounts" record.

    Args:
        _id_fields: Dictionary containing predetermined ID fields
                  (enterprise_account_id)
        dg: DataGenerator instance

    Returns:
        Dict containing a random account record
        (without ID fields)
    """

    # Generate opened_date (between 10 years ago and yesterday)
    now = datetime.now()
    max_age_days = 365 * 10  # 10 years
    opened_date = now - timedelta(days=random.randint(1, max_age_days))

    # Determine account status - weighted random
    status = AccountStatus.get_random()

    # Generate status_update_date_time (between opened_date and now)
    days_since_opened = (now - opened_date).days
    update_delay_days = min(days_since_opened, random.randint(0, 365 * 2))  # Max 2 years or account age
    status_update_date_time = opened_date + timedelta(days=update_delay_days)

    # If status is CLOSED, adjust status_update_date_time to be within last year
    # since closed accounts are less likely to have very old status updates
    if status == AccountStatus.CLOSED and days_since_opened > 365:
        days_ago = random.randint(1, 365)
        status_update_date_time = now - timedelta(days=days_ago)

    # Generate account_category - higher level designations
    categories = [
        "personal",  # For individual customers
        "business",  # For commercial customers
        "non-profit",  # For non-profit organizations
        "government",  # For government entities
        "trust",  # For trust accounts
        "institutional",  # For institutional clients
        "corporate",  # For large corporate entities
        "partnership",  # For business partnerships
        "education",  # For educational institutions
        "retirement",  # For retirement-focused accounts
        "estate"  # For estate accounts
    ]

    # Try to get additional categories from DBML if available
    try:
        additional_categories = generate_unique_json_array(
            dbml_string=dg.dbml,
            fully_qualified_column_name='enterprise.accounts.account_category',
            count=10,
            cache_key='account_categories'
        )
        categories.extend(additional_categories)
    except (anthropic.APIStatusError, Exception):
        pass

    account_category = random.choice(categories)

    # Generate description - more meaningful for the higher-level categories
    descriptions = []

    if account_category == "personal":
        descriptions = [
            "Primary Banking",
            "Family Banking",
            "Wealth Management",
            "Investment Focus",
            "Everyday Banking"
        ]
    elif account_category == "business":
        descriptions = [
            "Small Business",
            "Startup Operations",
            "Business Growth",
            "Commercial Banking",
            "Merchant Services"
        ]
    elif account_category == "non-profit":
        descriptions = [
            "Charitable Foundation",
            "Community Organization",
            "Religious Institution",
            "Educational Foundation",
            "Humanitarian Group"
        ]
    elif account_category == "government":
        descriptions = [
            "Municipal Services",
            "Agency Operations",
            "Public Works",
            "Legislative Branch",
            "Executive Department"
        ]
    elif account_category == "trust":
        descriptions = [
            "Family Trust",
            "Living Trust",
            "Revocable Trust",
            "Asset Protection",
            "Generation Skipping"
        ]
    elif account_category == "institutional":
        descriptions = [
            "Investment Institution",
            "Financial Services",
            "Fund Management",
            "Endowment",
            "Pension Management"
        ]
    elif account_category == "corporate":
        descriptions = [
            "Enterprise Operations",
            "Corporate Treasury",
            "Global Banking",
            "Multinational Accounts",
            "Corporate Investments"
        ]
    elif account_category == "partnership":
        descriptions = [
            "Professional Partnership",
            "Limited Partnership",
            "General Partnership",
            "Joint Venture",
            "Strategic Alliance"
        ]
    elif account_category == "education":
        descriptions = [
            "University Accounts",
            "School District",
            "Private Academy",
            "Research Institution",
            "Educational Endowment"
        ]
    elif account_category == "retirement":
        descriptions = [
            "Retirement Planning",
            "Senior Services",
            "Retirement Benefits",
            "Post-Career Planning",
            "Legacy Management"
        ]
    elif account_category == "estate":
        descriptions = [
            "Estate Management",
            "Posthumous Affairs",
            "Legacy Planning",
            "Executor Services",
            "Beneficiary Management"
        ]
    else:
        # Fallback generic descriptions
        descriptions = [
            f"{account_category.capitalize()} Banking",
            f"{account_category.capitalize()} Services",
            f"{account_category.capitalize()} Management",
            f"Primary {account_category.capitalize()}",
            f"{account_category.capitalize()} Operations"
        ]

    description = random.choice(descriptions)

    # Try to make description unique if we're tracking that
    if len(prev_account_descriptions) > 0:
        for _ in range(5):  # Try up to 5 times
            if description not in prev_account_descriptions:
                prev_account_descriptions.add(description)
                break
            description = random.choice(descriptions)

    # Construct the account record
    account = {
        "opened_date": opened_date.isoformat(),
        "status": status,
        "status_update_date_time": status_update_date_time.isoformat(),
        "account_category": account_category,
        "description": description
    }

    return account
