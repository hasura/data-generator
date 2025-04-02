from ..consumer_banking.enums import TransactionCategory, TransactionType
from ..enterprise import (generate_financial_institution_identifier,
                          generate_financial_institution_name)
from data_generator import DataGenerator, SkipRowGenerationError
from typing import Any, Dict

import random


def generate_random_transaction_debtor_agent(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random transaction debtor agent with plausible values.
    May raise SkipRowGenerationError if the transaction type doesn't typically have debtor agent.

    Args:
        id_fields: Dictionary containing the required ID fields
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated transaction debtor agent data
    """
    # Get database connection
    conn = dg.conn

    # Validate required fields
    if 'consumer_banking_transaction_id' not in id_fields:
        raise ValueError("consumer_banking_transaction_id is required")

    # Fetch the transaction to verify it exists and get transaction details
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT t.consumer_banking_transaction_id, t.transaction_type, t.category,
                   t.credit_debit_indicator, t.description, t.amount,
                   t.consumer_banking_account_id
            FROM consumer_banking.transactions t
            WHERE t.consumer_banking_transaction_id = %s
        """, (id_fields['consumer_banking_transaction_id'],))

        transaction = cursor.fetchone()

        if not transaction:
            raise ValueError(f"No transaction found with ID {id_fields['consumer_banking_transaction_id']}")

        transaction_type = transaction.get('transaction_type')
        transaction_category = transaction.get('category')
        credit_debit_indicator = transaction.get('credit_debit_indicator')
        description = transaction.get('description')

        # Determine if this transaction should have a debtor agent
        # Debtor agents are more likely for incoming transfers than outgoing

        # Skip generating debtor agent for certain transactions
        from ..enterprise.enums import CreditDebitIndicator
        if credit_debit_indicator == CreditDebitIndicator.DEBIT:
            # 85% chance of no debtor agent for outgoing transactions
            if random.random() < 0.85:
                raise SkipRowGenerationError

        # Skip for certain transaction types and categories
        transaction_type_enum = TransactionType(transaction_type)
        skip_types = [
            TransactionType.CASH_WITHDRAWAL,
            TransactionType.PURCHASE,
            TransactionType.TAX_PAYMENT,
            TransactionType.BILL_PAYMENT,
            TransactionType.MERCHANT_PAYMENT,
            TransactionType.RENT_PAYMENT,
            TransactionType.MORTGAGE_PAYMENT,
            TransactionType.UTILITY_PAYMENT,
            TransactionType.SUBSCRIPTION
        ]
        if transaction_type_enum in skip_types and random.random() < 0.95:
            raise SkipRowGenerationError

        skip_categories = [
            TransactionCategory.ATM.value,
            TransactionCategory.POINT_OF_SALE.value,
            TransactionCategory.FEE.value,
            TransactionCategory.INTEREST.value
        ]
        if transaction_category in skip_categories and random.random() < 0.95:
            raise SkipRowGenerationError

        # Determine region based on description or use random region
        region = "US"  # Default

        if description:
            description_lower = description.lower()
            if any(term in description_lower for term in ['international', 'global', 'foreign', 'overseas']):
                region = random.choice(["EU", "UK", "ASIA"])
            elif any(term in description_lower for term in ['europe', 'euro', 'eu']):
                region = "EU"
            elif any(term in description_lower for term in ['uk', 'britain', 'london', 'england']):
                region = "UK"
            elif any(term in description_lower for term in ['asia', 'china', 'japan', 'korea', 'hong kong']):
                region = "ASIA"

        # For transfers, use appropriate regional identifiers
        scheme_name, identification, lei = generate_financial_institution_identifier(region)

        # Generate a plausible financial institution name
        name = generate_financial_institution_name()

        # Add regional indicators to name where appropriate
        if region == "EU":
            if random.random() < 0.4:
                name += " " + random.choice(["Europe", "European", "EU"])
        elif region == "UK":
            if random.random() < 0.4:
                name += " " + random.choice(["UK", "Britain", "London"])
        elif region == "ASIA":
            if random.random() < 0.4:
                name += " " + random.choice(["Asia", "International", "Pacific"])

        # Create the debtor agent dictionary
        debtor_agent = {
            "consumer_banking_transaction_id": id_fields['consumer_banking_transaction_id'],
            "scheme_name": scheme_name.value,
            "identification": identification,
            "name": name,
            "lei": lei
        }

        return debtor_agent

    finally:
        cursor.close()
