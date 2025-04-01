from ..enterprise.enums import CurrencyCode, PartyType
from .enums import TransactionType, TransactionCategory, CardSchemeName, AuthorizationType
from data_generator import DataGenerator, SkipRowGenerationError
from typing import Any, Dict, Optional
import random


def generate_random_transaction_card_instrument(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random transaction card instrument with plausible values.
    May raise SkipRowGenerationError if the transaction type doesn't typically involve a card.

    Args:
        id_fields: Dictionary containing the required ID fields
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated transaction card instrument data
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
        description = transaction.get('description', '')
        # merchant_name = transaction.get('merchant_name', '')
        consumer_banking_account_id = transaction.get('consumer_banking_account_id')

        # Determine if this transaction should have a card instrument
        # Only certain transaction types typically use card instruments
        transaction_type_enum = TransactionType(transaction_type)

        # Transaction types that typically use cards
        card_transaction_types = [
            TransactionType.PURCHASE,
            TransactionType.REFUND,
            TransactionType.CASH_WITHDRAWAL,
            TransactionType.RETAIL,
            TransactionType.FOOD_DINING,
            TransactionType.TRANSPORTATION,
            TransactionType.TRAVEL,
            TransactionType.HEALTHCARE,
            TransactionType.ENTERTAINMENT
        ]

        # Transaction categories that typically use cards
        card_transaction_categories = [
            TransactionCategory.POINT_OF_SALE.value,
            TransactionCategory.CARD_PAYMENT.value
        ]

        # Skip if not a typical card transaction type
        if transaction_type_enum not in card_transaction_types and transaction_category not in card_transaction_categories:
            # Small chance of still having card data for other transaction types
            if random.random() > 0.05:  # 5% chance to continue for non-card transaction types
                raise SkipRowGenerationError

        # Skip for certain transaction descriptions that suggest non-card transactions
        skip_descriptions = ['direct deposit', 'ach transfer', 'wire transfer', 'check deposit',
                             'bank transfer', 'internal transfer', 'bill payment', 'standing order',
                             'direct debit']

        if any(term in description.lower() for term in
               skip_descriptions) and random.random() > 0.02:  # 2% chance to continue
            raise SkipRowGenerationError

        # Determine card scheme name based on patterns in the data
        # Check for merchant name patterns that suggest specific card networks
        merchant_name: Optional[str] = None
        if merchant_name:
            merchant_lower = merchant_name.lower()
            if 'amex' in merchant_lower or 'american express' in merchant_lower:
                card_scheme_name = CardSchemeName.AMEX
            elif 'discover' in merchant_lower:
                card_scheme_name = CardSchemeName.DISCOVER
            elif 'diners' in merchant_lower:
                card_scheme_name = CardSchemeName.DINERS
            else:
                # Use random selection with weights for other merchants
                card_scheme_name = CardSchemeName.get_random()
        else:
            # Use random selection with weights
            card_scheme_name = CardSchemeName.get_random()

        # Determine authorization type based on transaction amount and other factors
        amount = transaction.get('amount', 0)

        # For small amounts, contactless is more likely
        if amount < 50:
            auth_type_weights = [5, 5, 1, 10, 40, 20, 5, 10, 1, 1, 2, 0]  # Higher weight for contactless
            authorization_type = AuthorizationType.get_random(auth_type_weights)
        # For in-person higher amounts, PIN is more likely
        elif amount >= 50 and not any(term in description.lower() for term in ['online', 'web', 'internet']):
            auth_type_weights = [40, 10, 10, 0, 10, 20, 5, 0, 2, 1, 2, 0]  # Higher weight for PIN
            authorization_type = AuthorizationType.get_random(auth_type_weights)
        # For online transactions
        elif any(term in description.lower() for term in ['online', 'web', 'internet', 'e-commerce']):
            auth_type_weights = [0, 0, 0, 60, 0, 0, 0, 30, 0, 5, 5, 0]  # Higher weight for online and tokenized
            authorization_type = AuthorizationType.get_random(auth_type_weights)
        else:
            # Default random distribution
            authorization_type = AuthorizationType.get_random()

        # Generate cardholder name - directly from the transaction's account
        # First get the enterprise account ID for this transaction's account
        cursor.execute("""
            SELECT enterprise_account_id
            FROM consumer_banking.accounts
            WHERE consumer_banking_account_id = %s
        """, (consumer_banking_account_id,))

        account_result = cursor.fetchone()
        if not account_result:
            raise ValueError(f"No account found with consumer_banking_account_id {consumer_banking_account_id}")

        enterprise_account_id = account_result.get('enterprise_account_id')

        # Now get the primary account owner
        cursor.execute("""
            SELECT p.name, p.party_type
            FROM enterprise.parties p
            JOIN enterprise.account_ownership ao ON p.enterprise_party_id = ao.enterprise_party_id
            WHERE ao.enterprise_account_id = %s
            ORDER BY CASE WHEN p.party_type = 'INDIVIDUAL' THEN 0 ELSE 1 END
            LIMIT 1
        """, (enterprise_account_id,))

        owner_result = cursor.fetchone()

        if owner_result and owner_result.get('name'):
            name = owner_result.get('name')

            # If this is an organization, we need to get an individual associated with it
            if owner_result.get('party_type') != PartyType.INDIVIDUAL.value:
                # Try to find an individual connected to this organization
                cursor.execute("""
                    SELECT p.name
                    FROM enterprise.parties p
                    JOIN enterprise.party_relationships pr ON p.enterprise_party_id = pr.related_party_id
                    WHERE pr.enterprise_party_id = (
                        SELECT enterprise_party_id
                        FROM enterprise.account_ownership
                        WHERE enterprise_account_id = %s
                        LIMIT 1
                    )
                    AND p.party_type = 'INDIVIDUAL'
                    LIMIT 1
                """, (enterprise_account_id,))

                individual_result = cursor.fetchone()
                if individual_result and individual_result.get('name'):
                    name = individual_result.get('name')
        else:
            # Fallback to generated names if we can't find the account owner
            first_names = ["JOHN", "JANE", "MICHAEL", "SARAH", "DAVID", "EMILY", "ROBERT", "JESSICA",
                           "WILLIAM", "ELIZABETH", "JAMES", "JENNIFER", "RICHARD", "LISA", "JOSEPH", "MARY"]
            last_names = ["SMITH", "JOHNSON", "WILLIAMS", "BROWN", "JONES", "MILLER", "DAVIS", "GARCIA",
                          "RODRIGUEZ", "WILSON", "MARTINEZ", "ANDERSON", "TAYLOR", "THOMAS", "HERNANDEZ", "MOORE"]

            name = f"{random.choice(first_names)} {random.choice(last_names)}"

        # For American Express, names are often shorter on cards
        if card_scheme_name == CardSchemeName.AMEX and len(name) > 20:
            name_parts = name.split()
            if len(name_parts) > 2:
                name = f"{name_parts[0]} {name_parts[-1]}"

        # Generate masked card number based on card scheme
        if card_scheme_name == CardSchemeName.VISA:
            identification = f"4{'X' * 8}{random.randint(1000, 9999)}"
        elif card_scheme_name == CardSchemeName.MASTERCARD:
            identification = f"5{'X' * 8}{random.randint(1000, 9999)}"
        elif card_scheme_name == CardSchemeName.AMEX:
            identification = f"3{'X' * 9}{random.randint(1000, 9999)}"
        elif card_scheme_name == CardSchemeName.DISCOVER:
            identification = f"6{'X' * 8}{random.randint(1000, 9999)}"
        else:
            identification = f"{'X' * 8}{random.randint(1000, 9999)}"

        # Create the transaction card instrument dictionary
        transaction_card_instrument = {
            "consumer_banking_transaction_id": id_fields['consumer_banking_transaction_id'],
            "card_scheme_name": card_scheme_name.value,
            "authorisation_type": authorization_type.value if random.random() < 0.85 else None,  # 15% chance of None
            "name": name,
            "identification": identification
        }

        return transaction_card_instrument

    finally:
        cursor.close()
