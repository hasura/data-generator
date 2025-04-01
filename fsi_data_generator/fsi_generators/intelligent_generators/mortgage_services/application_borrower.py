from .enums import BorrowerType, RelationshipType
from data_generator import DataGenerator
from fsi_data_generator.fsi_generators.intelligent_generators.enterprise.enums import \
    PartyRelationshipType

import random


def generate_random_application_borrower(ids_dict, dg: DataGenerator):
    """
    Generate a realistic random mortgage_services.application_borrowers record.
    Adjusts contribution percentages of existing records if needed to maintain
    proper totals but does not perform the insert of the new record.

    Parameters:
    conn: PostgreSQL database connection
    ids_dict (dict): Dictionary containing ID references.
                     Expected keys:
                     - 'mortgage_services_application_id': ID of the related application
                     - 'mortgage_services_borrower_id': ID of the related borrower

    Returns:
    dict: An application_borrowers record with realistic data
    """
    # Extract IDs
    conn = dg.conn
    application_id = ids_dict.get('mortgage_services_application_id')
    borrower_id = ids_dict.get('mortgage_services_borrower_id')

    if not application_id or not borrower_id:
        raise ValueError("Must provide both application_id and borrower_id")

    cursor = conn.cursor()

    try:
        # First check if this borrower is already associated with the application
        cursor.execute("""
            SELECT * FROM mortgage_services.application_borrowers
            WHERE mortgage_services_application_id = %s AND mortgage_services_borrower_id = %s
        """, (application_id, borrower_id))

        existing_record = cursor.fetchone()
        if existing_record:
            # If the record already exists, just return it without changes
            return {
                "mortgage_services_application_borrower_id": existing_record.get(
                    'mortgage_services_application_borrower_id'),
                "mortgage_services_application_id": application_id,
                "mortgage_services_borrower_id": borrower_id,
                "borrower_type": existing_record.get('borrower_type'),
                "relationship_to_primary": existing_record.get('relationship_to_primary'),
                "contribution_percentage": float(existing_record.get('contribution_percentage'))
            }

        # Get all existing borrowers for this application
        cursor.execute("""
            SELECT * FROM mortgage_services.application_borrowers
            WHERE mortgage_services_application_id = %s
        """, (application_id,))

        existing_borrowers = cursor.fetchall() or []

        # Get current borrower information
        cursor.execute("""
            SELECT b.*, p.* 
            FROM mortgage_services.borrowers b
            JOIN enterprise.parties p ON b.enterprise_party_id = p.enterprise_party_id
            WHERE b.mortgage_services_borrower_id = %s
        """, (borrower_id,))

        current_borrower_info = cursor.fetchone() or {}

        # Determine if this is the first borrower record for this application
        is_first_record = len(existing_borrowers) == 0

        # For the first record, it's simple - this is the primary borrower
        if is_first_record:
            borrower_type = BorrowerType.PRIMARY
            relationship_to_primary = None
            contribution_percentage = 100.00
        else:
            # Find the primary borrower record
            primary_borrower = None
            for b in existing_borrowers:
                if b.get('borrower_type') == BorrowerType.PRIMARY.value:
                    primary_borrower = b
                    break

            if not primary_borrower:
                # This should never happen in well-formed data, but just in case
                raise ValueError("No primary borrower found for application")

            # Get primary borrower details
            cursor.execute("""
                SELECT b.*, p.* 
                FROM mortgage_services.borrowers b
                JOIN enterprise.parties p ON b.enterprise_party_id = p.enterprise_party_id
                WHERE b.mortgage_services_borrower_id = %s
            """, (primary_borrower.get('mortgage_services_borrower_id'),))

            primary_borrower_info = cursor.fetchone() or {}

            # Determine the appropriate contribution percentage
            # Start with a base percentage based on the relationship
            base_contribution = _determine_base_contribution(
                conn,
                current_borrower_info,
                primary_borrower_info
            )

            # Get the current primary borrower's contribution
            primary_contribution = primary_borrower.get('contribution_percentage', 0)

            # Make sure we don't exceed 100% total and leave the primary with a reasonable amount
            # Primary should keep at least 10% contribution
            max_available = primary_contribution - 10.00

            # Cap the contribution at what's available from the primary
            contribution_percentage = min(base_contribution, max_available)

            # Ensure contribution is reasonable (min 0.01%)
            contribution_percentage = max(contribution_percentage, 0.01)

            # Determine relationship to primary borrower
            formal_relationship = _get_formal_relationship(
                conn,
                current_borrower_info.get('enterprise_party_id'),
                primary_borrower_info.get('enterprise_party_id')
            )

            if formal_relationship == PartyRelationshipType.SPOUSE:
                relationship_to_primary = RelationshipType.SPOUSE
            elif formal_relationship == PartyRelationshipType.SIBLING:
                relationship_to_primary = RelationshipType.SIBLING
            elif formal_relationship == PartyRelationshipType.DEPENDENT:
                relationship_to_primary = RelationshipType.CHILD
            elif formal_relationship == PartyRelationshipType.BUSINESS_PARTNER:
                relationship_to_primary = RelationshipType.BUSINESS_PARTNER
            else:
                relationship_to_primary = None

            # Set relationship_to_primary based on formal relationship or inference
            if relationship_to_primary and formal_relationship:

                # Determine borrower type based on the formal relationship
                if formal_relationship == PartyRelationshipType.SPOUSE:
                    borrower_type = random.choices(
                        [BorrowerType.CO_BORROWER, BorrowerType.COSIGNER],
                        weights=[0.95, 0.05]
                    )[0]
                elif formal_relationship in [PartyRelationshipType.POWER_OF_ATTORNEY, PartyRelationshipType.GUARDIAN,
                                             PartyRelationshipType.TRUSTEE]:
                    borrower_type = random.choices(
                        [BorrowerType.CO_BORROWER, BorrowerType.COSIGNER],
                        weights=[0.7, 0.3]
                    )[0]
                elif formal_relationship in [PartyRelationshipType.BENEFICIARY, PartyRelationshipType.AUTHORIZED_USER]:
                    borrower_type = random.choices(
                        [BorrowerType.CO_BORROWER, BorrowerType.COSIGNER],
                        weights=[0.2, 0.8]
                    )[0]
                else:  # administrator, executor, or other formal relationships
                    borrower_type = random.choices(
                        [BorrowerType.CO_BORROWER, BorrowerType.COSIGNER],
                        weights=[0.4, 0.6]
                    )[0]
            else:
                # No formal relationship exists, so we need to infer a personal relationship
                personal_relationship = _infer_personal_relationship(current_borrower_info, primary_borrower_info)
                relationship_to_primary = personal_relationship

                # Determine borrower type based on inferred personal relationship
                if personal_relationship == RelationshipType.SPOUSE:
                    borrower_type = random.choices(
                        [BorrowerType.CO_BORROWER, BorrowerType.COSIGNER],
                        weights=[0.9, 0.1]
                    )[0]
                elif personal_relationship in [RelationshipType.PARENT, RelationshipType.CHILD]:
                    borrower_type = random.choices(
                        [BorrowerType.CO_BORROWER, BorrowerType.COSIGNER],
                        weights=[0.3, 0.7]
                    )[0]
                else:  # sibling, friend, other
                    borrower_type = random.choices(
                        [BorrowerType.CO_BORROWER, BorrowerType.COSIGNER],
                        weights=[0.4, 0.6]
                    )[0]

            # If this is a co-signer, reduce the contribution percentage
            if borrower_type == BorrowerType.COSIGNER:
                contribution_percentage = contribution_percentage * 0.5
                contribution_percentage = round(contribution_percentage, 2)

            # Update the primary borrower's contribution percentage in the database
            # Only if this is not a simulation (indicated by having an actual connection)
            if conn is not None:
                # Start a transaction
                # conn.autocommit = False
                try:
                    new_primary_contribution = primary_contribution - contribution_percentage

                    cursor.execute("""
                        UPDATE mortgage_services.application_borrowers
                        SET contribution_percentage = %s
                        WHERE mortgage_services_application_borrower_id = %s
                    """, (new_primary_contribution, primary_borrower.get('mortgage_services_application_borrower_id')))

                except Exception as e:
                    raise e

        # Create the application_borrowers record (but don't insert it - that's handled by the parent)
        record = {
            "borrower_type": borrower_type.value,
            "relationship_to_primary": relationship_to_primary.value if relationship_to_primary else RelationshipType.OTHER.value,
            "contribution_percentage": float(contribution_percentage)
        }

        return record

    finally:
        # Close cursor
        cursor.close()


def _determine_base_contribution(conn, borrower_info, primary_info) -> float:
    """
    Determine a base contribution percentage based on the relationship
    between the borrower and primary borrower.

    Parameters:
    conn: PostgreSQL database connection
    borrower_info: Dict with borrower information
    primary_info: Dict with primary borrower information

    Returns:
    float: Base contribution percentage
    """
    # Get formal relationship if it exists
    formal_relationship = _get_formal_relationship(
        conn,
        borrower_info.get('enterprise_party_id'),
        primary_info.get('enterprise_party_id')
    )

    if formal_relationship:
        formal_relationship = PartyRelationshipType(formal_relationship)

    # Determine base contribution based on relationship
    if formal_relationship == PartyRelationshipType.SPOUSE:
        # Spouses typically have higher contributions
        return round(random.uniform(35.0, 50.0), 2)

    elif formal_relationship in [PartyRelationshipType.POWER_OF_ATTORNEY, PartyRelationshipType.GUARDIAN,
                                 PartyRelationshipType.TRUSTEE]:
        return round(random.uniform(20.0, 40.0), 2)

    elif formal_relationship in [PartyRelationshipType.BENEFICIARY, PartyRelationshipType.AUTHORIZED_USER]:
        return round(random.uniform(5.0, 20.0), 2)

    else:
        # No formal relationship - infer personal relationship
        personal_relationship = _infer_personal_relationship(borrower_info, primary_info)

        if personal_relationship == RelationshipType.SPOUSE:
            return round(random.uniform(30.0, 45.0), 2)

        elif personal_relationship in [RelationshipType.PARENT, RelationshipType.CHILD]:
            return round(random.uniform(10.0, 30.0), 2)

        else:  # sibling, friend, other
            return round(random.uniform(5.0, 25.0), 2)


def _get_formal_relationship(conn, party_id1, party_id2):
    """
    Get the formal relationship between two parties from the database.

    Parameters:
    conn: PostgreSQL database connection
    party_id1: First party ID
    party_id2: Second party ID

    Returns:
    str or None: The relationship type if found, otherwise None
    """
    if not party_id1 or not party_id2:
        return None

    cursor = conn.cursor()

    try:
        cursor.execute("""
            SELECT relationship_type 
            FROM enterprise.party_relationships
            WHERE (enterprise_party_id = %s AND related_party_id = %s)
               OR (enterprise_party_id = %s AND related_party_id = %s)
        """, (party_id1, party_id2, party_id2, party_id1))

        relationship_record = cursor.fetchone()
        if relationship_record and relationship_record.get('relationship_type'):
            return relationship_record.get('relationship_type')

        return None
    finally:
        cursor.close()


def _infer_personal_relationship(borrower_info, primary_info):
    """
    Infer the personal relationship between borrowers based on available information.
    This is separate from formal legal relationships in party_relationships.

    Parameters:
    borrower_info: Dict with borrower/party information
    primary_info: Dict with primary borrower/party information

    Returns:
    str: Inferred personal relationship (spouse, parent, child, etc.)
    """
    if not borrower_info or not primary_info:
        return RelationshipType.get_random()

    # Get age differences
    borrower_age = _get_age_from_info(borrower_info)
    primary_age = _get_age_from_info(primary_info)

    # Check if they have the same last name
    same_last_name = False
    borrower_last_name = borrower_info.get('last_name', '').lower()
    primary_last_name = primary_info.get('last_name', '').lower()
    if borrower_last_name and primary_last_name and borrower_last_name == primary_last_name:
        same_last_name = True

    # Check marital status
    borrower_marital = borrower_info.get('marital_status', '').lower()
    primary_marital = primary_info.get('marital_status', '').lower()
    both_married = borrower_marital == 'married' and primary_marital == 'married'

    # Same address is a strong indicator
    same_address = False
    borrower_address_id = borrower_info.get('current_address_id')
    primary_address_id = primary_info.get('current_address_id')
    if borrower_address_id and primary_address_id and borrower_address_id == primary_address_id:
        same_address = True

    # Strong indicators of spousal relationship
    if same_address and both_married and (not borrower_age or not primary_age or abs(borrower_age - primary_age) < 15):
        return RelationshipType.SPOUSE

    # If we have ages, use them to infer relationship
    if borrower_age and primary_age:
        age_diff = abs(borrower_age - primary_age)

        # Infer relationship based on age difference and name
        if age_diff < 10:
            # Similar age
            if same_last_name:
                return random.choices([RelationshipType.SPOUSE, RelationshipType.SIBLING], weights=[3, 2], k=1)[0]
            elif same_address:
                return random.choices([RelationshipType.SPOUSE, RelationshipType.FRIEND], [4, 1], k=1)[0]
            else:
                return random.choice([RelationshipType.SPOUSE, RelationshipType.FRIEND, RelationshipType.SIBLING])
        elif 10 <= age_diff < 20:
            # Medium age gap
            if same_last_name:
                return random.choices([RelationshipType.SIBLING, RelationshipType.OTHER], [3, 1], k=1)[0]
            else:
                return random.choice([RelationshipType.FRIEND, RelationshipType.OTHER])
        else:
            # Large age gap (20+ years)
            if borrower_age > primary_age:
                return RelationshipType.PARENT
            else:
                return RelationshipType.CHILD

    # If we don't have enough information
    if same_last_name:
        return random.choice(
            [RelationshipType.SPOUSE, RelationshipType.SIBLING, RelationshipType.PARENT, RelationshipType.CHILD])
    elif same_address:
        return random.choice([RelationshipType.SPOUSE, RelationshipType.FRIEND])
    else:
        return RelationshipType.get_random()


def _get_age_from_info(info):
    """
    Extract age from party/borrower information if available.

    Parameters:
    info: Dict with party/borrower information

    Returns:
    int or None: Age if available
    """
    # Try to get age directly if available
    if 'age' in info:
        return info['age']

    # Try to calculate from date of birth if available
    from datetime import date

    dob = info.get('date_of_birth')
    if dob:
        try:
            today = date.today()
            born = dob
            age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
            return age
        except (TypeError, ValueError):
            pass

    return None
