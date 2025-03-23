import random


def generate_account_number(length=17, separator="-"):
    """
    Generates a random account number with the specified length and separator.

    Args:
      length: The total length of the account number (including separators).
      separator: The character used to separate groups of digits.

    Returns:
      A string representing the generated account number.
    """

    if length <= 0:
        return ""

    # Calculate the number of digits needed
    num_digits = length - (length // 4)  # Account for separators

    # Generate random digits
    digits = ''.join(random.choice('0123456789') for _ in range(num_digits))

    # Insert separators
    account_number = separator.join(digits[i:i + 4] for i in range(0, num_digits, 4))

    return account_number


def generate_account_numbers(num_account_numbers=10000):
    account_numbers = set()
    for _ in range(num_account_numbers):
        account_numbers.add(generate_account_number())
    return list(account_numbers)


fake_account_numbers = generate_account_numbers()
