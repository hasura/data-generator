import datetime
import logging
import random
from typing import Any, Dict, Optional

import anthropic
import psycopg2

from fsi_data_generator.fsi_generators.helpers.generate_unique_json_array import \
    generate_unique_json_array
from fsi_data_generator.fsi_generators.intelligent_generators.mortgage_services.enums.disbursement_status import \
    DisbursementStatus
from fsi_data_generator.fsi_generators.intelligent_generators.mortgage_services.enums.disbursement_type import \
    DisbursementType

logger = logging.getLogger(__name__)


def generate_random_escrow_disbursement(id_fields: Dict[str, Any], dg) -> Dict[str, Any]:
    """
    Generate a random mortgage services escrow disbursement record with realistic values.

    Args:
        id_fields: Dictionary containing the required ID fields (mortgage_services_servicing_account_id)
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated escrow disbursement data (without ID fields)
    """
    # Get servicing account information to make disbursement data reasonable
    conn = dg.conn
    servicing_account_info = _get_servicing_account_info(id_fields.get("mortgage_services_servicing_account_id"), conn)

    # Define weights for the enum values we want to select from
    # Only selecting a subset of the disbursement types, with specific weights
    disbursement_type_weights = [0.4, 0.3, 0.1, 0.1, 0.05, 0.05, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    # Use the BaseEnum.get_random method with the weights
    disbursement_type = DisbursementType.get_random(disbursement_type_weights)

    # Generate payee names based on disbursement type
    if disbursement_type == DisbursementType.PROPERTY_TAX:
        county_names = ["Adams", "Jefferson", "Washington", "Lincoln", "Franklin",
                        "Hamilton", "Jackson", "Madison", "Monroe", "Wilson"]
        state_names = ["AL", "CA", "FL", "GA", "IL", "NY", "OH", "PA", "TX", "VA"]
        payee_name = f"{random.choice(county_names)} County Tax Collector - {random.choice(state_names)}"

    elif disbursement_type in [DisbursementType.HOMEOWNERS_INSURANCE, DisbursementType.HAZARD_INSURANCE,
                               DisbursementType.FLOOD_INSURANCE]:
        insurance_companies = [
            "State Farm Insurance", "Allstate Insurance", "GEICO", "Liberty Mutual",
            "Nationwide Insurance", "Farmers Insurance", "Progressive Insurance",
            "American Family Insurance", "Travelers Insurance", "USAA Insurance"
        ]
        try:
            insurance_companies = insurance_companies + generate_unique_json_array(
                dbml_string=dg.dbml,
                fully_qualified_column_name='mortgage_services.escrow_disbursements.insurance_companies',
                count=50,
                cache_key='insurance_carrier_names'
            )
        except anthropic.APIStatusError:
            pass
        payee_name = random.choice(insurance_companies)

    elif disbursement_type == DisbursementType.MORTGAGE_INSURANCE:
        mi_companies = [
            "Mortgage Guaranty Insurance Corp", "Essent Guaranty", "Genworth Mortgage Insurance",
            "Radian Guaranty", "National Mortgage Insurance", "Arch Mortgage Insurance"
        ]
        try:
            mi_companies = mi_companies + generate_unique_json_array(
                dbml_string=dg.dbml,
                fully_qualified_column_name='mortgage_services.escrow_disbursements.mortgage_insurance_carrier',
                count=50,
                cache_key='mortgage_insurance_carrier_names'
            )
        except anthropic.APIStatusError:
            pass
        payee_name = random.choice(mi_companies)

    elif disbursement_type == DisbursementType.HOA_DUES:
        hoa_names = [
            "Willow Creek HOA", "Oakridge Community Association", "Pine Valley Homeowners",
            "Lakeside Estates HOA", "Meadowbrook Residents Association", "Highland Park HOA"
        ]
        try:
            hoa_names = hoa_names + generate_unique_json_array(
                dbml_string=dg.dbml,
                fully_qualified_column_name='mortgage_services.escrow_disbursements.hoa_names',
                count=50,
                cache_key='hoa_names'
            )
        except anthropic.APIStatusError:
            pass
        payee_name = random.choice(hoa_names)

    else:
        generic_payees = [
            "Municipal Services Inc", "County Services Department", "Regional Authority",
            "City Assessment Office", "Property Services LLC"
        ]
        payee_name = random.choice(generic_payees)

    # Generate disbursement date (typically within the last year)
    today = datetime.date.today()
    days_ago = random.randint(1, 365)
    disbursement_date = today - datetime.timedelta(days=days_ago)

    # Determine a realistic disbursement amount based on type and property information
    property_info = _get_property_info_from_servicing(servicing_account_info, conn)

    # Default amounts if we can't determine better values
    default_property_tax = 2500.00
    default_insurance = 1200.00
    default_mortgage_insurance = 1000.00
    default_hoa = 500.00

    # Try to calculate more appropriate values based on property info
    if property_info:
        # Calculate annual property tax (roughly 1-2% of property value)
        if 'property_value' in property_info and property_info['property_value']:
            annual_property_tax = float(property_info['property_value']) * random.uniform(0.01, 0.02)
        else:
            annual_property_tax = default_property_tax

        # Calculate annual homeowners/hazard insurance (roughly $3.50 per $1,000 of property value)
        if 'property_value' in property_info and property_info['property_value']:
            annual_insurance = float(property_info['property_value']) * 0.0035
        else:
            annual_insurance = default_insurance

        # Calculate flood insurance (typically $700-$3,000 annually)
        annual_flood_insurance = random.uniform(700, 3000)

        # Calculate mortgage insurance (0.5-1% of loan amount annually)
        if 'original_principal' in servicing_account_info and servicing_account_info['original_principal']:
            annual_mortgage_insurance = float(servicing_account_info['original_principal']) * random.uniform(0.005,
                                                                                                             0.01)
        else:
            annual_mortgage_insurance = default_mortgage_insurance

        # HOA dues (vary widely, $200-$600 monthly is common)
        annual_hoa = random.uniform(2400, 7200)
    else:
        annual_property_tax = default_property_tax
        annual_insurance = default_insurance
        annual_flood_insurance = random.uniform(700, 3000)
        annual_mortgage_insurance = default_mortgage_insurance
        annual_hoa = default_hoa

    # Set amount based on disbursement type - consider if payment is usually annual or semi-annual
    if disbursement_type == DisbursementType.PROPERTY_TAX:
        # Property taxes often paid semi-annually
        amount = round(annual_property_tax / 2, 2)
    elif disbursement_type in [DisbursementType.HOMEOWNERS_INSURANCE, DisbursementType.HAZARD_INSURANCE]:
        # Insurance typically paid annually
        amount = round(annual_insurance, 2)
    elif disbursement_type == DisbursementType.FLOOD_INSURANCE:
        # Flood insurance typically paid annually
        amount = round(annual_flood_insurance, 2)
    elif disbursement_type == DisbursementType.MORTGAGE_INSURANCE:
        # Mortgage insurance might be paid annually
        amount = round(annual_mortgage_insurance, 2)
    elif disbursement_type == DisbursementType.HOA_DUES:
        # HOA dues might be paid quarterly
        amount = round(annual_hoa / 4, 2)
    else:
        # Default case
        amount = round(random.uniform(500, 2000), 2)

    # Define weights for the status enum
    # Only selecting a subset of possible status values
    status_weights = [0.1, 0.2, 0.65, 0.05, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]  # pending, processing, completed, failed

    # Use the BaseEnum.get_random method with the weights
    status = DisbursementStatus.get_random(status_weights)

    # Generate payee account number (if electronic payment)
    payment_method = random.choice(["check", "electronic transfer", "wire"])
    payee_account_number = None
    check_number = None

    if payment_method == "electronic transfer" or payment_method == "wire":
        payee_account_number = f"XX-{random.randint(10000, 99999)}"
    elif payment_method == "check":
        check_number = str(random.randint(10000, 99999))

    # Generate due date (typically before or on disbursement date)
    days_before = random.randint(7, 30)
    due_date = disbursement_date - datetime.timedelta(days=random.randint(0, days_before))

    # For insurance payments, generate coverage period
    coverage_start_date = None
    coverage_end_date = None

    if disbursement_type in [DisbursementType.HOMEOWNERS_INSURANCE, DisbursementType.HAZARD_INSURANCE,
                             DisbursementType.FLOOD_INSURANCE, DisbursementType.MORTGAGE_INSURANCE]:
        # Coverage typically starts on disbursement date or soon after
        coverage_start_date = disbursement_date + datetime.timedelta(days=random.randint(0, 15))
        # Coverage typically lasts for a year
        coverage_end_date = coverage_start_date + datetime.timedelta(days=365)

    # Create the escrow disbursement record
    disbursement = {
        "disbursement_date": disbursement_date,
        "disbursement_type": disbursement_type.value,
        "amount": amount,
        "payee_name": payee_name,
        "payee_account_number": payee_account_number,
        "check_number": check_number,
        "status": status.value,
        "due_date": due_date,
        "coverage_start_date": coverage_start_date,
        "coverage_end_date": coverage_end_date
    }

    return disbursement


def _get_servicing_account_info(servicing_account_id: Optional[int], conn) -> Optional[Dict[str, Any]]:
    """
    Get servicing account information to make disbursement data reasonable.

    Args:
        servicing_account_id: The ID of the servicing account
        conn: PostgreSQL connection object

    Returns:
        Dictionary containing servicing account information or None if not found
    """
    if not servicing_account_id:
        return None

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT mortgage_services_loan_id, original_principal_balance, current_principal_balance, 
                   escrow_balance, property_tax_due_date, homeowners_insurance_due_date
            FROM mortgage_services.servicing_accounts 
            WHERE mortgage_services_servicing_account_id = %s
        """, (servicing_account_id,))

        result = cursor.fetchone()
        cursor.close()

        return result

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching servicing account information: {error}")
        return None


def _get_property_info_from_servicing(servicing_account_info: Optional[Dict[str, Any]], conn) -> Optional[Dict[str, Any]]:
    """
    Get property information from loan data to make disbursement amounts realistic.

    Args:
        servicing_account_info: Dictionary containing servicing account info
        conn: PostgreSQL connection object

    Returns:
        Dictionary containing property information or None if not found
    """
    if not servicing_account_info or "mortgage_services_loan_id" not in servicing_account_info:
        return None

    loan_id = servicing_account_info["mortgage_services_loan_id"]

    try:
        cursor = conn.cursor()

        # First get the application ID from the loan
        cursor.execute("""
            SELECT mortgage_services_application_id
            FROM mortgage_services.loans 
            WHERE mortgage_services_loan_id = %s
        """, (loan_id,))

        result = cursor.fetchone()

        if not result:
            cursor.close()
            return None

        application_id = result.get('mortgage_services_application_id')

        # Then get the property information from the application
        cursor.execute("""
            SELECT p.mortgage_services_property_id, p.property_type, p.bedrooms, p.bathrooms,
                   p.square_feet, p.lot_size, a.estimated_property_value
            FROM mortgage_services.properties p
            JOIN mortgage_services.applications a ON p.mortgage_services_application_id = a.mortgage_services_application_id
            WHERE p.mortgage_services_application_id = %s
        """, (application_id,))

        result = cursor.fetchone()
        cursor.close()

        return result

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching property information: {error}")
        return None
