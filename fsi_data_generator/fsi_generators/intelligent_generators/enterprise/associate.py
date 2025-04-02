from ...helpers.parse_address import parse_address
from data_generator import DataGenerator
from faker import Faker
from typing import Any, Dict

import datetime
import random


def generate_random_associate(_id_fields: Dict[str, Any], _dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random "enterprise.associates" record with reasonable values.

    Args:
        _id_fields: Dictionary containing the required ID fields
                   (enterprise_associate_id)
        _dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated associate data
        (without ID fields)
    """
    # Initialize Faker for consistent generation
    fake = Faker('en_US')

    # Job titles for various departments
    job_titles = [
        # Banking Roles
        "Teller", "Personal Banker", "Branch Manager", "Loan Officer",
        "Credit Analyst", "Mortgage Specialist", "Financial Advisor",

        # IT Roles
        "IT Support Specialist", "Network Administrator", "Security Analyst",
        "Software Developer", "Database Administrator", "Cloud Engineer",
        "Systems Architect", "DevOps Engineer",

        # Management Roles
        "Department Head", "Senior Manager", "Director", "Vice President",
        "Chief Technology Officer", "Chief Financial Officer",

        # Back Office Roles
        "Compliance Officer", "Risk Analyst", "Fraud Investigator",
        "Operations Specialist", "Customer Service Representative",

        # Finance Roles
        "Accountant", "Financial Analyst", "Investment Specialist",
        "Payroll Specialist", "Budget Analyst"
    ]

    # Officer titles
    officer_titles = [
        "VP", "SVP", "EVP", "MD", "Director", "Senior Director",
        "Chief", "Associate", "Junior", "Executive", None
    ]

    # Updated: Use the enum values for associate status
    associate_statuses = [
        "ACTIVE", "INACTIVE", "PENDING_START", "ON_LEAVE", "TERMINATED"
    ]

    # Updated: Use the enum values for relationship types
    relationship_types = [
        "EMPLOYEE", "CONTRACTOR", "CONSULTANT", "INTERN", "TEMPORARY"
    ]

    # Generate hire dates
    today = datetime.date.today()
    hire_date = today - datetime.timedelta(days=random.randint(30, 365 * 15))

    # Potentially generate a release date with updated status options
    # Weight the statuses to make Active more common
    status = random.choices(
        associate_statuses,
        weights=[0.7, 0.1, 0.1, 0.05, 0.05]
    )[0]

    # Only generate release date for Inactive or Terminated
    release_date = None
    if status in ["INACTIVE", "TERMINATED"]:
        release_date = today - datetime.timedelta(days=random.randint(1, 365))

    # Generate names using Faker
    first_name = fake.first_name()
    last_name = fake.last_name()

    # Generate email with consistent formatting
    email_domain = random.choice([
        "bank.com", "financialservices.com", "enterprise.com",
        "corporate.com", "businessbank.com"
    ])
    email = f"{first_name.lower()}.{last_name.lower()}@{email_domain}"

    # Generate a complete, consistent address
    full_address = fake.address()
    address_components = parse_address(full_address)

    # Generate salary (with variation based on job title)
    base_salaries = {
        "Teller": (35000, 55000),
        "Personal Banker": (45000, 75000),
        "Loan Officer": (55000, 95000),
        "Manager": (80000, 150000),
        "Director": (120000, 250000),
        "VP": (180000, 350000),
        "CTO": (200000, 400000),
        "Developer": (70000, 150000),
        "Analyst": (60000, 120000)
    }

    # Select job title and determine salary range
    job_title = random.choice(job_titles)
    salary_category = next(
        (cat for cat in base_salaries if cat.lower() in job_title.lower()),
        "Analyst"
    )
    min_salary, max_salary = base_salaries[salary_category]
    salary = round(random.uniform(min_salary, max_salary), 2)

    # Generate phone number
    phone_number = fake.phone_number()

    # Prepare associates record
    associate = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone_number": phone_number,
        "hire_date": hire_date,
        "status": status,
        "job_title": job_title,
        "officer_title": random.choice(officer_titles),
        "salary": salary,
        "relationship_type": random.choice(relationship_types),
        "street_address": address_components['street_address'],
        "city": address_components['city'],
        "state": address_components['state'],
        "post_code": address_components['post_code'],
        "country": "US"
    }

    # Add optional release date if applicable
    if release_date:
        associate["release_date"] = release_date

    return associate
