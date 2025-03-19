import random

def generate_credit_score(_a,_b,_c):
    """
    Generates a random credit score based on the distribution
    of credit scores in the United States in Q3 2024.
    """
    ranges = [
        (300, 580),
        (580, 670),
        (670, 740),
        (740, 800),
        (800, 851)
    ]
    probabilities = [0.132, 0.155, 0.210, 0.278, 0.225]

    chosen_range = random.choices(ranges, weights=probabilities, k=1)
    lower_bound = chosen_range
    upper_bound = chosen_range[1]

    return random.randint(lower_bound, upper_bound)
