from ..enterprise.enums import CreditDebitIndicator, CurrencyCode
from .enums import BalanceSubType, BalanceType
from data_generator import DataGenerator
from typing import Any, Dict

import datetime
import random


def generate_random_balance(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random consumer banking balance with plausible values.

    Args:
        id_fields: Dictionary containing the required ID fields
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated balance data
    """
    # Get database connection
    conn = dg.conn

    # Validate required fields
    if 'consumer_banking_account_id' not in id_fields:
        raise ValueError("consumer_banking_account_id is required")

    # Fetch the consumer banking account to get its opened date
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT opened_date 
            FROM consumer_banking.accounts 
            WHERE consumer_banking_account_id = %s
        """, (id_fields['consumer_banking_account_id'],))

        consumer_account = cursor.fetchone()

        if not consumer_account:
            raise ValueError(f"No consumer banking account found with ID {id_fields['consumer_banking_account_id']}")

        account_opened_date = consumer_account.get('opened_date')

        # Check if there are previous balances for this account
        cursor.execute("""
            SELECT date_time, amount, type, currency, credit_debit_indicator
            FROM consumer_banking.balances
            WHERE consumer_banking_account_id = %s
            ORDER BY date_time DESC
            LIMIT 1
        """, (id_fields['consumer_banking_account_id'],))

        previous_balance = cursor.fetchone()

        # Generate today's date
        today = datetime.datetime.now(datetime.timezone.utc)

        # If there's a previous balance, set the start date to that balance's date
        # Otherwise, use the account's opened date
        if previous_balance:
            start_date = previous_balance.get('date_time')
            # Add a small "time increment" to ensure the new balance is after the previous one
            start_date = start_date + datetime.timedelta(minutes=random.randint(5, 60))

            # Use previous balance's currency and type in most cases for consistency
            prev_type = previous_balance.get('type')
            prev_currency = previous_balance.get('currency')
            prev_amount = previous_balance.get('amount')
            prev_indicator = previous_balance.get('credit_debit_indicator')

            # 80% chance to keep the same balance type for consistency
            if random.random() < 0.8:
                # Find the enum member by value
                balance_type = next((t for t in BalanceType if t.value == prev_type), BalanceType.get_random())
            else:
                balance_type = BalanceType.get_random()

            # 95% chance to keep the same currency
            if random.random() < 0.95:
                currency = next((c for c in CurrencyCode if c.value == prev_currency), CurrencyCode.get_random())
            else:
                currency = CurrencyCode.get_random()

            # Generate a plausible amount based on previous balance
            # Usually within +/- 20% of previous amount
            amount_change_factor = random.uniform(0.8, 1.2)
            amount_base = abs(float(prev_amount)) * amount_change_factor

            # Determine credit/debit indicator
            # Usually maintain the same indicator
            if random.random() < 0.8:
                credit_debit_indicator = next(
                    (i for i in CreditDebitIndicator if i.value == prev_indicator),
                    CreditDebitIndicator.get_random()
                )
            else:
                credit_debit_indicator = CreditDebitIndicator.get_random()
        else:
            start_date = account_opened_date

            # If no previous balance, generate new values
            balance_type = BalanceType.get_random()
            currency = CurrencyCode.get_random()
            credit_debit_indicator = CreditDebitIndicator.get_random()

            # Generate plausible amount (between 0.01 and 100,000)
            # More weighted towards smaller amounts
            amount_base = random.choices(
                [
                    random.uniform(0.01, 100),
                    random.uniform(100, 1000),
                    random.uniform(1000, 10000),
                    random.uniform(10000, 100000)
                ],
                weights=[50, 30, 15, 5],
                k=1
            )[0]

        # Ensure the date is not after today
        if start_date > today:
            start_date = today - datetime.timedelta(days=1)

        # Calculate days between start date and today
        days_available = (today - start_date).days

        # Randomly choose a date between start date and now
        # For recent balances, favor more recent dates
        if days_available > 0:
            date_weight = [1] * (days_available + 1)
            for i in range(days_available + 1):
                # Exponential weighting to favor recent dates
                date_weight[int(i)] = 1.1 ** float(i)

            days_to_add = random.choices(
                range(days_available + 1),
                weights=date_weight,
                k=1
            )[0]

            balance_date_time = start_date + datetime.timedelta(days=days_to_add)
        else:
            # If start_date is today, add a random number of minutes
            hours_since_start = (today - start_date).total_seconds() / 3600
            if hours_since_start > 0:
                hours_to_add = random.uniform(0, hours_since_start)
                balance_date_time = start_date + datetime.timedelta(hours=hours_to_add)
            else:
                balance_date_time = start_date + datetime.timedelta(minutes=random.randint(5, 60))

        # Determine subtype (if applicable)
        include_sub_type = random.random() < 0.6  # 60% chance of having a subtype
        balance_sub_type = BalanceSubType.get_random() if include_sub_type else None

        # If it's a DEBIT balance, make it negative
        amount = -amount_base if credit_debit_indicator == CreditDebitIndicator.DEBIT else amount_base

        # Round to 2 decimal places for standard currencies
        # If JPY, round to whole numbers
        if currency == CurrencyCode.JPY:
            amount = round(amount)
        else:
            amount = round(amount, 2)

        # Create the balance dictionary
        balance = {
            "consumer_banking_account_id": id_fields['consumer_banking_account_id'],
            "credit_debit_indicator": credit_debit_indicator.value,
            "type": balance_type.value,
            "date_time": balance_date_time,
            "amount": amount,
            "currency": currency.value,
            "sub_type": balance_sub_type.value if include_sub_type else None,
        }

        return balance

    finally:
        cursor.close()
