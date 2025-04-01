from ..enterprise.enums import CreditDebitIndicator, CurrencyCode, Frequency
from .enums import InterestType, RateType
from data_generator import DataGenerator, SkipRowGenerationError
from typing import Any, Dict

import random


def generate_random_statement_interest(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random statement interest with plausible values.

    Args:
        id_fields: Dictionary containing the required ID fields
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated statement interest data
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
                   a.status, p.product_type, p.base_interest_rate, p.is_interest_bearing
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
        product_type = statement.get('product_type')
        base_interest_rate = statement.get('base_interest_rate', 0)
        is_interest_bearing = statement.get('is_interest_bearing', False)

        # Only generate interest for active accounts
        if account_status != 'ACTIVE':
            raise SkipRowGenerationError

        # Determine credit/debit indicator based on product type
        if product_type in ['SAVINGS', 'CHECKING', 'MONEY_MARKET', 'CERTIFICATE_OF_DEPOSIT'] and is_interest_bearing:
            # Interest-bearing accounts typically earn interest (credit)
            credit_debit_indicator = CreditDebitIndicator.CREDIT
        else:
            # Default to debit (interest charged)
            credit_debit_indicator = CreditDebitIndicator.DEBIT

        # Select interest type based on product type
        if credit_debit_indicator == CreditDebitIndicator.CREDIT:
            # For interest-bearing accounts, select appropriate interest type
            if product_type == 'SAVINGS':
                interest_type = InterestType.SAVINGS
            elif product_type == 'CHECKING':
                interest_type = InterestType.CHECKING
            elif product_type == 'MONEY_MARKET':
                interest_type = InterestType.MONEY_MARKET
            elif product_type == 'CERTIFICATE_OF_DEPOSIT':
                interest_type = InterestType.CERTIFICATE
            else:
                interest_type = InterestType.DEPOSIT
        else:
            # For interest charged, select appropriate type
            interest_types = [
                InterestType.LOAN,
                InterestType.CREDIT_CARD,
                InterestType.OVERDRAFT,
                InterestType.LINE_OF_CREDIT
            ]
            interest_type = random.choice(interest_types)

        # Occasionally generate special interest types
        if random.random() < 0.1:  # 10% chance
            special_types = [
                InterestType.BONUS,
                InterestType.PROMOTIONAL,
                InterestType.ADJUSTMENT
            ]
            interest_type = random.choice(special_types)

        # Generate description based on interest type and credit/debit indicator
        if credit_debit_indicator == CreditDebitIndicator.CREDIT:
            descriptions = {
                InterestType.DEPOSIT: ["Interest Earned", "Deposit Interest", "Account Interest"],
                InterestType.SAVINGS: ["Savings Interest", "Interest Payment", "Savings Account Interest"],
                InterestType.CERTIFICATE: ["CD Interest", "Certificate Interest", "Term Deposit Interest"],
                InterestType.MONEY_MARKET: ["Money Market Interest", "MM Account Interest"],
                InterestType.CHECKING: ["Checking Interest", "Interest Checking"],
                InterestType.BONUS: ["Bonus Interest", "Interest Bonus", "Relationship Bonus"],
                InterestType.PROMOTIONAL: ["Promotional Interest", "Special Rate Interest", "Limited Time Interest"],
                InterestType.ADJUSTMENT: ["Interest Adjustment", "Rate Correction", "Interest Credit"],
                InterestType.OTHER: ["Account Interest", "Interest Credit"]
            }
        else:
            descriptions = {
                InterestType.LOAN: ["Loan Interest", "Loan Interest Charge", "Finance Charge"],
                InterestType.CREDIT_CARD: ["Credit Card Interest", "Card Interest Charge", "Finance Charge"],
                InterestType.OVERDRAFT: ["Overdraft Interest", "Overdraft Fee Interest", "Negative Balance Interest"],
                InterestType.LINE_OF_CREDIT: ["Line of Credit Interest", "Credit Line Interest", "LOC Interest"],
                InterestType.PENALTY: ["Penalty Interest", "Late Payment Interest", "Penalty Rate Interest"],
                InterestType.ADJUSTMENT: ["Interest Adjustment", "Rate Correction", "Interest Debit"],
                InterestType.OTHER: ["Account Interest", "Interest Charge"]
            }

        description = random.choice(descriptions.get(interest_type, ["Interest"]))

        # Generate interest rate
        # Base rate on product's base rate if available
        if base_interest_rate:
            # Add some variation to the base rate
            rate = base_interest_rate + random.uniform(-0.25, 0.25)
            rate = max(0.01, round(rate, 2))  # Ensure rate is positive and rounded
        else:
            # Generate a reasonable rate based on type
            if credit_debit_indicator == CreditDebitIndicator.CREDIT:
                # Interest earned rates are typically lower
                if interest_type == InterestType.SAVINGS:
                    rate = round(random.uniform(0.01, 3.0), 2)
                elif interest_type == InterestType.MONEY_MARKET:
                    rate = round(random.uniform(0.5, 4.0), 2)
                elif interest_type == InterestType.CERTIFICATE:
                    rate = round(random.uniform(1.0, 5.0), 2)
                elif interest_type == InterestType.PROMOTIONAL:
                    rate = round(random.uniform(2.0, 7.0), 2)
                else:
                    rate = round(random.uniform(0.01, 2.5), 2)
            else:
                # Interest charged rates are typically higher
                if interest_type == InterestType.PENALTY:
                    rate = round(random.uniform(18.0, 29.99), 2)
                elif interest_type == InterestType.CREDIT_CARD:
                    rate = round(random.uniform(12.99, 24.99), 2)
                elif interest_type == InterestType.OVERDRAFT:
                    rate = round(random.uniform(15.0, 21.0), 2)
                else:
                    rate = round(random.uniform(5.99, 15.99), 2)

        # Select rate type
        rate_type = RateType.get_random()

        # Select frequency for interest calculation
        frequency_weights = [40, 0, 0, 30, 20, 0, 10, 0, 0, 0, 0, 0]  # Daily and monthly are most common
        frequency = Frequency.get_random(frequency_weights)

        # Generate interest amount
        # This would typically be calculated based on balance, rate, and time period
        # We'll simulate a plausible amount
        if credit_debit_indicator == CreditDebitIndicator.CREDIT:
            # Interest earned - typically smaller amounts
            if interest_type == InterestType.BONUS or interest_type == InterestType.PROMOTIONAL:
                amount = round(random.uniform(5, 100), 2)
            else:
                amount = round(random.uniform(0.01, 50), 2)
        else:
            # Interest charged - can be larger amounts
            amount = round(random.uniform(5, 200), 2)

        # Choose currency (predominantly USD)
        currency = CurrencyCode.get_random(
            [95, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        # Create the statement interest dictionary
        statement_interest = {
            "consumer_banking_statement_id": id_fields['consumer_banking_statement_id'],
            "description": description,
            "credit_debit_indicator": credit_debit_indicator.value,
            "type": interest_type.value,
            "rate": rate,
            "rate_type": rate_type.value,
            "frequency": frequency.value,
            "amount": amount,
            "currency": currency.value
        }

        return statement_interest

    finally:
        cursor.close()
