import random
from datetime import datetime, timedelta
from typing import Any, Dict

from data_generator import DataGenerator, SkipRowGenerationError
from .enums import ApplicationStatus, InterestRateType, LoanType

prev_app = set()


def generate_random_mortgage(_ids_dict: Dict[str, Any], dg: DataGenerator):
    """
    Generate a random mortgage with plausible correlations between various factors.

    Returns:
        dict: A dictionary with comprehensive mortgage details.
    """

    conn = dg.conn

    # Randomly choose an application ID
    application_id = _get_approved_application_id(dg)

    # SQL query to get the loan product details via the application_id
    query = """
        SELECT lp.*
        FROM mortgage_services.applications AS app
        JOIN mortgage_services.loan_products AS lp
        ON app.mortgage_services_loan_product_id = lp.mortgage_services_loan_product_id
        WHERE app.mortgage_services_application_id = %s
        """

    # Execute the query
    with conn.cursor() as cursor:
        cursor.execute(query, (application_id,))  # Parameterized query
        record = cursor.fetchone()  # Fetch the resulting record

    loan_product = record

    # SQL query to get the loan product details via the application_id
    query = """
                SELECT app.*
                FROM mortgage_services.applications AS app
                WHERE app.mortgage_services_application_id = %s
                """

    # Execute the query
    with conn.cursor() as cursor:
        cursor.execute(query, (application_id,))  # Parameterized query
        record = cursor.fetchone()  # Fetch the resulting record

    loan_application = record
    application_status = loan_application.get("status", "approved")

    max_amount = None

    application_credit_score = loan_application.get("estimated_credit_score", 700)
    application_loan_amount = loan_application.get("requested_loan_amount", 300000)
    application_loan_term = loan_application.get("requested_loan_term_months", 360)
    application_property_value = loan_application.get("estimated_property_value", 375000)

    # Extract loan details from the product
    product_type = LoanType[loan_product["loan_type"]]
    interest_rate_type = InterestRateType[loan_product["interest_rate_type"]]

    # Generate credit score that meets product requirements (if specified)
    min_credit_score = loan_product.get("min_credit_score", 0)
    if min_credit_score > 0:
        # Use application credit score if it meets minimum, otherwise adjust
        credit_score = max(min_credit_score, application_credit_score)
    else:
        # No minimum specified, use application credit score
        credit_score = application_credit_score

    # Generate ARM details if adjustable rate
    arm_details = {}
    if interest_rate_type == InterestRateType.ADJUSTABLE or product_type == LoanType.HOME_EQUITY:
        # Force adjustable for HELOC
        interest_rate_type = InterestRateType.ADJUSTABLE

        # Initial fixed period
        if product_type == LoanType.HOME_EQUITY:
            # HELOCs typically have 5-10 year draw periods
            initial_fixed_years = random.choice([5, 7, 10])
            arm_details["draw_period_years"] = initial_fixed_years
        else:
            # Common initial fixed periods for ARMs
            initial_fixed_years = random.choice([1, 3, 5, 7, 10])
            arm_details["initial_fixed_years"] = initial_fixed_years

        # Adjustment frequency (how often rate changes after initial period)
        arm_details["adjustment_frequency_months"] = random.choice([1, 6, 12])

        # Rate caps
        arm_details["initial_cap_percent"] = random.choice([1.0, 2.0, 3.0, 5.0])
        arm_details["periodic_cap_percent"] = random.choice([1.0, 2.0])
        arm_details["lifetime_cap_percent"] = random.choice([5.0, 6.0, 7.0])

        # Margin (added to index to determine new rate)
        arm_details["margin_percent"] = round(random.uniform(2.0, 3.5), 2)

        # Index type
        index_options = ["SOFR", "Treasury", "COFI", "LIBOR", "Prime Rate"]
        arm_details["index_type"] = random.choice(index_options)

        # Current index value (fake but plausible)
        index_value = round(random.uniform(1.0, 3.5), 2)
        arm_details["current_index_value"] = index_value

        # ARM naming convention (e.g., 5/1, 7/6)
        if product_type != LoanType.HOME_EQUITY:
            adjustment_frequency_years = arm_details["adjustment_frequency_months"] / 12
            if adjustment_frequency_years.is_integer():
                arm_details["arm_name"] = f"{initial_fixed_years}/{int(adjustment_frequency_years)}"
            else:
                arm_details["arm_name"] = f"{initial_fixed_years}/{arm_details['adjustment_frequency_months']}-month"

    # Set loan amount constraints based on product or default values
    if "min_loan_amount" in loan_product:
        min_amount = loan_product["min_loan_amount"]
    elif product_type == LoanType.JUMBO:
        min_amount = 750000
    elif product_type == LoanType.HOME_EQUITY:
        min_amount = 10000
    elif product_type == LoanType.REVERSE_MORTGAGE:
        min_amount = 50000
    elif product_type == LoanType.CONSTRUCTION:
        min_amount = 100000
    else:
        min_amount = 50000

    if "max_loan_amount" in loan_product:
        max_amount = loan_product["max_loan_amount"]
        max_amount_factor = 1.0  # Not needed but keeping for code structure
    elif product_type == LoanType.JUMBO:
        max_amount_factor = 0.7 + ((credit_score - 300) / 550) * 0.3  # Higher credit requirement
    elif product_type == LoanType.HOME_EQUITY:
        max_amount_factor = 0.3 + ((credit_score - 300) / 550) * 0.3
    elif product_type == LoanType.REVERSE_MORTGAGE:
        max_amount_factor = 0.4 + ((credit_score - 300) / 550) * 0.2
    elif product_type == LoanType.CONSTRUCTION:
        max_amount_factor = 0.5 + ((credit_score - 300) / 550) * 0.3
    else:
        max_amount_factor = 0.5 + ((credit_score - 300) / 550) * 0.5

    # If max_amount wasn't directly specified in the product
    if "max_loan_amount" not in loan_product:
        max_amount = int(2000000 * max_amount_factor)

    # Determine duration based on product constraints
    min_term_months = loan_product.get("min_term_months", 0)
    max_term_months = loan_product.get("max_term_months", 360)  # Default to 30 years max

    # Ensure the application term is within product constraints
    loan_term_months = max(min_term_months, min(max_term_months, application_loan_term))

    # Convert to years for easier handling
    duration_years = loan_term_months / 12

    # Use application loan amount, but ensure it's within product constraints
    # Also, slight variation can occur during underwriting (±5%)
    loan_amount_adjustment = random.uniform(0.95, 1.05)  # Underwriting may adjust amount slightly
    loan_amount = round(max(min_amount, min(max_amount, application_loan_amount * loan_amount_adjustment)), 2)

    # Generate start date (within last 30 years or next 2 months)
    now = datetime.now()

    # If application dates are provided, use them as reference
    if loan_application and "creation_date_time" in loan_application:
        try:
            app_creation_date = loan_application["creation_date_time"].date()
            # Origination typically happens 30-60 days after application
            min_days_after_app = 30
            max_days_after_app = 60
            days_after_app = random.randint(min_days_after_app, max_days_after_app)
            origination_date = app_creation_date + timedelta(days=days_after_app)
        except (ValueError, TypeError):
            # Fall back to random date if there's an issue parsing
            days_past = random.randint(-365 * 30, 60)  # 30 years in past to 2 months future
            origination_date = now + timedelta(days=days_past)
    else:
        # No application date provided, use random date
        days_past = random.randint(-365 * 30, 60)  # 30 years in past to 2 months future
        origination_date = now + timedelta(days=days_past)

    # Calculate first payment date (typically 1 month after origination)
    first_payment_date = origination_date + timedelta(days=30)

    # Calculate maturity date (loan term after first payment)
    if loan_term_months > 0:
        maturity_date = first_payment_date + timedelta(days=30 * loan_term_months)
    else:
        # For reverse mortgages or other special cases, use a default
        maturity_date = first_payment_date + timedelta(days=365 * 30)  # 30 years

    # Format dates as strings
    origination_date_str = origination_date.strftime("%Y-%m-%d")
    first_payment_date_str = first_payment_date.strftime("%Y-%m-%d")
    maturity_date_str = maturity_date.strftime("%Y-%m-%d")

    # Determine if this mortgage is in the past, present, or future
    years_from_now = (origination_date - now.date()).days / 365
    if years_from_now < 0:
        time_category = "existing"  # Started in the past
    else:
        time_category = "future"  # Will start in the future

    # Adjust interest rate based on historical trends
    # Rough approximation: rates were higher in the 1990s, lower in the 2010s
    # Historical rate adjustment (rough approximation)
    if years_from_now <= -25:  # 1995-2000
        historical_adjustment = random.uniform(1.5, 3.0)  # Higher rates in late 90s
    elif years_from_now <= -15:  # 2000-2010
        historical_adjustment = random.uniform(0.5, 1.5)  # Moderate rates
    elif years_from_now <= -5:  # 2010-2020
        historical_adjustment = random.uniform(-1.0, 0.5)  # Lower rates post-2008
    else:  # Recent past, present, or near future
        historical_adjustment = random.uniform(-0.5, 0.5)  # Current rate environment

    # Calculate interest rate using product base rate if provided
    if "base_interest_rate" in loan_product:
        base_rate = loan_product["base_interest_rate"]
    else:
        # Default base rate by loan type and interest rate type
        if product_type == LoanType.FHA:
            base_rate = 4.0 if interest_rate_type == InterestRateType.FIXED else 3.2
        elif product_type == LoanType.VA:
            base_rate = 3.7 if interest_rate_type == InterestRateType.FIXED else 3.0
        elif product_type == LoanType.USDA:
            base_rate = 3.9 if interest_rate_type == InterestRateType.FIXED else 3.2
        elif product_type == LoanType.JUMBO:
            base_rate = 4.2 if interest_rate_type == InterestRateType.FIXED else 3.5
        elif product_type == LoanType.HOME_EQUITY:
            base_rate = 5.5  # HELOCs typically higher
        elif product_type == LoanType.REVERSE_MORTGAGE:
            base_rate = 4.5
        elif product_type == LoanType.CONSTRUCTION:
            base_rate = 5.0 if interest_rate_type == InterestRateType.FIXED else 4.2
        else:  # conventional
            base_rate = 3.8 if interest_rate_type == InterestRateType.FIXED else 3.0

    # Credit score adjustment (higher score = lower rate)
    credit_adjustment = (800 - credit_score) / 100

    # Duration adjustment (longer term = higher rate)
    if duration_years > 0:  # Skip for reverse mortgage
        duration_adjustment = (duration_years - 10) / 40 if duration_years >= 10 else 0
    else:
        duration_adjustment = 0

    # Amount adjustment (larger loan = slightly lower rate due to economy of scale)
    amount_adjustment = -0.1 * (loan_amount / 2000000)

    # ARM adjustment (longer initial fixed periods get higher rates)
    if interest_rate_type == InterestRateType.ADJUSTABLE and "initial_fixed_years" in arm_details:
        arm_adjustment = arm_details["initial_fixed_years"] / 30  # Longer fixed = higher rate
    else:
        arm_adjustment = 0

    # Calculate final rate with historical adjustment
    interest_rate = base_rate + credit_adjustment + duration_adjustment + amount_adjustment + arm_adjustment + historical_adjustment
    interest_rate += random.uniform(-0.25, 0.25)  # Add small random variation
    interest_rate = max(2.0, min(12.0, interest_rate))  # Expanded range to accommodate historical rates
    interest_rate = round(interest_rate, 3)  # Round to 3 decimal places

    # Generate down payment information using product constraints if provided
    if "min_down_payment_percentage" in loan_product:
        min_down = loan_product["min_down_payment_percentage"]

        # Generate a down payment at or above the minimum
        if min_down == 0:
            # If 0% allowed, mostly use 0% but sometimes add small down payment
            down_payment_percentage = random.choices([0, 3, 5, 10], weights=[0.7, 0.1, 0.1, 0.1])[0]
        elif min_down <= 3.5:
            # FHA-like minimums
            down_payment_percentage = random.choices([min_down, 5, 10, 15], weights=[0.6, 0.2, 0.1, 0.1])[0]
        elif min_down <= 10:
            # Moderate minimums
            down_payment_percentage = random.choices([min_down, min_down + 5, 20], weights=[0.5, 0.3, 0.2])[0]
        else:
            # High minimums
            down_payment_percentage = random.choices([min_down, min_down + 5, min_down + 10], weights=[0.5, 0.3, 0.2])[
                0]
    else:
        # No product constraints, use defaults based on loan type
        if product_type == LoanType.VA:
            # VA loans can be 0% down
            down_payment_percentage = random.choices([0, 5, 10], weights=[0.7, 0.2, 0.1])[0]
        elif product_type == LoanType.FHA:
            # FHA requires at least 3.5%
            down_payment_percentage = random.choices([3.5, 5, 10], weights=[0.6, 0.3, 0.1])[0]
        elif product_type == "conventional":
            # Conventional typically 3-20%
            if credit_score > 740:
                down_payment_percentage = random.choices([3, 5, 10, 15, 20], weights=[0.1, 0.2, 0.3, 0.2, 0.2])[0]
            elif credit_score > 680:
                down_payment_percentage = random.choices([5, 10, 15, 20], weights=[0.3, 0.3, 0.2, 0.2])[0]
            else:
                down_payment_percentage = random.choices([10, 15, 20], weights=[0.4, 0.3, 0.3])[0]
        elif product_type == LoanType.JUMBO:
            # Jumbo loans typically require higher down payments
            down_payment_percentage = random.choices([10, 15, 20, 25, 30], weights=[0.1, 0.2, 0.3, 0.2, 0.2])[0]
        elif product_type == LoanType.HOME_EQUITY or product_type == LoanType.REVERSE_MORTGAGE:
            # These products don't have traditional down payments
            down_payment_percentage = 0
        else:
            # Default for other products
            down_payment_percentage = random.choices([5, 10, 15, 20], weights=[0.25, 0.35, 0.25, 0.15])[0]

    # Use application property value with a slight adjustment for appraisal
    # Appraisals can come in slightly different from estimated value
    appraisal_factor = random.uniform(0.95, 1.05)
    purchase_price = round(application_property_value * appraisal_factor, 2)

    # Calculate down payment amount from percentage and purchase price
    if down_payment_percentage > 0:
        down_payment = round(purchase_price * (down_payment_percentage / 100), 2)
    else:
        # For products without down payments
        down_payment = 0

    # Determine if PMI is required
    if "requires_pmi" in loan_product:
        # Use product specification
        private_mortgage_insurance = loan_product["requires_pmi"]
    else:
        # Default logic: PMI for conventional loans with < 20% down
        private_mortgage_insurance = (product_type == "conventional" and down_payment_percentage < 20)

    # PMI rate depends on credit score and down payment
    pmi_rate = 0
    if private_mortgage_insurance:
        if credit_score > 760:
            pmi_rate = round(random.uniform(0.2, 0.4), 3)
        elif credit_score > 740:
            pmi_rate = round(random.uniform(0.3, 0.5), 3)
        elif credit_score > 720:
            pmi_rate = round(random.uniform(0.5, 0.7), 3)
        elif credit_score > 700:
            pmi_rate = round(random.uniform(0.7, 0.9), 3)
        elif credit_score > 680:
            pmi_rate = round(random.uniform(0.8, 1.1), 3)
        else:
            pmi_rate = round(random.uniform(1.0, 1.5), 3)

    # Calculate estimated closing costs (typically 2-5% of loan amount)
    closing_cost_percentage = round(random.uniform(2.0, 5.0), 2)
    estimated_closing_costs = round(loan_amount * (closing_cost_percentage / 100), 2)

    # Calculate monthly payment (principal and interest)
    if product_type == LoanType.REVERSE_MORTGAGE:
        estimated_monthly_payment = 0  # Reverse mortgages pay the borrower
    else:
        estimated_monthly_payment = _calculate_monthly_payment(loan_amount, interest_rate, loan_term_months)

    # Calculate escrow amount (property taxes and insurance)
    # Typically around 0.25-0.5% of purchase price monthly
    if product_type not in [LoanType.HOME_EQUITY, LoanType.REVERSE_MORTGAGE]:
        yearly_escrow_percentage = round(random.uniform(2.0, 5.0), 2)  # Annual percentage
        yearly_escrow = purchase_price * (yearly_escrow_percentage / 100)
        escrow_amount = round(yearly_escrow / 12, 2)  # Monthly amount
    else:
        escrow_amount = 0  # HELOCs and reverse mortgages typically don't have escrow

    # Create the mortgage dictionary with the exact fields from the loans table
    _mortgage = {
        # Fields exactly matching mortgage_services.loans table
        "interest_rate": interest_rate,
        "loan_term_months": loan_term_months,
        "loan_amount": round(loan_amount, 2),
        "down_payment": down_payment,
        "down_payment_percentage": round(down_payment_percentage, 2),
        "closing_costs": estimated_closing_costs,  # renamed from estimated_closing_costs
        "monthly_payment": estimated_monthly_payment,  # renamed from estimated_monthly_payment
        "private_mortgage_insurance": private_mortgage_insurance,
        "pmi_rate": pmi_rate,
        "escrow_amount": escrow_amount,
        "origination_date": origination_date_str,
        "first_payment_date": first_payment_date_str,
        "maturity_date": maturity_date_str
    }

    # Optional additional fields that might be useful but aren't in the table schema
    mortgage_extras = {
        "credit_score": credit_score,
        "loan_type": interest_rate_type,  # fixed or adjustable
        "loan_product": product_type,
        "duration_years": duration_years,
        "time_category": time_category,
        "application_status": application_status  # Include application status for reference
    }

    # Add loan product name if available
    if "product_name" in loan_product:
        mortgage_extras["product_name"] = loan_product["product_name"]

    # Add loan product code if available
    if "product_code" in loan_product:
        mortgage_extras["product_code"] = loan_product["product_code"]

    # Add ARM details if applicable
    if arm_details:
        mortgage_extras["arm_details"] = arm_details

    # Merge the extras into the main mortgage dict
    _mortgage.update(mortgage_extras)

    prev_app.add(application_id)

    return _mortgage


def _get_approved_application_id(dg: DataGenerator):
    """
    Find an application ID that is approved and hasn't been used yet.

    Args:
        dg: DataGenerator instance with database connection

    Returns:
        An approved application ID that hasn't been used

    Raises:
        SkipRowGenerationError: If no valid applications found
    """
    conn = dg.conn
    global prev_app

    query = """
        SELECT mortgage_services_application_id 
        FROM mortgage_services.applications 
        WHERE status = %s
    """

    with conn.cursor() as cursor:
        cursor.execute(query, (ApplicationStatus.APPROVED.name,))
        approved_applications = [row.get('mortgage_services_application_id') for row in cursor.fetchall()]

    # Filter out applications that have already been used
    available_applications = [app_id for app_id in approved_applications if app_id not in prev_app]

    if not available_applications:
        raise SkipRowGenerationError("No approved applications available")

    # Return a random available application ID
    result = random.choice(available_applications)
    prev_app.add(result)
    return result


def _calculate_monthly_payment(principal, rate, term_months):
    """
    Calculate the monthly payment for a mortgage.

    Args:
        principal: Loan amount
        rate: Annual interest rate (as a percentage)
        term_months: Loan term in months

    Returns:
        Monthly payment amount
    """
    # Ensure term is always positive
    if term_months <= 0:
        term_months = 360  # Default to 30 years if no term specified

    monthly_rate = rate / 100 / 12

    if monthly_rate == 0:  # Edge case for 0% interest
        return round(principal / term_months, 2)

    monthly_payment = principal * (monthly_rate * (1 + monthly_rate) ** term_months) / (
            (1 + monthly_rate) ** term_months - 1)
    return round(monthly_payment, 2)
