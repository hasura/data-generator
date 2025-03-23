import datetime
import logging
import random
from typing import Any, Dict

import psycopg2

from data_generator import DataGenerator
from fsi_data_generator.fsi_generators.helpers.generate_unique_json_array import \
    generate_unique_json_array

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
        report_info = get_report_info(report_id, dg.conn)

    # Generate reporting year (current or previous year)
    reporting_year = report_info.get("reporting_year")
    if not reporting_year:
        current_year = datetime.datetime.now().year
        reporting_year = random.choice([current_year, current_year - 1])

    # Generate reporting period
    reporting_periods = {
        "annual": 0.7,  # 70% chance
        "quarterly_q1": 0.1,  # 10% chance
        "quarterly_q2": 0.1,  # 10% chance
        "quarterly_q3": 0.05,  # 5% chance
        "quarterly_q4": 0.05  # 5% chance
    }
    reporting_period = random.choices(
        list(reporting_periods.keys()),
        weights=list(reporting_periods.values()),
        k=1
    )[0]

    # Generate institution LEI (Legal Entity Identifier)
    institution_lei = report_info.get("institution_lei")
    if not institution_lei:
        institution_lei = generate_random_lei()

    # Generate submission date (within the past year)
    days_ago = random.randint(1, 365)
    submission_date = datetime.datetime.now() - datetime.timedelta(days=days_ago)

    # Generate submission status with realistic distribution
    submission_statuses = {
        "pending": 0.15,  # 15% chance
        "in progress": 0.15,  # 15% chance
        "submitted": 0.20,  # 20% chance
        "accepted": 0.40,  # 40% chance
        "rejected": 0.10  # 10% chance
    }
    submission_status = random.choices(
        list(submission_statuses.keys()),
        weights=list(submission_statuses.values()),
        k=1
    )[0]

    # Generate submission method
    submission_methods = {
        "portal": 0.6,  # 60% chance
        "api": 0.3,  # 30% chance
        "mail": 0.05,  # 5% chance
        "email": 0.05  # 5% chance
    }
    submission_method = random.choices(
        list(submission_methods.keys()),
        weights=list(submission_methods.values()),
        k=1
    )[0]

    # Generate confirmation number if submitted
    confirmation_number = None
    if submission_status in ["submitted", "accepted"]:
        confirmation_number = f"HMDA-{reporting_year}-{random.randint(100000, 999999)}"

    # Generate submitted_by (associate ID)
    submitted_by = generate_associate_id(dg)

    # Generate submission file path
    submission_file_path = None
    if submission_status != "pending":
        file_name = f"hmda_submission_{reporting_year}_{reporting_period}_{random.randint(1000, 9999)}.dat"
        submission_file_path = f"/data/hmda_submissions/{reporting_year}/{file_name}"

    # Generate response date and status for submissions
    response_date = None
    response_status = None
    response_details = None

    if submission_status in ["accepted", "rejected"]:
        # Response typically 1-14 days after submission
        response_days = random.randint(1, 14)
        response_date = submission_date + datetime.timedelta(days=response_days)

        if submission_status == "accepted":
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

        elif submission_status == "rejected":
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

    # Create the HMDA submission record
    hmda_submission = {
        "mortgage_services_report_id": report_id,
        "reporting_year": reporting_year,
        "reporting_period": reporting_period,
        "institution_lei": institution_lei,
        "submission_date": submission_date,
        "submission_method": submission_method,
        "confirmation_number": confirmation_number,
        "submitted_by": submitted_by,
        "submission_file_path": submission_file_path,
        "response_date": response_date,
        "response_status": response_status,
        "response_details": response_details,
        "submission_status": submission_status
    }

    # Print debug information
    # logger.debug(
    #     f"Generated HMDA Submission - Year: {reporting_year}, Period: {reporting_period}, Status: {submission_status}")

    return hmda_submission


def get_report_info(report_id: int, conn) -> Dict[str, Any]:
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
            reporting_year = result[0]
            if not reporting_year and result[1]:
                reporting_year = result[1].year

            # Generate LEI based on regulatory agency
            regulatory_agency = result[3] if result[3] else "CFPB"
            institution_lei = generate_agency_based_lei(regulatory_agency)

            return {
                "reporting_year": reporting_year,
                "period_start_date": result[1],
                "period_end_date": result[2],
                "regulatory_agency": regulatory_agency,
                "institution_lei": institution_lei
            }
        else:
            return {}

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching report information: {error}")
        return {}


def generate_random_lei():
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


def generate_agency_based_lei(agency: str):
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


def generate_associate_id(dg: DataGenerator):
    """
    Get a valid associate ID from the database or generate a plausible one.

    Args:
        dg: DataGenerator instance

    Returns:
        An associate ID
    """
    try:
        cursor = dg.conn.cursor()

        # Try to get a random associate ID from the database
        cursor.execute("""
            SELECT enterprise_associate_id 
            FROM enterprise.associates 
            ORDER BY RANDOM() 
            LIMIT 1
        """)

        result = cursor.fetchone()
        cursor.close()

        if result and result[0]:
            return result[0]
    except Exception as e:
        logger.error(f"Warning: Couldn't fetch associate ID: {e}")

    # Fallback to random ID
    return random.randint(1, 500)
