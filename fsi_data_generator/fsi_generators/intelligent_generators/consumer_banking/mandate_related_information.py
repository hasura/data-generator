from ..enterprise.enums.frequency import Frequency
from .enums import DirectDebitCategory, DirectDebitClassification
from data_generator import DataGenerator
from dateutil.relativedelta import relativedelta
from typing import Any, Dict

import datetime
import random


def generate_random_mandate_related_information(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate random mandate related information for a direct debit with plausible values.

    Args:
        id_fields: Dictionary containing the required ID fields
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated mandate related information
    """
    # Get database connection
    conn = dg.conn

    # Validate required fields
    if 'consumer_banking_direct_debit_id' not in id_fields:
        raise ValueError("consumer_banking_direct_debit_id is required")

    # Fetch the direct debit to verify it exists and get its details
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT dd.consumer_banking_direct_debit_id, dd.name, dd.direct_debit_status_code, 
                   dd.previous_payment_date_time, a.opened_date
            FROM consumer_banking.direct_debits dd
            JOIN consumer_banking.accounts a ON dd.consumer_banking_account_id = a.consumer_banking_account_id
            WHERE dd.consumer_banking_direct_debit_id = %s
        """, (id_fields['consumer_banking_direct_debit_id'],))

        direct_debit = cursor.fetchone()

        if not direct_debit:
            raise ValueError(f"No direct debit found with ID {id_fields['consumer_banking_direct_debit_id']}")

        # Extract useful information from the direct debit
        direct_debit_name = direct_debit.get('name')
        previous_payment_date = direct_debit.get('previous_payment_date_time')
        account_opened_date = direct_debit.get('opened_date')
        direct_debit_status = direct_debit.get('direct_debit_status_code')

        # Generate today's date
        today = datetime.datetime.now(datetime.timezone.utc)

        # Generate a unique mandate ID (6-8 digit number)
        mandate_id = random.randint(100000, 99999999)

        # Select a classification for the mandate based on the direct debit name
        classification = DirectDebitClassification.get_random()

        # Adjust classification based on direct debit name for more realism
        direct_debit_lower = direct_debit_name.lower()
        if "insurance" in direct_debit_lower:
            classification = DirectDebitClassification.INSURANCE
        elif "mortgage" in direct_debit_lower:
            classification = DirectDebitClassification.MORTGAGE
        elif "loan" in direct_debit_lower:
            classification = DirectDebitClassification.LOAN
        elif "tax" in direct_debit_lower:
            classification = DirectDebitClassification.TAX
        elif any(word in direct_debit_lower for word in ["power", "gas", "water", "electric", "energy"]):
            classification = DirectDebitClassification.UTILITY
        elif any(word in direct_debit_lower for word in ["tv", "media", "stream", "subscription"]):
            classification = DirectDebitClassification.SUBSCRIPTION
        elif "charity" in direct_debit_lower or "foundation" in direct_debit_lower:
            classification = DirectDebitClassification.CHARITY

        # Select a category for the mandate
        category = DirectDebitCategory.get_random()

        # Adjust category based on classification and direct debit name for consistency
        if classification == DirectDebitClassification.UTILITY:
            if "power" in direct_debit_lower or "electric" in direct_debit_lower or "energy" in direct_debit_lower:
                category = DirectDebitCategory.ELECTRICITY
            elif "gas" in direct_debit_lower:
                category = DirectDebitCategory.GAS
            elif "water" in direct_debit_lower:
                category = DirectDebitCategory.WATER
        elif classification == DirectDebitClassification.SUBSCRIPTION:
            if any(word in direct_debit_lower for word in ["tv", "stream", "media"]):
                category = DirectDebitCategory.SUBSCRIPTION_MEDIA
            elif "software" in direct_debit_lower:
                category = DirectDebitCategory.SUBSCRIPTION_SOFTWARE
            else:
                category = DirectDebitCategory.SUBSCRIPTION_MEMBERSHIP
        elif classification == DirectDebitClassification.INSURANCE:
            if "home" in direct_debit_lower:
                category = DirectDebitCategory.INSURANCE_HOME
            elif "health" in direct_debit_lower:
                category = DirectDebitCategory.INSURANCE_HEALTH
            elif "life" in direct_debit_lower:
                category = DirectDebitCategory.INSURANCE_LIFE
            elif "auto" in direct_debit_lower or "car" in direct_debit_lower:
                category = DirectDebitCategory.INSURANCE_AUTO
        elif classification == DirectDebitClassification.MORTGAGE:
            category = DirectDebitCategory.MORTGAGE
        elif classification == DirectDebitClassification.LOAN:
            category = DirectDebitCategory.LOAN_PAYMENT
        elif classification == DirectDebitClassification.CHARITY:
            category = DirectDebitCategory.CHARITY

        # Generate dates for the mandate
        # First payment date: between account opened and now or in future if status is PENDING
        if previous_payment_date:
            # If there's a previous payment, first payment was before that
            days_before_previous = random.randint(28, 365)  # Typical cycle lengths
            first_payment_date_time = previous_payment_date - datetime.timedelta(days=days_before_previous)

            # Ensure it's not before the account opened
            if first_payment_date_time < account_opened_date:
                first_payment_date_time = account_opened_date + datetime.timedelta(days=random.randint(1, 30))
        else:
            # No previous payment
            if direct_debit_status == "PENDING":
                # First payment is in the future
                days_in_future = random.randint(1, 30)
                first_payment_date_time = today + datetime.timedelta(days=days_in_future)
            else:
                # First payment was in the past
                days_since_opened = (today - account_opened_date).days
                if days_since_opened <= 0:
                    days_since_opened = 1
                days_after_opening = random.randint(1, min(days_since_opened, 180))
                first_payment_date_time = account_opened_date + datetime.timedelta(days=days_after_opening)

        # Select a frequency for the mandate
        frequency_type = Frequency.get_random()

        # Calculate recurring payment date based on frequency
        if frequency_type == Frequency.MONTHLY:
            # Monthly payments typically on same day of month
            recurring_day = first_payment_date_time.day
            next_month = first_payment_date_time.month + 1
            next_year = first_payment_date_time.year

            if next_month > 12:
                next_month = 1
                next_year += 1

            recurring_payment_date_time = datetime.datetime(
                next_year, next_month, min(recurring_day, 28),
                first_payment_date_time.hour, first_payment_date_time.minute,
                first_payment_date_time.second, tzinfo=first_payment_date_time.tzinfo
            )
        elif frequency_type == Frequency.WEEKLY:
            recurring_payment_date_time = first_payment_date_time + datetime.timedelta(days=7)
        elif frequency_type == Frequency.BI_WEEKLY:
            recurring_payment_date_time = first_payment_date_time + datetime.timedelta(days=14)
        elif frequency_type == Frequency.QUARTERLY:
            # 3 months later
            months_ahead = 3
            new_month = ((first_payment_date_time.month - 1 + months_ahead) % 12) + 1
            years_ahead = (first_payment_date_time.month - 1 + months_ahead) // 12
            recurring_payment_date_time = datetime.datetime(
                first_payment_date_time.year + years_ahead, new_month, min(first_payment_date_time.day, 28),
                first_payment_date_time.hour, first_payment_date_time.minute,
                first_payment_date_time.second, tzinfo=first_payment_date_time.tzinfo
            )
        elif frequency_type == Frequency.SEMI_ANNUALLY:
            # 6 months later
            months_ahead = 6
            first_payment_date_time = datetime.datetime(2023, 1, 31, 10, 0)  # January 31st, 2023
            recurring_payment_date_time = first_payment_date_time + relativedelta(months=months_ahead)
        elif frequency_type == Frequency.ANNUALLY:
            # 1 year later
            first_payment_date_time = datetime.datetime(2023, 2, 28, 15, 30)  # Example: February 28th, 2023
            recurring_payment_date_time = first_payment_date_time + relativedelta(years=1)
        elif frequency_type == Frequency.DAILY:
            recurring_payment_date_time = first_payment_date_time + datetime.timedelta(days=1)
        elif frequency_type == Frequency.SEMI_MONTHLY:
            first_payment_date_time = datetime.datetime(2023, 1, 31, 10, 0)  # January 31st, 2023
            if first_payment_date_time.day < 15:
                recurring_payment_date_time = first_payment_date_time.replace(day=15)
            else:
                recurring_payment_date_time = (first_payment_date_time.replace(day=1) + relativedelta(months=1))
        else:
            # For irregular, one-time, and custom frequencies
            if frequency_type == Frequency.ONE_TIME:
                recurring_payment_date_time = None
                # final_payment_date_time = first_payment_date_time
            else:
                # For irregular and custom, just set a plausible next date
                days_ahead = random.randint(14, 90)
                recurring_payment_date_time = first_payment_date_time + datetime.timedelta(days=days_ahead)

        # Generate final payment date (optional - 60% chance)
        final_payment_date_time = None
        if frequency_type != Frequency.ONE_TIME and random.random() < 0.6:
            # For recurring mandates, final payment is typically 6-60 months in the future
            months_ahead = random.randint(6, 60)
            years_ahead = months_ahead // 12
            months_remainder = months_ahead % 12

            new_month = ((first_payment_date_time.month - 1 + months_remainder) % 12) + 1
            new_year = first_payment_date_time.year + years_ahead + (
                    (first_payment_date_time.month - 1 + months_remainder) // 12)

            final_payment_date_time = datetime.datetime(
                new_year, new_month, min(first_payment_date_time.day, 28),
                first_payment_date_time.hour, first_payment_date_time.minute,
                first_payment_date_time.second, tzinfo=first_payment_date_time.tzinfo
            )

        # Generate frequency count per period (optional - 20% chance)
        frequency_count_per_period = None
        if random.random() < 0.2:
            if frequency_type == Frequency.MONTHLY:
                frequency_count_per_period = 1
            elif frequency_type == Frequency.QUARTERLY:
                frequency_count_per_period = 3
            elif frequency_type == Frequency.SEMI_ANNUALLY:
                frequency_count_per_period = 6
            elif frequency_type == Frequency.ANNUALLY:
                frequency_count_per_period = 12
            elif frequency_type == Frequency.WEEKLY:
                frequency_count_per_period = random.choice([4, 5])  # Weeks per month
            elif frequency_type == Frequency.BI_WEEKLY:
                frequency_count_per_period = random.choice([2, 3])  # Bi-weekly per month
            elif frequency_type == Frequency.DAILY:
                frequency_count_per_period = random.choice([28, 30, 31])  # Days per month
            elif frequency_type == Frequency.SEMI_MONTHLY:
                frequency_count_per_period = 2  # Twice per month

        # Generate frequency point in time (optional - 40% chance)
        frequency_point_in_time = None
        if random.random() < 0.4 and frequency_type in [Frequency.MONTHLY, Frequency.QUARTERLY,
                                                        Frequency.SEMI_ANNUALLY,
                                                        Frequency.ANNUALLY]:
            # For monthly-based frequencies, typically a specific day of month
            frequency_point_in_time = str(min(first_payment_date_time.day, 28))

        # Generate reason for the mandate (optional - 70% chance)
        reason = None
        if random.random() < 0.7:
            if classification == DirectDebitClassification.UTILITY:
                reasons = [
                    "Payment for utility services",
                    f"Monthly {category.value.lower().replace('_', ' ')} service",
                    f"Regular payment for {category.value.lower().replace('_', ' ')}"
                ]
            elif classification == DirectDebitClassification.SUBSCRIPTION:
                reasons = [
                    "Subscription payment",
                    f"Regular {category.value.lower().replace('_', ' ')} subscription",
                    f"Payment for {direct_debit_name} services"
                ]
            elif classification == DirectDebitClassification.MORTGAGE:
                reasons = [
                    "Mortgage payment",
                    "Home loan repayment",
                    "Property financing"
                ]
            elif classification == DirectDebitClassification.INSURANCE:
                insurance_type = category.value.split('_')[-1].lower() if '_' in category.value else ''
                reasons = [
                    f"{insurance_type.capitalize() if insurance_type else 'Insurance'} premium payment",
                    f"Regular {insurance_type if insurance_type else 'insurance'} payment",
                    f"{direct_debit_name} insurance premium"
                ]
            elif classification == DirectDebitClassification.CHARITY:
                reasons = [
                    "Regular charitable donation",
                    "Monthly support donation",
                    f"Regular contribution to {direct_debit_name}"
                ]
            else:
                reasons = [
                    f"Payment to {direct_debit_name}",
                    "Regular payment",
                    f"Authorized payment for {classification.value.lower()} services"
                ]

            reason = random.choice(reasons)

        # Create the mandate related information dictionary
        mandate = {
            "consumer_banking_direct_debit_id": id_fields['consumer_banking_direct_debit_id'],
            "mandate_id": mandate_id,
            "classification": classification.value,
            "category": category.value,
            "first_payment_date_time": first_payment_date_time,
            "recurring_payment_date_time": recurring_payment_date_time,
            "final_payment_date_time": final_payment_date_time,
            "frequency_type": frequency_type.value,
            "frequency_count_per_period": frequency_count_per_period,
            "frequency_point_in_time": frequency_point_in_time,
            "reason": reason
        }

        return mandate

    finally:
        cursor.close()
