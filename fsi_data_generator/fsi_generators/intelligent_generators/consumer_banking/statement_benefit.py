from ..enterprise.enums import CurrencyCode
from .enums import BenefitType
from data_generator import DataGenerator, SkipRowGenerationError
from typing import Any, Dict

import random


def generate_random_statement_benefit(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random consumer banking statement benefit with plausible values.

    Args:
        id_fields: Dictionary containing the required ID fields
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated statement benefit data
    """
    # Get database connection
    conn = dg.conn

    # Validate required fields
    if 'consumer_banking_statement_id' not in id_fields:
        raise ValueError("consumer_banking_statement_id is required")

    # Fetch the statement to verify it exists and get additional context
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT s.consumer_banking_statement_id, s.start_date_time, s.end_date_time,
                   s.consumer_banking_account_id, a.status, p.product_type
            FROM consumer_banking.statements s
            JOIN consumer_banking.accounts a ON s.consumer_banking_account_id = a.consumer_banking_account_id
            JOIN consumer_banking.products p ON a.consumer_banking_product_id = p.consumer_banking_product_id
            WHERE s.consumer_banking_statement_id = %s
        """, (id_fields['consumer_banking_statement_id'],))

        statement = cursor.fetchone()

        if not statement:
            raise ValueError(f"No statement found with ID {id_fields['consumer_banking_statement_id']}")

        # Extract relevant information
        account_status = statement.get('status')
        product_type = statement.get('product_type')

        # Only generate benefits for active accounts
        if account_status != 'ACTIVE':
            raise SkipRowGenerationError

        # Select benefit type based on product type
        # Different product types may have different typical benefits
        if product_type in ['PREMIUM', 'CREDIT_CARD', 'REWARDS_CHECKING']:
            # Premium products have more rewards
            benefit_weights = {
                BenefitType.CASHBACK: 30,
                BenefitType.POINTS: 25,
                BenefitType.MILES: 15,
                BenefitType.DISCOUNT: 10,
                BenefitType.INSURANCE: 5,
                BenefitType.FEE_WAIVER: 5,
                BenefitType.PROMOTIONAL: 5,
                BenefitType.LOYALTY: 3,
                BenefitType.REFERRAL: 1,
                BenefitType.ANNIVERSARY: 1,
                BenefitType.OTHER: 0
            }
        elif product_type in ['SAVINGS', 'MONEY_MARKET', 'CERTIFICATE_OF_DEPOSIT']:
            # Interest-bearing accounts focus on interest
            benefit_weights = {
                BenefitType.INTEREST: 80,
                BenefitType.FEE_WAIVER: 10,
                BenefitType.PROMOTIONAL: 5,
                BenefitType.LOYALTY: 3,
                BenefitType.REFERRAL: 1,
                BenefitType.ANNIVERSARY: 1,
                BenefitType.OTHER: 0
            }
        else:
            # Standard checking accounts have fewer benefits
            benefit_weights = {
                BenefitType.FEE_WAIVER: 40,
                BenefitType.CASHBACK: 20,
                BenefitType.POINTS: 15,
                BenefitType.PROMOTIONAL: 10,
                BenefitType.DISCOUNT: 8,
                BenefitType.REFERRAL: 5,
                BenefitType.OTHER: 2
            }

        # Get all available benefit types and their weights
        benefit_types = []
        weights = []
        for benefit_type, weight in benefit_weights.items():
            if weight > 0:
                benefit_types.append(benefit_type)
                weights.append(weight)

        # Select a benefit type
        benefit_type = random.choices(benefit_types, weights=weights, k=1)[0]

        # Generate benefit amount based on type
        if benefit_type == BenefitType.CASHBACK:
            # Cashback is typically 1-5% of spending
            amount = round(random.uniform(5, 150), 2)
        elif benefit_type == BenefitType.POINTS:
            # Points are usually whole numbers
            amount = random.randint(100, 2000)
        elif benefit_type == BenefitType.MILES:
            # Miles are usually whole numbers
            amount = random.randint(100, 5000)
        elif benefit_type == BenefitType.INTEREST:
            # Interest earned
            amount = round(random.uniform(0.01, 200), 2)
        elif benefit_type == BenefitType.DISCOUNT:
            # Discount amount
            amount = round(random.uniform(5, 50), 2)
        elif benefit_type == BenefitType.FEE_WAIVER:
            # Waived fee amount
            amount = round(random.uniform(5, 30), 2)
        elif benefit_type == BenefitType.PROMOTIONAL:
            # Promotional benefit
            amount = round(random.uniform(10, 100), 2)
        elif benefit_type == BenefitType.LOYALTY:
            # Loyalty reward
            amount = round(random.uniform(5, 75), 2)
        elif benefit_type == BenefitType.REFERRAL:
            # Referral bonus
            amount = round(random.uniform(25, 100), 2)
        elif benefit_type == BenefitType.ANNIVERSARY:
            # Anniversary bonus
            amount = round(random.uniform(10, 50), 2)
        else:  # OTHER
            amount = round(random.uniform(1, 25), 2)

        # Choose currency (predominantly USD)
        currency_options = [CurrencyCode.USD, CurrencyCode.EUR, CurrencyCode.GBP]
        currency_weights = [90, 7, 3]  # USD is most common
        currency = random.choices(currency_options, weights=currency_weights, k=1)[0]

        # Create the statement benefit dictionary
        statement_benefit = {
            "consumer_banking_statement_id": id_fields['consumer_banking_statement_id'],
            "type": benefit_type.value,
            "amount": amount,
            "currency": currency.value
        }

        return statement_benefit

    finally:
        cursor.close()
