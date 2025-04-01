from .enums import BeneficiaryType
from data_generator import DataGenerator
from typing import Any, Dict

import random


def generate_random_beneficiary(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random consumer banking beneficiary with plausible values.

    Args:
        id_fields: Dictionary containing the required ID fields
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated beneficiary data
    """
    # Get database connection
    conn = dg.conn

    # Validate required fields
    if 'consumer_banking_account_id' not in id_fields:
        raise ValueError("consumer_banking_account_id is required")

    # Fetch the consumer banking account to verify it exists
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT consumer_banking_account_id 
            FROM consumer_banking.accounts 
            WHERE consumer_banking_account_id = %s
        """, (id_fields['consumer_banking_account_id'],))

        consumer_account = cursor.fetchone()

        if not consumer_account:
            raise ValueError(f"No consumer banking account found with ID {id_fields['consumer_banking_account_id']}")

        # Determine beneficiary type using the enum
        beneficiary_type = BeneficiaryType.get_random()

        # Generate reference ID (optional - 70% chance of having one)
        reference = None
        if random.random() < 0.7:
            reference_length = random.randint(8, 25)
            reference = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=reference_length))

        # Generate supplementary data (optional - 40% chance of having some)
        supplementary_data = None
        if random.random() < 0.4:
            # Generate more detailed information based on beneficiary type
            if beneficiary_type == BeneficiaryType.INDIVIDUAL:
                supplementary_data_options = [
                    "Family member",
                    "Friend",
                    "Regular payment recipient",
                    "One-time payment",
                    "Contractor for home services",
                    "Healthcare provider",
                    "Rent payment"
                ]
            elif beneficiary_type == BeneficiaryType.MERCHANT:
                supplementary_data_options = [
                    "Online retailer",
                    "Local business",
                    "Subscription service",
                    "E-commerce platform",
                    "Wholesale supplier"
                ]
            elif beneficiary_type == BeneficiaryType.UTILITY:
                supplementary_data_options = [
                    "Electric company",
                    "Water service",
                    "Gas provider",
                    "Internet service provider",
                    "Mobile phone carrier",
                    "Cable/satellite TV"
                ]
            else:
                supplementary_data_options = [
                    "Regular payment",
                    "Scheduled transfer",
                    "Standing order recipient",
                    "Payment for services",
                    "Bill payment"
                ]

            supplementary_data = random.choice(supplementary_data_options)

        # Create the beneficiary dictionary
        beneficiary = {
            "consumer_banking_account_id": id_fields['consumer_banking_account_id'],
            "beneficiary_type": beneficiary_type.value,
            "reference": reference,
            "supplementary_data": supplementary_data
        }

        return beneficiary

    finally:
        cursor.close()
