from data_generator import DataGenerator, SkipRowGenerationError
from faker import Faker
from fsi_data_generator.fsi_generators.helpers.generate_unique_json_array import \
    generate_unique_json_array
from typing import Any, Dict

import anthropic
import logging
import psycopg2
import random
import sys

prev_policy_attributes = set()
logger = logging.getLogger(__name__)


def generate_random_policy_attribute(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random security.policy_attributes record.

    Args:
        id_fields: Dictionary containing predetermined ID fields
                  (security_policy_id)
        dg: DataGenerator instance

    Returns:
        Dict containing a random policy attribute record
        (without ID fields)
    """
    fake = Faker()

    # Try to fetch the related policy information
    policy_info = _fetch_policy_info(id_fields.get('security_policy_id'), dg)

    # Common attribute names for security policies, categorized by policy type
    attribute_categories = {
        "authentication": [
            "max_authentication_attempts",
            "password_expiry_days",
            "minimum_password_length",
            "require_special_characters",
            "mfa_required",
            "password_history_count",
            "lockout_duration_minutes"
        ],
        "session": [
            "session_timeout_minutes",
            "idle_timeout_minutes",
            "concurrent_sessions_allowed",
            "session_persistence_enabled",
            "session_encryption_required"
        ],
        "access": [
            "allowed_ip_range",
            "access_window_start",
            "access_window_end",
            "require_approval",
            "allow_remote_access",
            "geographic_restrictions",
            "device_restrictions",
            "max_daily_access_hours"
        ],
        "encryption": [
            "encryption_algorithm",
            "key_rotation_days",
            "encryption_key_length",
            "hash_algorithm",
            "tls_version_minimum"
        ],
        "audit": [
            "audit_level",
            "log_retention_days",
            "notification_email",
            "review_frequency_days",
            "alert_threshold",
            "real_time_monitoring"
        ],
        "compliance": [
            "gdpr_compliance_required",
            "hipaa_compliance_required",
            "pci_dss_compliance_required",
            "sox_compliance_required",
            "data_residency_requirement"
        ]
    }

    # Select attribute based on policy name/description if available
    if policy_info and policy_info.get('name'):
        policy_name = policy_info.get('name', '').lower()
        policy_description = policy_info.get('description', '').lower()

        # Determine most relevant category based on policy info
        category_score = {}
        for category, _ in attribute_categories.items():
            category_score[category] = 0
            if category in policy_name or category in policy_description:
                category_score[category] += 5

            # Additional keywords to match
            keywords = {
                "authentication": ["login", "password", "credential", "identity", "auth"],
                "session": ["session", "timeout", "idle", "connection"],
                "access": ["access", "permission", "restriction", "allowed", "remote"],
                "encryption": ["encrypt", "crypt", "secure", "key", "hash", "tls", "ssl"],
                "audit": ["audit", "log", "monitor", "alert", "review", "notification"],
                "compliance": ["compliance", "regulation", "gdpr", "hipaa", "pci", "sox", "legal"]
            }

            for keyword in keywords.get(category, []):
                if keyword in policy_name:
                    category_score[category] += 3
                if keyword in policy_description:
                    category_score[category] += 2

        # Select category with the highest score, or random if tied
        top_categories = [k for k, v in category_score.items()
                          if v == max(category_score.values())]
        selected_category = random.choice(top_categories if top_categories else list(attribute_categories.keys()))
    else:
        # Fallback to random category if no policy info
        selected_category = random.choice(list(attribute_categories.keys()))

    # Get attributes for the selected category
    attribute_options = attribute_categories[selected_category]

    # Try to get unique attribute names from DBML if available
    try:
        all_attributes = generate_unique_json_array(
            dbml_string=dg.dbml,
            fully_qualified_column_name='security.policy_attributes.attribute_name',
            count=50,
            cache_key='policy_attribute_names'
        )
        # Filter by category keywords if possible
        category_keywords = selected_category.split('_')
        filtered_attributes = [attr for attr in all_attributes
                               if any(keyword in attr for keyword in category_keywords)]
        if filtered_attributes:
            attribute_options = filtered_attributes
    except anthropic.APIStatusError:
        # Already using fallback attribute list
        pass

    # Select a random attribute name
    attribute_name = random.choice(attribute_options)

    # Generate appropriate value based on attribute name
    if "days" in attribute_name:
        attribute_value = str(random.randint(30, 365))
    elif "minutes" in attribute_name:
        attribute_value = str(random.randint(5, 120))
    elif "length" in attribute_name:
        attribute_value = str(random.randint(8, 16))
    elif "count" in attribute_name:
        attribute_value = str(random.randint(3, 24))
    elif "attempts" in attribute_name:
        attribute_value = str(random.randint(3, 10))
    elif "hours" in attribute_name:
        attribute_value = str(random.randint(1, 24))
    elif any(word in attribute_name for word in ["required", "enabled", "allowed"]):
        attribute_value = random.choice(["true", "false"])
    elif "email" in attribute_name:
        attribute_value = fake.email()
    elif "ip_range" in attribute_name:
        attribute_value = f"{fake.ipv4_network_class()}/24"
    elif "algorithm" in attribute_name:
        if "hash" in attribute_name:
            attribute_value = random.choice(["SHA-256", "SHA-512", "bcrypt", "Argon2id"])
        else:
            attribute_value = random.choice(["AES-256", "RSA-2048", "ChaCha20-Poly1305"])
    elif "version" in attribute_name:
        attribute_value = random.choice(["1.2", "1.3"])
    elif "level" in attribute_name:
        attribute_value = random.choice(["low", "medium", "high", "detailed", "comprehensive"])
    elif "window" in attribute_name:
        if "start" in attribute_name:
            attribute_value = f"{random.randint(6, 9)}:00"
        else:
            attribute_value = f"{random.randint(17, 23)}:00"
    elif "threshold" in attribute_name:
        attribute_value = str(random.randint(3, 20))
    elif "restrictions" in attribute_name:
        if "geographic" in attribute_name:
            attribute_value = random.choice(["US-only", "EU-only", "global", "restricted-countries"])
        else:
            attribute_value = random.choice(["managed-only", "approved-list", "block-mobile", "any"])
    elif "workflow" in attribute_name:
        attribute_value = fake.uuid4()
    elif "approval" in attribute_name and "workflow" not in attribute_name:
        attribute_value = random.choice(["required", "optional", "risk-based"])
    elif "access" in attribute_name:
        attribute_value = random.choice(["allowed", "prohibited", "by-approval", "limited"])
    elif "residency" in attribute_name:
        attribute_value = random.choice(["EU", "US", "local-only", "specified-regions"])
    elif "compliance" in attribute_name:
        attribute_value = random.choice(["true", "false", "partial"])
    else:
        # Default case
        attribute_value = fake.word()

    # Construct the policy attribute record (without ID fields)
    policy_attribute = {
        "attribute_name": attribute_name,
        "attribute_value": attribute_value
    }

    global prev_policy_attributes
    check = (id_fields.get('security_policy_id'), policy_attribute.get('attribute_name'))
    if check in prev_policy_attributes:
        raise SkipRowGenerationError
    else:
        prev_policy_attributes.add(check)

    return policy_attribute


def _fetch_policy_info(policy_id: Any, dg: DataGenerator) -> Dict[str, Any]:
    """
    Fetch policy information from the database

    Args:
        policy_id: UUID of the policy
        dg: DataGenerator instance

    Returns:
        Dictionary with policy name and description, or empty dict if not found
    """
    if not policy_id:
        return {}

    try:
        # Try to query the policy information
        query = """
        SELECT name, description 
        FROM security.policies 
        WHERE security_policy_id = %s
        """

        with dg.conn.cursor() as cursor:
            cursor.execute(query, (policy_id,))
            result = cursor.fetchone()

        return result

    except psycopg2.ProgrammingError as e:
        # Log the critical error
        logger.critical(f"Programming error detected in the SQL query: {e}")

        # Exit the program immediately with a non-zero status code
        sys.exit(1)
