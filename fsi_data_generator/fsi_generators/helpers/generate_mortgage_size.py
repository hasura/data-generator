import random


def generate_mortgage_size(_a, _b, _c):
    """
    Generates a random mortgage size based on the distribution
    of mortgage sizes in the United States in 2023.
    """

    ranges = [
        (0, 50000),
        (50000, 100000),
        (100000, 300000),
        (300000, 500000),
        (500000, 750000),
        (750000, 1000000),
        (1000000, float('inf'))
    ]
    probabilities = [0.0263, 0.0371, 0.3129, 0.2992, 0.1727, 0.0767, 0.0752]

    chosen_range = random.choices(ranges, weights=probabilities, k=1)[0]

    lower_bound, upper_bound = chosen_range

    if upper_bound == float('inf'):
        # For the open-ended range, we can pick a large number,
        # but it's important to acknowledge this is a simplification.
        # We could potentially use a Pareto distribution for a more realistic simulation
        # of the tail, but for simplicity, we'll pick a random number between 1M and 2M.
        return random.uniform(lower_bound, 2000000)
    else:
        return random.uniform(lower_bound, upper_bound)
