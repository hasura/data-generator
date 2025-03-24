import logging
import random
import re
import string
from typing import Any, Dict

from data_generator import DataGenerator

from .enums import AccountIdentifierScheme

logger = logging.getLogger(__name__)


def generate_random_account_identifier(_id_fields: Dict[str, Any], _dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random enterprise.account_identifiers record with reasonable values.

    Args:
        _id_fields: Dictionary containing the required ID fields (enterprise_account_identifier_id,
                    enterprise_account_id)
        _dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated account identifier data (without ID fields)
    """

    scheme = AccountIdentifierScheme.get_random()

    # Generate identification based on the selected scheme
    identification = generate_identification_for_scheme(scheme)

    # Generate a display name (40% chance of having one)
    name = None
    if random.random() < 0.4:
        prefixes = ["Primary", "Secondary", "Business", "Personal", "Joint", "Savings", "Checking", "Investment",
                    "Trust"]
        suffixes = ["Account", "Identifier", "ID", "Reference", "Number"]
        name = f"{random.choice(prefixes)} {scheme.value} {random.choice(suffixes)}"

    # Generate LEI (10% chance if scheme isn't already LEI)
    lei = None
    if scheme != AccountIdentifierScheme.LEI and random.random() < 0.1:
        lei = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))

    # Generate secondary identification (20% chance)
    secondary_identification = None
    if random.random() < 0.2:
        # For secondary ID, generate a simple alphanumeric string
        secondary_identification = ''.join(
            random.choices(string.ascii_uppercase + string.digits, k=random.randint(6, 20)))

    # Create the account identifier record
    account_identifier = {
        "identification": identification,
        "scheme_name": scheme.value,
        "name": name,
        "lei": lei,
        "secondary_identification": secondary_identification
    }

    return account_identifier


def generate_identification_for_scheme(scheme: AccountIdentifierScheme) -> str:
    """
    Generate a realistic identifier value based on the identification scheme.

    Args:
        scheme: The type of identification scheme (enum value)

    Returns:
        A string containing a realistic identifier for the given scheme
    """
    if scheme == AccountIdentifierScheme.IBAN:
        # Generate IBAN (International Bank Account Number)
        # Format varies by country, using a generic format here
        country_code = random.choice(["DE", "FR", "GB", "ES", "IT", "NL", "BE", "CH", "AT"])
        check_digits = f"{random.randint(10, 99)}"
        bank_code = ''.join(random.choices(string.digits, k=8))
        account_number = ''.join(random.choices(string.digits, k=10))
        return f"{country_code}{check_digits}{bank_code}{account_number}"

    elif scheme == AccountIdentifierScheme.BIC:
        # Generate BIC (Bank Identifier Code) / SWIFT code
        # Format: 4 bank code, 2 country code, 2 location code, 3 branch code (optional)
        bank_code = ''.join(random.choices(string.ascii_uppercase, k=4))
        country_code = random.choice(["US", "GB", "DE", "FR", "JP", "CN", "AU", "CA", "CH"])
        location_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=2))
        has_branch = random.random() < 0.5
        branch_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=3)) if has_branch else ""
        return f"{bank_code}{country_code}{location_code}{branch_code}"

    elif scheme == AccountIdentifierScheme.ACCOUNT_NUMBER:
        # Generate standard bank account number
        length = random.randint(8, 16)
        return ''.join(random.choices(string.digits, k=length))

    elif scheme == AccountIdentifierScheme.ROUTING_NUMBER:
        # Generate ABA routing number (9 digits)
        return ''.join(random.choices(string.digits, k=9))

    elif scheme == AccountIdentifierScheme.SORT_CODE:
        # Generate UK sort code (6 digits, often formatted as XX-XX-XX)
        digits = ''.join(random.choices(string.digits, k=6))
        return f"{digits[:2]}-{digits[2:4]}-{digits[4:6]}"

    elif scheme == AccountIdentifierScheme.CREDIT_CARD:
        # Generate masked credit card number (only showing last 4 digits)
        last_four = ''.join(random.choices(string.digits, k=4))
        return f"XXXX-XXXX-XXXX-{last_four}"

    elif scheme == AccountIdentifierScheme.CLABE:
        # Generate CLABE number (18 digits for Mexico)
        return ''.join(random.choices(string.digits, k=18))

    elif scheme == AccountIdentifierScheme.BSB:
        # Generate BSB number (6 digits for Australia, often formatted as XXX-XXX)
        digits = ''.join(random.choices(string.digits, k=6))
        return f"{digits[:3]}-{digits[3:6]}"

    elif scheme == AccountIdentifierScheme.IFSC:
        # Generate IFSC code (Indian Financial System Code)
        # Format: 4 bank code, 0, 6 branch code
        bank_code = ''.join(random.choices(string.ascii_uppercase, k=4))
        branch_code = ''.join(random.choices(string.digits, k=6))
        return f"{bank_code}0{branch_code}"

    elif scheme == AccountIdentifierScheme.CNAPS:
        # Generate CNAPS code (China National Advanced Payment System)
        # 12-digit code
        return ''.join(random.choices(string.digits, k=12))

    elif scheme == AccountIdentifierScheme.LEI:
        # Generate LEI (Legal Entity Identifier)
        # 20 characters
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))

    elif scheme == AccountIdentifierScheme.TAX_ID:
        # Generate Tax ID (like SSN or EIN in US)
        # Format as XXX-XX-XXXX or XX-XXXXXXX
        if random.random() < 0.7:  # SSN format
            digits = ''.join(random.choices(string.digits, k=9))
            return f"{digits[:3]}-{digits[3:5]}-{digits[5:9]}"
        else:  # EIN format
            digits = ''.join(random.choices(string.digits, k=9))
            return f"{digits[:2]}-{digits[2:9]}"

    elif scheme == AccountIdentifierScheme.CIF:
        # Generate CIF (Customer Information File) number
        # Usually alphanumeric with various formats
        length = random.randint(6, 12)
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

    elif scheme == AccountIdentifierScheme.DDA:
        # Generate DDA (Demand Deposit Account) number
        return ''.join(random.choices(string.digits, k=10))

    elif scheme == AccountIdentifierScheme.PROPRIETARY:
        # Generate proprietary identifier
        # Can be very diverse, using alphanumeric with possibly some separators
        length = random.randint(8, 20)
        result = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
        # Add some separators sometimes
        if random.random() < 0.5:
            result = re.sub(r'(.{4})', r'\1-', result, 0, re.DOTALL).rstrip('-')
        return result

    elif scheme == AccountIdentifierScheme.PASSPORT:
        # Generate passport number
        # Format varies by country, using a generic format
        country_code = random.choice(["US", "GB", "DE", "FR", "JP", "CN", "AU", "CA", "CH"])
        serial = ''.join(random.choices(string.digits, k=8))
        return f"{country_code}{serial}"

    elif scheme == AccountIdentifierScheme.DRIVERS_LICENSE:
        # Generate driver's license number
        # Format varies widely by jurisdiction
        letters = ''.join(random.choices(string.ascii_uppercase, k=random.randint(1, 3)))
        digits = ''.join(random.choices(string.digits, k=random.randint(6, 10)))
        return f"{letters}{digits}"

    elif scheme == AccountIdentifierScheme.NATIONAL_ID:
        # Generate national ID number
        # Format varies by country
        length = random.randint(8, 12)
        return ''.join(random.choices(string.digits, k=length))

    else:  # OTHER or unknown scheme
        # Generate a generic identifier
        length = random.randint(8, 20)
        return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
