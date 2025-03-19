import random
import datetime
from typing import Dict, Any, Optional
import psycopg2


def generate_random_document(id_fields: Dict[str, Any], dg) -> Dict[str, Any]:
    """
    Generate a random mortgage services document record with reasonable values.

    Args:
        id_fields: Dictionary containing the required ID fields (mortgage_services_application_id)
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated document data (without ID fields)
    """
    # Get application information to make document data reasonable
    conn = dg.conn

    status_options = [
        "pending review", "reviewed", "accepted", "rejected", "expired", "needs clarification"
    ]

    # Document type probabilities - more common document types should have higher weights
    document_type_weights = {
        "w2": 0.1,
        "pay stub": 0.12,
        "tax return": 0.1,
        "bank statement": 0.12,
        "credit report": 0.05,
        "identity document": 0.07,
        "proof of residence": 0.06,
        "asset statement": 0.08,
        "income verification": 0.07,
        "purchase agreement": 0.05,
        "title report": 0.04,
        "appraisal report": 0.04,
        "insurance declaration": 0.03,
        "loan estimate": 0.02,
        "closing disclosure": 0.02,
        "settlement statement": 0.01,
        "loan application": 0.02
    }

    # Generate upload date (typically within the last 120 days)
    today = datetime.date.today()
    days_ago = random.randint(7, 120)
    upload_date = today - datetime.timedelta(days=days_ago)

    # Select document type based on weights
    document_type = random.choices(
        list(document_type_weights.keys()),
        weights=list(document_type_weights.values()),
        k=1
    )[0]

    # Generate document name
    if document_type == "w2":
        tax_year = random.randint(today.year - 3, today.year - 1)
        document_name = f"W2_{tax_year}_Borrower.pdf"
    elif document_type == "pay stub":
        month = random.choice(["January", "February", "March", "April", "May", "June",
                              "July", "August", "September", "October", "November", "December"])
        document_name = f"PayStub_{month}_{today.year}.pdf"
    elif document_type == "tax return":
        tax_year = random.randint(today.year - 3, today.year - 1)
        document_name = f"Tax_Return_{tax_year}.pdf"
    elif document_type == "bank statement":
        month = random.choice(["January", "February", "March", "April", "May", "June",
                              "July", "August", "September", "October", "November", "December"])
        bank = random.choice(["Chase", "BofA", "Wells_Fargo", "Citi", "CapitalOne", "TD_Bank"])
        document_name = f"{bank}_Statement_{month}_{today.year}.pdf"
    elif document_type == "credit report":
        bureau = random.choice(["Equifax", "Experian", "TransUnion", "TriMerge"])
        document_name = f"Credit_Report_{bureau}.pdf"
    elif document_type == "identity document":
        id_type = random.choice(["Drivers_License", "Passport", "State_ID"])
        document_name = f"{id_type}_Scan.pdf"
    elif document_type == "proof of residence":
        proof_type = random.choice(["Utility_Bill", "Lease_Agreement", "Mortgage_Statement"])
        document_name = f"{proof_type}_Proof_of_Residence.pdf"
    else:
        # Generate a generic name for other document types
        random_number = random.randint(1000, 9999)
        document_name = f"{document_type.replace(' ', '_')}_{random_number}.pdf"

    # Generate document path
    application_id = id_fields.get("mortgage_services_application_id")
    document_path = f"/documents/mortgage_applications/{application_id}/{document_type.replace(' ', '_')}/{document_name}"

    # Determine status based on document type and upload date
    if days_ago < 3:
        # Very recent documents are likely still pending review
        status_weights = [0.9, 0.1, 0.0, 0.0, 0.0, 0.0]  # weights for each status
    elif days_ago < 14:
        # Documents within the last two weeks are likely reviewed or accepted
        status_weights = [0.2, 0.4, 0.3, 0.05, 0.0, 0.05]
    else:
        # Older documents are more likely to have a final status
        status_weights = [0.05, 0.1, 0.7, 0.1, 0.0, 0.05]

    status = random.choices(status_options, weights=status_weights, k=1)[0]

    # Generate review date if document has been reviewed
    review_date = None
    if status in ["reviewed", "accepted", "rejected", "needs clarification"]:
        # Review typically happens 1-10 days after upload
        days_after_upload = min(random.randint(1, 10), (today - upload_date).days)
        review_date = upload_date + datetime.timedelta(days=days_after_upload)

    # Get random associate ID for reviewer
    reviewer_id = None
    if review_date:
        reviewer_id = get_random_associate_id(conn)

    # Generate expiration date for certain document types
    expiration_date = None
    if document_type in ["credit report", "pre-approval letter", "loan estimate"]:
        expiration_days = random.randint(30, 120)
        expiration_date = upload_date + datetime.timedelta(days=expiration_days)

    # Generate notes based on status
    notes = None
    if status == "rejected":
        rejection_reasons = [
            "Document quality too low to read",
            "Missing required information",
            "Document appears to be altered",
            "Document is outdated",
            "Wrong document submitted for requirement",
            "Document is incomplete"
        ]
        notes = random.choice(rejection_reasons)
    elif status == "needs clarification":
        clarification_reasons = [
            "Please provide all pages of the document",
            "Need statement with account number visible",
            "Additional signatures required",
            "Need most recent version of this document",
            "Please explain large deposit on page 2"
        ]
        notes = random.choice(clarification_reasons)

    # Create the document record
    document = {
        "document_type": document_type,
        "document_name": document_name,
        "document_path": document_path,
        "upload_date": upload_date,
        "status": status,
        "review_date": review_date,
        "reviewer_id": reviewer_id,
        "expiration_date": expiration_date,
        "notes": notes
    }

    return document


def get_application_info(application_id: Optional[int], conn) -> Optional[Dict[str, Any]]:
    """
    Get application information to make document data reasonable.

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
            SELECT status, submission_date_time
            FROM mortgage_services.applications 
            WHERE mortgage_services_application_id = %s
        """, (application_id,))

        result = cursor.fetchone()
        cursor.close()

        if result:
            return {
                "status": result[0],
                "submission_date": result[1].date() if result[1] else None
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
