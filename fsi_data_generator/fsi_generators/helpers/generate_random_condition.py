import random
import datetime
from typing import Dict, Any, Optional
import psycopg2


def generate_random_condition(id_fields: Dict[str, Any], dg) -> Dict[str, Any]:
    """
    Generate a random mortgage services condition record with reasonable values.

    Args:
        id_fields: Dictionary containing the required ID fields (mortgage_services_application_id)
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated condition data (without ID fields)
    """
    # Get application information to make condition data reasonable
    conn = dg.conn
    application_info = get_application_info(id_fields.get("mortgage_services_application_id"), conn)

    # Define possible values for categorical fields
    condition_types = [
        "prior to approval",
        "prior to closing",
        "prior to funding",
        "post closing"
    ]

    status_options = [
        "open",
        "waived",
        "satisfied",
        "expired",
        "client conditionally approved"
    ]

    # Common mortgage conditions organized by type
    conditions_by_type = {
        "prior to approval": [
            "Verify employment history for the past two years",
            "Verify source of down payment funds",
            "Provide most recent pay stubs for all borrowers",
            "Provide bank statements for the past two months",
            "Provide tax returns for the past two years",
            "Explanation letter for recent credit inquiries",
            "Explanation letter for recent large deposits",
            "Provide government-issued photo ID for all borrowers",
            "Complete 4506-T form for tax transcript verification",
            "Verify self-employment income with additional documentation"
        ],
        "prior to closing": [
            "Property appraisal must meet or exceed purchase price",
            "Clear title search with no outstanding liens or encumbrances",
            "Verify homeowners insurance coverage",
            "Complete final verification of employment",
            "Provide proof of funds for closing costs",
            "Final credit check to verify no new debt obligations",
            "Verify all conditions from underwriting have been satisfied",
            "Complete flood zone determination",
            "HOA certification if applicable",
            "Survey or boundary determination if required"
        ],
        "prior to funding": [
            "All closing documents must be properly executed",
            "Ensure all signatures are present on loan documents",
            "Three-day right of rescission period must be completed for refinances",
            "Final title policy must be in place",
            "Escrow/closing funds must be verified as cleared",
            "Verification that no liens were filed between closing and funding",
            "All applicable riders and addendums must be signed",
            "Mortgage insurance must be in place if required",
            "Closing protection letter must be received",
            "All state-specific funding requirements must be met"
        ],
        "post closing": [
            "Record deed of trust/mortgage within statutory timeframe",
            "Send welcome package to borrower",
            "Verify all documents are imaged and stored properly",
            "Complete HMDA reporting requirements",
            "Complete mortgage servicing transfers if applicable",
            "Ensure tax service and flood service contracts are in place",
            "Complete final loan delivery to investor",
            "Resolve any trailing documentation issues",
            "Complete post-closing quality control review",
            "Ensure all fee disclosures match actual fees charged"
        ]
    }

    # Generate created date (typically within the last 90 days)
    today = datetime.datetime.now()
    days_ago = random.randint(10, 90)
    created_date = today - datetime.timedelta(days=days_ago)

    # Select condition type based on application status if available
    condition_type = random.choice(condition_types)
    if application_info and 'status' in application_info:
        app_status = application_info['status']
        if app_status == "submitted":
            condition_type = "prior to approval"
        elif app_status in ["approved", "conditionally approved"]:
            # More likely to have conditions prior to closing at this stage
            condition_type_weights = [0.2, 0.7, 0.1, 0.0]  # weights for each condition type
            condition_type = random.choices(condition_types, weights=condition_type_weights, k=1)[0]
        elif app_status == "closing":
            # More likely to have conditions prior to funding
            condition_type_weights = [0.0, 0.3, 0.6, 0.1]
            condition_type = random.choices(condition_types, weights=condition_type_weights, k=1)[0]
        elif app_status == "closed":
            # More likely to have post closing conditions
            condition_type_weights = [0.0, 0.1, 0.2, 0.7]
            condition_type = random.choices(condition_types, weights=condition_type_weights, k=1)[0]

    # Select a condition description from the appropriate list
    description = random.choice(conditions_by_type[condition_type])

    # Determine status based on condition type and creation date
    if condition_type == "prior to approval":
        if application_info and 'status' in application_info and application_info['status'] in ["approved",
                                                                                                "conditionally approved",
                                                                                                "closing", "closed"]:
            # Application is already approved, so condition is likely satisfied
            status_weights = [0.1, 0.2, 0.7, 0.0, 0.0]  # weights for each status
        else:
            # Application is not yet approved, so condition is likely still open
            status_weights = [0.8, 0.05, 0.15, 0.0, 0.0]
    elif condition_type == "prior to closing":
        if application_info and 'status' in application_info and application_info['status'] in ["closing", "closed"]:
            # Application is in closing or closed, so condition is likely satisfied
            status_weights = [0.1, 0.2, 0.7, 0.0, 0.0]
        else:
            # Not yet in closing, so condition is likely still open
            status_weights = [0.8, 0.05, 0.15, 0.0, 0.0]
    elif condition_type == "prior to funding":
        if application_info and 'status' in application_info and application_info['status'] == "closed":
            # Application is closed, so condition is likely satisfied
            status_weights = [0.1, 0.1, 0.8, 0.0, 0.0]
        else:
            # Not yet closed, so condition is likely still open
            status_weights = [0.9, 0.05, 0.05, 0.0, 0.0]
    else:  # post closing
        if days_ago < 20:
            # Recently created post-closing condition may still be open
            status_weights = [0.7, 0.1, 0.2, 0.0, 0.0]
        else:
            # Older post-closing condition likely satisfied
            status_weights = [0.3, 0.1, 0.6, 0.0, 0.0]

    status = random.choices(status_options, weights=status_weights, k=1)[0]

    # Get random associate IDs for created_by and cleared_by
    created_by = get_random_associate_id(conn)
    cleared_by = None

    # Generate due date (typically 5-30 days after created date)
    due_days = random.randint(5, 30)
    due_date = (created_date + datetime.timedelta(days=due_days)).date()

    # Generate cleared date if status is satisfied or waived
    cleared_date = None
    if status in ["satisfied", "waived"]:
        days_after_creation = min(random.randint(1, 20), (today - created_date).days)
        cleared_date = created_date + datetime.timedelta(days=days_after_creation)
        cleared_by = get_random_associate_id(conn)

    # Create the condition record
    condition = {
        "condition_type": condition_type,
        "description": description,
        "status": status,
        "created_date": created_date,
        "created_by": created_by,
        "due_date": due_date,
        "cleared_date": cleared_date,
        "cleared_by": cleared_by
    }

    return condition


def get_application_info(application_id: Optional[int], conn) -> Optional[Dict[str, Any]]:
    """
    Get application information to make condition data reasonable.

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
            SELECT status
            FROM mortgage_services.applications 
            WHERE mortgage_services_application_id = %s
        """, (application_id,))

        result = cursor.fetchone()
        cursor.close()

        if result:
            return {
                "status": result[0]
            }
        else:
            return None

    except (Exception, psycopg2.Error) as error:
        print(f"Error fetching application information: {error}")
        return None


def get_random_associate_id(conn) -> Optional[int]:
    """
    Get a random associate ID from the database.

    Args:
        conn: PostgreSQL connection object

    Returns:
        Random associate ID or None if query fails
    """
    try:
        cursor = conn.cursor()

        # First try to get associates from the department that handles mortgages
        cursor.execute("""
            SELECT enterprise_associate_id 
            FROM enterprise.associates a
            JOIN enterprise.departments d ON a.enterprise_department_id = d.enterprise_department_id
            WHERE d.department_name LIKE '%Mortgage%' OR d.department_name LIKE '%Loan%'
            ORDER BY RANDOM()
            LIMIT 1
        """)

        result = cursor.fetchone()

        # If no mortgage department associates found, get any associate
        if not result:
            cursor.execute("""
                SELECT enterprise_associate_id 
                FROM enterprise.associates
                ORDER BY RANDOM()
                LIMIT 1
            """)
            result = cursor.fetchone()

        cursor.close()

        if result:
            return result[0]
        else:
            # Return a reasonable default if no associates found
            return random.randint(1, 10)  # Assume there are at least a few associates

    except (Exception, psycopg2.Error) as error:
        print(f"Error fetching random associate ID: {error}")
        # Return a reasonable default if query fails
        return random.randint(1, 10)
