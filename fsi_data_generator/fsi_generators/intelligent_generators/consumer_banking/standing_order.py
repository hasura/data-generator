from ..enterprise.enums import CurrencyCode
from ..enterprise.enums.frequency import Frequency
from .enums import (StandingOrderCategory, StandingOrderStatusCode,
                    StandingOrderType)
from data_generator import DataGenerator, SkipRowGenerationError
from datetime import datetime, timedelta
from typing import Any, Dict

import json
import random


def generate_random_standing_order(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random standing order with plausible values.

    Args:
        id_fields: Dictionary containing the required ID fields
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated standing order data
    """
    # Get database connection
    conn = dg.conn

    # Validate required fields
    if 'consumer_banking_account_id' not in id_fields:
        raise ValueError("consumer_banking_account_id is required")

    # Fetch the account to verify it exists and get additional context
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT a.consumer_banking_account_id, a.status, a.opened_date 
            FROM consumer_banking.accounts a
            WHERE a.consumer_banking_account_id = %s
        """, (id_fields['consumer_banking_account_id'],))

        account = cursor.fetchone()

        if not account:
            raise ValueError(f"No account found with ID {id_fields['consumer_banking_account_id']}")

        # Only create standing orders for active accounts
        if account.get('status') != 'ACTIVE':
            raise SkipRowGenerationError

        # account_opened_date = account.get('opened_date')

        # Select random frequency using default weights
        chosen_frequency = Frequency.get_random()

        # Select random currency (predominantly account currency, which we assume is USD as default)
        # In a real application, you would get the account's currency
        currency_options = [
            CurrencyCode.USD,
            CurrencyCode.EUR,
            CurrencyCode.GBP
        ]
        currency_weights = [70, 20, 10]  # USD is most common
        chosen_currency = random.choices(currency_options, weights=currency_weights, k=1)[0]

        # Generate a plausible payment amount
        # Standing orders are typically for regular payments like rent, mortgage, savings
        amount_ranges = {
            "small": (10, 100),  # Small payments (subscriptions, small transfers)
            "medium": (100, 1000),  # Medium payments (utility bills, insurance)
            "large": (1000, 3000)  # Large payments (rent, mortgage)
        }
        amount_weights = [20, 60, 20]  # Medium payments are most common
        amount_type = random.choices(list(amount_ranges.keys()), weights=amount_weights, k=1)[0]
        min_amount, max_amount = amount_ranges[amount_type]

        payment_amount = round(random.uniform(min_amount, max_amount), 2)

        # Generate dates
        now = datetime.now()

        # Start date is usually in the near future
        # Most standing orders start within the next 30 days
        start_date = now.date() + timedelta(days=random.randint(1, 30))

        # End date is optional - about 40% of standing orders have an end date
        end_date = None
        if random.random() < 0.4:
            # End date is typically 6 months to 5 years in the future
            end_date = start_date + timedelta(days=random.randint(180, 1825))

        # Set day of month/week based on frequency
        day_of_month = None
        day_of_week = None

        if chosen_frequency in [Frequency.MONTHLY, Frequency.QUARTERLY, Frequency.SEMI_ANNUALLY, Frequency.ANNUALLY]:
            day_of_month = random.randint(1, 28)  # Avoid 29-31 for month consistency
        elif chosen_frequency in [Frequency.WEEKLY, Frequency.BI_WEEKLY]:
            day_of_week = random.randint(1, 5)  # Mon-Fri are more common for payments

        # Next payment date based on frequency and start date
        next_payment_date = start_date
        while next_payment_date < now.date():
            # Move next payment date forward based on frequency
            if chosen_frequency == Frequency.WEEKLY:
                next_payment_date += timedelta(days=7)
            elif chosen_frequency == Frequency.BI_WEEKLY:
                next_payment_date += timedelta(days=14)
            elif chosen_frequency == Frequency.MONTHLY:
                # Simple month addition (not accounting for all edge cases in this example)
                month = next_payment_date.month + 1
                year = next_payment_date.year
                if month > 12:
                    month = 1
                    year += 1
                next_payment_date = next_payment_date.replace(year=year, month=month)
            elif chosen_frequency == Frequency.QUARTERLY:
                month = next_payment_date.month + 3
                year = next_payment_date.year
                while month > 12:
                    month -= 12
                    year += 1
                next_payment_date = next_payment_date.replace(year=year, month=month)
            elif chosen_frequency == Frequency.SEMI_ANNUALLY:
                month = next_payment_date.month + 6
                year = next_payment_date.year
                while month > 12:
                    month -= 12
                    year += 1
                next_payment_date = next_payment_date.replace(year=year, month=month)
            elif chosen_frequency == Frequency.ANNUALLY:
                next_payment_date = next_payment_date.replace(year=next_payment_date.year + 1)

        # Convert to datetime with time
        next_payment_date_time = datetime.combine(next_payment_date, datetime.min.time())

        # Last payment date is either None (if not yet made) or before next payment
        last_payment_date_time = None
        last_payment_amount = None

        # If start date is in the past, we may already have made payments
        if start_date < now.date():
            # Calculate a plausible last payment date
            last_payment_date = next_payment_date

            # Move backward one period
            if chosen_frequency == Frequency.WEEKLY:
                last_payment_date -= timedelta(days=7)
            elif chosen_frequency == Frequency.BI_WEEKLY:
                last_payment_date -= timedelta(days=14)
            elif chosen_frequency == Frequency.MONTHLY:
                # Simple month subtraction
                month = last_payment_date.month - 1
                year = last_payment_date.year
                if month < 1:
                    month = 12
                    year -= 1
                last_payment_date = last_payment_date.replace(year=year, month=month)
            elif chosen_frequency == Frequency.QUARTERLY:
                month = last_payment_date.month - 3
                year = last_payment_date.year
                while month < 1:
                    month += 12
                    year -= 1
                last_payment_date = last_payment_date.replace(year=year, month=month)
            elif chosen_frequency == Frequency.SEMI_ANNUALLY:
                month = last_payment_date.month - 6
                year = last_payment_date.year
                while month < 1:
                    month += 12
                    year -= 1
                last_payment_date = last_payment_date.replace(year=year, month=month)
            elif chosen_frequency == Frequency.ANNUALLY:
                last_payment_date = last_payment_date.replace(year=last_payment_date.year - 1)

            if last_payment_date >= start_date:  # Only set if actually had a payment
                last_payment_date_time = datetime.combine(last_payment_date, datetime.min.time())
                # Usually same as regular payment amount
                last_payment_amount = payment_amount

        # Select random status using default weights
        chosen_status = StandingOrderStatusCode.get_random()

        # Select random payment type using default weights
        chosen_payment_type = StandingOrderType.get_random()

        # Select random category using default weights
        chosen_category = StandingOrderCategory.get_random()

        # Generate reference and description
        references = {
            StandingOrderCategory.BILL_PAYMENT: ["Utility Bill", "Phone Bill", "Internet", "Insurance Premium",
                                                 "Subscription"],
            StandingOrderCategory.SAVINGS: ["Regular Savings", "Emergency Fund", "Vacation Fund", "Holiday Savings",
                                            "Future Expenses"],
            StandingOrderCategory.INVESTMENT: ["Investment Fund", "Retirement Fund", "Stock Purchase",
                                               "401k Contribution"],
            StandingOrderCategory.LOAN_PAYMENT: ["Loan Repayment", "Credit Card", "Auto Loan", "Student Loan"],
            StandingOrderCategory.RENT: ["Monthly Rent", "Housing Payment", "Property Rental", "Apartment Fee"],
            StandingOrderCategory.FAMILY_SUPPORT: ["Family Support", "Child Support", "Allowance", "Education Fees"],
            StandingOrderCategory.CHARITY: ["Charitable Donation", "Monthly Contribution", "Support Fund"]
        }

        reference_options = references.get(chosen_category, ["Regular Payment"])
        reference = random.choice(reference_options)

        # Add a random reference number sometimes
        if random.random() < 0.3:
            reference += f" #{random.randint(1000, 9999)}"

        # Description is usually more detailed than reference
        description_prefix = {
            StandingOrderCategory.BILL_PAYMENT: ["Monthly payment for ", "Regular payment to ",
                                                 "Automatic payment for "],
            StandingOrderCategory.SAVINGS: ["Transfer to ", "Savings deposit to ", "Regular contribution to "],
            StandingOrderCategory.INVESTMENT: ["Investment in ", "Contribution to ", "Regular deposit to "],
            StandingOrderCategory.LOAN_PAYMENT: ["Loan payment to ", "Regular repayment of ", "Installment for "],
            StandingOrderCategory.RENT: ["Rent payment for ", "Monthly housing payment to ",
                                         "Property rental fee for "],
            StandingOrderCategory.FAMILY_SUPPORT: ["Support payment to ", "Regular allowance for ",
                                                   "Monthly assistance for "],
            StandingOrderCategory.CHARITY: ["Donation to ", "Charitable contribution to ", "Monthly support for "]
        }

        description_options = description_prefix.get(chosen_category, ["Payment to "])
        description = random.choice(description_options) + reference

        # First and final payment amounts (usually the same as regular amount)
        first_payment_amount = payment_amount
        final_payment_amount = None

        # 15% chance of different first payment
        if random.random() < 0.15:
            # First payment might be different (setup fee, prorated amount, etc.)
            first_payment_amount = round(payment_amount * random.uniform(0.5, 1.5), 2)

        # 10% chance of different final payment
        if end_date and random.random() < 0.1:
            # Final payment might be different (remainder, cleanup amount, etc.)
            final_payment_amount = round(payment_amount * random.uniform(0.5, 1.5), 2)

        # Generate supplementary data (as JSON string)
        supplementary_data_options = [
            None,  # Often no supplementary data
            {"setupFee": round(random.uniform(5, 50), 2)},
            {"notes": "Customer requested automatic payment setup"},
            {"originalReference": f"REF{random.randint(10000, 99999)}"},
            {"relationshipManager": f"RM{random.randint(100, 999)}"}
        ]
        supplementary_data = random.choice(supplementary_data_options)
        supplementary_data_str = None
        if supplementary_data:
            supplementary_data_str = json.dumps(supplementary_data)

        # Create the standing order dictionary
        standing_order = {
            "consumer_banking_account_id": id_fields['consumer_banking_account_id'],
            "next_payment_date_time": next_payment_date_time,
            "last_payment_date_time": last_payment_date_time,
            "standing_order_status_code": chosen_status.value,
            "first_payment_amount": first_payment_amount,
            "first_payment_currency": chosen_currency.value,
            "next_payment_amount": payment_amount,
            "next_payment_currency": chosen_currency.value,
            "last_payment_amount": last_payment_amount,
            "last_payment_currency": chosen_currency.value if last_payment_amount else None,
            "final_payment_amount": final_payment_amount,
            "final_payment_currency": chosen_currency.value if final_payment_amount else None,
            "frequency": chosen_frequency.value,
            "start_date": start_date,
            "end_date": end_date,
            "day_of_month": day_of_month,
            "day_of_week": day_of_week,
            "payment_type": chosen_payment_type.value,
            "category": chosen_category.value,
            "reference": reference,
            "description": description,
            "created_date": datetime.now(),
            "created_by": random.choice(["ONLINE_BANKING", "MOBILE_APP", "BRANCH", "PHONE_BANKING"]),
            "supplementary_data": supplementary_data_str
        }

        return standing_order

    finally:
        cursor.close()
