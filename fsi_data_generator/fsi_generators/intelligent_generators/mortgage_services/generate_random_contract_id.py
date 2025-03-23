import datetime
import random
import string


def generate_random_contract_id():
    """
    Generates a completely random contract ID for various financial contracts.
    """

    contract_types = ["FX_SPOT", "FX_FWD", "FX_OPT", "MM_DEPOSIT", "MM_LOAN", "BOND_TRADE", "EQUITY_TRADE",
                      "DERIVATIVE"]  # Expanded contract types

    random_type = random.choice(contract_types)
    timestamp_str = datetime.datetime.now().strftime(
        "%Y%m%d%H%M%S%f")  # Include microseconds for extra uniqueness.
    random_chars = "".join(
        random.choices(string.ascii_uppercase + string.digits, k=10))  # Increased random characters

    return f"{random_type}-{timestamp_str}-{random_chars}"
