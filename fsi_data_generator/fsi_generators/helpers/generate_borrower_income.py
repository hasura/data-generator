import random
from datetime import datetime, timedelta
import json


def generate_borrower_income(_ids_dict, _dg):
    """
    Generate a single random, realistic borrower income record.

    Returns:
        dict: A dictionary containing a realistic income record
    """
    # Income types based on the sample data, excluding W-2 wages (salary and hourly wages)
    income_types = [
        "self-employment", "rental income", "investment income", "pension",
        "social security", "disability income", "alimony", "child support", "other"
    ]

    # Frequency options
    frequencies = ["weekly", "bi-weekly", "semi-monthly", "monthly", "annually", "one-time"]

    # Verification status options
    verification_statuses = ["verified", "not verified", "pending", "partial verification"]

    # Generate a random date within the last 5 years
    end_date = datetime.now()
    start_date = end_date - timedelta(days=5 * 365)
    random_days = random.randint(0, (end_date - start_date).days)
    random_date = start_date + timedelta(days=random_days)
    verification_date = random_date.strftime("%Y-%m-%d")

    # Generate realistic income amounts based on type
    income_type = random.choice(income_types)

    # Base amounts by income type (realistic annual ranges in USD)
    base_amounts = {
        "self-employment": (25000, 250000),
        "rental income": (12000, 150000),
        "investment income": (5000, 200000),
        "pension": (15000, 80000),
        "social security": (10000, 40000),
        "disability income": (8000, 40000),
        "alimony": (10000, 60000),
        "child support": (5000, 30000),
        "other": (1000, 50000)
    }

    # Get base annual amount for the selected income type
    annual_min, annual_max = base_amounts[income_type]
    annual_amount = round(random.uniform(annual_min, annual_max), 2)

    # Adjust amount based on frequency
    frequency = random.choice(frequencies)
    amount = annual_amount

    if frequency == "monthly":
        amount = round(annual_amount / 12, 2)
    elif frequency == "bi-weekly":
        amount = round(annual_amount / 26, 2)
    elif frequency == "semi-monthly":
        amount = round(annual_amount / 24, 2)
    elif frequency == "weekly":
        amount = round(annual_amount / 52, 2)
    elif frequency == "one-time":
        # One-time payments might vary more
        amount = round(random.uniform(1000, annual_amount * 1.5), 2)

    # Create and return the income record
    income_record = {
        "income_type": income_type,
        "amount": amount,
        "frequency": frequency,
        "verification_status": random.choice(verification_statuses),
        "verification_date": verification_date
    }

    return income_record

