import datetime
import random
from typing import Any, Dict

from data_generator import DataGenerator
from fsi_data_generator.fsi_generators.intelligent_generators.mortgage_services.enums.document_status import \
    DocumentStatus
from fsi_data_generator.fsi_generators.intelligent_generators.mortgage_services.enums.document_type import \
    DocumentType


def generate_random_document(id_fields: Dict[str, Any], _dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random mortgage services document record with reasonable values.

    Args:
        id_fields: Dictionary containing the required ID fields (mortgage_services_application_id)
        _dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated document data (without ID fields)
    """

    # Document type weights for the document types we want to generate
    # Keep original "proof of residence" as IDENTITY_VERIFICATION for now
    # Adjust weights to account for enum order
    document_type_weights = [
        0.1,  # TAX_RETURN
        0.1,  # W2
        0.12,  # PAY_STUB
        0.12,  # BANK_STATEMENT
        0.05,  # CREDIT_REPORT
        0.07,  # IDENTITY_VERIFICATION
        0.08,  # ASSET_STATEMENT
        0.05,  # PURCHASE_AGREEMENT
        0.04,  # TITLE_INSURANCE
        0.04,  # PROPERTY_APPRAISAL
        0.03,  # INSURANCE_PROOF
        0.02,  # LOAN_ESTIMATE
        0.02,  # CLOSING_DISCLOSURE
        0.01,  # LETTER_OF_EXPLANATION
        0.01,  # GIFT_LETTER
        0.01,  # SELF_EMPLOYMENT
        0.01,  # BANKRUPTCY_DISCHARGE
        0.01,  # DIVORCE_DECREE
        0.01,  # MORTGAGE_NOTE
        0.01,  # DEED
        0.01  # OTHER
    ]

    # Generate upload date (typically within the last 120 days)
    today = datetime.date.today()
    days_ago = random.randint(7, 120)
    upload_date = today - datetime.timedelta(days=days_ago)

    # Select document type using BaseEnum's get_random method
    document_type = DocumentType.get_random(weights=document_type_weights)

    # Generate document name
    if document_type == DocumentType.W2:
        tax_year = random.randint(today.year - 3, today.year - 1)
        document_name = f"W2_{tax_year}_Borrower.pdf"
    elif document_type == DocumentType.PAY_STUB:
        month = random.choice(["January", "February", "March", "April", "May", "June",
                               "July", "August", "September", "October", "November", "December"])
        document_name = f"PayStub_{month}_{today.year}.pdf"
    elif document_type == DocumentType.TAX_RETURN:
        tax_year = random.randint(today.year - 3, today.year - 1)
        document_name = f"Tax_Return_{tax_year}.pdf"
    elif document_type == DocumentType.BANK_STATEMENT:
        month = random.choice(["January", "February", "March", "April", "May", "June",
                               "July", "August", "September", "October", "November", "December"])
        bank = random.choice(["Chase", "BofA", "Wells_Fargo", "Citi", "CapitalOne", "TD_Bank"])
        document_name = f"{bank}_Statement_{month}_{today.year}.pdf"
    elif document_type == DocumentType.CREDIT_REPORT:
        bureau = random.choice(["Equifax", "Experian", "TransUnion", "TriMerge"])
        document_name = f"Credit_Report_{bureau}.pdf"
    elif document_type == DocumentType.IDENTITY_VERIFICATION:
        id_type = random.choice(["Drivers_License", "Passport", "State_ID"])
        document_name = f"{id_type}_Scan.pdf"
    else:
        # Generate a generic name for other document types
        random_number = random.randint(1000, 9999)
        document_name = f"{document_type.value.lower().replace(' ', '_')}_{random_number}.pdf"

    # Generate document path using the display name for folder structure
    application_id = id_fields.get("mortgage_services_application_id")
    document_path = f"/documents/mortgage_applications/{application_id}/{document_type.value.lower().replace(' ', '_')}/{document_name}"

    # Calculate status weights based on document age
    if days_ago < 3:
        # Very recent documents are likely still pending review
        status_weights = [
            0.9,  # PENDING
            0.1,  # REVIEWED
            0.0,  # ACCEPTED
            0.0,  # REJECTED
            0.0,  # REQUIRES_REVISION
            0.0,  # IN_REVIEW
            0.0,  # ARCHIVED
            0.0,  # EXPIRED
            0.0  # OTHER
        ]
    elif days_ago < 14:
        # Documents within the last two weeks are likely reviewed or accepted
        status_weights = [
            0.2,  # PENDING
            0.4,  # REVIEWED
            0.3,  # ACCEPTED
            0.05,  # REJECTED
            0.05,  # REQUIRES_REVISION
            0.0,  # IN_REVIEW
            0.0,  # ARCHIVED
            0.0,  # EXPIRED
            0.0  # OTHER
        ]
    else:
        # Older documents are more likely to have a final status
        status_weights = [
            0.05,  # PENDING
            0.1,  # REVIEWED
            0.7,  # ACCEPTED
            0.1,  # REJECTED
            0.05,  # REQUIRES_REVISION
            0.0,  # IN_REVIEW
            0.0,  # ARCHIVED
            0.0,  # EXPIRED
            0.0  # OTHER
        ]

    # Select status using BaseEnum's get_random method
    status = DocumentStatus.get_random(weights=status_weights)

    # Generate review date if document has been reviewed
    review_date = None
    if status in [DocumentStatus.REVIEWED, DocumentStatus.ACCEPTED,
                  DocumentStatus.REJECTED, DocumentStatus.REQUIRES_REVISION]:
        # Review typically happens 1-10 days after upload
        days_after_upload = min(random.randint(1, 10), (today - upload_date).days)
        review_date = upload_date + datetime.timedelta(days=days_after_upload)

    # Generate expiration date for certain document types
    expiration_date = None
    if document_type in [DocumentType.CREDIT_REPORT, DocumentType.LOAN_ESTIMATE]:
        expiration_days = random.randint(30, 120)
        expiration_date = upload_date + datetime.timedelta(days=expiration_days)

    # Generate notes based on status
    notes = None
    if status == DocumentStatus.REJECTED:
        rejection_reasons = [
            "Document quality too low to read",
            "Missing required information",
            "Document appears to be altered",
            "Document is outdated",
            "Wrong document submitted for requirement",
            "Document is incomplete"
        ]
        notes = random.choice(rejection_reasons)
    elif status == DocumentStatus.REQUIRES_REVISION:
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
        "document_type": document_type.value,  # Store the enum value
        "document_name": document_name,
        "document_path": document_path,
        "upload_date": upload_date,
        "status": status.value,  # Store the enum value
        "review_date": review_date,
        "expiration_date": expiration_date,
        "notes": notes
    }

    return document
