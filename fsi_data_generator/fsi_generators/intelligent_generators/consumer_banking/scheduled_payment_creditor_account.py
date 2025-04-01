from ..enterprise import (generate_financial_institution_identifier,
                          generate_financial_institution_name)
from ..enterprise.enums import AccountIdentifierScheme
from data_generator import DataGenerator
from typing import Any, Dict

import random


def generate_random_scheduled_payment_creditor_account(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random scheduled payment creditor account with plausible values.

    Args:
        id_fields: Dictionary containing the required ID fields
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated scheduled payment creditor account data
    """
    # Get database connection
    conn = dg.conn

    # Validate required fields
    if 'consumer_banking_scheduled_payment_id' not in id_fields:
        raise ValueError("consumer_banking_scheduled_payment_id is required")

    # Fetch the scheduled payment to verify it exists and get additional context
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT sp.consumer_banking_scheduled_payment_id, sp.payment_method 
            FROM consumer_banking.scheduled_payments sp
            WHERE sp.consumer_banking_scheduled_payment_id = %s
        """, (id_fields['consumer_banking_scheduled_payment_id'],))

        scheduled_payment = cursor.fetchone()

        if not scheduled_payment:
            raise ValueError(f"No scheduled payment found with ID {id_fields['consumer_banking_scheduled_payment_id']}")

        payment_method = scheduled_payment.get('payment_method')

        # Check if there's already a creditor agent for this scheduled payment
        cursor.execute("""
            SELECT scheme_name, name 
            FROM consumer_banking.scheduled_payment_creditor_agents 
            WHERE consumer_banking_scheduled_payment_id = %s
        """, (id_fields['consumer_banking_scheduled_payment_id'],))

        creditor_agent = cursor.fetchone()
        agent_name = None

        if creditor_agent:
            agent_name = creditor_agent.get('name')

        # Payment method can influence the type of account identifiers used
        # Wire transfers are more likely to use international formats like IBAN
        # ACH transfers in the US use account number + routing number
        # Internal transfers might use proprietary formats

        if payment_method == 'WIRE':
            # International transfers need more specific schemes
            regions = ["EU", "UK", "ASIA", "OTHER"]
            region_weights = [40, 25, 20, 15]
            region = random.choices(regions, weights=region_weights, k=1)[0]
            scheme_name, identification, lei = generate_financial_institution_identifier(region)

        elif payment_method == 'ACH':
            # ACH is primarily US-based
            scheme_name, identification, lei = generate_financial_institution_identifier("US")

        elif payment_method == 'INTERNAL':
            # For internal transfers, use account number format
            scheme_name = AccountIdentifierScheme.ACCOUNT_NUMBER
            identification = ''.join(random.choices('0123456789', k=random.randint(8, 12)))
            lei = None

        else:
            # For other payment methods, use standard financial identifier generation
            scheme_name, identification, lei = generate_financial_institution_identifier()

        # Generate appropriate account name
        if agent_name:
            # If there's a creditor agent, use its name for the account name
            name = agent_name
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

        # Secondary identification (optional - 25% chance)
        secondary_identification = None
        if random.random() < 0.25:
            # Usually a reference number or internal bank identifier
            secondary_identification = ''.join(
                random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=random.randint(5, 10)))

        # Create the creditor account dictionary
        creditor_account = {
            "consumer_banking_scheduled_payment_id": id_fields['consumer_banking_scheduled_payment_id'],
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
