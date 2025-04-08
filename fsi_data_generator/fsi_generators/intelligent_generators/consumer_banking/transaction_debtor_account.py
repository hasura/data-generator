from ..consumer_banking.enums import TransactionCategory, TransactionType
from ..enterprise import (generate_financial_institution_identifier,
                          generate_financial_institution_name)
from ..enterprise.enums import IdentifierScheme
from data_generator import DataGenerator, SkipRowGenerationError
from typing import Any, Dict

import random


def generate_random_transaction_debtor_account(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random transaction debtor account with plausible values.
    May raise SkipRowGenerationError if the transaction type doesn't typically have debtor account.

    Args:
        id_fields: Dictionary containing the required ID fields
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated transaction debtor account data
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

        # Determine if this transaction should have a debtor account
        # Debtor accounts are more likely for incoming transfers than outgoing

        # Skip generating debtor account for certain transactions
        from ..enterprise.enums import CreditDebitIndicator
        if credit_debit_indicator == CreditDebitIndicator.DEBIT:
            # 80% chance of no debtor account for outgoing transactions
            if random.random() < 0.8:
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

        # Check if there's already a debtor agent for this transaction
        cursor.execute("""
            SELECT scheme_name, name 
            FROM consumer_banking.transaction_debtor_agents 
            WHERE consumer_banking_transaction_id = %s
        """, (id_fields['consumer_banking_transaction_id'],))

        debtor_agent = cursor.fetchone()
        agent_name = None

        if debtor_agent:
            agent_name = debtor_agent.get('name')

        # Transaction type influences the type of account identifiers used
        if transaction_type_enum == TransactionType.INTERNAL_TRANSFER:
            # For internal transfers, use account number format
            scheme_name = IdentifierScheme.ACCOUNT_NUMBER
            identification = ''.join(random.choices('0123456789', k=random.randint(8, 12)))

        elif transaction_type_enum == TransactionType.EXTERNAL_TRANSFER:
            # External transfers may use different formats based on region
            # Try to determine region from description
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

            # Generate appropriate identifier based on region
            scheme_name, identification, lei = generate_financial_institution_identifier(region)

        else:
            # For other transaction types, use region-based generation similar to external transfers
            region = random.choice(["US", "EU", "UK", "ASIA", "OTHER"])
            scheme_name, identification, lei = generate_financial_institution_identifier(region)

        # Generate account name
        if agent_name:
            # If there's a debtor agent, use its name for the account name
            name = agent_name + " " + random.choice(
                ["Account", "Business Account", "Customer Account", "Checking", "Savings"])
        else:
            # Generate a plausible account name
            account_type_options = ["Checking", "Savings", "Business", "Current", "Payment", "Settlement",
                                    "Collection", "Operating", "Payroll", "Expense"]

            account_owners = ["Personal", "Business", "Corporate", "Company", "Joint", "Trust",
                              "Organizational", "Client", "Customer"]

            # 70% chance of using financial institution name
            if random.random() < 0.7:
                bank_name = generate_financial_institution_name()
                name = f"{random.choice(account_owners)} {random.choice(account_type_options)} - {bank_name}"
            else:
                # Create a business or individual name format
                if random.random() < 0.6:  # Business account
                    business_prefixes = ["Global", "National", "Premier", "Elite", "Advanced", "Century",
                                         "United", "Reliable", "Precision", "Innovative"]
                    business_cores = ["Tech", "Services", "Solutions", "Enterprises", "Industries",
                                      "Systems", "Group", "Associates", "Partners", "Consulting"]
                    business_suffixes = ["Inc.", "LLC", "Ltd.", "Corp.", "Company", "International",
                                         "Holdings", "Group", "Co.", ""]

                    business_name = f"{random.choice(business_prefixes)} {random.choice(business_cores)} {random.choice(business_suffixes)}".strip()
                    name = f"{business_name} {random.choice(account_type_options)}"
                else:  # Individual account
                    first_names = ["John", "Jane", "Michael", "Sarah", "David", "Emily", "James",
                                   "Emma", "Robert", "Olivia"]
                    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia",
                                  "Miller", "Davis", "Rodriguez", "Martinez"]

                    name = f"{random.choice(first_names)} {random.choice(last_names)} {random.choice(account_type_options)}"

        # Secondary identification (optional - 20% chance)
        secondary_identification = None
        if random.random() < 0.2:
            # Usually a reference number or internal bank identifier
            secondary_identification = ''.join(
                random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=random.randint(5, 10)))

        # Create the debtor account dictionary
        debtor_account = {
            "consumer_banking_transaction_id": id_fields['consumer_banking_transaction_id'],
            "scheme_name": scheme_name.value,
            "identification": identification,
            "name": name,
            "secondary_identification": secondary_identification
        }

        return debtor_account

    finally:
        cursor.close()
