import random


def probability_return_string(return_value, probability):
    """
    Returns 'return_value' based on the given probability.
    If not selected, returns a blank string.

    :param return_value: The value to be returned based on probability.
    :param probability: A float (0.0 to 1.0) representing the probability of returning the value.
    :return: 'return_value' or an empty string.
    """
    if not (0 <= probability <= 1):
        raise ValueError("Probability must be a value between 0 and 1.")

    # Randomly choose to return the value based on the probability

    def func(_a,_b,_c):
        return return_value if random.random() < probability else ""

    return func
