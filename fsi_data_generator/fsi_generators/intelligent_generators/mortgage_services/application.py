from .enums import (ApplicationStatus, ApplicationType, LoanPurpose,
                    SubmissionChannel)
from data_generator import DataGenerator
from dateutil.relativedelta import relativedelta
from typing import Any, Dict

import calendar
import datetime
import random


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

    # Use relativedelta for safe date arithmetic
    creation_date = today - relativedelta(years=years_ago)

    # Randomly adjust months within the same year (safer than the previous approach)
    if years_ago > 0:  # Only adjust months if we're going back at least a year
        months_ago = random.randint(0, 11)
        creation_date = creation_date - relativedelta(months=months_ago)

    # Make sure we don't have invalid day (e.g., Feb 30)
    # Get last day of the target month
    _, last_day = calendar.monthrange(creation_date.year, creation_date.month)
    creation_date = creation_date.replace(day=min(creation_date.day, last_day))

    # Submission date is after or on creation date
    max_submission_days = min(60, (today - creation_date).days)
    submission_days = random.randint(0, max_submission_days)
    submission_date = creation_date + datetime.timedelta(days=submission_days)

    # Last updated date is between submission and now
    max_update_days = (today - submission_date).days
    update_days = random.randint(0, max_update_days)
    last_updated_date = submission_date + datetime.timedelta(days=update_days)

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
