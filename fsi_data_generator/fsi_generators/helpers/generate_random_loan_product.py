import random
import string

# List of possible loan types
loan_types = ['conventional', 'FHA', 'VA', 'USDA', 'jumbo', 'HELOC', 'reverse mortgage', 'construction loan']

def generate_random_loan_product(_ids_dict, _dg):
    """
    Generate a random, plausible loan product that could be currently offered
    or a historical product from the prior 30 years.

    Returns a dictionary with loan product details.
    """

    min_term_months = None
    max_term_months = None
    min_loan_amount = None
    max_loan_amount = None
    min_credit_score = None
    min_down_payment_percentage = None
    requires_pmi = None

    # Select a loan type
    loan_type = random.choice(loan_types)

    # Generate interest rate type based on loan type
    if loan_type == "HELOC":
        # HELOCs are almost always adjustable
        interest_rate_type = "adjustable"
    else:
        # Other products can be fixed or adjustable
        interest_rate_type = random.choice(["fixed", "adjustable", "fixed", "fixed"])  # Weighted toward fixed

    # Generate a product name
    product_name = generate_product_name(loan_type, interest_rate_type)

    # Generate a product code (alphanumeric, typically 4-10 characters)
    code_length = random.randint(4, 10)
    product_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=code_length))

    # Generate a description
    description = generate_product_description(loan_type, interest_rate_type, product_name)

    # Determine if the product is active (70% chance of being active)
    is_active = random.random() < 0.7

    # Generate loan terms based on loan type
    if loan_type == "conventional":
        min_term_months = random.choice([120, 180, 240])  # 10, 15, 20 years
        max_term_months = 360  # 30 years
        min_loan_amount = random.choice([10000, 25000, 50000])
        max_loan_amount = random.choice(
            [417000, 510400, 548250, 647200, 822375])  # Conforming limits from different years
        min_credit_score = random.choice([620, 640, 660])
        min_down_payment_percentage = random.choice([3.0, 5.0, 10.0])
        requires_pmi = min_down_payment_percentage < 20.0

    elif loan_type == "FHA":
        min_term_months = random.choice([120, 180, 240])  # 10, 15, 20 years
        max_term_months = 360  # 30 years
        min_loan_amount = random.choice([5000, 10000, 25000])
        # FHA limits vary by location and year
        max_loan_amount = random.choice([294515, 331760, 356362, 420680, 472030, 510400, 765600])
        min_credit_score = random.choice([500, 580, 600, 620])
        min_down_payment_percentage = 3.5 if min_credit_score >= 580 else 10.0
        requires_pmi = True  # FHA loans require mortgage insurance premium (MIP)

    elif loan_type == "VA":
        min_term_months = random.choice([120, 180, 240])  # 10, 15, 20 years
        max_term_months = 360  # 30 years
        min_loan_amount = random.choice([10000, 25000, 36000])
        max_loan_amount = random.choice([417000, 484350, 510400, 548250, 647200, 0])  # 0 = no limit for some periods
        min_credit_score = random.choice([580, 600, 620])
        min_down_payment_percentage = 0.0
        requires_pmi = False  # VA loans don't require PMI

    elif loan_type == "USDA":
        min_term_months = 360  # USDA typically only offers 30-year terms
        max_term_months = 360
        min_loan_amount = random.choice([5000, 10000])
        max_loan_amount = random.choice([250000, 300000, 350000, 400000])
        min_credit_score = random.choice([640, 660])
        min_down_payment_percentage = 0.0
        requires_pmi = True  # USDA loans have a guarantee fee

    elif loan_type == "jumbo":
        min_term_months = random.choice([120, 180, 240])
        max_term_months = random.choice([360, 480, 600])  # Some jumbo loans offer 40 or 50 year terms
        min_loan_amount = random.choice(
            [417001, 453101, 484351, 510401, 548251, 647201, 765601])  # Just above conforming limits
        max_loan_amount = random.choice([1000000, 1500000, 2000000, 2500000, 5000000, 10000000])
        min_credit_score = random.choice([680, 700, 720, 740])
        min_down_payment_percentage = random.choice([10.0, 15.0, 20.0, 25.0])
        requires_pmi = min_down_payment_percentage < 20.0

    elif loan_type == "HELOC":
        min_term_months = random.choice([60, 120])  # 5 or 10 year draw periods
        max_term_months = random.choice([180, 240, 300, 360])  # 15-30 year terms
        min_loan_amount = random.choice([10000, 15000, 25000])
        max_loan_amount = random.choice([250000, 500000, 750000, 1000000])
        min_credit_score = random.choice([660, 680, 700, 720])
        min_down_payment_percentage = 0.0  # HELOCs don't have down payments in the same way
        requires_pmi = False

    elif loan_type == "reverse mortgage":
        min_term_months = 0  # Reverse mortgages don't have fixed terms
        max_term_months = 0
        min_loan_amount = random.choice([10000, 25000, 50000])
        max_loan_amount = random.choice([417000, 510400, 625500, 765600, 970800])
        min_credit_score = 0  # Credit score is less important for reverse mortgages
        min_down_payment_percentage = 0.0
        requires_pmi = False

    elif loan_type == "construction loan":
        min_term_months = random.choice([6, 12, 18])
        max_term_months = random.choice([24, 36, 60])
        min_loan_amount = random.choice([50000, 100000])
        max_loan_amount = random.choice([500000, 750000, 1000000, 2000000])
        min_credit_score = random.choice([660, 680, 700])
        min_down_payment_percentage = random.choice([10.0, 15.0, 20.0, 25.0])
        requires_pmi = min_down_payment_percentage < 20.0

    # Randomly adjust for non-active (historical) products
    if not is_active:
        # Generate a date between 1 and 30 years ago when the product was discontinued
        years_ago = random.randint(1, 30)
        # Historical products might have had different parameters
        # Adjust base interest rate for historical products
        if years_ago > 25:  # 1990s
            base_interest_rate_adjustment = random.uniform(1.5, 5.0)
        elif years_ago > 15:  # 2000s
            base_interest_rate_adjustment = random.uniform(0.5, 2.0)
        elif years_ago > 5:  # 2010s
            base_interest_rate_adjustment = random.uniform(-0.5, 1.0)
        else:  # Recent
            base_interest_rate_adjustment = random.uniform(-0.25, 0.5)
    else:
        base_interest_rate_adjustment = 0

    # Generate base interest rate
    if loan_type == "FHA":
        base_rate = 4.0 if interest_rate_type == "fixed" else 3.2
    elif loan_type == "VA":
        base_rate = 3.7 if interest_rate_type == "fixed" else 3.0
    elif loan_type == "USDA":
        base_rate = 3.9 if interest_rate_type == "fixed" else 3.2
    elif loan_type == "jumbo":
        base_rate = 4.2 if interest_rate_type == "fixed" else 3.5
    elif loan_type == "HELOC":
        base_rate = 5.5  # HELOCs typically higher
    elif loan_type == "reverse mortgage":
        base_rate = 4.5
    elif loan_type == "construction loan":
        base_rate = 5.0 if interest_rate_type == "fixed" else 4.2
    else:  # conventional
        base_rate = 3.8 if interest_rate_type == "fixed" else 3.0

    # Apply historical adjustment and add some randomness
    base_rate += base_interest_rate_adjustment
    base_rate += random.uniform(-0.25, 0.25)  # Small random variation
    base_rate = max(2.0, min(12.0, base_rate))  # Keep within reasonable bounds
    base_interest_rate = round(base_rate, 3)

    # Create the loan product dictionary
    loan_product = {
        "product_name": product_name,
        "mortgage_services_loan_products_product_code": product_code,
        "description": description,
        "loan_type": loan_type,
        "interest_rate_type": interest_rate_type,
        "base_interest_rate": base_interest_rate,
        "min_term_months": min_term_months,
        "max_term_months": max_term_months,
        "min_loan_amount": min_loan_amount,
        "max_loan_amount": max_loan_amount,
        "min_credit_score": min_credit_score,
        "min_down_payment_percentage": min_down_payment_percentage,
        "requires_pmi": requires_pmi,
        "is_active": is_active
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


# Example usage
if __name__ == "__main__":
    # Generate a sample loan product
    product = generate_random_loan_product()

    # Print the product details
    print(f"Product Name: {product['product_name']}")
    print(f"Product Code: {product['product_code']}")
    print(f"Loan Type: {product['loan_type']}")
    print(f"Interest Rate Type: {product['interest_rate_type']}")
    print(f"Base Interest Rate: {product['base_interest_rate']}%")
    print(f"Term: {product['min_term_months']}-{product['max_term_months']} months")
    print(f"Loan Amount: ${product['min_loan_amount']:,} to ${product['max_loan_amount']:,}")

    if product['min_credit_score'] > 0:
        print(f"Minimum Credit Score: {product['min_credit_score']}")
    else:
        print("Minimum Credit Score: Not specified")

    print(f"Minimum Down Payment: {product['min_down_payment_percentage']}%")
    print(f"Requires PMI: {'Yes' if product['requires_pmi'] else 'No'}")
    print(f"Active Product: {'Yes' if product['is_active'] else 'No'}")
    print("\nDescription:")
    print(product['description'])
