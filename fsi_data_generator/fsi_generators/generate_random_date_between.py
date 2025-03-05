import random
from datetime import datetime, timedelta


def generate_random_date_between(base_date):
    """
    Generates a random datetime between a given date and today.

    :param base_date: date time object
    :return: A randomly generated datetime between the provided date and today.
    """

    # Validate the date
    if not isinstance(base_date, datetime):
        raise ValueError(f"'{base_date}' must be provided and must be a datetime object")

    # Get today's date
    today = datetime.now()

    # Ensure the base_date is before today
    if base_date >= today:
        raise ValueError(f"'{base_date}' must be in the past to generate a valid random datetime")

    # Calculate the number of days between base_date and today
    max_days = (today - base_date).days

    # Generate a random number of days to add (min: 1, max: max_days)
    random_days = random.randint(1, max_days - 1)

    # Generate and return the random datetime
    random_date = base_date + timedelta(days=random_days)
    return random_date
