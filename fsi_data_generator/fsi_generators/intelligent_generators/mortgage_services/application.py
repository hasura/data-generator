import datetime
import random
from typing import Any, Dict

from data_generator import DataGenerator

from .enums import (ApplicationStatus, ApplicationType, LoanPurpose,
                    SubmissionChannel)


def generate_random_application(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random mortgage application with plausible values.

    Args:
        id_fields: Dictionary containing the required ID fields
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated application data
    """
    # Get database connection
    conn = dg.conn

    # Fetch loan product using the ID from id_fields
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM mortgage_services.loan_products 
        WHERE mortgage_services_loan_product_id = %s
    """, (id_fields['mortgage_services_loan_product_id'],))

    loan_product = cursor.fetchone()
    cursor.close()

    # Generate historically consistent dates
    today = datetime.date.today()

    # Start date - typically 0-20 years ago
    years_ago = random.randint(0, 20)
    months_ago = random.randint(0, 11)
    creation_date = today.replace(year=today.year - years_ago)
    creation_date = creation_date.replace(month=((today.month - months_ago - 1) % 12) + 1)

    # Submission date is after or on creation date
    submission_days = random.randint(0, min(60, years_ago * 365))
    submission_date = creation_date + datetime.timedelta(days=submission_days)

    # Last updated date is between submission and now
    days_since_submission = (today - submission_date).days
    if days_since_submission > 0:
        update_days = random.randint(0, days_since_submission)
        last_updated_date = submission_date + datetime.timedelta(days=update_days)
    else:
        last_updated_date = submission_date

    # Generate application type
    application_type = ApplicationType.get_random()

    # Generate loan purpose
    loan_purpose = LoanPurpose.get_random()

    # Generate submission channel
    submission_channel = SubmissionChannel.get_random()

    # Generate application status
    # Higher probability of active statuses for loan products that are active
    is_product_active = loan_product.get('is_active', True)
    if is_product_active:
        status = ApplicationStatus.get_random([0.2, 0.2, 0.2, 0.1, 0.1, 0.1, 0.05, 0.03, 0.01, 0.01])
    else:
        status = ApplicationStatus.get_random([0.1, 0.1, 0.1, 0.1, 0.0, 0.1, 0.2, 0.2, 0.05, 0.05])

    # First generate the property value
    estimated_property_value = round(random.uniform(100000, 1000000), 2)

    # Then generate loan amount based on property value with a realistic LTV ratio
    max_ltv = 0.95  # Maximum loan-to-value ratio (e.g., 95%)
    min_ltv = 0.50  # Minimum loan-to-value ratio (e.g., 50%)
    ltv_ratio = random.uniform(min_ltv, max_ltv)
    requested_loan_amount = round(estimated_property_value * ltv_ratio, 2)

    # Create the application dictionary
    application = {
        "mortgage_services_loan_product_id": id_fields['mortgage_services_loan_product_id'],
        "application_type": application_type.value,
        "status": status.value,
        "loan_purpose": loan_purpose.value,
        "submission_channel": submission_channel.value,
        "creation_date_time": creation_date,
        "submission_date_time": submission_date,
        "last_updated_date_time": last_updated_date,
        "requested_loan_amount": requested_loan_amount,
        "requested_loan_term_months": random.choice([180, 240, 360]),
        "estimated_property_value": estimated_property_value,
        "estimated_credit_score": random.randint(640, 850),
        "referral_source": random.choice([
            "ONLINE_AD", "REAL_ESTATE_AGENT", "DIRECT_MAIL",
            "WALK_IN", "REFERRAL", "SOCIAL_MEDIA", "RETURNING_CUSTOMER"
        ])
    }

    return application
