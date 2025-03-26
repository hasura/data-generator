import datetime
import logging
import random
from typing import Any, Dict, Optional

import psycopg2

from data_generator import DataGenerator
from fsi_data_generator.fsi_generators.helpers.generate_unique_json_array import \
    generate_unique_json_array

from .enums import HmdaEditStatus, HmdaEditType

logger = logging.getLogger(__name__)


def generate_random_hmda_edit(ids_dict, dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random HMDA edit record with realistic values based on HMDA record ID.

    Args:
        ids_dict: The ID of the HMDA record this edit relates to
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated HMDA edit data
    """
    # Get HMDA record information to make edit data reasonable
    conn = dg.conn
    hmda_record_id = ids_dict["mortgage_services_hmda_record_id"]
    hmda_record_info = _get_hmda_record_info(hmda_record_id, conn)

    # Define edit types with their weights
    edit_type_weights = [0.2, 0.3, 0.4, 0.1]  # SYNTACTICAL, VALIDITY, QUALITY, MACRO

    # Use get_random from HmdaEditType with weights
    edit_type = HmdaEditType.get_random(weights=edit_type_weights)

    # Generate realistic edit codes based on the type
    edit_code = _generate_edit_code(edit_type.value)

    # Generate edit description based on type and code
    edit_description = _generate_edit_description(edit_type.value, edit_code, hmda_record_info, dg)

    status = HmdaEditStatus.get_random()

    # Generate dates that are tied to the HMDA record's timeline
    # Get reporting year from the HMDA record
    reporting_year = hmda_record_info.get('reporting_year')
    if not reporting_year:
        # Default to previous year if not found
        reporting_year = datetime.datetime.now().year - 1

    # Convert to integer if it's a string
    if isinstance(reporting_year, str):
        try:
            reporting_year = int(reporting_year)
        except (ValueError, TypeError):
            reporting_year = datetime.datetime.now().year - 1

    # HMDA submissions typically happen in early months of the following year
    # For records from the previous year, edits usually occur Jan-Mar of current year
    current_year = datetime.datetime.now().year
    if reporting_year == current_year - 1:
        # Generate date in Jan-Mar of current year for previous year's data
        month = random.randint(1, 3)  # Jan-Mar
        day = random.randint(1, 28)  # Safe for all months
        created_date = datetime.datetime(current_year, month, day)
    else:
        # For older records, generate date around March of the year following reporting_year
        month = random.randint(2, 4)  # Feb-Apr
        day = random.randint(1, 28)  # Safe for all months
        # Make sure we don't create future dates
        year = min(reporting_year + 1, current_year)
        created_date = datetime.datetime(year, month, day)

    # Generate resolved info if status is not OPEN
    resolved_date = None
    resolved_by_id = ids_dict.get('resolved_by_id')
    resolution_notes = None

    if status in [HmdaEditStatus.CORRECTED, HmdaEditStatus.VERIFIED, HmdaEditStatus.WAIVED]:
        # Resolution typically happens within 1-7 days of identification for HMDA edits
        days_after_creation = random.randint(1, 7)
        resolved_date = created_date + datetime.timedelta(days=days_after_creation)

        # Make sure resolved_date is not in the future
        if resolved_date > datetime.datetime.now():
            resolved_date = datetime.datetime.now() - datetime.timedelta(days=random.randint(1, 3))

        # Generate resolution notes
        resolution_notes = _generate_resolution_notes(status.value, edit_type.value, edit_code, dg)
    else:
        resolved_by_id = None

    # Create the HMDA edit record
    hmda_edit = {
        "mortgage_services_hmda_record_id": hmda_record_id,
        "edit_code": edit_code,
        "edit_type": edit_type.value,
        "edit_description": edit_description,
        "status": status.value,
        "created_date": created_date,
        "resolved_date": resolved_date,
        "resolved_by_id": resolved_by_id,
        "resolution_notes": resolution_notes
    }

    return hmda_edit


def _get_hmda_record_info(hmda_record_id: int, conn) -> Optional[Dict[str, Any]]:
    """
    Get HMDA record information to make edit data reasonable.

    Args:
        hmda_record_id: The ID of the HMDA record
        conn: PostgreSQL connection object

    Returns:
        Dictionary containing HMDA record information or None if not found
    """
    try:
        cursor = conn.cursor()

        cursor.execute("""
            SELECT 
                reporting_year,
                loan_amount,
                action_taken,
                census_tract,
                rate_spread,
                credit_score_applicant,
                property_value,
                loan_purpose
            FROM mortgage_services.hmda_records 
            WHERE mortgage_services_hmda_record_id = %s
        """, (hmda_record_id,))

        result = cursor.fetchone()
        cursor.close()
        return result or {}

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching HMDA record information: {error}")
        return {}  # Return empty dict rather than None


def _generate_edit_code(edit_type: str) -> str:
    """
    Generate a realistic edit code based on the edit type.

    Args:
        edit_type: The type of the edit (SYNTACTICAL, VALIDITY, QUALITY, MACRO)

    Returns:
        A realistic edit code string
    """
    if edit_type == "SYNTACTICAL":
        # Syntactical edit codes typically start with S and are followed by a number
        return f"S{random.randint(1, 999):03d}"
    elif edit_type == "VALIDITY":
        # Validity edit codes typically start with V and are followed by a number
        return f"V{random.randint(1, 999):03d}"
    elif edit_type == "QUALITY":
        # Quality edit codes typically start with Q and are followed by a number
        return f"Q{random.randint(1, 499):03d}"
    elif edit_type == "MACRO":
        # Macro quality edit codes also start with Q but typically have higher numbers
        return f"Q{random.randint(500, 999):03d}"
    else:
        # Default case
        return f"E{random.randint(1, 999):03d}"


def _generate_edit_description(edit_type: str, edit_code: str, hmda_info: Optional[Dict[str, Any]],
                               dg: DataGenerator) -> str:
    """
    Generate a realistic edit description based on the type, code, and HMDA record info.

    Args:
        edit_type: The type of the edit
        edit_code: The edit code
        hmda_info: Information about the HMDA record
        dg: DataGenerator instance

    Returns:
        A descriptive edit message
    """
    # Ensure hmda_info is a dict even if None was passed
    if hmda_info is None:
        hmda_info = {}

    # Common field names in HMDA records
    fields = [
        "loan_amount", "action_taken", "loan_purpose", "property_value",
        "rate_spread", "census_tract", "credit_score_applicant"
    ]

    # Syntactical errors relate to formatting and identification issues
    if edit_type == "SYNTACTICAL":
        try:
            alt_syntactical_messages = generate_unique_json_array(dbml_string=dg.dbml,
                                                                  fully_qualified_column_name='description of a syntactical HMDA error',
                                                                  count=50, cache_key='syntactical_hmda_edit_error')
        except Exception as e:
            logger.error(f"Warning: Couldn't generate alt_syntactical_messages: {e}")
            alt_syntactical_messages = []
        syntactical_messages = [
                                   f"The LEI in this record does not match a valid institution LEI.",
                                   f"The {random.choice(fields)} field contains an invalid format.",
                                   f"This record has an invalid recordID format.",
                                   f"The census tract format in this record is invalid.",
                                   f"This record contains an invalid application date format.",
                                   f"The reporting year in this record does not match the submission period."
                               ] + alt_syntactical_messages
        return random.choice(syntactical_messages)

    # Validity errors relate to invalid values or combinations
    elif edit_type == "VALIDITY":
        try:
            alt_validity_messages = generate_unique_json_array(dbml_string=dg.dbml,
                                                               fully_qualified_column_name='description of a validity HMDA error',
                                                               count=50, cache_key='validity_hmda_edit_error')
        except Exception as e:
            logger.error(f"Warning: Couldn't generate alt_syntactical_messages: {e}")
            alt_validity_messages = []
        validity_messages = [
                                f"The {random.choice(fields)} value is outside the valid range.",
                                f"An invalid value was reported for {random.choice(fields)}.",
                                f"Action taken reported as {hmda_info.get('action_taken', 'N/A')} is incompatible with loan purpose reported as {hmda_info.get('loan_purpose', 'N/A')}.",
                                f"Census tract {hmda_info.get('census_tract', 'N/A')} is not a valid census tract for the reported state.",
                                f"Rate spread of {hmda_info.get('rate_spread', 'N/A')} cannot be reported for this type of loan."
                            ] + alt_validity_messages
        return random.choice(validity_messages)

    # Quality errors indicate unusual but not necessarily incorrect values
    elif edit_type == "QUALITY":
        quality_messages = [
            f"The loan amount ({hmda_info.get('loan_amount', 'N/A')}) to property value ({hmda_info.get('property_value', 'N/A')}) ratio exceeds normal thresholds.",
            f"The reported debt-to-income ratio is unusually high.",
            f"The reported credit score ({hmda_info.get('credit_score_applicant', 'N/A')}) is unusually low for an approved loan.",
            f"The property value of {hmda_info.get('property_value', 'N/A')} is unusually low for this census tract.",
            f"This record reports an unusual rate spread of {hmda_info.get('rate_spread', 'N/A')} that may warrant verification."
        ]
        return random.choice(quality_messages)

    # Macro errors relate to patterns across multiple records
    elif edit_type == "MACRO":
        macro_messages = [
            f"The percentage of loans with action taken as {hmda_info.get('action_taken', 'N/A')} is significantly higher than industry averages.",
            f"The institution's denial rate for this reporting period differs significantly from prior years.",
            f"The percentage of loans with rate spreads exceeding 3% is unusually high.",
            f"The racial distribution of loan approvals differs significantly from demographic distributions in the lending area.",
            f"The institution's share of loans in low-income census tracts is significantly below the MSA average."
        ]
        return random.choice(macro_messages)

    # Default case
    else:
        return f"Edit {edit_code} requires review of the {random.choice(fields)} field."


def _generate_resolution_notes(status: str, _edit_type: str, edit_code: str, dg: DataGenerator) -> str:
    """
    Generate realistic resolution notes based on status and edit type.

    Args:
        status: The status of the edit (VERIFIED, CORRECTED, WAIVED)
        _edit_type: The type of the edit
        edit_code: The edit code
        dg: DataGenerator instance

    Returns:
        Resolution notes text
    """
    if status == "VERIFIED":
        # Try to get custom notes from DataGenerator, but handle possible failure
        try:
            alt_verified_notes = generate_unique_json_array(dbml_string=dg.dbml,
                                                            fully_qualified_column_name='Notes for a verified HMDA edit',
                                                            count=50, cache_key='verified_hmda_edit_notes')
        except Exception as e:
            logger.error(f"Warning: Couldn't generate unique notes: {e}")
            alt_verified_notes = []
        verified_notes = [
                             f"Verified that the reported value is correct despite triggering {edit_code}.",
                             f"Confirmed with originator that the unusual value is accurate.",
                             f"Documentation from the borrower supports the reported value.",
                             f"Special circumstances explain this apparent discrepancy.",
                             f"Verified through additional review that this exception is legitimate."
                         ] + alt_verified_notes
        return random.choice(verified_notes)

    elif status == "CORRECTED":
        # Try to get custom notes from DataGenerator, but handle possible failure
        try:
            alt_corrected_notes = generate_unique_json_array(dbml_string=dg.dbml,
                                                             fully_qualified_column_name='Notes for a corrected HMDA edit',
                                                             count=50, cache_key='corrected_hmda_edit_notes')
        except Exception as e:
            logger.error(f"Warning: Couldn't generate unique notes: {e}")
            alt_corrected_notes = []
        corrected_notes = [
                              f"Updated the incorrect value to resolve {edit_code}.",
                              f"Data entry error corrected to comply with reporting requirements.",
                              f"Updated field format to match HMDA requirements.",
                              f"Corrected the inconsistency between related fields.",
                              f"Recalculated and corrected the value based on loan documentation."
                          ] + alt_corrected_notes
        return random.choice(corrected_notes)

    elif status == "WAIVED":
        waived_notes = [
            f"Edit {edit_code} waived per regulatory exception guidance.",
            f"Waived by supervisory approval due to special circumstances.",
            f"Regulatory exemption applied to this reporting requirement.",
            f"Waived based on written documentation from regulatory agency.",
            f"Exception granted per institutional policy for this specific case."
        ]
        return random.choice(waived_notes)

    else:
        return ""
