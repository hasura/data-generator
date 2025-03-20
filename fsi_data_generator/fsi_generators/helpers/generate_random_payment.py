import random
import datetime
from decimal import Decimal
from typing import Dict, Any, Optional
import psycopg2

def get_loan_origination_date(servicing_account_id: int, conn) -> Optional[datetime.date]:
    """
    Get the loan origination date to determine expected payment history length.

    Args:
        servicing_account_id: The ID of the servicing account
        conn: PostgreSQL connection object

    Returns:
        Loan origination date or None if not found
    """
    try:
        cursor = conn.cursor()

        # First try to get origination date from the servicing account
        cursor.execute("""
            SELECT mortgage_services_loan_id
            FROM mortgage_services.servicing_accounts 
            WHERE mortgage_services_servicing_account_id = %s
        """, (servicing_account_id,))

        result = cursor.fetchone()

        if result and result[0]:
            loan_id = result[0]

            # Now get the origination date from the loan
            cursor.execute("""
                SELECT origination_date
                FROM mortgage_services.loans 
                WHERE mortgage_services_loan_id = %s
            """, (loan_id,))

            result = cursor.fetchone()
            cursor.close()

            if result and result[0]:
                return result[0]

        cursor.close()
        return None

    except (Exception, psycopg2.Error) as error:
        print(f"Error fetching loan origination date: {error}")
        return None

def generate_random_payment(id_fields: Dict[str, Any], dg) -> Dict[str, Any]:
    """
    Generate a random mortgage services payment record with reasonable values.

    Args:
        id_fields: Dictionary containing the required ID fields (mortgage_services_servicing_account_id)
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated payment data (without ID fields)

    Raises:
        SkipRowGenerationError: If payment history is already complete (reached loan origination date)
    """
    # Get loan servicing account information to make payment data reasonable
    conn = dg.conn
    servicing_account_info = get_servicing_account_info(id_fields["mortgage_services_servicing_account_id"], conn)

    if not servicing_account_info:
        # Use default values if no servicing account info is found
        servicing_account_info = {
            "payment_amount": 1500.00,
            "next_payment_due_date": datetime.date.today(),
            "interest_rate": 4.5,
            "monthly_escrow_amount": 250.00
        }

    # Get previous payments to ensure consistency
    previous_payments = get_previous_payments(id_fields["mortgage_services_servicing_account_id"], conn)

    # Get loan origination date to avoid generating payments before the loan existed
    loan_origination_date = get_loan_origination_date(id_fields["mortgage_services_servicing_account_id"], conn)

    # Define possible values for categorical fields
    payment_types = ["regular", "extra principal", "late", "escrow only"]
    payment_methods = ["ach", "check", "online", "mobile", "wire", "branch", "phone"]
    payment_statuses = ["pending", "completed", "returned", "canceled"]

    # Generate payment date based on servicing account info and previous payments
    today = datetime.date.today()

    # Use next_payment_due_date from servicing account if available
    next_payment_due_date = servicing_account_info.get("next_payment_due_date")
    last_payment_date = servicing_account_info.get("last_payment_date")

    # Ensure dates are in proper date format (not datetime)
    next_payment_due_date = next_payment_due_date.date() if hasattr(next_payment_due_date, 'date') else next_payment_due_date
    last_payment_date = last_payment_date.date() if hasattr(last_payment_date, 'date') else last_payment_date

    # Determine payment date based on existing payments and payment schedule
    if previous_payments:
        # If there are already payments in the system, place this payment before the earliest recorded payment
        earliest_payment_date = previous_payments[-1]["payment_date"] if len(previous_payments) > 1 else previous_payments[0]["payment_date"]

        # Ensure earliest_payment_date is in date format
        earliest_payment_date = earliest_payment_date.date() if hasattr(earliest_payment_date, 'date') else earliest_payment_date

        # Make this payment 28-31 days before the earliest payment (typical monthly cycle)
        days_before_earliest = random.randint(28, 31)
        payment_date = earliest_payment_date - datetime.timedelta(days=days_before_earliest)
    elif last_payment_date:
        # If no payments in payments table but servicing account shows last payment,
        # make this payment the one before that
        days_before_last = random.randint(28, 31)
        payment_date = last_payment_date - datetime.timedelta(days=days_before_last)
    elif next_payment_due_date:
        # If no existing payments, but we have a next payment due date,
        # set this payment as the previous cycle (due date minus one month)
        payment_date = next_payment_due_date - datetime.timedelta(days=random.randint(28, 31))
    else:
        # No reference dates available, use a date within the last 90 days
        days_ago = random.randint(30, 90)
        payment_date = today - datetime.timedelta(days=days_ago)

    # Ensure payment date isn't in the future
    # Convert payment_date to date type if it's datetime
    payment_date_obj = payment_date.date() if hasattr(payment_date, 'date') else payment_date
    if payment_date_obj > today:
        payment_date = today - datetime.timedelta(days=random.randint(1, 5))

    # Check if payment date is before loan origination date
    # Ensure both dates are the same type for comparison
    payment_date_obj = payment_date.date() if hasattr(payment_date, 'date') else payment_date
    loan_origination_date_obj = loan_origination_date.date() if hasattr(loan_origination_date, 'date') else loan_origination_date

    if loan_origination_date_obj and payment_date_obj < loan_origination_date_obj:
        # We've reached back to the beginning of the loan - payment history is complete
        # Signal to skip this row generation
        from data_generator import SkipRowGenerationError
        raise SkipRowGenerationError("Payment history is complete - already reached loan origination date")

    # Determine payment type
    # For the earliest payment in a sequence, regular payments are most common
    if not previous_payments:
        payment_type_weights = [0.9, 0.05, 0.03, 0.02]  # Regular payments most common for the first payment
    else:
        payment_type_weights = [0.85, 0.10, 0.03, 0.02]  # More variety in subsequent payments

    payment_type = random.choices(payment_types, weights=payment_type_weights, k=1)[0]

    # Generate payment method
    payment_method = random.choice(payment_methods)

    # Determine payment status
    # Most payments should be completed, especially if they're not recent
    payment_date_obj = payment_date.date() if hasattr(payment_date, 'date') else payment_date
    days_from_today = (today - payment_date_obj).days
    if days_from_today > 5:
        status_weights = [0.01, 0.97, 0.01, 0.01]  # Older payments almost always completed
    elif days_from_today > 3:
        status_weights = [0.05, 0.92, 0.02, 0.01]  # Most older payments are completed
    else:
        status_weights = [0.20, 0.75, 0.03, 0.02]  # More recent payments might be pending

    payment_status = random.choices(payment_statuses, weights=status_weights, k=1)[0]

    # Generate payment amounts
    # Get payment_amount as float from servicing_account_info
    regular_payment_amount = servicing_account_info.get("payment_amount", 1500.00)

    # Adjust payment amount based on payment type
    payment_amount = 0.0
    principal_amount = 0.0
    interest_amount = 0.0
    if payment_type == "regular":
        payment_amount = regular_payment_amount
    elif payment_type == "extra principal":
        # Extra principal payment is regular payment plus additional principal
        extra_amount = round(regular_payment_amount * random.uniform(0.1, 0.5), 2)
        payment_amount = regular_payment_amount + extra_amount
    elif payment_type == "late":
        payment_amount = regular_payment_amount
    elif payment_type == "escrow only":
        # Escrow only payment is typically smaller than regular payment
        payment_amount = round(regular_payment_amount * random.uniform(0.2, 0.4), 2)

    # Calculate principal and interest split
    # Get the split ratio from servicing account or use a reasonable default
    if "current_principal_balance" in servicing_account_info and servicing_account_info["current_principal_balance"]:
        loan_balance = servicing_account_info["current_principal_balance"]
        interest_rate = servicing_account_info["interest_rate"]

        # Calculate monthly interest
        monthly_interest_rate = interest_rate / 1200.0  # Annual rate to monthly percentage
        interest_amount = round(loan_balance * monthly_interest_rate, 2)

        # For regular payments, principal is payment minus interest
        if payment_type in ["regular", "late"]:
            principal_amount = min(payment_amount - interest_amount, payment_amount)
            # Ensure principal amount is not negative
            principal_amount = max(principal_amount, 0.0)
            interest_amount = payment_amount - principal_amount
        elif payment_type == "extra principal":
            # Calculate regular principal (payment minus interest)
            regular_principal = regular_payment_amount - interest_amount
            # Extra payment goes entirely to principal
            principal_amount = regular_principal + (payment_amount - regular_payment_amount)
            interest_amount = payment_amount - principal_amount
        elif payment_type == "escrow only":
            # Escrow payments don't apply to principal or interest
            principal_amount = 0.0
            interest_amount = 0.0
    else:
        # Default split if loan balance is unknown
        if payment_type in ["regular", "late"]:
            # Typical mortgage has more interest at first, more principal later
            principal_ratio = random.uniform(0.3, 0.7)
            principal_amount = round(payment_amount * principal_ratio, 2)
            interest_amount = payment_amount - principal_amount
        elif payment_type == "extra principal":
            # Regular portion split between principal and interest,
            # extra portion goes entirely to principal
            regular_principal_ratio = random.uniform(0.3, 0.7)
            regular_principal = round(regular_payment_amount * regular_principal_ratio, 2)
            regular_interest = regular_payment_amount - regular_principal
            extra_principal = payment_amount - regular_payment_amount

            principal_amount = regular_principal + extra_principal
            interest_amount = regular_interest
        elif payment_type == "escrow only":
            principal_amount = 0.0
            interest_amount = 0.0

    # Determine escrow amount based on servicing account info
    escrow_amount = 0.0
    if payment_type == "escrow only":
        # For Escrow Only payments, the entire amount goes to escrow
        escrow_amount = payment_amount
    else:
        # For other payment types, use the monthly escrow amount from the servicing account
        if "monthly_escrow_amount" in servicing_account_info and servicing_account_info[
            "monthly_escrow_amount"] is not None:
            escrow_amount = servicing_account_info["monthly_escrow_amount"]
        elif "escrow_balance" in servicing_account_info and servicing_account_info["escrow_balance"] is not None:
            # If no monthly escrow amount, but we have an escrow balance, estimate a reasonable monthly amount
            estimated_annual_escrow = 2400.00  # Reasonable estimate for taxes and insurance
            escrow_amount = round(estimated_annual_escrow / 12.0, 2)
        else:
            # Default escrow portion if no amount available (roughly 20-30% of payment)
            escrow_amount = round(regular_payment_amount * random.uniform(0.2, 0.3), 2)

    # Generate fee amounts
    late_fee_amount = 0.0
    if payment_type == "late":
        # Typical late fee is either a percentage or a flat amount
        if random.random() < 0.5:
            # Percentage-based late fee (typically 4-5% of payment)
            late_fee_amount = round(regular_payment_amount * random.uniform(0.04, 0.05), 2)
        else:
            # Flat late fee (typically $15-$50)
            late_fee_amount = float(random.randint(15, 50))

    other_fee_amount = 0.0
    # Small chance of other fees
    if random.random() < 0.05:
        other_fee_amount = float(random.randint(5, 25))

    # Generate transaction ID and confirmation number
    transaction_id = f"TX{random.randint(10000000, 99999999)}"
    confirmation_number = f"CONF{random.randint(1000000, 9999999)}"

    # For returned payments, generate a reason
    returned_reason = None
    returned_date = None
    if payment_status == "returned":
        return_reasons = [
            "insufficient funds", "account closed", "payment stopped",
            "invalid account number", "technical error"
        ]
        returned_reason = random.choice(return_reasons)
        # Return typically happens 1-3 days after payment
        days_after_payment = random.randint(1, 3)
        returned_date = payment_date + datetime.timedelta(days=days_after_payment)

    # Create the payment record
    payment = {
        "payment_date": payment_date,
        "payment_type": payment_type,
        "payment_method": payment_method,
        "payment_amount": payment_amount,
        "principal_amount": principal_amount,
        "interest_amount": interest_amount,
        "escrow_amount": escrow_amount if escrow_amount else None,
        "late_fee_amount": late_fee_amount if late_fee_amount else 0.0,
        "other_fee_amount": other_fee_amount if other_fee_amount else 0.0,
        "transaction_id": transaction_id,
        "confirmation_number": confirmation_number,
        "status": payment_status,
        "returned_reason": returned_reason,
        "returned_date": returned_date
    }

    return payment


def get_servicing_account_info(servicing_account_id: int, conn) -> Optional[Dict[str, Any]]:
    """
    Get loan servicing account information to make payment data reasonable.

    Args:
        servicing_account_id: The ID of the servicing account
        conn: PostgreSQL connection object

    Returns:
        Dictionary containing servicing account information or None if not found
    """
    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                CAST(current_principal_balance AS FLOAT), 
                CAST(original_principal_balance AS FLOAT),
                CAST(current_interest_rate AS FLOAT),
                CAST(next_payment_amount AS FLOAT),
                next_payment_due_date,
                last_payment_date,
                CAST(last_payment_amount AS FLOAT),
                CAST(escrow_balance AS FLOAT)
            FROM mortgage_services.servicing_accounts 
            WHERE mortgage_services_servicing_account_id = %s
        """, (servicing_account_id,))

        result = cursor.fetchone()
        cursor.close()

        if result:
            # Calculate monthly escrow amount based on the difference between total payment and principal+interest
            monthly_escrow_amount = None
            payment_amount = result[3]  # next_payment_amount

            # If we have a principal balance and interest rate, we can calculate the P&I portion
            if result[0] is not None and result[2] is not None:  # current_principal_balance and current_interest_rate
                principal_balance = float(result[0])
                interest_rate = float(result[2])

                # Calculate monthly principal and interest payment (P&I)
                # This is an approximation based on remaining balance and rate
                monthly_interest_rate = interest_rate / 1200.0  # Annual rate to monthly percentage
                monthly_interest = principal_balance * monthly_interest_rate

                # The monthly escrow would be the difference between total payment and estimated P&I
                # Estimate P&I by calculating interest and assuming the rest is principal
                payment_amount_float = float(payment_amount) if payment_amount is not None else 0.0
                estimated_pi_payment = monthly_interest + (payment_amount_float * 0.7)  # Assume ~70% of payment is P&I
                monthly_escrow_amount = payment_amount_float - estimated_pi_payment

                # Sanity check - escrow is typically 15-35% of payment
                if payment_amount_float > 0:  # Avoid division by zero
                    if monthly_escrow_amount < payment_amount_float * 0.15 or monthly_escrow_amount > payment_amount_float * 0.35:
                    # Default to a reasonable amount if calculation seems off
                        monthly_escrow_amount = payment_amount_float * 0.25

            # If we couldn't calculate it, set a reasonable default
            if monthly_escrow_amount is None and payment_amount is not None:
                monthly_escrow_amount = float(payment_amount) * 0.25  # Typical escrow is about 25% of payment
            elif monthly_escrow_amount is None:
                monthly_escrow_amount = 250.00  # Default value if no payment amount

            return {
                "current_principal_balance": result[0],
                "original_principal_balance": result[1],
                "interest_rate": result[2],
                "payment_amount": result[3],  # Using next_payment_amount as payment_amount
                "next_payment_due_date": result[4],
                "last_payment_date": result[5],
                "last_payment_amount": result[6],
                "escrow_balance": result[7],
                "monthly_escrow_amount": monthly_escrow_amount
            }
        else:
            return None

    except (Exception, psycopg2.Error) as error:
        print(f"Error fetching servicing account information: {error}")
        return None


def get_previous_payments(servicing_account_id: int, conn) -> list:
    """
    Get previous payments for consistency checking.

    Args:
        servicing_account_id: The ID of the servicing account
        conn: PostgreSQL connection object

    Returns:
        List of previous payments sorted by payment date (desc)
    """
    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                payment_date,
                payment_type,
                CAST(payment_amount AS FLOAT),
                CAST(principal_amount AS FLOAT),
                CAST(interest_amount AS FLOAT),
                CAST(escrow_amount AS FLOAT)
            FROM mortgage_services.payments 
            WHERE mortgage_services_servicing_account_id = %s
            ORDER BY payment_date DESC
        """, (servicing_account_id,))

        results = cursor.fetchall()
        cursor.close()

        payments = []
        for row in results:
            payments.append({
                "payment_date": row[0],
                "payment_type": row[1],
                "payment_amount": row[2],
                "principal_amount": row[3],
                "interest_amount": row[4],
                "escrow_amount": row[5]
            })

        return payments

    except (Exception, psycopg2.Error) as error:
        print(f"Error fetching previous payments: {error}")
        return []
