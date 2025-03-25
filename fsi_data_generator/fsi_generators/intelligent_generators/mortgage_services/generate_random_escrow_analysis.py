import datetime
import logging
import random
from typing import Any, Dict, Optional

import psycopg2

logger = logging.getLogger(__name__)


def generate_random_escrow_analysis(id_fields: Dict[str, Any], dg) -> Dict[str, Any]:
    """
    Generate a random mortgage services escrow analysis record with reasonable values.

    Args:
        id_fields: Dictionary containing the required ID fields (mortgage_services_servicing_account_id)
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated escrow analysis data (without ID fields)

    Raises:
        SkipRowGenerationError: If there are already multiple recent analyses for this account
    """
    # Get servicing account information to make escrow analysis data reasonable
    conn = dg.conn
    servicing_account_info = _get_servicing_account_info(id_fields["mortgage_services_servicing_account_id"], conn)

    if not servicing_account_info:
        # Use default values if no servicing account info is found
        servicing_account_info = {
            "escrow_balance": 1200.0,
            "next_payment_amount": 1500.0,
            "property_tax_due_date": datetime.date.today() + datetime.timedelta(days=90),
            "homeowners_insurance_due_date": datetime.date.today() + datetime.timedelta(days=180)
        }

    # Get previous escrow analyses to ensure consistency and avoid duplicates
    previous_analyses = _get_previous_escrow_analyses(id_fields["mortgage_services_servicing_account_id"], conn)

    # Check if we already have multiple recent analyses (fewer than 6 months old)
    today = datetime.date.today()
    recent_analyses = [a for a in previous_analyses if (today - a["analysis_date"]).days < 180]

    if len(recent_analyses) >= 2:
        # Already have multiple recent analyses, likely don't need another one
        from data_generator import SkipRowGenerationError
        raise SkipRowGenerationError("Account already has multiple recent escrow analyses")

    # Generate analysis date
    if previous_analyses:
        # Place this analysis before the earliest or after the latest previous analysis
        if random.random() < 0.7:  # 70% chance to create an older analysis
            earliest_analysis = min(previous_analyses, key=lambda x: x["analysis_date"])
            # Place this analysis 6-18 months before the earliest existing one
            days_before = random.randint(180, 540)
            analysis_date = earliest_analysis["analysis_date"] - datetime.timedelta(days=days_before)
            # Ensure analysis date isn't unreasonably old (not before 5 years ago)
            min_date = today - datetime.timedelta(days=365 * 5)
            analysis_date = max(analysis_date, min_date)
        else:
            # Place this analysis after the most recent one
            latest_analysis = max(previous_analyses, key=lambda x: x["analysis_date"])
            # Place this analysis 6-12 months after the latest existing one
            days_after = random.randint(180, 365)
            analysis_date = latest_analysis["analysis_date"] + datetime.timedelta(days=days_after)
            # Ensure analysis date isn't in the future
            analysis_date = min(analysis_date, today)
    else:
        # No previous analyses, create one within the last 12 months
        days_ago = random.randint(30, 365)
        analysis_date = today - datetime.timedelta(days=days_ago)

    # Generate effective date (typically 1-2 months after analysis date)
    days_after_analysis = random.randint(30, 60)
    effective_date = analysis_date + datetime.timedelta(days=days_after_analysis)

    # Calculate previous monthly escrow amount
    # If we have a previous analysis, use its new_monthly_escrow as our previous_monthly_escrow
    if previous_analyses and analysis_date > min(a["analysis_date"] for a in previous_analyses):
        # Find the most recent analysis that came before this one
        previous_analysis = None
        for a in previous_analyses:
            if a["analysis_date"] < analysis_date and (
                    previous_analysis is None or a["analysis_date"] > previous_analysis["analysis_date"]):
                previous_analysis = a

        if previous_analysis and "new_monthly_escrow" in previous_analysis and previous_analysis["new_monthly_escrow"]:
            previous_monthly_escrow = previous_analysis["new_monthly_escrow"]
        else:
            # Estimate based on typical escrow portion of payment
            previous_monthly_escrow = _estimate_monthly_escrow(servicing_account_info)
    else:
        # Estimate based on typical escrow portion of payment
        previous_monthly_escrow = _estimate_monthly_escrow(servicing_account_info)

    # Calculate new monthly escrow amount based on projections and any shortage/surplus
    # First, estimate annual escrow expenses
    annual_property_tax = _estimate_annual_property_tax(servicing_account_info)
    annual_homeowners_insurance = _estimate_annual_homeowners_insurance(servicing_account_info)
    other_annual_expenses = _estimate_other_escrow_expenses(servicing_account_info)

    total_annual_expenses = annual_property_tax + annual_homeowners_insurance + other_annual_expenses

    # New base monthly escrow would be annual expenses divided by 12
    base_monthly_escrow = total_annual_expenses / 12

    # Determine if there's a shortage or surplus
    # This would be based on current escrow balance vs. required cushion
    escrow_balance = servicing_account_info.get("escrow_balance", 0)

    # Required cushion is typically 2 months of escrow payments
    required_cushion = base_monthly_escrow * 2

    # Calculate shortage or surplus
    if escrow_balance < required_cushion:
        # There's a shortage
        escrow_shortage = required_cushion - escrow_balance
        escrow_surplus = 0
    else:
        # There's a surplus
        escrow_shortage = 0
        escrow_surplus = escrow_balance - required_cushion

    # Determine how to handle the shortage (if any)
    shortage_spread_months = 0
    if escrow_shortage > 0:
        # Typically spread over 12 months, but can range from 1-24 months
        shortage_spread_months = random.choice([1, 3, 6, 12, 24])

        # Add the shortage spread to the monthly amount
        monthly_shortage_payment = escrow_shortage / shortage_spread_months
        new_monthly_escrow = base_monthly_escrow + monthly_shortage_payment
    else:
        new_monthly_escrow = base_monthly_escrow

    # If there's a large surplus, it might be refunded to the borrower
    surplus_refund_amount = 0
    if escrow_surplus > base_monthly_escrow:
        # Large surplus - some might be refunded
        surplus_refund_amount = escrow_surplus - base_monthly_escrow

        # But sometimes they keep the whole surplus in the account
        if random.random() < 0.3:  # 30% chance of no refund
            surplus_refund_amount = 0

    # Round all monetary values to 2 decimal places
    previous_monthly_escrow = round(previous_monthly_escrow, 2)
    new_monthly_escrow = round(new_monthly_escrow, 2)
    escrow_shortage = round(escrow_shortage, 2)
    escrow_surplus = round(escrow_surplus, 2)
    surplus_refund_amount = round(surplus_refund_amount, 2)

    # Generate notification date (typically a few days after analysis)
    days_after_for_notification = random.randint(3, 10)
    customer_notification_date = analysis_date + datetime.timedelta(days=days_after_for_notification)

    # Set status based on dates and current date
    if effective_date > today:
        status = "pending"
    else:
        status = "active"

    # Create the escrow analysis record
    escrow_analysis = {
        "analysis_date": analysis_date,
        "effective_date": effective_date,
        "previous_monthly_escrow": float(previous_monthly_escrow),
        "new_monthly_escrow": float(new_monthly_escrow),
        "escrow_shortage": float(escrow_shortage) if escrow_shortage > 0 else None,
        "escrow_surplus": float(escrow_surplus) if escrow_surplus > 0 else None,
        "shortage_spread_months": shortage_spread_months if escrow_shortage > 0 else None,
        "surplus_refund_amount": float(surplus_refund_amount) if surplus_refund_amount > 0 else None,
        "status": status,
        "customer_notification_date": customer_notification_date
    }

    return escrow_analysis


def _get_servicing_account_info(servicing_account_id: int, conn) -> Optional[Dict[str, Any]]:
    """
    Get servicing account information to make escrow analysis data reasonable.

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
                current_principal_balance, 
                original_principal_balance,
                escrow_balance,
                next_payment_amount,
                property_tax_due_date,
                homeowners_insurance_due_date
            FROM mortgage_services.servicing_accounts 
            WHERE mortgage_services_servicing_account_id = %s
        """, (servicing_account_id,))

        result = cursor.fetchone()
        cursor.close()

        return result

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching servicing account information: {error}")
        return None


def _get_previous_escrow_analyses(servicing_account_id: int, conn) -> list:
    """
    Get previous escrow analyses for consistency checking.

    Args:
        servicing_account_id: The ID of the servicing account
        conn: PostgreSQL connection object

    Returns:
        List of previous escrow analyses sorted by analysis date (desc)
    """
    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                analysis_date,
                effective_date,
                previous_monthly_escrow,
                new_monthly_escrow,
                escrow_shortage,
                escrow_surplus,
                shortage_spread_months,
                surplus_refund_amount,
                status,
                customer_notification_date
            FROM mortgage_services.escrow_analyses 
            WHERE mortgage_services_servicing_account_id = %s
            ORDER BY analysis_date DESC
        """, (servicing_account_id,))

        results = cursor.fetchall()
        cursor.close()

        analyses = []
        for row in results:
            analyses.append(row)

        return analyses

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching previous escrow analyses: {error}")
        return []


def _estimate_monthly_escrow(servicing_account_info: Dict[str, Any]) -> float:
    """
    Estimate monthly escrow payment based on payment amount.

    Args:
        servicing_account_info: Dictionary containing servicing account information

    Returns:
        Estimated monthly escrow payment
    """
    payment_amount = servicing_account_info.get("next_payment_amount")

    if payment_amount:
        # Escrow is typically 15-35% of the payment
        escrow_percentage = random.uniform(0.15, 0.35)
        return payment_amount * escrow_percentage
    else:
        # If no payment info, estimate based on loan size
        principal_balance = servicing_account_info.get("current_principal_balance", 200000)
        # Rough estimate: annual escrow of 1-2% of loan balance divided by 12
        annual_percentage = random.uniform(0.01, 0.02)
        annual_escrow = principal_balance * annual_percentage
        return annual_escrow / 12


def _estimate_annual_property_tax(servicing_account_info: Dict[str, Any]) -> float:
    """
    Estimate annual property tax based on loan amount.

    Args:
        servicing_account_info: Dictionary containing servicing account information

    Returns:
        Estimated annual property tax
    """
    loan_amount = servicing_account_info.get("original_principal_balance", 200000.0)

    # Property value is typically higher than loan amount (80-95% LTV)
    ltv_ratio = random.uniform(0.8, 0.95)
    property_value = loan_amount / ltv_ratio

    # Property tax rate typically 0.5-2.5% of property value
    tax_rate = random.uniform(0.005, 0.025)

    annual_tax = property_value * tax_rate
    return round(annual_tax, 2)


def _estimate_annual_homeowners_insurance(servicing_account_info: Dict[str, Any]) -> float:
    """
    Estimate annual homeowners insurance based on loan amount.

    Args:
        servicing_account_info: Dictionary containing servicing account information

    Returns:
        Estimated annual homeowners insurance
    """
    loan_amount = servicing_account_info.get("original_principal_balance", 200000.0)

    # Property value is typically higher than loan amount (80-95% LTV)
    ltv_ratio = random.uniform(0.8, 0.95)

    # Insurance typically 0.25-0.5% of property value
    insurance_rate = random.uniform(0.0025, 0.005)
    property_value = loan_amount / ltv_ratio

    annual_insurance = property_value * insurance_rate
    return round(annual_insurance, 2)


def _estimate_other_escrow_expenses(servicing_account_info: Dict[str, Any]) -> float:
    """
    Estimate other annual escrow expenses (HOA, PMI, etc.)

    Args:
        servicing_account_info: Dictionary containing servicing account information

    Returns:
        Estimated annual other escrow expenses
    """
    loan_amount = servicing_account_info.get("original_principal_balance", 200000.0)

    # Small chance of other escrow expenses
    if random.random() < 0.2:  # 20% chance
        # Typically 0.1-0.5% of loan amount
        expense_rate = random.uniform(0.001, 0.005)
        annual_expense = loan_amount * expense_rate
        return round(annual_expense, 2)
    else:
        return 0.0
