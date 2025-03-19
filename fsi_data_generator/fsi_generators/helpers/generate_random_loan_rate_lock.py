import random
import datetime
from typing import Dict, Any, Optional
import psycopg2


def generate_random_loan_rate_lock(id_fields: Dict[str, Any], dg) -> Dict[str, Any]:
    """
    Generate a random mortgage services loan rate lock record with reasonable values.

    Args:
        id_fields: Dictionary containing the required ID fields (like mortgage_services_loan_id)
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated loan rate lock data (without ID fields)
    """
    # Get loan information to make rate lock data reasonable
    conn = dg.conn
    loan_info = get_loan_info(id_fields["mortgage_services_loan_id"], conn)

    # Generate lock date (typically within the last 90 days)
    today = datetime.datetime.now()
    days_ago = random.randint(5, 90)
    lock_date = today - datetime.timedelta(days=days_ago)

    # Generate lock period days (typical options are 15, 30, 45, 60, or 90 days)
    lock_period_options = [15, 30, 45, 60, 90]
    lock_period_days = random.choice(lock_period_options)

    # Calculate expiration date based on lock date and lock period
    expiration_date = lock_date + datetime.timedelta(days=lock_period_days)

    # Generate locked interest rate
    # If we got loan info, base it on that loan's interest rate with a small variation
    if loan_info and 'interest_rate' in loan_info and loan_info['interest_rate']:
        base_rate = loan_info['interest_rate']
        # Rate locks are usually at or slightly below the final rate
        locked_interest_rate = round(base_rate - random.uniform(0, 0.375), 3)
    else:
        # Otherwise use a reasonable range for mortgage rates
        locked_interest_rate = round(random.uniform(3.0, 7.0), 3)

    # Generate lock fee (typically 0.25% to 0.5% of loan amount)
    if loan_info and 'loan_amount' in loan_info and loan_info['loan_amount']:
        loan_amount = loan_info['loan_amount']
        lock_fee_percentage = random.uniform(0.0025, 0.005)  # 0.25% to 0.5%
        lock_fee = round(loan_amount * lock_fee_percentage, 2)
    else:
        # Default reasonable lock fee
        lock_fee = round(random.uniform(500, 2500), 2)

    # Determine if the lock was extended
    was_extended = random.random() < 0.2  # 20% chance of being extended

    extension_date = None
    extension_fee = None

    if was_extended:
        # Extension typically happens near expiration date
        days_before_expiration = random.randint(1, 5)
        extension_date = expiration_date - datetime.timedelta(days=days_before_expiration)

        # Extension extends the expiration by 7, 15, or 30 days typically
        extension_days = random.choice([7, 15, 30])
        expiration_date = expiration_date + datetime.timedelta(days=extension_days)

        # Extension fee is typically 0.125% to 0.25% of loan amount per week
        if loan_info and 'loan_amount' in loan_info and loan_info['loan_amount']:
            extension_fee_percentage = random.uniform(0.00125, 0.0025) * (extension_days / 7)
            extension_fee = round(loan_info['loan_amount'] * extension_fee_percentage, 2)
        else:
            extension_fee = round(random.uniform(250, 1000), 2)

    # Generate status
    if expiration_date < today:
        status_options = ["Expired", "Closed"]
        status = random.choice(status_options)
    else:
        status_options = ["Active", "Locked"]
        status = random.choice(status_options)

    # Create the rate lock record
    rate_lock = {
        "lock_date": lock_date,
        "expiration_date": expiration_date,
        "locked_interest_rate": locked_interest_rate,
        "lock_period_days": lock_period_days,
        "status": status,
        "lock_fee": lock_fee,
        "extension_date": extension_date,
        "extension_fee": extension_fee
    }

    return rate_lock


def get_loan_info(loan_id: int, conn) -> Optional[Dict[str, Any]]:
    """
    Get loan information to make rate lock data reasonable.

    Args:
        loan_id: The ID of the loan
        conn: PostgreSQL connection object

    Returns:
        Dictionary containing loan information
    """
    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT interest_rate, loan_amount 
            FROM mortgage_services.loans 
            WHERE mortgage_services_loan_id = %s
        """, (loan_id,))

        result = cursor.fetchone()
        cursor.close()

        if result:
            return {
                "interest_rate": float(result[0]),
                "loan_amount": float(result[1])
            }
        else:
            return None

    except (Exception, psycopg2.Error) as error:
        print(f"Error fetching loan information: {error}")
        return None
