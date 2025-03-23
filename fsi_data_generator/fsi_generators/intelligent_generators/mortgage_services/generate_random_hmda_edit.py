import datetime
import logging
import random
from typing import Any, Dict, Optional

import psycopg2

from data_generator import DataGenerator
from fsi_data_generator.fsi_generators.helpers.generate_unique_json_array import \
    generate_unique_json_array

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
    hmda_record_info = get_hmda_record_info(hmda_record_id, conn)

    # Define edit types with their weights
    edit_types = {
        "syntactical": 0.2,  # 20% chance
        "validity": 0.3,  # 30% chance
        "quality": 0.4,  # 40% chance
        "macro": 0.1  # 10% chance
    }

    edit_type = random.choices(list(edit_types.keys()), weights=list(edit_types.values()), k=1)[0]

    # Generate realistic edit codes based on the type
    edit_code = generate_edit_code(edit_type)

    # Generate edit description based on type and code
    edit_description = generate_edit_description(edit_type, edit_code, hmda_record_info, dg)

    # Define possible statuses with their weights
    statuses = {
        "open": 0.5,  # 50% chance
        "verified": 0.3,  # 30% chance
        "corrected": 0.2  # 20% chance
    }

    status = random.choices(list(statuses.keys()), weights=list(statuses.values()), k=1)[0]

    # Generate created date (usually within the last 30 days)
    days_ago = random.randint(0, 30)
    created_date = datetime.datetime.now() - datetime.timedelta(days=days_ago)

    # Generate resolved info if status is not open
    resolved_date = None
    resolved_by = None
    resolution_notes = None

    if status in ["verified", "corrected"]:
        # Resolution date is after creation but before now
        max_resolution_days = min(days_ago, 7)  # Usually resolved within 7 days
        if max_resolution_days > 0:
            days_after_creation = random.randint(1, max_resolution_days)
            resolved_date = created_date + datetime.timedelta(days=days_after_creation)
        else:
            resolved_date = created_date + datetime.timedelta(hours=random.randint(1, 24))

        # Generate a random associate ID between 1 and 100
        resolved_by = str(random.randint(1, 100))

        # Generate resolution notes
        resolution_notes = generate_resolution_notes(status, edit_type, edit_code, dg)

    # Print debug information
    # logger.debug(f"Generated HMDA edit - Type: {edit_type}, Code: {edit_code}, Status: {status}")

    # Create the HMDA edit record
    hmda_edit = {
        "mortgage_services_hmda_record_id": hmda_record_id,
        "edit_code": edit_code,
        "edit_type": edit_type,
        "edit_description": edit_description,
        "status": status,
        "created_date": created_date,
        "resolved_date": resolved_date,
        "resolved_by": resolved_by,
        "resolution_notes": resolution_notes
    }

    return hmda_edit


def get_hmda_record_info(hmda_record_id: int, conn) -> Optional[Dict[str, Any]]:
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

        if result:
            return {
                "reporting_year": result[0],
                "loan_amount": float(result[1]) if result[1] is not None else None,
                "action_taken": result[2],
                "census_tract": result[3],
                "rate_spread": float(result[4]) if result[4] is not None else None,
                "credit_score_applicant": result[5],
                "property_value": float(result[6]) if result[6] is not None else None,
                "loan_purpose": result[7]
            }
        else:
            # If record not found, return empty dict rather than None to prevent errors
            return {}

    except (Exception, psycopg2.Error) as error:
        logger.error(f"Error fetching HMDA record information: {error}")
        return {}  # Return empty dict rather than None


def generate_edit_code(edit_type: str) -> str:
    """
    Generate a realistic edit code based on the edit type.

    Args:
        edit_type: The type of the edit (syntactical, validity, quality, macro)

    Returns:
        A realistic edit code string
    """
    if edit_type == "syntactical":
        # Syntactical edit codes typically start with S and are followed by a number
        return f"S{random.randint(1, 999):03d}"
    elif edit_type == "validity":
        # Validity edit codes typically start with V and are followed by a number
        return f"V{random.randint(1, 999):03d}"
    elif edit_type == "quality":
        # Quality edit codes typically start with Q and are followed by a number
        return f"Q{random.randint(1, 999):03d}"
    elif edit_type == "macro":
        # Macro edit codes typically start with M and are followed by a number
        return f"M{random.randint(1, 999):03d}"
    else:
        # Default case
        return f"E{random.randint(1, 999):03d}"


def generate_edit_description(edit_type: str, edit_code: str, hmda_info: Optional[Dict[str, Any]],
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
    if edit_type == "syntactical":
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
    elif edit_type == "validity":
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
    elif edit_type == "quality":
        quality_messages = [
            f"The loan amount ({hmda_info.get('loan_amount', 'N/A')}) to property value ({hmda_info.get('property_value', 'N/A')}) ratio exceeds normal thresholds.",
            f"The reported debt-to-income ratio is unusually high.",
            f"The reported credit score ({hmda_info.get('credit_score_applicant', 'N/A')}) is unusually low for an approved loan.",
            f"The property value of {hmda_info.get('property_value', 'N/A')} is unusually low for this census tract.",
            f"This record reports an unusual rate spread of {hmda_info.get('rate_spread', 'N/A')} that may warrant verification."
        ]
        return random.choice(quality_messages)

    # Macro errors relate to patterns across multiple records
    elif edit_type == "macro":
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


def generate_resolution_notes(status: str, _edit_type: str, edit_code: str, dg: DataGenerator) -> str:
    """
    Generate realistic resolution notes based on status and edit type.

    Args:
        status: The status of the edit (verified, corrected)
        _edit_type: The type of the edit
        edit_code: The edit code
        dg: DataGenerator instance

    Returns:
        Resolution notes text
    """
    if status == "verified":
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

    elif status == "corrected":
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

    else:
        return ""
