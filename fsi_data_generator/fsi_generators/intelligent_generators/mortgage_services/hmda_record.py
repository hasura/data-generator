from .enums import (ApplicationStatus, ApplicationType, HmdaActionTaken,
                    HmdaAus, HmdaBalloonPayment,
                    HmdaBusinessOrCommercialPurpose, HmdaConstructionMethod,
                    HmdaCreditScoreModel, HmdaDenialReason, HmdaHoepaStatus,
                    HmdaInterestOnly, HmdaLienStatus, HmdaLoanPurpose,
                    HmdaManufacturedHomeType,
                    HmdaManufacturedLandPropertyInterest,
                    HmdaNegativeAmortization, HmdaOccupancyType,
                    HmdaOpenEndLineOfCredit, HmdaOtherNonAmortizing,
                    HmdaPreapproval, HmdaRecordEditStatus, HmdaReverseMortgage,
                    HmdaSubmissionMethod, HmdaSubmissionStatus, OccupancyType)
from data_generator import DataGenerator, SkipRowGenerationError
from datetime import timezone
from fsi_data_generator.fsi_generators.helpers import parse_address
from typing import Any, Dict, Optional, Tuple

import datetime
import logging
import psycopg2
import random
import string

logger = logging.getLogger(__name__)


def generate_random_hmda_record(id_fields: Dict, dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random mortgage services HMDA record with reasonable values.

    Args:
        id_fields: Dictionary containing the required ID fields
        dg: DataGenerator object

    Returns:
        Dictionary containing randomly generated HMDA record data
    """
    # Get application and loan information
    conn = dg.conn
    application_id, application_info = _get_valid_hmda_application(conn)
    loan_info = None
    property_info = None

    # Fetch loan and property information
    if "mortgage_services_loan_id" in id_fields:
        loan_info = _get_loan_info(id_fields.get("mortgage_services_loan_id"), conn)

        # Fetch associated property if loan exists
        if loan_info:
            property_info = _get_property_info(application_id, conn)

    # Validate input data
    if not (loan_info and property_info and _validate_hmda_details(loan_info, application_info)):
        logger.warning("Invalid or insufficient data for HMDA record generation")
        raise SkipRowGenerationError

    # Define reporting year
    reporting_year = datetime.date.today().year

    # Determine loan purpose based on application or loan type
    if application_info and 'application_type' in application_info:
        app_type = ApplicationType(application_info['application_type'])
        loan_purpose_mapping = {
            ApplicationType.PURCHASE: HmdaLoanPurpose.HOME_PURCHASE,
            ApplicationType.REFINANCE: HmdaLoanPurpose.REFINANCING,
            ApplicationType.CASH_OUT: HmdaLoanPurpose.CASH_OUT_REFINANCING,
            ApplicationType.HOME_IMPROVEMENT: HmdaLoanPurpose.HOME_IMPROVEMENT,
            ApplicationType.CONSTRUCTION: HmdaLoanPurpose.HOME_PURCHASE,
            ApplicationType.RENOVATION: HmdaLoanPurpose.HOME_IMPROVEMENT,
            ApplicationType.REVERSE_MORTGAGE: HmdaLoanPurpose.REVERSE_MORTGAGE,
            ApplicationType.JUMBO: HmdaLoanPurpose.HOME_PURCHASE,
            ApplicationType.LAND: HmdaLoanPurpose.HOME_PURCHASE,
            ApplicationType.OTHER: HmdaLoanPurpose.OTHER_PURPOSE
        }
        loan_purpose = loan_purpose_mapping.get(app_type, HmdaLoanPurpose.get_random())
    else:
        loan_purpose = HmdaLoanPurpose.get_random()

    # Generate LEI with more realistic generation
    lei = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))

    # Derive construction method from property
    construction_method = (
        HmdaConstructionMethod.MANUFACTURED_HOME
        if property_info.get('is_manufactured_home', False)
        else HmdaConstructionMethod.SITE_BUILT
    )

    # Mapping between property occupancy type and HMDA occupancy type
    occupancy_type_mapping = {
        OccupancyType.PRIMARY_RESIDENCE: HmdaOccupancyType.PRINCIPAL_RESIDENCE,
        OccupancyType.SECONDARY_RESIDENCE: HmdaOccupancyType.SECOND_RESIDENCE,
        OccupancyType.INVESTMENT: HmdaOccupancyType.INVESTMENT_PROPERTY,
        OccupancyType.NOT_APPLICABLE: HmdaOccupancyType.PRINCIPAL_RESIDENCE  # Default fallback
    }

    occupancy_type = occupancy_type_mapping.get(
        OccupancyType(property_info.get('occupancy_type', OccupancyType.PRIMARY_RESIDENCE)),
        HmdaOccupancyType.PRINCIPAL_RESIDENCE
    )

    # Action taken determination
    action_taken_mapping = {
        ApplicationStatus.APPROVED: HmdaActionTaken.LOAN_ORIGINATED,
        ApplicationStatus.CONDITIONAL_APPROVAL: HmdaActionTaken.LOAN_ORIGINATED,
        ApplicationStatus.DENIED: HmdaActionTaken.APPLICATION_DENIED,
        ApplicationStatus.WITHDRAWN: HmdaActionTaken.APPLICATION_WITHDRAWN,
        ApplicationStatus.DRAFT: HmdaActionTaken.FILE_CLOSED_FOR_INCOMPLETENESS,
        ApplicationStatus.SUBMITTED: HmdaActionTaken.APPLICATION_APPROVED_BUT_NOT_ACCEPTED,
        ApplicationStatus.IN_REVIEW: HmdaActionTaken.APPLICATION_APPROVED_BUT_NOT_ACCEPTED,
        ApplicationStatus.ADDITIONAL_INFO_REQUIRED: HmdaActionTaken.FILE_CLOSED_FOR_INCOMPLETENESS,
        ApplicationStatus.EXPIRED: HmdaActionTaken.FILE_CLOSED_FOR_INCOMPLETENESS,
        ApplicationStatus.SUSPENDED: HmdaActionTaken.FILE_CLOSED_FOR_INCOMPLETENESS
    }
    action_taken = action_taken_mapping.get(
        ApplicationStatus(application_info.get('status', 'DRAFT')),
        HmdaActionTaken.get_random()
    )

    # Calculate rate spread
    rate_spread = _calculate_rate_spread(
        loan_info.get('interest_rate', 0),
        reporting_year
    )

    # Determine loan amount
    loan_amount = loan_info.get('loan_amount', 0)

    address_components = parse_address(property_info.get('address', ''))

    # Generate denial reasons if application was denied
    denial_reasons = []
    if action_taken == HmdaActionTaken.APPLICATION_DENIED:
        # Add 1-4 random denial reason
        num_reasons = random.randint(1, 4)
        for _ in range(num_reasons):
            denial_reasons.append(HmdaDenialReason.get_random().value)

    # Fill with None to ensure we have all 4 slots
    denial_reasons.extend([None] * (4 - len(denial_reasons)))

    # Generate random but sensible loan term (common mortgage terms)
    loan_term = random.choice([180, 240, 360])  # 15, 20, or 30 years in months

    # Generate other loan details based on property and loan information
    total_loan_costs = round(loan_amount * random.uniform(0.02, 0.05), 2)  # 2-5% of loan amount
    total_points_and_fees = round(loan_amount * random.uniform(0.01, 0.03), 2)  # 1-3% of loan amount
    origination_charges = round(loan_amount * random.uniform(0.005, 0.02), 2)  # 0.5-2% of loan amount
    discount_points = round(loan_amount * random.uniform(0, 0.01), 2)  # 0-1% of loan amount
    lender_credits = round(loan_amount * random.uniform(0, 0.01),
                           2) if random.random() < 0.3 else None  # 30% chance of lender credits

    # Determine if there's an introductory rate period (for ARMs)
    intro_rate_period = random.choice(
        [None, 12, 36, 60, 84]) if random.random() < 0.2 else None  # 20% chance of ARM with intro period

    # Generate appropriate values for manufactured homes
    manufactured_home_secured_property_type = HmdaManufacturedHomeType.NOT_APPLICABLE
    manufactured_home_land_property_interest = HmdaManufacturedLandPropertyInterest.NOT_APPLICABLE
    if construction_method == HmdaConstructionMethod.MANUFACTURED_HOME:
        manufactured_home_secured_property_type = HmdaManufacturedHomeType.get_random().value
        manufactured_home_land_property_interest = HmdaManufacturedLandPropertyInterest.get_random().value

    # Generate property units info
    total_units = random.choices([1, 2, 3, 4, 5, 6, 8, 10, 12],
                                 weights=[70, 10, 5, 5, 2, 2, 2, 2, 2])[0]  # Weighted to favor single-family

    multifamily_affordable_units = None
    if total_units > 4:  # Only applicable for multifamily
        multifamily_affordable_units = random.randint(0, total_units)

    # Generate AUS (Automated Underwriting System) information
    aus_systems = [HmdaAus.get_random().value]
    # Small chance of having multiple AUS systems
    if random.random() < 0.2:
        aus_systems.append(HmdaAus.get_random().value)
    if random.random() < 0.1:
        aus_systems.append(HmdaAus.get_random().value)

    # Fill with None to ensure we have all 5 slots
    aus_systems.extend([None] * (5 - len(aus_systems)))

    # Application submission method
    submission_method = HmdaSubmissionMethod.get_random()

    # Determine if initially payable to institution
    initially_payable = bool(random.getrandbits(1))

    # Special loan types
    reverse_mortgage = HmdaReverseMortgage.get_random()
    open_end_line_of_credit = HmdaOpenEndLineOfCredit.get_random()
    business_or_commercial_purpose = HmdaBusinessOrCommercialPurpose.get_random()

    # Non-amortizing features
    balloon_payment = HmdaBalloonPayment.get_random()
    interest_only_payment = HmdaInterestOnly.get_random()
    negative_amortization = HmdaNegativeAmortization.get_random()
    other_non_amortizing = HmdaOtherNonAmortizing.get_random()

    # HMDA record creation
    hmda_record = {
        "mortgage_services_application_id": application_id,
        "reporting_year": reporting_year,
        "lei": lei,
        "loan_purpose": loan_purpose.value,
        "preapproval": HmdaPreapproval.get_random().value,
        "construction_method": construction_method.value,
        "occupancy_type": occupancy_type.value,
        "loan_amount": loan_amount,
        "action_taken": action_taken.value,
        "action_taken_date": datetime.date.today(),

        # Location details from property
        "state": address_components.get('state', random.choice(["CA", "TX", "FL", "NY", "PA"])),
        "county": address_components.get('county', f"{random.randint(1, 199):03d}"),
        "census_tract": address_components.get('census_tract',
                                               f"{random.randint(1, 9999):04d}.{random.randint(0, 99):02d}"),

        # Rate and financial metrics
        "rate_spread": rate_spread,
        "property_value": property_info.get('estimated_property_value', loan_amount * 1.2),

        # Additional HMDA-specific details
        "hoepa_status": HmdaHoepaStatus.get_random().value,
        "lien_status": HmdaLienStatus.get_random().value,
        "credit_score_applicant": application_info.get('estimated_credit_score', random.randint(300, 850)),
        "credit_score_model": HmdaCreditScoreModel.get_random().value,

        # Denial reasons if applicable
        "denial_reason1": denial_reasons[0] if denial_reasons[0] else HmdaDenialReason.NOT_APPLICABLE.value,
        "denial_reason2": denial_reasons[1],
        "denial_reason3": denial_reasons[2],
        "denial_reason4": denial_reasons[3],

        # Financial details
        "total_loan_costs": total_loan_costs,
        "total_points_and_fees": total_points_and_fees,
        "origination_charges": origination_charges,
        "discount_points": discount_points,
        "lender_credits": lender_credits,
        "loan_term": loan_term,
        "intro_rate_period": intro_rate_period,

        # Non-amortizing features
        "balloon_payment": balloon_payment.value,
        "interest_only_payment": interest_only_payment.value,
        "negative_amortization": negative_amortization.value,
        "other_non_amortizing_features": other_non_amortizing.value,

        # Property details
        "manufactured_home_secured_property_type": manufactured_home_secured_property_type.value,
        "manufactured_home_land_property_interest": manufactured_home_land_property_interest.value,
        "total_units": total_units,
        "multifamily_affordable_units": multifamily_affordable_units,

        # Application details
        "submission_of_application": submission_method.value,
        "initially_payable_to_institution": initially_payable,

        # AUS (Automated Underwriting System) information
        "aus1": aus_systems[0],
        "aus2": aus_systems[1],
        "aus3": aus_systems[2],
        "aus4": aus_systems[3],
        "aus5": aus_systems[4],

        # Special loan types
        "reverse_mortgage": reverse_mortgage.value,
        "open_end_line_of_credit": open_end_line_of_credit.value,
        "business_or_commercial_purpose": business_or_commercial_purpose.value,

        # Timestamps and status
        "last_modified_date": datetime.datetime.now(timezone.utc),
        "submission_status": HmdaSubmissionStatus.PENDING.value,
        "edit_status": HmdaRecordEditStatus.NOT_STARTED.value
    }

    return hmda_record


def _get_average_prime_offer_rate(reporting_year: int) -> float:
    """
    Retrieve or estimate the Average Prime Offer Rate (APOR) for a given year.
    In a production system, this would be fetched from a financial data source.

    Args:
        reporting_year (int): Year for which APOR is being determined

    Returns:
        float: Estimated APOR for the given year
    """
    # Placeholder implementation with some historical context
    # These are example/fictional rates and should be replaced with actual data
    apor_rates = {
        2020: 3.75,
        2021: 3.25,
        2022: 5.50,
        2023: 6.75,
        2024: 6.50
    }

    return apor_rates.get(reporting_year, 4.50)


def _calculate_rate_spread(interest_rate: float, reporting_year: int) -> Optional[float]:
    """
    Calculate the rate spread based on the loan's interest rate and APOR.

    Args:
        interest_rate (float): Actual loan interest rate
        reporting_year (int): Year of reporting

    Returns:
        Optional[float]: Rate spread, or None if not applicable
    """
    try:
        apor = _get_average_prime_offer_rate(reporting_year)
        rate_spread = round(interest_rate - apor, 3)
        return rate_spread if rate_spread > 0 else None
    except Exception as e:
        logger.warning(f"Error calculating rate spread: {e}")
        return None


def _validate_hmda_details(loan_info: Dict[str, Any], application_info: Dict[str, Any]) -> bool:
    """
    Validate consistency of HMDA-related details.

    Args:
        loan_info (Dict[str, Any]): Loan information
        application_info (Dict[str, Any]): Property information

    Returns:
        bool: Whether the details pass basic validation
    """
    validations = [
        # Ensure loan amount is reasonable compared to property value
        loan_info.get('loan_amount', 0) <= (application_info.get('estimated_property_value', 0) * 1.1),

        # Ensure loan term is within reasonable bounds
        30 <= loan_info.get('loan_term_months', 0) <= 360,

        # Validate interest rate
        0 < loan_info.get('interest_rate', 0) < 20,

        # Ensure positive loan amount
        loan_info.get('loan_amount', 0) > 0
    ]

    return all(validations)


def _get_application_info(application_id: Optional[int], conn) -> Optional[Dict[str, Any]]:
    """
    Get application information to support HMDA record generation.

    Args:
        application_id: The ID of the application
        conn: PostgreSQL connection object

    Returns:
        Dictionary containing application information or None if not found
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
                estimated_credit_score,
                estimated_property_value
            FROM mortgage_services.applications 
            WHERE mortgage_services_application_id = %s
        """, (application_id,))

        result = cursor.fetchone()
        cursor.close()
        return result

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching application information: {error}")
        return None


def _get_loan_info(loan_id: Optional[int], conn) -> Optional[Dict[str, Any]]:
    """
    Get loan information to support HMDA record generation.

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
            SELECT 
                loan_amount, 
                interest_rate, 
                loan_term_months
            FROM mortgage_services.loans 
            WHERE mortgage_services_loan_id = %s
        """, (loan_id,))

        result = cursor.fetchone()
        cursor.close()

        return result

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching loan information: {error}")
        return None


def _get_property_info(application_id: Optional[int], conn) -> Optional[Dict[str, Any]]:
    """
    Get property information to support HMDA record generation directly from the application.

    Args:
        application_id: The ID of the application
        conn: PostgreSQL connection object

    Returns:
        Dictionary containing property information or None if not found
    """
    if not application_id:
        return None

    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT 
                address,
                occupancy_type,
                is_new_construction
            FROM mortgage_services.properties 
            WHERE mortgage_services_application_id = %s
        """, (application_id,))

        result = cursor.fetchone()
        cursor.close()
        return result

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching property information: {error}")
        return None


# Global set to track used application IDs
used_hmda_applications = set()


def _get_valid_hmda_application(conn) -> Tuple[int, Dict]:
    """
    Get a valid application ID for HMDA record generation.

    Args:
        conn: Database connection

    Returns:
        Tuple of (application_id, application_info)

    Raises:
        SkipRowGenerationError: If no suitable application is found
    """
    global used_hmda_applications

    # List of application statuses that are reportable for HMDA
    reportable_statuses = [
        ApplicationStatus.APPROVED.value,
        ApplicationStatus.CONDITIONAL_APPROVAL.value,
        ApplicationStatus.DENIED.value,
        ApplicationStatus.WITHDRAWN.value,
        ApplicationStatus.EXPIRED.value
    ]

    # Find a valid application that hasn't been used yet in our global set
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT a.mortgage_services_application_id 
            FROM mortgage_services.applications a
            LEFT JOIN mortgage_services.hmda_records h 
                ON a.mortgage_services_application_id = h.mortgage_services_application_id
            WHERE a.status IN %s
            AND h.mortgage_services_application_id IS NULL
            ORDER BY a.mortgage_services_application_id
        """, (tuple(reportable_statuses),))

        results = cursor.fetchall()
        cursor.close()

        if not results:
            raise SkipRowGenerationError("No reportable applications available for HMDA record generation")

        # Find the first application ID that's not in our used set
        application_id = None
        for result in results:
            candidate_id = result.get('mortgage_services_application_id')
            if candidate_id not in used_hmda_applications:
                application_id = candidate_id
                break

        # If all applications have been used, raise an error
        if application_id is None:
            raise SkipRowGenerationError("All available applications have already been used in this session")

        # Add the chosen ID to our used set
        used_hmda_applications.add(application_id)

        # Get the application details
        application_info = _get_application_info(application_id, conn)

        if not application_info:
            raise SkipRowGenerationError(f"Could not retrieve details for application {application_id}")

        return application_id, application_info

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error finding reportable application: {error}")
        raise SkipRowGenerationError("Error searching for reportable applications")
