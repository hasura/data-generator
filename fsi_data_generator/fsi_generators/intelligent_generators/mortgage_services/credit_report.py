from .enums import CreditBureau, CreditReportType, VerificationStatus
from typing import Any, Dict, Optional

import datetime
import logging
import psycopg2
import random
import sys

logger = logging.getLogger(__name__)


def generate_random_credit_report(id_fields: Dict[str, Any], dg) -> Dict[str, Any]:
    """
    Generate a random mortgage services credit report record with reasonable values.

    Args:
        id_fields: Dictionary containing the required ID fields (mortgage_services_application_id,
                   mortgage_services_borrower_id)
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated credit report data (without ID fields)
    """
    # Get borrower information to make credit report data reasonable
    conn = dg.conn
    borrower_info = get_borrower_info(id_fields.get("mortgage_services_borrower_id"), conn)

    # Generate report date (typically within the last 120 days)
    today = datetime.datetime.now(datetime.timezone.utc)
    days_ago = random.randint(7, 120)
    report_date = today - datetime.timedelta(days=days_ago)

    # Generate expiration date (typically 90-120 days after report date)
    expiration_days = random.randint(90, 120)
    expiration_date = (report_date + datetime.timedelta(days=expiration_days)).date()

    # Use the CreditReportType enum with weight distribution to favor certain report types
    report_type = CreditReportType.get_random()

    # Set bureau name based on report type
    if report_type == CreditReportType.TRI_MERGE:
        bureau_name = None  # No specific bureau for tri-merge reports
    elif report_type == CreditReportType.MERGED_BUREAU:
        # For merged bureau reports, we don't specify a single bureau
        bureau_name = None
    else:
        # For single bureau reports, pick one of the three major bureaus with weighted distribution
        bureau_weights = [0.4, 0.35, 0.25, 0, 0, 0]  # Weights for Equifax, Experian, TransUnion, etc.
        bureau_name = CreditBureau.get_random(weights=bureau_weights)

    # Generate a realistic credit score
    # If we got borrower info with an estimated credit score, base the score on that
    if borrower_info and 'estimated_credit_score' in borrower_info and borrower_info['estimated_credit_score']:
        base_score = borrower_info['estimated_credit_score']
        # Credit score typically varies slightly from estimate
        credit_score = max(300, min(850, base_score + random.randint(-20, 20)))
    else:
        # Otherwise generate a reasonable credit score
        credit_score_distribution = [
            (300, 579, 0.05),  # Poor: 5%
            (580, 669, 0.15),  # Fair: 15%
            (670, 739, 0.30),  # Good: 30%
            (740, 799, 0.40),  # Very Good: 40%
            (800, 850, 0.10)  # Exceptional: 10%
        ]

        # Pick a range based on the distribution
        range_selection = random.random()
        cumulative_prob = 0
        selected_range = None

        for score_min, score_max, probability in credit_score_distribution:
            cumulative_prob += probability
            if range_selection <= cumulative_prob:
                selected_range = (score_min, score_max)
                break

        # Generate a score within the selected range
        credit_score = random.randint(selected_range[0], selected_range[1])

    # Generate a report reference ID
    bureau_prefix = bureau_name.value[:3] if bureau_name else "TRI"
    report_reference = f"{bureau_prefix}-{random.randint(10000, 99999)}-{report_date.strftime('%y%m%d')}"

    # Determine status based on report date and expiration
    if report_date.date() > today.date() - datetime.timedelta(days=7):
        # Very recent reports might still be pending
        status_weights = [0.0, 0.8, 0.2, 0.0, 0.0, 0.0]  # favor PENDING for recent reports
    elif expiration_date < today.date():
        # Expired reports
        status_weights = [0.0, 0.0, 0.0, 0.0, 0.0, 1.0]  # always EXPIRED for reports past expiration date
    else:
        # Most reports should be completed
        status_weights = [0.85, 0.05, 0.05, 0.0, 0.05, 0.0]  # mostly VERIFIED, some PENDING, FAILED or WAIVED

    status = VerificationStatus.get_random(weights=status_weights)

    # Generate file path for completed reports
    report_path = None
    if status == VerificationStatus.VERIFIED:
        app_id = id_fields.get("mortgage_services_application_id")
        borrower_id = id_fields.get("mortgage_services_borrower_id")
        file_id = random.randint(10000, 99999)
        report_path = f"/documents/credit/{app_id}/borrower_{borrower_id}/report_{file_id}.pdf"

    # Credit score should be None for pending or failed reports
    if status in [VerificationStatus.PENDING, VerificationStatus.FAILED]:
        credit_score = None

    # Create the credit report record
    credit_report = {
        "report_date": report_date,
        "expiration_date": expiration_date,
        "credit_score": credit_score,
        "report_type": report_type.value,
        "report_reference": report_reference,
        "report_path": report_path,
        "status": status.value
    }

    return credit_report


def get_borrower_info(borrower_id: Optional[int], conn) -> Optional[Dict[str, Any]]:
    """
    Get borrower information to make credit report data reasonable.

    Args:
        borrower_id: The ID of the borrower
        conn: PostgreSQL connection object

    Returns:
        Dictionary containing borrower information or None if borrower_id is None or borrower not found
    """
    if not borrower_id:
        return None

    try:
        cursor = conn.cursor()

        # First try to get credit score from the borrower record
        cursor.execute("""
            SELECT b.enterprise_party_id 
            FROM mortgage_services.borrowers b
            WHERE b.mortgage_services_borrower_id = %s
        """, (borrower_id,))

        result = cursor.fetchone()

        if not result:
            cursor.close()
            return {}

        enterprise_party_id = result.get('enterprise_party_id')

        # Try to get estimated credit score from applications associated with this borrower
        cursor.execute("""
            SELECT a.estimated_credit_score
            FROM mortgage_services.applications a
            JOIN mortgage_services.application_borrowers ab 
              ON a.mortgage_services_application_id = ab.mortgage_services_application_id
            WHERE ab.mortgage_services_borrower_id = %s
            ORDER BY a.submission_date_time DESC
            LIMIT 1
        """, (borrower_id,))

        result = cursor.fetchone()
        if not result:
            cursor.close()
            return {}

        estimated_credit_score = result.get('estimated_credit_score')

        return {
            "enterprise_party_id": enterprise_party_id,
            "estimated_credit_score": estimated_credit_score
        }

    except psycopg2.ProgrammingError as error:
        logger.error(f"Error fetching borrower information: {error}")
        sys.exit(-1)
    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching borrower information: {error}")
        return None
