import random
import string
from datetime import datetime, timedelta

from data_generator import DataGenerator
from fsi_data_generator.fsi_generators.intelligent_generators.mortgage_services.enums.interest_rate_type import \
    InterestRateType
from fsi_data_generator.fsi_generators.intelligent_generators.mortgage_services.enums.loan_type import \
    LoanType


def generate_random_loan_product(ids_dict, dg: DataGenerator):
    """
    Generate a random, plausible loan product that could be currently offered
    or a historical product from the prior 20 years.

    Returns a dictionary with loan product details.
    """
    conn = dg.conn

    # Select a loan type
    loan_type = LoanType.get_random()

    # Check if there's an existing active product of this type
    query = """
        SELECT product_code, loan_type, interest_rate_type, launch_date, is_active
        FROM mortgage_services.loan_products
        WHERE loan_type = %s
        ORDER BY launch_date DESC
        """

    existing_products = []
    with conn.cursor() as cursor:
        cursor.execute(query, (loan_type.value,))
        existing_products = cursor.fetchall()

    # Determine if this will be an active product
    # If there's already an active product of this type, this one will be historical
    has_active_product = any(product.get('is_active', False) for product in existing_products)

    if has_active_product:
        is_active = False
    else:
        # If no active product exists, 70% chance this will be active
        is_active = True

    # Generate interest rate type based on loan type
    if loan_type == LoanType.HOME_EQUITY:
        # HELOCs are almost always adjustable
        interest_rate_type = InterestRateType.ADJUSTABLE
    else:
        # Other products can be fixed or adjustable
        interest_rate_type = InterestRateType.get_random([0.7, 0.3, 0, 0, 0, 0, 0])  # Weighted toward fixed

    # Generate a product name
    product_name = generate_product_name(loan_type.value, interest_rate_type.value)

    # Generate a product code (alphanumeric, typically 4-10 characters)
    code_length = random.randint(4, 10)
    product_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=code_length))

    # Generate a description
    description = generate_product_description(loan_type, interest_rate_type, product_name)

    # Generate launch and discontinue dates based on existing products
    now = datetime.now()

    launch_date = None
    discontinue_date = None

    if existing_products:
        # If existing products, position this new one in the timeline

        if is_active:
            # If this is active, it's the newest product
            # Launch this product after the latest one
            latest_product = existing_products[0]  # First one (sorted by date desc)

            if latest_product.get('is_active', False):
                # If the latest is active, we need to replace it
                # Launch 1-30 days ago
                days_ago = random.randint(1, 30)
                launch_date = now - timedelta(days=days_ago)

                # Previous product discontinues the day before this one launches
                latest_launch_date = latest_product.get('launch_date')
                if latest_launch_date:
                    previous_discontinue_date = launch_date - timedelta(days=1)

                    # Update previous product's discontinue date
                    update_query = """
                        UPDATE mortgage_services.loan_products
                        SET discontinue_date = %s, is_active = false
                        WHERE product_code = %s
                        """
                    with conn.cursor() as cursor:
                        cursor.execute(update_query, (previous_discontinue_date.strftime("%Y-%m-%d"),
                                                      latest_product.get('product_code')))
            else:
                # If latest is not active, launch this one 1-30 days after the latest one was discontinued
                # We don't know discontinue_date from our query, so estimate it based on next product's launch
                latest_launch_str = latest_product.get('launch_date')
                if latest_launch_str:
                    try:
                        latest_launch = datetime.strptime(latest_launch_str, "%Y-%m-%d")
                        # Assume it was discontinued 1-180 days after launch
                        latest_lifetime = random.randint(180, 730)  # 6 months to 2 years
                        estimated_discontinue = latest_launch + timedelta(days=latest_lifetime)

                        # Launch this one 1-30 days after estimated discontinue date
                        gap_days = random.randint(1, 30)
                        launch_date = estimated_discontinue + timedelta(days=gap_days)

                        # If this would be in the future, adjust to recent past
                        if launch_date > now:
                            launch_date = now - timedelta(days=random.randint(1, 30))
                    except ValueError:
                        # Fallback if date parsing fails
                        launch_date = now - timedelta(days=random.randint(1, 30))
                else:
                    launch_date = now - timedelta(days=random.randint(1, 30))
        else:
            # This is a historical product
            # Find a gap in the timeline to insert this product

            if len(existing_products) > 1:
                # Try to find a gap between two products
                for i in range(len(existing_products) - 1):
                    current_product = existing_products[i]
                    next_product = existing_products[i + 1]

                    current_launch_str = current_product.get('launch_date')
                    next_launch_str = next_product.get('launch_date')

                    if current_launch_str and next_launch_str:
                        try:
                            current_launch = datetime.strptime(current_launch_str, "%Y-%m-%d")
                            next_launch = datetime.strptime(next_launch_str, "%Y-%m-%d")

                            gap_days = (current_launch - next_launch).days

                            # If gap is large enough for a product lifecycle (min 180 days)
                            if gap_days > 365:  # At least a year gap
                                # Position this product in the gap
                                # Launch after the older product
                                gap_position = random.uniform(0.3, 0.7)  # Position in the middle of the gap
                                days_after_older = int(gap_days * gap_position)
                                launch_date = next_launch + timedelta(days=days_after_older)

                                # Discontinue before the newer product (1-30 days before)
                                days_before_newer = random.randint(1, 30)
                                discontinue_date = current_launch - timedelta(days=days_before_newer)
                                break
                        except ValueError:
                            # Fallback if date parsing fails
                            pass

            # If we couldn't find a gap, or there aren't enough products to have gaps
            # Place this product before the oldest known product
            if 'launch_date' not in locals():
                oldest_product = existing_products[-1]  # Last one (sorted by date desc)
                oldest_launch_str = oldest_product.get('launch_date')

                if oldest_launch_str:
                    try:
                        oldest_launch = datetime.strptime(oldest_launch_str, "%Y-%m-%d")
                        # Launch 180-730 days before oldest
                        days_before = random.randint(180, 730)
                        launch_date = oldest_launch - timedelta(days=days_before)

                        # Discontinue 1-30 days before oldest launches
                        days_before_oldest = random.randint(1, 30)
                        discontinue_date = oldest_launch - timedelta(days=days_before_oldest)
                    except ValueError:
                        # Fallback if date parsing fails
                        max_years_ago = 20
                        launch_days_ago = random.randint(365 * 5, 365 * max_years_ago)  # 5-20 years ago
                        launch_date = now - timedelta(days=launch_days_ago)

                        # Product lasted 1-5 years
                        lifetime_days = random.randint(365, 365 * 5)
                        discontinue_date = launch_date + timedelta(days=lifetime_days)

                        # If discontinue date would be in the future, adjust it
                        if discontinue_date > now:
                            discontinue_date = now - timedelta(days=random.randint(30, 365))
                else:
                    # Fallback with no date information
                    max_years_ago = 20
                    launch_days_ago = random.randint(365 * 5, 365 * max_years_ago)  # 5-20 years ago
                    launch_date = now - timedelta(days=launch_days_ago)

                    # Product lasted 1-5 years
                    lifetime_days = random.randint(365, 365 * 5)
                    discontinue_date = launch_date + timedelta(days=lifetime_days)

                    # If discontinue date would be in the future, adjust it
                    if discontinue_date > now:
                        discontinue_date = now - timedelta(days=random.randint(30, 365))
    else:
        # No existing products of this type
        # Generate launch date (within last 20 years)
        if is_active:
            # Active products launched more recently
            max_years_ago = 5
            launch_days_ago = random.randint(1, 365 * max_years_ago)  # 0-5 years ago
            launch_date = now - timedelta(days=launch_days_ago)
            discontinue_date = None  # Active products don't have discontinue date
        else:
            # Historical products
            min_years_ago = 5
            max_years_ago = 20
            launch_days_ago = random.randint(365 * min_years_ago, 365 * max_years_ago)  # 5-20 years ago
            launch_date = now - timedelta(days=launch_days_ago)

            # Product lasted 1-5 years
            lifetime_days = random.randint(365, 365 * 5)
            discontinue_date = launch_date + timedelta(days=lifetime_days)

            # If discontinue date would be in the future, adjust it
            if discontinue_date > now:
                discontinue_date = now - timedelta(days=random.randint(30, 365))

    # Format dates as strings
    launch_date_str = launch_date.strftime("%Y-%m-%d") if 'launch_date' in locals() else None
    discontinue_date_str = discontinue_date.strftime("%Y-%m-%d") if discontinue_date else None

    # Calculate years_ago for interest rate adjustments
    years_ago = (now - launch_date).days / 365 if launch_date else 0

    # Rest of the function continues as before...
    # [The remainder of the function with loan terms generation remains unchanged]

    # Generate loan terms based on loan type
    if loan_type == LoanType.CONVENTIONAL:
        min_term_months = random.choice([120, 180, 240])  # 10, 15, 20 years
        max_term_months = 360  # 30 years
        min_loan_amount = random.choice([10000, 25000, 50000])
        max_loan_amount = random.choice(
            [417000, 510400, 548250, 647200, 822375])  # Conforming limits from different years
        min_credit_score = random.choice([620, 640, 660])
        min_down_payment_percentage = random.choice([3.0, 5.0, 10.0])
        requires_pmi = min_down_payment_percentage < 20.0

    elif loan_type == LoanType.FHA:
        min_term_months = random.choice([120, 180, 240])  # 10, 15, 20 years
        max_term_months = 360  # 30 years
        min_loan_amount = random.choice([5000, 10000, 25000])
        # FHA limits vary by location and year
        max_loan_amount = random.choice([294515, 331760, 356362, 420680, 472030, 510400, 765600])
        min_credit_score = random.choice([500, 580, 600, 620])
        min_down_payment_percentage = 3.5 if min_credit_score >= 580 else 10.0
        requires_pmi = True  # FHA loans require mortgage insurance premium (MIP)

    elif loan_type == LoanType.VA:
        min_term_months = random.choice([120, 180, 240])  # 10, 15, 20 years
        max_term_months = 360  # 30 years
        min_loan_amount = random.choice([10000, 25000, 36000])
        max_loan_amount = random.choice([417000, 484350, 510400, 548250, 647200, 0])  # 0 = no limit for some periods
        min_credit_score = random.choice([580, 600, 620])
        min_down_payment_percentage = 0.0
        requires_pmi = False  # VA loans don't require PMI

    elif loan_type == LoanType.USDA:
        min_term_months = 360  # USDA typically only offers 30-year terms
        max_term_months = 360
        min_loan_amount = random.choice([5000, 10000])
        max_loan_amount = random.choice([250000, 300000, 350000, 400000])
        min_credit_score = random.choice([640, 660])
        min_down_payment_percentage = 0.0
        requires_pmi = True  # USDA loans have a guarantee fee

    elif loan_type == LoanType.JUMBO:
        min_term_months = random.choice([120, 180, 240])
        max_term_months = random.choice([360, 480, 600])  # Some jumbo loans offer 40 or 50 year terms
        min_loan_amount = random.choice(
            [417001, 453101, 484351, 510401, 548251, 647201, 765601])  # Just above conforming limits
        max_loan_amount = random.choice([1000000, 1500000, 2000000, 2500000, 5000000, 10000000])
        min_credit_score = random.choice([680, 700, 720, 740])
        min_down_payment_percentage = random.choice([10.0, 15.0, 20.0, 25.0])
        requires_pmi = min_down_payment_percentage < 20.0

    elif loan_type == LoanType.HOME_EQUITY:
        min_term_months = random.choice([60, 120])  # 5 or 10 year draw periods
        max_term_months = random.choice([180, 240, 300, 360])  # 15-30 year terms
        min_loan_amount = random.choice([10000, 15000, 25000])
        max_loan_amount = random.choice([250000, 500000, 750000, 1000000])
        min_credit_score = random.choice([660, 680, 700, 720])
        min_down_payment_percentage = 0.0  # HELOCs don't have down payments in the same way
        requires_pmi = False

    elif loan_type == LoanType.REVERSE_MORTGAGE:
        min_term_months = 0  # Reverse mortgages don't have fixed terms
        max_term_months = 0
        min_loan_amount = random.choice([10000, 25000, 50000])
        max_loan_amount = random.choice([417000, 510400, 625500, 765600, 970800])
        min_credit_score = 0  # Credit score is less important for reverse mortgages
        min_down_payment_percentage = 0.0
        requires_pmi = False

    else:  # LoanType.CONSTRUCTION:
        min_term_months = random.choice([6, 12, 18])
        max_term_months = random.choice([24, 36, 60])
        min_loan_amount = random.choice([50000, 100000])
        max_loan_amount = random.choice([500000, 750000, 1000000, 2000000])
        min_credit_score = random.choice([660, 680, 700])
        min_down_payment_percentage = random.choice([10.0, 15.0, 20.0, 25.0])
        requires_pmi = min_down_payment_percentage < 20.0

    # Adjust for historical products
    if years_ago > 0:
        # Historical products might have had different parameters
        # Adjust base interest rate for historical products
        if years_ago > 15:  # 2005 or earlier
            base_interest_rate_adjustment = random.uniform(1.5, 5.0)
        elif years_ago > 10:  # 2010 or earlier
            base_interest_rate_adjustment = random.uniform(0.5, 2.0)
        elif years_ago > 5:  # 2015 or earlier
            base_interest_rate_adjustment = random.uniform(-0.5, 1.0)
        else:  # Recent
            base_interest_rate_adjustment = random.uniform(-0.25, 0.5)
    else:
        base_interest_rate_adjustment = 0

    # Generate base interest rate
    if loan_type == LoanType.FHA:
        base_rate = 4.0 if interest_rate_type == InterestRateType.FIXED else 3.2
    elif loan_type == LoanType.VA:
        base_rate = 3.7 if interest_rate_type == InterestRateType.FIXED else 3.0
    elif loan_type == LoanType.USDA:
        base_rate = 3.9 if interest_rate_type == InterestRateType.FIXED else 3.2
    elif loan_type == LoanType.JUMBO:
        base_rate = 4.2 if interest_rate_type == InterestRateType.FIXED else 3.5
    elif loan_type == LoanType.HOME_EQUITY:
        base_rate = 5.5  # HELOCs typically higher
    elif loan_type == LoanType.REVERSE_MORTGAGE:
        base_rate = 4.5
    elif loan_type == LoanType.CONSTRUCTION:
        base_rate = 5.0 if interest_rate_type == InterestRateType.FIXED else 4.2
    else:  # conventional
        base_rate = 3.8 if interest_rate_type == InterestRateType.FIXED else 3.0

    # Apply historical adjustment and add some randomness
    base_rate += base_interest_rate_adjustment
    base_rate += random.uniform(-0.25, 0.25)  # Small random variation
    base_rate = max(2.0, min(12.0, base_rate))  # Keep within reasonable bounds
    base_interest_rate = round(base_rate, 3)

    # Create the loan product dictionary
    loan_product = {
        "product_name": product_name,
        "product_code": product_code,
        "description": description,
        "loan_type": loan_type.value,
        "interest_rate_type": interest_rate_type.value,
        "base_interest_rate": base_interest_rate,
        "min_term_months": min_term_months,
        "max_term_months": max_term_months,
        "min_loan_amount": min_loan_amount,
        "max_loan_amount": max_loan_amount,
        "min_credit_score": min_credit_score,
        "min_down_payment_percentage": min_down_payment_percentage,
        "requires_pmi": requires_pmi,
        "is_active": is_active,
        "launch_date": launch_date_str,
        "discontinue_date": discontinue_date_str
    }

    return loan_product


def generate_product_name(loan_type, interest_rate_type):
    """Generate a plausible marketing name for a loan product."""

    # Bank/lender names
    lenders = ["Premier", "Horizon", "Liberty", "Nationwide", "First", "Century",
               "Golden State", "Heritage", "Pinnacle", "Cornerstone", "Capital",
               "Alliance", "Freedom", "HomePoint", "Patriot", "Sovereign",
               "United", "Royal", "Prosperity", "Guardian", "River"]

    # Product type adjectives
    adjectives = ["Advantage", "Select", "Premium", "Essential", "Preferred", "Elite",
                  "Platinum", "Gold", "Silver", "Choice", "Smart", "Value", "Optimum",
                  "Signature", "Classic", "Flexible", "Prime", "Standard", "Custom"]

    # Product type suffixes
    suffixes = ["Mortgage", "Home Loan", "Financing", "Advantage", "Solution",
                "Option", "Plan", "Path", "Choice"]

    # Specific product names by type
    if loan_type == "conventional":
        name = f"{random.choice(lenders)} {random.choice(adjectives)} {interest_rate_type} {random.choice(suffixes)}"
    elif loan_type == "FHA":
        name = f"{random.choice(lenders)} FHA {interest_rate_type} {random.choice(suffixes)}"
    elif loan_type == "VA":
        name = f"{random.choice(lenders)} VA {interest_rate_type} {random.choice(suffixes)}"
    elif loan_type == "USDA":
        name = f"{random.choice(lenders)} USDA Rural {random.choice(suffixes)}"
    elif loan_type == "jumbo":
        name = f"{random.choice(lenders)} {random.choice(adjectives)} Jumbo {random.choice(suffixes)}"
    elif loan_type == "HELOC":
        name = f"{random.choice(lenders)} Home Equity Line of Credit"
    elif loan_type == "reverse mortgage":
        name = f"{random.choice(lenders)} {random.choice(adjectives)} Reverse Mortgage"
    elif loan_type == "construction loan":
        name = f"{random.choice(lenders)} {random.choice(adjectives)} Construction {random.choice(suffixes)}"
    else:
        name = f"{random.choice(lenders)} {random.choice(adjectives)} {random.choice(suffixes)}"

    return name


def generate_product_description(loan_type, interest_rate_type, product_name):
    """Generate a plausible description for a loan product."""

    base_desc = None

    # Common benefits and features
    common_benefits = [
        "competitive rates",
        "flexible terms",
        "personalized service",
        "quick closing options",
        "low fees",
        "rate lock options",
        "online application and management",
        "dedicated loan officer",
        "streamlined approval process"
    ]

    # Select 2-4 random benefits
    num_benefits = random.randint(2, 4)
    selected_benefits = random.sample(common_benefits, num_benefits)
    benefits_text = ", ".join(selected_benefits)

    # Base description by loan type
    if loan_type == "conventional":
        base_desc = f"A traditional {interest_rate_type} rate mortgage offering "
        if interest_rate_type == "fixed":
            base_desc += "stable payments over the life of the loan."
        else:
            base_desc += "an initial fixed rate period followed by rate adjustments based on market conditions."

    elif loan_type == "FHA":
        base_desc = f"A government-backed loan with {interest_rate_type} interest rates, designed for borrowers with lower credit scores or limited down payment funds."

    elif loan_type == "VA":
        base_desc = f"A loan program for qualified veterans, active military personnel, and eligible spouses, offering {interest_rate_type} rates with no down payment requirement."

    elif loan_type == "USDA":
        base_desc = "A zero-down payment loan program for eligible rural and suburban homebuyers, backed by the U.S. Department of Agriculture."

    elif loan_type == "jumbo":
        base_desc = f"A {interest_rate_type} rate mortgage for high-value properties exceeding conventional loan limits."

    elif loan_type == "HELOC":
        base_desc = "A revolving line of credit secured by your home equity, allowing you to borrow as needed during the draw period."

    elif loan_type == "reverse mortgage":
        base_desc = "A loan that allows homeowners 62 and older to convert part of their home equity into cash without making monthly mortgage payments."

    elif loan_type == "construction loan":
        base_desc = f"A short-term, {interest_rate_type}-rate loan designed to finance the building of a new home, with funds disbursed in stages as construction progresses."

    # Combine base description with benefits
    full_description = f"The {product_name} offers {base_desc} Enjoy {benefits_text}. "

    # Add some specific details based on loan type
    if loan_type == "conventional":
        full_description += "Ideal for borrowers with good credit looking for predictable mortgage payments."

    elif loan_type == "FHA":
        full_description += "Perfect for first-time homebuyers or those with less-than-perfect credit."

    elif loan_type == "VA":
        full_description += "One of the best benefits available to those who have served our country."

    elif loan_type == "USDA":
        full_description += "Helps make home ownership accessible for moderate-income families in eligible rural areas."

    elif loan_type == "jumbo":
        full_description += "Designed for luxury properties and high-cost housing markets."

    elif loan_type == "HELOC":
        full_description += "A flexible financial tool for home improvements, education expenses, or other major purchases."

    elif loan_type == "reverse mortgage":
        full_description += "Provides financial security for seniors while allowing them to remain in their homes."

    elif loan_type == "construction loan":
        full_description += "Can be converted to a permanent mortgage once construction is complete."

    return full_description
