from ..enterprise.enums import CurrencyCode
from .enums import (PaymentFrequency, PaymentMethod, ScheduledPaymentStatus,
                    ScheduledPaymentType)
from .get_account import get_account
from .today import today
from data_generator import DataGenerator
from typing import Any, Dict

import datetime
import random


def generate_random_scheduled_payment(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random consumer banking scheduled payment with plausible values.

    Args:
        id_fields: Dictionary containing the required ID fields
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated scheduled payment data
    """
    # Get database connection
    conn = dg.conn

    # Validate required fields
    if 'consumer_banking_account_id' not in id_fields:
        raise ValueError("consumer_banking_account_id is required")

    # Fetch the consumer banking account to get its opened date
    cursor = conn.cursor()
    try:
        consumer_account = get_account(conn, id_fields['consumer_banking_account_id'])

        account_opened_date = consumer_account.get('opened_date')

        # Calculate days since account opened
        days_since_account_opened = (today - account_opened_date).days

        # Determine payment type using the enum
        scheduled_type = ScheduledPaymentType.get_random()

        # Determine payment method
        payment_method = PaymentMethod.get_random()

        # Determine payment status (bias toward PENDING for future payments)
        if random.random() < 0.7:  # 70% chance of PENDING for simple distribution
            payment_status = ScheduledPaymentStatus.PENDING
        else:
            payment_status = ScheduledPaymentStatus.get_random()

        # Generate payment date
        # For historical payments (non-PENDING status except for future dates)
        if payment_status not in [ScheduledPaymentStatus.PENDING, ScheduledPaymentStatus.ON_HOLD]:
            # Past payment (between account open date and today)
            days_offset = random.randint(1, max(1, days_since_account_opened - 1))
            scheduled_payment_date_time = account_opened_date + datetime.timedelta(days=days_offset)
        else:
            # Future payment (between today and next 30 days)
            days_offset = random.randint(1, 30)
            scheduled_payment_date_time = today + datetime.timedelta(days=days_offset)

        # Determine recurring payment frequency (only for RECURRING type)
        frequency = None
        end_date = None
        execution_count = None
        max_executions = None

        if scheduled_type == ScheduledPaymentType.RECURRING:
            frequency = PaymentFrequency.get_random()

            # Determine max executions (sometimes limited, sometimes open-ended)
            if random.random() < 0.6:  # 60% chance of having a max limit
                max_executions = random.randint(3, 36)

                # Calculate end date based on frequency and max executions
                if frequency == PaymentFrequency.DAILY:
                    end_date = scheduled_payment_date_time + datetime.timedelta(days=max_executions)
                elif frequency == PaymentFrequency.WEEKLY:
                    end_date = scheduled_payment_date_time + datetime.timedelta(weeks=max_executions)
                elif frequency == PaymentFrequency.BI_WEEKLY:
                    end_date = scheduled_payment_date_time + datetime.timedelta(weeks=max_executions * 2)
                elif frequency == PaymentFrequency.MONTHLY:
                    # Add months (approximate)
                    end_date = scheduled_payment_date_time + datetime.timedelta(days=max_executions * 30)
                elif frequency == PaymentFrequency.QUARTERLY:
                    end_date = scheduled_payment_date_time + datetime.timedelta(days=max_executions * 90)
                elif frequency == PaymentFrequency.SEMI_ANNUALLY:
                    end_date = scheduled_payment_date_time + datetime.timedelta(days=max_executions * 180)
                elif frequency == PaymentFrequency.ANNUALLY:
                    end_date = scheduled_payment_date_time + datetime.timedelta(days=max_executions * 365)
                else:  # CUSTOM
                    end_date = scheduled_payment_date_time + datetime.timedelta(
                        days=max_executions * random.randint(7, 60))
            else:
                # Open-ended recurring payment
                max_executions = None
                end_date = None

            # For existing recurring payments, calculate execution count so far
            if payment_status not in [ScheduledPaymentStatus.PENDING,
                                      ScheduledPaymentStatus.ON_HOLD] and scheduled_payment_date_time < today:
                days_since_first_payment = (today - scheduled_payment_date_time).days

                # Estimate execution count based on frequency
                if frequency == PaymentFrequency.DAILY:
                    execution_count = min(days_since_first_payment, max_executions if max_executions else 999)
                elif frequency == PaymentFrequency.WEEKLY:
                    execution_count = min(days_since_first_payment // 7, max_executions if max_executions else 999)
                elif frequency == PaymentFrequency.BI_WEEKLY:
                    execution_count = min(days_since_first_payment // 14, max_executions if max_executions else 999)
                elif frequency == PaymentFrequency.MONTHLY:
                    execution_count = min(days_since_first_payment // 30, max_executions if max_executions else 999)
                elif frequency == PaymentFrequency.QUARTERLY:
                    execution_count = min(days_since_first_payment // 90, max_executions if max_executions else 999)
                elif frequency == PaymentFrequency.SEMI_ANNUALLY:
                    execution_count = min(days_since_first_payment // 180, max_executions if max_executions else 999)
                elif frequency == PaymentFrequency.ANNUALLY:
                    execution_count = min(days_since_first_payment // 365, max_executions if max_executions else 999)
                else:  # CUSTOM
                    custom_interval = random.randint(7, 60)
                    execution_count = min(days_since_first_payment // custom_interval,
                                          max_executions if max_executions else 999)
            else:
                execution_count = 0

        # Generate reference number (optional - 70% chance of having one)
        reference = None
        if random.random() < 0.7:
            reference_length = random.randint(5, 15)
            reference = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=reference_length))

        # Generate debtor reference (optional - 40% chance of having one)
        debtor_reference = None
        if random.random() < 0.4:
            debtor_ref_length = random.randint(5, 15)
            debtor_reference = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=debtor_ref_length))

        # Generate payment amount (between $0.01 and $10,000)
        # Different distributions based on payment method
        if payment_method in [PaymentMethod.ACH, PaymentMethod.WIRE]:
            # Larger amounts more common for wire and ACH
            amount_ranges = [
                (0.01, 50),
                (50.01, 500),
                (500.01, 2000),
                (2000.01, 10000)
            ]
            amount_weights = [10, 30, 40, 20]
        elif payment_method == PaymentMethod.CHECK:
            # Medium amounts common for checks
            amount_ranges = [
                (0.01, 50),
                (50.01, 500),
                (500.01, 2000),
                (2000.01, 10000)
            ]
            amount_weights = [15, 45, 30, 10]
        else:
            # Smaller amounts more common for other methods
            amount_ranges = [
                (0.01, 50),
                (50.01, 500),
                (500.01, 2000),
                (2000.01, 10000)
            ]
            amount_weights = [40, 35, 20, 5]

        # Select amount range and generate random amount within that range
        selected_range = random.choices(amount_ranges, weights=amount_weights, k=1)[0]
        instructed_amount = round(random.uniform(selected_range[0], selected_range[1]), 2)

        # Choose currency (heavily biased toward account's domestic currency)
        instructed_amount_currency = CurrencyCode.USD  # Default to USD
        if random.random() < 0.02:  # 2% chance of using other currency
            instructed_amount_currency = CurrencyCode.get_random()

        # Create the scheduled payment dictionary
        scheduled_payment = {
            "consumer_banking_account_id": id_fields['consumer_banking_account_id'],
            "scheduled_payment_date_time": scheduled_payment_date_time,
            "scheduled_type": scheduled_type.value,
            "payment_method": payment_method.value,
            "payment_status": payment_status.value,
            "frequency": frequency.value if frequency else None,
            "reference": reference,
            "debtor_reference": debtor_reference,
            "instructed_amount": instructed_amount,
            "instructed_amount_currency": instructed_amount_currency.value,
            "end_date": end_date.date() if (end_date and isinstance(end_date, datetime.datetime)) else None,
            "execution_count": execution_count,
            "max_executions": max_executions
        }

        return scheduled_payment

    finally:
        cursor.close()
