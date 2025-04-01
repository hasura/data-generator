from .enums import AppointmentStatus, ClosingType
from typing import Any, Dict, Optional

import datetime
import logging
import psycopg2
import random

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
    loan_info = _get_loan_info(id_fields.get("mortgage_services_loan_id"), conn)

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

    # Determine loan state
    today = datetime.date.today()
    loan_is_closed = False
    # loan_is_funded = False

    if loan_info:
        # Check if loan has a first payment date (implies funding)
        if 'first_payment_date' in loan_info and loan_info['first_payment_date']:
            # loan_is_funded = True
            loan_is_closed = True

        # Check if loan has maturity date (implies funding)
        elif 'maturity_date' in loan_info and loan_info['maturity_date']:
            # loan_is_funded = True
            loan_is_closed = True

        # Check if origination date exists and is in the past
        elif 'origination_date' in loan_info and loan_info['origination_date'] and loan_info[
            'origination_date'] < today:
            loan_is_closed = True
            # Assume funding happens within 3 business days of origination
            # funding_estimated_date = loan_info['origination_date'] + datetime.timedelta(days=3)
            # loan_is_funded = (funding_estimated_date <= today)

    # Determine scheduled date based on loan state
    if loan_is_closed and 'origination_date' in loan_info and loan_info['origination_date']:
        # For closed loans, scheduled date is typically on or just before origination date
        days_diff = random.randint(-1, 0)  # Same day or 1 day before origination
        scheduled_date = loan_info['origination_date'] + datetime.timedelta(days=days_diff)
    elif loan_info and 'origination_date' in loan_info and loan_info['origination_date'] and loan_info[
        'origination_date'] > today:
        # For loans with future origination date, use the origination date
        scheduled_date = loan_info['origination_date'] - datetime.timedelta(days=random.randint(0, 1))
    else:
        # For loans without origination date or with past origination date but not closed
        days_in_future = random.randint(7, 30)
        scheduled_date = today + datetime.timedelta(days=days_in_future)

    # Determine appointment status based on loan state and scheduled date

    if loan_is_closed:
        # Closed loans should have completed appointments
        status_weights = [0.0, 0.0, 0.0, 0.0, 0.95, 0.05, 0.0, 0.0]  # Favor COMPLETED
    elif scheduled_date < today:
        # Past appointments that didn't lead to closing
        status_weights = [0.0, 0.1, 0.0, 0.0, 0.2, 0.6, 0.1, 0.0]  # Mostly CANCELLED
    elif scheduled_date == today:
        # Today's appointments could be in various states
        status_weights = [0.2, 0.1, 0.3, 0.3, 0.0, 0.1, 0.0, 0.0]  # Various states
    else:
        # Future appointments are likely scheduled/confirmed
        status_weights = [0.6, 0.1, 0.3, 0.0, 0.0, 0.0, 0.0, 0.0]  # Mostly SCHEDULED

    appointment_status = AppointmentStatus.get_random(weights=status_weights)

    # Select a closing type
    # In-person closings are most common, followed by hybrid and remote
    closing_type_weights = [0.6, 0.15, 0.1, 0.05, 0.05, 0.02, 0.02, 0.01]
    closing_type = ClosingType.get_random(weights=closing_type_weights)

    # Generate actual closing date based on status
    actual_closing_date = None
    if appointment_status == AppointmentStatus.COMPLETED:
        if loan_is_closed:
            # If loan is closed, actual closing date should be near origination date
            if 'origination_date' in loan_info and loan_info['origination_date']:
                # Usually same as scheduled date, occasionally 1 day off
                day_adjustment = random.choices([0, 1, -1], weights=[0.8, 0.1, 0.1], k=1)[0]
                actual_closing_date = scheduled_date + datetime.timedelta(days=day_adjustment)
        else:
            # Can't have actual closing date if loan isn't closed
            appointment_status = AppointmentStatus.SCHEDULED if scheduled_date >= today else AppointmentStatus.CANCELLED
            actual_closing_date = None

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
    if appointment_status == AppointmentStatus.RESCHEDULED:
        reschedule_reasons = [
            "Loan documents not ready",
            "Borrower schedule conflict",
            "Missing documentation",
            "Underwriting delay",
            "Seller requested delay",
            "Title issues need resolution"
        ]
        notes = random.choice(reschedule_reasons)
    elif appointment_status == AppointmentStatus.CANCELLED:
        cancel_reasons = [
            "Loan application withdrawn",
            "Buyer financing fell through",
            "Property inspection issues",
            "Appraisal came in low",
            "Title defects discovered",
            "Buyer/Seller dispute"
        ]
        notes = random.choice(cancel_reasons)
    elif closing_type != ClosingType.IN_PERSON:
        # Add notes about special closing arrangements
        closing_notes = {
            ClosingType.HYBRID: [
                "Seller attending remotely via video conference",
                "Borrower in person, co-borrower joining via video",
                "Agent attending remotely, all others in person"
            ],
            ClosingType.REMOTE: [
                "Remote online notarization (RON) closing",
                "All parties participating via secure video conference",
                "Electronic signature for all documents"
            ],
            ClosingType.MAIL_AWAY: [
                "Documents mailed to borrower on out-of-state assignment",
                "International borrower completing via mail",
                "Borrower unable to attend in person due to medical reasons"
            ],
            ClosingType.POWER_OF_ATTORNEY: [
                "Borrower's spouse signing via power of attorney",
                "Military deployment - brother acting as attorney-in-fact",
                "Co-borrower represented by designated power of attorney"
            ],
            ClosingType.DRY_CLOSING: [
                "Signing today, funding expected in 48 hours",
                "Three-day waiting period required",
                "Funds to be wired after lender reviews signed documents"
            ],
            ClosingType.WET_CLOSING: [
                "Same-day funding arranged",
                "All parties confirmed for on-site funding",
                "Wire transfer scheduled for immediate release after signing"
            ],
            ClosingType.ESCROW: [
                "Signing and closing through escrow service",
                "Progressive closing with multiple escrow disbursements",
                "Extended escrow arrangement for construction loan"
            ]
        }

        if closing_type in closing_notes:
            notes = random.choice(closing_notes[closing_type])

    # Create the closing appointment record
    closing_appointment = {
        "scheduled_date": scheduled_date,
        "status": appointment_status.value,
        "closing_type": closing_type.value,
        "closing_agent": closing_agent,
        "closing_company": closing_company,
        "closing_fee": round(closing_fee, 2),
        "actual_closing_date": actual_closing_date,
        "notes": notes
    }

    return closing_appointment


def _get_loan_info(loan_id: Optional[int], conn) -> Optional[Dict[str, Any]]:
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

        # Get loan information that would indicate funding or closing
        cursor.execute("""
            SELECT 
                loan_amount, 
                origination_date,
                first_payment_date,
                maturity_date
            FROM mortgage_services.loans 
            WHERE mortgage_services_loan_id = %s
        """, (loan_id,))

        result = cursor.fetchone()
        cursor.close()

        return result

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching loan information: {error}")
        return None
