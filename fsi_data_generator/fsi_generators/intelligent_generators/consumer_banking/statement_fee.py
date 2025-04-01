from ..enterprise.enums import CreditDebitIndicator, CurrencyCode
from .enums import FeeFrequency, FeeType, RateType
from data_generator import DataGenerator, SkipRowGenerationError
from typing import Any, Dict

import random


def generate_random_statement_fee(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random statement fee with plausible values.

    Args:
        id_fields: Dictionary containing the required ID fields
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated statement fee data
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
            SELECT s.consumer_banking_statement_id, s.consumer_banking_account_id, 
                   a.status, p.product_type, p.monthly_fee
            FROM consumer_banking.statements s
            JOIN consumer_banking.accounts a ON s.consumer_banking_account_id = a.consumer_banking_account_id
            JOIN consumer_banking.products p ON a.consumer_banking_product_id = p.consumer_banking_product_id
            WHERE s.consumer_banking_statement_id = %s
        """, (id_fields['consumer_banking_statement_id'],))

        statement = cursor.fetchone()

        if not statement:
            raise ValueError(f"No statement found with ID {id_fields['consumer_banking_statement_id']}")

        # Extract relevant information
        account_status = statement.get('status')
        # product_type = statement.get('product_type')
        standard_monthly_fee = statement.get('monthly_fee', 0)

        # Only generate fees for active accounts
        if account_status != 'ACTIVE':
            raise SkipRowGenerationError

        # Select fee type based on product type and randomness
        fee_type = FeeType.get_random()

        # Generate description based on fee type
        descriptions = {
            FeeType.SERVICE: ["Monthly Service Fee", "Account Maintenance Fee", "Account Service Charge"],
            FeeType.TRANSACTION: ["Transaction Fee", "Payment Processing Fee", "Transfer Fee"],
            FeeType.OVERDRAFT: ["Overdraft Fee", "Overdraft Protection Fee", "NSF Fee"],
            FeeType.ATM: ["ATM Withdrawal Fee", "Out-of-Network ATM Fee", "ATM Balance Inquiry Fee"],
            FeeType.WIRE_TRANSFER: ["Wire Transfer Fee", "International Wire Fee", "Domestic Wire Fee"],
            FeeType.FOREIGN_TRANSACTION: ["Foreign Transaction Fee", "Currency Conversion Fee", "Cross-Border Fee"],
            FeeType.PAPER_STATEMENT: ["Paper Statement Fee", "Statement Delivery Fee", "Statement Production Fee"],
            FeeType.STOP_PAYMENT: ["Stop Payment Fee", "Check Stop Payment", "Payment Cancellation Fee"],
            FeeType.REPLACEMENT_CARD: ["Card Replacement Fee", "Rush Replacement Card Fee", "Lost Card Fee"],
            FeeType.EARLY_WITHDRAWAL: ["Early Withdrawal Penalty", "Term Deposit Withdrawal Fee",
                                       "CD Early Termination Fee"],
            FeeType.INSUFFICIENT_FUNDS: ["Insufficient Funds Fee", "Returned Item Fee", "Declined Transaction Fee"],
            FeeType.DORMANT_ACCOUNT: ["Dormant Account Fee", "Inactivity Fee", "Inactive Account Charge"],
            FeeType.RESEARCH: ["Account Research Fee", "Document Retrieval Fee", "Investigation Fee"],
            FeeType.SPECIAL_STATEMENT: ["Statement Copy Fee", "Special Statement Request", "Duplicate Statement Fee"],
            FeeType.LATE_PAYMENT: ["Late Payment Fee", "Past Due Fee", "Delayed Payment Charge"],
            FeeType.OTHER: ["Miscellaneous Fee", "Service Charge", "Account Fee"]
        }

        description = random.choice(descriptions.get(fee_type, ["Fee"]))

        # Determine if this is a credit (refund) or debit (charge)
        # Most fees are debits, but occasionally there are credits (refunds, reversals)
        if random.random() < 0.05:  # 5% chance of being a credit
            credit_debit_indicator = CreditDebitIndicator.CREDIT
            # For credits, modify the description to indicate a refund or reversal
            description = f"{description} Refund" if random.random() < 0.5 else f"{description} Reversal"
        else:
            credit_debit_indicator = CreditDebitIndicator.DEBIT

        # Generate fee amount based on fee type
        if fee_type == FeeType.SERVICE:
            # Service fees are typically the standard monthly fee
            amount = standard_monthly_fee if standard_monthly_fee else round(random.uniform(5, 15), 2)
        elif fee_type == FeeType.OVERDRAFT:
            # Overdraft fees are typically higher
            amount = round(random.uniform(25, 40), 2)
        elif fee_type == FeeType.ATM:
            # ATM fees are typically lower
            amount = round(random.uniform(2, 5), 2)
        elif fee_type == FeeType.WIRE_TRANSFER:
            # Wire fees vary based on domestic/international
            if "International" in description:
                amount = round(random.uniform(30, 50), 2)
            else:
                amount = round(random.uniform(15, 30), 2)
        elif fee_type == FeeType.FOREIGN_TRANSACTION:
            # Foreign transaction fees are often percentage-based
            # We'll generate both a rate and an amount
            rate = round(random.uniform(1, 3), 2)  # Typically 1-3%
            # Amount depends on the assumed transaction value
            transaction_value = round(random.uniform(50, 1000), 2)
            amount = round(transaction_value * rate / 100, 2)
        else:
            # Other fees vary widely
            amount = round(random.uniform(5, 35), 2)

        # If it's a credit, make the amount negative
        if credit_debit_indicator == CreditDebitIndicator.CREDIT:
            amount = abs(amount)  # Ensure positive amount for database

        # Choose currency (predominantly USD)
        currency = CurrencyCode.get_random(
            [95, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        # Determine fee frequency
        fee_frequency = FeeFrequency.get_random()

        # For percentage-based fees, include rate information
        rate = None
        rate_type = None
        if fee_type == FeeType.FOREIGN_TRANSACTION or random.random() < 0.1:  # 10% chance for other fees to be rate-based
            rate = round(random.uniform(0.5, 5), 2)  # Rate as percentage
            rate_type = RateType.get_random()

        # Create the statement fee dictionary
        statement_fee = {
            "consumer_banking_statement_id": id_fields['consumer_banking_statement_id'],
            "description": description,
            "credit_debit_indicator": credit_debit_indicator.value,
            "type": fee_type.value,
            "rate": rate,
            "rate_type": rate_type.value if rate_type else None,
            "frequency": fee_frequency.value,
            "amount": amount,
            "currency": currency.value
        }

        return statement_fee

    finally:
        cursor.close()
