import random
import datetime
from typing import Dict, Any, Optional
import psycopg2


def generate_random_closing_disclosure(id_fields: Dict[str, Any], dg) -> Dict[str, Any]:
    """
    Generate a random mortgage services closing disclosure record with reasonable values.

    Args:
        id_fields: Dictionary containing the required ID fields (mortgage_services_loan_id)
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated closing disclosure data (without ID fields)
    """
    # Get loan information to make closing disclosure data reasonable
    conn = dg.conn
    loan_info = get_loan_info(id_fields.get("mortgage_services_loan_id"), conn)

    # Define possible values for categorical fields
    disclosure_types = [
        "initial closing disclosure",
        "revised closing disclosure",
        "final closing disclosure"
    ]

    # Generate created date
    today = datetime.date.today()

    if loan_info and 'origination_date' in loan_info and loan_info['origination_date']:
        # For loans that have originated, set created date before origination
        days_before_origination = random.randint(3, 14)
        created_date = loan_info['origination_date'] - datetime.timedelta(days=days_before_origination)
    else:
        # For loans without origination date, use a reasonable date in the past
        days_ago = random.randint(7, 90)
        created_date = today - datetime.timedelta(days=days_ago)

    # Determine disclosure type based on proximity to loan origination
    if loan_info and 'origination_date' in loan_info and loan_info['origination_date']:
        # For loans that have originated
        days_diff = (loan_info['origination_date'] - created_date).days

        if days_diff <= 3:
            disclosure_type = "final closing disclosure"
        elif days_diff <= 7:
            disclosure_type = random.choices(
                ["revised closing disclosure", "final closing disclosure"],
                weights=[0.7, 0.3],
                k=1
            )[0]
        else:
            disclosure_type = "initial closing disclosure"
    else:
        # For loans without origination date
        disclosure_type = random.choices(
            disclosure_types,
            weights=[0.6, 0.3, 0.1],  # Initial is most common
            k=1
        )[0]

    # Generate sent date (typically 0-3 days after created date)
    days_after_creation = random.randint(0, 3)
    sent_date = created_date + datetime.timedelta(days=days_after_creation)

    # Generate received date (typically 1-5 days after sent date)
    if random.random() < 0.9:  # 90% of disclosures have received dates
        days_after_sent = random.randint(1, 5)
        received_date = sent_date + datetime.timedelta(days=days_after_sent)
    else:
        received_date = None

    # Set document path
    loan_id = id_fields.get("mortgage_services_loan_id")
    file_id = random.randint(10000, 99999)
    document_path = f"/documents/closing_disclosures/{loan_id}/{disclosure_type.replace(' ', '_')}_{file_id}.pdf"

    # Determine financial values based on loan information
    if loan_info:
        # Use loan data with small variations
        loan_amount = loan_info.get('loan_amount', None)
        if loan_amount is None:
            loan_amount = random.uniform(100000, 500000)
        else:
            # Small variation from loan amount
            loan_amount = loan_amount * random.uniform(0.98, 1.02)

        interest_rate: Optional[float] = loan_info.get('interest_rate', None)
        if interest_rate is None:
            interest_rate = random.uniform(3.0, 7.0)
        else:
            # Small variation from loan interest rate
            interest_rate = max(2.5, min(8.0, interest_rate + random.uniform(-0.25, 0.25)))

        monthly_payment: Optional[float] = loan_info.get('monthly_payment', None)
        if monthly_payment is None:
            # Estimate monthly payment based on loan amount and interest rate
            monthly_payment = estimate_monthly_payment(loan_amount, interest_rate, 360)  # 30-year term
        else:
            # Small variation from loan monthly payment
            monthly_payment = monthly_payment * random.uniform(0.98, 1.02)
    else:
        # Generate reasonable values
        loan_amount = random.uniform(100000, 500000)
        interest_rate = random.uniform(3.0, 7.0)
        monthly_payment = estimate_monthly_payment(loan_amount, interest_rate, 360)  # 30-year term

    # Generate total closing costs (typically 2-5% of loan amount)
    closing_cost_percentage = random.uniform(0.02, 0.05)
    total_closing_costs = loan_amount * closing_cost_percentage

    # Generate cash to close
    if loan_info and 'loan_amount' in loan_info and loan_info.get('down_payment'):
        # Cash to close is typically down payment plus closing costs
        cash_to_close = loan_info.get('down_payment', 0) + total_closing_costs
    else:
        # Estimate cash to close as 20% of purchase price plus closing costs
        estimated_down_payment = loan_amount * 0.25  # Assuming loan is 80% of purchase price
        cash_to_close = estimated_down_payment + total_closing_costs

    # Round financial values
    loan_amount = round(loan_amount, 2)
    interest_rate = round(interest_rate, 3)
    monthly_payment = round(monthly_payment, 2)
    total_closing_costs = round(total_closing_costs, 2)
    cash_to_close = round(cash_to_close, 2)

    # Create the closing disclosure record
    closing_disclosure = {
        "disclosure_type": disclosure_type,
        "created_date": created_date,
        "sent_date": sent_date,
        "received_date": received_date,
        "document_path": document_path,
        "loan_amount": float(loan_amount),
        "interest_rate": float(interest_rate),
        "monthly_payment": float(monthly_payment),
        "total_closing_costs": float(total_closing_costs),
        "cash_to_close": float(cash_to_close)
    }

    return closing_disclosure


def get_loan_info(loan_id: Optional[int], conn) -> Optional[Dict[str, Any]]:
    """
    Get loan information to make closing disclosure data reasonable.

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
            SELECT loan_amount, interest_rate, monthly_payment, down_payment, origination_date
            FROM mortgage_services.loans 
            WHERE mortgage_services_loan_id = %s
        """, (loan_id,))

        result = cursor.fetchone()
        cursor.close()

        if result:
            return {
                "loan_amount": float(result[0]) if result[0] is not None else None,
                "interest_rate": float(result[1]) if result[1] is not None else None,
                "monthly_payment": float(result[2]) if result[2] is not None else None,
                "down_payment": float(result[3]) if result[3] is not None else None,
                "origination_date": result[4]
            }
        else:
            return None

    except (Exception, psycopg2.Error) as error:
        print(f"Error fetching loan information: {error}")
        return None


def estimate_monthly_payment(loan_amount: float, annual_interest_rate: float, term_months: int) -> float:
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
