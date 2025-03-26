import datetime
import logging
import random
from typing import Any, Dict

import psycopg2

from data_generator import DataGenerator
from fsi_data_generator.fsi_generators.helpers.generate_unique_json_array import \
    generate_unique_json_array

from .enums import (HmdaReportingPeriod, HmdaSubmissionStatus,
                    HmdaSubmissionStatusDetail)

logger = logging.getLogger(__name__)


def generate_random_hmda_submission(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random HMDA submission record with realistic values.

    Args:
        id_fields: Dictionary containing the required ID fields (mortgage_services_report_id)
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated HMDA submission data
    """
    # Extract the report ID from the id_fields dictionary if present
    report_id = id_fields.get("mortgage_services_report_id")

    # Get report information if available
    report_info = {}
    if report_id:
        report_info = _get_report_info(report_id, dg.conn)

    # Generate reporting year (current or previous year)
    reporting_year = report_info.get("reporting_year")
    if not reporting_year:
        current_year = datetime.datetime.now().year
        reporting_year = random.choice([current_year, current_year - 1])

    reporting_period = HmdaReportingPeriod.get_random()

    # Generate institution LEI (Legal Entity Identifier)
    institution_lei = report_info.get("institution_lei")
    if not institution_lei:
        institution_lei = _generate_random_lei()

    # Generate submission date (within the past year)
    days_ago = random.randint(1, 365)
    submission_date = datetime.datetime.now() - datetime.timedelta(days=days_ago)

    submission_status = HmdaSubmissionStatus.get_random()

    # Generate detailed submission status based on the main status using HmdaSubmissionStatusDetail enum
    detailed_status = None
    if submission_status == HmdaSubmissionStatus.PENDING:
        detailed_status = random.choice([
            HmdaSubmissionStatusDetail.NO_DATA_UPLOADED,
            HmdaSubmissionStatusDetail.UPLOAD_IN_PROGRESS
        ])
    elif submission_status == HmdaSubmissionStatus.SUBMITTED:
        detailed_status = random.choice([
            HmdaSubmissionStatusDetail.VALIDATED_WITH_VERIFICATION_NEEDED,
            HmdaSubmissionStatusDetail.VALIDATED_READY_FOR_VERIFICATION,
            HmdaSubmissionStatusDetail.VERIFICATION_IN_PROGRESS,
            HmdaSubmissionStatusDetail.MACRO_EDITS_NEED_REVIEW,
            HmdaSubmissionStatusDetail.READY_FOR_SUBMISSION
        ])
    elif submission_status == HmdaSubmissionStatus.ACCEPTED:
        detailed_status = HmdaSubmissionStatusDetail.SUBMISSION_ACCEPTED
    else:
        detailed_status = random.choice([
            HmdaSubmissionStatusDetail.PARSED_WITH_ERRORS,
            HmdaSubmissionStatusDetail.VALIDATION_ERRORS,
            HmdaSubmissionStatusDetail.VALIDATION_ERRORS_REQUIRE_CORRECTION
        ])

    # Generate confirmation number if submitted
    confirmation_number = None
    if submission_status in [HmdaSubmissionStatus.SUBMITTED, HmdaSubmissionStatus.ACCEPTED]:
        confirmation_number = f"HMDA-{reporting_year}-{random.randint(100000, 999999)}"

    # Generate submission file path
    submission_file_path = None
    if submission_status != HmdaSubmissionStatus.PENDING:
        file_name = f"hmda_submission_{reporting_year}_{reporting_period.value}_{random.randint(1000, 9999)}.dat"
        submission_file_path = f"/data/hmda_submissions/{reporting_year}/{file_name}"

    # Generate response date and status for submissions
    response_date = None
    response_status = None
    response_details = None

    if submission_status in [HmdaSubmissionStatus.ACCEPTED, HmdaSubmissionStatus.REJECTED]:
        # Response typically 1-14 days after submission
        response_days = random.randint(1, 14)
        response_date = submission_date + datetime.timedelta(days=response_days)

        if submission_status == HmdaSubmissionStatus.ACCEPTED:
            response_status = "accepted"

            # Start with hardcoded acceptance messages
            acceptance_messages = [
                "Submission accepted. All validation tests passed.",
                "Filing accepted with no validation errors.",
                "Submission complete - no further action required.",
                "Data quality and format verification complete. Filing accepted.",
                "Accepted with automated compliance checks completed."
            ]

            # Try to add AI-generated messages
            try:
                ai_acceptance_details = generate_unique_json_array(
                    dbml_string=dg.dbml,
                    fully_qualified_column_name='HMDA Submission Acceptance Notes',
                    count=15,
                    cache_key='hmda_acceptance_notes'
                )
                if ai_acceptance_details and len(ai_acceptance_details) > 0:
                    # Combine both lists
                    acceptance_messages.extend(ai_acceptance_details)
            except Exception as e:
                logger.error(f"Warning: Couldn't generate HMDA acceptance details: {e}")
                # Continue with just the hardcoded messages

            # Choose a random message
            response_details = random.choice(acceptance_messages)

        elif submission_status == HmdaSubmissionStatus.REJECTED:
            response_status = "rejected"

            # Start with hardcoded rejection messages
            rejection_messages = [
                "Submission rejected due to 12 validity edits that must be corrected.",
                "Multiple required fields missing. See attached report for details.",
                "Filing rejected due to format issues. Data does not conform to specifications.",
                "Syntactical errors found in 8 records. Correction required.",
                "Validation failed: Inconsistent LEI information across filing."
            ]

            # Try to add AI-generated messages
            try:
                ai_rejection_details = generate_unique_json_array(
                    dbml_string=dg.dbml,
                    fully_qualified_column_name='HMDA Submission Rejection Notes',
                    count=15,
                    cache_key='hmda_rejection_notes'
                )
                if ai_rejection_details and len(ai_rejection_details) > 0:
                    # Combine both lists
                    rejection_messages.extend(ai_rejection_details)
            except Exception as e:
                logger.error(f"Warning: Couldn't generate HMDA rejection details: {e}")
                # Continue with just the hardcoded messages

            # Choose a random message
            response_details = random.choice(rejection_messages)

    # Extract just the filename from the path, or generate a new one if needed
    file_name = None
    if submission_status != HmdaSubmissionStatus.PENDING:
        file_name = f"hmda_submission_{reporting_year}_{reporting_period.value}_{random.randint(1000, 9999)}.dat"

    # Create the HMDA submission record
    hmda_submission = {
        # We don't include mortgage_services_submission_id as it's auto-incremented
        "reporting_year": reporting_year,
        "reporting_period": reporting_period.value,
        "institution_lei": institution_lei,
        "submission_date": submission_date,
        "submission_status": detailed_status.value,
        "file_name": file_name if submission_status != HmdaSubmissionStatus.PENDING else None,
        "file_size": random.randint(1000, 10000000) if submission_status != HmdaSubmissionStatus.PENDING else None,
        "record_count": random.randint(100, 10000) if submission_status != HmdaSubmissionStatus.PENDING else None,
        "error_count": random.randint(0, 100) if submission_status == HmdaSubmissionStatus.REJECTED else 0,
        "warning_count": random.randint(0, 50) if submission_status != HmdaSubmissionStatus.PENDING else 0,
        "submitted_by_id": random.randint(1000, 9999),  # Reference to enterprise associate
        "submission_notes": response_details,  # Using the response details as notes
        "confirmation_number": confirmation_number,
        "completion_date": response_date if submission_status == HmdaSubmissionStatus.ACCEPTED else None
    }

    return hmda_submission


def _get_report_info(report_id: int, conn) -> Dict[str, Any]:
    """
    Get report information to make submission data reasonable.

    Args:
        report_id: The ID of the HMDA report
        conn: PostgreSQL connection object

    Returns:
        Dictionary containing report information or empty dict if not found
    """
    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                reporting_year,
                period_start_date,
                period_end_date,
                regulatory_agency
            FROM mortgage_services.regulatory_reports 
            WHERE mortgage_services_report_id = %s
        """, (report_id,))

        result = cursor.fetchone()
        cursor.close()

        if result:
            # Check if there's a valid year, otherwise use period start date
            reporting_year = result.get('reporting_year')
            if not reporting_year and result.get('period_start_date'):
                reporting_year = result.get('period_start_date').year

            # Generate LEI based on regulatory agency
            regulatory_agency = result.get('regulatory_agency', "CFPB")
            institution_lei = _generate_agency_based_lei(regulatory_agency)

            return {
                **result,
                "reporting_year": reporting_year,
                "regulatory_agency": regulatory_agency,
                "institution_lei": institution_lei
            }
        else:
            return {}

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching report information: {error}")
        return {}


def _generate_random_lei():
    """
    Generate a realistic Legal Entity Identifier (LEI).

    Returns:
        A 20-character LEI string
    """
    # LEIs are 20 characters:
    # - First 4 characters: prefix identifying the Local Operating Unit (LOU)
    # - Characters 5-18: entity-specific part
    # - Last 2 characters: checksum digits

    # Common LOU prefixes (simplified)
    lou_prefixes = ["5493", "2138", "9695", "2549", "5299"]

    # Generate random entity-specific part (14 alphanumeric characters)
    entity_chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    entity_part = ''.join(random.choice(entity_chars) for _ in range(14))

    # Simplified checksum (in reality, LEIs use a complex algorithm)
    checksum = f"{random.randint(0, 9)}{random.randint(0, 9)}"

    # Combine parts
    return f"{random.choice(lou_prefixes)}{entity_part}{checksum}"


def _generate_agency_based_lei(agency: str):
    """
    Generate an LEI with prefix that might be associated with a regulatory agency.

    Args:
        agency: Regulatory agency name

    Returns:
        A 20-character LEI string with agency-appropriate prefix
    """
    # Map agencies to plausible LOU prefixes (fictional mapping)
    agency_prefixes = {
        "FDIC": "5493",
        "Federal Reserve": "2138",
        "OCC": "9695",
        "CFPB": "5299",
        "NCUA": "2549"
    }

    # Get prefix or use random one
    lou_prefix = agency_prefixes.get(agency)
    if not lou_prefix:
        lou_prefix = random.choice(list(agency_prefixes.values()))

    # Generate entity part and checksum
    entity_chars = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    entity_part = ''.join(random.choice(entity_chars) for _ in range(14))
    checksum = f"{random.randint(0, 9)}{random.randint(0, 9)}"

    return f"{lou_prefix}{entity_part}{checksum}"
