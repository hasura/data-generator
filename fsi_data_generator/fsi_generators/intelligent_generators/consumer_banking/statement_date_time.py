from .enums import StatementDateType
from data_generator import DataGenerator, SkipRowGenerationError
from datetime import datetime, timedelta
from typing import Any, Dict

import random


def generate_random_statement_date_time(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random statement date time with plausible values.

    Args:
        id_fields: Dictionary containing the required ID fields
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated statement date time data
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
            SELECT s.consumer_banking_statement_id, s.start_date_time, s.end_date_time, s.creation_date_time
            FROM consumer_banking.statements s
            WHERE s.consumer_banking_statement_id = %s
        """, (id_fields['consumer_banking_statement_id'],))

        statement = cursor.fetchone()

        if not statement:
            raise ValueError(f"No statement found with ID {id_fields['consumer_banking_statement_id']}")

        # Extract statement dates for reference
        start_date = statement.get('start_date_time')
        end_date = statement.get('end_date_time')
        creation_date = statement.get('creation_date_time')

        # Determine date type
        date_type = StatementDateType.get_random()

        # Generate a plausible date based on the type and statement dates
        date_time = None
        is_estimated = False
        description = None

        if date_type == StatementDateType.STATEMENT_DATE:
            date_time = creation_date
            description = "Date statement was generated"

        elif date_type == StatementDateType.CYCLE_START_DATE:
            date_time = start_date
            description = "Billing cycle start date"

        elif date_type == StatementDateType.CLOSE_DATE:
            date_time = end_date
            description = "Billing cycle close date"

        elif date_type == StatementDateType.DUE_DATE:
            # Due date is typically 21-25 days after statement date
            days_to_add = random.randint(21, 25)
            date_time = creation_date + timedelta(days=days_to_add)
            description = "Payment due date"

        elif date_type == StatementDateType.PAYMENT_CUTOFF_DATE:
            # Payment cutoff is usually the due date at a specific time
            days_to_add = random.randint(21, 25)
            date_time = creation_date + timedelta(days=days_to_add)
            date_time = date_time.replace(hour=17, minute=0, second=0)  # 5:00 PM cutoff
            description = "Payment must be received by this time"

        elif date_type == StatementDateType.NEXT_STATEMENT_DATE:
            # Next statement is typically generated every 30 days
            date_time = creation_date + timedelta(days=30)
            is_estimated = True
            description = "Estimated next statement date"

        elif date_type == StatementDateType.MINIMUM_PAYMENT_DATE:
            # Same as due date
            days_to_add = random.randint(21, 25)
            date_time = creation_date + timedelta(days=days_to_add)
            description = "Minimum payment due date"

        elif date_type == StatementDateType.GRACE_PERIOD_END:
            # Grace period typically ends on the due date
            days_to_add = random.randint(21, 25)
            date_time = creation_date + timedelta(days=days_to_add)
            description = "Interest-free grace period end date"

        elif date_type == StatementDateType.LATE_FEE_DATE:
            # Late fees typically assessed the day after due date
            days_to_add = random.randint(21, 25) + 1
            date_time = creation_date + timedelta(days=days_to_add)
            description = "Late fees will be assessed after this date"

        elif date_type == StatementDateType.LAST_PAYMENT_DATE:
            # Last payment typically within the statement period
            days_since_start = (end_date - start_date).days
            if days_since_start <= 0:
                raise SkipRowGenerationError
            random_days = random.randint(0, days_since_start)
            date_time = start_date + timedelta(days=random_days)
            description = "Date last payment was received"

        elif date_type == StatementDateType.OTHER:
            # Some other arbitrary date
            date_time = creation_date + timedelta(days=random.randint(-30, 30))
            description = random.choice([
                "Account review date",
                "Interest rate change notice",
                "Promotional offer expiration",
                "Credit limit evaluation",
                "Annual account assessment"
            ])
            is_estimated = random.random() < 0.5  # 50% chance of being estimated

        # Create the statement date time dictionary
        statement_date_time = {
            "consumer_banking_statement_id": id_fields['consumer_banking_statement_id'],
            "date_time": date_time,
            "type": date_type.value,
            "description": description,
            "is_estimated": is_estimated,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }

        return statement_date_time

    finally:
        cursor.close()
