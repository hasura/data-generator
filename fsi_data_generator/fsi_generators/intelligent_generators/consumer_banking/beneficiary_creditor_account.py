from ..enterprise import (generate_financial_institution_identifier,
                          generate_financial_institution_identifier_for_type,
                          generate_financial_institution_name)
from .enums import BeneficiaryType
from data_generator import DataGenerator
from typing import Any, Dict

import random


def generate_random_beneficiary_creditor_account(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random beneficiary creditor account with plausible values.

    Args:
        id_fields: Dictionary containing the required ID fields
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated beneficiary creditor account data
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
            SELECT b.consumer_banking_beneficiary_id, b.beneficiary_type 
            FROM consumer_banking.beneficiaries b
            WHERE b.consumer_banking_beneficiary_id = %s
        """, (id_fields['consumer_banking_beneficiary_id'],))

        beneficiary = cursor.fetchone()

        if not beneficiary:
            raise ValueError(f"No beneficiary found with ID {id_fields['consumer_banking_beneficiary_id']}")

        beneficiary_type = beneficiary.get('beneficiary_type')

        # Check if there's already a creditor agent for this beneficiary
        cursor.execute("""
            SELECT scheme_name, name 
            FROM consumer_banking.beneficiary_creditor_agents 
            WHERE consumer_banking_beneficiary_id = %s
        """, (id_fields['consumer_banking_beneficiary_id'],))

        creditor_agent = cursor.fetchone()
        agent_name = None

        if creditor_agent:
            agent_name = creditor_agent.get('name')

        # For financial institutions, use a more targeted approach based on type
        if beneficiary_type == BeneficiaryType.FINANCIAL_INSTITUTION.value:
            # Financial institutions use more specific schemes
            scheme_name, identification, lei = generate_financial_institution_identifier_for_type(
                "FINANCIAL_INSTITUTION")
            # Generate institution name for account
            name = generate_financial_institution_name()
        else:
            # Region simulation - choose a random region for this beneficiary
            regions = ["EU", "UK", "US", "ASIA", "OTHER"]
            region_weights = [30, 20, 30, 15, 5]
            region = random.choices(regions, weights=region_weights, k=1)[0]

            # Generate appropriate financial identifiers based on region
            scheme_name, identification, lei = generate_financial_institution_identifier(region)

            # Generate account name based on beneficiary type
            if beneficiary_type == BeneficiaryType.INDIVIDUAL.value:
                # For individuals, use names
                first_names = ["John", "Jane", "Michael", "Sarah", "David", "Emily", "James", "Emma", "Robert",
                               "Olivia"]
                last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
                              "Rodriguez",
                              "Martinez"]
                name = f"{random.choice(first_names)} {random.choice(last_names)}"
            elif agent_name:
                # If there's a creditor agent, use its name for the account name
                name = agent_name
            else:
                # For organizations, create a business name
                business_prefixes = ["Global", "National", "Premier", "Elite", "Advanced", "Century", "United",
                                     "Reliable",
                                     "Precision", "Innovative"]
                business_cores = ["Tech", "Services", "Solutions", "Enterprises", "Industries", "Systems", "Group",
                                  "Associates", "Partners", "Consulting"]
                business_suffixes = ["Inc.", "LLC", "Ltd.", "Corp.", "Company", "International", "Holdings", "Group",
                                     "Co.",
                                     ""]

                name = f"{random.choice(business_prefixes)} {random.choice(business_cores)} {random.choice(business_suffixes)}".strip()

        # Secondary identification (optional - 30% chance)
        secondary_identification = None
        if random.random() < 0.3:
            # Usually a reference number or internal bank identifier
            secondary_identification = ''.join(
                random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=random.randint(5, 10)))

        # Create the creditor account dictionary
        creditor_account = {
            "consumer_banking_beneficiary_id": id_fields['consumer_banking_beneficiary_id'],
            "scheme_name": scheme_name.value,
            "identification": identification,
            "name": name,
            "secondary_identification": secondary_identification
        }

        # Add LEI if available
        if lei:
            creditor_account["lei"] = lei

        return creditor_account

    finally:
        cursor.close()
