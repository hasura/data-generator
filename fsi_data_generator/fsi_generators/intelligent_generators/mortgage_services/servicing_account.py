import datetime
import logging
import random
from typing import Any, Dict, Optional

import psycopg2

from fsi_data_generator.fsi_generators.intelligent_generators.mortgage_services.enums.servicing_account_status import \
    ServicingAccountStatus

logger = logging.getLogger(__name__)


def generate_random_servicing_account(id_fields: Dict[str, Any], dg) -> Dict[str, Any]:
    """
    Generate a random mortgage_services servicing account record with reasonable values.

    Args:
        id_fields: Dictionary containing the required ID fields (mortgage_services_loan_id)
        dg: PostgreSQL connection object

    Returns:
        Dictionary containing randomly generated servicing account data (without ID fields)
    """
    # Get loan and closed loan information to make servicing account data reasonable
    conn = dg.conn
    loan_info = _get_loan_info(id_fields.get("mortgage_services_loan_id"), conn)
    closed_loan_info = _get_closed_loan_info(id_fields.get("mortgage_services_loan_id"), conn)
    monthly_payment: Optional[float] = None
    escrow_portion: Optional[float] = None

    # Get basic details from loan or closed loan info
    if closed_loan_info:
        original_principal_balance = closed_loan_info.get('final_loan_amount')
        first_payment_date = closed_loan_info.get('first_payment_date')
        maturity_date = closed_loan_info.get('maturity_date')
        current_interest_rate = closed_loan_info.get('final_interest_rate')
    elif loan_info:
        original_principal_balance = loan_info.get('loan_amount')
        first_payment_date = loan_info.get('first_payment_date')
        maturity_date = loan_info.get('maturity_date')
        current_interest_rate = loan_info.get('interest_rate')
    else:
        # Default values if no loan info available
        original_principal_balance = round(random.uniform(100000, 500000), 2)
        # First payment typically 1-2 months after today
        today = datetime.date.today()
        months_ahead = random.randint(1, 2)
        payment_month = today.month + months_ahead
        payment_year = today.year
        if payment_month > 12:
            payment_month -= 12
            payment_year += 1
        first_payment_date = datetime.date(payment_year, payment_month, 1)
        # Default to 30 year term
        maturity_year = payment_year + 30
        maturity_date = datetime.date(maturity_year, payment_month, 1)
        current_interest_rate = round(random.uniform(3.0, 7.0), 3)

    # Determine account age and current status
    today = datetime.date.today()

    # Map enum values to weights based on account characteristics
    # Weights correspond to: [ACTIVE, DELINQUENT, DEFAULT, FORECLOSURE, BANKRUPTCY, PAID_OFF, TRANSFERRED,
    #                         MODIFICATION_IN_PROCESS, LOSS_MITIGATION, FORBEARANCE, REO, SHORT_SALE,
    #                         CHARGE_OFF, SATISFIED, SUSPENDED]
    if first_payment_date > today:
        # Account isn't active yet (first payment in future)
        months_active = int(0)
        status_weights = [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # Only ACTIVE
    else:
        # Calculate months since first payment
        months_active = (today.year - first_payment_date.year) * 12 + (today.month - first_payment_date.month)

        # Adjust status probabilities based on account age
        if months_active < 3:
            # New accounts are usually current
            status_weights = [0.95, 0.03, 0.0, 0.0, 0.0, 0.01, 0.0, 0.0, 0.0, 0.01, 0.0, 0.0, 0.0, 0.0, 0.0]
        elif months_active < 12:
            # Accounts under a year
            status_weights = [0.85, 0.05, 0.02, 0.01, 0.01, 0.02, 0.01, 0.01, 0.01, 0.01, 0.0, 0.0, 0.0, 0.0, 0.0]
        elif months_active < 60:
            # Established accounts (1-5 years)
            status_weights = [0.80, 0.06, 0.03, 0.01, 0.02, 0.03, 0.01, 0.01, 0.01, 0.01, 0.005, 0.005, 0.0, 0.0, 0.005]
        else:
            # Older accounts (higher payoff probability)
            status_weights = [0.75, 0.05, 0.02, 0.01, 0.01, 0.10, 0.01, 0.01, 0.01, 0.01, 0.005, 0.005, 0.005, 0.01,
                              0.005]

    # Validate that weights match enum length
    if len(status_weights) != len(ServicingAccountStatus):
        raise ValueError(
            f"Status weights length ({len(status_weights)}) must match number of enum values ({len(ServicingAccountStatus)})")

    # Use the enum's get_random method to select a status based on weights
    status = ServicingAccountStatus.get_random(status_weights)

    # Calculate current principal balance based on original balance, term, and months active
    if original_principal_balance:
        if status == ServicingAccountStatus.PAID_OFF or status == ServicingAccountStatus.SATISFIED:
            current_principal_balance = 0.0
        else:
            # Simple amortization estimate
            term_months = int((maturity_date.year - first_payment_date.year) * 12 + (
                    maturity_date.month - first_payment_date.month))
            amortization_factor = max(0, int((term_months - months_active) / term_months))
            current_principal_balance = round(original_principal_balance * amortization_factor, 2)
    else:
        current_principal_balance = 0.0

    # Set up next payment information
    if status == ServicingAccountStatus.PAID_OFF or status == ServicingAccountStatus.SATISFIED:
        next_payment_date = None
        next_payment_amount = 0.0
    else:
        # Next payment is due on the 1st of next month
        next_month = today.month + 1
        next_year = today.year
        if next_month > 12:
            next_month = 1
            next_year += 1
        next_payment_date = datetime.date(next_year, next_month, 1)

        # Calculate payment amount based on remaining balance and term
        if loan_info and loan_info.get('monthly_payment'):
            next_payment_amount = loan_info.get('monthly_payment')
        else:
            remaining_months = (maturity_date.year - next_payment_date.year) * 12 + (
                    maturity_date.month - next_payment_date.month)
            if remaining_months <= 0:
                next_payment_amount = current_principal_balance  # Final payment
            else:
                next_payment_amount = _estimate_monthly_payment(current_principal_balance, current_interest_rate,
                                                                remaining_months)

    # Generate last payment info
    if months_active > 0:
        # Last payment was on the 1st of the current month or the previous month
        if today.day < 15:  # Early in month, payment likely made on 1st
            last_payment_date = datetime.date(today.year, today.month, 1)
        else:  # Later in month, payment was likely the previous month
            last_month = today.month - 1
            last_year = today.year
            if last_month < 1:
                last_month = 12
                last_year -= 1
            last_payment_date = datetime.date(last_year, last_month, 1)

        if status == ServicingAccountStatus.DELINQUENT or status == ServicingAccountStatus.DEFAULT:
            # Delinquent accounts might have missed last payment
            if random.random() < 0.7:  # 70% chance last payment was missed
                # Go back one more month for last payment
                last_month = last_payment_date.month - 1
                last_year = last_payment_date.year
                if last_month < 1:
                    last_month = 12
                    last_year -= 1
                last_payment_date = datetime.date(last_year, last_month, 1)

        # Last payment amount similar to next payment amount
        if next_payment_amount:
            variation = random.uniform(0.95, 1.05)
            last_payment_amount = round(next_payment_amount * variation, 2)
        else:
            # Reasonable payment based on loan size
            last_payment_amount = round(original_principal_balance * 0.006, 2)  # Rough approximation
    else:
        last_payment_date = None
        last_payment_amount = None

    # Generate escrow balance
    if status not in [ServicingAccountStatus.PAID_OFF, ServicingAccountStatus.SATISFIED]:
        # Escrow typically holds 2-6 months of taxes and insurance
        monthly_payment = next_payment_amount if next_payment_amount else (original_principal_balance * 0.006)
        escrow_portion = monthly_payment * 0.25  # Taxes and insurance ~25% of payment
        escrow_balance = round(escrow_portion * random.uniform(2, 6), 2)
    else:
        escrow_balance = 0.0

    # Generate year-to-date values
    current_month = today.month
    year_progress_factor = min(1.0, current_month / 12)  # How far through the year we are

    # For a newly created account, YTD values should reflect payments made so far
    payments_made_this_year = min(current_month, months_active)

    if status == ServicingAccountStatus.PAID_OFF or status == ServicingAccountStatus.SATISFIED:
        # If paid off, YTD values include final payment
        interest_paid_ytd = round(original_principal_balance * current_interest_rate / 100 * 0.2, 2)  # Estimate
        principal_paid_ytd = original_principal_balance
        escrow_paid_ytd = round(escrow_balance * 2, 2)  # Assume escrow was emptied
    else:
        # Regular account
        yearly_interest = original_principal_balance * current_interest_rate / 100
        interest_paid_ytd = round(yearly_interest * year_progress_factor * 0.7, 2)  # 70% of expected yearly interest

        yearly_principal = (
                               monthly_payment if 'monthly_payment' in locals() else next_payment_amount) * 12 - yearly_interest
        principal_paid_ytd = round(yearly_principal * year_progress_factor, 2)

        # Escrow payments (taxes, insurance)
        escrow_paid_ytd = round(escrow_portion * payments_made_this_year, 2)

    # Generate property tax and insurance due dates
    if status not in [ServicingAccountStatus.PAID_OFF, ServicingAccountStatus.SATISFIED]:
        # Property taxes typically due once or twice a year
        months_ahead = random.randint(1, 6)
        tax_month = (today.month + months_ahead) % 12
        if tax_month == 0:
            tax_month = 12
        tax_year = today.year + ((today.month + months_ahead) // 12)
        property_tax_due_date = datetime.date(tax_year, tax_month, 1)

        # Insurance typically due once a year
        months_ahead_insurance = random.randint(1, 10)
        insurance_month = (today.month + months_ahead_insurance) % 12
        if insurance_month == 0:
            insurance_month = 12
        insurance_year = today.year + ((today.month + months_ahead_insurance) // 12)
        homeowners_insurance_due_date = datetime.date(insurance_year, insurance_month, 15)
    else:
        property_tax_due_date = None
        homeowners_insurance_due_date = None

    # Generate past due information
    if status in [ServicingAccountStatus.DELINQUENT, ServicingAccountStatus.DEFAULT,
                  ServicingAccountStatus.FORECLOSURE]:
        # 30/60/90 day delinquency
        delinquency_level = random.choices([30, 60, 90], weights=[0.6, 0.3, 0.1], k=1)[0]
        days_past_due = delinquency_level + random.randint(1, 15)
        past_due_amount = round(next_payment_amount * (days_past_due // 30), 2)
    else:
        days_past_due = 0
        past_due_amount = 0.0

    # Generate late payment counts
    if status in [ServicingAccountStatus.DELINQUENT, ServicingAccountStatus.DEFAULT,
                  ServicingAccountStatus.FORECLOSURE] or random.random() < 0.2:
        late_count_30 = random.randint(1, 3)
        late_count_60 = random.randint(0, late_count_30)
        late_count_90 = random.randint(0, late_count_60)
    else:
        late_count_30 = 0
        late_count_60 = 0
        late_count_90 = 0

    # Generate servicing transfer date (if applicable)
    if status == ServicingAccountStatus.TRANSFERRED or random.random() < 0.3:
        # Transfer happened between origination and now
        if first_payment_date:
            earliest_date = first_payment_date - datetime.timedelta(days=30)  # 30 days before first payment
            latest_date = today - datetime.timedelta(days=60)  # At least 60 days ago

            if earliest_date < latest_date:
                days_range = (latest_date - earliest_date).days
                random_days = random.randint(0, max(0, days_range))
                servicing_transferred_date = earliest_date + datetime.timedelta(days=random_days)
            else:
                servicing_transferred_date = earliest_date
        else:
            # Default to 3-12 months ago
            months_ago = random.randint(3, 12)
            servicing_transferred_date = today - datetime.timedelta(days=30 * months_ago)
    else:
        servicing_transferred_date = None

    # Generate autopay status (more likely for current accounts)
    if status == ServicingAccountStatus.ACTIVE:
        auto_pay_enabled = random.random() < 0.7  # 70% of current accounts use autopay
    else:
        auto_pay_enabled = random.random() < 0.3  # 30% of non-current accounts use autopay

    # Create the servicing account record
    servicing_account = {
        "status": status.value,  # Convert enum to string value
        "current_principal_balance": current_principal_balance,
        "original_principal_balance": original_principal_balance,
        "current_interest_rate": current_interest_rate,
        "escrow_balance": escrow_balance,
        "next_payment_due_date": next_payment_date,
        "next_payment_amount": next_payment_amount,
        "last_payment_date": last_payment_date,
        "last_payment_amount": last_payment_amount,
        "interest_paid_ytd": interest_paid_ytd,
        "principal_paid_ytd": principal_paid_ytd,
        "escrow_paid_ytd": escrow_paid_ytd,
        "property_tax_due_date": property_tax_due_date,
        "homeowners_insurance_due_date": homeowners_insurance_due_date,
        "past_due_amount": past_due_amount,
        "days_past_due": days_past_due,
        "late_count_30": late_count_30,
        "late_count_60": late_count_60,
        "late_count_90": late_count_90,
        "auto_pay_enabled": auto_pay_enabled,
        "servicing_transferred_date": servicing_transferred_date
    }

    return servicing_account


def _get_loan_info(loan_id: Optional[int], conn) -> Optional[Dict[str, Any]]:
    """
    Get loan information to make servicing account data reasonable.

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
            SELECT loan_amount, interest_rate, monthly_payment, first_payment_date, maturity_date
            FROM mortgage_services.loans 
            WHERE mortgage_services_loan_id = %s
        """, (loan_id,))

        result = cursor.fetchone()
        cursor.close()

        return result

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching loan information: {error}")
        return None


def _get_closed_loan_info(loan_id: Optional[int], conn) -> Optional[Dict[str, Any]]:
    """
    Get closed loan information to make servicing account data reasonable.

    Args:
        loan_id: The ID of the loan
        conn: PostgreSQL connection object

    Returns:
        Dictionary containing closed loan information or None if loan_id is None or closed loan not found
    """
    if not loan_id:
        return None

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT final_loan_amount, final_interest_rate, final_monthly_payment, 
                   first_payment_date, maturity_date
            FROM mortgage_services.closed_loans 
            WHERE mortgage_services_loan_id = %s
        """, (loan_id,))

        result = cursor.fetchone()
        cursor.close()

        return result

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching closed loan information: {error}")
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
