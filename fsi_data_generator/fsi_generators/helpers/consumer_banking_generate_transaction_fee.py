def consumer_banking_generate_transaction_fee(a, _b, _c):
    """
    Calculate a probable transaction fee based on transaction details.

    Parameters:
    transaction_type (str): Type of transaction (from the provided list, case-insensitive)
    amount (float): Amount of the transaction
    currency (str): Currency code of the transaction
    is_foreign (bool): Whether this is a foreign transaction
    """

    transaction_type = a.get('transaction_type')
    amount = a.get('amount')

    # Normalize transaction type to be case-insensitive
    normalized_type = transaction_type.lower() if transaction_type else "other"

    # Base fee structures by transaction type
    if normalized_type == "salary":
        # Usually no fee for receiving salary
        fee = 0.0
    elif normalized_type == "credit":
        # Small fixed fee for credit transactions
        fee = 1.50
    elif normalized_type == "debit":
        # Debit transactions might have small fees
        fee = 0.75
    elif normalized_type == "payment":
        # Payment processing fees (percentage-based)
        fee = amount * 0.01  # 1% fee
        fee = min(fee, 20.00)  # Cap at $20
    elif normalized_type == "cash":
        # Cash handling fee
        fee = 3.00 + (amount * 0.005)  # Base fee + 0.5% of amount
        fee = min(fee, 25.00)  # Cap at $25
    elif normalized_type == "intra-company":
        # Internal transfers usually have minimal fees
        fee = 0.50
    elif normalized_type == "dividend":
        # Dividend processing fee
        fee = amount * 0.005  # 0.5% fee
        fee = min(fee, 15.00)  # Cap at $15
    elif normalized_type == "government":
        # Government-related transactions often have fixed fees
        fee = 5.00
    elif normalized_type == "loan":
        # Loan processing fee
        fee = amount * 0.02  # 2% fee
        fee = min(fee, 50.00)  # Cap at $50
    else:  # "other"
        # Default fee for miscellaneous transactions
        fee = 2.00

    # Round to 2 decimal places
    fee = round(fee, 2)

    # Some fee waiver conditions
    if normalized_type == "salary" or (amount > 10000 and normalized_type in ["intra-company", "dividend"]):
        fee = 0.0  # Waive fees for salaries and large intra-company/dividend transactions

    return fee
