import random
import datetime
from typing import Dict, Any, Optional
import psycopg2

from data_generator import DataGenerator


def generate_random_appraisal(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random mortgage services appraisal record with reasonable values.

    Args:
        id_fields: Dictionary containing the required ID fields (mortgage_services_loan_id
                   and mortgage_services_property_id)
        dg: DataGenertor instance

    Returns:
        Dictionary containing randomly generated appraisal data (without ID fields)
    """
    # Get application from property and loan information
    conn = dg.conn
    property_info = get_property_info(id_fields.get("mortgage_services_property_id"), conn)
    application_id = property_info.get("mortgage_services_application_id") if property_info else None
    application_info = get_application_info(application_id, conn)

    # Define possible values for categorical fields - using lowercase for enum-like fields
    appraisal_types = [
        "full appraisal", "drive-by appraisal", "desktop appraisal",
        "automated valuation model", "broker price opinion", "streamlined appraisal"
    ]

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

    status_options = [
        "ordered", "scheduled", "inspection complete", "in review", "completed", "rejected"
    ]

    # Generate ordered date (typically within the last 180 days)
    today = datetime.date.today()
    days_ago = random.randint(30, 180)
    ordered_date = today - datetime.timedelta(days=days_ago)

    # Determine appraisal type based on requested loan amount if available
    if application_info and 'requested_loan_amount' in application_info and application_info['requested_loan_amount']:
        loan_amount = application_info['requested_loan_amount']
        if loan_amount < 250000:
            # Lower loan amounts might use less intensive appraisals
            appraisal_type_weights = [0.5, 0.2, 0.2, 0.05, 0.03, 0.02]
        else:
            # Higher loan amounts typically require full appraisals
            appraisal_type_weights = [0.8, 0.1, 0.05, 0.02, 0.02, 0.01]
    else:
        appraisal_type_weights = [0.7, 0.1, 0.1, 0.03, 0.05, 0.02]

    appraisal_type = random.choices(appraisal_types, weights=appraisal_type_weights, k=1)[0]

    # Randomly select appraiser and company
    appraiser_name = random.choice(appraiser_names)
    appraisal_company = random.choice(appraisal_companies)

    # Generate inspection date (after ordered date)
    days_after_order = random.randint(3, 14)  # Typically 3 days to 2 weeks after ordering
    inspection_date = ordered_date + datetime.timedelta(days=days_after_order)

    # Generate completion date (after inspection date)
    days_after_inspection = random.randint(5, 14)  # Typically 5 days to 2 weeks after inspection
    completion_date = inspection_date + datetime.timedelta(days=days_after_inspection)

    # If the completion date would be in the future, adjust status accordingly
    if completion_date > today:
        completion_date = None
        status_options = ["ordered", "scheduled", "inspection complete", "in review"]

    status = random.choice(status_options)

    # Determine a realistic appraised value
    # Set default reasonable property value range
    default_min = 150000
    default_max = 800000

    # Determine a reasonable appraised value in a safe range
    if application_info:
        if 'estimated_property_value' in application_info and application_info['estimated_property_value']:
            estimated_value = application_info['estimated_property_value']
            # Ensure estimated value is within reasonable bounds before applying variation
            if estimated_value > 0 and estimated_value < 10000000:  # Cap at 10 million
                # Appraisal typically varies from estimate by -10% to +15%
                variation_factor = random.uniform(0.9, 1.15)
                appraised_value = round(estimated_value * variation_factor, 2)
            else:
                # Fall back to reasonable defaults if value is too high or invalid
                appraised_value = round(random.uniform(default_min, default_max), 2)
        elif 'requested_loan_amount' in application_info and application_info['requested_loan_amount']:
            loan_amount = application_info['requested_loan_amount']
            # Ensure loan amount is within reasonable bounds before calculating
            if loan_amount > 0 and loan_amount < 10000000:  # Cap at 10 million
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
    if status in ["ordered", "scheduled", "inspection complete", "in review"]:
        appraised_value = None

    # Generate a reasonable appraisal fee
    if appraisal_type == "full appraisal":
        appraisal_fee = round(random.uniform(450, 800), 2)
    elif appraisal_type == "drive-by appraisal":
        appraisal_fee = round(random.uniform(350, 550), 2)
    elif appraisal_type == "desktop appraisal":
        appraisal_fee = round(random.uniform(250, 400), 2)
    elif appraisal_type == "automated valuation model":
        appraisal_fee = round(random.uniform(75, 200), 2)
    else:
        appraisal_fee = round(random.uniform(300, 600), 2)

    # Generate report path (only if status is completed)
    report_path = None
    if status == "completed":
        file_id = random.randint(10000, 99999)
        loan_id = id_fields.get('mortgage_services_loan_id')
        report_path = f"/documents/appraisals/{loan_id}/appraisal_{file_id}.pdf"

    # Create the appraisal record
    appraisal = {
        "appraisal_type": appraisal_type,
        "ordered_date": ordered_date,
        "appraiser_name": appraiser_name,
        "appraisal_company": appraisal_company,
        "inspection_date": inspection_date if status != "ordered" else None,
        "completion_date": completion_date if status == "completed" else None,
        "appraised_value": float(appraised_value) if appraised_value is not None else None,
        "status": status,
        "appraisal_fee": float(appraisal_fee),
        "report_path": report_path
    }

    return appraisal


def get_property_info(property_id: Optional[int], conn) -> Optional[Dict[str, Any]]:
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

        if result:
            return {
                "mortgage_services_application_id": result[0],
                "property_type": result[1],
                "occupancy_type": result[2],
                "square_feet": float(result[3]) if result[3] is not None else None,
                "year_built": result[4]
            }
        else:
            return None

    except (Exception, psycopg2.Error) as error:
        print(f"Error fetching property information: {error}")
        return None


def get_application_info(application_id: Optional[int], conn) -> Optional[Dict[str, Any]]:
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
            requested_loan_amount = float(result[0]) if result[0] is not None else None
            estimated_property_value = float(result[1]) if result[1] is not None else None

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
        print(f"Error fetching application information: {error}")
        return None
