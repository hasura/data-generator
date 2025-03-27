import datetime
import logging
import random
from typing import Any, Dict, Optional

import anthropic
import psycopg2

from data_generator import DataGenerator
from fsi_data_generator.fsi_generators.helpers.generate_unique_json_array import \
    generate_unique_json_array

from .enums import AppraisalStatus, AppraisalType

logger = logging.getLogger(__name__)


def generate_random_appraisal(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random mortgage services appraisal record with reasonable values.

    Args:
        id_fields: Dictionary containing the required ID fields (mortgage_services_loan_id
                   and mortgage_services_property_id)
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated appraisal data (without ID fields)
    """
    # Get application from property and loan information
    conn = dg.conn
    property_info = _get_property_info(id_fields.get("mortgage_services_property_id"), conn)
    application_id = property_info.get("mortgage_services_application_id") if property_info else None
    application_info = _get_application_info(application_id, conn)

    # Define appraisal type weights
    appraisal_type_weights = None

    # Determine appraisal type weights based on requested loan amount if available
    if application_info and 'requested_loan_amount' in application_info and application_info['requested_loan_amount']:
        loan_amount = application_info['requested_loan_amount']
        if loan_amount < 250000:
            # Lower loan amounts might use less intensive appraisals
            appraisal_type_weights = [
                0.5,  # FULL_APPRAISAL
                0.2,  # DRIVE_BY
                0.2,  # DESKTOP
                0.05,  # BPO
                0.03,  # AVM
                0.02,  # APPRAISAL_UPDATE
                0.0,  # FIELD_REVIEW
                0.0,  # DESK_REVIEW
                0.0,  # RECERTIFICATION
                0.0,  # FHA_APPRAISAL
                0.0,  # VA_APPRAISAL
                0.0,  # USDA_APPRAISAL
                0.0  # OTHER
            ]
        else:
            # Higher loan amounts typically require full appraisals
            appraisal_type_weights = [
                0.8,  # FULL_APPRAISAL
                0.1,  # DRIVE_BY
                0.05,  # DESKTOP
                0.0,  # BPO
                0.0,  # AVM
                0.0,  # APPRAISAL_UPDATE
                0.01,  # FIELD_REVIEW
                0.01,  # DESK_REVIEW
                0.01,  # RECERTIFICATION
                0.01,  # FHA_APPRAISAL
                0.01,  # VA_APPRAISAL
                0.0,  # USDA_APPRAISAL
                0.0  # OTHER
            ]

    # Get random appraisal type using BaseEnum's get_random method
    appraisal_type = AppraisalType.get_random(weights=appraisal_type_weights)

    # Define appraiser names and companies
    appraiser_names = [
        "John Smith", "Maria Garcia", "David Johnson", "Sarah Lee",
        "Michael Brown", "Jennifer Wilson", "Robert Davis", "Lisa Miller",
        "William Rodriguez", "Elizabeth Martinez", "James Taylor", "Patricia Thomas"
    ]

    appraisal_companies = [
        "Premier Appraisal Services", "Accurate Valuations Inc", "National Appraisal Group",
        "Elite Property Assessors", "American Appraisal Associates", "Quality Valuation Services",
        "Certified Appraisal Specialists", "Metro Appraisal Company", "Allied Appraisal Network"
    ]
    try:
        appraisal_companies = appraisal_companies + generate_unique_json_array(
            dg.dbml,
            fully_qualified_column_name='mortgage_services.appraisals.appraisal_companies',
            count=50
        )
    except anthropic.APIStatusError:
        pass

    # Generate ordered date (typically within the last 180 days)
    today = datetime.date.today()
    days_ago = random.randint(30, 180)
    ordered_date = today - datetime.timedelta(days=days_ago)

    # Randomly select appraiser and company
    appraiser_name = random.choice(appraiser_names)
    appraisal_company = random.choice(appraisal_companies)

    # Generate inspection date (after ordered date)
    days_after_order = random.randint(3, 14)  # Typically 3 days to 2 weeks after ordering
    inspection_date = ordered_date + datetime.timedelta(days=days_after_order)

    # Generate completion date (after inspection date)
    days_after_inspection = random.randint(5, 14)  # Typically 5 days to 2 weeks after inspection
    completion_date = inspection_date + datetime.timedelta(days=days_after_inspection)

    # Define status weights based on dates
    # Define an appropriate mapping of statuses for appraisals

    # If the completion date would be in the future, adjust status and weights accordingly
    if completion_date > today:
        completion_date = None
        status_weights = [
            0.3,  # ORDERED
            0.4,  # ASSIGNED
            0.3,  # SCHEDULED
            0.0,  # INSPECTION_COMPLETED
            0.0,  # IN_PROGRESS
            0.0,  # SUBMITTED
            0.0,  # UNDER_REVIEW
            0.0,  # REVISION_NEEDED
            0.0,  # COMPLETED
            0.0,  # REJECTED
            0.0,  # CANCELLED
            0.0,  # EXPIRED
            0.0  # OTHER
        ]
    elif inspection_date > today:
        # After ordering but before inspection
        status_weights = [
            0.1,  # ORDERED
            0.5,  # ASSIGNED
            0.4,  # SCHEDULED
            0.0,  # INSPECTION_COMPLETED
            0.0,  # IN_PROGRESS
            0.0,  # SUBMITTED
            0.0,  # UNDER_REVIEW
            0.0,  # REVISION_NEEDED
            0.0,  # COMPLETED
            0.0,  # REJECTED
            0.0,  # CANCELLED
            0.0,  # EXPIRED
            0.0  # OTHER
        ]
    else:
        # After inspection date
        status_weights = [
            0.0,  # ORDERED
            0.0,  # ASSIGNED
            0.0,  # SCHEDULED
            0.2,  # INSPECTION_COMPLETED
            0.2,  # IN_PROGRESS
            0.1,  # SUBMITTED
            0.1,  # UNDER_REVIEW
            0.05,  # REVISION_NEEDED
            0.25,  # COMPLETED
            0.05,  # REJECTED
            0.03,  # CANCELLED
            0.02,  # EXPIRED
            0.0  # OTHER
        ]

    # Get random status using BaseEnum's get_random method
    status = AppraisalStatus.get_random(weights=status_weights)

    # Determine a realistic appraised value
    # Set default reasonable property value range
    default_min = 150000
    default_max = 800000

    # Determine a reasonable appraised value in a safe range
    if application_info:
        if 'estimated_property_value' in application_info and application_info['estimated_property_value']:
            estimated_value = application_info['estimated_property_value']
            # Ensure estimated value is within reasonable bounds before applying variation
            if 0 < estimated_value < 10000000:  # Cap at 10 million
                # Appraisal typically varies from estimate by -10% to +15%
                variation_factor = random.uniform(0.9, 1.15)
                appraised_value = round(estimated_value * variation_factor, 2)
            else:
                # Fall back to reasonable defaults if value is too high or invalid
                appraised_value = round(random.uniform(default_min, default_max), 2)
        elif 'requested_loan_amount' in application_info and application_info['requested_loan_amount']:
            loan_amount = application_info['requested_loan_amount']
            # Ensure loan amount is within reasonable bounds before calculating
            if 0 < loan_amount < 10000000:  # Cap at 10 million
                # Use requested loan amount as a basis (typically loan amount is 70-95% of property value)
                ltv_ratio = random.uniform(0.7, 0.95)  # Loan-to-value ratio
                appraised_value = round(loan_amount / ltv_ratio, 2)

                # Double-check that the calculated value is reasonable
                if appraised_value > 10000000:
                    appraised_value = round(random.uniform(default_min, default_max), 2)
            else:
                appraised_value = round(random.uniform(default_min, default_max), 2)
        else:
            # Default to a reasonable range if no other information is available
            appraised_value = round(random.uniform(default_min, default_max), 2)
    else:
        # Default to a reasonable range if no other information is available
        appraised_value = round(random.uniform(default_min, default_max), 2)

    # Set appraised value to None if status indicates it's not completed
    if status not in [AppraisalStatus.COMPLETED]:
        appraised_value = None

    # Generate a reasonable appraisal fee based on appraisal type
    if appraisal_type == AppraisalType.FULL_APPRAISAL:
        appraisal_fee = round(random.uniform(450, 800), 2)
    elif appraisal_type == AppraisalType.DRIVE_BY:
        appraisal_fee = round(random.uniform(350, 550), 2)
    elif appraisal_type == AppraisalType.DESKTOP:
        appraisal_fee = round(random.uniform(250, 400), 2)
    elif appraisal_type == AppraisalType.AVM:
        appraisal_fee = round(random.uniform(75, 200), 2)
    elif appraisal_type == AppraisalType.BPO:
        appraisal_fee = round(random.uniform(150, 300), 2)
    else:
        appraisal_fee = round(random.uniform(300, 600), 2)

    # Generate report path (only if status is completed)
    report_path = None
    if status == AppraisalStatus.COMPLETED:
        file_id = random.randint(10000, 99999)
        loan_id = id_fields.get('mortgage_services_loan_id')
        report_path = f"/documents/appraisals/{loan_id}/appraisal_{file_id}.pdf"

    # Create the appraisal record
    appraisal = {
        "appraisal_type": appraisal_type.value,
        "ordered_date": ordered_date,
        "appraiser_name": appraiser_name,
        "appraisal_company": appraisal_company,
        "inspection_date": inspection_date if status not in [AppraisalStatus.ORDERED,
                                                             AppraisalStatus.ASSIGNED] else None,
        "completion_date": completion_date if status == AppraisalStatus.COMPLETED else None,
        "appraised_value": float(appraised_value) if appraised_value is not None else None,
        "status": status.value,
        "appraisal_fee": float(appraisal_fee),
        "report_path": report_path
    }

    return appraisal


def _get_property_info(property_id: Optional[int], conn) -> Optional[Dict[str, Any]]:
    """
    Get property information including the application ID.

    Args:
        property_id: The ID of the property
        conn: PostgreSQL connection object

    Returns:
        Dictionary containing property information or None if property_id is None or property not found
    """
    if not property_id:
        return None

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT mortgage_services_application_id, property_type, occupancy_type, 
                   square_feet, year_built
            FROM mortgage_services.properties 
            WHERE mortgage_services_property_id = %s
        """, (property_id,))

        result = cursor.fetchone()
        cursor.close()
        return result

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching property information: {error}")
        return None


def _get_application_info(application_id: Optional[int], conn) -> Optional[Dict[str, Any]]:
    """
    Get application information to make appraisal data reasonable.

    Args:
        application_id: The ID of the application
        conn: PostgreSQL connection object

    Returns:
        Dictionary containing application information or None if application_id is None or application not found
    """
    if not application_id:
        return None

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT requested_loan_amount, estimated_property_value
            FROM mortgage_services.applications 
            WHERE mortgage_services_application_id = %s
        """, (application_id,))

        result = cursor.fetchone()
        cursor.close()

        if result:
            requested_loan_amount = result.get('requested_loan_amount')
            estimated_property_value = result.get('estimated_property_value')

            # Validate the values to ensure they're reasonable
            if requested_loan_amount is not None and (requested_loan_amount <= 0 or requested_loan_amount > 10000000):
                requested_loan_amount = None

            if estimated_property_value is not None and (
                    estimated_property_value <= 0 or estimated_property_value > 10000000):
                estimated_property_value = None

            return {
                "requested_loan_amount": requested_loan_amount,
                "estimated_property_value": estimated_property_value
            }
        else:
            return None

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching application information: {error}")
        return None
