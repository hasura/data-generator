from data_generator import DataGenerator, SkipRowGenerationError
from typing import Any, Dict

from .enums import TransactionBankCode


prev_codes = set()
def generate_random_transaction_bank_transaction_code(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random bank transaction code record with plausible values.

    Args:
        id_fields: Dictionary containing the required ID fields
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated transaction bank transaction code data
    """
    # Get database connection
    conn = dg.conn

    # Validate required fields
    if 'consumer_banking_transaction_id' not in id_fields:
        raise ValueError("consumer_banking_transaction_id is required")

    # Fetch the transaction to verify it exists
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT t.consumer_banking_transaction_id
            FROM consumer_banking.transactions t
            WHERE t.consumer_banking_transaction_id = %s
        """, (id_fields['consumer_banking_transaction_id'],))

        transaction = cursor.fetchone()

        if not transaction:
            raise ValueError(f"No transaction found with ID {id_fields['consumer_banking_transaction_id']}")

        # Use get_random from BaseEnum
        transaction_code = TransactionBankCode.get_random()

        # Create the transaction bank transaction code dictionary
        transaction_bank_transaction_code = {
            "consumer_banking_transaction_id": id_fields['consumer_banking_transaction_id'],
            "code": transaction_code.value
        }

        prev = (id_fields['consumer_banking_transaction_id'], transaction_code.value)
        if prev in prev_codes:
            raise SkipRowGenerationError

        prev_codes.add(prev)

        return transaction_bank_transaction_code

    finally:
        cursor.close()
