import random
import datetime
from typing import Dict, Any, Optional
import psycopg2

from fsi_data_generator.fsi_generators.helpers.generate_unique_json_array import generate_unique_json_array


def generate_random_customer_communication(id_fields: Dict[str, Any], dg) -> Dict[str, Any]:
    """
    Generate a random mortgage services customer communication record with realistic values.

    Args:
        id_fields: Dictionary containing the required ID fields (mortgage_services_servicing_account_id
                   and/or mortgage_services_application_id)
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated customer communication data (without ID fields)
    """
    # Get context information based on provided IDs
    conn = dg.conn

    # Initialize fields that will be set based on available IDs
    servicing_account_info = None
    application_info = None

    # Get servicing account info if available
    if "mortgage_services_servicing_account_id" in id_fields and id_fields["mortgage_services_servicing_account_id"]:
        servicing_account_info = get_servicing_account_info(id_fields["mortgage_services_servicing_account_id"], conn)

    # Get application info if available
    if "mortgage_services_application_id" in id_fields and id_fields["mortgage_services_application_id"]:
        application_info = get_application_info(id_fields["mortgage_services_application_id"], conn)

    # Define possible values for categorical fields - ensure all are lowercase for consistency
    communication_types = [
        "email", "letter", "phone call", "text message", "in-person", "portal message", "video call"
    ]

    # Weight distribution for communication types
    type_weights = [0.35, 0.20, 0.25, 0.10, 0.05, 0.04, 0.01]

    # Select the communication type based on weights
    communication_type = random.choices(communication_types, weights=type_weights, k=1)[0]

    # Define possible direction values
    directions = ["inbound", "outbound"]

    # Outbound communications are more common
    direction = random.choices(directions, weights=[0.3, 0.7], k=1)[0]

    # Generate communication date (typically within the last year)
    today = datetime.date.today()
    days_ago = random.randint(1, 365)
    communication_date = datetime.datetime.combine(
        today - datetime.timedelta(days=days_ago),
        datetime.time(
            hour=random.randint(8, 17),
            minute=random.randint(0, 59),
            second=random.randint(0, 59)
        )
    )

    # Generate subject based on context (servicing account or application)
    subjects = []

    # Servicing related subjects
    if servicing_account_info:
        subjects.extend([
            "monthly payment reminder",
            "payment confirmation",
            "escrow analysis results",
            "interest rate change notification",
            "payment change notification",
            "late payment notice",
            "payment options",
            "statement availability",
            "loan modification inquiry",
            "insurance information update",
            "tax information update",
            "online account access",
            "autopay setup confirmation",
            "payment arrangement"
        ])

    # Application related subjects
    if application_info:
        subjects.extend([
            "application status update",
            "required documentation",
            "conditions to clear",
            "application approval",
            "application denial",
            "closing schedule",
            "rate lock confirmation",
            "appraisal ordered",
            "appraisal complete",
            "disclosure delivery",
            "loan estimate",
            "closing disclosure",
            "underwriting questions",
            "pre-approval letter",
            "verification of employment"
        ])

    # General subjects for both
    general_subjects = [
        "general inquiry",
        "contact information update",
        "address change request",
        "authorization question",
        "website help",
        "customer service feedback",
        "document request",
        "payment question",
        "account question"
    ]

    # Combine all applicable subjects
    subjects.extend(general_subjects)

    # Try to load additional subjects from DBML
    try:
        alt_subjects = generate_unique_json_array(
            dbml_string=dg.dbml,
            fully_qualified_column_name='mortgage_services.customer_communications.communication_subjects',
            count=50,
            cache_key='communication_subjects'
        )
        subjects.extend(alt_subjects)
    except:
        pass

    # Select a subject
    subject = random.choice(subjects)

    # Generate content based on subject and type
    content_intros = [
        "I wanted to inform you that",
        "I'm writing to let you know that",
        "This is regarding",
        "I'm contacting you about",
        "As requested, I'm providing information about",
        "Thank you for inquiring about",
        "We are pleased to inform you that",
        "Please be advised that",
        "We wanted to update you on",
        "As per our conversation about",
        "Following up on"
    ]

    # Try to load additional content intros from DBML
    try:
        alt_intros = generate_unique_json_array(
            dbml_string=dg.dbml,
            fully_qualified_column_name='mortgage_services.customer_communications.content_intros',
            count=50,
            cache_key='communication_content_intros'
        )
        content_intros.extend(alt_intros)
    except:
        pass

    content_details = [
        "your recent payment was processed successfully",
        "we have received your documentation",
        "your application is being reviewed by our underwriting team",
        "there has been a change to your escrow account",
        "your insurance information needs to be updated",
        "we need additional information to proceed with your request",
        "your loan modification has been approved",
        "your closing has been scheduled",
        "we've received your inquiry",
        "your payment is currently past due",
        "we need to verify some information on your account",
        "your interest rate will be adjusting",
        "we've updated your contact information as requested"
    ]

    # Try to load additional content details from DBML
    try:
        alt_details = generate_unique_json_array(
            dbml_string=dg.dbml,
            fully_qualified_column_name='mortgage_services.customer_communications.content_details',
            count=50,
            cache_key='communication_content_details'
        )
        content_details.extend(alt_details)
    except:
        pass

    content_closings = [
        "Please let us know if you have any questions.",
        "Don't hesitate to contact us with any concerns.",
        "We're here to help if you need any assistance.",
        "Thank you for choosing our services.",
        "We appreciate your business.",
        "Please respond at your earliest convenience.",
        "We look forward to hearing from you."
    ]

    # Try to load additional content closings from DBML
    try:
        alt_closings = generate_unique_json_array(
            dbml_string=dg.dbml,
            fully_qualified_column_name='mortgage_services.customer_communications.content_closings',
            count=50,
            cache_key='communication_content_closings'
        )
        content_closings.extend(alt_closings)
    except:
        pass

    # Generate full content for email/letter
    if communication_type in ["email", "letter", "portal message"]:
        content = f"{random.choice(content_intros)} {random.choice(content_details)}. {random.choice(content_closings)}"

    # Shorter content for text/phone
    elif communication_type in ["text message", "phone call", "video call"]:
        content = f"{random.choice(content_details)}. {random.choice(content_closings)}"

    # For in-person, just summarize the conversation
    else:
        content = f"In-person discussion regarding {subject}. {random.choice(content_details)}."

    # Generate sender and recipient based on direction
    common_senders = [
        "Loan Officer", "Customer Service", "Loan Servicing", "Collections Dept",
        "Escrow Department", "Loan Processing", "Mortgage Support", "Underwriting Team"
    ]

    borrower_values = ["Borrower", "Customer", "Client", "Account Holder"]

    if direction == "outbound":
        sender = random.choice(common_senders)
        recipient = random.choice(borrower_values)
    else:
        sender = random.choice(borrower_values)
        recipient = random.choice(common_senders)

    # Generate template ID if it was a system-generated communication
    template_id = None
    if direction == "outbound" and communication_type in ["email", "letter"] and random.random() < 0.7:
        template_id = f"TMPL-{random.randint(1000, 9999)}"

    # Define status options based on communication type
    if communication_type == "email":
        status_options = ["sent", "delivered", "opened", "bounced"]
        status_weights = [0.1, 0.5, 0.35, 0.05]
    elif communication_type == "letter":
        status_options = ["generated", "sent", "delivered", "returned"]
        status_weights = [0.1, 0.2, 0.65, 0.05]
    elif communication_type in ["portal message", "text message"]:
        status_options = ["sent", "delivered", "read"]
        status_weights = [0.1, 0.5, 0.4]
    else:
        status_options = ["completed"]
        status_weights = [1.0]

    status = random.choices(status_options, weights=status_weights, k=1)[0]

    # Generate document path for emails and letters
    document_path = None
    if communication_type in ["email", "letter"] and direction == "outbound":
        date_str = communication_date.strftime("%Y%m%d")
        if "mortgage_services_servicing_account_id" in id_fields:
            doc_id = id_fields["mortgage_services_servicing_account_id"]
            document_path = f"/documents/communications/servicing/{doc_id}/{date_str}_{communication_type}.pdf"
        elif "mortgage_services_application_id" in id_fields:
            doc_id = id_fields["mortgage_services_application_id"]
            document_path = f"/documents/communications/application/{doc_id}/{date_str}_{communication_type}.pdf"

    # Generate related_to (what the communication is about)
    related_to_options = []

    if servicing_account_info:
        related_to_options.extend([
            "payment", "escrow", "insurance", "taxes", "interest rate",
            "statement", "loan terms", "modification", "payoff"
        ])

    if application_info:
        related_to_options.extend([
            "application status", "documentation", "conditions", "approval",
            "closing", "rate lock", "appraisal", "disclosures", "underwriting"
        ])

    # General options for both
    related_to_options.extend([
        "general inquiry", "contact update", "complaint", "information request"
    ])

    related_to = random.choice(related_to_options)

    # Create the customer communication record
    # Ensure all fields match the mortgage_services.customer_communications table in DBML
    communication = {
        "communication_date": communication_date,
        "communication_type": communication_type,
        "direction": direction,
        "subject": subject,
        "content": content,
        "sender": sender,
        "recipient": recipient,
        "template_id": template_id,
        "status": status,
        "document_path": document_path,
        "related_to": related_to
    }

    return communication


def get_servicing_account_info(servicing_account_id: Optional[int], conn) -> Optional[Dict[str, Any]]:
    """
    Get servicing account information to make communication data reasonable.

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
            SELECT mortgage_services_loan_id, 
                   CAST(current_principal_balance AS FLOAT), 
                   CAST(current_interest_rate AS FLOAT), 
                   status,
                   next_payment_due_date
            FROM mortgage_services.servicing_accounts 
            WHERE mortgage_services_servicing_account_id = %s
        """, (servicing_account_id,))

        result = cursor.fetchone()
        cursor.close()

        if result:
            return {
                "mortgage_services_loan_id": result[0],
                "current_principal": result[1],
                "current_interest_rate": result[2],
                "status": result[3],
                "next_payment_due_date": result[4]
            }
        else:
            return None

    except (Exception, psycopg2.Error) as error:
        print(f"Error fetching servicing account information: {error}")
        return None


def get_application_info(application_id: Optional[int], conn) -> Optional[Dict[str, Any]]:
    """
    Get application information to make communication data reasonable.

    Args:
        application_id: The ID of the application
        conn: PostgreSQL connection object

    Returns:
        Dictionary containing application information or None if not found
    """
    if not application_id:
        return None

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT status, 
                   application_type, 
                   CAST(requested_loan_amount AS FLOAT), 
                   loan_purpose,
                   creation_date_time,
                   submission_date_time,
                   last_updated_date_time
            FROM mortgage_services.applications 
            WHERE mortgage_services_application_id = %s
        """, (application_id,))

        result = cursor.fetchone()
        cursor.close()

        if result:
            return {
                "status": result[0],
                "application_type": result[1],
                "requested_loan_amount": result[2],
                "loan_purpose": result[3],
                "creation_date": result[4],
                "submission_date": result[5],
                "last_updated_date": result[6]
            }
        else:
            return None

    except (Exception, psycopg2.Error) as error:
        print(f"Error fetching application information: {error}")
        return None
