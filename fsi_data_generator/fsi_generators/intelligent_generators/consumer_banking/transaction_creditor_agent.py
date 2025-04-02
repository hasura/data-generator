from ..consumer_banking.enums import TransactionCategory, TransactionType
from ..enterprise import (generate_financial_institution_identifier,
                          generate_financial_institution_name)
from ..enterprise.enums import CreditDebitIndicator
from data_generator import DataGenerator, SkipRowGenerationError
from typing import Any, Dict

import random


def generate_random_transaction_creditor_agent(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random transaction creditor agent with plausible values.
    May raise SkipRowGenerationError if the transaction type doesn't typically have creditor agent.

    Args:
        id_fields: Dictionary containing the required ID fields
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated transaction creditor agent data
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
                   t.credit_debit_indicator, t.description
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

        # Determine if this transaction should have a creditor agent
        # Typically, only outgoing payments, transfers, and similar transactions have creditor agents
        # Credit transactions (money coming in) typically don't have creditor agents

        # Skip generating creditor agent for credit transactions (money coming in)
        if credit_debit_indicator == CreditDebitIndicator.CREDIT.value:
            # 90% chance of no creditor agent for incoming transactions
            if random.random() < 0.9:
                raise SkipRowGenerationError

        # Skip for certain transaction types and categories
        skip_types = [
            TransactionType.CASH_WITHDRAWAL.value,
            TransactionType.PURCHASE.value,
            TransactionType.REFUND.value,
            TransactionType.DIVIDEND.value
        ]
        if transaction_type in skip_types and random.random() < 0.95:
            raise SkipRowGenerationError

        skip_categories = [
            TransactionCategory.ATM.value,
            TransactionCategory.POINT_OF_SALE.value,
            TransactionCategory.FEE.value,
            TransactionCategory.INTEREST.value,
            TransactionCategory.CARD_PAYMENT.value
        ]
        if transaction_category in skip_categories and random.random() < 0.95:
            raise SkipRowGenerationError

        # For other transactions, there's still a small chance (10%) they don't have a creditor agent
        if random.random() < 0.1:
            raise SkipRowGenerationError

        # Determine region for identifier generation based on transaction context
        regions = ["US", "EU", "UK", "ASIA", "OTHER"]
        region_weights = [40, 30, 15, 10, 5]  # US most common

        # Adjust weights based on transaction description if available
        if description:
            description_lower = description.lower()
            # Check for international indicators in description
            if any(term in description_lower for term in ['international', 'global', 'foreign', 'overseas']):
                # More likely to be non-US
                region_weights = [20, 35, 20, 15, 10]
            elif any(term in description_lower for term in ['europe', 'euro', 'eu']):
                # Likely European
                region_weights = [10, 60, 20, 5, 5]
            elif any(term in description_lower for term in ['uk', 'britain', 'london', 'england']):
                # Likely UK
                region_weights = [10, 20, 60, 5, 5]
            elif any(term in description_lower for term in ['asia', 'china', 'japan', 'korea', 'hong kong']):
                # Likely Asian
                region_weights = [10, 10, 5, 70, 5]

        # Select region based on weights
        region = random.choices(regions, weights=region_weights, k=1)[0]

        # Generate appropriate financial identifiers based on region
        scheme_name, identification, lei = generate_financial_institution_identifier(region)

        # Generate creditor agent name
        name = generate_financial_institution_name()

        # Create the creditor agent dictionary
        creditor_agent = {
            "consumer_banking_transaction_id": id_fields['consumer_banking_transaction_id'],
            "scheme_name": scheme_name.value,  # Convert enum to string value
            "identification": identification,
            "name": name
        }

        # Add LEI if available (only include if it exists)
        if lei:
            creditor_agent["lei"] = lei

        return creditor_agent

    finally:
        cursor.close()
