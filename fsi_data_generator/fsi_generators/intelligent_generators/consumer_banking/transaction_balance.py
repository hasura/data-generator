from data_generator import DataGenerator
from typing import Any, Dict

from .enums import BalanceType
from ..enterprise.enums import CreditDebitIndicator, CurrencyCode
import random


def generate_random_transaction_balance(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random transaction balance with plausible values,
    attempting to maintain logical running balances.

    Args:
        id_fields: Dictionary containing the required ID fields
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated transaction balance data
    """
    # Get database connection
    conn = dg.conn

    # Validate required fields
    if 'consumer_banking_transaction_id' not in id_fields:
        raise ValueError("consumer_banking_transaction_id is required")

    # Fetch the transaction to verify it exists and get additional context
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT t.consumer_banking_transaction_id, t.amount, t.currency, 
                   t.credit_debit_indicator, t.consumer_banking_account_id,
                   t.transaction_date
            FROM consumer_banking.transactions t
            WHERE t.consumer_banking_transaction_id = %s
        """, (id_fields['consumer_banking_transaction_id'],))

        transaction = cursor.fetchone()

        if not transaction:
            raise ValueError(f"No transaction found with ID {id_fields['consumer_banking_transaction_id']}")

        # Extract transaction details
        transaction_amount = transaction.get('amount', 0)
        transaction_currency = transaction.get('currency')
        transaction_credit_debit = transaction.get('credit_debit_indicator')
        account_id = transaction.get('consumer_banking_account_id')
        transaction_date = transaction.get('transaction_date')

        # Try to find the most recent balance before this transaction
        cursor.execute("""
            SELECT b.amount, b.currency, b.type, b.credit_debit_indicator
            FROM consumer_banking.balances b
            WHERE b.consumer_banking_account_id = %s
              AND b.date_time <= %s
            ORDER BY b.date_time DESC
            LIMIT 1
        """, (account_id, transaction_date))

        prior_balance = cursor.fetchone()

        # Try to find any transaction balances associated with this account
        # that occurred after this balance but before our current transaction
        cursor.execute("""
            SELECT tb.amount, tb.credit_debit_indicator, tb.type,
                   t.credit_debit_indicator as transaction_credit_debit, 
                   t.amount as transaction_amount
            FROM consumer_banking.transaction_balances tb
            JOIN consumer_banking.transactions t 
              ON tb.consumer_banking_transaction_id = t.consumer_banking_transaction_id
            WHERE t.consumer_banking_account_id = %s
              AND t.transaction_date > %s
              AND t.transaction_date <= %s
              AND tb.type = 'AVAILABLE'
            ORDER BY t.transaction_date DESC
            LIMIT 1
        """, (account_id,
              prior_balance.get('date_time') if prior_balance else '1900-01-01',
              transaction_date))

        latest_transaction_balance = cursor.fetchone()

        # Default values if no prior balance
        base_balance_amount = 1000.0
        base_balance_currency = CurrencyCode.USD
        base_balance_credit_debit = CreditDebitIndicator.CREDIT

        # If we have a prior transaction balance, use that as our starting point
        if latest_transaction_balance:
            base_balance_amount = latest_transaction_balance.get('amount', base_balance_amount)
            base_balance_credit_debit = latest_transaction_balance.get('credit_debit_indicator',
                                                                       base_balance_credit_debit)
        # Otherwise use the account balance if available
        elif prior_balance:
            base_balance_amount = prior_balance.get('amount', base_balance_amount)
            base_balance_currency = prior_balance.get('currency', base_balance_currency)
            base_balance_credit_debit = prior_balance.get('credit_debit_indicator', base_balance_credit_debit)

        # Ensure currency consistency
        currency = transaction_currency if transaction_currency else base_balance_currency

        # Calculate balance after this transaction
        # Convert amount to signed value based on credit/debit indicator
        balance_sign = 1 if base_balance_credit_debit == CreditDebitIndicator.CREDIT else -1
        transaction_sign = 1 if transaction_credit_debit == CreditDebitIndicator.CREDIT else -1

        # Calculate signed amounts
        signed_balance = base_balance_amount * balance_sign
        signed_transaction = transaction_amount * transaction_sign

        # New balance after transaction
        new_balance = signed_balance + signed_transaction

        # Determine new credit/debit indicator
        new_credit_debit = CreditDebitIndicator.CREDIT if new_balance >= 0 else CreditDebitIndicator.DEBIT

        # For display, use absolute value
        new_balance_amount = abs(new_balance)

        # Determine balance type - include both common types
        balance_type_options = [
            BalanceType.AVAILABLE,
            BalanceType.CURRENT,
            BalanceType.LEDGER
        ]
        balance_type_weights = [60, 30, 10]  # Available balance is most common
        chosen_balance_type = random.choices(balance_type_options, weights=balance_type_weights, k=1)[0]

        # Create the transaction balance dictionary
        transaction_balance = {
            "consumer_banking_transaction_id": id_fields['consumer_banking_transaction_id'],
            "credit_debit_indicator": new_credit_debit.value,
            "type": chosen_balance_type.value,
            "amount": round(new_balance_amount, 2),
            "currency": currency.value if hasattr(currency, 'value') else currency
        }

        return transaction_balance

    finally:
        cursor.close()
