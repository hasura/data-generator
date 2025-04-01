from ..enterprise.enums import CreditDebitIndicator, CurrencyCode
from .enums import (AccountStatus, TransactionCategory, TransactionMutability,
                    TransactionStatus, TransactionType)
from data_generator import DataGenerator, SkipRowGenerationError
from datetime import datetime, timedelta, timezone
from typing import Any, Dict

import random


def generate_random_transaction(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random consumer banking transaction with plausible values.

    Args:
        id_fields: Dictionary containing the required ID fields
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated transaction data
    """
    # Get database connection
    conn = dg.conn

    # Validate required fields
    if 'consumer_banking_account_id' not in id_fields:
        raise ValueError("consumer_banking_account_id is required")

    # Fetch the account to verify it exists and get additional context
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT a.consumer_banking_account_id, a.status, a.status_update_date_time, a.opened_date, b.amount AS balance, b.type 
            FROM consumer_banking.accounts a
            JOIN consumer_banking.balances b ON a.consumer_banking_account_id = b.consumer_banking_account_id
            WHERE a.consumer_banking_account_id = %s
            AND b.type = 'CURRENT'
            ORDER BY b.date_time DESC
            LIMIT 1
        """, (id_fields['consumer_banking_account_id'],))

        account_data = cursor.fetchone()

        if not account_data:
            # Most likely no balance has been generated
            raise SkipRowGenerationError

        account_opened_date = account_data.get('opened_date')
        # current_balance = account_data.get('balance', 0)

        # Generate a plausible transaction date
        # It should be:
        # 1. After the account opened date
        # 2. Within the last 20 years
        # 3. Not in the future

        now = datetime.now(timezone.utc)
        last_date = now
        if account_data.get('status') != AccountStatus.ACTIVE.value:
            last_date = account_data.get('status_update_date_time')
        if last_date <= account_opened_date:
            raise SkipRowGenerationError

        earliest_date = min(
            account_opened_date,  # After account opened
            last_date
        )

        # Generate random transaction date between earliest date and now
        days_range = (now - earliest_date).days
        if days_range <= 0:
            # If account was just opened, use today's date
            transaction_date = now
        else:
            random_days = random.randint(0, days_range)
            transaction_date = earliest_date + timedelta(days=random_days)

        # Select random transaction category using default weights
        chosen_category = TransactionCategory.get_random()

        # Select transaction type that makes sense for the category
        # For some categories, specific types are more appropriate
        if chosen_category == TransactionCategory.PAYMENT:
            type_options = [
                TransactionType.BILL_PAYMENT,
                TransactionType.MERCHANT_PAYMENT,
                TransactionType.UTILITY_PAYMENT
            ]
            chosen_type = random.choice(type_options)
        elif chosen_category == TransactionCategory.DEPOSIT:
            type_options = [
                TransactionType.SALARY,
                TransactionType.REFUND,
                TransactionType.TAX_REFUND
            ]
            chosen_type = random.choice(type_options)
        elif chosen_category == TransactionCategory.ATM:
            chosen_type = TransactionType.CASH_WITHDRAWAL
        elif chosen_category == TransactionCategory.DIRECT_DEBIT:
            type_options = [
                TransactionType.BILL_PAYMENT,
                TransactionType.UTILITY_PAYMENT,
                TransactionType.INSURANCE_PREMIUM,
                TransactionType.SUBSCRIPTION
            ]
            chosen_type = random.choice(type_options)
        else:
            # Use random type appropriate for the category
            chosen_type = TransactionType.get_random()

        # Determine credit/debit based on category
        if chosen_category in [
            TransactionCategory.DEPOSIT,
            TransactionCategory.CREDIT,
            TransactionCategory.REVERSAL
        ]:
            credit_debit_indicator = CreditDebitIndicator.CREDIT
        else:
            credit_debit_indicator = CreditDebitIndicator.DEBIT

        # Generate transaction amount based on type
        if chosen_type in [
            TransactionType.SALARY,
            TransactionType.TAX_REFUND
        ]:
            # Larger amounts
            amount = round(random.uniform(500, 5000), 2)
        elif chosen_type in [
            TransactionType.MORTGAGE_PAYMENT,
            TransactionType.RENT_PAYMENT
        ]:
            # Medium-large amounts
            amount = round(random.uniform(500, 2500), 2)
        elif chosen_type == TransactionType.CASH_WITHDRAWAL:
            # Usually rounded to nearest 10/20
            amount = round(random.choice([20, 40, 60, 80, 100, 200, 300, 500]), 2)
        elif chosen_type in [
            TransactionType.UTILITY_PAYMENT,
            TransactionType.INSURANCE_PREMIUM,
            TransactionType.SUBSCRIPTION
        ]:
            # Smaller regular payments
            amount = round(random.uniform(10, 200), 2)
        else:
            # General purchases and other transactions
            amount = round(random.uniform(5, 500), 2)

        # Value date is usually same as transaction date or next business day
        # 80% chance of same day, 20% chance of 1-2 days later
        if random.random() < 0.8:
            value_date = transaction_date
        else:
            value_date = transaction_date + timedelta(days=random.randint(1, 2))

        # Transaction mutability based on status and timing
        # Recent pending transactions are often mutable
        # Completed transactions are usually immutable

        # Select status first (weighted toward BOOKED)
        chosen_status = TransactionStatus.get_random()

        # Override for very recent transactions - more likely to be PENDING
        days_ago = (now - transaction_date).days
        if days_ago < 2 and random.random() < 0.6:
            chosen_status = TransactionStatus.PENDING

        # Determine mutability based on status
        if chosen_status == TransactionStatus.PENDING:
            chosen_mutability = TransactionMutability.MUTABLE
        elif chosen_status in [TransactionStatus.BOOKED, TransactionStatus.HELD]:
            # Most booked transactions are immutable, but some can be conditional
            mutability_options = [TransactionMutability.IMMUTABLE, TransactionMutability.CONDITIONAL]
            mutability_weights = [90, 10]
            chosen_mutability = random.choices(
                mutability_options,
                weights=mutability_weights,
                k=1
            )[0]
        else:
            chosen_mutability = TransactionMutability.IMMUTABLE

        # Generate transaction description based on type
        descriptions = {
            TransactionType.PURCHASE: [
                "Purchase at {merchant}",
                "{merchant} Purchase",
                "Card Purchase - {merchant}"
            ],
            TransactionType.CASH_WITHDRAWAL: [
                "ATM Withdrawal",
                "Cash Withdrawal - {location}",
                "ATM {location}"
            ],
            TransactionType.REFUND: [
                "Refund from {merchant}",
                "{merchant} Refund",
                "Credit - {merchant}"
            ],
            TransactionType.BILL_PAYMENT: [
                "Bill Payment - {biller}",
                "{biller} Payment",
                "Online Payment to {biller}"
            ],
            TransactionType.SALARY: [
                "Salary Payment",
                "Direct Deposit - Salary",
                "Payroll Deposit - {employer}"
            ],
            TransactionType.SUBSCRIPTION: [
                "Subscription - {service}",
                "Monthly Subscription {service}",
                "Recurring Payment - {service}"
            ],
            TransactionType.INTERNAL_TRANSFER: [
                "Transfer to Account {account}",
                "Internal Transfer",
                "Own Account Transfer"
            ],
            TransactionType.EXTERNAL_TRANSFER: [
                "Transfer to {recipient}",
                "External Transfer",
                "Payment to {recipient}"
            ],
            TransactionType.MERCHANT_PAYMENT: [
                "Payment to {merchant}",
                "{merchant} Transaction",
                "Purchase - {merchant}"
            ],
            TransactionType.UTILITY_PAYMENT: [
                "Utility Payment - {utility}",
                "{utility} Bill Payment",
                "Monthly {utility} Service"
            ]
        }

        # Lists for template substitutions
        merchants = [
            "Amazon", "Walmart", "Target", "Costco", "Best Buy", "Starbucks",
            "McDonald's", "Home Depot", "Kroger", "Walgreens", "CVS", "eBay",
            "Apple Store", "Nike", "Whole Foods", "Trader Joe's", "Macy's",
            "Nordstrom", "Uber", "Lyft", "DoorDash", "Instacart"
        ]

        locations = [
            "Downtown", "Main St", "Plaza", "Mall", "Shopping Center",
            "Airport", "Train Station", "Gas Station", "Bank Branch"
        ]

        billers = [
            "Electric Company", "Water Utility", "Gas Company", "Internet Provider",
            "Phone Company", "Cable TV", "Insurance Co", "Credit Card", "Loan Provider"
        ]

        employers = [
            "ABC Corp", "XYZ Inc", "National Bank", "Tech Solutions", "Healthcare Inc",
            "University", "Government", "Retail Group", "Financial Services"
        ]

        services = [
            "Netflix", "Spotify", "Amazon Prime", "Disney+", "Hulu", "Xbox Live",
            "PlayStation Plus", "Office 365", "Adobe CC", "Gym Membership",
            "News Subscription", "Cloud Storage"
        ]

        utilities = [
            "Electric", "Water", "Gas", "Internet", "Phone", "Cable", "Waste Management"
        ]

        recipients = [
            "John Smith", "Mary Johnson", "Robert Williams", "James Brown",
            "Patricia Davis", "Jennifer Miller", "Michael Wilson", "Linda Moore"
        ]

        # Get description templates for this transaction type
        desc_templates = descriptions.get(
            chosen_type,
            ["{type} Transaction"]  # Default if no specific templates
        )

        desc_template = random.choice(desc_templates)

        # Fill in the template with appropriate values
        if "{merchant}" in desc_template:
            description = desc_template.format(merchant=random.choice(merchants))
        elif "{location}" in desc_template:
            description = desc_template.format(location=random.choice(locations))
        elif "{biller}" in desc_template:
            description = desc_template.format(biller=random.choice(billers))
        elif "{employer}" in desc_template:
            description = desc_template.format(employer=random.choice(employers))
        elif "{service}" in desc_template:
            description = desc_template.format(service=random.choice(services))
        elif "{utility}" in desc_template:
            description = desc_template.format(utility=random.choice(utilities))
        elif "{recipient}" in desc_template:
            description = desc_template.format(recipient=random.choice(recipients))
        elif "{account}" in desc_template:
            description = desc_template.format(account=f"x{random.randint(1000, 9999)}")
        elif "{type}" in desc_template:
            description = desc_template.format(type=chosen_type.value.replace("_", " ").title())
        else:
            description = desc_template

        # Generate a transaction reference
        # Format varies by transaction type
        if chosen_type in [TransactionType.INTERNAL_TRANSFER, TransactionType.EXTERNAL_TRANSFER]:
            reference = f"TRF{random.randint(10000000, 99999999)}"
        elif chosen_type == TransactionType.BILL_PAYMENT:
            reference = f"BILL{random.randint(1000000, 9999999)}"
        elif chosen_type in [TransactionType.PURCHASE, TransactionType.MERCHANT_PAYMENT]:
            reference = f"POS{random.randint(10000000, 99999999)}"
        elif chosen_type == TransactionType.CASH_WITHDRAWAL:
            reference = f"ATM{random.randint(10000000, 99999999)}"
        elif chosen_type == TransactionType.SALARY:
            reference = f"SAL{random.randint(100000, 999999)}"
        else:
            reference = f"REF{random.randint(10000000, 99999999)}"

        # Generate merchant address (optional - 40% chance if it's a merchant transaction)
        merchant_address = None
        if chosen_type in [
            TransactionType.PURCHASE,
            TransactionType.MERCHANT_PAYMENT,
            TransactionType.RETAIL,
            TransactionType.FOOD_DINING
        ] and random.random() < 0.4:
            streets = [
                "Main St", "Oak Ave", "Maple Rd", "Washington Blvd", "Park Ave",
                "Broadway", "Market St", "1st Ave", "Central Ave", "Pine St"
            ]
            cities = [
                "New York", "Los Angeles", "Chicago", "Houston", "Phoenix",
                "Philadelphia", "San Antonio", "San Diego", "Dallas", "San Jose"
            ]
            merchant_address = f"{random.randint(100, 9999)} {random.choice(streets)}, {random.choice(cities)}"

        # Select currency (predominantly USD)
        # In a real application, you would get the account's currency
        currency_options = [
            CurrencyCode.USD,  # 95% US Dollar
            CurrencyCode.EUR,  # 2% Euro
            CurrencyCode.GBP,  # 1% British Pound
            CurrencyCode.CAD,  # 1% Canadian Dollar
            CurrencyCode.AUD  # 1% Australian Dollar
        ]
        currency_weights = [95, 2, 1, 1, 1]
        chosen_currency = random.choices(
            currency_options,
            weights=currency_weights,
            k=1
        )[0]

        # Transaction charge/fee (10% chance)
        charge_amount = None
        charge_currency = None
        if random.random() < 0.1:
            # Fees are typically small
            charge_amount = round(random.uniform(0.50, 25.00), 2)
            charge_currency = chosen_currency  # Usually same as transaction currency

        # Create the transaction dictionary
        transaction = {
            "consumer_banking_account_id": id_fields['consumer_banking_account_id'],
            "transaction_reference": reference,
            "credit_debit_indicator": credit_debit_indicator.value,
            "status": chosen_status.value,
            "transaction_mutability": chosen_mutability.value,
            "transaction_date": transaction_date,
            "category": chosen_category.value,
            "transaction_type": chosen_type.value,
            "value_date": value_date,
            "description": description,
            "merchant_address": merchant_address,
            "amount": amount,
            "currency": chosen_currency.value,
            "charge_amount": charge_amount,
            "charge_currency": charge_currency.value if charge_currency else None
        }

        return transaction

    finally:
        cursor.close()
