from .enums import DirectDebitStatusCode
from .get_account import get_account
from .today import today
from data_generator import DataGenerator
from typing import Any, Dict

import datetime
import random


def generate_random_direct_debit(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random consumer banking direct debit with plausible values.

    Args:
        id_fields: Dictionary containing the required ID fields
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated direct debit data
    """
    # Get database connection
    conn = dg.conn

    # Validate required fields
    if 'consumer_banking_account_id' not in id_fields:
        raise ValueError("consumer_banking_account_id is required")

    # Fetch the consumer banking account to verify it exists and get its opened date
    cursor = conn.cursor()
    try:

        consumer_account = get_account(conn, id_fields['consumer_banking_account_id'])

        account_opened_date = consumer_account.get('opened_date')

        # Calculate days since account opened
        days_since_account_opened = (today - account_opened_date).days

        # Generate merchant/organization name
        merchant_types = [
            "Utility", "Telecom", "Insurance", "Mortgage", "Loan", "Subscription",
            "Charity", "Gym", "Membership", "Publishing", "Education", "Healthcare"
        ]
        merchant_names = [
            "National", "City", "Metro", "United", "Central", "Premier", "Royal",
            "Global", "First", "Pacific", "Atlantic", "Eastern", "Western", "Digital"
        ]
        merchant_suffixes = [
            "Power", "Gas", "Water", "Communications", "Mobile", "Broadband", "Insurance",
            "Bank", "Finance", "Services", "Media", "Healthcare", "Fitness", "Association"
        ]

        selected_type = random.choice(merchant_types)
        selected_name = random.choice(merchant_names)
        selected_suffix = random.choice(merchant_suffixes)

        # Ensure the combination makes sense (e.g., "National Power" for utilities)
        if selected_type == "Utility" and selected_suffix not in ["Power", "Gas", "Water"]:
            selected_suffix = random.choice(["Power", "Gas", "Water"])
        elif selected_type == "Telecom" and selected_suffix not in ["Communications", "Mobile", "Broadband"]:
            selected_suffix = random.choice(["Communications", "Mobile", "Broadband"])
        elif selected_type == "Insurance" and selected_suffix != "Insurance":
            selected_suffix = "Insurance"

        name = f"{selected_name} {selected_suffix}"

        # Determine direct debit status using the enum
        status = DirectDebitStatusCode.get_random()

        # Generate previous payment details (if applicable)
        # 80% chance of having previous payment data if account is old enough
        previous_payment_date_time = None
        previous_payment_amount = None
        previous_payment_currency = None

        if days_since_account_opened > 30 and random.random() < 0.8:
            # Previous payment was between account opened date and today
            # But more weighted towards recent dates
            days_since_opened = min(days_since_account_opened, 365)  # Cap at 1 year for typical cycle
            days_back = random.choices(
                range(1, days_since_opened + 1),
                weights=[1 / (i + 1) for i in range(days_since_opened)],  # Higher weight for recent days
                k=1
            )[0]

            previous_payment_date_time = today - datetime.timedelta(days=days_back)

            # Generate a plausible amount based on the type of merchant
            if selected_type == "Utility":
                previous_payment_amount = round(random.uniform(30, 250), 2)
            elif selected_type == "Telecom":
                previous_payment_amount = round(random.uniform(20, 150), 2)
            elif selected_type == "Insurance":
                previous_payment_amount = round(random.uniform(50, 500), 2)
            elif selected_type == "Mortgage":
                previous_payment_amount = round(random.uniform(500, 2500), 2)
            elif selected_type == "Loan":
                previous_payment_amount = round(random.uniform(100, 1000), 2)
            elif selected_type == "Subscription":
                previous_payment_amount = round(random.uniform(5, 50), 2)
            elif selected_type == "Charity":
                previous_payment_amount = round(random.uniform(5, 100), 2)
            elif selected_type == "Gym":
                previous_payment_amount = round(random.uniform(20, 150), 2)
            else:
                previous_payment_amount = round(random.uniform(10, 200), 2)

            # Select a currency - mostly USD, but with some variation
            currencies = ["USD", "EUR", "GBP", "CAD", "AUD"]
            currency_weights = [70, 10, 10, 5, 5]  # USD most common
            previous_payment_currency = random.choices(currencies, weights=currency_weights, k=1)[0]

            # Adjust status if there's payment history
            if status == DirectDebitStatusCode.PENDING:
                # Can't be pending if there are previous payments
                status = random.choice([
                    DirectDebitStatusCode.ACTIVE,
                    DirectDebitStatusCode.SUSPENDED,
                    DirectDebitStatusCode.CANCELED
                ])

        # Create the direct debit dictionary
        direct_debit = {
            "consumer_banking_account_id": id_fields['consumer_banking_account_id'],
            "direct_debit_status_code": status.value,
            "name": name,
            "previous_payment_date_time": previous_payment_date_time,
            "previous_payment_amount": previous_payment_amount,
            "previous_payment_currency": previous_payment_currency
        }

        return direct_debit

    finally:
        cursor.close()
