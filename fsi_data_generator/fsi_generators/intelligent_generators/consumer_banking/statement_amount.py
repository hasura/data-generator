from ..enterprise.enums import CreditDebitIndicator, CurrencyCode
from .enums import AmountSubType, AmountType
from data_generator import DataGenerator
from typing import Any, Dict

import random


def generate_random_statement_amount(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random consumer banking statement amount with plausible values.

    Args:
        id_fields: Dictionary containing the required ID fields
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated statement amount data
    """
    # Get database connection
    conn = dg.conn

    # Validate required fields
    if 'consumer_banking_statement_id' not in id_fields:
        raise ValueError("consumer_banking_statement_id is required")

    # Fetch the statement to verify it exists and get additional context
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT s.consumer_banking_statement_id, s.start_date_time, s.end_date_time 
            FROM consumer_banking.statements s
            WHERE s.consumer_banking_statement_id = %s
        """, (id_fields['consumer_banking_statement_id'],))

        statement = cursor.fetchone()

        if not statement:
            raise ValueError(f"No statement found with ID {id_fields['consumer_banking_statement_id']}")

        # Determine amount type using the enum
        amount_type = AmountType.get_random()

        # Determine credit/debit indicator based on type
        # Some types are typically credits, others are debits
        if amount_type in [AmountType.DEPOSITS, AmountType.CREDITS, AmountType.TRANSFERS_IN,
                           AmountType.INTEREST_EARNED]:
            credit_debit_indicator = CreditDebitIndicator.CREDIT
        elif amount_type in [AmountType.WITHDRAWALS, AmountType.FEES, AmountType.INTEREST_CHARGED,
                             AmountType.TRANSFERS_OUT]:
            credit_debit_indicator = CreditDebitIndicator.DEBIT
        else:
            # For other types, it could be either, but with different probabilities
            if random.random() < 0.7:  # 70% chance of being a debit
                credit_debit_indicator = CreditDebitIndicator.DEBIT
            else:
                credit_debit_indicator = CreditDebitIndicator.CREDIT

        # Generate amount based on type
        if amount_type in [AmountType.OPENING_BALANCE, AmountType.CLOSING_BALANCE, AmountType.CURRENT_BALANCE,
                           AmountType.AVAILABLE_BALANCE]:
            # Balances tend to be larger
            amount = round(random.uniform(500, 10000), 2)
        elif amount_type in [AmountType.FEES, AmountType.INTEREST_EARNED, AmountType.INTEREST_CHARGED]:
            # Fees and interest tend to be smaller
            amount = round(random.uniform(0.01, 100), 2)
        elif amount_type in [AmountType.MINIMUM_PAYMENT_DUE]:
            # Minimum payments are usually moderate
            amount = round(random.uniform(20, 200), 2)
        else:
            # Other amounts can vary widely
            amount = round(random.uniform(10, 2000), 2)

        # Determine amount subtype (optional - 60% chance of having one)
        sub_type = None
        if random.random() < 0.6:
            sub_type = AmountSubType.get_random()

        # Choose currency (heavily biased toward USD)
        currency = CurrencyCode.USD  # Default to USD
        if random.random() < 0.05:  # 5% chance of using other currency
            currency = CurrencyCode.get_random()

        # Create the statement amount dictionary
        statement_amount = {
            "consumer_banking_statement_id": id_fields['consumer_banking_statement_id'],
            "credit_debit_indicator": credit_debit_indicator.value,
            "type": amount_type.value,
            "amount": amount,
            "currency": currency.value,
            "sub_type": sub_type.value if sub_type else None
        }

        return statement_amount

    finally:
        cursor.close()
