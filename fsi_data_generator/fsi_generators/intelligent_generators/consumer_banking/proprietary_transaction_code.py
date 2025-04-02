from ..enterprise.enums import CreditDebitIndicator
from .enums.transaction import (TransactionCategory, TransactionStatus,
                                TransactionType)
from data_generator import DataGenerator, SkipRowGenerationError
from typing import Any, Dict

import random


def generate_random_proprietary_transaction_code(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random proprietary transaction code with plausible values,
    related to the referenced transaction.

    Args:
        id_fields: Dictionary containing the required ID fields
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated proprietary transaction code data
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
            SELECT t.consumer_banking_transaction_id, t.transaction_reference, 
                   t.credit_debit_indicator, t.status, t.category, t.transaction_type,
                   t.description, t.amount, t.merchant_address
            FROM consumer_banking.transactions t
            WHERE t.consumer_banking_transaction_id = %s
        """, (id_fields['consumer_banking_transaction_id'],))

        transaction = cursor.fetchone()

        if not transaction:
            raise ValueError(f"No transaction found with ID {id_fields['consumer_banking_transaction_id']}")

        # Extract transaction details to inform the proprietary code
        transaction_reference = transaction.get('transaction_reference')
        credit_debit_indicator = transaction.get('credit_debit_indicator')
        status = transaction.get('status')
        category = transaction.get('category')
        transaction_type = transaction.get('transaction_type')
        description = transaction.get('description', '')
        amount = transaction.get('amount', 0)
        merchant_address = transaction.get('merchant_address')

        # Convert string status to enum (if needed)
        try:
            status_enum = TransactionStatus[status] if isinstance(status, str) else status
        except (KeyError, TypeError):
            status_enum = TransactionStatus.OTHER

        # Convert string category to enum (if needed)
        try:
            category_enum = TransactionCategory[category] if isinstance(category, str) else category
        except (KeyError, TypeError):
            category_enum = TransactionCategory.OTHER

        # Convert string transaction_type to enum (if needed)
        try:
            type_enum = TransactionType[transaction_type] if isinstance(transaction_type, str) else transaction_type
        except (KeyError, TypeError):
            type_enum = TransactionType.OTHER

        # Not all transactions have proprietary codes - skip generation in some cases
        # Particularly for transactions in certain states
        if status_enum in [TransactionStatus.REJECTED, TransactionStatus.REVERSED,
                           TransactionStatus.CANCELLED] and random.random() < 0.7:
            raise SkipRowGenerationError

        # Determine issuer based on transaction category
        issuers = [
            "MASTERCARD", "VISA", "AMEX", "DISCOVER",  # Card networks
            "FISERV", "FIS", "JACK HENRY", "FINASTRA",  # Core banking providers
            "SWIFT", "NACHA", "FEDWIRE", "CHIPS",  # Payment networks
            "CLEARINGHOUSE", "THE CLEARING HOUSE",  # Payment clearing organizations
            "INTERNAL", "PROPRIETARY", "BANK SYSTEM",  # Bank's own systems
            "MERCHANT", "POS PROVIDER", "PROCESSOR",  # Merchant/POS systems
            "PAYPAL", "SQUARE", "STRIPE", "ADYEN",  # Payment processors
            "VENMO", "ZELLE", "CASH APP"  # P2P payment platforms
        ]

        # Select appropriate issuers based on transaction category
        potential_issuers = ["INTERNAL", "BANK SYSTEM"]  # Default

        if category_enum == TransactionCategory.PAYMENT:
            potential_issuers = ["SWIFT", "NACHA", "FEDWIRE", "CHIPS", "CLEARINGHOUSE",
                                 "THE CLEARING HOUSE", "INTERNAL", "BANK SYSTEM"]
        elif category_enum == TransactionCategory.POINT_OF_SALE:
            potential_issuers = ["MASTERCARD", "VISA", "AMEX", "DISCOVER", "MERCHANT",
                                 "POS PROVIDER", "PROCESSOR"]
        elif category_enum == TransactionCategory.CARD_PAYMENT:
            potential_issuers = ["MASTERCARD", "VISA", "AMEX", "DISCOVER", "PROCESSOR"]
        elif category_enum == TransactionCategory.DIRECT_DEBIT:
            potential_issuers = ["NACHA", "BANK SYSTEM", "INTERNAL"]
        elif category_enum == TransactionCategory.TRANSFER:
            potential_issuers = ["INTERNAL", "BANK SYSTEM", "FISERV", "FIS", "JACK HENRY", "FINASTRA"]
        elif category_enum == TransactionCategory.ATM:
            potential_issuers = ["ATM NETWORK", "MASTERCARD", "VISA", "BANK SYSTEM"]
        elif category_enum == TransactionCategory.FEE:
            potential_issuers = ["BANK SYSTEM", "INTERNAL", "FIS", "FISERV"]
        elif category_enum == TransactionCategory.CHECK:
            potential_issuers = ["BANK SYSTEM", "CLEARINGHOUSE", "THE CLEARING HOUSE"]
        else:
            # Default to all issuers with some weighting toward banking systems
            core_systems = ["FISERV", "FIS", "JACK HENRY", "FINASTRA", "INTERNAL", "BANK SYSTEM"]
            potential_issuers = issuers
            # Increase likelihood of core systems
            potential_issuers.extend(core_systems * 2)

        issuer = random.choice(potential_issuers)

        # Generate proprietary code based on issuer and transaction details
        if issuer in ["MASTERCARD", "VISA", "AMEX", "DISCOVER"]:
            # Card networks use standardized formats
            network_prefix = issuer[0:2]

            # Transaction type code
            type_mapping = {
                TransactionType.PURCHASE: 'PR',
                TransactionType.CASH_WITHDRAWAL: 'CW',
                TransactionType.REFUND: 'RF',
                TransactionType.BILL_PAYMENT: 'BP',
                TransactionType.RETAIL: 'RT',
                TransactionType.FOOD_DINING: 'FD',
                TransactionType.TRAVEL: 'TV',
                TransactionType.ENTERTAINMENT: 'ET'
            }
            type_code = type_mapping.get(type_enum, 'OT')

            # Transaction sequence
            seq = ''.join(random.choices('0123456789', k=8))

            # Format for card networks: NETWORK-TYPE-SEQ
            code = f"{network_prefix}{type_code}{seq}"

        elif issuer in ["SWIFT", "NACHA", "FEDWIRE", "CHIPS"]:
            # Payment networks often use standardized codes
            # Date component (YYMMDD)
            date_component = ''.join(random.choices('0123456789', k=6))

            # Indicator for credit/debit
            try:
                cd_indicator = "C" if credit_debit_indicator == CreditDebitIndicator.CREDIT else "D"
            except (TypeError, AttributeError):
                # Fallback if not a proper enum
                cd_indicator = "C" if str(credit_debit_indicator).upper() == "CREDIT" else "D"

            # Format payment type
            payment_type_mapping = {
                TransactionType.BILL_PAYMENT: 'BILL',
                TransactionType.SALARY: 'SLRY',
                TransactionType.TAX_PAYMENT: 'TAXP',
                TransactionType.UTILITY_PAYMENT: 'UTIL',
                TransactionType.RENT_PAYMENT: 'RENT',
                TransactionType.MORTGAGE_PAYMENT: 'MRTG',
                TransactionType.INSURANCE_PREMIUM: 'INSR',
                TransactionType.DONATION: 'DONA',
                TransactionType.INTERNAL_TRANSFER: 'INTR',
                TransactionType.EXTERNAL_TRANSFER: 'EXTR'
            }
            payment_code = payment_type_mapping.get(type_enum, 'PMNT')

            # Format for payment networks: NETWORK-DATE-CD-TYPE
            code = f"{issuer[:3]}{date_component}{cd_indicator}{payment_code}"

        elif issuer in ["FISERV", "FIS", "JACK HENRY", "FINASTRA"]:
            # Core banking systems typically use structured codes

            # Category code
            category_mapping = {
                TransactionCategory.PAYMENT: 'PMT',
                TransactionCategory.DEPOSIT: 'DEP',
                TransactionCategory.WITHDRAWAL: 'WTH',
                TransactionCategory.FEE: 'FEE',
                TransactionCategory.INTEREST: 'INT',
                TransactionCategory.TRANSFER: 'TRF',
                TransactionCategory.ATM: 'ATM',
                TransactionCategory.POINT_OF_SALE: 'POS',
                TransactionCategory.CARD_PAYMENT: 'CRD',
                TransactionCategory.DIRECT_DEBIT: 'DDB',
                TransactionCategory.STANDING_ORDER: 'STD',
                TransactionCategory.CREDIT: 'CRD',
                TransactionCategory.DEBIT: 'DBT',
                TransactionCategory.REVERSAL: 'REV',
                TransactionCategory.ADJUSTMENT: 'ADJ',
                TransactionCategory.CHECK: 'CHK',
                TransactionCategory.LOAN_DISBURSEMENT: 'LND',
                TransactionCategory.LOAN_PAYMENT: 'LNP'
            }
            category_code = category_mapping.get(category_enum, 'GEN')

            # Julian date (day of year 001-366)
            julian_date = str(random.randint(1, 366)).zfill(3)

            # Batch number
            batch = str(random.randint(1, 999)).zfill(3)

            # Sequence in batch
            seq = str(random.randint(1, 9999)).zfill(4)

            # Format for core systems: CAT-JULIAN-BATCH-SEQ
            code = f"{category_code}{julian_date}{batch}{seq}"

        elif issuer in ["INTERNAL", "PROPRIETARY", "BANK SYSTEM"]:
            # Internal systems often use combinations of meaningful components

            # Branch code
            branch = str(random.randint(1, 999)).zfill(3)

            # Teller/system ID
            teller = str(random.randint(1, 99)).zfill(2)

            # Transaction type code
            type_mapping = {
                TransactionType.PURCHASE: 'PUR',
                TransactionType.CASH_WITHDRAWAL: 'CSH',
                TransactionType.REFUND: 'REF',
                TransactionType.BILL_PAYMENT: 'BIL',
                TransactionType.SALARY: 'SAL',
                TransactionType.SUBSCRIPTION: 'SUB',
                TransactionType.DIVIDEND: 'DIV',
                TransactionType.TAX_PAYMENT: 'TAX',
                TransactionType.TAX_REFUND: 'TRF',
                TransactionType.INTERNAL_TRANSFER: 'INT',
                TransactionType.EXTERNAL_TRANSFER: 'EXT',
                TransactionType.MERCHANT_PAYMENT: 'MER',
                TransactionType.UTILITY_PAYMENT: 'UTL',
                TransactionType.RENT_PAYMENT: 'RNT',
                TransactionType.MORTGAGE_PAYMENT: 'MTG',
                TransactionType.INVESTMENT: 'INV',
                TransactionType.INSURANCE_PREMIUM: 'INS',
                TransactionType.DONATION: 'DON'
            }
            type_code = type_mapping.get(type_enum, 'GEN')

            # Transaction sequence
            seq = str(random.randint(1, 999999)).zfill(6)

            # Format for internal systems: BRANCH-TELLER-TYPE-SEQ
            code = f"{branch}{teller}{type_code}{seq}"

        elif issuer in ["PAYPAL", "SQUARE", "STRIPE", "ADYEN", "VENMO", "ZELLE", "CASH APP"]:
            # Payment processors often use web-friendly formats

            # Create alphanumeric code with processor-specific prefix
            prefix = issuer[:2].upper()

            # Transaction type as part of code
            type_mapping = {
                TransactionType.PURCHASE: 'p',
                TransactionType.REFUND: 'r',
                TransactionType.BILL_PAYMENT: 'b',
                TransactionType.SUBSCRIPTION: 's',
                TransactionType.DONATION: 'd',
                TransactionType.MERCHANT_PAYMENT: 'm',
                TransactionType.EXTERNAL_TRANSFER: 't',
                TransactionType.INTERNAL_TRANSFER: 'i'
            }
            type_char = type_mapping.get(type_enum, 'x')

            # Random parts
            alpha_part = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=3))
            numeric_part = ''.join(random.choices('0123456789', k=8))

            # Format for payment processors: PREFIX_TYPE_ALPHA_NUMERIC
            code = f"{prefix}_{type_char}_{alpha_part}_{numeric_part}"

        else:
            # Generic format for other issuers - merchant or POS systems

            # Use parts of merchant address if available
            merchant_code = "M"
            if merchant_address:
                # Take first letters of merchant address words
                merchant_code = ''.join([word[0] for word in merchant_address.split(' ') if word])[:3]

            # Terminal/register ID
            terminal = str(random.randint(1, 999)).zfill(3)

            # Transaction type abbreviation
            type_mapping = {
                TransactionType.PURCHASE: 'P',
                TransactionType.REFUND: 'R',
                TransactionType.FOOD_DINING: 'F',
                TransactionType.ENTERTAINMENT: 'E',
                TransactionType.RETAIL: 'S',
                TransactionType.TRAVEL: 'T',
                TransactionType.HEALTHCARE: 'H',
                TransactionType.EDUCATION: 'D'
            }
            type_code = type_mapping.get(type_enum, 'X')

            # Transaction date code (MMDD)
            date_code = ''.join(random.choices('0123456789', k=4))

            # Transaction sequence
            seq = str(random.randint(1, 9999)).zfill(4)

            # Format for merchant systems: MERCH-TERM-TYPE-DATE-SEQ
            code = f"{merchant_code}{terminal}{type_code}{date_code}{seq}"

        # If the transaction has a reference, incorporate it sometimes
        if transaction_reference and random.random() < 0.3:
            # Take a portion of the transaction reference and add it
            ref_part = ''.join(c for c in transaction_reference if c.isalnum())[:6]
            if ref_part:
                code = f"{code}-{ref_part}"

        # Ensure code doesn't exceed 35 characters
        if len(code) > 35:
            code = code[:35]

        # Create the proprietary transaction code dictionary
        proprietary_code = {
            "consumer_banking_transaction_id": id_fields['consumer_banking_transaction_id'],
            "code": code,
            "issuer": issuer
        }

        return proprietary_code

    finally:
        cursor.close()
