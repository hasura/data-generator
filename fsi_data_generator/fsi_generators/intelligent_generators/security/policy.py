import logging
import random
from datetime import datetime, timedelta
from typing import Any, Dict, Set

import anthropic
from faker import Faker

from data_generator import DataGenerator, SkipRowGenerationError
from fsi_data_generator.fsi_generators.helpers.generate_unique_json_array import \
    generate_unique_json_array

# Track previously generated policy names to ensure uniqueness
prev_policy_names: Set[str] = set()
logger = logging.getLogger(__name__)


def generate_random_policy(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random security.policies record.

    Args:
        id_fields: Dictionary containing predetermined ID fields
                  (security_policy_id, created_by_id, updated_by_id)
        dg: DataGenerator instance

    Returns:
        Dict containing a random policy record
        (without ID fields)
    """
    fake = Faker()

    # Try to get policy name examples from DBML if available
    policy_prefixes = [
        "Access Control",
        "Data Classification",
        "Password Management",
        "Network Security",
        "Remote Access",
        "Incident Response",
        "Acceptable Use",
        "Business Continuity",
        "Disaster Recovery",
        "Email Security",
        "Mobile Device Management",
        "Physical Security",
        "Risk Assessment",
        "Vulnerability Management",
        "Application Security",
        "Cloud Security",
        "Data Retention",
        "Device Encryption",
        "Identity Management",
        "Wireless Security"
    ]
    try:
        policy_prefixes = policy_prefixes + generate_unique_json_array(
            dbml_string=dg.dbml,
            fully_qualified_column_name='security.policies.name',
            count=20,
            cache_key='policy_names'
        )
    except anthropic.APIStatusError:
        pass

    # Generate policy name
    for _ in range(10):  # Try up to 10 times to generate a unique name
        prefix = random.choice(policy_prefixes)
        qualifier = random.choice([
            f"v{random.randint(1, 5)}.{random.randint(0, 9)}",
            f"for {random.choice(['Enterprise', 'Finance', 'Retail', 'Banking', 'Operations', 'Corporate', 'Customer Data'])}",
            f"- {random.choice(['Standard', 'Requirement', 'Guideline', 'Framework', 'Control'])}",
            f"({random.choice(['Internal', 'External', 'Global', 'Regional', 'Departmental'])})"
        ])

        policy_name = f"{prefix} Policy {qualifier}"

        # Check if name is unique
        if policy_name not in prev_policy_names:
            prev_policy_names.add(policy_name)
            break
    else:
        # If we couldn't generate a unique name after 10 tries, skip this row
        raise SkipRowGenerationError("Could not generate a unique policy name")

    # Generate timestamps
    now = datetime.now()

    # created_at: Between 1 and 730 days ago (1-2 years)
    created_at = now - timedelta(days=random.randint(1, 730))

    # started_at: Same as created_at or up to 30 days later
    started_at = created_at + timedelta(days=random.randint(0, 30))

    # Determine if the policy has an end date
    has_end_date = random.random() < 0.15  # 15% chance of having an end date

    # ended_at: If has_end_date, between start date and now
    ended_at = None
    if has_end_date:
        # Must be at least 30 days after start
        min_days_active = 30
        max_days_active = (now - started_at).days - 1

        if max_days_active >= min_days_active:
            days_active = random.randint(min_days_active, max_days_active)
            ended_at = started_at + timedelta(days=days_active)
        else:
            # If the start date is too recent for a minimum duration, don't end it
            has_end_date = False

    # updated_at: Between created_at and now
    days_since_creation = (now - created_at).days
    update_delay = random.randint(0, max(1, days_since_creation))
    updated_at = created_at + timedelta(days=update_delay)

    # active: True if no end date or end date is in the future
    active = not has_end_date

    # Generate description
    # Get some context about the policy from its name
    context = policy_name.lower()

    description = generate_policy_description(context, dg)

    # Construct the policy record
    policy = {
        "name": policy_name,
        "description": description,
        "created_at": created_at.isoformat(),
        "updated_at": updated_at.isoformat(),
        "started_at": started_at.isoformat(),
        "ended_at": ended_at.isoformat() if ended_at else None,
        "active": active
    }

    return policy


def generate_policy_description(context: str, dg: DataGenerator) -> str:
    """
    Generate a policy description based on the policy name context
    """
    # Extract key themes from the context
    access_keywords = ['access control', 'remote access', 'identity']
    data_keywords = ['data', 'classification', 'retention']
    network_keywords = ['network', 'wireless', 'remote']
    password_keywords = ['password', 'authentication', 'credential']
    device_keywords = ['device', 'mobile', 'encryption', 'physical']
    incident_keywords = ['incident', 'disaster', 'continuity']
    cloud_keywords = ['cloud', 'saas', 'iaas', 'paas']
    application_keywords = ['application', 'software', 'code']
    risk_keywords = ['risk', 'vulnerability', 'assessment']

    # Determine primary theme
    if any(keyword in context for keyword in access_keywords):
        return generate_access_policy_description(dg)
    elif any(keyword in context for keyword in data_keywords):
        return generate_data_policy_description(dg)
    elif any(keyword in context for keyword in network_keywords):
        return generate_network_policy_description(dg)
    elif any(keyword in context for keyword in password_keywords):
        return generate_password_policy_description(dg)
    elif any(keyword in context for keyword in device_keywords):
        return generate_device_policy_description(dg)
    elif any(keyword in context for keyword in incident_keywords):
        return generate_incident_policy_description(dg)
    elif any(keyword in context for keyword in cloud_keywords):
        return generate_cloud_policy_description(dg)
    elif any(keyword in context for keyword in application_keywords):
        return generate_application_policy_description(dg)
    elif any(keyword in context for keyword in risk_keywords):
        return generate_risk_policy_description(dg)
    else:
        return generate_generic_policy_description(dg)


def generate_access_policy_description(dg: DataGenerator) -> str:
    """Generate a description for an access control policy"""

    # Base descriptions
    descriptions = [
        "This policy establishes requirements for controlling access to the organization's information systems, applications, and data. It defines the principles of least privilege, separation of duties, and need-to-know basis for all access decisions.",
        "Defines the standards and procedures for granting, reviewing, and revoking access to information systems and data assets. Includes requirements for access approval workflows, periodic reviews, and automated deprovisioning of access rights.",
        "Outlines the organization's approach to managing user access rights throughout the identity lifecycle. Covers onboarding, role changes, and offboarding processes to ensure appropriate access controls are maintained at all times.",
        "Establishes the framework for managing privileged access to critical systems and sensitive data. Includes requirements for privileged account inventory, just-in-time access, and enhanced monitoring of privileged activities."
    ]

    # Try to get additional descriptions from DBML if available
    if dg:
        try:
            additional_descriptions = generate_unique_json_array(
                dbml_string=dg.dbml,
                fully_qualified_column_name='security.policies.description.access_control',
                count=20,
                cache_key='access_policy_descriptions'
            )
            descriptions.extend(additional_descriptions)
        except (anthropic.APIStatusError, Exception):
            pass

    return random.choice(descriptions)


def generate_data_policy_description(dg: DataGenerator = None) -> str:
    """Generate a description for a data-related policy"""

    # Base descriptions
    descriptions = [
        "This policy establishes the framework for classifying and handling data based on sensitivity and regulatory requirements. Defines data categories, labeling requirements, and appropriate security controls for each classification level.",
        "Outlines requirements for data storage, transmission, and disposal throughout the data lifecycle. Specifies encryption standards, secure transfer mechanisms, and secure disposal methods to protect data confidentiality and integrity.",
        "Defines responsibilities and procedures for data backup, archiving, and retention. Includes requirements for backup frequency, testing, offsite storage, and retention periods aligned with legal and regulatory obligations.",
        "Establishes standards for managing personally identifiable information (PII) and other regulated data. Includes requirements for data minimization, consent management, and data subject access requests."
    ]

    # Try to get additional descriptions from DBML if available
    if dg:
        try:
            additional_descriptions = generate_unique_json_array(
                dbml_string=dg.dbml,
                fully_qualified_column_name='security.policies.description.data_policy',
                count=20,
                cache_key='data_policy_descriptions'
            )
            descriptions.extend(additional_descriptions)
        except (anthropic.APIStatusError, Exception):
            pass

    return random.choice(descriptions)


def generate_network_policy_description(dg: DataGenerator = None) -> str:
    """Generate a description for a network security policy"""

    # Base descriptions
    descriptions = [
        "This policy establishes requirements for securing network infrastructure, connections, and communications. Defines standards for network segmentation, traffic filtering, and monitoring to protect against unauthorized access and data breaches.",
        "Outlines the organization's approach to securing wireless networks and connections. Includes requirements for encryption, authentication, guest access, and protection against rogue access points.",
        "Defines requirements for securing remote network access by employees, contractors, and third parties. Establishes standards for VPN, multi-factor authentication, and endpoint security checks before granting network access.",
        "Establishes standards for network architecture, boundary protection, and defense-in-depth. Includes requirements for firewalls, intrusion detection/prevention systems, and traffic flow controls."
    ]

    # Try to get additional descriptions from DBML if available
    if dg:
        try:
            additional_descriptions = generate_unique_json_array(
                dbml_string=dg.dbml,
                fully_qualified_column_name='security.policies.description.network_security',
                count=20,
                cache_key='network_policy_descriptions'
            )
            descriptions.extend(additional_descriptions)
        except (anthropic.APIStatusError, Exception):
            pass

    return random.choice(descriptions)


def generate_password_policy_description(dg: DataGenerator = None) -> str:
    """Generate a description for a password management policy"""

    # Base descriptions
    descriptions = [
        "This policy establishes requirements for creating and managing strong authentication credentials. Defines standards for password complexity, rotation, history, and secure storage to protect against unauthorized access.",
        "Outlines the organization's approach to multi-factor authentication (MFA) implementation and management. Specifies systems requiring MFA, approved authentication methods, and processes for emergency access.",
        "Defines standards for managing shared and system account credentials. Includes requirements for password vaults, privileged access management solutions, and emergency access procedures.",
        "Establishes requirements for credential lifecycle management from creation to retirement. Includes provisions for automated password resets, self-service portals, and secure credential recovery."
    ]

    # Try to get additional descriptions from DBML if available
    if dg:
        try:
            additional_descriptions = generate_unique_json_array(
                dbml_string=dg.dbml,
                fully_qualified_column_name='security.policies.description.password_management',
                count=20,
                cache_key='password_policy_descriptions'
            )
            descriptions.extend(additional_descriptions)
        except (anthropic.APIStatusError, Exception):
            pass

    return random.choice(descriptions)


def generate_device_policy_description(dg: DataGenerator = None) -> str:
    """Generate a description for a device security policy"""

    # Base descriptions
    descriptions = [
        "This policy establishes requirements for securing end-user computing devices including laptops, desktops, and mobile devices. Defines standards for device configuration, encryption, and security controls.",
        "Outlines the organization's approach to managing mobile devices that access corporate data and systems. Includes requirements for device enrollment, security controls, application management, and remote wiping capabilities.",
        "Defines standards for securing devices used for remote work. Establishes requirements for device encryption, VPN usage, endpoint protection, and secure home network configurations.",
        "Establishes requirements for physical protection of computing devices and media. Includes standards for screen locking, cable locks, secure transport, and proper disposal of hardware."
    ]

    # Try to get additional descriptions from DBML if available
    if dg:
        try:
            additional_descriptions = generate_unique_json_array(
                dbml_string=dg.dbml,
                fully_qualified_column_name='security.policies.description.device_security',
                count=20,
                cache_key='device_policy_descriptions'
            )
            descriptions.extend(additional_descriptions)
        except (anthropic.APIStatusError, Exception):
            pass

    return random.choice(descriptions)


def generate_incident_policy_description(dg: DataGenerator = None) -> str:
    """Generate a description for an incident or continuity policy"""

    # Base descriptions
    descriptions = [
        "This policy establishes the framework for detecting, reporting, and responding to security incidents. Defines incident classification, response procedures, communication protocols, and post-incident activities.",
        "Outlines requirements for maintaining business operations during disruptive events. Includes business impact analysis, recovery time objectives, and procedures for activating contingency plans.",
        "Defines the organization's approach to recovering from disasters affecting information systems and facilities. Establishes recovery strategies, alternate processing sites, and testing requirements.",
        "Establishes procedures for managing major security incidents including data breaches, ransomware, and DDoS attacks. Includes requirements for containment, eradication, recovery, and lessons learned."
    ]

    # Try to get additional descriptions from DBML if available
    if dg:
        try:
            additional_descriptions = generate_unique_json_array(
                dbml_string=dg.dbml,
                fully_qualified_column_name='security.policies.description.incident_response',
                count=20,
                cache_key='incident_policy_descriptions'
            )
            descriptions.extend(additional_descriptions)
        except (anthropic.APIStatusError, Exception):
            pass

    return random.choice(descriptions)


def generate_cloud_policy_description(dg: DataGenerator = None) -> str:
    """Generate a description for a cloud security policy"""

    # Base descriptions
    descriptions = [
        "This policy establishes requirements for securing cloud services and data across IaaS, PaaS, and SaaS environments. Defines standards for secure configuration, access controls, and monitoring of cloud resources.",
        "Outlines the organization's approach to evaluating and selecting cloud service providers. Includes requirements for security assessments, contractual safeguards, and compliance verification.",
        "Defines standards for protecting data stored in cloud environments. Establishes requirements for encryption, data segregation, backup, and secure deletion across cloud platforms.",
        "Establishes the framework for maintaining security visibility and governance across multi-cloud environments. Includes requirements for centralized monitoring, configuration management, and identity federation."
    ]

    # Try to get additional descriptions from DBML if available
    if dg:
        try:
            additional_descriptions = generate_unique_json_array(
                dbml_string=dg.dbml,
                fully_qualified_column_name='security.policies.description.cloud_security',
                count=20,
                cache_key='cloud_policy_descriptions'
            )
            descriptions.extend(additional_descriptions)
        except (anthropic.APIStatusError, Exception):
            pass

    return random.choice(descriptions)


def generate_application_policy_description(dg: DataGenerator = None) -> str:
    """Generate a description for an application security policy"""

    # Base descriptions
    descriptions = [
        "This policy establishes requirements for securing applications throughout the software development lifecycle. Defines standards for secure coding, testing, and deployment to prevent security vulnerabilities.",
        "Outlines the organization's approach to application security testing. Includes requirements for static analysis, dynamic testing, and penetration testing at key stages of development.",
        "Defines standards for managing third-party and open source components in applications. Establishes requirements for component inventory, vulnerability scanning, and patch management.",
        "Establishes the framework for securing application programming interfaces (APIs). Includes standards for authentication, authorization, input validation, and API traffic monitoring."
    ]

    # Try to get additional descriptions from DBML if available
    if dg:
        try:
            additional_descriptions = generate_unique_json_array(
                dbml_string=dg.dbml,
                fully_qualified_column_name='security.policies.description.application_security',
                count=20,
                cache_key='application_policy_descriptions'
            )
            descriptions.extend(additional_descriptions)
        except (anthropic.APIStatusError, Exception):
            pass

    return random.choice(descriptions)


def generate_risk_policy_description(dg: DataGenerator = None) -> str:
    """Generate a description for a risk management policy"""

    # Base descriptions
    descriptions = [
        "This policy establishes the framework for identifying, assessing, and managing information security risks. Defines methodologies, roles, responsibilities, and reporting requirements for risk management activities.",
        "Outlines the organization's approach to vulnerability management. Includes requirements for scanning, prioritization, remediation timelines, and exception handling.",
        "Defines standards for conducting security assessments of information systems and infrastructure. Establishes requirements for assessment scope, methodology, frequency, and reporting.",
        "Establishes requirements for managing third-party security risks. Includes standards for vendor assessment, contractual requirements, ongoing monitoring, and termination procedures."
    ]

    # Try to get additional descriptions from DBML if available
    if dg:
        try:
            additional_descriptions = generate_unique_json_array(
                dbml_string=dg.dbml,
                fully_qualified_column_name='security.policies.description.risk_management',
                count=20,
                cache_key='risk_policy_descriptions'
            )
            descriptions.extend(additional_descriptions)
        except (anthropic.APIStatusError, Exception):
            pass

    return random.choice(descriptions)


def generate_generic_policy_description(dg: DataGenerator = None) -> str:
    """Generate a generic policy description"""

    # Base descriptions
    descriptions = [
        "This policy establishes requirements for safeguarding the confidentiality, integrity, and availability of organizational information assets. It defines controls, responsibilities, and compliance measures aligned with industry standards and regulatory requirements.",
        "Outlines the organization's approach to managing information security risks and implementing appropriate controls. Includes requirements for regular reviews, compliance monitoring, and continuous improvement.",
        "Defines standards and procedures for protecting sensitive information and systems from unauthorized access, use, disclosure, disruption, modification, or destruction. Establishes a framework for security governance and accountability.",
        "Establishes security requirements and baseline controls to protect the organization's information assets. Includes provisions for regular assessment, awareness training, and enforcement of security measures."
    ]

    # Try to get additional descriptions from DBML if available
    if dg:
        try:
            additional_descriptions = generate_unique_json_array(
                dbml_string=dg.dbml,
                fully_qualified_column_name='security.policies.description.generic',
                count=20,
                cache_key='generic_policy_descriptions'
            )
            descriptions.extend(additional_descriptions)
        except (anthropic.APIStatusError, Exception):
            pass

    return random.choice(descriptions)
