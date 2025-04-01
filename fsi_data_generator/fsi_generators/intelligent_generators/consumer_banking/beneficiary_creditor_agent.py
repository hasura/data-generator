from ..enterprise import (generate_financial_institution_identifier,
                          generate_financial_institution_identifier_for_type,
                          generate_financial_institution_name)
from .enums import BeneficiaryType
from data_generator import DataGenerator
from typing import Any, Dict


def generate_random_beneficiary_creditor_agent(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random beneficiary creditor agent with plausible values.

    Args:
        id_fields: Dictionary containing the required ID fields
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated beneficiary creditor agent data
    """
    # Get database connection
    conn = dg.conn

    # Validate required fields
    if 'consumer_banking_beneficiary_id' not in id_fields:
        raise ValueError("consumer_banking_beneficiary_id is required")

    # Fetch the beneficiary to verify it exists and get its type
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT consumer_banking_beneficiary_id, beneficiary_type 
            FROM consumer_banking.beneficiaries 
            WHERE consumer_banking_beneficiary_id = %s
        """, (id_fields['consumer_banking_beneficiary_id'],))

        beneficiary = cursor.fetchone()

        if not beneficiary:
            raise ValueError(f"No beneficiary found with ID {id_fields['consumer_banking_beneficiary_id']}")

        beneficiary_type = beneficiary.get('beneficiary_type')

        # Determine region for identifier generation
        # For financial institutions, use a more targeted approach based on type
        if beneficiary_type == BeneficiaryType.FINANCIAL_INSTITUTION.value:
            # Financial institutions use more specific schemes
            # Generate regional identifier with emphasis on appropriate identifiers for financial institutions
            scheme_name, identification, lei = generate_financial_institution_identifier_for_type(
                "FINANCIAL_INSTITUTION")
        else:
            # For other beneficiary types, use standard region-based generation
            scheme_name, identification, lei = generate_financial_institution_identifier()

        # Generate institution name
        name = generate_financial_institution_name()

        # Create the creditor agent dictionary
        creditor_agent = {
            "consumer_banking_beneficiary_id": id_fields['consumer_banking_beneficiary_id'],
            "scheme_name": scheme_name.value,
            "identification": identification,
            "name": name,
            "lei": lei
        }

        return creditor_agent

    finally:
        cursor.close()
