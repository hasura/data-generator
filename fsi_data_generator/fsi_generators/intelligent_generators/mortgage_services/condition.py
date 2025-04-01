from .enums import ApplicationStatus, ConditionStatus, ConditionType
from typing import Any, Dict, Optional

import datetime
import logging
import psycopg2
import random

logger = logging.getLogger(__name__)


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

    # Common mortgage conditions organized by type
    conditions_by_type = {
        ConditionType.PRIOR_TO_APPROVAL.value: [
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
        ConditionType.PRIOR_TO_CLOSING.value: [
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
        ConditionType.PRIOR_TO_FUNDING.value: [
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
        ConditionType.POST_CLOSING.value: [
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
        ],
        ConditionType.PRIOR_TO_DOCS.value: [
            "Verify all outstanding documentation has been received",
            "Confirm final loan terms with borrower",
            "Prepare closing disclosure for borrower review",
            "Verify property taxes are current",
            "Verify hazard insurance is in place",
            "Ensure all legal descriptions are accurate",
            "Verify all rate lock requirements have been met",
            "Complete compliance review of loan file",
            "Secure final loan approval signatures",
            "Verify all regulatory disclosure timing requirements are met"
        ],
        ConditionType.AT_CLOSING.value: [
            "Verify borrower identity with government-issued photo ID",
            "Ensure all documents are signed in the correct locations",
            "Verify funds have been received or wired to escrow",
            "Confirm no material changes to borrower's credit profile",
            "Verify payment of all required closing costs",
            "Ensure all required property inspections are complete",
            "Verify all TILA/RESPA requirements have been met",
            "Confirm seller has signed all required transfer documents",
            "Ensure all addenda are properly executed",
            "Verify all notary requirements are met"
        ],
        ConditionType.UNDERWRITER_REQUIREMENT.value: [
            "Complete income stability analysis",
            "Analyze debt-to-income ratio against guidelines",
            "Verify credit score meets minimum requirements",
            "Complete asset sufficiency analysis",
            "Verify borrower's residency status",
            "Complete loan-to-value ratio analysis",
            "Verify property meets lender guidelines",
            "Complete borrower housing payment history analysis",
            "Analyze potential risk factors in application",
            "Verify applicant meets all underwriting criteria"
        ],
        ConditionType.AGENCY_REQUIREMENT.value: [
            "Complete Uniform Residential Loan Application (URLA)",
            "Verify all FHA/VA/USDA specific requirements",
            "Complete required government program certifications",
            "Verify property meets agency eligibility requirements",
            "Complete required government insurance applications",
            "Verify borrower meets agency eligibility criteria",
            "Complete required agency-specific forms and disclosures",
            "Verify loan amount is within agency limits",
            "Ensure property appraisal meets agency requirements",
            "Complete all required agency compliance checks"
        ],
        ConditionType.OTHER.value: [
            "Verify power of attorney if applicable",
            "Complete trust review if property held in trust",
            "Verify divorce decree terms if applicable",
            "Complete bankruptcy discharge review if applicable",
            "Verify citizenship documentation if required",
            "Complete required investor-specific documentation",
            "Verify condominium project eligibility if applicable",
            "Complete disaster area verification if property in affected area",
            "Verify all construction documentation if new construction",
            "Complete specialized property inspection requirements"
        ]
    }

    # Generate created date (typically within the last 90 days)
    today = datetime.datetime.now(datetime.timezone.utc)
    days_ago = random.randint(10, 90)
    created_date = today - datetime.timedelta(days=days_ago)

    # Select condition type based on application status if available
    condition_type = ConditionType.get_random()

    has_loan = has_loan_query_result(id_fields.get("mortgage_services_application_id"), conn)

    if application_info and 'status' in application_info:
        try:
            app_status = ApplicationStatus[application_info['status']]

            if app_status == ApplicationStatus.SUBMITTED:
                condition_type = ConditionType.PRIOR_TO_APPROVAL
            elif app_status in [ApplicationStatus.APPROVED, ApplicationStatus.CONDITIONAL_APPROVAL]:
                if not has_loan:
                    # Approved but no loan yet - focus on closing conditions
                    condition_type_weights = [0.2, 0.7, 0.1, 0.0]  # Approval, Closing, Funding, Post-closing
                    condition_types = [
                        ConditionType.PRIOR_TO_APPROVAL,
                        ConditionType.PRIOR_TO_CLOSING,
                        ConditionType.PRIOR_TO_FUNDING,
                        ConditionType.POST_CLOSING
                    ]
                    condition_type = random.choices(condition_types, weights=condition_type_weights, k=1)[0]

            if has_loan:
                # If loan exists, more likely to have conditions related to closing/funding/post-closing
                condition_type_weights = [0.0, 0.3, 0.6, 0.1]
                condition_types = [
                    ConditionType.PRIOR_TO_APPROVAL,
                    ConditionType.PRIOR_TO_CLOSING,
                    ConditionType.PRIOR_TO_FUNDING,
                    ConditionType.POST_CLOSING
                ]
                condition_type = random.choices(condition_types, weights=condition_type_weights, k=1)[0]
        except (KeyError, ValueError):
            # Handle case where status doesn't match enum
            pass

    # Select a condition description from the appropriate list
    condition_descriptions = conditions_by_type.get(condition_type.value, conditions_by_type[ConditionType.OTHER.value])
    description = random.choice(condition_descriptions)

    if condition_type == ConditionType.PRIOR_TO_APPROVAL:
        if application_info and 'status' in application_info:
            try:
                app_status = ApplicationStatus[application_info['status']]
                if app_status in [ApplicationStatus.APPROVED, ApplicationStatus.CONDITIONAL_APPROVAL]:
                    # Application is already approved, so condition is likely satisfied
                    status_weights = [0.1, 0.2, 0.1, 0.1, 0.0, 0.1, 0.0, 0.4, 0.0]  # weights for each status
                else:
                    # Application is not yet approved, so condition is likely still open
                    status_weights = [0.5, 0.3, 0.1, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0]
            except (KeyError, ValueError):
                status_weights = [0.3, 0.3, 0.1, 0.1, 0.1, 0.0, 0.0, 0.1, 0.0]
        else:
            status_weights = [0.3, 0.3, 0.1, 0.1, 0.1, 0.0, 0.0, 0.1, 0.0]
    elif condition_type == ConditionType.PRIOR_TO_CLOSING:
        if has_loan:
            # Loan exists, so condition is likely satisfied
            status_weights = [0.1, 0.2, 0.1, 0.1, 0.0, 0.1, 0.0, 0.4, 0.0]
        else:
            # No loan yet, so condition is likely still open
            status_weights = [0.5, 0.3, 0.1, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0]
    elif condition_type == ConditionType.PRIOR_TO_FUNDING:
        if has_loan and check_loan_funded(id_fields.get("mortgage_services_application_id"), conn):
            # Loan is funded, so condition is likely satisfied
            status_weights = [0.1, 0.1, 0.1, 0.1, 0.0, 0.1, 0.0, 0.5, 0.0]
        else:
            # Loan not funded or doesn't exist, so condition is likely still open
            status_weights = [0.4, 0.4, 0.1, 0.0, 0.1, 0.0, 0.0, 0.0, 0.0]
    else:  # Other condition types
        if days_ago < 20:
            # Recently created condition may still be open
            status_weights = [0.4, 0.3, 0.1, 0.1, 0.1, 0.0, 0.0, 0.0, 0.0]
        else:
            # Older condition likely processed to some extent
            status_weights = [0.2, 0.2, 0.1, 0.2, 0.1, 0.1, 0.0, 0.1, 0.0]

    status = ConditionStatus.get_random(weights=status_weights)

    # Generate due date (typically 5-30 days after created date)
    due_days = random.randint(5, 30)
    due_date = (created_date + datetime.timedelta(days=due_days)).date()

    # Generate cleared date if status is ACCEPTED, WAIVED, or CLEARED
    cleared_date = None
    if status in [ConditionStatus.ACCEPTED, ConditionStatus.WAIVED, ConditionStatus.CLEARED]:
        days_after_creation = min(random.randint(1, 20), (today - created_date).days)
        cleared_date = created_date + datetime.timedelta(days=days_after_creation)

    # Create the condition record
    condition = {
        "condition_type": condition_type.value,
        "description": description,
        "status": status.value,
        "created_date": created_date,
        "due_date": due_date,
        "cleared_date": cleared_date,
        "cleared_by_id": id_fields.get("cleared_by_id") if cleared_date else None,
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
        return result

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching application information: {error}")
        return None


def has_loan_query_result(application_id: Optional[int], conn) -> bool:
    """
    Check if an application has an associated loan.

    Args:
        application_id: The ID of the application
        conn: PostgreSQL connection object

    Returns:
        True if a loan exists for the application, False otherwise
    """
    if not application_id:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) > 0 as has_loan
            FROM mortgage_services.loans
            WHERE mortgage_services_application_id = %s
        """, (application_id,))
        result = cursor.fetchone()
        cursor.close()
        return result['has_loan'] if result else False
    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error checking for loan: {error}")
        return False


def check_loan_funded(application_id: Optional[int], conn) -> bool:
    """
    Check if a loan associated with an application has been funded.

    Args:
        application_id: The ID of the application
        conn: PostgreSQL connection object

    Returns:
        True if a funded loan exists for the application, False otherwise
    """
    if not application_id:
        return False

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT COUNT(*) > 0 as is_funded
            FROM mortgage_services.loans
            WHERE mortgage_services_application_id = %s
            AND first_payment_date IS NOT NULL
        """, (application_id,))
        result = cursor.fetchone()
        cursor.close()
        return result['is_funded'] if result else False
    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error checking loan funded status: {error}")
        return False
