def identify_account_scheme(account_identifier):
    """
    Identifies the scheme of a bank account identifier.

    Args:
        account_identifier (str): The bank account identifier.

    Returns:
        str: The scheme name, or None if the scheme cannot be identified.
    """

    account_identifier = str(account_identifier).upper().strip()  # Normalize input

    # IBAN Check (simplified)
    if 15 <= len(account_identifier) <= 34 and account_identifier[0:2].isalpha() and account_identifier[
                                                                                     2:4].isdigit():
        return "IBAN"

    # BIC/SWIFT Check (simplified)
    if 8 <= len(account_identifier) <= 11 and account_identifier.isalnum():
        return "BIC/SWIFT Code"

    # ISO 9362 (BIC/SWIFT Standard) - Since BIC is based on it, the BIC check will cover this.
    # Therefore, this is not needed as a separate check.

    # ABA Routing Number (US) Check
    if len(account_identifier) == 9 and account_identifier.isdigit():
        return "ABA Routing Transit Number (RTN)"

    # Sort Code (UK/Ireland) Check
    if len(account_identifier) == 6 and account_identifier.isdigit():
        return "Sort Code"

    # CLABE (Mexico) Check
    if len(account_identifier) == 18 and account_identifier.isdigit():
        return "CLABE"

    # Transit Number (Canada) Check - Typically 9 digits (5 transit, 3 institution, 1 branch)
    if len(account_identifier) == 9 and account_identifier.isdigit():
        return "Transit Number"

    # BSB Number (Australia) Check - 6 digits
    if len(account_identifier) == 6 and account_identifier.isdigit():
        return "BSB Number"

    # Issuer Identification Number (IIN) - First 6 digits of card, or first 8.
    if 6 <= len(account_identifier) <= 8 and account_identifier.isdigit():
        return "Issuer Identification Number (IIN)"

    # Basic Account Number (Generic) - Very Broad, should be last.
    if account_identifier.isdigit():
        return "Account Number"

    return None  # Scheme not identified
