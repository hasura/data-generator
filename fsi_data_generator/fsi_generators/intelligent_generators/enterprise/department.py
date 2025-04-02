from .enums.operating_unit import OperatingUnit
from data_generator import DataGenerator, SkipRowGenerationError
from faker import Faker
from typing import Any, Dict

import logging
import psycopg2
import random

logger = logging.getLogger(__name__)
fake = Faker()  # Initialize Faker

prev_department = set()


def generate_random_department(_id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random "enterprise.departments" record with reasonable values.

    Args:
        _id_fields: Dictionary containing the required ID fields (enterprise_department_id)
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated department data (without ID fields)
    """
    # Get connection for fetching related data
    conn = dg.conn

    # First, get existing department names to avoid duplicates (as department_name is unique)
    existing_department_names = get_existing_department_names(conn)

    # Choose a random operating unit
    operating_unit = OperatingUnit.get_random()

    # Create department names based on operating unit
    department_name = generate_department_name_for_operating_unit(operating_unit, existing_department_names)

    # Create the department record
    department = {
        "department_name": department_name,
        "operating_unit": operating_unit.name
        # No need to generate enterprise_building_id as it will be provided
        # in _id_fields or managed by the system/data insertion process
    }

    if department_name in prev_department:
        raise SkipRowGenerationError

    prev_department.add(department_name)

    return department


def generate_department_name_for_operating_unit(operating_unit, existing_names):
    """
    Generate a department name appropriate for the given operating unit.

    Args:
        operating_unit: The OperatingUnit enum value
        existing_names: List of existing department names to avoid duplicates

    Returns:
        A department name that aligns with the operating unit
    """
    # Define department names by operating unit
    department_options = {
        OperatingUnit.HR: [
            "Talent Acquisition", "Employee Relations", "Benefits Administration",
            "Compensation", "Workforce Planning", "HR Operations",
            "Training & Development", "HR Analytics", "Organizational Development",
            "Payroll Services", "Executive Recruitment", "Employee Engagement"
        ],
        OperatingUnit.IT: [
            "Application Development", "Infrastructure Services", "Network Administration",
            "Cybersecurity", "Data Center Operations", "IT Support",
            "Architecture & Design", "Database Administration", "Quality Assurance",
            "Digital Transformation", "Cloud Services", "IT Governance",
            "Software Engineering", "IT Project Management", "Enterprise Systems"
        ],
        OperatingUnit.OPS: [
            "Transaction Processing", "Operations Support", "Back Office Operations",
            "Process Improvement", "Vendor Management", "Operational Risk",
            "Facilities Management", "Business Continuity", "Document Services",
            "Procurement", "Administrative Services", "Operational Excellence",
            "Branch Operations", "ATM Operations", "Cash Management Operations"
        ],
        OperatingUnit.RISK: [
            "Credit Risk", "Market Risk", "Operational Risk Management",
            "Enterprise Risk", "Fraud Prevention", "Risk Analytics",
            "Model Risk Management", "Regulatory Risk", "Financial Risk",
            "Risk Governance", "Risk Reporting", "Stress Testing",
            "Risk Technology", "Risk Advisory", "Compliance Risk"
        ],
        OperatingUnit.LEGAL: [
            "Corporate Legal", "Regulatory Compliance", "Litigation",
            "Contract Management", "Intellectual Property", "Legal Operations",
            "Corporate Governance", "Ethics & Compliance", "Privacy",
            "Employment Law", "Securities Law", "Banking Law"
        ],
        OperatingUnit.CONSUMER_BANKING: [
            "Retail Banking", "Branch Services", "Digital Banking",
            "Account Services", "Customer Experience", "ATM Banking",
            "Personal Banking", "Deposit Operations", "Customer Acquisition",
            "Transaction Banking", "Savings Programs", "Banking Products",
            "Banking Services", "Daily Banking", "Customer Onboarding"
        ],
        OperatingUnit.CONSUMER_LENDING: [
            "Personal Loans", "Auto Lending", "Student Loans",
            "Credit Underwriting", "Loan Origination", "Collections",
            "Loan Servicing", "Consumer Credit", "Debt Recovery",
            "Loan Processing", "Credit Authorization", "Loan Documentation",
            "Personal Lines of Credit", "Debt Consolidation", "Home Improvement Loans"
        ],
        OperatingUnit.SMALL_BUSINESS_BANKING: [
            "Business Banking", "Small Business Lending", "Merchant Services",
            "Business Accounts", "Business Development", "Treasury Services",
            "Business Credit Cards", "Business Client Services", "Business Loans",
            "Startup Banking", "Nonprofit Banking", "Business Cash Management",
            "Business Advisory", "Franchise Banking", "Professional Services Banking"
        ],
        OperatingUnit.CREDIT_CARDS: [
            "Card Products", "Card Operations", "Card Services",
            "Card Marketing", "Card Partnerships", "Card Risk Management",
            "Card Fraud", "Card Benefits", "Card Technology",
            "Card Issuance", "Card Processing", "Rewards Programs",
            "Card Analytics", "Card Portfolio Management", "Card Acquisition"
        ],
        OperatingUnit.MORTGAGE_SERVICES: [
            "Mortgage Lending", "Mortgage Origination", "Mortgage Servicing",
            "Mortgage Underwriting", "Appraisal Services", "Mortgage Processing",
            "Home Equity", "Mortgage Compliance", "Mortgage Operations",
            "Residential Mortgages", "Mortgage Documentation", "Closing Services",
            "Refinancing", "Mortgage Product Development", "Construction Lending"
        ]
    }

    options = department_options[operating_unit]

    # Filter out existing names
    available_options = [name for name in options if name not in existing_names]

    if available_options:
        return random.choice(available_options)
    else:
        # If all specific names are taken, create a more generic but still relevant name
        prefixes = ["Primary", "Central", "Core", "Strategic", "Global", "Regional", "Advanced", "Integrated"]
        while True:
            base_name = random.choice(options)
            prefix = random.choice(prefixes)
            new_name = f"{prefix} {base_name}"
            if new_name not in existing_names:
                return new_name


def get_existing_department_names(conn) -> list:
    """
    Get all existing department names from the database.

    Args:
        conn: PostgreSQL connection object

    Returns:
        List of existing department names
    """
    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT department_name
            FROM enterprise.departments
        """)

        results = cursor.fetchall()
        cursor.close()

        # Extract the names from the results
        return [result[0] for result in results] if results else []

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching existing department names: {error}")
        return []  # Return empty list on error to avoid blocking generation
