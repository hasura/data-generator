from data_generator import DataGenerator, SkipRowGenerationError
from typing import Any, Dict

import random


def generate_random_transaction_ultimate_debtor(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random transaction ultimate debtor with plausible values.
    May raise SkipRowGenerationError if the transaction type doesn't typically have an ultimate debtor.

    Args:
        id_fields: Dictionary containing the required ID fields
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated transaction ultimate debtor data
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
        # transaction_category = transaction.get('category')
        description = transaction.get('description', '')
        # amount = transaction.get('amount', 0)

        # Check if there's a debtor agent/account already for this transaction
        cursor.execute("""
            SELECT COUNT(*) as has_debtor
            FROM consumer_banking.transaction_debtor_agents
            WHERE consumer_banking_transaction_id = %s
        """, (id_fields['consumer_banking_transaction_id'],))

        has_debtor_agent = cursor.fetchone().get('has_debtor', 0) > 0

        cursor.execute("""
            SELECT COUNT(*) as has_debtor_account
            FROM consumer_banking.transaction_debtor_accounts
            WHERE consumer_banking_transaction_id = %s
        """, (id_fields['consumer_banking_transaction_id'],))

        has_debtor_account = cursor.fetchone().get('has_debtor_account', 0) > 0

        # Ultimate debtors are only used in specific transaction scenarios:
        # 1. When there's an intermediary (debtor_agent/account exists)
        # 2. For specific transaction types like external transfers, bill payments

        from ..consumer_banking.enums import (TransactionCategory,
                                              TransactionType)
        from ..enterprise.enums import CreditDebitIndicator

        transaction_type_enum = TransactionType(transaction_type)
        # credit_debit_indicator = transaction.get('credit_debit_indicator')

        # Skip if no debtor agent/account and not a transaction type that would have an ultimate debtor
        if not (has_debtor_agent or has_debtor_account):
            # 90% chance to skip if there's no debtor agent or account
            if random.random() < 0.9:
                raise SkipRowGenerationError

        # Ultimate debtors are more likely for certain transaction types
        ultimate_debtor_types = [
            TransactionType.EXTERNAL_TRANSFER,
            TransactionType.BILL_PAYMENT,
            TransactionType.MORTGAGE_PAYMENT,
            TransactionType.TAX_PAYMENT
        ]

        if transaction_type_enum not in ultimate_debtor_types:
            # 80% chance to skip for non-typical transaction types
            if random.random() < 0.8:
                raise SkipRowGenerationError

        # Look for keywords in description suggesting an ultimate debtor
        description_lower = None
        if description:
            description_lower = description.lower()
            ultimate_debtor_keywords = [
                'on behalf of', 'for the account of', 'originator', 'sender', 'initiator',
                'from', 'source', 'remitter', 'payer', 'originally from'
            ]
            has_keyword = any(keyword in description_lower for keyword in ultimate_debtor_keywords)

            if not has_keyword:
                # 70% chance to skip if no keyword suggesting an ultimate debtor
                if random.random() < 0.7:
                    raise SkipRowGenerationError

        # Generate ultimate debtor name
        # If there's description text, try to extract a debtor name from it
        name = None
        if description:
            # Look for patterns like "on behalf of [NAME]" or "from [NAME]" in the description
            for prefix in ['on behalf of ', 'for the account of ', 'originator: ', 'from ', 'remitter: ']:
                if prefix in description_lower:
                    # Extract potential name after the prefix
                    start_index = description_lower.find(prefix) + len(prefix)
                    potential_name = description[start_index:].split(',')[0].strip()

                    # Use if it's a reasonable name length
                    if 3 <= len(potential_name) <= 100:
                        name = potential_name
                        break

        # If we couldn't extract a name, generate a plausible one
        if not name:
            # Decide if individual or business (70% individual for ultimate debtors)
            if random.random() < 0.3:  # Business name (30%)
                business_prefixes = ["Global", "National", "Premier", "Elite", "Advanced", "Century",
                                     "United", "Reliable", "Precision", "Innovative", "Apex", "Cascade",
                                     "Dynamic", "Evergreen", "Frontier", "Harbor", "Insight", "Landmark"]

                business_cores = ["Tech", "Services", "Solutions", "Enterprises", "Industries",
                                  "Systems", "Group", "Associates", "Partners", "Consulting",
                                  "Financial", "Capital", "Holdings", "Investments", "Management",
                                  "Materials", "Resources", "Energy", "Properties", "Builders"]

                business_suffixes = ["Inc.", "LLC", "Ltd.", "Corp.", "Company", "International",
                                     "Holdings", "Group", "Co.", "Incorporated", "Corporation",
                                     "Partners", "Associates", "Enterprises", "Venture", "Trust"]

                # Generate business name
                business_name = ""
                if random.random() < 0.3:  # 30% chance of prefix
                    business_name += f"{random.choice(business_prefixes)} "

                business_name += random.choice(business_cores)

                if random.random() < 0.4:  # 40% chance of second core term
                    business_name += f" {random.choice(business_cores)}"

                if random.random() < 0.7:  # 70% chance of suffix
                    business_name += f" {random.choice(business_suffixes)}"

                name = business_name.strip()
            else:  # Individual name (70%)
                first_names = ["John", "Jane", "Michael", "Sarah", "David", "Emily", "James",
                               "Emma", "Robert", "Olivia", "William", "Sophia", "Joseph", "Isabella",
                               "Thomas", "Mia", "Charles", "Charlotte", "Daniel", "Amelia"]

                last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller",
                              "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez",
                              "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"]

                name = f"{random.choice(first_names)} {random.choice(last_names)}"

        # Generate identification (for businesses/institutions often)
        identification = None
        if random.random() < 0.4:  # 40% chance of having identifier
            id_types = ["ACC", "ID", "REF", "CUS", "REM", "ORG", "PAY", "SND"]
            id_prefix = random.choice(id_types)
            id_number = ''.join(random.choices('0123456789', k=random.randint(6, 10)))
            identification = f"{id_prefix}{id_number}"

        # Generate LEI for organizations (rarely used for ultimate debtors)
        lei = None
        if random.random() < 0.15:  # 15% chance of having LEI
            # Legal Entity Identifier format: [0-9A-Z]{18}[0-9]{2}
            lei_prefix = ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=18))
            lei_checksum = ''.join(random.choices('0123456789', k=2))
            lei = f"{lei_prefix}{lei_checksum}"

        # Generate scheme name (if identification provided)
        scheme_name = None
        if identification:
            # For ultimate debtors, scheme_name refers to the identification scheme for the originator
            schemes = [
                "Customer ID",
                "Account Number",
                "Remitter Reference",
                "Originator Code",
                "Payer Reference",
                "Order Number",
                "Tax ID",
                "Registration Number"
            ]
            scheme_name = random.choice(schemes)

        # Create the ultimate debtor dictionary
        ultimate_debtor = {
            "consumer_banking_transaction_id": id_fields['consumer_banking_transaction_id'],
            "name": name,
            "identification": identification,
            "lei": lei,
            "scheme_name": scheme_name
        }

        return ultimate_debtor

    finally:
        cursor.close()
