from ..enterprise.enums import CurrencyCode
from .enums import AccountStatus, OfferType
from data_generator import DataGenerator, SkipRowGenerationError
from typing import Any, Dict

import datetime
import random


def generate_random_offer(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random consumer banking offer with plausible values.

    Args:
        id_fields: Dictionary containing the required ID fields
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated offer data
    """
    # Get database connection
    conn = dg.conn

    # Validate required fields
    if 'consumer_banking_account_id' not in id_fields:
        raise ValueError("consumer_banking_account_id is required")

    # Fetch the consumer banking account to verify it exists and get its opened date
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT a.opened_date, a.status, p.product_type 
            FROM consumer_banking.accounts a
            LEFT JOIN consumer_banking.products p ON a.consumer_banking_product_id = p.consumer_banking_product_id
            WHERE a.consumer_banking_account_id = %s
        """, (id_fields['consumer_banking_account_id'],))

        consumer_account = cursor.fetchone()

        if not consumer_account:
            raise ValueError(f"No consumer banking account found with ID {id_fields['consumer_banking_account_id']}")

        account_opened_date = consumer_account.get('opened_date')
        account_status = consumer_account.get('status')
        product_type = consumer_account.get('product_type')

        # Only active accounts should get offers
        if account_status != AccountStatus.ACTIVE.value:
            raise SkipRowGenerationError

        # Generate today's date
        today = datetime.datetime.now(datetime.timezone.utc)

        # Calculate days since account opened
        days_since_account_opened = (today - account_opened_date).days

        # Only accounts open for at least 90 days should get offers (typically)
        if days_since_account_opened < 90:
            chance_of_offer = 0.2  # 20% chance for newer accounts
        else:
            chance_of_offer = 0.8  # 80% chance for established accounts

        if random.random() > chance_of_offer:
            raise SkipRowGenerationError

        # Determine offer type using the enum
        offer_type = OfferType.get_random()

        # Adjust offer type based on product type for more realism
        if product_type:
            product_type_lower = product_type.lower()
            # For savings accounts, offer savings, investment, or premium offers
            if 'savings' in product_type_lower:
                offer_type = random.choice([
                    OfferType.INVESTMENT,
                    OfferType.SAVINGS,
                    OfferType.PREMIUM_ACCOUNT,
                    OfferType.INTEREST_RATE_REDUCTION
                ])
            # For checking/current accounts, offer overdraft or fee waivers
            elif 'checking' in product_type_lower or 'current' in product_type_lower:
                offer_type = random.choice([
                    OfferType.OVERDRAFT,
                    OfferType.FEE_WAIVER,
                    OfferType.PREMIUM_ACCOUNT,
                    OfferType.REWARDS
                ])
            # For loan/credit products, offer balance transfers or rate reductions
            elif 'loan' in product_type_lower or 'credit' in product_type_lower:
                offer_type = random.choice([
                    OfferType.BALANCE_TRANSFER,
                    OfferType.INTEREST_RATE_REDUCTION,
                    OfferType.CREDIT_LIMIT_INCREASE,
                    OfferType.LOAN
                ])

        # Generate offer description based on the offer type
        if offer_type == OfferType.LOAN:
            descriptions = [
                "Pre-approved personal loan offer with competitive rates",
                "Low-interest loan opportunity exclusively for valued customers",
                "Special loan offer with flexible repayment terms",
                "Fast-track loan approval with reduced documentation"
            ]
        elif offer_type == OfferType.BALANCE_TRANSFER:
            descriptions = [
                "0% interest on balance transfers for 12 months",
                "Transfer existing balances at preferential rates",
                "Consolidate your debts with our balance transfer offer",
                "No fee balance transfer for qualifying customers"
            ]
        elif offer_type == OfferType.CREDIT_LIMIT_INCREASE:
            descriptions = [
                "You've been approved for a credit limit increase",
                "Enjoy greater flexibility with an increased credit limit",
                "Expanded borrowing power with your pre-approved limit increase",
                "Access more funds with your new credit limit"
            ]
        elif offer_type == OfferType.INTEREST_RATE_REDUCTION:
            descriptions = [
                "Special interest rate reduction on your existing products",
                "Reduced APR offer for loyal customers",
                "Limited time interest rate discount opportunity",
                "Preferential rate available on your account"
            ]
        elif offer_type == OfferType.OVERDRAFT:
            descriptions = [
                "Increased overdraft facility at reduced rates",
                "Fee-free overdraft for 6 months",
                "Extended overdraft protection for your account",
                "Enhanced overdraft buffer for financial flexibility"
            ]
        elif offer_type == OfferType.SAVINGS:
            descriptions = [
                "Higher interest rate savings account exclusive offer",
                "Special savings account with bonus interest rates",
                "Premium savings opportunity for existing customers",
                "Boost your savings with our enhanced interest rates"
            ]
        elif offer_type == OfferType.PREMIUM_ACCOUNT:
            descriptions = [
                "Upgrade to our premium account package with exclusive benefits",
                "Enhanced account features available for your profile",
                "Premium banking services with dedicated support",
                "Exclusive account upgrade offer with waived monthly fees"
            ]
        elif offer_type == OfferType.FEE_WAIVER:
            descriptions = [
                "Monthly maintenance fee waiver for one year",
                "Transaction fee exemption for qualifying customers",
                "International transfer fee waiver promotion",
                "Service charge exemption for your account"
            ]
        else:
            descriptions = [
                "Special promotion for valued customers",
                "Limited time offer on financial services",
                "Exclusive account enhancement opportunity",
                "Personalized financial offer based on your profile"
            ]

        description = random.choice(descriptions)

        # Generate start and end dates for the offer
        # Start date: typically today or within the next 7 days
        days_until_start = random.randint(0, 7)
        start_date_time = today + datetime.timedelta(days=days_until_start)

        # End date: typically 30-90 days after start date
        offer_duration_days = random.randint(30, 90)
        end_date_time = start_date_time + datetime.timedelta(days=offer_duration_days)

        # Generate rate (if applicable)
        rate = None
        if offer_type in [OfferType.LOAN, OfferType.INTEREST_RATE_REDUCTION,
                          OfferType.BALANCE_TRANSFER, OfferType.OVERDRAFT]:
            # Generate plausible interest rate
            if offer_type == OfferType.INTEREST_RATE_REDUCTION:
                rate = round(random.uniform(0.5, 5.0), 2)  # Lower for rate reduction offers
            elif offer_type == OfferType.BALANCE_TRANSFER:
                rate = round(random.uniform(0.0, 3.5), 2)  # Often zero or very low for promotions
            else:
                rate = round(random.uniform(3.5, 15.0), 2)  # Standard loan rates

        # Generate value (if applicable)
        value = None
        if offer_type in [OfferType.REWARDS, OfferType.CASHBACK]:
            # Points value or cashback percentage
            value = random.randint(1000, 50000)

        # Generate terms (if applicable - 80% chance)
        term = None
        if random.random() < 0.8:
            terms_options = [
                "Subject to credit approval. Terms and conditions apply.",
                "Limited time offer. Not valid with other promotions.",
                "Available to qualifying customers only. See full terms online.",
                "Offer valid for 30 days. Standard underwriting criteria apply.",
                "Minimum balance requirements apply. See representative for details."
            ]
            term = random.choice(terms_options)

        # Generate URL (if applicable - 70% chance)
        url = None
        if random.random() < 0.7:
            url_options = [
                "https://bank.example.com/offers/special",
                "https://bank.example.com/promotions/exclusive",
                "https://bank.example.com/personal/offers",
                "https://bank.example.com/banking/promotions"
            ]
            url = f"{random.choice(url_options)}/{offer_type.value.lower()}"

        # Generate amount and currency (if applicable)
        amount = None
        amount_currency = None
        if offer_type in [OfferType.LOAN, OfferType.CREDIT_LIMIT_INCREASE,
                          OfferType.BALANCE_TRANSFER, OfferType.OVERDRAFT]:
            # Generate plausible amounts based on offer type
            if offer_type == OfferType.LOAN:
                amount = round(random.uniform(1000, 25000), 2)
            elif offer_type == OfferType.CREDIT_LIMIT_INCREASE:
                amount = round(random.uniform(500, 10000), 2)
            elif offer_type == OfferType.BALANCE_TRANSFER:
                amount = round(random.uniform(1000, 15000), 2)
            elif offer_type == OfferType.OVERDRAFT:
                amount = round(random.uniform(100, 5000), 2)

            # Select a currency
            amount_currency = CurrencyCode.get_random().value

        # Generate fee and fee currency (if applicable - 30% chance)
        fee = None
        fee_currency = None
        if random.random() < 0.3 and offer_type not in [OfferType.FEE_WAIVER]:
            # Generate plausible fee
            if offer_type == OfferType.BALANCE_TRANSFER:
                fee = round(amount * random.uniform(0.01, 0.05), 2)  # 1-5% of transfer amount
            elif offer_type == OfferType.LOAN:
                fee = round(amount * random.uniform(0.01, 0.03), 2)  # 1-3% origination fee
            else:
                fee = round(random.uniform(10, 100), 2)  # Standard fee

            # Use same currency as amount if available, otherwise select
            if amount_currency:
                fee_currency = amount_currency
            else:
                fee_currency = CurrencyCode.get_random().value

        # Create the offer dictionary
        offer = {
            "consumer_banking_account_id": id_fields['consumer_banking_account_id'],
            "offer_type": offer_type.value,
            "description": description,
            "start_date_time": start_date_time,
            "end_date_time": end_date_time,
            "rate": rate,
            "value": value,
            "term": term,
            "url": url,
            "amount": amount,
            "amount_currency": amount_currency,
            "fee": fee,
            "fee_currency": fee_currency
        }

        return offer

    finally:
        cursor.close()
