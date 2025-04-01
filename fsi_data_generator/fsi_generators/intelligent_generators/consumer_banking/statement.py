from .enums import StatementType
from data_generator import DataGenerator
from datetime import datetime, timedelta, timezone
from dateutil.relativedelta import relativedelta
from typing import Any, Dict

import random

cycle_cut_day = random.randint(1, 28)


def generate_random_statement(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random account statement with plausible values.
    Args:
        id_fields: Dictionary containing the required ID fields
        dg: DataGenerator instance
    Returns:
        Dictionary containing randomly generated statement data
    """
    # Get database connection
    conn = dg.conn

    # Validate required fields
    if 'consumer_banking_account_id' not in id_fields:
        raise ValueError("consumer_banking_account_id is required")

    # Fetch the account to verify it exists
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT a.consumer_banking_account_id, a.status, a.opened_date
            FROM consumer_banking.accounts a
            WHERE a.consumer_banking_account_id = %s
        """, (id_fields['consumer_banking_account_id'],))
        account = cursor.fetchone()

        if not account:
            raise ValueError(f"No account found with ID {id_fields['consumer_banking_account_id']}")

        account_opened_date = account.get('opened_date')
        global cycle_cut_day
        now = datetime.now(tz=timezone.utc)

        # Find the most recent and earliest statement dates for this account
        cursor.execute("""
            SELECT MAX(end_date_time) as most_recent_statement_end,
                   MIN(start_date_time) as earliest_statement_start
            FROM consumer_banking.statements
            WHERE consumer_banking_account_id = %s
        """, (id_fields['consumer_banking_account_id'],))
        statement_result = cursor.fetchone()

        most_recent_statement_end = statement_result.get('most_recent_statement_end')
        earliest_statement_start = statement_result.get('earliest_statement_start')

        # Randomly select a statement type
        statement_type = StatementType.get_random()

        # Initialize start_date_time and end_date_time
        start_date_time = None
        end_date_time = None

        if most_recent_statement_end:
            # We already have statements for this account
            # Determine if there's a significant gap to fill
            cursor.execute("""
                SELECT end_date_time
                FROM consumer_banking.statements
                WHERE consumer_banking_account_id = %s
                ORDER BY end_date_time DESC
                LIMIT 1 OFFSET 1
            """, (id_fields['consumer_banking_account_id'],))
            second_most_recent = cursor.fetchone()

            if second_most_recent:
                second_most_recent_end = second_most_recent.get('end_date_time')
                gap_days = (most_recent_statement_end - second_most_recent_end).days - 1

                if gap_days > 35:  # Fill the gap if the period is too long
                    start_date_time = second_most_recent_end + timedelta(days=1)
                    end_date_time = calculate_statement_end_date(start_date_time, most_recent_statement_end)
                else:
                    # Go back further if not filling the gap
                    start_date_time, end_date_time = generate_prior_statement(
                        earliest_statement_start, account_opened_date
                    )
            else:
                # Only one statement exists, generate the previous one
                end_date_time = most_recent_statement_end - timedelta(days=1)
                start_date_time = end_date_time - timedelta(days=30)

                if account_opened_date and start_date_time < account_opened_date:
                    start_date_time = account_opened_date
        else:
            # No statements exist yet, generate the first statement
            if account_opened_date:
                start_date_time = account_opened_date
            else:
                start_date_time = now - timedelta(days=90)  # Default to 90 days ago

            end_date_time = calculate_statement_end_date(start_date_time, now)

        # Special handling for statement types
        if statement_type == StatementType.ANNUAL and random.random() < 0.8:
            year = start_date_time.year
            start_date_time = datetime(year, 1, 1, tzinfo=timezone.utc)
            end_date_time = datetime(year, 12, 31, 23, 59, 59, tzinfo=timezone.utc)
        elif statement_type == StatementType.TAX and random.random() < 0.9:
            year = start_date_time.year
            start_date_time = datetime(year, 1, 1, tzinfo=timezone.utc)
            end_date_time = datetime(year, 12, 31, 23, 59, 59, tzinfo=timezone.utc)

        # Creation date is shortly after end_date_time
        creation_date_time = (end_date_time + timedelta(days=random.randint(1, 3))).replace(tzinfo=timezone.utc)
        if creation_date_time > now:
            creation_date_time = now

        # Generate the statement reference number
        year_month = end_date_time.strftime("%Y%m")
        statement_sequence = random.randint(1, 999999)
        statement_reference = f"STM-{year_month}-{statement_sequence:06d}"

        # Build and return the statement dictionary
        statement = {
            "consumer_banking_account_id": id_fields['consumer_banking_account_id'],
            "statement_reference": statement_reference,
            "type": statement_type.value,
            "start_date_time": start_date_time,
            "end_date_time": end_date_time,
            "creation_date_time": creation_date_time
        }
        return statement

    finally:
        cursor.close()


def calculate_statement_end_date(start_date_time: datetime, max_end_date: datetime) -> datetime:
    """
    Calculate the appropriate statement end date.
    """
    global cycle_cut_day
    next_month = start_date_time + relativedelta(months=1)
    month_end = next_month.replace(day=1) - timedelta(days=1)

    if cycle_cut_day <= month_end.day:
        end_date = month_end.replace(day=cycle_cut_day)
    else:
        end_date = month_end

    end_date_time = datetime.combine(end_date, datetime.max.time()).replace(tzinfo=timezone.utc)

    # Ensure the end date does not surpass max_end_date
    return min(end_date_time, max_end_date)


def generate_prior_statement(earliest_statement_start: datetime, account_opened_date: datetime):
    """
    Generate a statement that precedes the earliest existing statement.
    """
    if earliest_statement_start and account_opened_date:
        gap_days = (earliest_statement_start - account_opened_date).days
        if gap_days > 5:  # Requires a gap of at least 5 days
            end_date_time = earliest_statement_start - timedelta(days=1)
            start_date_time = max(end_date_time - timedelta(days=30), account_opened_date)
            return start_date_time, end_date_time

    # Default fallback for very early statements
    end_date_time = datetime.now(tz=timezone.utc) - timedelta(days=90)
    start_date_time = end_date_time - timedelta(days=30)
    return start_date_time, end_date_time
