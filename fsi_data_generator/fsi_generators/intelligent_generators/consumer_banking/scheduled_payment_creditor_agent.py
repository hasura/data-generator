from ..enterprise import (generate_financial_institution_identifier,
                          generate_financial_institution_name)
from data_generator import DataGenerator
from typing import Any, Dict

import random


def generate_random_scheduled_payment_creditor_agent(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random scheduled payment creditor agent with plausible values.

    Args:
        id_fields: Dictionary containing the required ID fields
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated scheduled payment creditor agent data
    """
    # Get database connection
    conn = dg.conn

    # Validate required fields
    if 'consumer_banking_scheduled_payment_id' not in id_fields:
        raise ValueError("consumer_banking_scheduled_payment_id is required")

    # Fetch the scheduled payment to verify it exists
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT consumer_banking_scheduled_payment_id 
            FROM consumer_banking.scheduled_payments 
            WHERE consumer_banking_scheduled_payment_id = %s
        """, (id_fields['consumer_banking_scheduled_payment_id'],))

        scheduled_payment = cursor.fetchone()

        if not scheduled_payment:
            raise ValueError(f"No scheduled payment found with ID {id_fields['consumer_banking_scheduled_payment_id']}")

        # Simulate a region for this agent
        regions = ["EU", "UK", "US", "ASIA", "OTHER"]
        region_weights = [30, 20, 30, 15, 5]
        region = random.choices(regions, weights=region_weights, k=1)[0]

        # Generate identifier scheme and value
        scheme_name, identification, lei = generate_financial_institution_identifier(region)

        # Generate institution name
        name = generate_financial_institution_name(region)

        # Create the creditor agent dictionary
        creditor_agent = {
            "consumer_banking_scheduled_payment_id": id_fields['consumer_banking_scheduled_payment_id'],
            "scheme_name": scheme_name.value,
            "identification": identification,
            "name": name,
            "lei": lei
        }

        return creditor_agent

    finally:
        cursor.close()
