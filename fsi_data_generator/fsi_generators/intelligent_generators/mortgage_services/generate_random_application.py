import random
from datetime import datetime, timedelta

import numpy as np


def generate_random_application(loan_product=None):
    """
    Generate a random mortgage application with plausible values.

    Args:
        loan_product (dict, optional): Loan product details to use for constraints.
            If provided, the generated application will conform to the product specifications.

    Returns:
        dict: A dictionary with comprehensive mortgage application details.
    """
    # If no loan product provided, use default values
    if loan_product is None:
        loan_product = {
            "loan_type": "conventional",
            "interest_rate_type": "fixed",
            "base_interest_rate": 4.125,
            "min_term_months": 360,
            "max_term_months": 360,
            "min_loan_amount": 50000,
            "max_loan_amount": 647200,
            "min_credit_score": 640,
            "min_down_payment_percentage": 3.0,
            "requires_pmi": True,
            "is_active": True
        }

    # Extract loan product details
    product_type = loan_product.get("loan_type", "conventional")
    is_product_active = loan_product.get("is_active", True)
    min_credit_score = loan_product.get("min_credit_score", 620)
    min_loan_amount = loan_product.get("min_loan_amount", 50000)
    max_loan_amount = loan_product.get("max_loan_amount", 647200)
    min_term_months = loan_product.get("min_term_months", 60)
    max_term_months = loan_product.get("max_term_months", 360)

    # Map loan product type to application type
    if product_type.upper() == "HELOC":
        application_type = "HELOC"
    elif product_type.upper() in ["CONVENTIONAL", "FHA", "VA", "USDA", "JUMBO"]:
        # For most mortgage types, randomly choose between purchase and refinance
        application_type = random.choices(
            ["purchase", "refinance"],
            weights=[0.6, 0.4]
        )[0]
    else:
        application_type = random.choices(
            ["purchase", "refinance", "HELOC"],
            weights=[0.5, 0.4, 0.1]
        )[0]

    # Define loan purposes based on application type
    purpose_map = {
        "purchase": ["primary residence", "second home", "investment property"],
        "refinance": ["rate and term refinancing", "cash-out refinancing", "home improvement", "refinancing"],
        "HELOC": ["home improvement", "debt consolidation", "education expenses", "other purpose"]
    }
    loan_purpose = random.choice(purpose_map.get(application_type, ["primary residence"]))

    # Application status depends on product activity
    if not is_product_active:
        # If product is not active, application must be in an inactive state
        status = random.choice(["denied", "withdrawn", "cancelled"])
    else:
        # Normal status distribution for active products
        statuses = ["draft", "submitted", "under review", "approved", "denied", "withdrawn", "funded", "cancelled"]
        # Set the probability of "approved" to 90%
        approved_weight = 0.9
        remaining_weight = 1 - approved_weight  # Remaining weight for other statuses
        other_weights = [0.15, 0.10, 0.15, 0.10, 0.05, 0.15, 0.05]  # Original weights excluding "approved"
        normalized_other_weights = [w * (remaining_weight / sum(other_weights)) for w in other_weights]

        # Create the new weights, with "approved" having 90%
        status_weights = normalized_other_weights[:3] + [approved_weight] + normalized_other_weights[3:]

        # Randomly choose a status
        status = random.choices(statuses, weights=status_weights, k=1)[0]

    # Generate credit score based on product requirements
    credit_distribution = np.random.normal(loc=max(700, min_credit_score + 30), scale=50)
    credit_score = max(min_credit_score, min(850, int(credit_distribution)))

    # Generate dates
    now = datetime.now()
    max_years_past = 30  # Applications from up to 30 years ago
    days_past = random.randint(0, 365 * max_years_past)
    creation_date = now - timedelta(days=days_past)

    # Submission date is after creation date (or sometimes same day)
    max_days_to_submit = min(60, days_past)  # Typically submitted within 60 days
    days_to_submit = random.randint(0, max_days_to_submit)
    submission_date = creation_date + timedelta(days=days_to_submit)

    # Last updated date is between submission and now
    days_since_submission = (now - submission_date).days
    if days_since_submission > 0:
        days_to_update = random.randint(0, days_since_submission)
        last_updated_date = submission_date + timedelta(days=days_to_update)
    else:
        last_updated_date = submission_date

    # Generate loan term within product constraints
    if application_type == "HELOC":
        term_options = [60, 120, 180, 240, 300, 360]  # 5, 10, 15, 20, 25, or 30 years
    else:
        term_options = [180, 240, 360]  # 15, 20, or 30 years

    # Filter terms to only those within product constraints
    term_options = [t for t in term_options if min_term_months <= t <= max_term_months]

    # If no options match the constraints, use the min term
    if not term_options:
        requested_loan_term_months = min_term_months
    else:
        requested_loan_term_months = random.choice(term_options)

    # Generate loan amount based on product constraints and application type
    loan_amount_base = {
        "purchase": (min_loan_amount + max_loan_amount) / 2,
        "refinance": (min_loan_amount + max_loan_amount) / 2,
        "HELOC": min(150000, (min_loan_amount + max_loan_amount) / 2)
    }.get(application_type, (min_loan_amount + max_loan_amount) / 2)

    # Better credit = higher loan amount potential
    credit_factor = 0.5 + ((credit_score - min_credit_score) / (850 - min_credit_score)) * 1.0

    # Add randomness to loan amount
    loan_amount_variation = min((max_loan_amount - min_loan_amount) / 4, loan_amount_base * 0.4)
    prelim_amount = loan_amount_base * credit_factor + random.uniform(-loan_amount_variation, loan_amount_variation)

    # Ensure it's within the product's constraints
    requested_loan_amount = round(max(min_loan_amount, min(max_loan_amount, prelim_amount)), 2)

    # Estimated property value is typically higher than loan amount (unless high LTV)
    ltv_ratio = random.uniform(0.6, 0.95)  # Loan-to-Value ratio
    estimated_property_value = round(requested_loan_amount / ltv_ratio, 2)

    # Referral sources with realistic weights
    referral_sources = [
        "online ad", "real estate agent", "direct mail", "walk-in",
        "referral", "social media", "returning customer"
    ]
    referral_weights = [0.25, 0.20, 0.10, 0.15, 0.20, 0.05, 0.05]
    referral_source = random.choices(referral_sources, weights=referral_weights)[0]

    # Create the application dictionary
    _application = {
        "application_type": application_type,
        "status": status,
        "creation_date_time": creation_date.strftime("%Y-%m-%d %H:%M:%S.%f"),
        "submission_date_time": submission_date.strftime("%Y-%m-%d %H:%M:%S.%f"),
        "last_updated_date_time": last_updated_date.strftime("%Y-%m-%d %H:%M:%S.%f"),
        "loan_purpose": loan_purpose,
        "requested_loan_amount": requested_loan_amount,
        "requested_loan_term_months": requested_loan_term_months,
        "estimated_property_value": estimated_property_value,
        "estimated_credit_score": credit_score,
        "referral_source": referral_source
    }

    return _application
