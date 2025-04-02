from ..enterprise.enums import CurrencyCode
from .enums import ExchangeRateProvider, ExchangeRateType
from data_generator import DataGenerator, SkipRowGenerationError
from typing import Any, Dict

import datetime
import random


def generate_random_transaction_currency_exchange(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random transaction currency exchange with plausible values.

    Args:
        id_fields: Dictionary containing the required ID fields
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated transaction currency exchange data
    """
    # Get database connection
    conn = dg.conn

    # Validate required fields
    if 'consumer_banking_transaction_id' not in id_fields:
        raise ValueError("consumer_banking_transaction_id is required")

    # Fetch the transaction to verify it exists and get its details
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT t.consumer_banking_transaction_id, t.transaction_date, 
                   t.amount, t.currency, t.transaction_type, t.category
            FROM consumer_banking.transactions t
            WHERE t.consumer_banking_transaction_id = %s
        """, (id_fields['consumer_banking_transaction_id'],))

        transaction = cursor.fetchone()

        if not transaction:
            raise ValueError(f"No transaction found with ID {id_fields['consumer_banking_transaction_id']}")

        # Extract relevant information
        transaction_date = transaction.get('transaction_date')
        target_currency = transaction.get('currency')
        amount = transaction.get('amount')
        transaction_type = transaction.get('transaction_type')
        category = transaction.get('category')

        # Derive whether the transaction is international based on:
        # 1. Non-USD currency
        # 2. Transaction category or type that suggests international activity
        is_international = (
                target_currency != CurrencyCode.USD.value or
                (category and 'INTERNATIONAL' in category.upper()) or
                (transaction_type and 'FOREIGN' in transaction_type.upper()) or
                random.random() < 0.15
        # Assume ~15% of transactions without other indicators might still be international
        )

        # Only generate currency exchange for international transactions
        # or transactions with non-default currency (with some exceptions)
        if not is_international and target_currency == CurrencyCode.USD.value and random.random() > 0.05:
            raise SkipRowGenerationError

        # Determine source currency
        # For international transactions, likely to be a foreign currency
        # Only generate plausible currency exchanges
        if is_international:
            # Exclude the target currency from the options
            source_currencies = [c for c in CurrencyCode if c.value != target_currency and not c.name.startswith('_')]

            # Common international currencies have higher weight
            common_international = [CurrencyCode.EUR, CurrencyCode.GBP, CurrencyCode.JPY,
                                    CurrencyCode.CAD, CurrencyCode.AUD, CurrencyCode.CHF]

            if random.random() < 0.8:  # 80% chance of using common international currency
                source_currency_options = [c for c in common_international if c.value != target_currency]
                if source_currency_options:
                    source_currency = random.choice(source_currency_options)
                else:
                    source_currency = random.choice(source_currencies)
            else:
                source_currency = random.choice(source_currencies)
        else:
            # For domestic transactions with currency exchange, target is likely foreign
            source_currency = CurrencyCode.USD  # Assuming USD as domestic currency

        # Generate exchange rate based on currency pair
        # Use realistic exchange rate ranges based on currency pairs
        # exchange_rate = None
        if source_currency == CurrencyCode.USD and target_currency == CurrencyCode.EUR.value:
            exchange_rate = round(random.uniform(0.8, 0.95), 6)
        elif source_currency == CurrencyCode.USD and target_currency == CurrencyCode.GBP.value:
            exchange_rate = round(random.uniform(0.7, 0.85), 6)
        elif source_currency == CurrencyCode.USD and target_currency == CurrencyCode.JPY.value:
            exchange_rate = round(random.uniform(100, 150), 6)
        elif source_currency == CurrencyCode.EUR and target_currency == CurrencyCode.USD.value:
            exchange_rate = round(random.uniform(1.05, 1.25), 6)
        elif source_currency == CurrencyCode.GBP and target_currency == CurrencyCode.USD.value:
            exchange_rate = round(random.uniform(1.2, 1.4), 6)
        elif source_currency == CurrencyCode.JPY and target_currency == CurrencyCode.USD.value:
            exchange_rate = round(random.uniform(0.006, 0.01), 6)
        else:
            # Generic exchange rate for other pairs
            exchange_rate = round(random.uniform(0.5, 2.0), 6)

        # Exchange rate provider
        exchange_rate_provider = ExchangeRateProvider.get_random()

        # Exchange rate type
        exchange_rate_type = ExchangeRateType.get_random()

        # Generate quotation date
        # Typically same day or 1-2 days before transaction
        days_before = random.randint(0, 2)
        quotation_date = transaction_date - datetime.timedelta(days=days_before)

        # Determine unit currency (usually one of the two currencies)
        if random.random() < 0.95:  # 95% chance it's one of the two currencies
            unit_currency = random.choice([source_currency.value, target_currency])
        else:
            # 5% chance it's a third currency
            unit_currencies = [c.value for c in CurrencyCode
                               if c.value != source_currency.value and c.value != target_currency]
            unit_currency = random.choice(unit_currencies)

        # Calculate instructed amount based on exchange rate
        # This would be the original amount before conversion
        if random.random() < 0.6:  # 60% chance we have the instructed amount
            if target_currency == unit_currency:
                instructed_amount = round(amount / exchange_rate, 2)
            else:
                instructed_amount = round(amount * exchange_rate, 2)

            instructed_amount_currency = source_currency.value
        else:
            instructed_amount = None
            instructed_amount_currency = None

        # Generate margin percentage (bank's markup on the exchange rate)
        margin_percentage = round(random.uniform(0.5, 4.5), 4)

        # Generate fee (optional - 70% chance)
        fee_amount = None
        fee_currency = None
        if random.random() < 0.7:
            # Fee is typically a percentage of the transaction or flat fee
            if random.random() < 0.6:  # 60% chance of percentage-based fee
                fee_amount = round(amount * random.uniform(0.01, 0.03), 2)  # 1-3% fee
            else:  # 40% chance of flat fee
                fee_amount = round(random.uniform(2.0, 15.0), 2)

            # Fee is typically in the target currency
            fee_currency = target_currency

        # Create the transaction currency exchange dictionary
        currency_exchange = {
            "consumer_banking_transaction_id": id_fields['consumer_banking_transaction_id'],
            "source_currency": source_currency.value,
            "target_currency": target_currency,
            "unit_currency": unit_currency,
            "exchange_rate": exchange_rate,
            "exchange_rate_provider": exchange_rate_provider.value,
            "exchange_rate_type": exchange_rate_type.value,
            "quotation_date": quotation_date,
            "instructed_amount": instructed_amount,
            "instructed_amount_currency": instructed_amount_currency,
            "margin_percentage": margin_percentage,
            "fee_amount": fee_amount,
            "fee_currency": fee_currency
        }

        return currency_exchange

    finally:
        cursor.close()
