from fsi_data_generator.fsi_generators.intelligent_generators.enterprise.enums import IdentifierScheme


def generate_financial_institution_identifier(region=None):
    """
    Generate a financial institution identifier scheme and value based on region.

    Args:
        region (str, optional): Region code (EU, UK, US, ASIA, OTHER). If None, a random region is selected.

    Returns:
        tuple: (scheme_name, identification, lei) where:
            - scheme_name is the AccountIdentifierScheme enum value
            - identification is the generated identifier string
            - lei is an optional Legal Entity Identifier (may equal None)
    """

    import random

    # If no region specified, choose one
    if not region:
        regions = ["EU", "UK", "US", "ASIA", "OTHER"]
        region_weights = [30, 20, 30, 15, 5]
        region = random.choices(regions, weights=region_weights, k=1)[0]

    # Choose appropriate scheme based on region
    if region == "EU":
        # EU primarily uses BIC
        scheme_options = [
            IdentifierScheme.BIC,
            IdentifierScheme.LEI,
            IdentifierScheme.OTHER
        ]
        weights = [80, 15, 5]
    elif region == "UK":
        # UK uses BIC or Sort Code
        scheme_options = [
            IdentifierScheme.BIC,
            IdentifierScheme.SORT_CODE,
            IdentifierScheme.OTHER
        ]
        weights = [50, 45, 5]
    elif region == "US":
        # US primarily uses Routing Number
        scheme_options = [
            IdentifierScheme.ROUTING_NUMBER,
            IdentifierScheme.BIC,
            IdentifierScheme.OTHER
        ]
        weights = [70, 25, 5]
    elif region == "ASIA":
        # Asia uses various identifier schemes
        scheme_options = [
            IdentifierScheme.BIC,
            IdentifierScheme.OTHER
        ]
        weights = [85, 15]
    else:
        # Other regions
        scheme_options = [
            IdentifierScheme.BIC,
            IdentifierScheme.OTHER
        ]
        weights = [90, 10]

    scheme_name = random.choices(scheme_options, weights=weights, k=1)[0]

    # Generate plausible identification based on the scheme
    if scheme_name == IdentifierScheme.BIC:
        # BIC format: 8 or 11 characters - bank code (4), country code (2), location code (2), branch code (3, optional)
        bank_code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=4))
        country_code = random.choice(['US', 'GB', 'DE', 'FR', 'JP', 'CN', 'CA', 'AU', 'CH', 'IT'])
        location_code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=2))

        # 60% chance of including branch code (11-character BIC)
        if random.random() < 0.6:
            branch_code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=3))
            identification = f"{bank_code}{country_code}{location_code}{branch_code}"
        else:
            identification = f"{bank_code}{country_code}{location_code}"

    elif scheme_name == IdentifierScheme.SORT_CODE:
        # UK Sort Code format: 6 digits, often shown as 3 pairs (e.g., 12-34-56)
        identification = ''.join(random.choices('0123456789', k=6))

    elif scheme_name == IdentifierScheme.ROUTING_NUMBER:
        # US ABA Routing Number: 9 digits
        identification = ''.join(random.choices('0123456789', k=9))

    elif scheme_name == IdentifierScheme.LEI:
        # LEI format: 20 characters - prefix (4), zeros (2), entity-specific (12), check digits (2)
        prefix = ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=4))
        entity_part = ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=12))
        check_digits = ''.join(random.choices('0123456789', k=2))
        identification = f"{prefix}00{entity_part}{check_digits}"

    else:  # Other identifier types
        identification = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=random.randint(8, 15)))

    # Generate LEI (optional - 40% chance if not already using LEI as main identifier)
    lei = None
    if scheme_name != IdentifierScheme.LEI and random.random() < 0.4:
        prefix = ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=4))
        entity_part = ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=12))
        check_digits = ''.join(random.choices('0123456789', k=2))
        lei = f"{prefix}00{entity_part}{check_digits}"

    return scheme_name, identification, lei


def generate_financial_institution_name(region=None):
    """
    Generate a plausible financial institution name based on region.

    Args:
        region (str, optional): Region code (EU, UK, US, ASIA, OTHER). If None, a random region is selected.

    Returns:
        str: Generated institution name
    """
    import random

    # If no region specified, choose one
    if not region:
        regions = ["EU", "UK", "US", "ASIA", "OTHER"]
        region_weights = [30, 20, 30, 15, 5]
        region = random.choices(regions, weights=region_weights, k=1)[0]

    # Generic bank name components
    bank_name_prefixes = ["United", "National", "First", "Capital", "Royal", "Metro", "City", "Global",
                         "Continental", "Pacific", "Atlantic", "Central", "Eastern", "Western", "Union",
                         "Trust", "Security"]

    bank_name_suffixes = ["Bank", "Financial", "Credit Union", "Savings", "Trust", "Banking Group",
                         "Banking Corporation", "Bancorp", "Investments", "Savings & Loan"]

    # Region-specific real-world-inspired bank names
    regional_bank_names = {
        "US": ["Chase", "Wells Fargo", "Bank of America", "Citibank", "PNC", "TD", "US Bank"],
        "UK": ["Barclays", "HSBC", "NatWest", "Lloyds", "Santander UK", "TSB"],
        "EU": ["Deutsche Bank", "BNP Paribas", "Société Générale", "UniCredit", "ING", "Rabobank"],
        "ASIA": ["Mitsubishi UFJ", "ICBC", "DBS", "OCBC", "Mizuho", "Bank of China"],
        "OTHER": ["Standard Chartered", "ANZ", "Westpac", "RBC", "Scotiabank", "Banco Santander"]
    }

    # Choose name generation strategy
    if random.random() < 0.6:  # 60% chance of using regional bank name
        name = random.choice(regional_bank_names.get(region, regional_bank_names["OTHER"]))
    else:  # 40% chance of generating a generic bank name
        name = f"{random.choice(bank_name_prefixes)} {random.choice(bank_name_suffixes)}"

    return name


def generate_financial_institution_identifier_for_type(entity_type):
    """
    Specialized version of generate_financial_institution_identifier
    that adjusts probabilities based on entity type.

    Args:
        entity_type (str): Type of entity (e.g., "FINANCIAL_INSTITUTION")

    Returns:
        tuple: (scheme_name, identification, lei) as in the standard function
    """
    from ..enterprise.enums import IdentifierScheme

    import random

    if entity_type == "FINANCIAL_INSTITUTION":
        # Financial institutions typically use BIC, LEI, or other specialized codes
        scheme_options = [
            IdentifierScheme.BIC,
            IdentifierScheme.LEI,
            IdentifierScheme.SORT_CODE,
            IdentifierScheme.ROUTING_NUMBER
        ]
        weights = [50, 20, 15, 15]  # BIC is most common for financial institutions

        scheme_name = random.choices(scheme_options, weights=weights, k=1)[0]

        # Rest of identifier generation handled by main function
        if scheme_name == IdentifierScheme.BIC:
            # BIC format: 8 or 11 characters
            bank_code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=4))
            country_code = random.choice(['US', 'GB', 'DE', 'FR', 'JP', 'CN', 'CA', 'AU', 'CH', 'IT'])
            location_code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=2))

            # 80% chance of including branch code (11-character BIC) for financial institutions
            if random.random() < 0.8:
                branch_code = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', k=3))
                identification = f"{bank_code}{country_code}{location_code}{branch_code}"
            else:
                identification = f"{bank_code}{country_code}{location_code}"

        elif scheme_name == IdentifierScheme.LEI:
            # LEI format: 20 characters - prefix (4), zeros (2), entity-specific (12), check digits (2)
            prefix = ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=4))
            entity_part = ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=12))
            check_digits = ''.join(random.choices('0123456789', k=2))
            identification = f"{prefix}00{entity_part}{check_digits}"

            # Ensure we generate an LEI (always include for financial institutions)
            # lei = identification
        else:
            # Use the standard function for other identifier types
            return generate_financial_institution_identifier()

        # Additional LEI generation (60% chance of adding secondary LEI)
        lei = None
        if random.random() < 0.6:
            prefix = ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=4))
            entity_part = ''.join(random.choices('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=12))
            check_digits = ''.join(random.choices('0123456789', k=2))
            lei = f"{prefix}00{entity_part}{check_digits}"

        return scheme_name, identification, lei

    # For non-financial institution types, use the standard function
    return generate_financial_institution_identifier()
