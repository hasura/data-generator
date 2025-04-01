from .enums import (AccountFeeSchedule, InterestCalculationMethod,
                    ProductStatus, ProductType)
from data_generator import DataGenerator
from typing import Any, Dict

import datetime
import random


def generate_random_product(_id_fields: Dict[str, Any], _dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random consumer banking product with plausible values.

    Args:
        _id_fields: Dictionary containing the required ID fields (empty for products)
        _dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated product data
    """
    # Generate a product code
    # Format: 3 letters + 2-3 digits
    product_prefix = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=3))
    product_number = ''.join(random.choices('0123456789', k=random.randint(2, 3)))
    product_code = f"{product_prefix}{product_number}"

    # Determine product type using the enum
    product_type = ProductType.get_random()

    # Generate product name based on type
    product_name_prefix = ["Premium", "Standard", "Basic", "Advanced", "Elite",
                           "Select", "Essential", "Preferred", "Signature", "Gold",
                           "Platinum", "Value", "Ultimate", "Smart", "Optimum"]

    # Generate name based on product type
    if product_type == ProductType.CHECKING:
        product_name_suffix = ["Checking", "Checking Account", "Direct Checking", "eChecking", "Advantage Checking"]
    elif product_type == ProductType.SAVINGS:
        product_name_suffix = ["Savings", "Savings Account", "High-Yield Savings", "eSavings", "Goal Savings"]
    elif product_type == ProductType.MONEY_MARKET:
        product_name_suffix = ["Money Market", "Money Market Account", "Premium Money Market", "Select Money Market"]
    elif product_type == ProductType.CERTIFICATE_OF_DEPOSIT:
        product_name_suffix = ["CD", "Certificate of Deposit", "Term Deposit", "Fixed Deposit"]
    elif product_type == ProductType.IRA:
        product_name_suffix = ["IRA", "Retirement Account", "IRA Savings", "Retirement Savings"]
    elif product_type == ProductType.HSA:
        product_name_suffix = ["HSA", "Health Savings Account", "Medical Savings"]
    elif product_type == ProductType.STUDENT:
        product_name_suffix = ["Student Account", "Student Checking", "Student Savings", "Campus Account"]
    elif product_type == ProductType.YOUTH:
        product_name_suffix = ["Youth Account", "Kids Account", "Teen Account", "Junior Savings"]
    elif product_type == ProductType.SENIOR:
        product_name_suffix = ["Senior Account", "Retirement Checking", "Senior Advantage", "Senior Savings"]
    elif product_type == ProductType.BUSINESS_CHECKING:
        product_name_suffix = ["Business Checking", "Commercial Checking", "Business Account", "Business Advantage"]
    elif product_type == ProductType.BUSINESS_SAVINGS:
        product_name_suffix = ["Business Savings", "Commercial Savings", "Business Reserve", "Commercial Reserve"]
    elif product_type == ProductType.PREMIUM:
        product_name_suffix = ["Premium Package", "Premier Account", "Private Client", "Wealth Management"]
    elif product_type == ProductType.FOREIGN_CURRENCY:
        product_name_suffix = ["Foreign Currency Account", "Multi-Currency", "Global Account", "International Banking"]
    else:  # SPECIALIZED or others
        product_name_suffix = ["Special Account", "Custom Banking", "Tailored Account", "Flex Banking"]

    # Combine prefix and suffix for product name
    product_name = f"{random.choice(product_name_prefix)} {random.choice(product_name_suffix)}"

    # Detailed product description
    product_descriptions = {
        ProductType.CHECKING: [
            "A versatile checking account for everyday banking needs with online and mobile access.",
            "Full-featured checking account with debit card, bill pay, and mobile deposit capabilities.",
            "Checking account designed for customers who prefer a simple approach to banking.",
            "Comprehensive checking solution with direct deposit and overdraft protection options."
        ],
        ProductType.SAVINGS: [
            "Interest-bearing savings account to help customers reach their financial goals.",
            "Competitive savings account with easy access to funds when needed.",
            "Savings account with automatic deposit options and goal-setting features.",
            "Flexible savings solution with tiered interest rates based on balance."
        ],
        ProductType.MONEY_MARKET: [
            "Higher-yield account that combines features of checking and savings accounts.",
            "Premium account with competitive interest rates and limited check-writing capability.",
            "Money market account with tiered interest rates for higher balances.",
            "Liquid account offering higher returns than standard savings with some transaction capabilities."
        ],
        ProductType.CERTIFICATE_OF_DEPOSIT: [
            "Fixed-term deposit account with guaranteed interest rate for the full term.",
            "Secure investment option with higher rates for longer commitment periods.",
            "Time deposit with flexible term options from 3 months to 5 years.",
            "Premium CD with special rates and automatic renewal options."
        ],
        ProductType.IRA: [
            "Tax-advantaged retirement savings account with multiple investment options.",
            "Individual Retirement Account with competitive interest rates.",
            "Long-term savings vehicle designed for retirement planning.",
            "Tax-deferred retirement account with convenient contribution options."
        ],
        ProductType.HSA: [
            "Tax-advantaged account for qualified medical expenses.",
            "Health Savings Account that helps customers save for healthcare costs.",
            "Medical expense account with investment options for long-term growth.",
            "Tax-free health savings solution for eligible customers with high-deductible health plans."
        ],
        ProductType.STUDENT: [
            "No-fee checking account designed specifically for students.",
            "Banking solution for students with special benefits and educational resources.",
            "Student-focused account with mobile banking and financial literacy tools.",
            "Starter account for students with no minimum balance requirements."
        ],
        ProductType.YOUTH: [
            "Account for minors with parental monitoring features.",
            "Youth savings account designed to teach financial responsibility.",
            "Starter account for children with educational tools and parent controls.",
            "Junior savings solution that grows with your child's financial needs."
        ],
        ProductType.SENIOR: [
            "Banking package with special benefits for customers age 55 and older.",
            "Senior account with preferential rates and reduced fees.",
            "Retirement-focused banking solution with added conveniences.",
            "Premium account for seniors with personalized service options."
        ],
        ProductType.BUSINESS_CHECKING: [
            "Robust checking account for small to medium businesses.",
            "Commercial checking solution with cash management tools.",
            "Business account with scalable features to grow with your company.",
            "Comprehensive business checking with integrated merchant services."
        ],
        ProductType.BUSINESS_SAVINGS: [
            "Business savings account to help manage excess cash and reserves.",
            "Commercial savings solution with competitive interest rates.",
            "Business reserve account with flexible access options.",
            "Short-term investment vehicle for business cash management."
        ],
        ProductType.PREMIUM: [
            "Exclusive package combining premium banking services and personalized support.",
            "Relationship banking solution with dedicated advisor and preferential rates.",
            "Elite account package with enhanced benefits and wealth management options.",
            "Premium banking experience with concierge services and exclusive offers."
        ],
        ProductType.FOREIGN_CURRENCY: [
            "Multi-currency account for customers with international banking needs.",
            "Foreign currency solution with favorable exchange rates and international transfers.",
            "Global account supporting multiple currencies and international transactions.",
            "International banking package for frequent travelers and global businesses."
        ],
        ProductType.SPECIALIZED: [
            "Customized banking solution for specific industry or customer needs.",
            "Specialized account with features tailored to unique banking requirements.",
            "Niche banking product designed for specific market segments.",
            "Targeted account solution with customizable features and options."
        ]
    }

    description = random.choice(product_descriptions.get(product_type, product_descriptions[ProductType.SPECIALIZED]))

    # Generate minimum opening deposit
    # Different ranges based on product type
    if product_type in [ProductType.PREMIUM, ProductType.FOREIGN_CURRENCY, ProductType.BUSINESS_CHECKING]:
        min_opening_deposit = random.choice([500, 1000, 2500, 5000, 10000, 25000])
    elif product_type in [ProductType.MONEY_MARKET, ProductType.CERTIFICATE_OF_DEPOSIT, ProductType.IRA]:
        min_opening_deposit = random.choice([100, 250, 500, 1000, 2500])
    elif product_type in [ProductType.STUDENT, ProductType.YOUTH]:
        min_opening_deposit = random.choice([0, 1, 5, 10, 25, 50])
    else:
        min_opening_deposit = random.choice([0, 25, 50, 100, 250, 500])

    # Generate monthly fee
    # Higher probability of having a fee for premium products
    if product_type in [ProductType.PREMIUM, ProductType.FOREIGN_CURRENCY, ProductType.BUSINESS_CHECKING]:
        monthly_fee_options = [0, 5, 10, 15, 20, 25, 30, 35, 50]
        monthly_fee_weights = [5, 5, 10, 15, 20, 20, 15, 5, 5]
    elif product_type in [ProductType.STUDENT, ProductType.YOUTH, ProductType.SENIOR]:
        monthly_fee_options = [0, 3, 5, 8, 10]
        monthly_fee_weights = [70, 10, 10, 5, 5]
    else:
        monthly_fee_options = [0, 5, 8, 10, 12, 15, 20, 25]
        monthly_fee_weights = [20, 15, 15, 20, 10, 10, 5, 5]

    monthly_fee = random.choices(monthly_fee_options, weights=monthly_fee_weights, k=1)[0]

    # Fee schedule
    if monthly_fee == 0:
        fee_schedule = AccountFeeSchedule.NO_FEE
    else:
        fee_schedule = AccountFeeSchedule.get_random()

    # Transaction limit (more common for savings accounts)
    transaction_limit = None
    if product_type in [ProductType.SAVINGS, ProductType.MONEY_MARKET, ProductType.HSA,
                        ProductType.BUSINESS_SAVINGS, ProductType.YOUTH]:
        # 80% chance of having a transaction limit for these account types
        if random.random() < 0.8:
            transaction_limit = random.choice([3, 6, 8, 10, 12, 15, 20, 25])
    elif random.random() < 0.3:  # 30% chance for other account types
        transaction_limit = random.choice([15, 20, 25, 30, 50, 100])

    # Transaction fee (only if there's a transaction limit)
    transaction_fee = None
    if transaction_limit is not None:
        transaction_fee = round(random.uniform(0.5, 5.0), 2)

    # Minimum balance to avoid fees (only if there's a monthly fee)
    min_balance = None
    if monthly_fee > 0 and fee_schedule == AccountFeeSchedule.WAIVED_WITH_MINIMUM_BALANCE:
        # Minimum balance is typically a multiple of the monthly fee
        min_balance_multipliers = [10, 25, 50, 100, 200, 500]
        min_balance = monthly_fee * random.choice(min_balance_multipliers)

        # Round to a "nice" number
        magnitude = 10 ** (len(str(int(min_balance))) - 1)
        min_balance = round(min_balance / magnitude) * magnitude

        # Ensure minimum balance is at least slightly higher than minimum opening deposit
        if min_opening_deposit is not None:
            min_balance = max(min_balance, min_opening_deposit * 1.5)

    # Interest-bearing status
    # Higher chance for savings products, lower for checking products
    if product_type in [ProductType.SAVINGS, ProductType.MONEY_MARKET, ProductType.CERTIFICATE_OF_DEPOSIT,
                        ProductType.IRA, ProductType.HSA, ProductType.BUSINESS_SAVINGS]:
        is_interest_bearing = random.choices([True, False], weights=[95, 5], k=1)[0]
    elif product_type in [ProductType.PREMIUM, ProductType.FOREIGN_CURRENCY]:
        is_interest_bearing = random.choices([True, False], weights=[80, 20], k=1)[0]
    elif product_type in [ProductType.CHECKING, ProductType.BUSINESS_CHECKING]:
        is_interest_bearing = random.choices([True, False], weights=[30, 70], k=1)[0]
    else:
        is_interest_bearing = random.choices([True, False], weights=[50, 50], k=1)[0]

    # Base interest rate (only if interest-bearing)
    base_interest_rate = None
    if is_interest_bearing:
        if product_type == ProductType.CERTIFICATE_OF_DEPOSIT:
            # CDs typically have higher rates
            base_interest_rate = round(random.uniform(1.0, 5.0), 2)
        elif product_type in [ProductType.MONEY_MARKET, ProductType.IRA]:
            # These often have medium rates
            base_interest_rate = round(random.uniform(0.5, 3.0), 2)
        else:
            # Standard accounts have lower rates
            base_interest_rate = round(random.uniform(0.01, 1.5), 2)

    # Interest calculation method (only if interest-bearing)
    interest_calculation_method = None
    if is_interest_bearing:
        interest_calculation_method = InterestCalculationMethod.get_random()

    # Term length in months (only for term products)
    term_length = None
    if product_type == ProductType.CERTIFICATE_OF_DEPOSIT:
        term_options = [1, 3, 6, 9, 12, 18, 24, 36, 48, 60, 84, 120]
        term_length = random.choice(term_options)

    # Product status
    product_status = ProductStatus.get_random()

    # Launch date (between 1-10 years ago)
    today = datetime.datetime.now(datetime.timezone.utc)
    days_back = random.randint(365, 3650)
    launch_date = today - datetime.timedelta(days=days_back)

    # Discontinue date (only if status is DISCONTINUED, ARCHIVED, or GRANDFATHERED)
    discontinue_date = None
    if product_status in [ProductStatus.DISCONTINUED, ProductStatus.ARCHIVED, ProductStatus.GRANDFATHERED]:
        # Discontinue date is between launch date and today
        days_since_launch = (today - launch_date).days
        days_to_discontinue = random.randint(int(days_since_launch * 0.3), days_since_launch)
        discontinue_date = launch_date + datetime.timedelta(days=days_to_discontinue)

    # Create the product dictionary
    product = {
        "product_code": product_code,
        "product_name": product_name,
        "product_type": product_type.value,
        "description": description,
        "min_opening_deposit": min_opening_deposit,
        "monthly_fee": monthly_fee,
        "fee_schedule": fee_schedule.value,
        "transaction_limit": transaction_limit,
        "transaction_fee": transaction_fee,
        "min_balance": min_balance,
        "is_interest_bearing": is_interest_bearing,
        "base_interest_rate": base_interest_rate,
        "interest_calculation_method": interest_calculation_method.value if interest_calculation_method else None,
        "term_length": term_length,
        "status": product_status.value,
        "launch_date": launch_date.date(),
        "discontinue_date": discontinue_date.date() if discontinue_date else None
    }

    return product
