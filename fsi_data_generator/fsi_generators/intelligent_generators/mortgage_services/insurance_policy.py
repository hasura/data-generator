from .enums import InsurancePolicyStatus, InsuranceType
from data_generator import DataGenerator
from fsi_data_generator.fsi_generators.helpers.generate_unique_json_array import \
    generate_unique_json_array
from typing import Any, Dict, Optional

import anthropic
import calendar
import datetime
import logging
import psycopg2
import random
import sys

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
    conn = dg.conn
    servicing_info = _get_servicing_info(id_fields.get("mortgage_services_servicing_account_id"), conn)
    property_info = None
    if servicing_info and 'mortgage_services_loan_id' in servicing_info:
        property_info = _get_property_info(servicing_info['mortgage_services_loan_id'], conn)

    carrier_names = [
        "State Farm Insurance",
        "Allstate Insurance",
        "Liberty Mutual",
        "Nationwide Insurance",
        "Farmers Insurance",
        "Progressive Insurance",
        "USAA Insurance",
    ]
    try:
        carrier_names += generate_unique_json_array(
            dbml_string=dg.dbml,
            fully_qualified_column_name='mortgage_services.insurance_policies.carrier_name',
            count=50,
            cache_key='insurance_carrier_names'
        )
    except anthropic.APIStatusError:
        pass

    insurance_type = InsuranceType.get_random()
    carrier_name = random.choice(carrier_names)

    if "State Farm" in carrier_name:
        policy_number = f"SF-{random.randint(10000, 99999)}-{random.choice('ABCDEFGH')}"
    elif "Allstate" in carrier_name:
        policy_number = f"AL{random.randint(100000000, 999999999)}"
    elif "USAA" in carrier_name:
        policy_number = f"USAA{random.randint(1000000, 9999999)}-0{random.randint(1, 9)}"
    else:
        letters = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=2))
        policy_number = f"{letters}-{random.randint(1000000, 9999999)}"

    if property_info and 'estimated_property_value' in property_info and property_info['estimated_property_value']:
        base_value = property_info['estimated_property_value']
    elif servicing_info and 'original_principal_balance' in servicing_info:
        base_value = servicing_info['original_principal_balance'] * 1.25
    else:
        base_value = random.uniform(200000, 750000)

    if insurance_type == InsuranceType.HAZARD:
        coverage_amount = round(base_value * random.uniform(0.9, 1.1), 2)
    elif insurance_type == InsuranceType.FLOOD:
        coverage_amount = round(base_value * random.uniform(0.6, 0.9), 2)
    elif insurance_type == InsuranceType.WIND:
        coverage_amount = round(base_value * random.uniform(0.7, 0.9), 2)
    elif insurance_type == InsuranceType.EARTHQUAKE:
        coverage_amount = round(base_value * random.uniform(0.6, 0.8), 2)
    else:
        coverage_amount = round(base_value * random.uniform(0.8, 1.0), 2)

    if insurance_type == InsuranceType.HAZARD:
        premium_rate = random.uniform(0.0025, 0.005)
        annual_premium = round(base_value * premium_rate, 2)
    elif insurance_type == InsuranceType.FLOOD:
        premium_rate = random.uniform(0.005, 0.015)
        annual_premium = round(base_value * premium_rate, 2)
    elif insurance_type == InsuranceType.WIND:
        premium_rate = random.uniform(0.003, 0.008)
        annual_premium = round(base_value * premium_rate, 2)
    elif insurance_type == InsuranceType.EARTHQUAKE:
        premium_rate = random.uniform(0.004, 0.01)
        annual_premium = round(base_value * premium_rate, 2)
    else:
        annual_premium = round(base_value * random.uniform(0.003, 0.006), 2)

    today = datetime.date.today()

    if servicing_info and 'homeowners_insurance_due_date' in servicing_info and servicing_info[
        'homeowners_insurance_due_date']:
        expiration_date = servicing_info['homeowners_insurance_due_date']
        effective_date = _get_valid_expiration_date(expiration_date.year - 1, expiration_date.month,
                                                    expiration_date.day)
    else:
        months_ahead = random.randint(-10, 14)
        expiration_month = (today.month + months_ahead) % 12 or 12
        expiration_year = today.year + ((today.month + months_ahead) // 12)
        expiration_day = today.day
        expiration_date = _get_valid_expiration_date(expiration_year, expiration_month, expiration_day)
        effective_date = _get_valid_expiration_date(expiration_date.year - 1, expiration_date.month,
                                                    expiration_date.day)

    if expiration_date < today:
        status_weights = [0, 0, 0.8, 0.2, 0, 0, 0, 0, 0, 0, 0, 0]
        status = InsurancePolicyStatus.get_random(status_weights)
    elif (expiration_date - today).days < 30:
        status_weights = [0.6, 0.4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        status = InsurancePolicyStatus.get_random(status_weights)
    else:
        status_weights = [0.85, 0.03, 0.02, 0.02, 0.01, 0.01, 0.01, 0.02, 0.01, 0.01, 0.005, 0.005]
        status = InsurancePolicyStatus.get_random(status_weights)

    paid_through_escrow = random.random() < 0.85

    agent_first_names = ["Michael", "Christopher", "Jessica", "Matthew", "Ashley", "Jennifer",
                         "Joshua", "Amanda", "Daniel", "Sarah", "James", "Robert", "John",
                         "Joseph", "William", "Linda", "Emily", "Patricia", "Nicole"]
    agent_last_names = ["Smith", "Johnson", "Williams", "Jones", "Brown", "Davis", "Miller",
                        "Wilson", "Moore", "Taylor", "Anderson", "Thomas", "Jackson", "White",
                        "Harris", "Martin", "Thompson", "Garcia", "Martinez"]
    agent_name = f"{random.choice(agent_first_names)} {random.choice(agent_last_names)}"
    area_code = random.randint(201, 989)
    prefix = random.randint(200, 999)
    line = random.randint(1000, 9999)
    agent_phone = f"({area_code}) {prefix}-{line}"

    insurance_policy = {
        "insurance_type": insurance_type.value,
        "carrier_name": carrier_name,
        "policy_number": policy_number,
        "coverage_amount": coverage_amount,
        "annual_premium": annual_premium,
        "effective_date": effective_date,
        "expiration_date": expiration_date,
        "paid_through_escrow": paid_through_escrow,
        "agent_name": agent_name,
        "agent_phone": agent_phone,
        "status": status.value
    }
    return insurance_policy


def _get_valid_expiration_date(year: int, month: int, day: int) -> datetime.date:
    last_day_of_month = calendar.monthrange(year, month)[1]
    valid_day = min(day, last_day_of_month)
    return datetime.date(year, month, valid_day)


def _get_servicing_info(servicing_account_id: Optional[int], conn) -> Optional[Dict[str, Any]]:
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
        return result
    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching servicing account information: {error}")
        return None


def _get_property_info(loan_id: Optional[int], conn) -> Optional[Dict[str, Any]]:
    if not loan_id:
        return None
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT mortgage_services_application_id
            FROM mortgage_services.loans 
            WHERE mortgage_services_loan_id = %s
        """, (loan_id,))
        loan_result = cursor.fetchone()
        if not loan_result or 'mortgage_services_application_id' not in loan_result:
            cursor.close()
            return None
        application_id = loan_result['mortgage_services_application_id']

        cursor.execute("""
            SELECT estimated_property_value
            FROM mortgage_services.applications
            WHERE mortgage_services_application_id = %s
        """, (application_id,))
        app_result = cursor.fetchone()
        cursor.close()
        return app_result
    except psycopg2.ProgrammingError as error:
        logger.error(f"Error fetching property information: {error}")
        sys.exit(-1)
    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching property information: {error}")
        return None
