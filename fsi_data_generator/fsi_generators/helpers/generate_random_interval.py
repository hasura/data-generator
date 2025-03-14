import random


def generate_random_interval_with_optional_weights(
        year_ranges=None, year_weights=None,
        month_ranges=None, month_weights=None,
        week_ranges=None, week_weights=None,
        day_ranges=None, day_weights=None,
        hour_ranges=None, hour_weights=None,
        minute_ranges=None, minute_weights=None,
        second_ranges=None, second_weights=None):
    """
    Generate a random PostgreSQL-compatible interval with optional weighted probabilities.

    :param year_ranges: List of possible year ranges. Defaults to [0, 1, 2].
    :param year_weights: List of weights for year_ranges. Defaults to no weights.
    :param month_ranges: List of possible month ranges. Defaults to [0, 1, 6, 12].
    :param month_weights: List of weights for month_ranges. Defaults to no weights.
    :param week_ranges: List of possible week ranges. Defaults to [0, 1, 2, 4].
    :param week_weights: List of weights for week_ranges. Defaults to no weights.
    :param day_ranges: List of possible day ranges. Defaults to [0, 1, 7, 30].
    :param day_weights: List of weights for day_ranges. Defaults to no weights.
    :param hour_ranges: List of possible hour ranges. Defaults to [0, 23].
    :param hour_weights: List of weights for hour_ranges. Defaults to no weights.
    :param minute_ranges: List of possible minute ranges. Defaults to [0, 59].
    :param minute_weights: List of weights for minute_ranges. Defaults to no weights.
    :param second_ranges: List of possible second ranges. Defaults to [0, 59].
    :param second_weights: List of weights for second_ranges. Defaults to no weights.
    :return: A PostgreSQL-compatible interval (e.g., '1 year 3 months 2 days 10:15:00').
    """
    # Default ranges if no ranges are provided
    year_ranges = year_ranges or [0, 1, 2]
    month_ranges = month_ranges or [0, 1, 6, 12]
    week_ranges = week_ranges or [0, 1, 2, 4]
    day_ranges = day_ranges or [0, 1, 7, 30]
    hour_ranges = hour_ranges or [random.randint(0, 23)]
    minute_ranges = minute_ranges or [random.randint(0, 59)]
    second_ranges = second_ranges or [random.randint(0, 59)]

    # Generate random values, applying weights if provided
    years = random.choices(year_ranges, weights=year_weights, k=1)[0] if len(year_ranges) > 1 else year_ranges[0]
    months = random.choices(month_ranges, weights=month_weights, k=1)[0] if len(month_ranges) > 1 else month_ranges[0]
    weeks = random.choices(week_ranges, weights=week_weights, k=1)[0] if len(week_ranges) > 1 else week_ranges[0]
    days = random.choices(day_ranges, weights=day_weights, k=1)[0] if len(day_ranges) > 1 else day_ranges[0]
    hours = random.choices(hour_ranges, weights=hour_weights, k=1)[0] if len(hour_ranges) > 1 else hour_ranges[0]
    minutes = random.choices(minute_ranges, weights=minute_weights, k=1)[0] if len(minute_ranges) > 1 else \
        minute_ranges[0]
    seconds = random.choices(second_ranges, weights=second_weights, k=1)[0] if len(second_ranges) > 1 else \
        second_ranges[0]

    # Combine weeks into days since PostgreSQL intervals do not directly accept `weeks`
    days += weeks * 7

    # Build the interval string components
    parts = []
    if years > 0:
        parts.append(f"{years} year{'s' if years > 1 else ''}")
    if months > 0:
        parts.append(f"{months} month{'s' if months > 1 else ''}")
    if days > 0:
        parts.append(f"{days} day{'s' if days > 1 else ''}")
    if hours > 0 or minutes > 0 or seconds > 0:
        parts.append(f"{hours:02}:{minutes:02}:{seconds:02}")

    # Join the parts into a PostgreSQL-compatible interval string
    return ' '.join(parts)

# Example Usages:
# print("---- Default Ranges and No Weights ----")
# print(generate_random_interval_with_optional_weights())

# print("\n---- With Weighted Probabilities for Years and Months ----")
# print(generate_random_interval_with_optional_weights(
#     year_ranges=[0, 1, 2], year_weights=[50, 30, 20],
#     month_ranges=[0, 6, 12], month_weights=[40, 40, 20],
#     week_ranges=[0, 2], week_weights=[70, 30],
#     hour_ranges=[0, 23], minute_ranges=[0, 59], second_ranges=[0, 59]
# ))
