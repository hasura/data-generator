import datetime
import logging
import random
from decimal import Decimal
from typing import Any, Dict

import psycopg2

logger = logging.getLogger(__name__)


def generate_random_borrower_liability(id_fields: Dict[str, Any], dg) -> Dict[str, Any]:
    """
    Generate a random mortgage services borrower liability record with reasonable values.

    Args:
        id_fields: Dictionary containing the required ID fields (like mortgage_services_borrower_id)
        dg: DataGenertor instance

    Returns:
        Dictionary containing randomly generated borrower liability data (without ID fields)
    """
    # Define possible values for categorical fields
    conn = dg.conn
    liability_types = [
        "credit card", "auto loan", "student loan", "personal loan",
        "HELOC", "medical debt", "retail credit"
    ]

    creditor_names = [
        "Chase Bank", "Bank of America", "Wells Fargo", "Citibank",
        "Capital One", "Discover", "American Express", "Sallie Mae",
        "Navient", "SoFi", "USAA", "PNC Bank", "TD Bank", "Synchrony Bank"
    ]

    # Get borrower income information to make liability data reasonable
    borrower_income = get_borrower_income(id_fields["mortgage_services_borrower_id"], conn)

    # Generate a reasonable monthly payment based on borrower income
    # Typically, all debt payments should be less than 43% of income for mortgage qualification
    max_monthly_payment = borrower_income * Decimal('0.1')  # Individual debt up to 10% of income
    monthly_payment = round(random.uniform(50, float(max_monthly_payment)), 2)

    # Generate reasonable amounts for other fields
    current_balance = round(monthly_payment * random.randint(6, 120), 2)  # 6 months to 10 years worth of payments

    # Generate original amount (slightly higher than current balance)
    original_amount = round(current_balance * random.uniform(1.05, 1.5), 2)

    # Generate reasonable interest rate
    liability_type = random.choice(liability_types)

    # Different liability types have different typical interest rate ranges
    if liability_type == "credit card":
        interest_rate = round(random.uniform(12.0, 24.99), 3)
    elif liability_type == "auto loan":
        interest_rate = round(random.uniform(3.0, 8.0), 3)
    elif liability_type == "student loan":
        interest_rate = round(random.uniform(4.0, 7.5), 3)
    elif liability_type == "personal loan":
        interest_rate = round(random.uniform(6.0, 15.0), 3)
    else:
        interest_rate = round(random.uniform(5.0, 12.0), 3)

    # Generate dates
    today = datetime.date.today()

    # Origination date (1-10 years ago)
    years_ago = random.randint(1, 10)
    origination_date = today - datetime.timedelta(days=365 * years_ago + random.randint(0, 364))

    # Maturity date (0-15 years in future, depending on liability type)
    if liability_type in ["auto loan", "personal loan"]:
        years_in_future = random.randint(1, 5)
    elif liability_type == "student loan":
        years_in_future = random.randint(5, 15)
    else:
        years_in_future = random.randint(1, 10)

    maturity_date = today + datetime.timedelta(days=365 * years_in_future + random.randint(0, 364))

    # Generate verification status and date
    verification_statuses = ["self-reported", "verified", "pending verification"]
    verification_status = random.choice(verification_statuses)

    verification_date = None
    if verification_status == "verified":
        # Verification happened between 1 and 30 days ago
        days_ago = random.randint(1, 30)
        verification_date = today - datetime.timedelta(days=days_ago)

    # Decide if the liability will be paid off with mortgage proceeds
    will_be_paid_off = random.random() < 0.3  # 30% chance of being paid off

    # Create the liability record
    liability = {
        "liability_type": liability_type,
        "creditor_name": random.choice(creditor_names),
        "account_number": f"xxxx-xxxx-xxxx-{random.randint(1000, 9999)}",
        "monthly_payment": monthly_payment,
        "current_balance": current_balance,
        "original_amount": original_amount,
        "interest_rate": interest_rate,
        "origination_date": origination_date,
        "maturity_date": maturity_date,
        "verification_status": verification_status,
        "verification_date": verification_date,
        "will_be_paid_off": will_be_paid_off
    }

    return liability


def get_borrower_income(borrower_id: int, conn) -> Decimal:
    """
    Get the borrower's monthly income to make liability data reasonable.

    Args:
        borrower_id: The ID of the borrower
        conn: PostgreSQL connection object

    Returns:
        Monthly income as a Decimal
    """
    try:
        cursor = conn.cursor()

        # First try to get income from borrower_employments
        cursor.execute("""
            SELECT SUM(monthly_income) 
            FROM mortgage_services.borrower_employments 
            WHERE mortgage_services_borrower_id = %s
        """, (borrower_id,))

        result = cursor.fetchone()
        income = result[0] if result and result[0] else None

        # If no employment income, check borrower_incomes
        if not income:
            cursor.execute("""
                SELECT SUM(amount) 
                FROM mortgage_services.borrower_incomes 
                WHERE mortgage_services_borrower_id = %s
                AND frequency = 'Monthly'
            """, (borrower_id,))

            result = cursor.fetchone()
            income = result[0] if result and result[0] else None

            # If no monthly income records, check for annual income and convert
            if not income:
                cursor.execute("""
                    SELECT SUM(amount) 
                    FROM mortgage_services.borrower_incomes 
                    WHERE mortgage_services_borrower_id = %s
                    AND frequency = 'Annual'
                """, (borrower_id,))

                result = cursor.fetchone()
                if result and result[0]:
                    income = Decimal(result[0]) / 12

        cursor.close()

        # If no income found, use a reasonable default
        if not income or income <= 0:
            income = Decimal('5000.00')  # Reasonable default monthly income

        return income

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching borrower income: {error}")
        # Return a reasonable default if there's an error
        return Decimal('5000.00')
