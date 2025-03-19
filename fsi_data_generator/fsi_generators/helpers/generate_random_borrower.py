import random
from typing import Dict, Any, Optional
import psycopg2


def generate_random_borrower(id_fields: Dict[str, Any], dg) -> Dict[str, Any]:
    """
    Generate a random mortgage services borrower record with reasonable values.

    Args:
        id_fields: Dictionary containing the required ID fields (enterprise_party_id)
        dg: DataGenertor instance

    Returns:
        Dictionary containing randomly generated borrower data (without ID fields)
    """
    # Get party information to make borrower data reasonable
    conn = dg.conn
    party_info = get_party_info(id_fields.get("enterprise_party_id"), conn)

    # Generate random values for education and dependents
    years_in_school = random.randint(12, 20)  # High school (12) to graduate degree (20)
    dependent_count = random.choices([0, 1, 2, 3, 4, 5],
                                     weights=[0.35, 0.25, 0.2, 0.15, 0.03, 0.02],
                                     k=1)[0]

    # Get or create addresses
    current_address_id = id_fields.get("current_address_id", None)
    mailing_address_id = id_fields.get("mailing_address_id", None)
    previous_address_id = id_fields.get("previous_address_id", None)

    # If address IDs are not provided, try to get existing addresses from party info
    if not current_address_id and party_info and 'addresses' in party_info and party_info['addresses']:
        if len(party_info['addresses']) > 0:
            current_address_id = party_info['addresses'][0]
        if len(party_info['addresses']) > 1:
            mailing_address_id = party_info['addresses'][1]
        if len(party_info['addresses']) > 2:
            previous_address_id = party_info['addresses'][2]

    # Create the borrower record
    borrower = {
        "years_in_school": years_in_school,
        "dependent_count": dependent_count,
        "current_address_id": current_address_id,
        "mailing_address_id": mailing_address_id,
        "previous_address_id": previous_address_id
    }

    return borrower


def get_party_info(party_id: Optional[int], conn) -> Optional[Dict[str, Any]]:
    """
    Get party information to make borrower data reasonable.

    Args:
        party_id: The ID of the enterprise party
        conn: PostgreSQL connection object

    Returns:
        Dictionary containing party information or None if party_id is None or party not found
    """
    if not party_id:
        return None

    try:
        cursor = conn.cursor()

        # Get basic party information
        cursor.execute("""
            SELECT name, party_type, date_of_birth, marital_status
            FROM enterprise.parties 
            WHERE enterprise_party_id = %s
        """, (party_id,))

        result = cursor.fetchone()

        if not result:
            cursor.close()
            return None

        party_info = {
            "name": result[0],
            "party_type": result[1],
            "date_of_birth": result[2],
            "marital_status": result[3],
            "addresses": []
        }

        # Get associated addresses
        cursor.execute("""
            SELECT enterprise_party_address_id
            FROM enterprise.party_addresses 
            WHERE enterprise_party_id = %s
            ORDER BY enterprise_party_address_id
        """, (party_id,))

        address_results = cursor.fetchall()

        if address_results:
            party_info["addresses"] = [addr[0] for addr in address_results]

        cursor.close()
        return party_info

    except (Exception, psycopg2.Error) as error:
        print(f"Error fetching party information: {error}")
        return None


def get_or_create_address(conn) -> Optional[int]:
    """
    Get a random existing address ID or create a new one.

    Args:
        conn: PostgreSQL connection object

    Returns:
        Address ID or None if query fails
    """
    try:
        cursor = conn.cursor()

        # Try to get a random existing address
        cursor.execute("""
            SELECT enterprise_address_id 
            FROM enterprise.addresses
            ORDER BY RANDOM()
            LIMIT 1
        """)

        result = cursor.fetchone()
        cursor.close()

        if result:
            return result[0]
        else:
            # No addresses found - this would typically mean creating a new address
            # But for simplicity, we'll return None which means no address
            return None

    except (Exception, psycopg2.Error) as error:
        print(f"Error fetching address ID: {error}")
        return None
