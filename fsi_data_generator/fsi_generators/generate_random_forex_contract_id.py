import datetime
import random
import string


def generate_random_forex_contract_id():
    """
    Generates a completely random contract ID for Forex (FX) contracts only.
    """

    # Restrict to Forex contract types
    forex_contract_types = ["FX_SPOT", "FX_FWD", "FX_OPT"]  # Focus on Forex contracts only

    random_type = random.choice(forex_contract_types)  # Randomly select a Forex contract type
    timestamp_str = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")  # Current timestamp with microseconds
    random_chars = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))  # Random alphanumeric chars

    return f"{random_type}-{timestamp_str}-{random_chars}"
