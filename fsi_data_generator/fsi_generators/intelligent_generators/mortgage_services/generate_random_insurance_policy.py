import datetime
import logging
import random
from typing import Any, Dict, Optional

import psycopg2

from data_generator import DataGenerator
from fsi_data_generator.fsi_generators.helpers.generate_unique_json_array import \
    generate_unique_json_array

logger = logging.getLogger(__name__)


def generate_random_insurance_policy(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random mortgage services insurance policy record with reasonable values.

    Args:
        id_fields: Dictionary containing the required ID fields (mortgage_services_servicing_account_id)
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated insurance policy data (without ID fields)
    """
    # Get servicing account information to make insurance policy data reasonable
    conn = dg.conn
    servicing_info = get_servicing_info(id_fields.get("mortgage_services_servicing_account_id"), conn)

    # Get property info based on the loan ID from servicing account
    property_info = None
    if servicing_info and 'mortgage_services_loan_id' in servicing_info:
        property_info = get_property_info(servicing_info['mortgage_services_loan_id'], conn)

    # Define possible values for categorical fields
    insurance_types = [
        "hazard",
        "flood",
        "wind",
        "earthquake",
        "liability",
        "umbrella"
    ]

    insurance_type_weights = [0.6, 0.2, 0.1, 0.05, 0.03, 0.02]  # Hazard is most common

    carrier_names = generate_unique_json_array(
        dbml_string=dg.dbml,
        fully_qualified_column_name='mortgage_services.insurance_policies.carrier_name',
        count=50,
        cache_key='insurance_carrier_names'
    )

    status_options = [
        "active",
        "cancelled",
        "expired",
        "pending renewal",
        "lapsed"
    ]

    status_weights = [0.85, 0.05, 0.05, 0.03, 0.02]  # Active is most common

    # Select insurance type and carrier
    insurance_type = random.choices(insurance_types, weights=insurance_type_weights, k=1)[0]
    carrier_name = random.choice(carrier_names)

    # Generate policy number
    # Format varies by carrier but typically includes letters and numbers
    if "State Farm" in carrier_name:
        policy_number = f"SF-{random.randint(10000, 99999)}-{random.choice('ABCDEFGH')}"
    elif "Allstate" in carrier_name:
        policy_number = f"AL{random.randint(100000000, 999999999)}"
    elif "USAA" in carrier_name:
        policy_number = f"USAA{random.randint(1000000, 9999999)}-0{random.randint(1, 9)}"
    else:
        # Generic format for other carriers
        letters = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=2))
        policy_number = f"{letters}-{random.randint(1000000, 9999999)}"

    # Generate coverage amount
    if property_info and 'estimated_property_value' in property_info and property_info['estimated_property_value']:
        base_value = property_info['estimated_property_value']
    elif servicing_info and 'original_principal_balance' in servicing_info:
        # Estimate property value as 125% of loan amount (assuming 80% LTV)
        base_value = servicing_info['original_principal_balance'] * 1.25
    else:
        # Default to reasonable home value
        base_value = random.uniform(200000, 750000)

    # Coverage amount varies by insurance type
    if insurance_type == "hazard":
        # Hazard insurance typically covers the replacement cost of the home
        coverage_amount = round(base_value * random.uniform(0.9, 1.1), 2)
    elif insurance_type == "flood":
        # Flood insurance might cover less than full value
        coverage_amount = round(base_value * random.uniform(0.6, 0.9), 2)
    elif insurance_type == "wind":
        coverage_amount = round(base_value * random.uniform(0.7, 0.9), 2)
    elif insurance_type == "earthquake":
        coverage_amount = round(base_value * random.uniform(0.6, 0.8), 2)
    elif insurance_type == "liability":
        # Liability coverage often in standard increments
        coverage_options = [300000, 500000, 1000000]
        coverage_amount = random.choice(coverage_options)
    elif insurance_type == "umbrella":
        # Umbrella policies typically start at $1 million
        coverage_options = [1000000, 2000000, 3000000, 5000000]
        coverage_amount = random.choice(coverage_options)
    else:
        coverage_amount = round(base_value * random.uniform(0.8, 1.0), 2)

    # Generate annual premium
    if insurance_type == "hazard":
        # Hazard insurance typically 0.25% to 0.5% of home value annually
        premium_rate = random.uniform(0.0025, 0.005)
        annual_premium = round(base_value * premium_rate, 2)
    elif insurance_type == "flood":
        # Flood insurance can be more expensive
        premium_rate = random.uniform(0.005, 0.015)
        annual_premium = round(base_value * premium_rate, 2)
    elif insurance_type == "wind":
        premium_rate = random.uniform(0.003, 0.008)
        annual_premium = round(base_value * premium_rate, 2)
    elif insurance_type == "earthquake":
        premium_rate = random.uniform(0.004, 0.01)
        annual_premium = round(base_value * premium_rate, 2)
    elif insurance_type == "liability":
        # Liability is typically a flat rate
        annual_premium = round(random.uniform(150, 500), 2)
    elif insurance_type == "umbrella":
        # Umbrella policies often priced per million of coverage
        rate_per_million = random.uniform(150, 300)
        annual_premium = round(rate_per_million * (coverage_amount / 1000000), 2)
    else:
        annual_premium = round(base_value * random.uniform(0.003, 0.006), 2)

    # Generate effective and expiration dates
    today = datetime.date.today()

    # Policy expiration date - typically 1 year from effective date
    if servicing_info and 'homeowners_insurance_due_date' in servicing_info and servicing_info[
        'homeowners_insurance_due_date']:
        # Use due date from servicing account if available
        expiration_date = servicing_info['homeowners_insurance_due_date']
        # Effective date is typically 1 year before expiration
        effective_date = datetime.date(expiration_date.year - 1, expiration_date.month, expiration_date.day)
    else:
        # Randomly generate dates
        months_ahead = random.randint(-10, 14)  # Policy might have expired or be valid for over a year
        expiration_month = (today.month + months_ahead) % 12
        if expiration_month == 0:
            expiration_month = 12
        expiration_year = today.year + ((today.month + months_ahead) // 12)
        expiration_day = min(today.day, [31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][expiration_month - 1])
        expiration_date = datetime.date(expiration_year, expiration_month, expiration_day)

        # Effective date is typically 1 year before expiration
        effective_date = datetime.date(expiration_date.year - 1, expiration_date.month, expiration_date.day)

    # Determine status based on dates
    if expiration_date < today:
        # Policy has expired
        status = random.choices(["expired", "cancelled"], weights=[0.8, 0.2], k=1)[0]
    elif (expiration_date - today).days < 30:
        # Close to expiration
        status = random.choices(["active", "pending renewal"], weights=[0.6, 0.4], k=1)[0]
    else:
        # Normal active policy
        status = random.choices(status_options, weights=status_weights, k=1)[0]

    # Generate paid through escrow flag
    # Most mortgage insurance is paid through escrow
    paid_through_escrow = random.random() < 0.85  # 85% chance

    # Generate agent information
    agent_first_names = ["Michael", "Christopher", "Jessica", "Matthew", "Ashley", "Jennifer",
                         "Joshua", "Amanda", "Daniel", "Sarah", "James", "Robert", "John",
                         "Joseph", "William", "Linda", "Emily", "Patricia", "Nicole"]
    agent_last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller",
                        "Wilson", "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White",
                        "Harris", "Martin", "Thompson", "Garcia", "Martinez"]

    agent_name = f"{random.choice(agent_first_names)} {random.choice(agent_last_names)}"

    # Generate agent phone with format (XXX) XXX-XXXX
    area_code = random.randint(201, 989)
    prefix = random.randint(200, 999)
    line = random.randint(1000, 9999)
    agent_phone = f"({area_code}) {prefix}-{line}"

    # Create the insurance policy record
    insurance_policy = {
        "insurance_type": insurance_type,
        "carrier_name": carrier_name,
        "policy_number": policy_number,
        "coverage_amount": float(coverage_amount),
        "annual_premium": float(annual_premium),
        "effective_date": effective_date,
        "expiration_date": expiration_date,
        "paid_through_escrow": paid_through_escrow,
        "agent_name": agent_name,
        "agent_phone": agent_phone,
        "status": status
    }

    return insurance_policy


def get_servicing_info(servicing_account_id: Optional[int], conn) -> Optional[Dict[str, Any]]:
    """
    Get servicing account information to make insurance policy data reasonable.

    Args:
        servicing_account_id: The ID of the servicing account
        conn: PostgreSQL connection object

    Returns:
        Dictionary containing servicing account information or None if servicing_account_id is None or not found
    """
    if not servicing_account_id:
        return None

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT mortgage_services_loan_id, original_principal_balance, homeowners_insurance_due_date
            FROM mortgage_services.servicing_accounts 
            WHERE mortgage_services_servicing_account_id = %s
        """, (servicing_account_id,))

        result = cursor.fetchone()
        cursor.close()

        if result:
            return {
                "mortgage_services_loan_id": result[0],
                "original_principal_balance": float(result[1]) if result[1] is not None else None,
                "homeowners_insurance_due_date": result[2]
            }
        else:
            return None

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching servicing account information: {error}")
        return None


def get_property_info(loan_id: Optional[int], conn) -> Optional[Dict[str, Any]]:
    """
    Get property information to make insurance policy data reasonable.

    Args:
        loan_id: The ID of the loan
        conn: PostgreSQL connection object

    Returns:
        Dictionary containing property information or None if loan_id is None or property not found
    """
    if not loan_id:
        return None

    try:
        cursor = conn.cursor()

        # First get the application ID from the loan
        cursor.execute("""
            SELECT mortgage_services_application_id
            FROM mortgage_services.loans 
            WHERE mortgage_services_loan_id = %s
        """, (loan_id,))

        loan_result = cursor.fetchone()

        if not loan_result or not loan_result[0]:
            cursor.close()
            return None

        application_id = loan_result[0]

        # Then get property details from the application
        cursor.execute("""
            SELECT estimated_property_value
            FROM mortgage_services.applications
            WHERE mortgage_services_application_id = %s
        """, (application_id,))

        app_result = cursor.fetchone()
        cursor.close()

        if app_result:
            return {
                "estimated_property_value": float(app_result[0]) if app_result[0] is not None else None
            }
        else:
            return None

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching property information: {error}")
        return None
