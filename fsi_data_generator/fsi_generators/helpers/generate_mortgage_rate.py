import random

def generate_mortgage_rate(_a,_b_,_c):
    """
    Generates a random mortgage rate as a percentage.
    """
    min_rate = 2.0  # Minimum plausible mortgage rate
    max_rate = 10.0 # Maximum plausible mortgage rate
    return round(random.uniform(min_rate, max_rate), 2)

