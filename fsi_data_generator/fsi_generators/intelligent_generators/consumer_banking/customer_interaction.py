from ..enterprise.enums import Frequency
from .enums import (InteractionChannel, InteractionPriority, InteractionStatus,
                    InteractionType)
from data_generator import DataGenerator
from typing import Any, Dict

import datetime
import pytz
import random


def generate_random_customer_interaction(id_fields: Dict[str, Any], dg: DataGenerator) -> Dict[str, Any]:
    """
    Generate a random customer interaction with plausible values.

    Args:
        id_fields: Dictionary containing the required ID fields
        dg: DataGenerator instance

    Returns:
        Dictionary containing randomly generated customer interaction data
    """
    # Get database connection
    conn = dg.conn

    # Validate required fields
    if 'customer_id' not in id_fields:
        raise ValueError("customer_id is required")

    # Fetch the customer to verify it exists
    cursor = conn.cursor()
    try:
        cursor.execute("""
            SELECT enterprise_party_id, name
            FROM enterprise.parties
            WHERE enterprise_party_id = %s
        """, (id_fields['customer_id'],))

        customer = cursor.fetchone()

        if not customer:
            raise ValueError(f"No customer found with ID {id_fields['customer_id']}")

        # Determine if this interaction is related to a specific account
        account_id = id_fields.get('account_id')
        if account_id and not random.random() < 0.7:  # 70% chance to be account-related if not specified
            account_id = None

        # Determine if this is an automated interaction or handled by an associate
        enterprise_associate_id = id_fields.get('enterprise_associate_id')
        if enterprise_associate_id and not random.random() < 0.9:  # 90% chance to have an associate if not specified
            enterprise_associate_id = None

        # Determine the interaction type and ensure channel is consistent
        interaction_type = InteractionType.get_random()

        # Match channel to type
        if interaction_type == InteractionType.PHONE_CALL:
            channel = InteractionChannel.PHONE
        elif interaction_type == InteractionType.EMAIL:
            channel = InteractionChannel.EMAIL
        elif interaction_type == InteractionType.CHAT:
            channel = random.choice([InteractionChannel.WEB, InteractionChannel.MOBILE_APP])
        elif interaction_type == InteractionType.IN_PERSON:
            channel = InteractionChannel.BRANCH
        elif interaction_type == InteractionType.VIDEO_CALL:
            channel = InteractionChannel.VIDEO
        elif interaction_type == InteractionType.ONLINE_FORM:
            channel = InteractionChannel.WEB
        elif interaction_type == InteractionType.SOCIAL_MEDIA:
            channel = InteractionChannel.SOCIAL_MEDIA
        elif interaction_type == InteractionType.ATM_INTERACTION:
            channel = InteractionChannel.ATM
        elif interaction_type == InteractionType.MOBILE_APP:
            channel = InteractionChannel.MOBILE_APP
        elif interaction_type == InteractionType.MAIL:
            channel = InteractionChannel.MAIL
        elif interaction_type == InteractionType.SMS:
            channel = InteractionChannel.SMS
        elif interaction_type == InteractionType.FAX:
            channel = InteractionChannel.PHONE  # FAX typically goes through phone lines
        else:
            channel = InteractionChannel.get_random()

        # Generate a plausible interaction date and time
        # Most interactions occur during business hours
        utc = pytz.UTC
        now = datetime.datetime.now(utc)

        # Generate a date within the last 90 days
        days_ago = random.randint(0, 90)
        interaction_date = now - datetime.timedelta(days=days_ago)

        # Adjust time to be during business hours (9 AM to 5 PM) on weekdays
        if interaction_date.weekday() >= 5:  # Weekend
            # Move to previous Friday or following Monday
            if random.random() < 0.5:
                # Previous Friday
                days_to_adjust = interaction_date.weekday() - 4
                interaction_date = interaction_date - datetime.timedelta(days=days_to_adjust)
            else:
                # Following Monday
                days_to_adjust = 7 - interaction_date.weekday()
                interaction_date = interaction_date + datetime.timedelta(days=days_to_adjust)

        # Adjust to business hours
        hour = random.randint(9, 17)  # 9 AM to 5 PM
        minute = random.randint(0, 59)
        second = random.randint(0, 59)

        interaction_date_time = interaction_date.replace(hour=hour, minute=minute, second=second)

        # For non-business hours channels (ATM, WEB, MOBILE_APP), potentially use any time
        if channel in [InteractionChannel.ATM, InteractionChannel.WEB, InteractionChannel.MOBILE_APP]:
            if random.random() < 0.3:  # 30% chance of non-business hours
                hour = random.randint(0, 23)  # Any hour
                interaction_date_time = interaction_date.replace(hour=hour, minute=minute, second=second)

        # Determine interaction status based on how recent it is
        # Recent interactions more likely to be open
        if days_ago < 3:
            status_weights = {
                InteractionStatus.OPEN: 0.4,
                InteractionStatus.PENDING: 0.3,
                InteractionStatus.IN_PROGRESS: 0.2,
                InteractionStatus.RESOLVED: 0.05,
                InteractionStatus.CLOSED: 0.05
            }
            status_choices = list(status_weights.keys())
            status_probabilities = [status_weights[s] for s in status_choices]
            status = random.choices(status_choices, weights=status_probabilities, k=1)[0]
        elif days_ago < 7:
            status_weights = {
                InteractionStatus.OPEN: 0.2,
                InteractionStatus.PENDING: 0.2,
                InteractionStatus.IN_PROGRESS: 0.3,
                InteractionStatus.RESOLVED: 0.15,
                InteractionStatus.CLOSED: 0.15
            }
            status_choices = list(status_weights.keys())
            status_probabilities = [status_weights[s] for s in status_choices]
            status = random.choices(status_choices, weights=status_probabilities, k=1)[0]
        else:
            # Older interactions more likely to be resolved
            status_weights = {
                InteractionStatus.OPEN: 0.05,
                InteractionStatus.PENDING: 0.05,
                InteractionStatus.IN_PROGRESS: 0.1,
                InteractionStatus.RESOLVED: 0.3,
                InteractionStatus.CLOSED: 0.5
            }
            status_choices = list(status_weights.keys())
            status_probabilities = [status_weights[s] for s in status_choices]
            status = random.choices(status_choices, weights=status_probabilities, k=1)[0]

        # If escalated or transferred, adjust timing
        if random.random() < 0.1:  # 10% chance of being escalated/transferred
            if random.random() < 0.5:
                status = InteractionStatus.ESCALATED
            else:
                status = InteractionStatus.TRANSFERRED

        # Special case for some older interactions being reopened
        if days_ago > 30 and random.random() < 0.05:  # 5% of older interactions
            status = InteractionStatus.REOPENED

        # Generate a priority level
        # Critical or high priority for certain channels or transaction-related
        if channel in [InteractionChannel.PHONE, InteractionChannel.BRANCH,
                       InteractionChannel.VIDEO] and random.random() < 0.2:
            priority = random.choice([InteractionPriority.CRITICAL, InteractionPriority.HIGH])
        else:
            priority = InteractionPriority.get_random()

        # For resolved/closed interactions, set a resolution
        resolution = None
        if status in [InteractionStatus.RESOLVED, InteractionStatus.CLOSED]:
            resolutions = [
                "Issue was resolved to customer's satisfaction.",
                "Provided the requested information.",
                "Updated account settings as requested.",
                "Transaction was processed successfully.",
                "Explained bank policy and customer understood.",
                "Fee was refunded as a one-time courtesy.",
                "Document was sent to customer via requested method.",
                "Customer's concern was addressed and they were satisfied with the outcome.",
                "Issue was escalated and resolved by a specialist.",
                "No further action required."
            ]
            resolution = random.choice(resolutions)

        # Set a realistic subject
        if account_id:
            # Account-related subjects
            subjects = [
                f"Account balance inquiry",
                f"Transaction dispute",
                f"Statement question",
                f"Fee inquiry",
                f"Direct deposit setup",
                f"Online banking access",
                f"Debit card issue",
                f"Change of address",
                f"Account preferences update",
                f"Automatic payment setup"
            ]
        else:
            # General subjects
            subjects = [
                "Product information request",
                "New account inquiry",
                "Branch location question",
                "General services question",
                "Banking hours inquiry",
                "Financial advice request",
                "Contact information update",
                "Mobile app technical issue",
                "Website technical issue",
                "Feedback on services"
            ]

        subject = random.choice(subjects)

        # Generate a description based on subject and type
        description = f"Customer {interaction_type.name.lower().replace('_', ' ')} regarding {subject.lower()}."

        # Look for a related transaction if account-related and 30% chance
        related_transaction_id = None
        if account_id and not random.random() < 0.3:
            related_transaction_id = None

        # Set creation and update times
        created_at = interaction_date_time
        updated_at = created_at

        # For interactions that have progressed (not OPEN), add some time for updates
        if status != InteractionStatus.OPEN:
            hours_passed = random.randint(1, 48)
            updated_at = created_at + datetime.timedelta(hours=hours_passed)
            if updated_at > now:
                updated_at = now

        # Create the customer interaction dictionary
        interaction = {
            "customer_id": id_fields['customer_id'],
            "account_id": account_id,
            "enterprise_associate_id": enterprise_associate_id,
            "interaction_type": interaction_type.value,
            "interaction_date_time": interaction_date_time,
            "channel": channel.value,
            "subject": subject,
            "description": description,
            "resolution": resolution,
            "status": status.value,
            "priority": priority.value if random.random() < 0.8 else None,  # 80% have priority set
            "related_transaction_id": related_transaction_id,
            "created_at": created_at,
            "updated_at": updated_at
        }

        return interaction

    finally:
        cursor.close()
