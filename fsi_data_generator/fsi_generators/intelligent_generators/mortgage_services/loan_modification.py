from .enums import HardshipReason, LoanModificationStatus, LoanModificationType
from typing import Any, Dict, Optional

import datetime
import logging
import psycopg2
import random

logger = logging.getLogger(__name__)


def generate_random_loan_modification(id_fields: Dict[str, Any], dg) -> Dict[str, Any]:
    """
    Generate a random mortgage services loan modification record with realistic values.

    Args:
        id_fields: Dictionary containing the required ID fields (mortgage_services_servicing_account_id)
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated loan modification data (without ID fields)
    """
    # Get servicing account information to make modification data reasonable
    conn = dg.conn
    servicing_account_info = _get_servicing_account_info(id_fields.get("mortgage_services_servicing_account_id"), conn)

    # Set up weights for modification types
    type_weights = [0.30, 0.25, 0.15, 0.05, 0.15, 0.05, 0.02, 0.03, 0, 0, 0, 0, 0]

    # Select the modification type based on weights
    modification_type = LoanModificationType.get_random(type_weights)

    # Generate request date (typically within the last 2 years)
    today = datetime.date.today()
    days_ago = random.randint(30, 730)  # Between 1 month and 2 years ago
    request_date = today - datetime.timedelta(days=days_ago)

    # Generate approval date (typically 15-60 days after request)
    days_after_request = random.randint(15, 60)
    approval_date = request_date + datetime.timedelta(days=days_after_request)

    # If approval date would be in the future, there's a chance it's still pending
    # Ensure we're comparing same types (date objects)
    approval_date_obj = approval_date if isinstance(approval_date, datetime.date) else approval_date.date() if hasattr(
        approval_date, 'date') else None

    if approval_date_obj and approval_date_obj > today:
        # 80% chance it's still pending
        if random.random() < 0.8:
            approval_date = None
            # Use enum status values
            status_weights = [0.6, 0, 0, 0, 0.4, 0, 0, 0, 0, 0, 0, 0, 0]  # Weights for PENDING and IN_PROGRESS
            status = LoanModificationStatus.get_random(status_weights)
            effective_date = None
        else:
            # It got approved very recently
            approval_date = today - datetime.timedelta(days=random.randint(0, 7))
            status = LoanModificationStatus.APPROVED

            # Effective date is typically 1-30 days after approval
            days_after_approval = random.randint(1, 30)
            effective_date = approval_date + datetime.timedelta(days=days_after_approval)

            # If effective date would be in the future, keep it
            effective_date_obj = effective_date if isinstance(effective_date,
                                                              datetime.date) else effective_date.date() if hasattr(
                effective_date, 'date') else None
            if effective_date_obj and effective_date_obj > today:
                # Keep the future effective date as is
                pass
            else:
                effective_date = None
    else:
        # Approval happened in the past, so it could be in any state
        status_weights = [0, 0.2, 0.1, 0.25, 0.4, 0.05, 0, 0, 0, 0, 0, 0, 0]  # Weights for statuses in enum order
        status = LoanModificationStatus.get_random(status_weights)

        if status in [LoanModificationStatus.APPROVED, LoanModificationStatus.IN_PROGRESS,
                      LoanModificationStatus.COMPLETED]:
            # Effective date is typically 1-30 days after approval
            days_after_approval = random.randint(1, 30)
            effective_date = approval_date + datetime.timedelta(days=days_after_approval)

            # If effective date would be in the future, it's in 'approved' status
            effective_date_obj = effective_date if isinstance(effective_date,
                                                              datetime.date) else effective_date.date() if hasattr(
                effective_date, 'date') else None
            if effective_date_obj and effective_date_obj > today:
                status = LoanModificationStatus.APPROVED
        else:
            # Rejected or withdrawn doesn't have effective date
            effective_date = None

    # Get initial loan terms from servicing account
    original_rate = None
    original_term_months = None
    original_principal_balance = None

    if servicing_account_info:
        if 'current_interest_rate' in servicing_account_info and servicing_account_info[
            'current_interest_rate'] is not None:
            # Explicitly convert to float to handle Decimal objects
            original_rate = float(servicing_account_info['current_interest_rate'])

        if 'original_term_months' in servicing_account_info and servicing_account_info[
            'original_term_months'] is not None:
            original_term_months = int(servicing_account_info['original_term_months'])

        if 'current_principal' in servicing_account_info and servicing_account_info['current_principal'] is not None:
            # Explicitly convert to float to handle Decimal objects
            original_principal_balance = float(servicing_account_info['current_principal'])

    # Generate new terms based on modification type
    # For rate reduction
    if original_rate:
        # For rate reduction, decrease interest rate by 0.25% to 2.0%
        if modification_type == LoanModificationType.RATE_REDUCTION:
            rate_decrease = random.uniform(0.25, 2.0)
            new_rate = max(1.0, original_rate - rate_decrease)  # Ensure rate doesn't go below 1%
        # For other types with similar rate reduction
        elif modification_type in [LoanModificationType.OTHER, LoanModificationType.STEP_RATE]:
            rate_decrease = random.uniform(0.1, 0.75)
            new_rate = max(1.5, original_rate - rate_decrease)
        # For other modifications, rate typically stays the same or changes slightly
        else:
            rate_change = random.uniform(-0.25, 0.25)
            new_rate = max(1.0, original_rate + rate_change)
    else:
        # Default reasonable rate if we don't have original
        new_rate = random.uniform(3.5, 6.5)

    # For term extension
    if original_term_months:
        if modification_type == LoanModificationType.TERM_EXTENSION:
            # Extend term by 60-180 months
            term_extension = random.choice([60, 120, 180])
            new_term_months = original_term_months + term_extension
        elif modification_type == LoanModificationType.PAYMENT_DEFERRAL:
            # Term might be extended slightly to accommodate deferral
            term_extension = random.randint(3, 24)
            new_term_months = original_term_months + term_extension
        else:
            # Other modifications may have small term changes
            term_change = random.randint(-12, 12)
            new_term_months = max(120, original_term_months + term_change)  # Minimum 10 year term
    else:
        # Default reasonable term if we don't have original
        new_term_months = random.choice([180, 240, 360])  # 15, 20, or 30 years

    # For principal modifications
    if original_principal_balance:
        if modification_type == LoanModificationType.PRINCIPAL_REDUCTION:
            # Forbear 10-30% of principal
            forbearance_percentage = random.uniform(0.1, 0.3)
            new_principal_balance = original_principal_balance * (1 - forbearance_percentage)
        elif modification_type == LoanModificationType.PRINCIPAL_FORGIVENESS:
            # Forgive 5-15% of principal
            forgiveness_percentage = random.uniform(0.05, 0.15)
            new_principal_balance = original_principal_balance * (1 - forgiveness_percentage)
        else:
            # Other modifications typically don't change principal
            new_principal_balance = original_principal_balance
    else:
        # Default to a reasonable principal balance
        new_principal_balance = random.uniform(150000, 500000)

    # Round values appropriately
    new_rate = round(new_rate, 3)
    new_principal_balance = round(new_principal_balance, 2)

    reason = HardshipReason.get_random()

    # Create the loan modification record
    # Ensure all fields match the mortgage_services.loan_modifications table in DBML
    modification = {
        "modification_type": modification_type.value,
        "request_date": request_date,
        "approval_date": approval_date,
        "effective_date": effective_date,
        "original_rate": original_rate,
        "new_rate": new_rate,
        "original_term_months": original_term_months,
        "new_term_months": new_term_months,
        "original_principal_balance": original_principal_balance,
        "new_principal_balance": new_principal_balance,
        "status": status.value,
        "reason": reason.value
    }

    return modification


def _get_servicing_account_info(servicing_account_id: Optional[int], conn) -> Optional[Dict[str, Any]]:
    """
    Get servicing account information to make modification data reasonable.

    Args:
        servicing_account_id: The ID of the servicing account
        conn: PostgreSQL connection object

    Returns:
        Dictionary containing servicing account information or None if not found
    """
    if not servicing_account_id:
        return None

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT l.mortgage_services_loan_id, 
                   sa.original_principal_balance, 
                   sa.current_principal_balance, 
                   sa.current_interest_rate, 
                   l.loan_term_months AS original_term_months, 
                   /* Calculate remaining term based on maturity date and current date */
                   CASE 
                      WHEN l.maturity_date IS NOT NULL 
                      THEN GREATEST(0, EXTRACT(YEAR FROM age(l.maturity_date, CURRENT_DATE)) * 12 
                                     + EXTRACT(MONTH FROM age(l.maturity_date, CURRENT_DATE)))::INTEGER
                      ELSE l.loan_term_months
                   END AS remaining_term_months
            FROM mortgage_services.servicing_accounts sa
            JOIN mortgage_services.loans l ON sa.mortgage_services_loan_id = l.mortgage_services_loan_id
            WHERE sa.mortgage_services_servicing_account_id = %s
        """, (servicing_account_id,))

        result = cursor.fetchone()
        cursor.close()

        return result

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching servicing account information: {error}")
        return None


def _get_loan_info(loan_id: Optional[int], conn) -> Optional[Dict[str, Any]]:
    """
    Get loan information to make modification data reasonable.

    Args:
        loan_id: The ID of the loan
        conn: PostgreSQL connection object

    Returns:
        Dictionary containing loan information or None if not found
    """
    if not loan_id:
        return None

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT CAST(interest_rate AS FLOAT), 
                   loan_term_months, 
                   CAST(loan_amount AS FLOAT), 
                   origination_date, 
                   maturity_date
            FROM mortgage_services.loans 
            WHERE mortgage_services_loan_id = %s
        """, (loan_id,))

        result = cursor.fetchone()
        cursor.close()

        if result:
            return {
                "interest_rate": result[0],
                "loan_term_months": result[1],
                "loan_amount": result[2],
                "origination_date": result[3],
                "maturity_date": result[4]
            }
        else:
            return None

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching loan information: {error}")
        return None
