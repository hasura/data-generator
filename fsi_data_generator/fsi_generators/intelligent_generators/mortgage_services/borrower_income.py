import datetime
import random
from typing import Any, Dict

from fsi_data_generator.fsi_generators.intelligent_generators.mortgage_services.employment import \
    _get_application_info_for_borrower
from fsi_data_generator.fsi_generators.intelligent_generators.mortgage_services.enums.application_status import \
    ApplicationStatus
from fsi_data_generator.fsi_generators.intelligent_generators.mortgage_services.enums.income_frequency import \
    IncomeFrequency
from fsi_data_generator.fsi_generators.intelligent_generators.mortgage_services.enums.income_type import \
    IncomeType
from fsi_data_generator.fsi_generators.intelligent_generators.mortgage_services.enums.verification_status import \
    VerificationStatus


def generate_random_borrower_income(id_fields: Dict[str, Any], dg) -> Dict[str, Any]:
    """
    Generate a random mortgage services borrower income record with reasonable values.

    Args:
        id_fields: Dictionary containing the required ID fields (mortgage_services_borrower_id)
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated borrower income data (without ID fields)
    """
    # Get borrower information and application status to make income data reasonable
    conn = dg.conn
    application_info = _get_application_info_for_borrower(id_fields.get("mortgage_services_borrower_id"), conn)

    # Select income type using weighted random choice
    income_type = IncomeType.get_random()

    # Generate income amount based on type
    if income_type == IncomeType.SALARY:
        # Monthly salary typically between $3,000 and $12,000
        amount = round(random.uniform(3000, 12000), 2)
        frequency = IncomeFrequency.MONTHLY
    elif income_type == IncomeType.BONUS:
        # Annual bonus typically between $2,000 and $30,000
        amount = round(random.uniform(2000, 30000), 2)
        frequency = IncomeFrequency.ANNUALLY
    elif income_type == IncomeType.COMMISSION:
        # Commission can be monthly or quarterly
        amount = round(random.uniform(1000, 15000), 2)
        frequency = random.choices([IncomeFrequency.MONTHLY, IncomeFrequency.QUARTERLY], weights=[0.7, 0.3], k=1)[0]
    elif income_type == IncomeType.OVERTIME:
        # Overtime typically bi-weekly or monthly
        amount = round(random.uniform(500, 3000), 2)
        frequency = random.choices([IncomeFrequency.BI_WEEKLY, IncomeFrequency.MONTHLY], weights=[0.6, 0.4], k=1)[0]
    elif income_type == IncomeType.SELF_EMPLOYMENT:
        # Self-employment typically monthly
        amount = round(random.uniform(3000, 20000), 2)
        frequency = IncomeFrequency.MONTHLY
    elif income_type == IncomeType.RENTAL:
        # Rental income typically monthly
        amount = round(random.uniform(1000, 5000), 2)
        frequency = IncomeFrequency.MONTHLY
    elif income_type == IncomeType.INVESTMENT:
        # Investment income typically quarterly or annually
        amount = round(random.uniform(1000, 20000), 2)
        frequency = random.choices([IncomeFrequency.QUARTERLY, IncomeFrequency.SEMI_ANNUALLY, IncomeFrequency.ANNUALLY],
                                   weights=[0.4, 0.3, 0.3], k=1)[0]
    elif income_type in [IncomeType.RETIREMENT, IncomeType.PENSION, IncomeType.SOCIAL_SECURITY]:
        # Retirement income typically monthly
        amount = round(random.uniform(1500, 4000), 2)
        frequency = IncomeFrequency.MONTHLY
    elif income_type == IncomeType.DISABILITY:
        # Disability income typically monthly
        amount = round(random.uniform(1000, 3000), 2)
        frequency = IncomeFrequency.MONTHLY
    elif income_type in [IncomeType.ALIMONY, IncomeType.CHILD_SUPPORT]:
        # Support payments typically monthly
        amount = round(random.uniform(500, 3000), 2)
        frequency = IncomeFrequency.MONTHLY
    elif income_type == IncomeType.TRUST:
        # Trust income typically monthly or quarterly
        amount = round(random.uniform(2000, 15000), 2)
        frequency = random.choices([IncomeFrequency.MONTHLY, IncomeFrequency.QUARTERLY], weights=[0.6, 0.4], k=1)[0]
    elif income_type == IncomeType.GOVERNMENT_ASSISTANCE:
        # Government assistance typically monthly
        amount = round(random.uniform(800, 2000), 2)
        frequency = IncomeFrequency.MONTHLY
    elif income_type == IncomeType.ROYALTIES:
        # Royalties typically quarterly or semi-annually
        amount = round(random.uniform(500, 10000), 2)
        frequency = random.choices([IncomeFrequency.QUARTERLY, IncomeFrequency.SEMI_ANNUALLY], weights=[0.6, 0.4], k=1)[
            0]
    else:  # OTHER
        # Other income with random frequency
        amount = round(random.uniform(500, 5000), 2)
        frequency = IncomeFrequency.get_random()

    # Initialize verification date
    verification_date = None

    # Determine verification status based on application status
    if application_info and 'status' in application_info:
        app_status = ApplicationStatus[application_info['status']]
        today = datetime.date.today()

        if app_status in [ApplicationStatus.APPROVED, ApplicationStatus.CONDITIONAL_APPROVAL]:
            # For approved applications, incomes are usually verified
            verification_status = VerificationStatus.get_random([0.8, 0.0, 0.0, 0.1, 0.1])

            if verification_status == VerificationStatus.VERIFIED:
                # Set verification date to 1-30 days before today
                days_ago = random.randint(1, 30)
                verification_date = today - datetime.timedelta(days=days_ago)

        elif app_status in [ApplicationStatus.SUBMITTED, ApplicationStatus.IN_REVIEW]:
            # For in-process applications, verification could be pending or completed
            verification_status = VerificationStatus.get_random([0.3, 0.6, 0.0, 0.1, 0.0])

            if verification_status == VerificationStatus.VERIFIED:
                days_ago = random.randint(1, 15)
                verification_date = today - datetime.timedelta(days=days_ago)

        elif app_status == ApplicationStatus.DENIED:
            # Denied applications might have failed verification
            verification_status = VerificationStatus.get_random([0.2, 0.1, 0.4, 0.3, 0.0])

            if verification_status in [VerificationStatus.VERIFIED, VerificationStatus.FAILED]:
                days_ago = random.randint(1, 30)
                verification_date = today - datetime.timedelta(days=days_ago)

        else:  # draft or other status
            # For draft applications, often no verification yet
            verification_status = VerificationStatus.get_random([0.05, 0.15, 0.0, 0.8, 0.0])

            if verification_status == VerificationStatus.VERIFIED:
                days_ago = random.randint(1, 15)
                verification_date = today - datetime.timedelta(days=days_ago)
    else:
        # If no application info, use default verification distribution
        verification_status = VerificationStatus.get_random([0.2, 0.2, 0.1, 0.5, 0.0, 0.0])

        if verification_status not in [VerificationStatus.UNVERIFIED, VerificationStatus.PENDING]:
            days_ago = random.randint(1, 30)
            verification_date = datetime.date.today() - datetime.timedelta(days=days_ago)

    # Create the borrower income record
    borrower_income = {
        "income_type": income_type.value,  # Convert enum to string for DB storage
        "amount": float(amount),
        "frequency": frequency.value,  # Convert enum to string for DB storage
        "verification_status": verification_status.value,  # Convert enum to string for DB storage
        "verification_date": verification_date
    }

    return borrower_income
