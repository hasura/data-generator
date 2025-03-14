import random


def generate_currency(probabilities=None):
    """
    Generates a currency code based on the provided or default probability distribution.

    :param probabilities: A dictionary specifying probabilities for each currency.
                          Example: {'USD': 0.5, 'JPY': 0.2, 'FRF': 0.2, 'GBP': 0.1}
    :return: A randomly chosen currency code.
    """
    # Define the available currencies
    currencies = ['USD', 'JPY', 'FRF', 'GBP']

    # If no probabilities provided, assign default uniform probabilities
    if probabilities is None:
        probabilities = {'USD': 0.4, 'JPY': 0.3, 'FRF': 0.2, 'GBP': 0.1}

    # Validate probabilities
    if set(probabilities.keys()) != set(currencies):
        raise ValueError("The probabilities dictionary must contain all these keys: 'USD', 'JPY', 'FRF', 'GBP'")
    if not (0 <= sum(probabilities.values()) <= 1):
        raise ValueError("Probabilities must sum to 1 or less.")

    def func(_a,_b,_c):
        # Generate currency based on the given probabilities
        value = random.choices(currencies, weights=[probabilities[c] for c in currencies], k=1)[0]

        return value

    return func



