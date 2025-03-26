import datetime
import logging
import random
from typing import Any, Dict, Optional

import psycopg2

logger = logging.getLogger(__name__)


def generate_random_closed_loan(id_fields: Dict[str, Any], dg) -> Dict[str, Any]:
    """
    Generate a random mortgage services closed loan record with reasonable values.

    Args:
        id_fields: Dictionary containing the required ID fields (mortgage_services_loan_id)
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated closed loan data (without ID fields)
    """
    # Get loan information to make closed loan data reasonable
    conn = dg.conn
    loan_info = get_loan_info(id_fields.get("mortgage_services_loan_id"), conn)

    # Define possible values for categorical fields
    settlement_agents = [
        "John Smith", "Maria Garcia", "David Johnson", "Sarah Lee",
        "Michael Brown", "Jennifer Wilson", "Robert Davis", "Lisa Miller",
        "William Rodriguez", "Elizabeth Martinez", "James Taylor", "Patricia Thomas"
    ]

    settlement_companies = [
        "First American Title", "Fidelity National Title", "Old Republic Title",
        "Stewart Title", "Chicago Title", "Investors Title", "Title Resources",
        "North American Title", "Commonwealth Land Title", "WFG National Title"
    ]

    # Get base data from loan
    today = datetime.date.today()

    if loan_info and loan_info.get('origination_date'):
        closing_date = loan_info.get('origination_date')
    else:
        # If no origination date, use a reasonable past date
        days_ago = random.randint(30, 365)
        closing_date = today - datetime.timedelta(days=days_ago)

    # Funding date is typically 1-3 days after closing
    funding_days_after = random.randint(1, 3)
    funding_date = closing_date + datetime.timedelta(days=funding_days_after)

    # Disbursement date is typically same as funding date, occasionally 1 day later
    if random.random() < 0.8:  # 80% chance same as funding date
        disbursement_date = funding_date
    else:
        disbursement_date = funding_date + datetime.timedelta(days=1)

    # First payment is typically first day of the month 1-2 months after closing
    # Calculate first payment month
    payment_month = closing_date.month + random.randint(1, 2)
    payment_year = closing_date.year
    if payment_month > 12:
        payment_month -= 12
        payment_year += 1
    first_payment_date = datetime.date(payment_year, payment_month, 1)

    # Maturity date is first payment date plus term (typically 30 years = 360 months)
    if loan_info and loan_info.get('loan_term_months'):
        term_months = loan_info.get('loan_term_months')
    else:
        # Default to common term options
        term_options = [180, 240, 360]  # 15, 20, or 30 years
        term_weights = [0.15, 0.15, 0.7]  # 30 years is most common
        term_months = random.choices(term_options, weights=term_weights, k=1)[0]

    # Calculate maturity date
    years = term_months // 12
    months = term_months % 12
    maturity_year = first_payment_date.year + years
    maturity_month = first_payment_date.month + months
    if maturity_month > 12:
        maturity_month -= 12
        maturity_year += 1
    maturity_date = datetime.date(maturity_year, maturity_month, 1)

    # Recording date is typically 1-10 days after closing
    recording_days_after = random.randint(1, 10)
    recording_date = closing_date + datetime.timedelta(days=recording_days_after)

    # Generate financial values
    if loan_info:
        final_loan_amount = loan_info.get('loan_amount', None)
        final_interest_rate = loan_info.get('interest_rate', None)
        final_monthly_payment = loan_info.get('monthly_payment', None)
    else:
        final_loan_amount: Optional[float] = None
        final_interest_rate: Optional[float] = None
        final_monthly_payment: Optional[float] = None

    # Generate reasonable defaults if values are missing
    if final_loan_amount is None:
        final_loan_amount = round(random.uniform(100000, 500000), 2)
    else:
        # Small variation from original amount
        final_loan_amount = round(final_loan_amount * random.uniform(0.995, 1.005), 2)

    if final_interest_rate is None:
        final_interest_rate = round(random.uniform(3.0, 7.0), 3)
    else:
        # Small variation from original rate
        final_interest_rate = round(final_interest_rate * random.uniform(0.995, 1.005), 3)

    if final_monthly_payment is None:
        final_monthly_payment = round(_estimate_monthly_payment(final_loan_amount, final_interest_rate, term_months), 2)
    else:
        # Small variation from original payment
        final_monthly_payment = round(final_monthly_payment * random.uniform(0.995, 1.005), 2)

    # Generate final cash to close
    down_payment_percentage = random.uniform(0.03, 0.25)  # 3% to 25% down payment
    home_price = final_loan_amount / (1 - down_payment_percentage)
    down_payment = home_price * down_payment_percentage

    # Closing costs typically 2-5% of loan amount
    closing_costs = final_loan_amount * random.uniform(0.02, 0.05)

    # Cash to close is typically down payment plus closing costs
    final_cash_to_close = down_payment + closing_costs

    # Round financial values
    final_cash_to_close = round(final_cash_to_close, 2)

    # Select settlement agent and company
    settlement_agent = random.choice(settlement_agents)
    settlement_company = random.choice(settlement_companies)

    # Create the closed loan record
    closed_loan = {
        "closing_date": closing_date,
        "funding_date": funding_date,
        "final_loan_amount": float(final_loan_amount),
        "final_interest_rate": float(final_interest_rate),
        "final_monthly_payment": float(final_monthly_payment),
        "final_cash_to_close": float(final_cash_to_close),
        "disbursement_date": disbursement_date,
        "first_payment_date": first_payment_date,
        "maturity_date": maturity_date,
        "recording_date": recording_date,
        "settlement_agent": settlement_agent,
        "settlement_company": settlement_company
    }

    return closed_loan


def get_loan_info(loan_id: Optional[int], conn) -> Optional[Dict[str, Any]]:
    """
    Get loan information to make closed loan data reasonable.

    Args:
        loan_id: The ID of the loan
        conn: PostgreSQL connection object

    Returns:
        Dictionary containing loan information or None if loan_id is None or loan not found
    """
    if not loan_id:
        return None

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT loan_amount, interest_rate, loan_term_months, monthly_payment, 
                   down_payment, origination_date
            FROM mortgage_services.loans 
            WHERE mortgage_services_loan_id = %s
        """, (loan_id,))

        result = cursor.fetchone()
        cursor.close()

        return result

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching loan information: {error}")
        return None


def _estimate_monthly_payment(loan_amount: float, annual_interest_rate: float, term_months: int) -> float:
    """
    Estimate monthly payment for a loan.

    Args:
        loan_amount: Principal amount of the loan
        annual_interest_rate: Annual interest rate (percentage)
        term_months: Term of the loan in months

    Returns:
        Estimated monthly payment
    """
    # Convert annual interest rate to monthly
    monthly_interest_rate = annual_interest_rate / 100 / 12

    # Calculate monthly payment using the loan payment formula
    if monthly_interest_rate == 0:
        return loan_amount / term_months
    else:
        return loan_amount * (monthly_interest_rate * (1 + monthly_interest_rate) ** term_months) / \
            ((1 + monthly_interest_rate) ** term_months - 1)
