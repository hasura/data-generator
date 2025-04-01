from .enums import StatementRateType
from data_generator import DataGenerator
from datetime import datetime, timedelta
from typing import Any, Dict

import pytz
import random


def generate_random_statement_rate(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random statement rate with plausible values.

    Args:
        id_fields: Dictionary containing the required ID fields
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated statement rate data
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
                   s.consumer_banking_account_id
            FROM consumer_banking.statements s
            WHERE s.consumer_banking_statement_id = %s
        """, (id_fields['consumer_banking_statement_id'],))

        statement = cursor.fetchone()

        if not statement:
            raise ValueError(f"No statement found with ID {id_fields['consumer_banking_statement_id']}")

        # Get the account ID to fetch product information
        account_id = statement.get('consumer_banking_account_id')

        # Extract statement data for reference
        start_date = statement.get('start_date_time')

        # Fetch product information for the account
        cursor.execute("""
            SELECT a.consumer_banking_product_id, p.product_type, p.is_interest_bearing
            FROM consumer_banking.accounts a
            JOIN consumer_banking.products p ON a.consumer_banking_product_id = p.consumer_banking_product_id
            WHERE a.consumer_banking_account_id = %s
        """, (account_id,))

        account_product = cursor.fetchone()

        # Default values if product info not found
        product_type = "CHECKING"
        is_interest_bearing = False

        if account_product:
            product_type = account_product.get('product_type', 'CHECKING')
            is_interest_bearing = account_product.get('is_interest_bearing', False)

        # Determine rate type
        rate_type = StatementRateType.get_random()

        # Adjust rate type selection based on product type
        if product_type in ['CREDIT_CARD']:
            # Credit products are more likely to have APR and promotional rates
            rate_weights = {
                StatementRateType.APR: 30.0,
                StatementRateType.CASH_ADVANCE_APR: 20.0,
                StatementRateType.BALANCE_TRANSFER_APR: 20.0,
                StatementRateType.PENALTY_APR: 10.0,
                StatementRateType.PROMOTIONAL_APR: 15.0,
                StatementRateType.INTRODUCTORY_RATE: 5.0
            }
            weighted_types = [k for k, v in rate_weights.items() for _ in range(int(v))]
            rate_type = random.choice(weighted_types)
        elif product_type in ['SAVINGS', 'MONEY_MARKET', 'CERTIFICATE_OF_DEPOSIT'] and is_interest_bearing:
            # Interest-bearing accounts are more likely to have savings rates
            rate_weights = {
                StatementRateType.SAVINGS_RATE: 40.0,
                StatementRateType.CD_RATE: 20.0,
                StatementRateType.EFFECTIVE_RATE: 20.0,
                StatementRateType.PROMOTIONAL_APR: 10.0,
                StatementRateType.INTRODUCTORY_RATE: 10.0
            }
            weighted_types = [k for k, v in rate_weights.items() for _ in range(int(v))]
            rate_type = random.choice(weighted_types)

        # Generate rate value based on type
        rate_value = None
        is_variable = False
        index_rate = None
        margin = None
        balance = None
        description = None
        effective_date = None
        expiration_date = None

        # Credit card APRs
        if rate_type in [StatementRateType.APR, StatementRateType.CASH_ADVANCE_APR,
                         StatementRateType.BALANCE_TRANSFER_APR, StatementRateType.PENALTY_APR]:
            # APR ranges typical for credit products
            if rate_type == StatementRateType.APR:
                rate_value = round(random.uniform(12.99, 24.99), 2)
                description = "Purchase APR"
            elif rate_type == StatementRateType.CASH_ADVANCE_APR:
                rate_value = round(random.uniform(19.99, 29.99), 2)
                description = "Cash Advance APR"
            elif rate_type == StatementRateType.BALANCE_TRANSFER_APR:
                rate_value = round(random.uniform(14.99, 26.99), 2)
                description = "Balance Transfer APR"
            elif rate_type == StatementRateType.PENALTY_APR:
                rate_value = round(random.uniform(24.99, 29.99), 2)
                description = "Penalty APR applied to late payments"

            # Determine if variable
            is_variable = random.random() < 0.7  # 70% of APRs are variable
            if is_variable:
                index_rate = round(random.uniform(3.0, 5.5), 2)  # Prime rate or similar
                margin = round(rate_value - index_rate, 2)
                description = f"Variable {description} (Prime + {margin}%)"

        # Promotional and Introductory APRs
        elif rate_type in [StatementRateType.PROMOTIONAL_APR, StatementRateType.INTRODUCTORY_RATE]:
            # Promotional rates are typically lower
            rate_value = round(random.uniform(0.0, 12.99), 2)

            # Promotions have limited time periods
            effective_date = start_date.date() - timedelta(days=random.randint(0, 90))
            months_duration = random.choice([6, 12, 15, 18])
            expiration_date = effective_date + timedelta(days=30 * months_duration)

            if rate_type == StatementRateType.PROMOTIONAL_APR:
                description = f"{rate_value}% Promotional APR for {months_duration} months"
            else:
                description = f"{rate_value}% Introductory Rate for {months_duration} months"

        # Savings and CD rates
        elif rate_type in [StatementRateType.SAVINGS_RATE, StatementRateType.CD_RATE]:
            # Savings rates are typically much lower than lending rates
            rate_value = round(random.uniform(0.05, 3.5), 2)

            if rate_type == StatementRateType.SAVINGS_RATE:
                description = "Annual Percentage Yield (APY)"
            else:
                term_months = random.choice([3, 6, 12, 18, 24, 36, 60])
                description = f"{term_months}-Month CD Rate"

        # Exchange rates
        elif rate_type == StatementRateType.EXCHANGE_RATE:
            # Common exchange rates (approximated)
            currency_pairs = {
                "USD/EUR": round(random.uniform(0.85, 0.95), 4),
                "USD/GBP": round(random.uniform(0.75, 0.85), 4),
                "USD/CAD": round(random.uniform(1.25, 1.40), 4),
                "USD/JPY": round(random.uniform(105.0, 145.0), 2),
                "USD/AUD": round(random.uniform(1.30, 1.50), 4)
            }

            pair, rate_value = random.choice(list(currency_pairs.items()))
            description = f"Exchange Rate for {pair}"

        # Reward rates
        elif rate_type == StatementRateType.REWARD_RATE:
            # Reward rates are typically 1-5% for credit cards
            reward_rates = [1.0, 1.5, 2.0, 3.0, 5.0]
            rate_value = random.choice(reward_rates)

            categories = ["all purchases", "grocery", "dining", "travel", "gas", "online shopping"]
            selected_category = random.choice(categories)
            description = f"{rate_value}% cash back on {selected_category}"

        # Other rate types
        else:
            # Generic rate handling for other types
            rate_value = round(random.uniform(0.05, 29.99), 2)
            description = f"{rate_type.value.replace('_', ' ')} - {rate_value}%"

        # Some rates apply to specific balances
        if rate_type in [StatementRateType.APR, StatementRateType.CASH_ADVANCE_APR,
                         StatementRateType.BALANCE_TRANSFER_APR, StatementRateType.PENALTY_APR,
                         StatementRateType.PROMOTIONAL_APR]:
            # Generate a plausible balance for this rate
            balance = round(random.uniform(100, 10000), 2)

        # Create the statement rate dictionary with UTC timezone
        utc = pytz.UTC
        now = datetime.now(utc)

        statement_rate = {
            "consumer_banking_statement_id": id_fields['consumer_banking_statement_id'],
            "rate": rate_value,
            "type": rate_type.value,  # Use name instead of value to match enum column type
            "description": description,
            "effective_date": effective_date,
            "expiration_date": expiration_date,
            "is_variable": is_variable,
            "index_rate": index_rate,
            "margin": margin,
            "balance_subject_to_rate": balance,
            "created_at": now,
            "updated_at": now
        }

        return statement_rate

    finally:
        cursor.close()
