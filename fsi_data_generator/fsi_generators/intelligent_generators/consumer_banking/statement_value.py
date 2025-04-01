from .enums import StatementValueType
from data_generator import DataGenerator, SkipRowGenerationError
from datetime import datetime
from typing import Any, Dict

import json
import numpy as np
import pytz
import random


def generate_random_statement_value(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random statement value with plausible values.

    Args:
        id_fields: Dictionary containing the required ID fields
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated statement value data
    """
    # Get database connection
    conn = dg.conn

    # Validate required fields
    if 'consumer_banking_statement_id' not in id_fields:
        raise ValueError("consumer_banking_statement_id is required")

    # Fetch the statement to verify it exists and get additional context
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT s.consumer_banking_statement_id, s.creation_date_time, s.start_date_time, s.end_date_time, 
                   s.consumer_banking_account_id, a.opened_date
            FROM consumer_banking.statements s
            JOIN consumer_banking.accounts a ON s.consumer_banking_account_id = a.consumer_banking_account_id
            WHERE s.consumer_banking_statement_id = %s
        """, (id_fields['consumer_banking_statement_id'],))

        statement = cursor.fetchone()

        if not statement:
            raise ValueError(f"No statement found with ID {id_fields['consumer_banking_statement_id']}")

        creation_date_time = statement.get('creation_date_time')
        statement_period_start = statement.get('start_date_time')
        statement_period_end = statement.get('end_date_time')
        # account_opened_date = statement.get('opened_date')
        consumer_banking_account_id = statement.get('consumer_banking_account_id')

        # Only create statement values for valid statements
        if not statement_period_start or not statement_period_end:
            raise SkipRowGenerationError

        # Check if there's a previous statement for this account
        cursor.execute("""
            SELECT consumer_banking_statement_id, creation_date_time
            FROM consumer_banking.statements
            WHERE consumer_banking_account_id = %s
              AND creation_date_time < %s
            ORDER BY creation_date_time DESC
            LIMIT 1
        """, (consumer_banking_account_id, creation_date_time))

        previous_statement = cursor.fetchone()
        previous_statement_id = previous_statement.get('consumer_banking_statement_id') if previous_statement else None

        # Always use UTC timezone
        utc = pytz.UTC

        # Select random value type using default weights
        chosen_value_type = StatementValueType.get_random()

        # Generate value and previous value based on the type
        value, previous_value, description = _generate_value_by_type(chosen_value_type, previous_statement_id, cursor)

        # Calculate change percentage if there's a previous value
        change_percentage = None
        if previous_value is not None:
            try:
                # Handle different value types
                if chosen_value_type in [StatementValueType.LOYALTY_POINTS, StatementValueType.REWARD_BALANCE,
                                         StatementValueType.POINTS_EARNED, StatementValueType.POINTS_REDEEMED,
                                         StatementValueType.MILES_EARNED, StatementValueType.MILES_BALANCE,
                                         StatementValueType.CREDIT_SCORE]:
                    # Numeric values
                    current_val = float(value)
                    prev_val = float(previous_value)
                    if prev_val != 0:
                        change_percentage = round(((current_val - prev_val) / abs(prev_val)) * 100, 2)
            except (ValueError, TypeError):
                # Handle non-numeric values
                change_percentage = None

        # Determine if this is an estimated value (15% chance)
        is_estimated = random.random() < 0.15

        # Reference period - typically matches statement period but can be different
        # 70% chance of using statement period
        reference_period_start = statement_period_start.date()
        reference_period_end = statement_period_end.date()

        if random.random() > 0.7:
            # Custom reference period - often calendar month, quarter, or year-to-date
            if random.random() < 0.5:
                # Calendar month
                reference_period_start = datetime(reference_period_end.year, reference_period_end.month, 1,
                                                  tzinfo=utc).date()
            elif random.random() < 0.7:
                # Calendar quarter
                quarter_start_month = ((reference_period_end.month - 1) // 3) * 3 + 1
                reference_period_start = datetime(reference_period_end.year, quarter_start_month, 1,
                                                  tzinfo=utc).date()
            else:
                # Year-to-date
                reference_period_start = datetime(reference_period_end.year, 1, 1,
                                                  tzinfo=utc).date()

        # Create the statement value dictionary with UTC timezone
        now = datetime.now(utc)

        statement_value = {
            "consumer_banking_statement_id": id_fields['consumer_banking_statement_id'],
            "value": value,
            "type": chosen_value_type.value,
            "description": description,
            "previous_value": previous_value,
            "change_percentage": change_percentage,
            "is_estimated": is_estimated,
            "reference_period_start": reference_period_start if random.random() < 0.8 else None,
            "reference_period_end": reference_period_end if random.random() < 0.8 else None,
            "created_at": now,
            "updated_at": now
        }

        return statement_value

    finally:
        cursor.close()


def _generate_value_by_type(value_type: StatementValueType, previous_statement_id: int, cursor) -> tuple:
    """
    Generate appropriate value content based on the value type.

    Args:
        value_type: The type of statement value
        previous_statement_id: ID of the previous statement, if any
        cursor: Database cursor for querying previous values

    Returns:
        Tuple of (value, previous_value, description)
    """
    previous_value = None
    # description = None

    # Check for previous value if we have a previous statement
    if previous_statement_id:
        cursor.execute("""
            SELECT value 
            FROM consumer_banking.statement_values
            WHERE consumer_banking_statement_id = %s AND type = %s
            LIMIT 1
        """, (previous_statement_id, value_type.value))

        prev_value_record = cursor.fetchone()
        if prev_value_record:
            previous_value = prev_value_record.get('value')

    if value_type == StatementValueType.LOYALTY_POINTS:
        # Loyalty points are typically whole numbers
        if previous_value:
            base = int(float(previous_value))
            # Points usually increase, sometimes decrease due to redemptions
            change = random.randint(-int(base * 0.2) if random.random() < 0.2 else 0, int(base * 0.3))
            value = str(max(0, base + change))
        else:
            # Initial value - usually between 500-20000 for established accounts
            value = str(random.randint(500, 20000))

        description = "Total loyalty points available for redemption"

    elif value_type == StatementValueType.REWARD_BALANCE:
        # Similar to loyalty points but can be decimal for cash rewards
        if previous_value:
            base = float(previous_value)
            change = random.uniform(-base * 0.15 if random.random() < 0.2 else 0, base * 0.25)
            value = str(round(max(0, base + change), 2))
        else:
            value = str(round(random.uniform(50, 2000), 2))

        description = "Current reward balance in dollars"

    elif value_type == StatementValueType.CASH_BACK_EARNED:
        # Cash back earned this period - relatively small amount
        value = str(round(random.uniform(5, 150), 2))
        description = "Cash back earned during this statement period"

    elif value_type == StatementValueType.POINTS_EARNED:
        # Points earned this period
        value = str(random.randint(100, 5000))
        description = "Points earned during this statement period"

    elif value_type == StatementValueType.POINTS_REDEEMED:
        # Points redeemed this period (often zero)
        if random.random() < 0.7:  # 70% chance of redemption
            value = str(random.randint(500, 10000))
        else:
            value = "0"
        description = "Points redeemed during this statement period"

    elif value_type == StatementValueType.TIER_LEVEL:
        # Tier levels are typically named
        tiers = ["Bronze", "Silver", "Gold", "Platinum", "Diamond", "Elite"]
        tier_weights = [20, 30, 25, 15, 7, 3]  # Lower tiers are more common
        value = random.choices(tiers, weights=tier_weights, k=1)[0]

        # Previous tier might be different
        if random.random() < 0.05:  # 5% chance of tier change
            prev_index = tiers.index(value)
            possible_prev_indices = [i for i in range(len(tiers)) if i != prev_index]
            # More likely to move up than down
            weights = [3 if i < prev_index else 1 for i in possible_prev_indices]
            prev_index = random.choices(possible_prev_indices, weights=weights, k=1)[0]
            previous_value = tiers[prev_index]
        else:
            previous_value = value

        description = "Current loyalty program tier level"

    elif value_type == StatementValueType.CREDIT_SCORE:
        # Credit scores range from 300-850
        if previous_value:
            base = int(previous_value)
            # Credit scores don't change dramatically month-to-month
            change = random.randint(-15, 15)
            value = str(max(300, min(850, base + change)))
        else:
            # Distribution weighted toward middle scores
            scores = list(range(300, 850, 10))
            # Generate Gaussian-like weights
            mean = sum(scores) / len(scores)  # Center around the middle
            std_dev = 100  # Standard deviation controls spread
            weights = [np.exp(-((x - mean) ** 2) / (2 * std_dev ** 2)) for x in scores]

            # Normalize weights to ensure sum(weights) > 0
            weights = [w / sum(weights) for w in weights]

            # Generate random value
            value = str(random.choices(scores, weights=weights, k=1)[0] + random.randint(0, 9))

        description = "Your current FICO credit score"

    elif value_type == StatementValueType.CARBON_FOOTPRINT:
        # Carbon footprint in kg CO2
        value = str(round(random.uniform(50, 500), 1))
        if previous_value:
            previous_value = str(round(float(previous_value) * random.uniform(0.9, 1.1), 1))

        description = "Estimated carbon footprint of purchases (kg CO2)"

    elif value_type == StatementValueType.SPENDING_CATEGORY:
        # JSON object with spending breakdown
        categories = ["Dining", "Shopping", "Travel", "Groceries", "Entertainment", "Bills & Utilities",
                      "Transportation", "Health & Wellness", "Other"]

        percentages = []
        remaining = 100
        for i in range(len(categories) - 1):
            p = min(remaining, random.randint(5, 40))
            percentages.append(p)
            remaining -= p
        percentages.append(remaining)

        random.shuffle(percentages)

        spending_data = {categories[i]: percentages[i] for i in range(len(categories))}
        value = json.dumps(spending_data)
        description = "Breakdown of spending by category (percentage)"

    elif value_type == StatementValueType.MILES_EARNED:
        # Miles earned this period
        value = str(random.randint(100, 5000))
        description = "Travel miles earned during this statement period"

    elif value_type == StatementValueType.MILES_BALANCE:
        # Similar to loyalty points
        if previous_value:
            base = int(float(previous_value))
            # Miles usually increase, sometimes decrease due to redemptions
            change = random.randint(-int(base * 0.1) if random.random() < 0.15 else 0, int(base * 0.2))
            value = str(max(0, base + change))
        else:
            # Initial value - usually between 1000-50000 for established accounts
            value = str(random.randint(1000, 50000))

        description = "Total travel miles available for redemption"

    elif value_type == StatementValueType.MERCHANT_CATEGORY:
        # JSON object with merchant breakdown
        merchants = ["Restaurants", "Retail Stores", "Online Merchants", "Gas Stations",
                     "Supermarkets", "Subscription Services", "Travel & Transportation", "Other"]

        percentages = []
        remaining = 100
        for i in range(len(merchants) - 1):
            p = min(remaining, random.randint(5, 40))
            percentages.append(p)
            remaining -= p
        percentages.append(remaining)

        random.shuffle(percentages)

        merchant_data = {merchants[i]: percentages[i] for i in range(len(merchants))}
        value = json.dumps(merchant_data)
        description = "Breakdown of spending by merchant type (percentage)"

    elif value_type == StatementValueType.NEXT_TIER_PROGRESS:
        # Progress as percentage to next tier
        value = str(random.randint(0, 100))
        if previous_value:
            # Progress generally increases
            prev = int(previous_value)
            value = str(min(100, prev + random.randint(0, 15)))

        description = "Progress towards next loyalty tier level (%)"

    elif value_type == StatementValueType.ANNUAL_REWARDS_SUMMARY:
        # JSON object with annual rewards data
        if previous_value and random.random() < 0.9:  # 90% chance of building on previous
            prev_data = json.loads(previous_value)
            earned = prev_data.get("earned", 0) + random.randint(10, 200)
            redeemed = prev_data.get("redeemed", 0)
            if random.random() < 0.3:  # 30% chance of redemption
                redeemed += random.randint(50, min(earned, 1000))

            rewards_data = {
                "earned": earned,
                "redeemed": redeemed,
                "balance": earned - redeemed
            }
        else:
            earned = random.randint(100, 2000)
            redeemed = random.randint(0, earned - 50) if earned > 100 else 0
            rewards_data = {
                "earned": earned,
                "redeemed": redeemed,
                "balance": earned - redeemed
            }

        value = json.dumps(rewards_data)
        description = "Year-to-date rewards summary"

    elif value_type == StatementValueType.ANNUAL_SPENDING_SUMMARY:
        # JSON object with annual spending data
        categories = ["Dining", "Shopping", "Travel", "Groceries", "Entertainment", "Bills & Utilities",
                      "Transportation", "Health & Wellness", "Other"]

        spending_data = {}
        total = 0

        for category in categories:
            amount = round(random.uniform(100, 5000), 2)
            spending_data[category] = amount
            total += amount

        spending_data["Total"] = round(total, 2)

        if previous_value and random.random() < 0.9:  # 90% chance of building on previous
            try:
                prev_data = json.loads(previous_value)
                # Increment previous values by some random amount
                for key in prev_data:
                    if key != "Total":
                        prev_amount = prev_data[key]
                        increase = round(random.uniform(50, 500), 2)
                        spending_data[key] = round(prev_amount + increase, 2)

                total = sum(spending_data[k] for k in spending_data if k != "Total")
                spending_data["Total"] = round(total, 2)
            except (json.JSONDecodeError, TypeError):
                # If previous value is invalid, use the newly generated data
                pass

        value = json.dumps(spending_data)
        description = "Year-to-date spending by category (dollars)"

    else:  # OTHER or fallback
        # Generic value
        value = str(random.randint(0, 1000))
        description = "Other account information"

    return value, previous_value, description
