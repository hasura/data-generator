import random


def generate_clabe():
    """Generates a fake CLABE number."""

    # Generate 3-digit bank code
    bank_code = str(random.randint(1, 999)).zfill(3)

    # Generate 4-digit branch code
    branch_code = str(random.randint(1, 9999)).zfill(4)

    # Generate 11-digit account number
    account_number = str(random.randint(1, 99999999999)).zfill(11)

    # Combine the components into the base CLABE
    base = bank_code + branch_code + account_number

    # Multiplicative weights for CLABE check digit
    weights = [3, 7, 1] * 6  # List has 18 elements to match the length of base

    # Calculate weighted sum
    total = sum(int(digit) * weights[i] for i, digit in enumerate(base))

    # Calculate check digit
    check_digit = (10 - (total % 10)) % 10

    # Return the complete CLABE number
    return base + str(check_digit)
