from .enums import (ApplicationLifecycleStatus, ApplicationType,
                    DeploymentEnvironment)
from data_generator import DataGenerator
from fsi_data_generator.fsi_generators.helpers.generate_unique_json_array import \
    generate_unique_json_array
from typing import Any, Dict

import datetime
import logging
import psycopg2
import random

logger = logging.getLogger(__name__)


def generate_random_application(_id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random app_mgmt application record with reasonable values.
    Ensures application owners are active employees for non-archived applications,
    and sets the department ID to match the owner's department.

    Args:
        _id_fields: Dictionary containing the required ID fields (app_mgmt_application_id)
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated application data (without ID fields)
    """
    # Get connection for fetching related data
    conn = dg.conn

    # First, get existing application names to avoid duplicates
    existing_application_names = get_existing_application_names(conn)

    # Default fallback values
    application_names = [
        "Customer Account Portal", "Loan Origination System", "Mobile Banking App",
        "Credit Card Management", "Risk Assessment Platform", "Regulatory Reporting Tool",
        "Fraud Detection System", "Transaction Processing Engine", "Investment Dashboard",
        "Mortgage Servicing Platform", "Customer Relationship Manager", "Financial Analysis Tool",
        "Compliance Monitoring System", "Payment Gateway", "Treasury Management System",
        "Credit Scoring Engine", "Document Management System", "Customer Onboarding Portal",
        "Collections Management System", "Branch Operations Platform", "ATM Network Manager",
        "Card Issuance System", "Internal HR Portal", "Financial Planning Tool",
        "Anti-Money Laundering System", "Wealth Management Platform", "Core Banking System"
    ]

    vendors = [
        "FIS", "Fiserv", "Jack Henry", "Temenos", "Oracle Financial Services",
        "Finastra", "Mambu", "nCino", "Upstart", "Q2", "ACI Worldwide", "BlackRock",
        "In-House Development", "Fintech Partners", "Bank Systems Inc.",
        "Financial Software Solutions", "Banking Technology Corp", "Custom Solutions Team",
        "Enterprise FinTech", "Core Systems Group", "Banking Cloud Solutions"
    ]

    # Try to use generate_unique_json_array for application names
    try:
        generated_names = generate_unique_json_array(
            dbml_string=dg.dbml,
            fully_qualified_column_name='app_mgmt.applications.application_name - Financial institution applications including account management systems, transaction processing, loan origination, credit scoring, fraud detection, customer portals, mobile banking, investment platforms, risk management, regulatory reporting, and internal operational tools',
            count=50,
            cache_key='application_names'
        )
        if generated_names:
            application_names = generated_names
    except Exception as e:
        logger.error(f"Error generating application names: {e}")
        # Continue with fallback values
        pass

    # Try to use generate_unique_json_array for vendor names
    try:
        generated_vendors = generate_unique_json_array(
            dbml_string=dg.dbml,
            fully_qualified_column_name='app_mgmt.applications.vendor - Major financial software vendors like FIS, Fiserv, Jack Henry, Temenos, Oracle Financial Services, Finastra, Mambu, nCino, Upstart, Q2, ACI Worldwide, BlackRock, and custom in-house development teams',
            count=30,
            cache_key='application_vendors'
        )
        if generated_vendors:
            vendors = generated_vendors
    except Exception as e:
        logger.error(f"Error generating vendor names: {e}")
        # Continue with fallback values
        pass

    # Filter out names that already exist in the database
    available_names = [name for name in application_names if name not in existing_application_names]

    # If we've run out of available names, create a new unique name
    if not available_names:
        base_names = [
            "Financial", "Banking", "Credit", "Loan", "Investment", "Customer",
            "Transaction", "Regulatory", "Risk", "Security", "Compliance", "Payment"
        ]

        suffixes = [
            "System", "Platform", "Portal", "Manager", "Engine", "Dashboard",
            "Service", "Application", "Gateway", "Tracker", "Hub", "Central"
        ]

        # Keep generating new combinations until we find a unique one
        while True:
            timestamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d%H%M%S")
            application_name = f"{random.choice(base_names)} {random.choice(suffixes)} {timestamp[-4:]}"

            if application_name not in existing_application_names:
                break
    else:
        # Choose a random available name
        application_name = random.choice(available_names)

    # Get random values from enums using weighted selection
    application_type = ApplicationType.get_random()
    deployment_environment = DeploymentEnvironment.get_random()
    lifecycle_status = ApplicationLifecycleStatus.get_random()

    # Select vendor
    vendor = random.choice(vendors) if random.random() < 0.7 else None  # 30% chance of in-house app

    # Generate version with appropriate format
    if vendor and vendor != "In-House Development":
        # Vendor applications typically have formal versioning
        major = random.randint(1, 20)
        minor = random.randint(0, 40)
        patch = random.randint(0, 50)
        version = f"{major}.{minor}.{patch}"
    else:
        # Internal applications may have simpler versioning
        major = random.randint(1, 5)
        minor = random.randint(0, 9)
        version = f"{major}.{minor}"

    # Generate description based on application name and type
    descriptions = [
        f"A {application_type.name.lower()} application for {application_name.lower()} that provides essential functionality for financial operations.",
        f"Enterprise {application_name} system that enables secure and compliant banking operations.",
        f"Comprehensive {application_name.lower()} platform for processing financial transactions and managing customer data.",
        f"High-performance {application_name} solution designed for scale and reliability in banking environments.",
        f"{application_name} that ensures regulatory compliance and secure data handling for financial institutions.",
        f"Mission-critical {application_name.lower()} that supports core banking functions and integrates with enterprise systems.",
        f"Customer-facing {application_name} that provides self-service capabilities while maintaining strict security controls."
    ]
    description = random.choice(descriptions)

    # Generate deployment date based on lifecycle status
    today = datetime.date.today()

    if lifecycle_status == ApplicationLifecycleStatus.DEVELOPMENT:
        # Not deployed yet
        date_deployed = None
        date_retired = None
    elif lifecycle_status == ApplicationLifecycleStatus.PILOT:
        # Recently deployed
        days_ago = random.randint(1, 90)
        date_deployed = today - datetime.timedelta(days=days_ago)
        date_retired = None
    elif lifecycle_status == ApplicationLifecycleStatus.PRODUCTION:
        # Deployed some time ago
        days_ago = random.randint(90, 1825)  # 3 months to 5 years
        date_deployed = today - datetime.timedelta(days=days_ago)
        date_retired = None
    elif lifecycle_status == ApplicationLifecycleStatus.DEPRECATED:
        # Older application
        days_ago = random.randint(730, 2555)  # 2-7 years
        date_deployed = today - datetime.timedelta(days=days_ago)
        date_retired = None
    elif lifecycle_status == ApplicationLifecycleStatus.DATA_MAINTENANCE:
        # Very old application
        days_ago = random.randint(1095, 3650)  # 3-10 years
        date_deployed = today - datetime.timedelta(days=days_ago)
        date_retired = None
    elif lifecycle_status in [ApplicationLifecycleStatus.DECOMMISSIONED, ApplicationLifecycleStatus.ARCHIVED]:
        # Deployed and retired
        retired_days_ago = random.randint(30, 730)  # Retired between 1 month and 2 years ago
        deployment_duration = random.randint(365, 2555)  # Was in use for 1-7 years
        total_days_ago = retired_days_ago + deployment_duration

        date_deployed = today - datetime.timedelta(days=total_days_ago)
        date_retired = today - datetime.timedelta(days=retired_days_ago)
    else:
        # Default case
        date_deployed = None
        date_retired = None

    # Generate code repository URL
    domain = random.choice(["github.internal.bank.com", "gitlab.internal.bank.com", "bitbucket.internal.bank.com",
                            "azure-devops.internal.bank.com"])
    repo_name = application_name.lower().replace(" ", "-")
    source_code_repository = f"https://{domain}/{repo_name}"

    # Generate documentation URL
    doc_domains = ["confluence.bank.internal", "docs.bank.internal", "wiki.bank.internal", "sharepoint.bank.internal"]
    doc_domain = random.choice(doc_domains)
    documentation_url = f"https://{doc_domain}/applications/{repo_name}"

    # Generate RTO (Recovery Time Objective) and RPO (Recovery Point Objective)
    rto, rpo = determine_rto_rpo(application_name, lifecycle_status.name)

    # Find suitable application owner and get their department
    application_owner_id, enterprise_department_id = _get_suitable_application_owner(conn, lifecycle_status)

    candidate_created_by, candidate_modified_by = _get_created_and_modified_user_ids(conn, date_deployed, date_retired)

    # Create the application record
    application = {
        "application_name": application_name,
        "description": description,
        "application_type": application_type.name,  # Use the name attribute of the enum
        "vendor": vendor,
        "version": version,
        "deployment_environment": deployment_environment.name,  # Use the name attribute of the enum
        "lifecycle_status": lifecycle_status.name,  # Use the name attribute of the enum
        "date_deployed": date_deployed,
        "date_retired": date_retired,
        "source_code_repository": source_code_repository,
        "documentation_url": documentation_url,
        "rto": rto,
        "rpo": rpo,
        "application_owner_id": application_owner_id,
        "enterprise_department_id": enterprise_department_id,
        "created_by_user_id": candidate_created_by if candidate_created_by else _id_fields.get('created_by_user_id'),
        "modified_by_user_id": candidate_modified_by if candidate_modified_by else _id_fields.get('modified_by_user_id')
    }

    return application


def get_existing_application_names(conn) -> list:
    """
    Get all existing application names from the database.

    Args:
        conn: PostgreSQL connection object

    Returns:
        List of existing application names
    """
    try:
        cursor = conn.cursor()

        cursor.execute("""
                SELECT application_name
                FROM app_mgmt.applications
            """)

        results = cursor.fetchall()
        cursor.close()

        # Extract the names from the results
        return [result.get('application_name') for result in results] if results else []

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching existing application names: {error}")
        return []  # Return empty list on error to avoid blocking generation


def is_critical_application(application_name: str) -> bool:
    """
    Determine if an application is business-critical based on similarity to known critical applications.

    Args:
        application_name: Name of the application to evaluate

    Returns:
        Boolean indicating if the application is likely business-critical
    """
    # List of terms that suggest a business-critical application
    critical_terms = [
        "core", "banking", "payment", "transaction", "processing",
        "settlement", "clearing", "fraud", "authentication", "gateway",
        "platform", "central", "backbone", "regulatory", "compliance",
        "reporting", "customer", "account", "master", "data"
    ]

    # Convert application name to lowercase for easier comparison
    app_name_lower = application_name.lower()

    # Count how many critical terms appear in the application name
    term_matches = sum(1 for term in critical_terms if term in app_name_lower)

    # Check for specific highly critical combinations
    critical_combinations = [
        ("core", "banking"),
        ("payment", "gateway"),
        ("transaction", "processing"),
        ("settlement", "system"),
        ("customer", "account"),
        ("fraud", "detection"),
        ("identity", "authentication")
    ]

    # Count how many critical combinations appear in the application name
    combination_matches = sum(1 for combo in critical_combinations
                              if combo[0] in app_name_lower and combo[1] in app_name_lower)

    # Calculate a criticality score based on matches
    criticality_score = term_matches + (combination_matches * 3)

    # Applications with a score above a threshold are considered critical
    return criticality_score >= 3


def determine_rto_rpo(application_name: str, lifecycle_status: str) -> tuple:
    """
    Determine appropriate RTO and RPO values based on application criticality and lifecycle status.

    Args:
        application_name: Name of the application
        lifecycle_status: Current lifecycle status of the application

    Returns:
        Tuple of (RTO, RPO) as formatted strings
    """
    # Determine criticality
    is_critical = is_critical_application(application_name)

    # Check if application is in a production-like state
    is_production = lifecycle_status.lower() in ["production", "pilot"]

    # Determine RTO and RPO based on both criticality and lifecycle status
    if is_critical and is_production:
        # Critical applications in production - most stringent requirements
        rto_hours = random.randint(1, 4)
        rpo_minutes = random.randint(5, 30)
        rto = f"{rto_hours} hours"
        rpo = f"{rpo_minutes} minutes"
    elif is_critical and not is_production:
        # Critical applications not yet in production
        rto_hours = random.randint(8, 24)  # Less stringent than production
        rpo_hours = random.randint(1, 4)
        rto = f"{rto_hours} hours"
        rpo = f"{rpo_hours} hours"
    elif not is_critical and is_production:
        # Non-critical but production applications
        rto_hours = random.randint(24, 48)
        rpo_hours = random.randint(4, 12)
        rto = f"{rto_hours} hours"
        rpo = f"{rpo_hours} hours"
    else:
        # Non-critical and non-production applications
        rto_days = random.randint(3, 7)
        rpo_days = random.randint(1, 3)
        rto = f"{rto_days} days"
        rpo = f"{rpo_days} days"

    return rto, rpo


def _get_suitable_application_owner(conn, lifecycle_status) -> tuple:
    """
    Find a suitable application owner based on application lifecycle status.
    For non-archived applications, owners must be active employees.

    Args:
        conn: Database connection for executing queries
        lifecycle_status: Current lifecycle status of the application

    Returns:
        Tuple containing (application_owner_id, enterprise_department_id)
    """
    try:
        cursor = conn.cursor()

        if lifecycle_status not in [ApplicationLifecycleStatus.DECOMMISSIONED, ApplicationLifecycleStatus.ARCHIVED]:
            # Find active employees only for non-archived applications
            cursor.execute("""
                SELECT a.enterprise_associate_id, a.enterprise_department_id 
                FROM enterprise.associates a
                WHERE a.status = 'ACTIVE' AND a.relationship_type = 'EMPLOYEE'
                ORDER BY RANDOM()
                LIMIT 1
            """)
        else:
            # For archived or decommissioned applications, any associate is fine
            cursor.execute("""
                SELECT enterprise_associate_id, enterprise_department_id 
                FROM enterprise.associates
                ORDER BY RANDOM()
                LIMIT 1
            """)

        owner_data = cursor.fetchone()
        cursor.close()

        if owner_data:
            application_owner_id = owner_data.get('enterprise_associate_id')
            enterprise_department_id = owner_data.get('enterprise_department_id')
            return application_owner_id, enterprise_department_id
        else:
            # Fallback to random department if no suitable owner found
            application_owner_id = None
            cursor = conn.cursor()
            cursor.execute("""
                SELECT enterprise_department_id FROM enterprise.departments
                ORDER BY RANDOM() LIMIT 1
            """)
            dept_data = cursor.fetchone()
            cursor.close()
            enterprise_department_id = dept_data.get('enterprise_department_id') if dept_data else None
            return application_owner_id, enterprise_department_id

    except Exception as e:
        logger.error(f"Error finding application owner: {e}")
        return None, None


def _get_created_and_modified_user_ids(conn, date_deployed, date_retired) -> tuple:
    """
    Find appropriate user IDs for application creation and modification based on dates.
    - created_by_user_id must be an associate who was employed during date_deployed
    - If DECOMMISSIONED, modified_by_user_id must be an associate who was employed on date_retired

    Args:
        conn: Database connection for executing queries
        date_deployed: Date when the application was deployed
        date_retired: Date when the application was retired (if applicable)

    Returns:
        Tuple containing (created_by_user_id, modified_by_user_id)
    """
    created_by_user_id = None
    modified_by_user_id = None

    try:
        cursor = conn.cursor()

        # Find an associate who was employed during date_deployed
        if date_deployed:
            cursor.execute("""
                SELECT enterprise_associate_id 
                FROM enterprise.associates
                WHERE hire_date <= %s 
                AND (release_date IS NULL OR release_date >= %s)
                ORDER BY RANDOM()
                LIMIT 1
            """, (date_deployed, date_deployed))

            result = cursor.fetchone()
            if result:
                created_by_user_id = result.get('enterprise_associate_id')
        else:
            # If no deployment date, just get a random associate
            cursor.execute("""
                SELECT enterprise_associate_id 
                FROM enterprise.associates
                ORDER BY RANDOM()
                LIMIT 1
            """)
            result = cursor.fetchone()
            if result:
                created_by_user_id = result.get('enterprise_associate_id')

        # For retired applications, find an associate who was employed on the retirement date
        if date_retired:
            cursor.execute("""
                SELECT enterprise_associate_id 
                FROM enterprise.associates
                WHERE hire_date <= %s 
                AND (release_date IS NULL OR release_date >= %s)
                ORDER BY RANDOM()
                LIMIT 1
            """, (date_retired, date_retired))

            result = cursor.fetchone()
            if result:
                modified_by_user_id = result.get('enterprise_associate_id')

        cursor.close()

    except Exception as e:
        logger.error(f"Error finding application user IDs: {e}")
        # Default to None if there's an error

    return created_by_user_id, modified_by_user_id
