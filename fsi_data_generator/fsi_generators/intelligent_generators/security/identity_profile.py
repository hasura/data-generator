from data_generator import DataGenerator, SkipRowGenerationError
from datetime import datetime, timedelta
from faker import Faker
from fsi_data_generator.fsi_generators.helpers.generate_unique_json_array import \
    generate_unique_json_array
from typing import Any, Dict

import anthropic
import random

# Track previously generated profile names for uniqueness
prev_profile_names = set()


def generate_random_identity_profile(_id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random security.identity_profiles record.

    Args:
        _id_fields: Dictionary containing predetermined ID fields
                  (security_identity_profile_id)
        dg: DataGenerator instance

    Returns:
        Dict containing a random identity profile record
        (without ID fields)
    """
    fake = Faker()

    # Try to get profile names from DBML if available
    profile_names = [
        "Standard User",
        "Privileged Admin",
        "Service Account",
        "External Contractor",
        "Executive",
        "System Admin",
        "Database Admin",
        "Network Admin",
        "Help Desk",
        "Developer",
        "Auditor",
        "Temporary Access",
        "Vendor Access",
        "Cloud Admin",
        "Application Owner",
        "Emergency Access",
        "Read-Only User",
        "API Access",
        "Report Generator",
        "Customer Service"
    ]
    try:
        profile_names = profile_names + generate_unique_json_array(
            dbml_string=dg.dbml,
            fully_qualified_column_name='security.identity_profiles.name',
            count=20,
            cache_key='identity_profile_names'
        )
    except anthropic.APIStatusError:
        pass

    # Generate a profile name
    if profile_names:
        # Use existing profile name with a random descriptor
        profile_name = random.choice(profile_names)
    else:
        # Generate a random profile name from components
        adjectives = ["Standard", "Enhanced", "Restricted", "Enterprise", "Secure", "Limited", "Advanced"]
        roles = ["User", "Admin", "Service", "Manager", "Analyst", "Developer", "Operator"]
        profile_name = f"{random.choice(adjectives)} {random.choice(roles)}"

    # Ensure name uniqueness
    global prev_profile_names
    retries = 0
    base_name = profile_name
    while profile_name in prev_profile_names and retries < 5:
        # Append random qualifier to ensure uniqueness
        profile_name = f"{base_name} - {fake.word().title()}"
        retries += 1

    if profile_name in prev_profile_names:
        raise SkipRowGenerationError
    else:
        prev_profile_names.add(profile_name)

    # Generate a meaningful description based on the profile name
    lower_name = profile_name.lower()

    # Description components based on profile type
    if "admin" in lower_name:
        access_level = "administrative access"
        purposes = ["system configuration", "user management", "security operations"]
        access_scope = "elevated privileges"
        review_frequency = random.randint(30, 90)  # More frequent reviews for admin accounts
    elif "service" in lower_name:
        access_level = "automated system access"
        purposes = ["data processing", "system integration", "scheduled operations"]
        access_scope = "specific service functions"
        review_frequency = random.randint(60, 180)  # Medium frequency for service accounts
    elif "executive" in lower_name or "manager" in lower_name:
        access_level = "management-level access"
        purposes = ["oversight functions", "approval workflows", "business reporting"]
        access_scope = "sensitive business data"
        review_frequency = random.randint(90, 180)  # Medium-long frequency
    elif "temporary" in lower_name or "emergency" in lower_name:
        access_level = "time-limited access"
        purposes = ["emergency response", "temporary project work", "incident handling"]
        access_scope = "specific critical systems"
        review_frequency = random.randint(7, 30)  # Very frequent reviews
    elif "read" in lower_name:
        access_level = "read-only access"
        purposes = ["data analysis", "report generation", "monitoring"]
        access_scope = "view-only capabilities"
        review_frequency = random.randint(90, 365)  # Less frequent reviews
    else:
        access_level = "standard user access"
        purposes = ["daily operations", "business functions", "routine tasks"]
        access_scope = "standard business applications"
        review_frequency = random.randint(90, 365)  # Standard review cycle

    # Construct description
    description = f"Profile for {access_level} to support {random.choice(purposes)}. "
    description += f"Provides {access_scope} with appropriate security controls. "
    description += f"Requires review every {review_frequency} days."

    # Generate security settings based on profile type
    # Determine MFA requirements
    requires_mfa = True
    if "service" in lower_name:
        # Service accounts often exempted from MFA
        requires_mfa = random.random() < 0.3
    elif "admin" in lower_name or "privileged" in lower_name:
        # Admin accounts almost always require MFA
        requires_mfa = random.random() < 0.95
    elif "standard" in lower_name or "user" in lower_name:
        # Standard users typically require MFA
        requires_mfa = random.random() < 0.8

    # Password expiry based on profile type
    if "admin" in lower_name or "privileged" in lower_name:
        password_expiry_days = random.randint(30, 90)  # Shorter for admins
    elif "service" in lower_name:
        password_expiry_days = random.randint(180, 365)  # Longer for service accounts
    elif "temporary" in lower_name:
        password_expiry_days = random.randint(1, 30)  # Very short for temp access
    else:
        password_expiry_days = random.randint(60, 180)  # Standard for regular users

    # Session timeout based on profile security needs
    if "admin" in lower_name or "privileged" in lower_name:
        # Shorter sessions for privileged accounts
        default_session_timeout_minutes = random.randint(15, 60)
    elif "service" in lower_name:
        # Longer sessions for service accounts
        default_session_timeout_minutes = random.randint(240, 1440)
    else:
        # Standard timeout for regular users
        default_session_timeout_minutes = random.randint(30, 240)

    # Risk level based on profile type and privileges
    risk_levels = ["LOW", "MEDIUM", "HIGH", "CRITICAL"]
    risk_weights = [0.2, 0.4, 0.3, 0.1]  # Default distribution

    if "admin" in lower_name or "privileged" in lower_name:
        risk_weights = [0.0, 0.1, 0.6, 0.3]  # Higher risk for admins
    elif "service" in lower_name:
        risk_weights = [0.1, 0.3, 0.5, 0.1]  # Medium-high for service accounts
    elif "temporary" in lower_name or "emergency" in lower_name:
        risk_weights = [0.0, 0.2, 0.5, 0.3]  # Higher risk for temporary access
    elif "read" in lower_name:
        risk_weights = [0.4, 0.5, 0.1, 0.0]  # Lower risk for read-only

    risk_level = random.choices(
        risk_levels,
        weights=risk_weights,
        k=1
    )[0]

    # Generate reasonable timestamps
    now = datetime.now()
    created_at = now - timedelta(days=random.randint(30, 365 * 2))  # 1 month to 2 years ago
    updated_at = created_at + timedelta(days=random.randint(0, (now - created_at).days))

    # Max inactive days based on risk level
    max_inactive_days_map = {
        "LOW": random.randint(90, 180),
        "MEDIUM": random.randint(60, 90),
        "HIGH": random.randint(30, 60),
        "CRITICAL": random.randint(7, 30)
    }
    max_inactive_days = max_inactive_days_map.get(risk_level, 90)

    # Construct the identity profile record (without ID fields)
    identity_profile = {
        "name": profile_name,
        "description": description,
        "access_review_frequency_days": review_frequency,
        "max_inactive_days": max_inactive_days,
        "requires_mfa": requires_mfa,
        "password_expiry_days": password_expiry_days,
        "default_session_timeout_minutes": default_session_timeout_minutes,
        "risk_level": risk_level,
        "created_at": created_at.isoformat(),
        "updated_at": updated_at.isoformat()
    }

    return identity_profile
