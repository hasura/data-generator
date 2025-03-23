import datetime
import logging
import random
from typing import Any, Dict, Optional

import psycopg2

logger = logging.getLogger(__name__)


def generate_random_closing_appointment(id_fields: Dict[str, Any], dg) -> Dict[str, Any]:
    """
    Generate a random mortgage services closing appointment record with reasonable values.

    Args:
        id_fields: Dictionary containing the required ID fields (mortgage_services_loan_id)
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated closing appointment data (without ID fields)
    """
    # Get loan information to make closing appointment data reasonable
    conn = dg.conn
    loan_info = get_loan_info(id_fields.get("mortgage_services_loan_id"), conn)

    # Define possible values for categorical fields
    status_options = [
        "scheduled",
        "completed",
        "rescheduled",
        "cancelled"
    ]

    closing_agents = [
        "John Smith", "Maria Garcia", "David Johnson", "Sarah Lee",
        "Michael Brown", "Jennifer Wilson", "Robert Davis", "Lisa Miller",
        "William Rodriguez", "Elizabeth Martinez", "James Taylor", "Patricia Thomas"
    ]

    closing_companies = [
        "First American Title", "Fidelity National Title", "Old Republic Title",
        "Stewart Title", "Chicago Title", "Investors Title", "Title Resources",
        "North American Title", "Commonwealth Land Title", "WFG National Title"
    ]

    # Determine scheduled date based on loan origination date
    today = datetime.date.today()

    if loan_info and 'origination_date' in loan_info and loan_info['origination_date']:
        # For loans that have originated, set scheduled date at or before origination
        days_diff = random.randint(-1, 0)  # Typically same day or 1 day before origination
        scheduled_date = loan_info['origination_date'] + datetime.timedelta(days=days_diff)
    else:
        # For loans without origination date, use a date in the near future
        days_in_future = random.randint(7, 30)
        scheduled_date = today + datetime.timedelta(days=days_in_future)

    # Get random branch address ID for the closing location
    location_address_id = get_random_branch_address_id(conn)

    # Determine status based on scheduled date
    if scheduled_date < today:
        # Past appointments are likely completed
        status_weights = [0.0, 0.9, 0.05, 0.05]  # weights for each status
    elif scheduled_date == today:
        # Today's appointments could be any status
        status_weights = [0.5, 0.3, 0.1, 0.1]
    else:
        # Future appointments are likely still scheduled
        status_weights = [0.85, 0.0, 0.1, 0.05]

    status = random.choices(status_options, weights=status_weights, k=1)[0]

    # Generate actual closing date based on status
    actual_closing_date = None
    if status == "completed":
        # Usually same as scheduled date, occasionally 1 day off
        day_adjustment = random.choices([0, 1, -1], weights=[0.8, 0.1, 0.1], k=1)[0]
        actual_closing_date = scheduled_date + datetime.timedelta(days=day_adjustment)

    # Generate closing agent and company
    closing_agent = random.choice(closing_agents)
    closing_company = random.choice(closing_companies)

    # Generate closing fee
    # Typically between 0.5% and 1% of loan amount, with minimum fees
    if loan_info and 'loan_amount' in loan_info and loan_info['loan_amount']:
        loan_amount = loan_info['loan_amount']
        fee_percentage = random.uniform(0.005, 0.01)
        base_fee = loan_amount * fee_percentage
        # Ensure minimum fee of $500
        closing_fee = max(500, min(5000, base_fee))  # Cap at $5000
    else:
        # Default range if loan amount unknown
        closing_fee = random.uniform(800, 2500)

    # Round fee to nearest dollar
    closing_fee = round(closing_fee, 2)

    # Generate notes based on status
    notes = None
    if status == "rescheduled":
        reschedule_reasons = [
            "Loan documents not ready",
            "Borrower schedule conflict",
            "Missing documentation",
            "Underwriting delay",
            "Seller requested delay",
            "Title issues need resolution"
        ]
        notes = random.choice(reschedule_reasons)
    elif status == "cancelled":
        cancel_reasons = [
            "Loan application withdrawn",
            "Buyer financing fell through",
            "Property inspection issues",
            "Appraisal came in low",
            "Title defects discovered",
            "Buyer/Seller dispute"
        ]
        notes = random.choice(cancel_reasons)

    # Create the closing appointment record
    closing_appointment = {
        "scheduled_date": scheduled_date,
        "location_address_id": location_address_id,
        "status": status,
        "closing_agent": closing_agent,
        "closing_company": closing_company,
        "closing_fee": float(closing_fee),
        "actual_closing_date": actual_closing_date,
        "notes": notes
    }

    return closing_appointment


def get_loan_info(loan_id: Optional[int], conn) -> Optional[Dict[str, Any]]:
    """
    Get loan information to make closing appointment data reasonable.

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
            SELECT loan_amount, origination_date
            FROM mortgage_services.loans 
            WHERE mortgage_services_loan_id = %s
        """, (loan_id,))

        result = cursor.fetchone()
        cursor.close()

        if result:
            return {
                "loan_amount": float(result[0]) if result[0] is not None else None,
                "origination_date": result[1]
            }
        else:
            return None

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching loan information: {error}")
        return None


def get_random_branch_address_id(conn) -> Optional[int]:
    """
    Get a random branch address ID from the database for closing appointments.

    Args:
        conn: PostgreSQL connection object

    Returns:
        Random branch address ID or None if query fails
    """
    try:
        cursor = conn.cursor()

        # Query to get addresses for BRANCH buildings
        cursor.execute("""
            SELECT a.enterprise_address_id 
            FROM enterprise.addresses a
            JOIN enterprise.buildings b ON a.enterprise_address_id = b.enterprise_address_id
            WHERE b.building_type = 'BRANCH'
            ORDER BY RANDOM()
            LIMIT 1
        """)

        result = cursor.fetchone()

        if not result:
            # If no branch addresses found, fall back to any address
            cursor.execute("""
                SELECT enterprise_address_id 
                FROM enterprise.addresses
                ORDER BY RANDOM()
                LIMIT 1
            """)
            result = cursor.fetchone()

        cursor.close()

        if result:
            return result[0]
        else:
            # If no addresses found, return None
            return None

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching random branch address ID: {error}")
        return None
