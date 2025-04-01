from data_generator import DataGenerator, SkipRowGenerationError
from faker import Faker
from fsi_data_generator.fsi_generators.helpers.generate_unique_json_array import \
    generate_unique_json_array
from typing import Any, Dict

import anthropic
import logging
import random

# Track previously generated governance group names for uniqueness
prev_governance_group_names = set()
logger = logging.getLogger(__name__)


def generate_random_governance_group(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random security.governance_groups record.

    Args:
        id_fields: Dictionary containing predetermined ID fields
                  (security_governance_group_id, owner_id)
        dg: DataGenerator instance

    Returns:
        Dict containing a random governance group record
        (without ID fields)
    """
    fake = Faker()

    # Try to fetch the related owner information if possible
    owner_info = _fetch_owner_info(id_fields.get('owner_id'), dg)

    # Base group names - now includes finance-focused groups
    group_names = [
        # Security groups
        "Security Administration",
        "User Access Management",
        "Network Security",
        "Application Security",
        "Cloud Security",
        "Data Protection",
        "Identity Management",
        "Compliance",
        "Incident Response",
        "Risk Management",
        "Disaster Recovery",
        "Vendor Security",
        "Audit",
        "Physical Security",
        "Endpoint Security",
        "Executive Security Council",
        "IT Operations",
        "Database Security",
        "Development Security",
        "API Security",

        # Finance groups
        "Financial Risk Committee",
        "Capital Planning Committee",
        "Asset Liability Committee",
        "Investment Review Board",
        "Credit Risk Committee",
        "Treasury Management",
        "Liquidity Risk Oversight",
        "Financial Controls Committee",
        "Model Risk Governance",
        "Financial Reporting Oversight",
        "Regulatory Compliance Committee",
        "Trading Risk Committee",
        "Fraud Prevention Council",
        "Financial Technology Governance",
        "Executive Finance Committee",
        "Operational Risk Management",
        "Transaction Monitoring Committee",
        "Market Risk Oversight",
        "Financial Crime Prevention",
        "ESG Investment Committee"
    ]

    try:
        group_names = group_names + generate_unique_json_array(
            dbml_string=dg.dbml,
            fully_qualified_column_name='security.governance_groups.name',
            count=20,
            cache_key='governance_group_names'
        )
    except anthropic.APIStatusError:
        pass

    # Generate a governance group name
    if owner_info and 'job_title' in owner_info and owner_info['job_title']:
        # If we have owner job title, try to create a relevant group name
        job_title = owner_info['job_title'].lower()

        if any(keyword in job_title for keyword in ['security', 'risk', 'compliance']):
            domain = random.choice(["Security", "Risk", "Compliance", "Governance"])
            action = random.choice(["Management", "Review", "Oversight", "Control"])
            group_name = f"{domain} {action} Group"

        elif any(keyword in job_title for keyword in ['finance', 'financial', 'treasury', 'accounting']):
            domain = random.choice(["Financial", "Treasury", "Fiscal", "Accounting", "Finance"])
            action = random.choice(["Governance", "Review", "Oversight", "Strategy", "Control"])
            group_name = f"{domain} {action} Committee"

        elif any(keyword in job_title for keyword in ['invest', 'portfolio', 'asset', 'wealth']):
            domain = random.choice(["Investment", "Portfolio", "Asset", "Wealth"])
            action = random.choice(["Management", "Strategy", "Allocation", "Advisory"])
            group_name = f"{domain} {action} Committee"

        elif any(keyword in job_title for keyword in ['credit', 'loan', 'lending', 'underwriting']):
            domain = random.choice(["Credit", "Lending", "Loan", "Underwriting"])
            action = random.choice(["Risk", "Policy", "Review", "Oversight"])
            group_name = f"{domain} {action} Council"

        elif any(keyword in job_title for keyword in ['trade', 'trading', 'market', 'capital']):
            domain = random.choice(["Trading", "Market", "Capital", "Liquidity"])
            action = random.choice(["Risk", "Strategy", "Oversight", "Management"])
            group_name = f"{domain} {action} Committee"

        elif any(keyword in job_title for keyword in ['develop', 'engineer', 'architect']):
            domain = random.choice(["Application", "Development", "Code", "Software", "System"])
            action = random.choice(["Security", "Review", "Governance", "Approval"])
            group_name = f"{domain} {action} Committee"

        elif any(keyword in job_title for keyword in ['data', 'analytics', 'database']):
            domain = random.choice(["Data", "Information", "Database"])
            action = random.choice(["Protection", "Governance", "Security", "Privacy"])
            group_name = f"{domain} {action} Council"

        elif any(keyword in job_title for keyword in ['network', 'infrastructure', 'cloud']):
            domain = random.choice(["Network", "Infrastructure", "Cloud"])
            action = random.choice(["Security", "Management", "Oversight"])
            group_name = f"{domain} {action} Team"

        else:
            # Fallback to predefined names if job title doesn't match known patterns
            group_name = random.choice(group_names)
    else:
        # Use predefined names
        group_name = random.choice(group_names)

    # Ensure name uniqueness
    global prev_governance_group_names
    retries = 0
    base_name = group_name
    while group_name in prev_governance_group_names and retries < 5:
        # Append random qualifier to ensure uniqueness
        qualifier = random.choice([
            fake.word().title(),
            f"Level {random.randint(1, 3)}",
            f"Tier {random.randint(1, 3)}",
            random.choice(["Global", "Regional", "Enterprise", "Corporate", "Departmental"])
        ])
        group_name = f"{base_name} - {qualifier}"
        retries += 1

    if group_name in prev_governance_group_names:
        raise SkipRowGenerationError
    else:
        prev_governance_group_names.add(group_name)

    # Construct the governance group record (without ID fields)
    governance_group = {
        "name": group_name,
        "description": _generate_group_description(group_name)
    }

    return governance_group


def _generate_group_description(group_name: str) -> str:
    """
    Generate a description for the governance group based on its name.

    Args:
        group_name: The name of the governance group

    Returns:
        A relevant description for the governance group
    """
    name_lower = group_name.lower()

    # Finance related descriptions
    if any(term in name_lower for term in ['financial', 'finance', 'treasury', 'accounting']):
        return f"Responsible for overseeing financial governance, controls, and reporting standards across the organization."

    elif any(term in name_lower for term in ['investment', 'portfolio', 'asset']):
        return f"Oversees investment strategies, portfolio performance, and ensures alignment with organizational risk appetite."

    elif any(term in name_lower for term in ['credit', 'loan', 'lending']):
        return f"Reviews and approves credit policies, major lending activities, and monitors credit risk exposure."

    elif any(term in name_lower for term in ['trading', 'market', 'capital']):
        return f"Monitors trading activities, market risk exposure, and ensures compliance with capital requirements."

    # Security related descriptions
    elif any(term in name_lower for term in ['security', 'risk', 'compliance']):
        return f"Oversees the development and implementation of security policies, risk management protocols, and compliance requirements."

    elif any(term in name_lower for term in ['data', 'information']):
        return f"Ensures proper management and protection of organization's data assets and information systems."

    else:
        return f"Provides governance, oversight, and strategic direction related to {group_name}."


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
