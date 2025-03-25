import datetime
import logging
import random
from typing import Any, Dict, Optional

import psycopg2

from data_generator import DataGenerator

logger = logging.getLogger(__name__)


def generate_random_hmda_record(id_fields: Dict, dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random mortgage services HMDA record with reasonable values.

    Args:
        id_fields: Dictionary containing the required ID fields (mortgage_services_application_id,
                   mortgage_services_loan_id as optional)
        dg: DataGenerator object

    Returns:
        Dictionary containing randomly generated HMDA record data (without ID fields)
    """
    # Get application and loan information to make HMDA record data reasonable
    conn = dg.conn
    application_info = get_application_info(id_fields.get("mortgage_services_application_id"), conn)
    loan_info = None
    if "mortgage_services_loan_id" in id_fields:
        loan_info = get_loan_info(id_fields.get("mortgage_services_loan_id"), conn)

    # Define possible values for categorical fields
    reporting_year = datetime.date.today().year

    # Get a legal entity identifier (LEI) for the reporting institution
    lei = "ABCDEFGHIJKLM1234567"  # Example LEI (typically 20 characters)

    # Generate loan purpose based on application type if available
    loan_purposes = {
        "1": "Home purchase",
        "2": "Home improvement",
        "31": "Refinancing",
        "32": "Cash-out refinancing",
        "4": "Other purpose",
        "5": "Not applicable"
    }

    loan_purpose_weights = [0.5, 0.1, 0.2, 0.15, 0.04, 0.01]

    # Create mappings for application types to ensure consistency
    application_type_mapping = {
        # Direct matches (case-insensitive)
        "purchase": "Purchase",
        "refinance": "Refinance",
        "heloc": "HomeEquity",
        # Alternative formats that might appear
        "home equity": "HomeEquity",
        "cash-out refinance": "Refinance",
        "rate and term refinance": "Refinance"
    }

    if application_info and 'application_type' in application_info:
        app_type = application_info['application_type']

        # Convert to standard format using the mapping (case-insensitive)
        app_type_normalized = app_type.lower()
        app_type = application_type_mapping.get(app_type_normalized, app_type)

        if app_type == "Purchase":
            loan_purpose = "1"  # Home purchase
        elif app_type == "Refinance":
            loan_purpose = random.choices(["31", "32"], weights=[0.6, 0.4], k=1)[0]  # Various refinancing options
        elif app_type == "HomeEquity":
            loan_purpose = "2"  # Home improvement
        else:
            loan_purpose = random.choices(list(loan_purposes.keys()), weights=loan_purpose_weights, k=1)[0]
    else:
        loan_purpose = random.choices(list(loan_purposes.keys()), weights=loan_purpose_weights, k=1)[0]

    # Generate preapproval status
    preapproval_options = {
        "1": "Preapproval requested",
        "2": "Preapproval not requested"
    }
    preapproval = random.choices(list(preapproval_options.keys()), weights=[0.2, 0.8], k=1)[0]

    # Generate construction method
    construction_methods = {
        "1": "Site-built",
        "2": "Manufactured home"
    }
    construction_method = random.choices(list(construction_methods.keys()), weights=[0.95, 0.05], k=1)[0]

    # Generate occupancy type
    occupancy_types = {
        "1": "Primary residence",
        "2": "Second residence",
        "3": "Investment property"
    }

    occupancy_weights = [0.8, 0.1, 0.1]
    occupancy_type = random.choices(list(occupancy_types.keys()), weights=occupancy_weights, k=1)[0]

    # Generate loan amount based on application or loan info
    if loan_info and 'loan_amount' in loan_info:
        loan_amount = loan_info['loan_amount']
    elif application_info and 'requested_loan_amount' in application_info:
        loan_amount = application_info['requested_loan_amount']
    else:
        loan_amount = round(random.uniform(50000, 750000), 2)

    # Create mappings for application status to ensure consistency
    application_status_mapping = {
        # Direct matches (case-insensitive)
        "approved": "approved",
        "denied": "denied",
        "withdrawn": "withdrawn",
        # Alternative formats that might appear
        "under review": "in review",
        "in review": "in review",
        "incomplete": "incomplete",
        "cancelled": "withdrawn",
        "canceled": "withdrawn",
        "funded": "approved",  # A funded loan was approved
        "draft": "incomplete",
        "submitted": "in review",
    }

    # Generate action taken based on application status if available
    action_taken_options = {
        "1": "Loan originated",
        "2": "Application approved but not accepted",
        "3": "Application denied",
        "4": "Application withdrawn by applicant",
        "5": "File closed for incompleteness",
        "6": "Loan purchased by institution",
        "7": "Preapproval request denied",
        "8": "Preapproval request approved but not accepted"
    }

    action_weights = [0.6, 0.05, 0.15, 0.1, 0.05, 0.03, 0.01, 0.01]

    if application_info and 'status' in application_info:
        app_status = application_info['status']

        # Convert to standard format using the mapping (case-insensitive)
        if isinstance(app_status, str):
            app_status_normalized = app_status.lower()
            app_status = application_status_mapping.get(app_status_normalized, app_status)

        if app_status == "approved" and loan_info:
            action_taken = "1"  # Loan originated
        elif app_status == "approved" and not loan_info:
            action_taken = "2"  # Application approved but not accepted
        elif app_status == "denied":
            action_taken = "3"  # Application denied
        elif app_status == "withdrawn":
            action_taken = "4"  # Application withdrawn by applicant
        elif app_status == "incomplete":
            action_taken = "5"  # File closed for incompleteness
        else:
            action_taken = random.choices(list(action_taken_options.keys()), weights=action_weights, k=1)[0]
    else:
        action_taken = random.choices(list(action_taken_options.keys()), weights=action_weights, k=1)[0]

    # Generate action taken date
    today = datetime.date.today()
    if application_info and 'submission_date' in application_info and application_info['submission_date']:
        submission_date = application_info['submission_date'].date() if hasattr(application_info['submission_date'],
                                                                                'date') else application_info[
            'submission_date']
        # Action typically taken 1-45 days after submission
        days_after_submission = random.randint(1, 45)
        action_taken_date = submission_date + datetime.timedelta(days=days_after_submission)
        # Ensure action date isn't in the future
        action_taken_date = min(action_taken_date, today)
    else:
        # Default to a recent date if no submission date available
        days_ago = random.randint(1, 180)
        action_taken_date = today - datetime.timedelta(days=days_ago)

    # Generate location info (state, county, census tract)
    states = ["CA", "TX", "FL", "NY", "PA", "IL", "OH", "GA", "NC", "MI", "NJ", "VA", "WA", "AZ", "MA"]
    state = random.choice(states)

    # Generate a plausible county code (FIPS code)
    county = f"{random.randint(1, 199):03d}"

    # Generate a plausible census tract (format: XXXX.XX)
    tract_base = random.randint(1, 9999)
    tract_suffix = random.randint(0, 99)
    census_tract = f"{tract_base:04d}.{tract_suffix:02d}"

    # Generate rate spread (difference between APR and average prime offer rate)
    if action_taken == "1":  # Only for originated loans
        rate_spread = round(random.uniform(-0.5, 3.0), 3)
        if rate_spread < 0:
            rate_spread = None  # Only report positive spreads
    else:
        rate_spread = None

    # Most loans are not high-cost
    hoepa_weights = [0.01, 0.94, 0.05]
    hoepa_status = random.choices([1, 2, 3], weights=hoepa_weights, k=1)[0]

    lien_weights = [0.75, 0.2, 0.03, 0.02]
    lien_status = random.choices([1, 2, 3, 4], weights=lien_weights, k=1)[0]

    # Generate credit score for applicant
    if application_info and 'estimated_credit_score' in application_info and application_info['estimated_credit_score']:
        credit_score_applicant = application_info['estimated_credit_score']
    else:
        # Generate a realistic credit score distribution
        score_ranges = [
            (300, 579, 0.1),  # Poor: 10%
            (580, 669, 0.2),  # Fair: 20%
            (670, 739, 0.25),  # Good: 25%
            (740, 799, 0.35),  # Very Good: 35%
            (800, 850, 0.1)  # Excellent: 10%
        ]

        # Select a range based on the distribution
        range_selection = random.random()
        cumulative_prob = 0
        selected_range = None

        for score_min, score_max, probability in score_ranges:
            cumulative_prob += probability
            if range_selection <= cumulative_prob:
                selected_range = (score_min, score_max)
                break

        # Generate a score within the selected range
        credit_score_applicant = random.randint(selected_range[0], selected_range[1])

    # Generate credit score for co-applicant (if applicable)
    if random.random() < 0.3:  # 30% chance of having a co-applicant
        # Generate a score that's somewhat correlated with the primary applicant
        base_score = max(300, min(850, credit_score_applicant + random.randint(-50, 50)))
        credit_score_co_applicant = base_score
    else:
        credit_score_co_applicant = None

    # Generate credit score model
    credit_score_models = {
        "1": "Equifax Beacon 5.0",
        "2": "Experian Fair Isaac",
        "3": "FICO Risk Score Classic 04",
        "4": "FICO Risk Score Classic 98",
        "5": "VantageScore 2.0",
        "6": "VantageScore 3.0",
        "7": "More than one credit scoring model",
        "8": "Other credit scoring model",
        "9": "Not applicable"
    }

    credit_score_model = random.choices(list(credit_score_models.keys()),
                                        weights=[0.2, 0.2, 0.2, 0.1, 0.1, 0.1, 0.05, 0.03, 0.02],
                                        k=1)[0]

    # Generate denial reasons if application was denied
    denial_reasons = [
        "1",  # Debt-to-income ratio
        "2",  # Employment history
        "3",  # Credit history
        "4",  # Collateral
        "5",  # Insufficient cash
        "6",  # Unverifiable information
        "7",  # Credit application incomplete
        "8",  # Mortgage insurance denied
        "9",  # Other
        "10"  # Not applicable
    ]

    if action_taken == "3":  # Application denied
        # Select 1-3 denial reasons
        num_reasons = random.choices([1, 2, 3], weights=[0.5, 0.3, 0.2], k=1)[0]
        all_reasons = random.sample(denial_reasons[:-1], k=num_reasons)  # Exclude "Not applicable"

        denial_reason1 = all_reasons[0] if len(all_reasons) > 0 else None
        denial_reason2 = all_reasons[1] if len(all_reasons) > 1 else None
        denial_reason3 = all_reasons[2] if len(all_reasons) > 2 else None
        denial_reason4 = None
    else:
        denial_reason1 = "10"  # Not applicable
        denial_reason2 = None
        denial_reason3 = None
        denial_reason4 = None

    # Generate loan costs and terms for originated loans
    if action_taken == "1":  # Loan originated
        # Generate loan costs as a percentage of loan amount
        total_loan_costs_pct = random.uniform(0.01, 0.05)  # 1-5% of loan amount
        total_loan_costs = round(loan_amount * total_loan_costs_pct, 2)

        # Generate points and fees as a percentage of loan amount
        points_fees_pct = random.uniform(0.005, 0.02)  # 0.5-2% of loan amount
        total_points_and_fees = round(loan_amount * points_fees_pct, 2)

        # Generate origination charges as a percentage of loan amount
        origination_pct = random.uniform(0.005, 0.015)  # 0.5-1.5% of loan amount
        origination_charges = round(loan_amount * origination_pct, 2)

        # Generate discount points (often zero, sometimes up to 2%)
        if random.random() < 0.7:  # 70% chance of having discount points
            discount_points = round(loan_amount * random.uniform(0.005, 0.02), 2)
        else:
            discount_points = 0

        # Generate lender credits (often zero, sometimes up to 1%)
        if random.random() < 0.3:  # 30% chance of having lender credits
            lender_credits = round(loan_amount * random.uniform(0.002, 0.01), 2)
        else:
            lender_credits = 0

        # Generate loan term
        loan_term_options = [180, 240, 360]  # 15, 20, or 30 years
        loan_term_weights = [0.1, 0.1, 0.8]  # 30 years is most common
        loan_term = random.choices(loan_term_options, weights=loan_term_weights, k=1)[0]

        # Generate introductory rate period (if applicable)
        if random.random() < 0.2:  # 20% chance of having an intro rate
            intro_rate_options = [12, 36, 60, 84, 120]  # 1, 3, 5, 7, or 10 years
            intro_rate_period = random.choice(intro_rate_options)
        else:
            intro_rate_period = 0  # No intro rate
    else:
        # If loan not originated, these fields are not applicable
        total_loan_costs = None
        total_points_and_fees = None
        origination_charges = None
        discount_points = None
        lender_credits = None
        loan_term = None
        intro_rate_period = None

    # Generate non-amortizing features
    balloon_payment = random.choices(["1", "2"], weights=[0.05, 0.95], k=1)[0]  # 1=Yes, 2=No
    interest_only_payment = random.choices(["1", "2"], weights=[0.03, 0.97], k=1)[0]  # 1=Yes, 2=No
    negative_amortization = random.choices(["1", "2"], weights=[0.01, 0.99], k=1)[0]  # 1=Yes, 2=No
    other_non_amortizing_features = random.choices(["1", "2"], weights=[0.02, 0.98], k=1)[0]  # 1=Yes, 2=No

    # Generate property value
    if application_info and 'estimated_property_value' in application_info and application_info[
        'estimated_property_value']:
        property_value = application_info['estimated_property_value']
    else:
        # Assume loan-to-value ratio between 70% and 95%
        ltv = random.uniform(0.7, 0.95)
        property_value = round(loan_amount / ltv, 2)

    # Generate manufactured home information
    if construction_method == "2":  # Manufactured home
        manufactured_home_secured_property_types = {
            "1": "Manufactured home and land",
            "2": "Manufactured home and not land",
            "3": "Not applicable"
        }
        manufactured_home_land_property_interests = {
            "1": "Direct ownership",
            "2": "Indirect ownership",
            "3": "Paid leasehold",
            "4": "Unpaid leasehold",
            "5": "Not applicable"
        }

        manufactured_home_secured_property_type = random.choices(list(manufactured_home_secured_property_types.keys()),
                                                                 weights=[0.6, 0.3, 0.1], k=1)[0]

        manufactured_home_land_property_interest = \
            random.choices(list(manufactured_home_land_property_interests.keys()),
                           weights=[0.4, 0.1, 0.2, 0.2, 0.1], k=1)[0]
    else:
        manufactured_home_secured_property_type = "3"  # Not applicable
        manufactured_home_land_property_interest = "5"  # Not applicable

    # Generate total units
    total_units_options = [1, 2, 3, 4]
    total_units_weights = [0.9, 0.05, 0.03, 0.02]  # Single-family is most common
    total_units = random.choices(total_units_options, weights=total_units_weights, k=1)[0]

    # Generate multifamily affordable units (only relevant for 5+ unit properties)
    multifamily_affordable_units = None  # Not applicable for 1-4 unit properties

    # Generate application submission details
    submission_of_application = random.choices(["1", "2", "3"], weights=[0.7, 0.2, 0.1], k=1)[0]
    # 1=Submitted directly to institution, 2=Not submitted directly, 3=Not applicable

    initially_payable_to_institution = random.choices(["1", "2", "3"], weights=[0.8, 0.15, 0.05], k=1)[0]
    # 1=Initially payable to institution, 2=Not initially payable to institution, 3=Not applicable

    # Generate automated underwriting system (AUS) information
    aus_options = {
        "1": "Desktop Underwriter (DU)",
        "2": "Loan Prospector (LP) or Loan Product Advisor",
        "3": "Technology Open to Approved Lenders (TOTAL) Scorecard",
        "4": "Guaranteed Underwriting System (GUS)",
        "5": "Other",
        "6": "Not applicable"
    }

    # Select primary AUS
    aus1 = random.choices(list(aus_options.keys()), weights=[0.4, 0.3, 0.1, 0.05, 0.05, 0.1], k=1)[0]

    # Some applications use multiple systems
    if aus1 != "6" and random.random() < 0.2:  # 20% chance of using a second AUS
        remaining_aus = [k for k in aus_options.keys() if k != aus1 and k != "6"]
        aus2 = random.choice(remaining_aus)

        if random.random() < 0.1:  # 10% chance of using a third AUS
            remaining_aus = [k for k in remaining_aus if k != aus2]
            aus3 = random.choice(remaining_aus)
        else:
            aus3 = None
    else:
        aus2 = None
        aus3 = None

    aus4 = None
    aus5 = None

    # Generate reverse mortgage, open-end line of credit, and business purpose flags
    reverse_mortgage = random.choices(["1", "2"], weights=[0.02, 0.98], k=1)[0]  # 1=Yes, 2=No
    open_end_line_of_credit = random.choices(["1", "2"], weights=[0.05, 0.95], k=1)[0]  # 1=Yes, 2=No
    business_or_commercial_purpose = random.choices(["1", "2"], weights=[0.03, 0.97], k=1)[0]  # 1=Yes, 2=No

    # Generate HMDA submission status
    submission_status = "pending"

    # Generate dates for submission tracking
    last_modified_date = datetime.datetime.now()

    # Generate edit status
    edit_status = "not_started"

    # Create the HMDA record
    hmda_record = {
        "reporting_year": reporting_year,
        "lei": lei,
        "loan_purpose": loan_purpose,
        "preapproval": preapproval,
        "construction_method": construction_method,
        "occupancy_type": occupancy_type,
        "loan_amount": float(loan_amount),
        "action_taken": action_taken,
        "action_taken_date": action_taken_date,
        "state": state,
        "county": county,
        "census_tract": census_tract,
        "rate_spread": float(rate_spread) if rate_spread is not None else None,
        "hoepa_status": hoepa_status,
        "lien_status": lien_status,
        "credit_score_applicant": credit_score_applicant,
        "credit_score_co_applicant": credit_score_co_applicant,
        "credit_score_model": credit_score_model,
        "denial_reason1": denial_reason1,
        "denial_reason2": denial_reason2,
        "denial_reason3": denial_reason3,
        "denial_reason4": denial_reason4,
        "total_loan_costs": float(total_loan_costs) if total_loan_costs is not None else None,
        "total_points_and_fees": float(total_points_and_fees) if total_points_and_fees is not None else None,
        "origination_charges": float(origination_charges) if origination_charges is not None else None,
        "discount_points": float(discount_points) if discount_points is not None else None,
        "lender_credits": float(lender_credits) if lender_credits is not None else None,
        "loan_term": loan_term,
        "intro_rate_period": intro_rate_period,
        "balloon_payment": balloon_payment,
        "interest_only_payment": interest_only_payment,
        "negative_amortization": negative_amortization,
        "other_non_amortizing_features": other_non_amortizing_features,
        "property_value": float(property_value),
        "manufactured_home_secured_property_type": manufactured_home_secured_property_type,
        "manufactured_home_land_property_interest": manufactured_home_land_property_interest,
        "total_units": total_units,
        "multifamily_affordable_units": multifamily_affordable_units,
        "submission_of_application": submission_of_application,
        "initially_payable_to_institution": initially_payable_to_institution,
        "aus1": aus1,
        "aus2": aus2,
        "aus3": aus3,
        "aus4": aus4,
        "aus5": aus5,
        "reverse_mortgage": reverse_mortgage,
        "open_end_line_of_credit": open_end_line_of_credit,
        "business_or_commercial_purpose": business_or_commercial_purpose,
        "submission_status": submission_status,
        "last_modified_date": last_modified_date,
        "edit_status": edit_status
    }

    return hmda_record


def get_application_info(application_id: Optional[int], conn) -> Optional[Dict[str, Any]]:
    """
    Get application information to make HMDA record data reasonable.

    Args:
        application_id: The ID of the application
        conn: PostgreSQL connection object

    Returns:
        Dictionary containing application information or None if application_id is None or not found
    """
    if not application_id:
        return None

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                application_type, 
                status, 
                submission_date_time, 
                requested_loan_amount, 
                estimated_property_value,
                estimated_credit_score
            FROM mortgage_services.applications 
            WHERE mortgage_services_application_id = %s
        """, (application_id,))

        result = cursor.fetchone()
        cursor.close()

        return result

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching application information: {error}")
        return None


def get_loan_info(loan_id: Optional[int], conn) -> Optional[Dict[str, Any]]:
    """
    Get loan information to make HMDA record data reasonable.

    Args:
        loan_id: The ID of the loan
        conn: PostgreSQL connection object

    Returns:
        Dictionary containing loan information or None if loan_id is None or not found
    """
    if not loan_id:
        return None

    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT loan_amount, interest_rate
            FROM mortgage_services.loans 
            WHERE mortgage_services_loan_id = %s
        """, (loan_id,))

        result = cursor.fetchone()
        cursor.close()

        return result

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching loan information: {error}")
        return None
