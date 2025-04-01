from .today import today
from ..enterprise.enums import Frequency
from .enums import StatementFormat, CommunicationMethod, AccountStatus
from data_generator import DataGenerator
from typing import Any, Dict

import random
import datetime
from dateutil.relativedelta import relativedelta


def generate_random_account_statement_preference(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate random account statement preferences with plausible values.

    Args:
        id_fields: Dictionary containing the required ID fields
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated account statement preferences data
    """
    # Get database connection
    conn = dg.conn

    # Validate required fields
    if 'consumer_banking_account_id' not in id_fields:
        raise ValueError("consumer_banking_account_id is required")

    # Fetch the consumer banking account to verify it exists and get its status
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT a.consumer_banking_account_id, a.opened_date, a.status, a.status_update_date_time
            FROM consumer_banking.accounts a
            WHERE a.consumer_banking_account_id = %s
        """, (id_fields['consumer_banking_account_id'],))

        account = cursor.fetchone()

        if not account:
            raise ValueError(f"No account found with ID {id_fields['consumer_banking_account_id']}")

        account_status = AccountStatus(account['status'])
        opened_date = account['opened_date']
        status_update_date = account['status_update_date_time']

        # Determine statement frequency based on account status
        if account_status in [AccountStatus.ACTIVE, AccountStatus.INACTIVE]:
            # Active accounts have normal statement frequencies
            frequency = Frequency.get_random()
            # Bias towards more common frequencies
            frequency_weights = {
                Frequency.DAILY: 0.05,
                Frequency.WEEKLY: 0.1,
                Frequency.BI_WEEKLY: 0.1,
                Frequency.SEMI_MONTHLY: 0.1,
                Frequency.MONTHLY: 0.5,  # Most common
                Frequency.QUARTERLY: 0.1,
                Frequency.SEMI_ANNUALLY: 0.03,
                Frequency.ANNUALLY: 0.02
            }

            if random.random() > frequency_weights.get(frequency, 0.5):
                frequency = Frequency.MONTHLY  # Default to monthly if random check fails
        elif account_status in [AccountStatus.DORMANT, AccountStatus.SUSPENDED]:
            # Dormant accounts typically have less frequent statements
            frequencies = [Frequency.QUARTERLY, Frequency.SEMI_ANNUALLY, Frequency.ANNUALLY]
            frequency = random.choice(frequencies)
        elif account_status in [AccountStatus.CLOSED, AccountStatus.ARCHIVED]:
            # Closed accounts don't get new statements, but keep their frequency setting
            frequency = Frequency.MONTHLY  # Default setting
        else:
            # Default for other statuses
            frequency = Frequency.MONTHLY

        # Determine statement format - same for all account statuses
        statement_format = StatementFormat.get_random()

        # Determine communication method - for closed accounts, might bias toward digital
        if account_status in [AccountStatus.CLOSED, AccountStatus.ARCHIVED]:
            # Closed accounts more likely to have digital delivery
            methods = [CommunicationMethod.EMAIL, CommunicationMethod.PORTAL,
                       CommunicationMethod.EMAIL, CommunicationMethod.PORTAL]  # Double weighting
            communication_method = random.choice(methods)
        else:
            communication_method = CommunicationMethod.get_random()

        # For physical mail, we need an address
        enterprise_address_id = None
        if communication_method == CommunicationMethod.MAIL or communication_method == CommunicationMethod.MULTIPLE:
            # Look up or assign an address
            cursor.execute("""
                SELECT ea.enterprise_address_id
                FROM enterprise.party_entity_addresses pea
                JOIN enterprise.account_ownership ao ON pea.enterprise_party_id = ao.enterprise_party_id
                JOIN consumer_banking.accounts a ON ao.enterprise_account_id = a.enterprise_account_id
                JOIN enterprise.addresses ea ON pea.enterprise_address_id = ea.enterprise_address_id
                WHERE a.consumer_banking_account_id = %s
                LIMIT 1
            """, (id_fields['consumer_banking_account_id'],))

            address_record = cursor.fetchone()
            if address_record:
                enterprise_address_id = address_record['enterprise_address_id']

        # Calculate a plausible next statement date and last statement date based on account status
        next_statement_date = None
        last_statement_date = None

        # Look up most recent statement for this account
        cursor.execute("""
            SELECT MAX(end_date_time) as last_statement_date
            FROM consumer_banking.statements
            WHERE consumer_banking_account_id = %s
        """, (id_fields['consumer_banking_account_id'],))

        result = cursor.fetchone()

        if result and result['last_statement_date']:
            last_statement_date = result['last_statement_date']
        else:
            # If no statements found, set a plausible last statement date
            if account_status in [AccountStatus.CLOSED, AccountStatus.ARCHIVED]:
                # For closed accounts, last statement was likely around closure date
                if status_update_date:
                    last_statement_date = status_update_date.date()
                else:
                    # Default to a random date between open date and today
                    days_open = (today - opened_date).days
                    if days_open > 0:
                        last_statement_date = opened_date + datetime.timedelta(days=random.randint(1, days_open))
                    else:
                        last_statement_date = opened_date
            else:
                # For active accounts, last statement was recent
                # Calculate based on monthly cycle typically
                current_month_start = datetime.date(today.year, today.month, 1)
                last_month_start = current_month_start - relativedelta(months=1)
                statement_day = random.randint(10, 28)  # Most statements come mid-month to end-month

                if today.day >= statement_day:
                    # This month's statement has been generated
                    last_statement_date = datetime.date(today.year, today.month, statement_day)
                else:
                    # Last month's statement is the most recent
                    last_month_days = (current_month_start - datetime.timedelta(days=1)).day
                    last_statement_date = datetime.date(
                        last_month_start.year,
                        last_month_start.month,
                        min(statement_day, last_month_days)
                    )

                # Ensure last statement date isn't before account opened
                if last_statement_date < opened_date:
                    last_statement_date = opened_date + datetime.timedelta(days=30)

        # Calculate next statement date based on frequency and account status
        if account_status in [AccountStatus.CLOSED, AccountStatus.ARCHIVED]:
            # No more statements for closed accounts
            next_statement_date = None
        elif last_statement_date:
            # Calculate next date based on frequency and last date
            if frequency == Frequency.DAILY:
                next_statement_date = last_statement_date + datetime.timedelta(days=1)
            elif frequency == Frequency.WEEKLY:
                next_statement_date = last_statement_date + datetime.timedelta(weeks=1)
            elif frequency == Frequency.BI_WEEKLY:
                next_statement_date = last_statement_date + datetime.timedelta(weeks=2)
            elif frequency == Frequency.SEMI_MONTHLY:
                # Two statements per month, typically 15th and last day
                if last_statement_date.day < 15:
                    next_statement_date = datetime.date(last_statement_date.year, last_statement_date.month, 15)
                else:
                    # Last day of the month
                    next_month = last_statement_date.replace(day=28) + datetime.timedelta(days=4)
                    next_statement_date = next_month - datetime.timedelta(days=next_month.day)
            elif frequency == Frequency.MONTHLY:
                next_statement_date = last_statement_date + relativedelta(months=1)
            elif frequency == Frequency.QUARTERLY:
                next_statement_date = last_statement_date + relativedelta(months=3)
            elif frequency == Frequency.SEMI_ANNUALLY:
                next_statement_date = last_statement_date + relativedelta(months=6)
            elif frequency == Frequency.ANNUALLY:
                next_statement_date = last_statement_date + relativedelta(years=1)
            else:
                # Default to monthly for other frequencies
                next_statement_date = last_statement_date + relativedelta(months=1)

            # For dormant accounts, only generate next date if it's within a year
            if account_status == AccountStatus.DORMANT and (next_statement_date - today).days > 365:
                next_statement_date = None

        # Create the account statement preferences record
        preferences = {
            "consumer_banking_account_id": id_fields['consumer_banking_account_id'],
            "frequency": frequency.value,
            "format": statement_format.value,
            "communication_method": communication_method.value,
            "next_statement_date": next_statement_date,
            "last_statement_date": last_statement_date,
            "enterprise_address_id": enterprise_address_id
        }

        return preferences

    finally:
        cursor.close()
