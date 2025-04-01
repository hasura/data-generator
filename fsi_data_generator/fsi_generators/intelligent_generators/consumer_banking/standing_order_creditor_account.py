from ..enterprise import (generate_financial_institution_identifier,
                          generate_financial_institution_name)
from data_generator import DataGenerator
from typing import Any, Dict


def generate_random_standing_order_creditor_account(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random standing order creditor account with plausible values.

    Args:
        id_fields: Dictionary containing the required ID fields
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated standing order creditor account data
    """
    # Get database connection
    conn = dg.conn

    # Validate required fields
    if 'consumer_banking_standing_order_id' not in id_fields:
        raise ValueError("consumer_banking_standing_order_id is required")

    # Fetch the standing order to verify it exists
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT so.consumer_banking_standing_order_id
            FROM consumer_banking.standing_orders so
            WHERE so.consumer_banking_standing_order_id = %s
        """, (id_fields['consumer_banking_standing_order_id'],))

        standing_order = cursor.fetchone()

        if not standing_order:
            raise ValueError(f"No standing order found with ID {id_fields['consumer_banking_standing_order_id']}")

        # Generate appropriate account identifiers
        # This will produce region-appropriate identifiers
        scheme_name, identification, secondary_identification = generate_financial_institution_identifier()

        # Generate standard financial institution name
        name = generate_financial_institution_name()

        # Create the creditor account dictionary
        creditor_account = {
            "consumer_banking_standing_order_id": id_fields['consumer_banking_standing_order_id'],
            "scheme_name": scheme_name.value,
            "identification": identification,
            "name": name,
            "secondary_identification": secondary_identification
        }

        return creditor_account

    finally:
        cursor.close()
